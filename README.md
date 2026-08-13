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

Regenerate the canonical KPI report from committed scored outputs:

```bash
python3 scripts/generate-canonical-kpi-report.py --month 2026-08
```

Generate one provider/mode view:

```bash
python3 scripts/generate-canonical-kpi-report.py --month 2026-08 --view anthropic-on
```

Valid views: `anthropic-on`, `openai-on`, `anthropic-off`, `openai-off`.
Do not manually blend providers for executive readouts.
