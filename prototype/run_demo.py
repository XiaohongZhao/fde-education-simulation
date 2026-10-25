"""Run from any working directory. No files written unless --output is supplied."""
import argparse
import json
from pathlib import Path
from education import ROOT, run, add_live_draft


def main():
    parser = argparse.ArgumentParser(description="Adult Training FDE Simulation: enquiry drafts and routing")
    parser.add_argument("--input", type=Path, help="One structured learner JSON object")
    parser.add_argument("--example", type=int, default=1, choices=range(1, 5))
    parser.add_argument("--as-of", default="2026-10-25", help="Fixed simulation clock; explicitly use the actual business date for real use")
    parser.add_argument("--live", action="store_true", help="Explicitly call the Anthropic API; provider charges may apply")
    parser.add_argument("--output", type=Path, help="Optional output JSON path")
    args = parser.parse_args()
    try:
        lead = json.loads(args.input.read_text(encoding="utf-8")) if args.input else json.loads(
            (ROOT / "data/examples.json").read_text(encoding="utf-8"))[args.example - 1]
        result = run(lead, as_of=args.as_of)
        if args.live:
            result = add_live_draft(result)
        text = json.dumps(result, ensure_ascii=False, indent=2)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(text + "\n", encoding="utf-8")
        print(text)
        if args.live and result["llm"]["status"] != "generated_unverified":
            return 2
        return 0
    except (ValueError, OSError, KeyError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    raise SystemExit(main())
