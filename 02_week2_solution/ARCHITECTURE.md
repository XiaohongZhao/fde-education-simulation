# Solution Architecture and Interfaces

## Initial delivery workflow

```text
Synthetic form / adviser-confirmed JSON
                  |
Intake: field types, missing information, adult scope and intent
                  |
Match: valid catalogue + goal + budget + level + time + mode + places
                  |
Draft: deterministic fact cards and template -> optional model draft
                  |
Policy: contact consent, escalation, proposal state and no external writes
                  |
Audit: sources, routing reasons and processing stages -> adviser review
```

These names describe responsibilities. The current implementation has five stages within one Python workflow. Multiple independent agents would not automatically improve it: the model drafts language, while explicit rules remain outside model judgement.

## Input contract

| Field | Meaning and values | Missing or invalid behaviour |
|---|---|---|
| age | Integer age; adults are at least 18 in this case | Missing: clarify; minor: human review |
| goal | data / automation / ai_office / design | Missing: clarify; unknown goal: no match |
| budget | Total tuition budget ceiling, a finite non-negative CNY amount | Missing: clarify; reject negative values, booleans and NaN |
| level | 0 beginner; 1 basic application skills; 2 proficient | Missing: clarify; reject out-of-range values |
| availability | Array containing weekend / weekday_evening | Empty: clarify; other slots do not match |
| format | online / offline / any | Missing: clarify; unknown value: no match |
| intent | consult / trial / enroll / refund / job_guarantee | Defaults to consult when omitted; reject unknown values |
| consent_followup | Explicit boolean; no consent by default | false or omitted: no follow-up task |
| opt_out | Whether consent has been withdrawn; defaults to false | true overrides historical consent |
| requested_course | Optional course ID | Human review if absent from the catalogue or incompatible with requirements |
| message | Optional original description, at most 8,000 characters | Human reference only; no automated intent recognition |

**The entry point depends on confirmed structured fields.** If a message says “do not contact me” but the form still says true, the programme does not understand that semantic conflict. An adviser must correct the field first. Free-text extraction, negation, changed preferences and multi-turn state synchronisation remain to be developed. C28 establishes only that message text cannot overwrite the catalogue, not that a model resists prompt injection.

## Output contract

- `route`: recommend / clarify / human_review.
- `recommendations`: course fact cards and source IDs, ordered by price and course ID rather than margin.
- `trial_proposals`: future-date trial proposals with status fixed at proposal_only. Same-day trials are conservatively excluded.
- `followup_task`: an adviser task draft created only when contact is permitted; it sends nothing.
- `draft`: template text with rule-controlled facts.
- `llm`: optional model text and an explicit status. It does not overwrite `draft` or structured fact cards.
- `trace`: missing fields, routing reasons, catalogue version, sources and review requirements; no names or contact details.
- `external_actions`: always empty; `requires_human_review`: always true.

## External integration boundaries

| Boundary | Prototype behaviour | Decisions needed before real integration |
|---|---|---|
| Course source | Local JSON snapshot | Publishing authority, version, validity and update frequency |
| Trial confirmation | Proposals only | Current places, concurrent reservations, duplicate requests, cancellation and rescheduling |
| Contact tasks | Local drafts | Consent purpose and channel, withdrawal synchronisation, frequency limits and human confirmation |
| Payments and refunds | Human review | Order state, contract version, review authority and service receipts |
| Model | Optional single API call for drafting | Output review, failure rates, cost, timeout and provider availability |

## Rationale

Course-selection errors can be reproduced using explicit fields, so rules handle selection. A model may help with wording, but the system supplies facts and action states. Keeping unverified model text in a separate field makes it possible to test whether the model actually reduces editing effort, rather than allowing fluent language to conceal errors.

The prototype prioritises inspectability. Document retrieval, chat intent recognition, CRM write-back and background task queues each need their own design and validation; they are not part of the implemented workflow.
