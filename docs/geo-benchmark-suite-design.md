# GEO Benchmark Suite Design

Status: implemented V1  
Scope: repeatable, comparable, and auditable measurement for AI answer-engine visibility in database buying scenarios.

## Objective

The suite measures how AI answer engines talk about database products across realistic buyer prompts. It is designed to answer three executive questions:

| Executive KPI | Question | Output |
| --- | --- | --- |
| Mention Rate | Are we present? | Percentage of eligible non-branded answers, trend, competitor gap |
| Intent-weighted Prominence Score | How prominently are we seen? | 0-100 score, trend, competitor gap |
| Citation Authority Index | Are we trusted? | 0-100 score, source mix, accuracy, freshness |
| Qualified Recommendation Rate | Are we recommended? | 0-100 score, recommendation quality, competitor gap |
| Comparison Win Rate | Do we win head-to-head evaluations? | 0-100 score and explicit winner counts |

Design principles:

- Repeatable: monthly prompt set, provider list, and rubric are frozen before running.
- Comparable: reports include both Overall and Unchanged views.
- Auditable: raw prompts, config, scored rows, and reports are stored with hashes and timestamps.
- Anti-gaming: at least 70% of prompts stay stable; at most 30% can be refreshed each month.

## Benchmark Set

V1 uses 120 neutral buying-scenario prompts:

| Prompt Type | Count | Purpose | Default Intent Weight |
| --- | ---: | --- | ---: |
| `pain_point` | 36 | Customer pain and operational trigger | 3 |
| `database_type` | 30 | Database category and architecture choice | 2 |
| `ai_infra` | 30 | AI app, serverless AI, and operational AI data | 3 |
| `case_selection` | 24 | Industry and workload selection patterns | 2 |

Prompt objectivity rules:

- Prompt text must not name measured targets such as TiDB, CockroachDB, YugabyteDB, Supabase, PlanetScale, or Neon.
- Prompts should ask about pain, category, use case, architecture, or workload selection.
- `geo-bench audit-prompts` checks target-name leakage before running.

Required prompt metadata:

| Field | Purpose |
| --- | --- |
| `prompt_id` | Stable tracking |
| `prompt_text` | Actual model input |
| `prompt_type` | Breakdown reporting |
| `persona` | Buyer persona analysis |
| `region` | Regional analysis |
| `funnel_stage` | Funnel-stage analysis |
| `use_case` | Use-case analysis |
| `intent_weight` | Opportunity weighting |
| `qualified_recommendation_opportunity` | Recommendation-rate denominator |
| `panel` | Stable versus dynamic comparison |
| `source` | Source evidence and validation status |

Canonical prompt storage:

```text
geo-benchmark/prompts/<month>/prompts.json
```

Provider-specific data directories must not keep separate prompt copies. They read from this canonical prompt tree so prompt uniqueness is preserved.

## Monthly Update Rule

The suite separates the monthly prompt set into:

| Panel | Count | Rule | Purpose |
| --- | ---: | --- | --- |
| Stable | 84 | Locked for at least six months | Strict month-over-month comparison |
| Dynamic | 36 | May refresh monthly | Fresh market language and emerging buyer questions |

The dynamic share must not exceed 30%. If there are not enough high-quality new prompts, update fewer prompts rather than lowering evidence quality.

## Run Matrix

Default production surfaces:

| Provider Surface | Purpose |
| --- | --- |
| OpenAI | General answer and buying recommendation coverage |
| Anthropic | Long-context technical recommendation coverage |
| Gemini | Google ecosystem coverage |
| Perplexity | Citation-oriented/search-augmented answer coverage |

Each provider answer is scored locally for every configured target. Adding targets does not increase provider-call cost.

## KPI 1: Mention Rate and Prominence Score

Mention Rate measures the percentage of eligible non-branded answer rows that mention the target at all. It treats every eligible answer equally and does not depend on mention order or prompt intent.

Prominence Score measures how early a target appears, weighted by prompt intent. It preserves the metric previously named Answer Share; `answer_share` remains in machine-readable output as a deprecated compatibility alias.

Single-answer presence score:

| Position | Score |
| --- | ---: |
| First mentioned product | 1.0 |
| Top-three product | 0.6 |
| Other mention | 0.2 |
| Not mentioned | 0.0 |

Monthly KPI:

```text
Intent-weighted Prominence Score =
sum(prompt_weight * presence_score) / sum(prompt_weight)
```

Scores are reported on a 0-100 scale.

## KPI 2: Citation Authority

Citation Authority measures whether a target mention is supported by credible, relevant, accurate, and fresh sources.

```text
Citation Authority =
citation_presence
* source_authority
* grounding
* accuracy
* freshness
```

Source authority examples:

| Source Type | Weight |
| --- | ---: |
| Official docs, official site, GitHub, marketplace | 1.0 |
| Customer case, cloud partner content, technical paper | 0.9 |
| Analyst report or trusted technical publication | 0.8 |
| Third-party technical blog | 0.5 |
| Aggregator, forum, unknown source | 0.2 |

Accuracy is checked against the configured fact registry. Freshness defaults to a 12-month window unless the source is explicitly marked as evergreen.

## KPI 3: Recommendation Rate

Recommendation Rate measures whether the model recommends the target, not merely whether it lists the target.

| Recommendation Class | Score |
| --- | ---: |
| Best choice | 1.0 |
| Strong option | 0.75 |
| Conditional fit | 0.5 |
| Listed only | 0.2 |
| Negative | -0.5 |
| Not mentioned | 0.0 |

Qualified Recommendation Rate:

```text
recommended answers / qualified recommendation opportunities
```

The denominator excludes prompts that are not reasonable recommendation opportunities.

## KPI 4: Comparison Win Rate

Comparison Win Rate measures how often the target is the single explicit winner in valid head-to-head comparison answers. It uses recommendation language such as “recommend,” “choose,” or “preferred”; mention order does not determine the winner. Answers with no clear or unique winner are excluded from the win-rate denominator and reported through the valid-comparison count.

## Comparability

Reports show two views:

| View | Scope | Use |
| --- | --- | --- |
| Overall | All 120 prompts | Current-month market view |
| Unchanged | Stable prompts only | Strict like-for-like trend view |

If Overall improves but Unchanged does not, do not interpret the change as strict month-over-month improvement.

## Anti-Gaming Controls

| Risk | Control |
| --- | --- |
| Selecting prompts that favor one product | Fixed type, persona, region, use-case, and intent quotas |
| Deleting weak prompts after results | Stable prompts are locked; deprecated prompts retain history |
| Replacing prompts after a run | Prompt set is frozen before running and hashed |
| Cherry-picking runs | Fixed run count; all valid runs are scored |
| Retrying low-score answers | Only technical failures can be retried |
| Selective model publishing | Provider list should be frozen and missing providers marked |
| Manual answer editing | Raw answer hash and timestamp are retained when raw answers are stored |
| Rubric changes after scoring | Rubric changes must be versioned and disclosed |

Technical failures include API timeout, empty content, malformed response, and provider errors. They do not include unfavorable recommendations, missing target mentions, or negative sentiment.

## One-Command CLI

```bash
./geo-bench run --month 2026-08
```

Flow:

1. Load or prepare monthly prompts.
2. Call provider surfaces.
3. Store answer artifacts.
4. Retry configured technical failures.
5. Score mentions, citations, facts, and recommendations.
6. Write Markdown, CSV, and JSON reports.

OpenAI default policy:

```text
primary model: gpt-5-mini
primary max output tokens: 1600
fallback model: gpt-4o-mini
fallback max output tokens: 1000
fallback scope: failed rows only
```

Filtered refresh:

```bash
./geo-bench run --month 2026-08 --providers openai --runs 1 --force --only-prompt-type ai_infra
./geo-bench run --month 2026-08 --providers openai --runs 1 --force --only-prompt-ids stable_ai_infra_001,dyn_202608_ai_infra_009
```

## Reports

Each provider directory keeps one human-facing Markdown report:

```text
geo-benchmark/reports/<month>/llm-report.md
```

Machine-readable artifacts include:

```text
target-kpi-summary.csv
kpi_summary.json
scored_answers.csv
cost_summary.json
planned_cost_summary.json
prompt-type-breakdown-*.csv
use-case-breakdown-*.csv
model-breakdown-*.csv
```

## V1 Boundaries

V1 includes:

- Prompt generation and audit.
- Provider abstraction.
- Raw answer collection.
- Automated scoring.
- Monthly reports.
- Cost estimation.
- Filtered rerun and failed-answer repair.

V1 does not include:

- Automatic website edits.
- Automatic CMS publication.
- Full dashboard UI.
- Backfilling every historical month.
- Per-prompt surface routing. Prompts carry a `surface` field (`api` /
  `product`), but the runner does not read it: every prompt, including the
  product-surface prompts, is sent to each provider's developer API. Answers
  that would differ on a product surface (for example the Cloud Zero case)
  are therefore measured only as the developer API returns them.
