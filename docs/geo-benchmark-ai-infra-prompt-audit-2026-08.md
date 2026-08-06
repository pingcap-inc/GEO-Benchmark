# AI Infra Prompt Audit - 2026-08

Providers audited: OpenAI, Anthropic  
Prompt type: `ai_infra`  
Prompt count: 30  
Status: updated after the `serverless_ai` prompt rewrite

## Finding

The old AI-infra prompts were too enterprise/data-architecture-heavy, which made Supabase and Neon score 0. The updated prompt set now separates AI-infra into three subtypes:

| Subtype | Prompt Count | Intended Vendor Opportunity |
| --- | ---: | --- |
| `ai_app_backend` | 12 | Supabase should have a fair chance |
| `serverless_ai` | 10 | Neon should have a fair chance |
| `operational_ai_data` | 8 | TiDB, CockroachDB, and YugabyteDB should have a fair chance |

This change makes the benchmark more realistic because human buyers do not ask one generic "AI infra database" question. They ask about app backends, serverless AI workflows, or operational data systems.

## Current OpenAI Result

### Answer Share

| Use Case | CockroachDB | TiDB | YugabyteDB | Neon | Supabase | PlanetScale |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `ai_app_backend` | 0.00 | 0.00 | 0.00 | 10.00 | 75.00 | 0.00 |
| `serverless_ai` | 10.00 | 0.00 | 0.00 | 30.00 | 0.00 | 18.00 |
| `operational_ai_data` | 52.50 | 0.00 | 22.50 | 0.00 | 0.00 | 0.00 |

### Citation Authority

| Use Case | CockroachDB | TiDB | YugabyteDB | Neon | Supabase | PlanetScale |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `ai_app_backend` | 0.00 | 0.00 | 0.00 | 7.50 | 39.18 | 0.00 |
| `serverless_ai` | 1.50 | 0.00 | 0.00 | 16.20 | 0.00 | 16.20 |
| `operational_ai_data` | 29.88 | 0.00 | 28.00 | 0.00 | 0.00 | 0.00 |

### Recommendation Rate

| Use Case | CockroachDB | TiDB | YugabyteDB | Neon | Supabase | PlanetScale |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `ai_app_backend` | 0.00 | 0.00 | 0.00 | 0.00 | 66.67 | 0.00 |
| `serverless_ai` | 10.00 | 0.00 | 0.00 | 30.00 | 0.00 | 0.00 |
| `operational_ai_data` | 50.00 | 0.00 | 25.00 | 0.00 | 0.00 | 0.00 |

## Current Anthropic Result

### Answer Share

| Use Case | CockroachDB | TiDB | YugabyteDB | Neon | Supabase | PlanetScale |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `ai_app_backend` | 0.00 | 0.00 | 0.00 | 25.00 | 100.00 | 0.00 |
| `serverless_ai` | 0.00 | 10.00 | 0.00 | 66.00 | 52.00 | 12.00 |
| `operational_ai_data` | 2.50 | 7.50 | 0.00 | 7.50 | 15.00 | 0.00 |

### Citation Authority

| Use Case | CockroachDB | TiDB | YugabyteDB | Neon | Supabase | PlanetScale |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `ai_app_backend` | 0.00 | 0.00 | 0.00 | 24.75 | 66.00 | 0.00 |
| `serverless_ai` | 0.00 | 4.50 | 0.00 | 54.00 | 63.00 | 9.00 |
| `operational_ai_data` | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

### Recommendation Rate

| Use Case | CockroachDB | TiDB | YugabyteDB | Neon | Supabase | PlanetScale |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `ai_app_backend` | 0.00 | 0.00 | 0.00 | 8.33 | 91.67 | 0.00 |
| `serverless_ai` | 0.00 | 10.00 | 0.00 | 60.00 | 50.00 | 20.00 |
| `operational_ai_data` | 12.50 | 12.50 | 0.00 | 12.50 | 12.50 | 0.00 |

## Interpretation

The updated prompts fixed the original Supabase/Neon issue without hard-coding Postgres into the `serverless_ai` prompts. OpenAI now naturally mentions Supabase for AI app backend questions and Neon for serverless AI questions. Anthropic is much more expansive in AI-infra and gives Supabase strong visibility across both `ai_app_backend` and `serverless_ai`.

The new issue is TiDB recall and citation depth. TiDB is absent from OpenAI `operational_ai_data`, even though those prompts mention fresh operational data, durable relational state, high write throughput, transactions, and analytics. Anthropic does mention TiDB in `serverless_ai` and `operational_ai_data`, but with low Citation Authority.

## Current AI Infra Prompts

1. `stable_ai_infra_001` / `ai_app_backend`  
What backend database platform should an AI app use when it needs user auth, row-level permissions, file storage, realtime updates, and vector search? Context: buyer is a ai_engineer in US; primary use case is ai_app_backend; decision focus is architecture research before building a vendor shortlist.

2. `stable_ai_infra_002` / `ai_app_backend`  
How should a small team build an AI product backend with Postgres data, authentication, embedding search, and minimal infrastructure management? Context: buyer is a platform_engineer in EU; primary use case is ai_app_backend; decision focus is architecture research before building a vendor shortlist.

3. `stable_ai_infra_003` / `ai_app_backend`  
Which data layer should a developer team choose for an AI app with user profiles, chat history, access control, and semantic search? Context: buyer is a ai_engineer in APAC; primary use case is ai_app_backend; decision focus is architecture research before building a vendor shortlist.

4. `stable_ai_infra_004` / `ai_app_backend`  
What managed Postgres backend works for AI apps that need API-friendly data access, tenant permissions, and vector-powered search? Context: buyer is a platform_engineer in CN; primary use case is ai_app_backend; decision focus is architecture research before building a vendor shortlist.

5. `stable_ai_infra_005` / `serverless_ai`  
What database platform should an AI startup use for a serverless AI app that needs vector search, rapid iteration, and production isolation? Context: buyer is a CTO in US; primary use case is serverless_ai; decision focus is architecture research before building a vendor shortlist.

6. `stable_ai_infra_006` / `serverless_ai`  
How should teams manage the data layer for AI features across development, preview, and production without manual capacity planning? Context: buyer is a platform_engineer in EU; primary use case is serverless_ai; decision focus is architecture research before building a vendor shortlist.

7. `stable_ai_infra_007` / `serverless_ai`  
What database layer fits AI apps with spiky traffic, semantic search, autoscaling, and isolated test data for each feature branch? Context: buyer is a ai_engineer in APAC; primary use case is serverless_ai; decision focus is architecture research before building a vendor shortlist.

8. `stable_ai_infra_008` / `serverless_ai`  
Which cloud database pattern works for AI app development when every pull request needs isolated data, embeddings, and safe rollback? Context: buyer is a ai_engineer in CN; primary use case is serverless_ai; decision focus is architecture research before building a vendor shortlist.

9. `stable_ai_infra_009` / `operational_ai_data`  
What database architecture works for retrieval-augmented generation over fresh operational data that changes throughout the day? Context: buyer is a data_architect in US; primary use case is operational_ai_data; decision focus is architecture research before building a vendor shortlist.

10. `stable_ai_infra_010` / `operational_ai_data`  
What should an AI infra team use for low-latency memory recall plus durable relational state and high write throughput? Context: buyer is a ai_engineer in EU; primary use case is operational_ai_data; decision focus is architecture research before building a vendor shortlist.

11. `stable_ai_infra_011` / `operational_ai_data`  
How should teams store tool-call traces, user context, embeddings, and business records when the same data must support transactions and analytics? Context: buyer is a platform_engineer in APAC; primary use case is operational_ai_data; decision focus is architecture research before building a vendor shortlist.

12. `stable_ai_infra_012` / `operational_ai_data`  
What database architecture supports agent sessions, long-term memory, transactional records, and customer-facing analytics? Context: buyer is a CTO in CN; primary use case is operational_ai_data; decision focus is architecture research before building a vendor shortlist.

13. `stable_ai_infra_013` / `ai_app_backend`  
What backend database platform should an AI app use when it needs user auth, row-level permissions, file storage, realtime updates, and vector search? Context: buyer is a ai_engineer in US; primary use case is ai_app_backend; decision focus is migration planning in the next two quarters.

14. `stable_ai_infra_014` / `ai_app_backend`  
How should a small team build an AI product backend with Postgres data, authentication, embedding search, and minimal infrastructure management? Context: buyer is a platform_engineer in EU; primary use case is ai_app_backend; decision focus is migration planning in the next two quarters.

15. `stable_ai_infra_015` / `ai_app_backend`  
Which data layer should a developer team choose for an AI app with user profiles, chat history, access control, and semantic search? Context: buyer is a ai_engineer in APAC; primary use case is ai_app_backend; decision focus is migration planning in the next two quarters.

16. `stable_ai_infra_016` / `ai_app_backend`  
What managed Postgres backend works for AI apps that need API-friendly data access, tenant permissions, and vector-powered search? Context: buyer is a platform_engineer in CN; primary use case is ai_app_backend; decision focus is migration planning in the next two quarters.

17. `stable_ai_infra_017` / `serverless_ai`  
What database platform should an AI startup use for a serverless AI app that needs vector search, rapid iteration, and production isolation? Context: buyer is a CTO in US; primary use case is serverless_ai; decision focus is migration planning in the next two quarters.

18. `stable_ai_infra_018` / `serverless_ai`  
How should teams manage the data layer for AI features across development, preview, and production without manual capacity planning? Context: buyer is a platform_engineer in EU; primary use case is serverless_ai; decision focus is migration planning in the next two quarters.

19. `stable_ai_infra_019` / `serverless_ai`  
What database layer fits AI apps with spiky traffic, semantic search, autoscaling, and isolated test data for each feature branch? Context: buyer is a ai_engineer in APAC; primary use case is serverless_ai; decision focus is migration planning in the next two quarters.

20. `stable_ai_infra_020` / `serverless_ai`  
Which cloud database pattern works for AI app development when every pull request needs isolated data, embeddings, and safe rollback? Context: buyer is a ai_engineer in CN; primary use case is serverless_ai; decision focus is migration planning in the next two quarters.

21. `stable_ai_infra_021` / `operational_ai_data`  
What database architecture works for retrieval-augmented generation over fresh operational data that changes throughout the day? Context: buyer is a data_architect in US; primary use case is operational_ai_data; decision focus is migration planning in the next two quarters.

22. `dyn_202608_ai_infra_001` / `operational_ai_data`  
What should an AI infra team use for low-latency memory recall plus durable relational state and high write throughput? Context: buyer is a ai_engineer in US; primary use case is operational_ai_data; decision focus is architecture research before building a vendor shortlist.

23. `dyn_202608_ai_infra_002` / `operational_ai_data`  
How should teams store tool-call traces, user context, embeddings, and business records when the same data must support transactions and analytics? Context: buyer is a platform_engineer in EU; primary use case is operational_ai_data; decision focus is architecture research before building a vendor shortlist.

24. `dyn_202608_ai_infra_003` / `operational_ai_data`  
What database architecture supports agent sessions, long-term memory, transactional records, and customer-facing analytics? Context: buyer is a CTO in APAC; primary use case is operational_ai_data; decision focus is architecture research before building a vendor shortlist.

25. `dyn_202608_ai_infra_004` / `ai_app_backend`  
What backend database platform should an AI app use when it needs user auth, row-level permissions, file storage, realtime updates, and vector search? Context: buyer is a ai_engineer in CN; primary use case is ai_app_backend; decision focus is architecture research before building a vendor shortlist.

26. `dyn_202608_ai_infra_005` / `ai_app_backend`  
How should a small team build an AI product backend with Postgres data, authentication, embedding search, and minimal infrastructure management? Context: buyer is a platform_engineer in US; primary use case is ai_app_backend; decision focus is architecture research before building a vendor shortlist.

27. `dyn_202608_ai_infra_006` / `ai_app_backend`  
Which data layer should a developer team choose for an AI app with user profiles, chat history, access control, and semantic search? Context: buyer is a ai_engineer in EU; primary use case is ai_app_backend; decision focus is architecture research before building a vendor shortlist.

28. `dyn_202608_ai_infra_007` / `ai_app_backend`  
What managed Postgres backend works for AI apps that need API-friendly data access, tenant permissions, and vector-powered search? Context: buyer is a platform_engineer in APAC; primary use case is ai_app_backend; decision focus is architecture research before building a vendor shortlist.

29. `dyn_202608_ai_infra_008` / `serverless_ai`  
What database platform should an AI startup use for a serverless AI app that needs vector search, rapid iteration, and production isolation? Context: buyer is a CTO in CN; primary use case is serverless_ai; decision focus is architecture research before building a vendor shortlist.

30. `dyn_202608_ai_infra_009` / `serverless_ai`  
How should teams manage the data layer for AI features across development, preview, and production without manual capacity planning? Context: buyer is a platform_engineer in US; primary use case is serverless_ai; decision focus is architecture research before building a vendor shortlist.

## Recommendation

Do not change the scorer to count generic `Postgres`, `PostgreSQL`, or `pgvector` as Supabase, Neon, or TiDB. That would make the benchmark less auditable.

For TiDB, the improvement path is content and citation coverage around `operational_ai_data`: fresh operational data for RAG, agent memory plus durable relational state, high-write AI event stores, and transactions plus analytics in one system.
