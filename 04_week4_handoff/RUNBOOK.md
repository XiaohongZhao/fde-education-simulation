# Handoff and Incident Runbook

This runbook covers the teaching prototype. Named owners below are fictional roles. Before a real pilot, replace them with actual owners, contact routes and staffing arrangements.

## Routine handling

1. The admissions adviser confirms input fields, particularly changed availability, budget, intent and contact consent.
2. Run the prototype and inspect route and reason. Clarify missing information first; do not force a recommendation after escalation.
3. Check course sources, prices, schedules and prerequisites. Academic operations must still confirm current capacity for a trial.
4. Compare any model draft against the structured facts. If the model is unavailable or fails, use the deterministic template as a starting point for a human reply.
5. After a person books, sends a message or enrols a learner, record the status using the real system's receipt. Prototype output is not proof of completion.
6. Execute post-trial contact tasks only after prerequisites such as actual attendance have been confirmed. The single consent boolean still requires a human to check purpose, channel and frequency.

## Responsibilities

| Work | Fictional owner | Checks |
|---|---|---|
| Catalogue publication | Wang Ning, academic operations | Price, schedule, places, discontinued status, prerequisites, version and validity |
| Reply and task review | Zhou Min and the on-duty adviser | Suitability, promises, consent and next steps |
| Course entry requirements | Zhao Ran, instructor | Prerequisites and learning objectives |
| Payments and refunds | He Yue, finance and learner support | Orders, contracts, receipts and attendance |
| Operation and fallback | Sun Yue, systems administration | Configuration, logs, errors and version recovery |
| Continue or stop the pilot | Lin Cheng, director | Operational effects, quality and maintenance burden |

## Catalogue updates

1. Edit a separate working copy. Update the version, validity and changed courses; retain source and academic-operations approval records.
2. Verify changed facts and add corresponding expected behaviours. Do not simply change test labels to make incorrect output pass.
3. Run offline evaluations and tests, then manually inspect examples for affected courses.
4. Academic operations confirms the course facts; the systems administrator releases the update. The initial catalogue is case material. Do not extend its validity to make it appear to be a current real catalogue.

A capacity snapshot cannot resolve simultaneous booking attempts. Real integration must recheck availability at confirmation and prevent duplicate reservations. This remains unimplemented.

## Incident handling

| Symptom | Immediate response | Follow-up repair |
|---|---|---|
| Wrong price | Stop using that course draft and check the latest catalogue manually | Check versions, field mappings and model output; add a regression case |
| stale_catalog | Do not continue recommending from cached prices | Academic operations confirms and publishes a valid catalogue |
| Model timeout or truncation | Inspect llm.status and use the template or a human reply | Investigate configuration and availability; retain failure counts |
| Consent withdrawn | Stop current and pending contact tasks | Correct the input and synchronise withdrawal events in a real integration |
| Trial full or rescheduled | Do not confirm an old proposal | Academic operations reconfirms; a person explains alternatives |
| Enrolment or refund dispute | Refer to finance/support without guessing amounts or status | Check actual contracts and order records |

## Fallback and recovery

To disable model drafting, omit `--live`; deterministic templates remain available. For a full fallback, stop using prototype outputs and restore manual course lookup and enquiry handling. The current prototype makes no external writes, so there are no CRM records from it to undo. Real write operations would require a separate rollback design.

Before recovery, the owner confirms that the error was reproduced and fixed, affected cases pass, the catalogue is valid and reviewers can explain the change. A service starting successfully is not proof that the business process has recovered.

## Entry criteria for a real pilot

These are outstanding tasks, not completed acceptance sign-offs:

- Academic operations confirms sources, validity and the booking-confirmation process.
- Admissions confirms draft quality, review time and rejection/editing workflows.
- Systems administration confirms actual input adapters, consent synchronisation, monitoring and fallback.
- Finance confirms enrolment and refund definitions.
- The director confirms scope, model and maintenance costs, and pause thresholds.

## Retrospective template

Initial hypothesis: ____. Tests or pilots actually conducted: ____. Most important counterexample: ____. Changes made in response to evidence: ____. Total time actually saved or added: ____. Still unverified: ____. Next owner and review date: ____.
