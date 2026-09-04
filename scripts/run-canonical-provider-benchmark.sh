#!/usr/bin/env bash
set -euo pipefail

VIEW="${VIEW:-${1:-}}"
MONTH="${MONTH:-2026-08}"
RUNS="${RUNS:-1}"
PROMPTS="${PROMPTS:-120}"
UPDATE_RATIO="${UPDATE_RATIO:-0.3}"
ASSUMED_OUTPUT_TOKENS="${ASSUMED_OUTPUT_TOKENS:-700}"
FORCE="${FORCE:-0}"
RETRIES="${RETRIES:-1}"

if [[ -z "$VIEW" ]]; then
  echo "Usage: VIEW=<anthropic-on|openai-on|anthropic-off|openai-off|gemini-off|perplexity-on> MONTH=2026-08 FORCE=1 $0" >&2
  exit 2
fi

case "$VIEW" in
  anthropic-on)
    DATA_DIR="geo-benchmark-websearch-on"
    PROVIDERS="anthropic"
    WEB_SEARCH="on"
    EXPECTED_MODEL="claude-sonnet-5"
    ;;
  openai-on)
    DATA_DIR="geo-benchmark-websearch-on"
    PROVIDERS="openai"
    WEB_SEARCH="on"
    EXPECTED_MODEL="gpt-5-mini-2025-08-07"
    ;;
  anthropic-off)
    DATA_DIR="geo-benchmark"
    PROVIDERS="anthropic"
    WEB_SEARCH="off"
    EXPECTED_MODEL="claude-sonnet-5"
    ;;
  openai-off)
    DATA_DIR="geo-benchmark-openai"
    PROVIDERS="openai"
    WEB_SEARCH="off"
    EXPECTED_MODEL="gpt-5-mini-2025-08-07"
    ;;
  gemini-off)
    # Gemini has no web-search tool wired up; off is its only canonical mode.
    DATA_DIR="geo-benchmark-gemini"
    PROVIDERS="gemini"
    WEB_SEARCH="off"
    EXPECTED_MODEL="gemini-2.5-flash-lite"
    ;;
  perplexity-on)
    # Perplexity Sonar is always web-grounded; on is its only canonical mode.
    DATA_DIR="geo-benchmark-websearch-on"
    PROVIDERS="perplexity"
    WEB_SEARCH="on"
    EXPECTED_MODEL="sonar"
    ;;
  *)
    echo "Unknown VIEW: $VIEW" >&2
    echo "Valid views: anthropic-on, openai-on, anthropic-off, openai-off, gemini-off, perplexity-on" >&2
    exit 2
    ;;
esac

if [[ "$RUNS" != "1" ]]; then
  echo "Canonical runs require RUNS=1. Got RUNS=$RUNS" >&2
  exit 2
fi

run_args=(
  --data-dir "$DATA_DIR"
  run
  --month "$MONTH"
  --providers "$PROVIDERS"
  --runs "$RUNS"
  --prompts "$PROMPTS"
  --update-ratio "$UPDATE_RATIO"
  --assumed-output-tokens "$ASSUMED_OUTPUT_TOKENS"
  --retries "$RETRIES"
  --web-search "$WEB_SEARCH"
  --no-fallback
)

if [[ "$FORCE" == "1" ]]; then
  run_args+=(--force)
fi

echo "Canonical view: $VIEW"
echo "Data dir: $DATA_DIR"
echo "Provider: $PROVIDERS"
echo "Web search: $WEB_SEARCH"
echo "Expected model: $EXPECTED_MODEL"
echo "Fallback: disabled"

./geo-bench check-env --providers "$PROVIDERS"
./geo-bench "${run_args[@]}"

python3 scripts/audit-canonical-provider-run.py \
  --month "$MONTH" \
  --view "$VIEW" \
  --data-dir "$DATA_DIR" \
  --provider "$PROVIDERS" \
  --web-search "$WEB_SEARCH" \
  --expected-model "$EXPECTED_MODEL"

echo "Canonical raw-to-score run complete."
