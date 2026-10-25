# Four-Stage Reference Solution

> This is a worked approach and proposed validation plan for a simulation, not a report of completed client discovery or production deployment. Attempt the exercises before comparing your work.

## Discovery findings

The kick-off complaint about slow replies includes both queueing and preparation. F01 identifies 18 minutes as a waiting measure; F03 identifies eight minutes as preparation for eligible enquiries. They must be measured separately. F05 and F06 suggest that incomplete requirements and changing preferences cause recommendation rework, so advisers should confirm the initial structured inputs.

F07 and F08 show that a timetable snapshot cannot guarantee current capacity, and that trial bookings and enrolment are different states. Direct automated booking would introduce writes and state-consistency problems. Starting with adviser assistance allows matching rules to be tested against the synthetic catalogue while keeping action outcomes checkable.

F09 and F10 distinguish self-reported experience from demonstrated ability. The prototype's level is a demonstration field; a real project needs actionable classification criteria from instructors. F11 and F12 establish clear human-system boundaries around completed enrolment and refunds.

## Choosing the pilot

| Option | Potential value | Main dependencies | Initial decision |
|---|---|---|---|
| Reply assistance and trial proposals | Less lookup and copying; more consistent information | Valid catalogue, confirmed requirements and human review | Start here: fewer integrations are needed to test operational effects |
| Automated booking, payment reminders and enrolment | Less downstream manual work | Live capacity, consent, orders, payments and reliable writes | Defer: the required interfaces and state evidence are absent |
| Learning-progress intervention | Potential improvement in learning processes | Attendance, assignments, learning objectives and instructor involvement | Treat as a separate project; admissions metrics cannot stand in for learning outcomes |

Conditions that would overturn the preferred option: if measurement shows that evening understaffing causes most delay and lookup takes little time, prioritise staffing or task allocation. If materials are already accurate and advisers draft quickly, a model may not create a net benefit.

## Solution development

Use a versioned catalogue, structured requirements and explicit filters. Selection considers goals, budget, prerequisites, time, delivery mode, active status and available places together. No consent means no follow-up task; no match retains an explicit reason.

Rules supply facts, and the model may express confirmed information in more natural English. Drafts remain separate from external actions, and every output requires adviser review. This makes errors easier to locate: incorrect inputs, stale catalogue facts, unsuitable rules or unsupported model additions.

Recommendations are not ranked by margin. Price and course ID provide an inspectable order. A real product could add relevance to learner goals, but the basis must be explained and checked for inappropriate recommendations.

## Validation and value definitions

Offline results answer whether rules behave as specified. Live model evaluation asks whether wording is accurate and usable. Adviser trials test whether time is saved after review and rework. Report these separately.

Forty hours per month is a scenario based on 600 learners and four minutes saved each. If measurement instead showed an average saving of two minutes, with an additional 12 hours per month for maintenance and review, net released time would be 600 × 2 ÷ 60 − 12 = 8 hours per month. Continuing would still depend on cost and quality; model generation speed cannot be converted directly into a business benefit.

Calculate enrolment outcomes within the same enquiry cohort's 30-day window. Compare working time and quality first, then cautiously observe funnel changes. This version does not predict purchase probability or label learner value from budget or response speed.

## Handoff and product feedback

Academic operations owns course facts, advisers verify inputs and drafts, systems administration maintains integrations and failure handling, and the director decides whether to continue. Rerun affected cases whenever the catalogue or prompt changes.

Reusable capabilities include versioned facts, explicit proposal/confirmation/execution states, consent withdrawal, readable routing reasons and tests showing that the evaluator detects errors. Education-specific prerequisites and trial rules still require separate maintenance; a generic customer-service template is not sufficient on its own.

## Five common traps

1. Counting trial proposals as successful bookings, inflating the denominator for attendance.
2. Recommending an affordable course while overlooking time or prerequisites.
3. Allowing old consent to override a withdrawal, or treating one follow-up permission as unlimited marketing consent.
4. Testing only ordinary enquiries while omitting full courses, old prices, refunds and changed preferences.
5. Presenting synthetic pass rates, hypothetical savings or reference materials as real business achievements.
