# Client Review, Scoring and Portfolio Guidance

## Five-minute review

Give your actual deliverables, test outputs and the following prompt to an AI assistant:

> Act as the director and project reviewer at Qicheng Vocational Learning Centre. Ask one question at a time, no more than six, based on the work I supply. Challenge evidence and trade-offs without answering for me. Focus on why this workflow comes first, incomplete inputs, catalogue updates, human escalation, what the evaluation actually proves and post-handoff ownership. Then score the work using the rubric below. Mark dimensions without submitted evidence as “not demonstrated”; do not invent performance.

Possible questions:

1. If replies become faster but conversion stays the same, has the project failed?
2. A learner's latest message says weekends are impossible, but the form says weekends. What does your system do?
3. Two advisers see one remaining trial place simultaneously. Does the current prototype resolve that?
4. Do 32 cases passing five times show that a real model will never misquote a price?
5. Why use a model? Could templates alone already be sufficient?
6. When academic operations changes a price, who learns about it, who updates it and who detects mistakes?

## Scoring rubric

Score each dimension from 0 to 3, for a maximum of 15. **0:** no evidence. **1:** an idea with important steps missing. **2:** implementation or materials with the main limitations explained. **3:** relevant validation, counterexamples addressed and a workable handoff. Scores provide exercise feedback, not any company's official hiring standard.

| Dimension | Evidence to look for |
|---|---|
| Client understanding | Multiple stakeholder perspectives, checkable definitions and conditions that would overturn the initial hypothesis |
| Scope and design | Explicit inputs, sources, rule/model responsibilities and action boundaries |
| Engineering | Reproducible commands, error handling, states and sources |
| Evaluation | Independently specified cases, critical failures and separate live/offline results |
| Handoff | Routine ownership, updates, fallback and outstanding work |

## Difficult client situations

Spend ten minutes on each. Restate the facts, explain current boundaries, then propose an actionable next step and a way to verify it.

- **The director expands scope:** “Start collecting payments automatically next week.” Explain the missing links to orders, payments and receipts. Propose a testable next phase without inventing completed actions in a demo.
- **An adviser reports more work:** “I have to edit every model reply.” Examine total preparation, review and rework time. Compare against the template baseline and disable model rewriting if necessary.
- **A learner complains about contact:** “I already told you not to contact me.” Separate message understanding, structured consent and queued-task state. Stop further contact first, then find the synchronisation gap. This prototype does not implement real message sending or withdrawal synchronisation.

## Portfolio wording

Suggested title: **Adult Training Course Advisory and Trial Follow-up — FDE Simulation**.

Write a paragraph following business problem → your actual contribution → implementation and trade-offs → validation → limitations. Claim only work you actually performed. If using the reference implementation, acknowledge that your work extends an open-source simulation structure and reference code.

Fill-in template:

> In a fictional adult-training scenario, I completed ____ and scoped the initial workflow to ____. I implemented ____, using ____ as the factual source and ____ to control consequential actions. Across ____ independently specified cases and ____ executions, I verified ____. Live model evaluation/adviser testing is ____. The project has not yet ____, so I do not claim ____.

Do not turn the synthetic 40 hours per month, 48 paying learners or simulated interviews into real achievements. If you only ran the reference scripts, describe that as reproduction and analysis, not a client deployment.
