# Four-Stage Exercises and Deliverables

Work over four weeks or compress the schedule to suit your availability. These are exercise timings, not a promised client delivery schedule. Attempt each stage before reading the [reference solution](REFERENCE_SOLUTION.md).

| Stage | Suggested time | Work | Evidence needed to progress |
|---|---|---|---|
| Week 1 — Discovery | 4–6 hours | Interview the director, advisers, academic operations and learners; request minimal data; reconstruct the workflow | Explain where time is actually spent, give denominators and keep unknowns distinct from facts |
| Week 2 — Solution development | 6–8 hours | Compare pilot options; design fields and rule/model responsibilities; run and extend the prototype | Specific scope, traceable course facts, explicit human checkpoints and a demonstrable programme |
| Week 3 — Validation | 6–10 hours | Define acceptance criteria first; run synthetic evaluations; add failures; design human review | Critical failures cannot be hidden by an average; offline and model results remain separate |
| Week 4 — Handoff | 3–5 hours | Write operating, incident and fallback guidance; demonstrate and defend the solution | Explain who updates courses, who reviews drafts and how service continues during failure |

## Stage 1 deliverables

Use the [discovery worksheet](01_week1_discovery/WORKSHEET.md) to produce a one-page discovery memo, simulated interview notes for at least four roles, a field-level data request and three possible pilots.

## Stage 2 deliverables

Read the [architecture and interface guide](02_week2_solution/ARCHITECTURE.md). Run the existing prototype, then extend it with a distinct task type that asks academic operations to confirm a time when no future trial slot is available. Specify the expected behaviour before coding, then add evaluation cases. Do not move an expired trial to a new date merely to make a test pass.

Write an architecture decision explaining why this project uses a single orchestrator and explicit rules. What new evidence would justify another model call rather than another deterministic function?

## Stage 3 deliverables

Follow the [validation plan](03_week3_validation/VALIDATION.md). Record the catalogue, code and case-set versions and the commands used. Add at least eight cases, including a conflicting field, a scheduling boundary and an example where an adviser disagrees with a model suggestion.

If you run live model tests, keep each model output and human judgement separately. Do not report the 160 offline passes as model evaluation results.

## Stage 4 deliverables

Replace the role-based owners and outstanding integration items in the [runbook](04_week4_handoff/RUNBOOK.md) with actual arrangements. Write a one-page retrospective covering the initial hypothesis, counterexamples, implementation choices, validation evidence and unanswered questions. Only tests that were actually performed belong in the results.

## Five-hour compressed exercise

1. **0:00–0:45:** read the brief, interview admissions and academic operations, and define an initial scope.
2. **0:45–1:30:** specify inputs, course sources, routing rules and acceptance criteria.
3. **1:30–3:00:** run the prototype and implement the no-future-trial extension.
4. **3:00–4:00:** add failure cases, run the evaluation and fix errors.
5. **4:00–5:00:** prepare a one-page client explanation, evidence and fallback steps, then complete the [review](ASSESSMENT.md).

The final submission is a simulation supported by evidence. If it is not connected to real systems, retain “simulation” or “prototype” in its portfolio title and description.
