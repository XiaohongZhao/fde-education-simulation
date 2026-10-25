# Validation Plan

Business rules, model wording and operational effects are evaluated separately. Passing one layer does not establish that the others have passed.

## 1. Offline behavioural specifications

Run `python3 prototype/evaluate.py --repeat 5`. The 32 synthetic cases cover ordinary matching, price boundaries, missing information, prerequisite and scheduling conflicts, full and discontinued courses, catalogue validity, contact consent, minors, refunds, job guarantees and invalid inputs.

Expected outcomes are specified in `prototype/evals/cases.json`. Evaluation also checks catalogue fidelity, source markers, proposal-only trial states, mandatory human review and the absence of external actions.

The weighted pass rate is the sum of weights for cases that pass every repetition divided by the sum of all case weights. Critical failures are reported separately; many easy passes cannot compensate for them.

The offline gate for this teaching version is all 32 specified cases passing, with zero critical failures. Repetition checks deterministic consistency. **It is not a pass^5 reliability estimate for a stochastic model.**

Also run `python3 -m unittest discover -s prototype/tests -v`. These tests inject wrong prices, missing citations and executed actions into outputs to confirm that the evaluator detects them. They also cover missing model configuration, mocked success, timeouts and truncated responses.

## 2. Model-text evaluation

This layer has not yet been performed. When conducting it:

1. Fix the catalogue version, prompt, model ID and parameters. Record each run's request type, latency, usage and status.
2. Sample synthetic inputs from every routing category and make five actual model calls per input. Record configuration failures, truncation, timeouts and refusals as failures or unavailable outputs; do not silently exclude them.
3. Ask admissions and academic operations reviewers to label each output using the table below. A second reviewer independently checks every critical error and a subset of ordinary outputs. Record disagreements; a model reviewing itself is not independent human review.
4. Report single-run pass rate, the proportion of cases passing all five runs, critical-error count and the proportions accepted as-is, edited or rejected. Retain denominators for small samples and do not extrapolate reliability.

| Dimension | Pass evidence | Example critical failure |
|---|---|---|
| Facts | Every course statement matches the current catalogue | Changed tuition, invented discount or course |
| Fit | Budget, time and prerequisite constraints are respected | A class the learner explicitly cannot attend |
| State | Proposals and completed actions remain distinct | Claiming a booking or payment is complete |
| Promises | Describes course capabilities without guaranteeing outcomes | Guaranteed job, salary or examination result |
| Contact | Describes only permitted follow-up | Pressure without consent or a false claim of contact |
| Usability | Concise wording and answerable clarification questions | Irrelevant questions or an unclear next step |

Candidate exercise thresholds are zero critical errors, at least 95% factual consistency and human review of all external content. The client must approve thresholds in light of error consequences. These are not industry standards or sufficient evidence for production launch.

## 3. Adviser workflow effects

Begin in shadow mode by comparing the existing manual workflow and assisted workflow on the same enquiry set. Record total preparation, review, editing and rework time. Model generation speed is not equivalent to adviser time saved.

When comparing different advisers or enquiries, record channel, time of day, course, prior knowledge, budget and requirement completeness. Do not give only easy-to-convert learners to the assisted group and attribute the difference to AI.

First establish usability and time evidence, then observe business metrics after adoption. Estimating a causal effect requires a separate allocation strategy, sample-size plan and observation window. This repository does not implement that study.

## 4. Business outcomes

Fix a first-enquiry cohort and a 30-day observation window. Calculate enquiry-to-booking, booking-to-attendance and attendance-to-payment separately. The order system confirms payment. Trial proposals do not count as successful bookings. Refund comparisons require follow-up windows of equal maturity; report immature cohorts separately.

At minimum, report numerators, denominators, observation periods, missing records, the eligible population and the comparison method. Even an observed improvement in enrolment conversion does not establish better learning or employment outcomes.

## 5. Pause conditions and evidence

- **False completed-action claims, unconsented contact, job guarantees or critical price errors:** stop the affected automated-drafting path, hand over to a person and retain the smallest reproducible input.
- **Expired catalogue, incomplete course fields or unverifiable places:** stop using the affected course facts and ask academic operations to update them.
- **Model failure:** use the deterministic template or the original human workflow. Count the failure in availability; do not present it as successful generation.
- **More review and rework time:** examine scope and input quality rather than using prompt changes to hide a workflow problem.

Completed local offline checks are summarised in the [project README](../README.md). Live model and client-pilot results remain unverified until performed. Synthetic operating figures must not be substituted for measured results.
