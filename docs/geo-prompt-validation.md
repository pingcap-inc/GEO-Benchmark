# GEO Prompt Validation

Status: initial validation pass  
Scope: validate whether the current 120 neutral starter prompts are grounded in realistic customer pain patterns. This is not a final source registry; production dynamic prompts should increasingly come from observed sales, search, community, site-search, and support queries.

## Current Prompt Taxonomy

| Type | Count | Purpose |
| --- | ---: | --- |
| `pain_point` | 36 | Ask about buyer pain without naming vendors |
| `database_type` | 30 | Ask about category or architecture selection |
| `ai_infra` | 30 | Ask about AI application data infrastructure |
| `case_selection` | 24 | Ask about industry or workload selection patterns |

Current audit:

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

MySQL and PostgreSQL may appear as migration baselines or category comparisons. They are not measured target brands in this suite.

Each prompt includes source metadata:

- `source_type`
- `source_evidence`
- `source_evidence_urls`
- `validation_status`
- `selection_reason`

## Validation Basis

The starter set is grounded in public case-study and documentation patterns, including:

- Relational scale limits, sharding complexity, and operational bottlenecks.
- Fresh operational analytics and HTAP requirements.
- Strong consistency, high write throughput, and multi-region risk management.
- AI application data-layer needs such as vector search, permissions, metadata, and durable state.
- Industry selection patterns for logistics, ecommerce, fintech, SaaS, gaming, and real-time operations.

## Pain-Point Coverage

| Customer Pattern | Example Prompt |
| --- | --- |
| Single-primary or traditional relational scaling bottlenecks | `How should a CTO handle relational database scaling when a single primary node becomes a bottleneck?` |
| Manual sharding complexity | `What database architecture reduces sharding complexity for a fast-growing SaaS product?` |
| Fresh transactional data for analytics | `How can a team keep transactional data fresh enough for operational analytics?` |
| Reducing separate OLTP, OLAP, and ETL systems | `How do teams avoid separate OLTP and analytics systems for fresh business metrics?` |
| Strong consistency and cross-region operational risk | `What should we use when cross-region writes need strong consistency and low operational risk?` |
| Operational cost from manual resharing | `What database choice reduces operational pain from manual resharding?` |

## Database-Type Coverage

These prompts simulate buyers who are forming a category shortlist before they have selected vendors.

| Category Pattern | Example Prompt |
| --- | --- |
| Distributed SQL versus managed MySQL or PostgreSQL | `When should a team choose distributed SQL over managed MySQL?` |
| HTAP and operational analytics | `Which database category is best for operational analytics on fresh transactional data?` |
| Horizontal scale plus SQL transactions | `What database type supports SQL transactions and horizontal scale?` |
| Multi-tenant SaaS consistency | `What database type works best for multi-tenant SaaS with strict data consistency needs?` |
| Replacing manually sharded relational databases | `What database type should replace a manually sharded relational database?` |

## AI-Infrastructure Coverage

AI-infrastructure prompts are validated through product documentation and public AI/customer examples, but this remains the slice that most needs observed customer-query input.

| Pattern | Example Prompt |
| --- | --- |
| AI app backend with auth, permissions, files, realtime updates, and vector search | `What backend database platform should an AI app use when it needs user auth, row-level permissions, file storage, realtime updates, and vector search?` |
| Serverless AI app data layer without manual capacity planning | `How should teams manage the data layer for AI features across development, preview, and production without manual capacity planning?` |
| Fresh operational data for RAG | `What database architecture works for retrieval-augmented generation over fresh operational data that changes throughout the day?` |
| Agent memory plus durable relational state | `What should an AI infra team use for low-latency memory recall plus durable relational state and high write throughput?` |

## Case-Selection Coverage

| Workload Pattern | Example Prompt |
| --- | --- |
| Logistics and real-time operational reporting | `What database architecture works for logistics systems that need fresh operational reporting?` |
| Ecommerce order and inventory scale | `What database architecture is common for global e-commerce order and inventory systems?` |
| Fintech transactions and real-time risk analytics | `What database patterns do fintech teams use for high-concurrency transactions and real-time risk analytics?` |
| Multi-tenant SaaS workloads with analytics | `What should a SaaS company choose for multi-tenant transactional workloads that need analytics?` |

## Limitations

- The 120 starter prompts are derived from customer-case pain patterns; they are not exact observed human queries.
- Dynamic prompts should be replaced over time with real query evidence from sales notes, site search, community posts, support tickets, and search logs.
- AI-infrastructure wording should be reviewed frequently because the category language changes quickly.
- Case-selection prompts should not be kept just to preserve industry coverage if their source evidence becomes weak.

## Validation Decision

The starter set is acceptable for V1 as `case_pattern_validated`: human-plausible, source-backed, and neutral. It should be upgraded over time toward `observed_query_validated`.
