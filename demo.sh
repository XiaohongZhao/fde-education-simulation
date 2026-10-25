#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
export PYTHONDONTWRITEBYTECODE=1
python3 "$ROOT/prototype/run_demo.py"
python3 "$ROOT/prototype/evaluate.py" --repeat 5
