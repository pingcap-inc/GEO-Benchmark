# GEO Benchmark Suite

A repeatable benchmark for measuring how AI answer engines mention, cite, and recommend database products in realistic buying scenarios.

## Metrics

- Answer Share: how often a product appears, weighted by position and intent.
- Citation Authority: whether product claims are backed by credible, fresh, accurate sources.
- Recommendation Rate: whether a product is actually recommended, not just listed.

## Quick Start

```bash
cp .env.example .env.local
./geo-bench check-env --providers openai,anthropic

MONTH=2026-08 PROVIDERS=openai,anthropic RUNS=1 ./scripts/run-benchmark-workflow.sh
```

Run with provider web search:

```bash
MONTH=2026-08 PROVIDERS=openai,anthropic WEB_SEARCH=on RUNS=1 ./scripts/run-benchmark-workflow.sh
```

Run a no-cost local smoke test:

```bash
MONTH=2026-08 PROVIDERS=mock RUNS=1 ./scripts/run-benchmark-workflow.sh
```

## Key Files

- Prompts: `geo-benchmark/prompts/2026-08/prompts.json`
- Anthropic report: `geo-benchmark/reports/2026-08/llm-report.md`
- OpenAI report: `geo-benchmark-openai/reports/2026-08/llm-report.md`
- Web search on report: `geo-benchmark-websearch-on/reports/2026-08/llm-report.md`
- Canonical KPI report: `docs/geo-benchmark-2026-08-canonical-kpi.md`

Raw answer files are intentionally not published. Reports and scored outputs are included for review and comparison.

## Canonical Report Regeneration

Run a canonical raw-to-score benchmark for exactly one provider/mode view:

```bash
VIEW=openai-on MONTH=2026-08 FORCE=1 ./scripts/run-canonical-provider-benchmark.sh
VIEW=openai-off MONTH=2026-08 FORCE=1 ./scripts/run-canonical-provider-benchmark.sh
VIEW=anthropic-on MONTH=2026-08 FORCE=1 ./scripts/run-canonical-provider-benchmark.sh
VIEW=anthropic-off MONTH=2026-08 FORCE=1 ./scripts/run-canonical-provider-benchmark.sh
VIEW=gemini-on MONTH=2026-08 FORCE=1 ./scripts/run-canonical-provider-benchmark.sh
VIEW=gemini-off MONTH=2026-08 FORCE=1 ./scripts/run-canonical-provider-benchmark.sh
VIEW=perplexity-on MONTH=2026-08 FORCE=1 ./scripts/run-canonical-provider-benchmark.sh
```

This command collects raw answers, scores them, writes reports, and audits that the run has 120 successful answers, 720 scored target rows, the expected provider/mode, and the expected model. Fallback is disabled for canonical runs.
For OpenAI, canonical on/off runs both use the Responses API; the only intended difference is whether the web search tool is enabled.
Gemini grounds through the `google_search` tool, so it has both `gemini-on` and `gemini-off` views; Perplexity Sonar is always web-grounded, so its only canonical view is `perplexity-on`.

The audit step runs after local collection because raw answer files are not committed to this repository.

Regenerate the canonical KPI report from committed scored outputs:

```bash
python3 scripts/generate-canonical-kpi-report.py --month 2026-08
```

The default report includes four provider/mode KPI views plus Anthropic on/off and OpenAI on/off comparisons.

Generate one provider/mode view:

```bash
python3 scripts/generate-canonical-kpi-report.py --month 2026-08 --view anthropic-on --comparison none
```

Valid views: `anthropic-on`, `openai-on`, `anthropic-off`, `openai-off`.
Valid comparisons: `anthropic`, `openai`, `all`, `none`.
Do not manually blend providers for executive readouts.
