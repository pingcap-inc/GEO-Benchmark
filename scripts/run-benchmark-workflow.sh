#!/usr/bin/env bash
set -euo pipefail

DATA_DIR="${DATA_DIR:-geo-benchmark}"
MONTH="${MONTH:-}"
PROVIDERS="${PROVIDERS:-mock}"
RUNS="${RUNS:-1}"
PROMPTS="${PROMPTS:-120}"
UPDATE_RATIO="${UPDATE_RATIO:-0.3}"
ASSUMED_OUTPUT_TOKENS="${ASSUMED_OUTPUT_TOKENS:-700}"

if [[ -z "$MONTH" ]]; then
  echo "Set MONTH=YYYY-MM before running this workflow." >&2
  exit 2
fi

run_args=(
  --month "$MONTH"
  --providers "$PROVIDERS"
  --runs "$RUNS"
  --prompts "$PROMPTS"
  --update-ratio "$UPDATE_RATIO"
  --assumed-output-tokens "$ASSUMED_OUTPUT_TOKENS"
)

if [[ "${FORCE:-0}" == "1" ]]; then
  run_args+=(--force)
fi

if [[ "${NO_FALLBACK:-0}" == "1" ]]; then
  run_args+=(--no-fallback)
fi

if [[ -n "${ONLY_PROMPT_TYPE:-}" ]]; then
  run_args+=(--only-prompt-type "$ONLY_PROMPT_TYPE")
fi

if [[ -n "${ONLY_PROMPT_IDS:-}" ]]; then
  run_args+=(--only-prompt-ids "$ONLY_PROMPT_IDS")
fi

echo "Preparing prompt set and configuration..."
./geo-bench --data-dir "$DATA_DIR" prepare \
  --month "$MONTH" \
  --prompts "$PROMPTS" \
  --update-ratio "$UPDATE_RATIO"

echo "Validating prompt set..."
./geo-bench --data-dir "$DATA_DIR" validate-prompts --month "$MONTH"

echo "Running benchmark..."
./geo-bench --data-dir "$DATA_DIR" run "${run_args[@]}"

echo "Running local checks..."
PYTHONPYCACHEPREFIX="${PYTHONPYCACHEPREFIX:-/private/tmp/geo-benchmark-pycache}" python3 -m py_compile geo_benchmark/*.py
python3 -m unittest tests/test_geo_benchmark.py

echo "Workflow complete."
