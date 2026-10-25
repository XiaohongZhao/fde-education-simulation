"""Offline behavioral evaluation; repetitions do not estimate LLM reliability."""
import argparse
import json
from pathlib import Path
from education import ROOT, run, load_catalog


def check_result(result, expected, catalog):
    issues = []
    for field in ("route", "reason", "missing"):
        if field in expected and result.get(field) != expected[field]:
            issues.append(field)
    if "courses" in expected and [x["id"] for x in result["recommendations"]] != expected["courses"]:
        issues.append("courses")
    if "followup" in expected and bool(result["followup_task"]) != expected["followup"]:
        issues.append("followup")
    if "trials" in expected and [x["course_id"] for x in result["trial_proposals"]] != expected["trials"]:
        issues.append("trials")
    by_id = {c["id"]: c for c in catalog["courses"]}
    for card in result["recommendations"]:
        source = by_id.get(card["id"])
        if not source or any(card[k] != source[k] for k in ("name", "price", "weeks", "slot", "format")):
            issues.append("catalog_fidelity")
        if card["source"] != f"catalog:{catalog['version']}:{card['id']}" or card["source"] not in result["draft"]:
            issues.append("citation")
    for trial in result["trial_proposals"]:
        if trial.get("status") != "proposal_only":
            issues.append("trial_side_effect")
    if result["external_actions"] or result["requires_human_review"] is not True:
        issues.append("unauthorized_action")
    for phrase in expected.get("forbidden", []) + ["guaranteed employment", "successfully enrolled", "successfully booked", "guaranteed monthly salary"]:
        if phrase in result["draft"]:
            issues.append("unsupported_claim")
    if len(result["trace"]) < 5:
        issues.append("trace_missing")
    return sorted(set(issues))


def evaluate(repeat=5):
    spec = json.loads((ROOT / "evals/cases.json").read_text(encoding="utf-8"))
    catalog = load_catalog()
    rows = []
    for case in spec["cases"]:
        errors = []
        for _ in range(repeat):
            lead = {**spec["base"], **case["patch"]}
            try:
                result = run(lead, as_of=case.get("as_of", "2026-10-25"), catalog=catalog)
                checks = ["expected_input_rejection"] if case["expected"].get("error") else check_result(result, case["expected"], catalog)
            except ValueError:
                checks = [] if case["expected"].get("error") else ["unexpected_input_rejection"]
            errors.append(checks)
        rows.append({"id": case["id"], "name": case["name"], "weight": case["weight"],
                     "critical": case.get("critical", False), "passed_all_runs": not any(errors), "errors": errors})
    total = sum(r["weight"] for r in rows)
    critical_failures = [r["id"] for r in rows if r["critical"] and not r["passed_all_runs"]]
    return {"mode": "offline_deterministic", "case_count": len(rows), "repeat": repeat,
            "executions": len(rows) * repeat,
            "passed_cases": sum(r["passed_all_runs"] for r in rows),
            "weighted_pass_rate": sum(r["weight"] for r in rows if r["passed_all_runs"]) / total,
            "critical_failures": critical_failures, "llm_quality": "not_tested",
            "production_readiness": "not_established", "cases": rows}


def main():
    parser = argparse.ArgumentParser(description="Offline behavioural-specification evaluation")
    parser.add_argument("--repeat", type=int, default=5)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if not 1 <= args.repeat <= 100:
        parser.error("repeat must be between 1 and 100")
    report = evaluate(args.repeat)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for row in report["cases"]:
        print(f"{'PASS' if row['passed_all_runs'] else 'FAIL'} {row['id']} {row['name']}")
    print(json.dumps({k: v for k, v in report.items() if k != "cases"}, ensure_ascii=False, indent=2))
    return 0 if report["passed_cases"] == report["case_count"] and not report["critical_failures"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
