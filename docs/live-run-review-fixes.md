# September live-run review corrections

## What the saved evidence actually shows

The first live run contains 276 TiDB-branded answers: 152 have a decisive semantic score and 124 do not. This is **decision coverage**, not the percentage the pipeline processed. Inspection of the saved answer-review evidence reconciles the remaining 124 as follows:

| Missing decisive score | Answers |
| --- | ---: |
| Approved `comparison_metric_only` mapping | 96 |
| Review-required mapping, no selected ready fact/conflict | 17 |
| Selected facts judged `not_enough_information` only | 10 |
| Judge unavailable, no decisive result | 1 |

Of the 96 comparison exclusions, 62 are in the Competitive Comparisons **topic** and 34 are in other topics. The alleged 25 both-missing prompts outside that topic comprise 17 comparison-only prompts and eight pending-review prompts. The 12 one-provider-only cases comprise one pending-review answer, ten inconclusive answers and one judge failure. The supplied evidence does not demonstrate 62 silently skipped judge calls. The legacy `accuracy_checked_facts=4` is a different rule-based measure and is not semantic eligibility. `semantic_checked_facts` counts correct/incorrect decisions, not attempted evaluations.

Pending-review prompts without a decisive result on either provider: `stable_scalearch_001`, `stable_scalearch_002`, `stable_scalearch_003`, `stable_deploycloud_015`, `stable_entcomp_001`, `stable_entcomp_002`, `stable_branddef_001`, `stable_branddef_033`. The additional one-provider pending case is `stable_agentinfra_010` on Anthropic. The unavailable case is `stable_branddef_030` on Anthropic. These are review/retry queues, not permission to approve unsupported facts.

## Changes

### 1. Make semantic coverage explainable

`scored_answers.csv` now exports disposition, outcome status/reason, selected facts, not-applicable facts and pending fact/review IDs. Each report also generates `semantic-coverage-audit.csv` (exact answer/prompt/provider rows) and `semantic-coverage-summary.json` (reconciled counts, provider breakdown and prompt IDs by status). The Markdown and HTML review report explains each outcome. A historical row without sufficient evidence is `not_recorded`, never guessed from topic or legacy accuracy. Original accuracy formulas and denominators are unchanged.

Runtime safeguards reject missing branded mappings, unapproved mappings and empty/non-ready `fact_covered` selections before a judge call. Review-required facts remain gated. Inconclusive evaluations remain distinct from failures. Existing approved fact content and semantic cache keys are not changed by these diagnostics.

### 2. Correct reporting topics without rewriting historical prompts

A versioned `geo-benchmark/config/prompt_metadata_overrides.json` supplies exact-ID/exact-text metadata corrections. `load_prompts` and the prompt builder apply the same corrections. Five discovery prompts (`branddef_006`, `_008`, `_009`, `_010`, `_013`) move to AI Agent Infrastructure; two (`_007`, `_011`) move to Hybrid Search & RAG. `_012` is not one of the seven and is unchanged. `prompt_type` and `use_case` move together. IDs, wording, brand class, intent weights and group remain unchanged.

The builder reserves the original IDs **before** applying reporting-topic corrections. Keep those identity-source cluster assignments when importing the existing sheet; do not renumber the panel. Frozen prompt files, hashes and saved September answers/reports are not modified by this PR. New score outputs record both the effective prompt hash and the frozen source prompt hash plus the metadata revision. Cluster results after this correction must be labeled a restatement, not a visibility gain/loss.

### 3. Correct comparison extraction and review eligibility

The brand-agnostic winner extractor normalizes Markdown and gives the final recommendation/verdict section priority over earlier conditional product profiles. It recognizes explicit `shortlist <product> first`, checks negation before verdict patterns, and retains no-winner outcomes for ambiguous/tied final guidance. Tests reverse the product names to ensure the logic does not favor TiDB.

The `compcomp_001` regression captures the earlier conditional Aurora choice followed by the final TiDB-first shortlist. `compcomp_018` is **not** rewritten to make TiDB win. The metadata overlay marks it `comparison_eligible=false`, `comparison_review_status=needs_review`, with an explicit scope-mismatch reason. Its original question and detected winner remain available for audit; excluded answers leave the competitive KPI denominator. Reports show total, excluded, eligible-no-winner and detected-winner counts.

A reviewer should decide whether to retain that temporary/preview-versus-production comparison, or add a correctly scoped production comparison under a new ID. This PR does not certify the model's product claims or automatically approve a replacement prompt. Remove/update the review override through a reviewed change when that decision is made.

## Validation and operational boundaries

Offline regression tests cover coverage reconciliation, review gates, inconclusive processing, exact seven-prompt retagging, stable IDs, repeat generation, provider-independent selection, Markdown, final guidance, conditional ties, negation, legitimate competitor wins and excluded-comparison denominators. No paid answer collection or live judge calls are needed to run these tests.

The original run is preserved. To see corrected scores, rescore a **copy** of the saved local run, retaining the original output directory and recording the new code/metadata revision. A plain report refresh can explain saved semantic judgments; applying a new comparison extractor requires rescoring from saved raw answers. Enabling `FACT_JUDGE=live` may incur charges on cache misses, so review that explicitly. Do not claim a new accuracy percentage or win rate until the revised outputs have been generated and reviewed.
