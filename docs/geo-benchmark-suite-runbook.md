# GEO Benchmark Suite Runbook

## One-Command Run

The repository includes a dependency-light Python CLI:

```bash
./geo-bench run --month 2026-08 --providers mock --runs 1
```

This command:

1. Creates or reads the monthly prompt set.
2. Calls the selected provider.
3. Stores provider answers.
4. Retries failed answers for providers with fallback configuration.
5. Scores Answer Share, Citation Authority, and Recommendation Rate.
6. Generates Overall and Unchanged KPI views for every target in `targets.json`.
7. Writes cost estimates and reports.

Output layout:

```text
geo-benchmark/
  config/
  prompts/<month>/
  runs/<month>/
  reports/<month>/
```

Primary report artifacts:

```text
geo-benchmark/reports/<month>/llm-report.md
geo-benchmark/reports/<month>/target-kpi-summary.csv
geo-benchmark/reports/<month>/kpi_summary.json
geo-benchmark/reports/<month>/planned_cost_summary.json
geo-benchmark/reports/<month>/cost_summary.json
```

The human-readable LLM report is always a single Markdown file: `llm-report.md`. CSV and JSON files are audit and downstream-analysis artifacts.

## Real Providers

The `mock` provider is free and useful for pipeline validation, but it is not a market benchmark. Before running real providers, configure API keys:

```bash
export OPENAI_API_KEY="..."
export ANTHROPIC_API_KEY="..."
export GEMINI_API_KEY="..."
export PERPLEXITY_API_KEY="..."
```

Then run:

```bash
./geo-bench run \
  --month 2026-08 \
  --providers openai,anthropic,gemini,perplexity \
  --runs 3
```

## Filtered Refresh

If only one prompt slice changes, do not rerun the whole month. Use a filtered refresh to preserve all other provider answers:

```bash
./geo-bench --data-dir geo-benchmark-openai run \
  --month 2026-08 \
  --providers openai \
  --runs 1 \
  --assumed-output-tokens 1600 \
  --force \
  --only-prompt-type ai_infra
```

You can also refresh exact prompt IDs:

```bash
./geo-bench --data-dir geo-benchmark-openai run \
  --month 2026-08 \
  --providers openai \
  --runs 1 \
  --force \
  --only-prompt-ids stable_ai_infra_001,dyn_202608_ai_infra_009
```

Semantics:

1. `--force` alone removes that provider's monthly raw answers and reruns the full provider/month.
2. `--force --only-prompt-type <type>` removes only matching provider/prompt-type rows.
3. `--force --only-prompt-ids <ids>` removes only matching provider/prompt-id rows.
4. Every filtered refresh still regenerates the full score and report from the final answer set.

## OpenAI Fallback

The standard OpenAI execution policy is:

```text
primary:  gpt-5-mini, max_output_tokens=1600
fallback: gpt-4o-mini, max_output_tokens=1000
```

`run` calls the primary model first. If OpenAI returns recoverable failures such as empty content or timeout, the CLI retries only failed rows and then scores/reports the final answer set. Missing keys, invalid keys, insufficient quota, billing, and authorization errors are not automatically retried.

To audit pure primary-model output, disable fallback:

```bash
./geo-bench run \
  --month 2026-08 \
  --providers openai \
  --runs 1 \
  --no-fallback
```

To repair failures after a completed run:

```bash
./geo-bench retry-errors \
  --month 2026-08 \
  --provider openai \
  --model gpt-4o-mini \
  --max-output-tokens 1000
```

## Configuration

Provider and model settings:

```text
geo-benchmark/config/models.json
```

Pricing settings:

```text
geo-benchmark/config/pricing.json
```

Prices change over time. Review pricing before production runs.

Target products:

```text
geo-benchmark/config/targets.json
```

Default target set: TiDB, CockroachDB, YugabyteDB, Supabase, PlanetScale, Neon.

## Prompt Audit

Check whether prompt text contains measured target names:

```bash
./geo-bench audit-prompts --month 2026-08
```

Current starter-set audit:

```text
Total prompts: 120
tidb: 0
cockroachdb: 0
yugabytedb: 0
aurora: 0
spanner: 0
planetscale: 0
alloydb: 0
```

The starter set asks buyer-pain, database-category, AI-infrastructure, and case-selection questions without naming measured vendors.

## Cost Estimate

Estimate budget without calling providers:

```bash
./geo-bench estimate-cost \
  --month 2026-08 \
  --providers openai,anthropic,gemini,perplexity \
  --runs 3 \
  --assumed-output-tokens 700
```

Default planning assumptions: 120 prompts, 4 providers, 3 runs per prompt, and 700 assumed output tokens per answer. Adding scoring targets does not increase provider-call cost because targets are scored locally against the same answers.

Example estimate:

```text
Total estimated cost: $5.2894
openai / gpt-5-mini: $0.5124
anthropic / claude-sonnet-5: $2.5872
gemini / gemini-2.5-flash-lite: $0.1042
perplexity / sonar: $2.0856
```

Perplexity Sonar includes a request fee, so its cost is not token-only.

## Monthly Comparability

The default monthly suite has 120 prompts:

- 84 stable prompts locked for at least six months.
- 36 dynamic prompts updated at most monthly.

Reports show both:

- `Overall KPI`: all 120 prompts.
- `Unchanged KPI`: stable prompts only.

If Overall improves but Unchanged does not, do not claim a strict like-for-like GEO improvement.

## Anti-Gaming Controls

- Freeze `prompt_set_hash` before running.
- Lock 84 stable prompts for at least six months.
- Keep source evidence on every dynamic prompt.
- Use fixed run counts per prompt.
- Retry only technical failures, never low-scoring answers.
- Report both Overall and Unchanged views.

## Monthly Compare

```bash
./geo-bench compare --from 2026-08 --to 2026-09
```
