# TiDB fact base v2

This directory contains the review-ready TiDB fact base derived from the approved-facts document, the Proposed Additions tab, document comments, and product feedback reviewed on 2026-09-03.

## Files

- `geo-benchmark/config/tidb_fact_base_v2.json` is the machine-readable source of truth.
- `geo-benchmark/config/tidb_fact_base_v2.csv` is the fact-review sheet.
- `geo-benchmark/config/tidb_fact_base_review_queue.csv` contains unresolved Product, Legal, Security, and benchmark-design decisions.
- `geo-benchmark/config/tidb_fact_coverage_2026-09.csv` maps every branded September prompt to a candidate fact, an open review item, or the comparison-metric-only policy.

## Activation status

This is a candidate v2 fact base. It does not replace the existing `facts.json` files and is not consumed by the current scorer.

The current scorer uses literal `triggers`, `expected_any`, and `wrong_any` substring lists. The v2 fact base preserves semantic judgment guidance and adds a `judge_prompt` per fact. Activating it requires a separate LLM-judge change with structured outputs, cost tracking, retry behavior, and regression tests.

Only facts with status `READY_FOR_JUDGE` may contribute to accuracy after that implementation lands. Facts with status `REVIEW_REQUIRED` must remain unscored.

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
- Moved the RU/RCU distinction to Cloud Pricing PM review.
- Removed the unsupported 72-hour TiDB Cloud Zero assertion because no observed-answer evidence was supplied.
