# GEO Benchmark Suite

One-command benchmark suite for measuring how AI answer engines mention, cite, and recommend database products in realistic buying scenarios.

The default target set is:

- TiDB
- CockroachDB
- YugabyteDB
- Supabase
- PlanetScale
- Neon

## What It Measures

- Answer Share: whether the target product is visible in model answers.
- Citation Authority: whether target claims are supported by credible, fresh, and accurate sources.
- Recommendation Rate: whether the target is actually recommended, not merely listed.

## Quick Start

Run a local smoke test with the mock provider:

```bash
./geo-bench run --month 2026-08 --providers mock --runs 1
```

The mock provider does not call external APIs and must not be used as a market result.

Run real providers:

```bash
cp .env.example .env.local
# Edit .env.local and fill in the provider keys you want to use.

./geo-bench check-env --providers openai,anthropic,gemini

./geo-bench run \
  --month 2026-08 \
  --providers openai,anthropic,gemini \
  --runs 1 \
  --force
```

`.env.local` is loaded automatically and is ignored by git.

## Filtered Refresh

If only one prompt slice changes, do not rerun the whole month. Use a filtered refresh so other raw answers are preserved:

```bash
./geo-bench --data-dir geo-benchmark-openai run \
  --month 2026-08 \
  --providers openai \
  --runs 1 \
  --assumed-output-tokens 1600 \
  --force \
  --only-prompt-type ai_infra
```

You can also target specific prompts:

```bash
./geo-bench --data-dir geo-benchmark-openai run \
  --month 2026-08 \
  --providers openai \
  --runs 1 \
  --force \
  --only-prompt-ids stable_ai_infra_001,dyn_202608_ai_infra_009
```

With `--force` plus either filter, the CLI removes only matching provider/prompt rows and keeps the rest of the month intact.

## OpenAI Fallback

OpenAI runs use the configured fallback model when primary answers fail:

1. Run primary model: `gpt-5-mini`.
2. Retry only failed OpenAI answers with `gpt-4o-mini`.
3. Score and report after fallback recovery.

Manual repair command:

```bash
./geo-bench --data-dir geo-benchmark-openai retry-errors \
  --month 2026-08 \
  --provider openai \
  --model gpt-4o-mini \
  --max-output-tokens 1000
```

## Cost Estimate

```bash
./geo-bench estimate-cost \
  --month 2026-08 \
  --providers openai,anthropic,gemini,perplexity \
  --runs 3 \
  --assumed-output-tokens 700
```

## Prompt Audit

```bash
./geo-bench audit-prompts --month 2026-08
```

The current starter prompt set contains 120 neutral prompts: 84 stable prompts and 36 dynamic prompts. Prompt text does not name TiDB, CockroachDB, or other measured vendor targets.

## Reports

```text
geo-benchmark/reports/<month>/llm-report.md
geo-benchmark/reports/<month>/target-kpi-summary.csv
geo-benchmark/reports/<month>/kpi_summary.json
geo-benchmark/reports/<month>/planned_cost_summary.json
geo-benchmark/reports/<month>/cost_summary.json
```

## Documentation

- [Design](docs/geo-benchmark-suite-design.md)
- [Runbook](docs/geo-benchmark-suite-runbook.md)
- [Benchmark Briefing](docs/geo-benchmark-briefing.md)
- [Prompt Validation](docs/geo-prompt-validation.md)
- [2026-08 Anthropic Report](docs/geo-benchmark-2026-08-anthropic.md)
- [2026-08 OpenAI Report](docs/geo-benchmark-2026-08-openai.md)
