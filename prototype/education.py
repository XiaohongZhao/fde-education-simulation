"""Adult-training FDE simulation. Standard library only; no external writes."""
from __future__ import annotations

import hashlib
import json
import math
import os
from datetime import date, datetime
from pathlib import Path
from urllib import request, error

ROOT = Path(__file__).resolve().parent
REQUIRED = ("age", "goal", "budget", "level", "availability", "format")
ALLOWED = {"id", "age", "goal", "budget", "level", "availability", "format",
           "consent_followup", "intent", "message", "requested_course", "opt_out"}
INTENTS = {"consult", "trial", "enroll", "refund", "job_guarantee"}


def load_catalog():
    return json.loads((ROOT / "data/catalog.json").read_text(encoding="utf-8"))


def validate_input(lead):
    if not isinstance(lead, dict):
        raise ValueError("Input must be a JSON object")
    if set(lead) - ALLOWED:
        raise ValueError("Unsupported input fields; use the fields shown in data/examples.json")
    for key in ("id", "goal", "format", "intent", "message", "requested_course"):
        if key in lead and lead[key] is not None and not isinstance(lead[key], str):
            raise ValueError(f"{key} must be a string")
    for key in ("age", "level"):
        value = lead.get(key)
        if value is not None and (type(value) is not int or value < 0):
            raise ValueError(f"{key} must be a non-negative integer")
    if lead.get("age") is not None and lead["age"] > 120:
        raise ValueError("age is outside the supported range")
    if lead.get("level") is not None and lead["level"] > 2:
        raise ValueError("level must be 0, 1 or 2")
    budget = lead.get("budget")
    if budget is not None and (type(budget) not in (int, float) or not math.isfinite(budget) or budget < 0):
        raise ValueError("budget must be a finite non-negative number")
    for key in ("consent_followup", "opt_out"):
        if key in lead and type(lead[key]) is not bool:
            raise ValueError(f"{key} must be a boolean")
    slots = lead.get("availability")
    if slots is not None and (not isinstance(slots, list) or any(not isinstance(x, str) for x in slots)):
        raise ValueError("availability must be a list of strings")
    if lead.get("intent", "consult") not in INTENTS:
        raise ValueError("intent is not supported")
    if len(lead.get("message") or "") > 8000:
        raise ValueError("message exceeds 8,000 characters")


def validate_catalog(catalog):
    if not isinstance(catalog, dict) or not catalog.get("version"):
        raise ValueError("Catalogue version is missing")
    start, end = date.fromisoformat(catalog["valid_from"]), date.fromisoformat(catalog["valid_until"])
    if start > end:
        raise ValueError("Invalid catalogue validity period")
    ids = set()
    for course in catalog["courses"]:
        if course["id"] in ids:
            raise ValueError("Duplicate course ID")
        ids.add(course["id"])
        if type(course["price"]) is not int or course["price"] < 0:
            raise ValueError("Invalid course price")
        if type(course["seats"]) is not int or course["seats"] < 0:
            raise ValueError("Invalid course capacity")
        if course["level_min"] > course["level_max"]:
            raise ValueError("Invalid course-level range")
        datetime.fromisoformat(course["trial_at"])


def matches(lead, course):
    return (course["active"] and course["seats"] > 0
            and lead["goal"] in course["goals"]
            and lead["budget"] >= course["price"]
            and course["level_min"] <= lead["level"] <= course["level_max"]
            and course["slot"] in lead["availability"]
            and lead["format"] in ("any", course["format"]))


def draft_text(result):
    reason = result["reason"]
    if result["route"] == "clarify":
        labels = {"age": "age", "goal": "learning goal", "budget": "budget ceiling", "level": "current skill level",
                  "availability": "available class times", "format": "online or in-person preference"}
        text = "Please provide: " + ", ".join(labels[x] for x in result["missing"]) + ". We can then check suitable courses."
    elif result["route"] == "recommend":
        lines = [f"Based on the confirmed information, consider these courses (catalogue {result['catalog_version']}):"]
        for course in result["recommendations"]:
            lines.append(f"{course['name']}: CNY {course['price']}, {course['weeks']} weeks, "
                         f"{course['slot']}, {course['format']}. [{course['source']}]")
        lines.append("This is course advice, not confirmation of enrolment or a promise of employment outcomes.")
        if result["trial_proposals"]:
            lines.append("Trial times for human confirmation: " + "; ".join(
                x["course_id"] + " " + x["trial_at"] for x in result["trial_proposals"]) + "; no booking has been made.")
        text = "\n".join(lines)
    else:
        texts = {
            "minor": "This case serves adults only. A person must confirm the service scope for this enquiry.",
            "refund": "Refunds require a person to check the order, contract and attendance. No amount or payment date is determined here.",
            "job_guarantee": "The courses do not guarantee employment, salary or admission outcomes. An adviser should explain these expectations.",
            "enrollment": "Enrolment requires a person to check capacity, the contract and payment status. No enrolment or payment has been completed here.",
            "stale_catalog": "The catalogue is outside its validity period. A person must update and confirm prices and schedules.",
            "conflicting_request": "The requested course conflicts with confirmed goals, budget or availability. An adviser should check before selecting a course.",
            "no_match": "No current course satisfies the goal, budget, prior knowledge and timing together. Please discuss alternatives with an adviser.",
        }
        text = texts[reason]
    if result["followup_task"]:
        text += "\nA follow-up task draft is ready for adviser review. No message has been sent."
    return text


def run(lead, *, as_of=None, catalog=None):
    validate_input(lead)
    catalog = load_catalog() if catalog is None else catalog
    validate_catalog(catalog)
    today = date.fromisoformat(as_of) if as_of else date.today()
    missing = [key for key in REQUIRED if lead.get(key) is None or lead.get(key) == "" or lead.get(key) == []]
    trace = [{"stage": "intake", "missing": missing,
              "note": "Decisions use structured fields; message is for human reference only, without automated intent recognition"}]
    route, reason, selected = "human_review", "no_match", []
    # Escalations precede course matching. Message text cannot override the structured policy fields.
    if lead.get("age") is not None and lead["age"] < 18:
        reason = "minor"
    elif lead.get("intent") in {"refund", "job_guarantee", "enroll"}:
        reason = {"enroll": "enrollment"}.get(lead["intent"], lead["intent"])
    elif not (date.fromisoformat(catalog["valid_from"]) <= today <= date.fromisoformat(catalog["valid_until"])):
        reason = "stale_catalog"
    elif missing:
        route, reason = "clarify", "missing_fields"
    else:
        selected = sorted((c for c in catalog["courses"] if matches(lead, c)), key=lambda c: (c["price"], c["id"]))
        requested = lead.get("requested_course")
        if requested and requested not in {c["id"] for c in selected}:
            selected, reason = [], "conflicting_request"
        elif selected:
            if requested:
                selected = [c for c in selected if c["id"] == requested]
            route, reason = "recommend", "matched"
    trace.append({"stage": "match", "route": route, "reason": reason,
                  "selected": [c["id"] for c in selected], "catalog_version": catalog["version"]})
    cards = [{**{k: c[k] for k in ("id", "name", "price", "weeks", "slot", "format")},
              "source": f"catalog:{catalog['version']}:{c['id']}"} for c in selected]
    trials = []
    if lead.get("intent") == "trial" and route == "recommend":
        for course in selected:
            if datetime.fromisoformat(course["trial_at"]).date() > today:
                trials.append({"course_id": course["id"], "trial_at": course["trial_at"], "status": "proposal_only"})
    eligible = (lead.get("consent_followup") is True and not lead.get("opt_out", False)
                and route == "recommend" and lead.get("age", 0) >= 18)
    task = {"kind": "contact_after_trial" if trials else "course_consultation", "status": "draft", "owner": "Admissions adviser",
            "prerequisite": "actual_trial_attendance_and_contact_permission_confirmed" if trials else "contact_permission_reconfirmed"} if eligible else None
    result = {"mode": "offline", "as_of": today.isoformat(), "route": route, "reason": reason,
              "missing": missing, "catalog_version": catalog["version"], "recommendations": cards,
              "trial_proposals": trials, "followup_task": task, "requires_human_review": True,
              "external_actions": [], "llm": {"status": "not_requested"}}
    result["draft"] = draft_text(result)
    trace.extend([
        {"stage": "draft", "type": "deterministic_template", "sources": [c["source"] for c in cards]},
        {"stage": "policy", "followup_allowed": eligible, "external_write_enabled": False},
        {"stage": "audit", "review_required": True, "input_fingerprint": hashlib.sha256(
            json.dumps(lead, ensure_ascii=False, sort_keys=True).encode()).hexdigest()[:16]},
    ])
    result["trace"] = trace
    return result


def add_live_draft(result, *, opener=None):
    """Explicit opt-in only. LLM cannot change structured decisions or execute actions.

    The original message and learner ID are deliberately not sent to the API.
    Output is unverified text for a human reviewer, never an approved reply.
    """
    key, model = os.environ.get("ANTHROPIC_API_KEY"), os.environ.get("ANTHROPIC_MODEL")
    if not key or not model:
        raise ValueError("Live mode requires ANTHROPIC_API_KEY and ANTHROPIC_MODEL; no API request was made")
    payload = {"model": model, "max_tokens": 800,
               "system": "You draft text for adult-training advisers. Write a concise English reply using only the supplied facts. Do not add prices, discounts, employment promises or claims that a booking or payment is complete. Preserve source markers. Output is for human review.",
               "messages": [{"role": "user", "content": json.dumps({
                   "verified_template": result["draft"], "route": result["route"],
                   "recommendations": result["recommendations"]}, ensure_ascii=False)}]}
    req = request.Request("https://api.anthropic.com/v1/messages", data=json.dumps(payload).encode(),
                          headers={"Content-Type": "application/json", "x-api-key": key,
                                   "anthropic-version": "2023-06-01"}, method="POST")
    result["mode"] = "live_requested"
    try:
        with (opener or request.urlopen)(req, timeout=30) as response:
            data = json.loads(response.read())
        text = "\n".join(c["text"] for c in data.get("content", []) if c.get("type") == "text")
        if data.get("stop_reason") != "end_turn" or not text.strip():
            result["llm"] = {"status": "incomplete", "review_required": True}
        else:
            result["llm"] = {"status": "generated_unverified", "text": text,
                             "model": model, "review_required": True, "usage": data.get("usage", {})}
    except (error.URLError, TimeoutError, ValueError, KeyError, TypeError) as exc:
        # Do not echo request headers, API credentials, or provider response bodies.
        result["llm"] = {"status": "error", "error_type": type(exc).__name__, "fallback": "deterministic_template"}
    result["trace"].append({"stage": "llm_draft", "status": result["llm"]["status"], "approved_for_send": False})
    return result
