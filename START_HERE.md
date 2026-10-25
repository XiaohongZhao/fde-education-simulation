# Start with a Client Kick-off

It is 08:30 on Monday of the first simulated project week. Director Lin Cheng sends you this message:

> We are meeting admissions and academic operations at nine. I want to start with the evening enquiries we struggle to handle. If possible, two advisers could try something next week. Tell me what data you need, what you would tackle first and how we will decide whether to continue.

You are the FDE responsible for delivery. Read the [client brief](00_brief.md) first; do not open the reference solution yet.

## Thirty minutes before the meeting

1. Spend ten minutes mapping the existing journey: enquiry → missing information → course selection → trial booking → attendance → enrolment. Mark possible waiting and rework.
2. Spend ten minutes identifying five important unknowns. Include deduplication, catalogue ownership, what counts as successful enrolment, who may contact learners and when a person must take over.
3. Spend ten minutes writing a falsifiable hypothesis: which workflow, which users, which metric and what result would make you stop or change direction?

## Run the kick-off

Open the [interview role cards](01_week1_discovery/STAKEHOLDER_INTERVIEWS.md). Give the facilitator prompt and Lin Cheng's card to an AI assistant. Act as the FDE yourself and ask one question at a time. Listen to how the client describes the work before proposing a multi-agent architecture.

Afterwards, record confirmed facts, information still requiring checks, the initial scope, explicit exclusions, the next data request and its owner. Statements made by simulated roles remain case material; do not present them as real customer interviews in a portfolio.

## If you want to see the code first

Run `bash demo.sh` from the project directory. Then explain why the programme can recommend DATA-101, why it cannot claim a booking is confirmed, and which output should disappear if the learner does not permit follow-up.
