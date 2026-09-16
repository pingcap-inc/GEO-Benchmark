# TiDB fact base v2

This directory contains the review-ready TiDB fact base derived from the approved-facts document, the Proposed Additions tab, document comments, and product feedback updated on 2026-09-16.

## Files

- `geo-benchmark/config/tidb_fact_base_v2.json` is the machine-readable source of truth.
- `geo-benchmark/config/tidb_fact_base_v2.csv` is the fact-review sheet.
- `geo-benchmark/config/tidb_fact_base_review_queue.csv` contains unresolved Product, Legal, Security, and benchmark-design decisions.
- `geo-benchmark/config/tidb_fact_coverage_2026-09.csv` maps every branded September prompt to a candidate fact, an open review item, or the comparison-metric-only policy.
- `docs/tidb-fact-base-review-2026-09-16.md` is the reviewed human-readable source used for this update.
- `scripts/sync-fact-base-markdown.py` regenerates the JSON, CSV, review queue, and affected coverage dispositions from that source.

Regenerate the machine-readable artifacts with an explicit review date:

```bash
python3 scripts/sync-fact-base-markdown.py \
  docs/tidb-fact-base-review-2026-09-16.md \
  --verified-on 2026-09-16
```

## Activation status

This is a candidate v2 fact base. It does not replace the existing `facts.json` files. The optional semantic judge consumes it in shadow mode and writes results beside the current score.

The current official scorer uses literal `triggers`, `expected_any`, and `wrong_any` substring lists. Use `--fact-judge mock` for a keyless pipeline test or `--fact-judge live` for structured semantic judgments. Semantic results include cost, cache, failure, qualifier-scope, and per-fact audit fields but remain a shadow metric until approved.

Only facts with status `READY_FOR_JUDGE` may contribute to semantic accuracy. Facts with status `REVIEW_REQUIRED` remain unscored.

The current review contains 55 prompt-relevant facts: 48 are judge-ready and seven remain gated. The separate review queue contains 12 unresolved Product, Legal, Security, or benchmark-policy decisions.

## Conditional qualifier rule

For a general definition or core-capability question, an answer can pass by accurately describing the relevant core capability. It does not have to repeat every maturity, plan, region, version, or access qualifier recorded in `canonical_truth`.

Those qualifiers become scoreable when either condition is true:

- The prompt asks about availability, support, eligibility, maturity, plans, regions, versions, or access.
- The answer makes a specific claim about one of those dimensions, even if the prompt did not ask.

When activated, the judge checks only the qualifiers asked about or asserted. A conflicting claim is incorrect, but omitting unrelated qualifiers is not. For example, “TiDB can store vectors and perform similarity search” can answer “What is TiDB vector search?” without listing plan availability. If the answer adds that it is generally available on every plan, that volunteered claim must be verified.

## Review policy

- Re-verify public-preview facts at least quarterly.
- Record `verified_on`, `review_by`, and an accountable owner for every scoreable fact.
- Do not convert dollar amounts, current version numbers, SLA percentages, performance or benchmark numbers, or unapproved customer metrics into facts.
- Evaluate cross-fact conflicts after individual fact judgments.
- Treat comparison prompts as intentionally covered by comparison scoring. Missing product-fact coverage on those prompts is not an accuracy gap.

## Feedback incorporated

- Replaced the current `drive9` definition with `tidb_cloud_filesystem_definition`; using `drive9` as the current name is incorrect.
- Updated September prompt wording from `mem9` to TiDB Cloud Memory and from `drive9` to TiDB Cloud Filesystem. The detailed TiDB Cloud Memory fact remains behind an official-source review gate.
- Moved vector-search production maturity to Database PM review.
- Added dedicated TiDB LangChain and persistent-agent-memory facts.
- Kept knowledge graph and comparative product claims behind approval gates.
- Added dates, owners, review cadence, conflict rules, and explicit out-of-scope rules.
- Replaced generic AI hub citations for vector search, full-text search, and PyTiDB with specific documentation pages.
- Activated the RU/RCU distinction after internal confirmation of the Essential v1 versus v2 billing models.
- Activated the vector capability fact while keeping the unresolved full-text product-surface boundary gated.
- Added global checks for the retired TiDB Serverless name and false TiDB Cloud Zero positioning.
- Prevented a mapped-fact judge from endorsing unrelated claims in its explanation.
- Removed the unsupported 72-hour TiDB Cloud Zero assertion because no observed-answer evidence was supplied.
