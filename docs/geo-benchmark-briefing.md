# GEO Benchmark Briefing

Status: working benchmark suite  
Primary use: monthly GEO measurement for database buying scenarios  
Current target set: TiDB, CockroachDB, YugabyteDB, Supabase, PlanetScale, Neon

## What It Is

This benchmark is a repeatable test suite for measuring how AI answer engines talk about database products in realistic buyer questions. It is designed to answer three executive questions:

1. Are we seen?
2. Are we trusted?
3. Are we recommended?

The suite runs a fixed prompt set across selected model providers, stores raw answers, scores each target product against the same answers, and generates monthly reports with overall and stable-panel comparisons.

## What It Measures

### Answer Share

Measures whether a target product appears in the answer, with higher credit for better placement.

```text
first mention = 1.0
top 3 mention = 0.6
other mention = 0.2
not mentioned = 0.0
```

The final KPI is intent-weighted, so higher-intent prompts matter more than generic educational prompts.

### Citation Authority

Measures whether a target mention is supported by credible sources.

```text
Citation Authority =
citation presence
* source authority
* grounding
* accuracy
* freshness
```

Official docs, official sites, GitHub, cloud marketplace pages, analyst reports, third-party blogs, and forums are weighted differently.

### Recommendation Rate

Measures whether the answer actually recommends the target, not merely whether it mentions it.

```text
best choice = 1.0
strong option = 0.75
conditional fit = 0.5
listed only = 0.2
negative = -0.5
not mentioned = 0.0
```

Qualified Recommendation Rate counts explicit best, strong, or conditional recommendations over qualified recommendation opportunities.

## Prompt Set

The current suite uses 120 neutral prompts:

| Prompt Type | Count | Purpose |
| --- | ---: | --- |
| `pain_point` | 36 | Buyer pain without naming vendors |
| `database_type` | 30 | Category and architecture selection |
| `ai_infra` | 30 | AI app, vector, RAG, and agent memory infrastructure |
| `case_selection` | 24 | Industry and workload selection patterns |

The monthly panel is split into:

| Panel | Count | Purpose |
| --- | ---: | --- |
| Stable | 84 | Strict month-over-month comparability |
| Dynamic | 36 | Freshness from new market/customer inputs |

The prompt generator keeps measured target names out of prompt text. The audit command checks this explicitly.

## Target Set

The current scoring target set is:

```text
TiDB
CockroachDB
YugabyteDB
Supabase
PlanetScale
Neon
```

Each model answer is collected once per prompt and then scored locally for every target. Adding scoring targets does not increase model API cost unless the prompt set or provider run count changes.

## Monthly Run Model

Recommended production run:

```bash
./geo-bench run \
  --month 2026-08 \
  --providers openai,anthropic,gemini,perplexity \
  --runs 3 \
  --force
```

Local smoke test:

```bash
./geo-bench run --month 2026-08 --providers mock --runs 3 --force
```

The mock provider is only for validating pipeline behavior. It is not a market benchmark.

## Comparability

The report has two views:

| View | Meaning |
| --- | --- |
| Overall | All prompts in the month, including dynamic updates |
| Unchanged | Stable prompts only, the strict comparable view |

Monthly updates should preserve the stable 70% and refresh only the dynamic 30%. This keeps the benchmark current without destroying trend comparability.

## Anti-Gaming Controls

The suite currently includes:

- Neutral prompts with no measured target names.
- Stable/dynamic split to prevent prompt-set manipulation.
- Prompt audit for target brand leakage.
- Per-prompt source evidence fields.
- Separate overall and unchanged monthly comparisons.
- Raw answer retention for auditability.
- Target-level scoring against identical answer sets.

Current prompt validation status is `case_pattern_validated`: the starter prompts are grounded in public customer case patterns and docs, but they are not yet exact observed search, sales, or community query text.

## Cost Estimate

Using 120 prompts, 4 providers, 3 runs, and 700 assumed output tokens per answer:

| Provider | Requests | Estimated Cost |
| --- | ---: | ---: |
| OpenAI | 360 | $0.514 |
| Anthropic | 360 | $2.6001 |
| Gemini | 360 | $0.1048 |
| Perplexity | 360 | $2.092 |
| Total | 1,440 | $5.311 |

These are editable planning defaults. Verify provider billing pages before a production run.

## Main Artifacts

```text
geo-benchmark/prompts/<month>/prompts.json
geo-benchmark/runs/<month>/raw_answers.jsonl
geo-benchmark/runs/<month>/scored_answers.jsonl
geo-benchmark/reports/<month>/llm-report.md
geo-benchmark/reports/<month>/target-kpi-summary.csv
geo-benchmark/reports/<month>/kpi_summary.json
```
