# Qicheng Vocational Learning Centre — Client Brief

> Everything in this brief is fictional teaching material. It is not an industry benchmark, a real client fact or an achieved project outcome.

## The provider and its operations

Qicheng offers short courses for adults in data analysis, Python automation, AI office workflows and visual design. Online evening and weekend classes run alongside a smaller number of in-person courses. There are six admissions advisers and two academic operations staff; instructors participate by course.

Course information is stored in academic operations spreadsheets, while leads sit in a lightweight CRM. Advisers receive enquiries in chat, look up prices, check prior knowledge and ask about availability before contacting academic operations to confirm trial places. The course catalogue and saved response scripts do not share a consistent version.

## The presenting problem

In the simulated kick-off, director Lin Cheng says:

> Every day we answer the same questions about prices, prerequisites and class times. We are slow to respond in the evenings, and some people leave after seeing only the price. I want AI to help us handle more enquiries so advisers have time for meaningful conversations. Could we start with course selection and trial sessions?

Your task is to identify which sources of wasted effort technology can actually address and choose a first step that can be tested. The director's wish for more enrolments does not justify automatically steering every enquiry towards payment.

## Synthetic operating figures

The following fictional monthly enquiry cohort has completed a 30-day observation window. People are deduplicated: several chats with one learner count as one person making an enquiry.

| Metric | Synthetic value | Definition |
|---|---:|---|
| New learners making enquiries | 1,000 | First enquiry that month, deduplicated |
| Learners eligible for the initial pilot | 600 | Adults with complete requirements, an in-scope course goal and follow-up consent |
| Trial bookings | 240 | Among the 1,000 learners, a confirmed booking within 30 days of first enquiry |
| Trial attendance | 144 | Learners who attended among those with a booking |
| Completed enrolment payments | 48 | Among trial attendees, payment within 30 days of first enquiry |
| Mean adviser response-preparation time | 8 minutes per person | For the 600 pilot-eligible learners; course lookup, drafting and record preparation |
| Median wait for a first human response | 18 minutes | From initial enquiry to the first human reply, including queue time |

Trial attendance is therefore 144/240 = 60%; attendance-to-paid-enrolment conversion is 48/144 ≈ 33.3%; and enquiry-to-paid-enrolment conversion is 48/1,000 = 4.8%. These denominators are different and must not be interchanged. Eight minutes of preparation and 18 minutes of waiting are also different measures: adding or subtracting them does not establish time saved.

## Initial hypothesis

Start by giving advisers **verifiable course recommendations, trial proposals and draft contact tasks** to reduce lookup and copying. A versioned catalogue and explicit rules govern fees, prerequisites, schedules and places. The model only drafts text for review.

If preparation falls from eight to four minutes for each of the 600 learners, the scenario would release 600 × 4 ÷ 60 = 40 hours per month. This is a calculation to test, not an observed saving. It does not yet deduct review, correction, maintenance or model costs, and it is not equivalent to staff reductions or additional revenue.

## Scope and constraints

- **Audience:** adults. Enquiries from minors go to a person to confirm the service scope and are excluded from automated course recommendations in this case.
- **Initial courses:** use the [synthetic catalogue](prototype/data/catalog.json). Do not quote or recommend discontinued or full courses, or use a catalogue outside its validity period.
- **Client requirements:** traceable quotations; no promises of employment, salary or examination results; no automated refund decisions.
- **Action boundaries:** trial sessions remain proposals. People handle enrolment, payment, external contact and CRM writes.
- **Integration status:** the prototype reads local synthetic data only. No real CRM, messaging or scheduling API is connected.
- **Follow-up:** create a task draft only with explicit consent; withdrawal overrides prior consent. A draft is not evidence of contact.

## Stakeholders to interview

| Role | Fictional name | Main concern | Decision authority |
|---|---|---|---|
| Director | Lin Cheng | Business outcomes and delivery speed | Budget and pilot scope |
| Admissions manager | Zhou Min | Adviser efficiency and useful enquiries | Workflow and staffing |
| Frontline adviser | Chen Xiao | Complete information and less rework | Whether to adopt a draft |
| Academic operations lead | Wang Ning | Schedules, places and course fit | Catalogue and trial confirmation |
| Instructor | Zhao Ran | Prerequisites and realistic learning expectations | Entry requirements and learning objectives |
| Finance and learner support lead | He Yue | Receipts, contracts and refund definitions | Payment verification and after-sales handling |
| Systems administrator | Sun Yue | Maintainability and fallback | Integration and release |
| Learner representative | Liu He | Time, budget and practical usefulness | Their own course and contact preferences |

## What should exist after four weeks

A scope statement revised through interviews, a runnable prototype, an evaluation covering failures, an operating guide that admissions and academic operations can use, and a retrospective that distinguishes simulated results from hypotheses still awaiting validation.
