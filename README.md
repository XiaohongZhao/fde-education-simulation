# Adult Training FDE Simulation

**[Try the interactive web demo on GitHub Pages →](https://xiaohongzhao.github.io/fde-education-simulation/)**

Open the public demo in your browser, choose a scenario, edit learner requirements and run the simulation. No login, installation or API key is required. The English interface shows course matches, trial proposals, follow-up drafts and a five-stage decision trace. It uses the same deterministic business rules as the Python reference; no live AI calls or real bookings are made. See the [web implementation](web/README.md) for source and local setup.

An end-to-end Forward Deployed Engineering case for **course enquiries, trial-session proposals and enrolment follow-up** at the fictional Qicheng Vocational Learning Centre. You take the role of an FDE working with the client: understand the business problem, choose a pilot scope, build a prototype, validate it and hand it over to the provider's team.

The project adapts the four-stage simulation structure of [kalyvask/fde-simulation](https://github.com/kalyvask/fde-simulation) with an education-specific scenario, data, code and exercises. All people, business figures, courses, learners and interview evidence are fictional teaching material. See [NOTICE.md](NOTICE.md) for attribution and the scope of the adaptation.

## Start here

| What you want to do | Start with |
|---|---|
| Understand the client engagement | [Client brief](00_brief.md) |
| Step into the FDE role | [Kick-off scenario](START_HERE.md) |
| Complete a four-stage portfolio exercise | [Exercises and deliverables](EXERCISE.md) |
| Run the reference prototype | The commands below and the [prototype guide](prototype/README.md) |
| Simulate stakeholder interviews with AI | [Role cards and interview prompt](01_week1_discovery/STAKEHOLDER_INTERVIEWS.md) |
| Compare your approach with a worked solution | [Reference solution](REFERENCE_SOLUTION.md), after attempting the exercises |
| Practise a client review or portfolio discussion | [Assessment and portfolio guidance](ASSESSMENT.md) |

## Business workflow

Learner enquiry → adviser confirms structured requirements → catalogue-based matching → response draft with sources → trial-session or contact-task proposal → adviser review.

For example, a 28-year-old beginner wants to learn data analysis, is available only at weekends and has a budget of CNY 3,500. The prototype identifies an introductory course costing CNY 2,980 in the synthetic catalogue, provides its source and proposes a trial time for confirmation. If the learner permits follow-up, it also drafts a contact task. A proposal is never represented as a confirmed booking. The prototype does not collect payments, send messages or write to a CRM.

## Run the project

Python 3.10+ is required. The default mode uses only the standard library: no dependency installation, API key or network connection is needed.

From the project directory:

```bash
bash demo.sh
```

Or run individual steps:

```bash
python3 prototype/run_demo.py --example 1
python3 prototype/run_demo.py --example 3
python3 prototype/evaluate.py --repeat 5
python3 -m unittest discover -s prototype/tests -v
```

The four built-in examples cover a suitable trial enquiry, refusal of follow-up contact, a request for a job guarantee and a fully booked target course. English JSON output includes matched courses, sources, routing reasons, a response draft, a follow-up draft and a five-stage trace.

The simulation clock is fixed at **2026-10-25**. The catalogue is valid from 2026-10-01 to 2026-11-30. Use `--as-of 2026-12-01` to check that an expired catalogue routes to human review. Actual use requires the real business date and an actively maintained catalogue.

## Where AI fits

- **Interviews and client reviews:** give a role card to your chosen AI assistant and ask it to play the provider's director, admissions adviser or academic operations lead.
- **Optional model drafting:** explicitly pass `--live` to call the Anthropic Messages API. Configure an available model and credentials yourself. Output is labelled `generated_unverified` for human review and cannot change course matches or action states. See the [prototype guide](prototype/README.md).
- **Default offline mode:** deterministic code implements five processing stages. Template outputs validate interfaces and business rules; they are not evidence of validated multi-model collaboration or natural-language understanding.

## Validation and delivery status

Verified on 2026-10-25 with Python 3.11.11: **32 synthetic behavioural cases × 5 repetitions = 160 executions**, with all cases passing, plus **11 contract and failure-detection tests**. Repetition checks consistency; it does not estimate the probability of an LLM succeeding five times. The commands above reproduce these checks.

The project includes a runnable offline prototype, an optional model adapter and the complete exercise materials. **Live model calls, real learner data, CRM or scheduling integration, and business outcomes remain unverified.** The adapter has been tested only with mocked responses, failures and truncation.

This is an extensible FDE learning project. Pilots, interviews and business acceptance in the four-stage programme are exercises for the participant to carry out; the reference solution does not imply that those activities have already happened.

All documentation, sample data, prompts and programme messages are in English. The original scenario's CNY amounts and UTC+08:00 trial times are retained; translation does not relocate the fictional business.
