# Prototype Guide

Python 3.10+ is required; no third-party dependencies are needed by default. Paths are resolved relative to the script, so it can run from any working directory. Commands below assume the project root as the current directory.

```bash
python3 prototype/run_demo.py --example 1
python3 prototype/run_demo.py --example 2
python3 prototype/run_demo.py --example 3
python3 prototype/run_demo.py --example 4
python3 prototype/evaluate.py --repeat 5
python3 -m unittest discover -s prototype/tests -v
```

## Custom inputs and dates

Save one object from `data/examples.json` as your own JSON input, edit it according to the [interface guide](../02_week2_solution/ARCHITECTURE.md), then run:

```bash
python3 prototype/run_demo.py --input /absolute/path/learner.json --as-of 2026-10-25
```

Input must be one object. Do not pass the four-object examples.json array directly to `--input`. The CLI fixes the simulation date for future reproducibility; the underlying `run()` function uses the system date if no date is supplied.

Use `--output /absolute/path/result.json` to save output; otherwise it is printed only. The evaluator also supports `--output`. `demo.sh` writes no result files and disables Python bytecode caches.

## Optional live model drafting

Set `ANTHROPIC_API_KEY` and `ANTHROPIC_MODEL` in your own terminal environment. Use the exact ID of a model currently available to your account. Do not place a key in data files or commit it to Git. Once configured, explicitly run:

```bash
python3 prototype/run_demo.py --example 1 --live
```

Only `--live` triggers a request. An API key in the environment does not make the default mode call the API. Each command makes at most one model request, with a 30-second timeout and no automatic retries; provider charges may apply. Only filtered course facts and the template go to the fixed Anthropic Messages API endpoint, not the original enquiry text or learner ID.

| llm.status | Meaning |
|---|---|
| not_requested | This run is entirely offline |
| generated_unverified | The model completed text generation; human review is still required |
| incomplete | Empty, truncated or abnormally ended response; not a completed draft |
| error | Request or parsing failure; the deterministic template is retained |

Missing configuration causes a non-zero exit code without a request. An API error or truncated response prints the result with its retained template and exits with code 2. JSON appearing in the terminal does not by itself prove a successful model call.

The adapter implements HTTP calls to `/v1/messages` using the [Anthropic Python SDK API definitions](https://github.com/anthropics/anthropic-sdk-python/blob/main/api.md) and [client header definitions](https://github.com/anthropics/anthropic-sdk-python/blob/main/src/anthropic/_client.py). Only mocked responses have been tested here; live authentication, model availability and output quality remain unverified.

## Code map

| File | Responsibility |
|---|---|
| education.py | Field validation, catalogue matching, routing, templates, audit trace and optional model adapter |
| run_demo.py | Command-line entry point |
| evaluate.py | Independent case specifications, factual consistency and side-effect checks |
| data/catalog.json | Fictional versioned catalogue |
| data/examples.json | Four runnable synthetic inputs |
| evals/cases.json | 32 manually specified expected behaviours |
| tests/test_contracts.py | Error-detection tests for the evaluator and failure handling for the adapter |

## Reviewing model output

Compare `llm.text`, `recommendations` and `draft` item by item. Are prices and course durations consistent? Are sources retained? Are there additional discounts or outcome promises? Has a proposal become a claim of success?

The prototype does not automatically identify every semantic error in arbitrary model text, so generated wording always remains an unreviewed draft. Offline evaluation does not perform this review for you.

## Troubleshooting

- **Every course goes to human review:** check whether `as_of` is within the catalogue validity period, then inspect goals, availability, level and budget.
- **No trial proposal:** a course must match, intent must be trial, and the trial date must be later than the simulation date. This does not affect the course match itself.
- **No follow-up:** check explicit consent, withdrawal, adult eligibility and whether a recommendation was made.
- **Message/form conflict:** use adviser-confirmed fields; this version has no chat intent extractor.
- **Model error:** the template remains available for human use. Check status and configuration without copying credentials or provider error bodies into deliverables.
