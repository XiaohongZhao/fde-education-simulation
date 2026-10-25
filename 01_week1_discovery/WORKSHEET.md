# Discovery Worksheet

## One-page discovery memo

Use the questions below to write a connected explanation. Label each fact with a simulated evidence ID or a source still requiring verification.

1. Who experiences which problem, in which workflow? What are its frequency, time cost and consequences?
2. How do the director, actual users, academic operations and learners describe it differently?
3. What is the most credible current explanation, and what alternatives remain?
4. Who and which workflow step are in the smallest useful pilot? What is excluded?
5. How are success, failure and pausing defined, and who decides?
6. What evidence is still missing? Who will provide it, and in what form?

## Minimal data request

| Data | Minimum fields | Purpose | Equivalent in the simulation |
|---|---|---|---|
| Course catalogue | course_id, version, validity, fee, prerequisites, schedule, delivery mode and places | Recommendation facts and filters | `prototype/data/catalog.json` |
| Enquiry requirements | Anonymous ID, age, goal, budget, prior knowledge, availability and intent | Clarification and course fit | `prototype/data/examples.json` |
| Contact consent | Purpose, channel, time and withdrawal state | Eligibility for follow-up | Simplified boolean only; production structure remains to be designed |
| Trial state | Proposal, confirmation, cancellation and attendance time | Separate proposals from success and define the attendance denominator | Not connected; participant designs it |
| Adviser time | Start, completion, review and rework times, plus applicable scope | Compare total human effort | No real measurements collected |
| Business outcomes | First enquiry, booking, attendance, payment and refund times | Calculate a funnel for the same cohort and observation window | Synthetic aggregates in the client brief only |

Do not request every conversation, payment or identity record because it might be useful later. Each field needs a purpose in this engagement. This case does not require real names, phone numbers or identity-document numbers.

## Compare three pilots

Compare adviser response assistance, automated booking and payment reminders, and learning-progress intervention. For each, specify users, existing data, required write access, the main consequences of errors, measurable benefits and maintenance ownership. Select one and name at least one condition that would change your choice.

## Interview notes template

Role: ____; question to verify in this interview: ____.

| Statement or situation | My interpretation of the fact | Evidence ID | Cross-check needed? | Next step |
|---|---|---|---|---|
| ____ | ____ | ____ | ____ | ____ |

Finish with separate lists of facts, hypotheses, decisions and unresolved questions. Label role-play material as “simulated interviews”.
