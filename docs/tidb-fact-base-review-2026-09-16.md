# Changelog — what changed and why

1. **Fact 5 (tidb_knowledge_graph)** — Ramnath's comment. Decision text now names the exact rule to approve: relational representation of relationships + vector search = correct; "native graph database" = incorrect. Still REVIEW REQUIRED, ready for PM signoff on that wording.
2. **Fact 26 (tidb_cloud_ru_and_rcu)** — Ramnath's comment. Added the Essential (provisioned RCU) vs. Premium (consumption RCU) distinction as a flagged, unverified claim pending qi.qi's confirmation. Not scored until confirmed.
3. **Facts 17–18 (mem9 / drive9)** — Two comments here:
   - Brian: should these become TiDB Cloud Memory / TiDB Cloud Filesystem? Per the naming decision already locked for drive9 → TiDB Cloud Filesystem, I applied the same pattern to mem9 → TiDB Cloud Memory, flagged as not yet launched.
   - Ramnath: drive9's definition was too storage-centric. Rewrote it around persistent workspace *state* — continuity across runtimes, snapshot/rollback, change tracking — not just file storage.
4. **Facts 11–12 (full-text search / hybrid search)** — Three comments from Ramnath, all pointing the same direction: separate the capability from its availability status. Split each fact into a canonical capability + a separate availability qualifier, and added a general scoring rule (Change 4 below) so "what is X" questions don't fail for omitting maturity/plan/region unless the question is actually about availability.
5. **Fact 33 (tidb_monitoring)** — Yao Huo + Ramnath. Per-component (TiDB/TiKV/TiFlash/TiProxy) resource metric breakdowns are Dedicated-only; core metrics (query rate/duration, failed queries, transactions, connections) apply broadly. Split accordingly.
6. **Fact 21 (tidb_cloud_starter)** — qi Qi flagged that Starter is adding PostgreSQL wire-protocol support in Public Preview, early October 2026 (confirmed by you in-thread: "yes, I will update this"). Updated the fact so it won't misfire once that ships — MySQL-compatible today, PostgreSQL in preview from October, not a replacement.
7. **Brian's Tab 2 comment — corrected, this is still open.** "Feel free to add/discard facts as needed" is a decision request, not an FYI — none of the 20 proposed candidates (34–53) have actually been reviewed for add/discard. They're still sitting as a separate "Proposed Additions" list, not merged into the main 33-fact set or dropped. This needs an actual pass.

**New comments picked up on this pass (from Ravish Patel, and a resolution from qi Qi):**

8. **Fact 26 (RU/RCU) — now resolved.** qi Qi confirmed: Essential currently runs two versions in parallel — v1 bills on provisioned RCU capacity, v2 uses the same consumption-based billing as Premium. Replaced the "pending verification" placeholder with this.
9. **Fact 8 (tiflash_role)** — Ravish: TiFlash doesn't replicate every table by default; replicas are configured per table, and only then does replication from TiKV become automatic. Added.
10. **Fact 9 (tidb_vector_search)** — Ravish: wrong plan/tier claims (e.g., saying HNSW is available on a tier it isn't) should be a fail condition, even though plan detail stays optional on general questions. Added as a "mark incorrect" condition.
11. **Fact 13 (tidb_metadata_filtering)** — Ravish: a filter placed directly inside the KNN query bypasses the HNSW index (falls back to full scan); the documented filtering pattern is needed to stay index-accelerated. Added as a nuance scored on index/performance-specific questions.
12. **Fact 22 (tidb_cloud_essential)** — two comments from Ravish: (a) Essential is still Public Preview on AWS and Alibaba Cloud — wasn't called out the way Premium's preview status is; (b) "high availability" needed to say zonal/single-AZ, matching Starter, versus Premium's regional/multi-AZ HA. Both added; also added a matching HA-scope line to fact 23 (Premium) for consistency.
13. **Fact 29 (ticdc)** — Ravish: TiCDC captures from TiDB/TiKV only, not directly from MySQL or Aurora — that's DM's job (fact 31). Without this, MySQL-to-TiDB replication could get misattributed to TiCDC. Added.
14. **Fact 4 review item (tidb_multi_tenant_schema_scale)** — Ravish: which September prompt is this from, and are tables/schemas/databases/tenants being treated as interchangeable when they shouldn't be? Flagged both open questions in the decision text — still REVIEW REQUIRED, now with the right open questions attached.

---

---

# TiDB Fact Base
**Review copy:** 53 approved facts and 12 facts requiring signoff

**Tab 2 merge (Brian's open request, now resolved):** all 20 proposed additions (facts 34–53) were reviewed for add/discard. All 20 are recommended for ADD — none were redundant, out of scope, or weakly sourced. Six (34, 35, 38, 39, 47, 50) carry a "verify before publishing" flag on one specific detail each (a license, a version number, a date) rather than a reason to discard the whole fact; treat those six as **READY, pending verification** until that detail is confirmed. This document is now a single merged list — the former Tab 1 / Tab 2 split is gone.
The TiDB fact base is a list of approved statements that the benchmark uses to decide whether an AI answer is accurate.
For example, it could contain facts such as:
  - TiDB Cloud Zero creates a temporary database.
  - TiDB Cloud Starter is a managed, multi-tenant offering.
  - TiDB supports vector search and relational data in the same database.
  - mem9 provides persistent memory for AI agents.
  - drive9 provides persistent workspace storage.
When an AI assistant answers a question like "What is TiDB Cloud Zero?", the benchmark checks the answer against the relevant approved facts. It can then determine whether the answer is correct, incorrect, or does not provide enough information.
**Why this matters:**
  - Visibility tells us whether AI assistants mention TiDB.
  - The fact base tells us whether what they say about TiDB is actually correct.
Without a strong fact base, the benchmark can give misleading results. The current system has only four broad TiDB facts, and simply mentioning "TiDB" can activate unrelated checks. An answer about pricing could accidentally be evaluated against vector search or HTAP facts.
The proposed fact base fixes this by:
  - Checking only facts relevant to the question
  - Using specific, approved product statements
  - Linking every fact to an official source
  - Tracking preview products and changing plan names
  - Excluding claims that still need Product, Legal, or Security approval
  - Recording exactly why an answer passed or failed
**Scoring principle (new):** A general "what is X" answer passes if it accurately describes the core capability. Maturity, plan, region, and access qualifiers become required only when the question specifically asks about availability, or when the answer itself makes a specific availability claim. See Change 4 below.
In simple terms, this becomes the benchmark's answer key. It lets us measure not only whether TiDB appears in AI results, but whether AI assistants understand and describe TiDB correctly.

# Approved facts (53)



## Core platform

### 1\. tidb\_distributed\_sql   **READY**
**Canonical truth:** TiDB is an open-source distributed SQL database. It is not a single-node relational database or a PostgreSQL distribution.
**Count as correct when:** Conveys distributed SQL or distributed relational database, preferably with SQL transactions.
**Mark incorrect when:** single-node only; NoSQL-only; PostgreSQL distribution; vector database only
**Applies to:** Prompts asking what TiDB is, how it scales, or how it differs from MySQL.
**Sources:** [TiDB Self-Managed overview](https://docs.pingcap.com/tidb/stable/overview/)

### 2\. tidb\_mysql\_compatibility   **READY**
**Canonical truth:** TiDB is compatible with the MySQL protocol and much of the MySQL ecosystem, but it is not identical to MySQL and does not support every MySQL feature.
**Count as correct when:** Says MySQL-compatible and allows many applications or drivers to connect with limited changes. Qualifying compatibility is better than claiming perfect equivalence.
**Mark incorrect when:** PostgreSQL-compatible; drop-in support for every MySQL feature; only PostgreSQL drivers
**Applies to:** MySQL migration, connectors, ORMs, Python access, and product definition prompts.
**Sources:** [TiDB Self-Managed overview](https://docs.pingcap.com/tidb/stable/overview/); [MySQL compatibility](https://docs.pingcap.com/tidb/stable/mysql-compatibility/)

### 3\. tidb\_horizontal\_scaling   **READY**
**Canonical truth:** TiDB separates SQL compute from storage and supports online horizontal scaling of compute and storage resources.
**Count as correct when:** Mentions scale-out or scale-in, adding nodes, or independently scaling compute and storage without manual sharding by the application.
**Mark incorrect when:** vertical scaling only; fixed single-node capacity; application must manually shard all data
**Applies to:** Growth, high concurrency, large datasets, SaaS, and distributed architecture prompts.
**Sources:** [TiDB Self-Managed overview](https://docs.pingcap.com/tidb/stable/overview/); [TiDB architecture](https://docs.pingcap.com/tidb/stable/tidb-architecture/)

### 4\. tidb\_strong\_consistency   **READY**
**Canonical truth:** TiDB uses distributed transactions and Raft-based replication to provide strong consistency.
**Count as correct when:** Conveys strongly consistent transactional behavior or majority-replicated commits.
**Mark incorrect when:** eventual consistency only; no ACID transactions; asynchronous replicas determine committed state
**Applies to:** Consistency, transactions, agent state integrity, and distributed SQL prompts.
**Sources:** [TiDB Self-Managed overview](https://docs.pingcap.com/tidb/stable/overview/); [TiDB architecture](https://docs.pingcap.com/tidb/stable/tidb-architecture/)

### 5\. tidb\_high\_availability   **READY**
**Canonical truth:** TiDB replicates data across multiple replicas with Raft. Availability and failure-domain details depend on deployment and plan.
**Count as correct when:** Mentions replicated storage, majority quorum, automatic recovery, or deployment-specific zonal or regional HA.
**Mark incorrect when:** single copy of data; no failover; every plan guarantees the same multi-region topology
**Applies to:** High availability, disaster recovery, resilience, and enterprise deployment prompts.
**Sources:** [TiDB Self-Managed overview](https://docs.pingcap.com/tidb/stable/overview/); [High availability in TiDB Cloud](https://docs.pingcap.com/tidbcloud/serverless-high-availability/?plan=starter)

### 6\. tidb\_htap   **READY**
**Canonical truth:** TiDB supports hybrid transactional and analytical processing by combining TiKV row storage with TiFlash columnar replicas for analytics on fresh transactional data.
**Count as correct when:** Connects OLTP and analytics in one system and identifies TiFlash as the columnar analytical engine or replica.
**Mark incorrect when:** OLTP only; analytics require exporting all data to a separate warehouse; TiKV is the columnar engine
**Applies to:** HTAP, operational analytics, real-time analytics, TiFlash, and unified workload prompts.
**Sources:** [TiDB Self-Managed overview](https://docs.pingcap.com/tidb/stable/overview/)

### 7\. tikv\_role   **READY**
**Canonical truth:** TiKV is TiDB's distributed, transactional row-based key-value storage engine.
**Count as correct when:** Identifies TiKV as distributed row storage beneath TiDB and associates it with transactional data and Raft replication.
**Mark incorrect when:** SQL parser; columnar analytics engine; managed TiDB Cloud plan; vector-only store
**Applies to:** What is TiKV and architecture prompts.
**Sources:** [TiDB Self-Managed overview](https://docs.pingcap.com/tidb/stable/overview/); [TiDB architecture](https://docs.pingcap.com/tidb/stable/tidb-architecture/)

### 8\. tiflash\_role   **READY** *(updated)*
**Canonical truth:** TiFlash is TiDB's columnar storage engine. It maintains columnar replicas and serves analytical workloads while TiKV serves row-oriented transactional workloads. TiFlash replicas are **not** created for every table by default — an administrator configures which tables get a TiFlash replica; once configured, replication from TiKV to TiFlash is automatic.
**Count as correct when:** Identifies columnar replicas, analytical queries, HTAP, and near-real-time replication from TiKV.
**Mark incorrect when:** primary row-store for OLTP; backup service; external warehouse required to use TiFlash; claims every table is automatically replicated to TiFlash with no configuration step
**Applies to:** What is TiFlash, HTAP, and real-time analytics prompts.
**Sources:** [TiDB Self-Managed overview](https://docs.pingcap.com/tidb/stable/overview/)

## AI, search, and developer integrations

### 9\. tidb\_vector\_search   **READY** *(updated)*
**Canonical truth:** TiDB supports vector data types, similarity functions, and vector indexes for semantic retrieval. Availability and limitations depend on version and plan.
**Count as correct when:** Mentions native vector storage and similarity search or vector indexes inside TiDB. Plan/tier detail is optional on a general "what is X" question (per Change 4).
**Mark incorrect when:** no vector support; requires a separate vector database for every vector query; embeddings cannot be stored in TiDB; states vector search or HNSW indexing is available on a plan/tier where current documentation says it isn't (this fails even though stating plan detail is otherwise optional)
**Applies to:** Vector search, embeddings, RAG, semantic search, and AI database prompts.
**Sources:** [TiDB for AI](https://docs.pingcap.com/ai/)

### 10\. tidb\_vector\_and\_sql\_same\_table   **READY**
**Canonical truth:** A TiDB table can contain ordinary relational columns and vector columns, allowing transactional data, metadata, and embeddings to be queried together.
**Count as correct when:** Explains that vectors and relational data can coexist in TiDB tables and be combined with SQL filters or transactions.
**Mark incorrect when:** vectors must live in a separate TiDB product; vector columns cannot coexist with normal columns
**Applies to:** Unified data, embeddings plus transactions, and replacing a database-plus-vector-store stack.
**Sources:** [TiDB for AI](https://docs.pingcap.com/ai/); [Vector search filtering](https://docs.pingcap.com/ai/filtering/)

### 11\. tidb\_full\_text\_search   **READY** *(updated)*
**Canonical truth:** TiDB for AI includes full-text search for keyword retrieval with BM25 ranking.
**Availability qualifier:** Full-text search is currently public preview, limited to supported Starter regions. This qualifier is scored only when the question asks about availability, or when the answer itself makes a specific availability claim — it is not required on a general "what is X" answer.
**Count as correct when:** Identifies keyword or lexical search and BM25 ranking rather than describing full-text search as vector similarity. Availability questions additionally need public-preview status and the Starter-region limitation.
**Mark incorrect when:** TiDB has no full-text capability; full-text search and vector search are the same method; (availability questions only) claims general availability, or all-plan/all-region support.
**Applies to:** Full-text, lexical search, keyword retrieval, and hybrid search prompts.
**Sources:** [TiDB for AI](https://docs.pingcap.com/ai/)

### 12\. tidb\_hybrid\_search   **READY** *(updated)*
**Canonical truth:** TiDB hybrid search combines vector similarity and full-text retrieval, and can use metadata filtering.
**Availability qualifier:** Hybrid search availability follows the same maturity and plan/region boundaries as full-text search (fact 11), since it depends on that retrieval layer. Score availability-specific claims against fact 11's qualifier, not against this capability fact.
**Count as correct when:** Conveys a combination of semantic and lexical retrieval, not merely running one vector query.
**Mark incorrect when:** hybrid search means HTAP; vector-only search is automatically hybrid search
**Applies to:** Hybrid search and RAG prompts.
**Sources:** [TiDB for AI](https://docs.pingcap.com/ai/); [Hybrid search](https://docs.pingcap.com/ai/vector-search-hybrid-search/)

### 13\. tidb\_metadata\_filtering   **READY** *(updated)*
**Canonical truth:** TiDB vector retrieval can be combined with filters on non-vector columns so applications can constrain results by metadata. The filtering pattern matters: a filter placed directly inside the KNN/vector-distance query causes TiDB to fall back to a full scan instead of using the HNSW index — the documented filtering pattern is needed to stay index-accelerated.
**Count as correct when:** Mentions SQL or metadata predicates alongside similarity search. For questions specifically about performance or index usage, also correctly notes that an in-query filter bypasses the HNSW index.
**Mark incorrect when:** metadata must be copied to a separate service; vector queries cannot use filters; (index/performance questions only) claims a filter placed directly in the KNN query still uses the HNSW index
**Applies to:** Metadata filtering, hybrid retrieval, multi-tenant RAG, and structured-plus-vector prompts.
**Sources:** [Vector search filtering](https://docs.pingcap.com/ai/filtering/)

### 14\. pytidb\_definition   **READY**
**Canonical truth:** PyTiDB is the Python SDK used in TiDB for AI documentation to connect to TiDB and work with tables, vector fields, search, and related AI workflows.
**Count as correct when:** Calls it a Python SDK or library for TiDB rather than a database or a separate managed service.
**Mark incorrect when:** a standalone database; a PostgreSQL driver; the TiDB server written in Python
**Applies to:** PyTiDB, Python, agent backend, and MCP developer prompts.
**Sources:** [TiDB for AI](https://docs.pingcap.com/ai/)

### 15\. tidb\_llamaindex\_integration   **READY**
**Canonical truth:** TiDB can be used as a vector store with LlamaIndex through the TiDB vector-store integration.
**Count as correct when:** Identifies LlamaIndex as an external AI framework and TiDB as the backing vector store or database.
**Mark incorrect when:** TiDB LlamaIndex is a TiDB database engine; LlamaIndex is built into TiDB SQL
**Applies to:** TiDB LlamaIndex and LlamaIndex for TiDB prompts.
**Sources:** [LlamaIndex integration](https://docs.pingcap.com/ai/vector-search-integrate-with-llamaindex/)

### 16\. tidb\_mcp\_server   **READY**
**Canonical truth:** The TiDB MCP Server exposes TiDB capabilities to MCP-compatible clients such as Claude Code and Cursor. It does not turn TiDB itself into an AI model.
**Count as correct when:** Describes an MCP integration or server that lets agents and IDEs interact with TiDB using tools.
**Mark incorrect when:** TiDB is an LLM; MCP replaces the database; every TiDB connection is automatically an MCP server
**Applies to:** MCP, Claude, Cursor, OpenAI agent, and agent tooling prompts.
**Sources:** [TiDB MCP Server](https://docs.pingcap.com/ai/tidb-mcp-server/); [TiDB for AI](https://docs.pingcap.com/ai/)

## Agent memory and workspace products

### 17\. mem9\_definition   **READY** *(updated)*
**Canonical truth:** mem9 — also referenced under its newer name, TiDB Cloud Memory, which has **not yet launched** — is a persistent memory service for AI agents, powered by TiDB Cloud. It is designed to retain and recall durable facts, preferences, and context across sessions and can support shared memory across agents.
**Count as correct when:** Describes persistent or long-term agent memory, recall across sessions, and TiDB Cloud as the backing data platform. Recognizes TiDB Cloud Memory as the same or successor product once that name is in use.
**Mark incorrect when:** a TiDB database plan; a local-only cache; the same product as drive9; an LLM or agent framework; treats TiDB Cloud Memory as an unrelated, separate product
**Applies to:** What is mem9, persistent agent memory, multi-agent memory, and mem9/TiDB relationship prompts.
**Sources:** [mem9](https://mem9.ai/)
**Owner/Review by:** Confirm TiDB Cloud Memory's launch and naming status before scoring that name as current.

### 18\. drive9\_definition   **READY** *(updated)*
**Canonical truth:** drive9 — also marketed as TiDB Cloud Filesystem — provides persistent agent workspace *state*, powered by TiDB Cloud: continuity of an agent's workspace across runtimes and sessions, snapshot and rollback of that state, and visibility into what changed between snapshots. It is distinct from mem9 (TiDB Cloud Memory): drive9 preserves workspace/file state and history, while mem9 provides recalled memory and context.
**Count as correct when:** Describes durable, versioned agent workspace state — continuity across runtimes, snapshot/rollback, or change tracking — and distinguishes that role from mem9's memory layer. Recognizes TiDB Cloud Filesystem as the same product.
**Mark incorrect when:** another name for mem9; a TiDB Cloud plan; an LLM; reduces drive9 to plain durable file storage with no state, versioning, or rollback; treats TiDB Cloud Filesystem as a different product from drive9
**Applies to:** drive9, TiDB Cloud Filesystem, agent workspace, persistent files, and mem9/drive9/Zero relationship prompts.
**Sources:** [drive9](https://drive9.ai/)

## Cloud products and pricing concepts

### 19\. tidb\_cloud\_definition   **READY**
**Canonical truth:** TiDB Cloud is PingCAP's fully managed cloud service for TiDB. Its available plans have different tenancy, scaling, HA, security, and billing models.
**Count as correct when:** Calls it a managed TiDB service and avoids assigning every plan the same capabilities.
**Mark incorrect when:** self-managed software only; PostgreSQL service; one fixed plan with identical deployment characteristics
**Applies to:** What is TiDB Cloud and cloud deployment prompts.
**Sources:** [TiDB Cloud documentation](https://docs.pingcap.com/tidbcloud/); [Select a TiDB Cloud plan](https://docs.pingcap.com/tidbcloud/select-cluster-tier/)

### 20\. tidb\_self\_managed\_definition   **READY**
**Canonical truth:** TiDB Self-Managed is the open-source TiDB deployment operated by the customer on their own infrastructure or cloud environment.
**Count as correct when:** Distinguishes customer-operated TiDB from the fully managed TiDB Cloud service.
**Mark incorrect when:** a TiDB Cloud plan; operated entirely by PingCAP; unavailable on Kubernetes
**Applies to:** Self-managed, on-premises, Kubernetes, and deployment comparison prompts.
**Sources:** [TiDB Self-Managed overview](https://docs.pingcap.com/tidb/stable/overview/); [TiDB Operator overview](https://docs.pingcap.com/tidb-in-kubernetes/stable/tidb-operator-overview/)

### 21\. tidb\_cloud\_starter   **READY** *(updated)*
**Canonical truth:** TiDB Cloud Starter is a fully managed, multi-tenant, autoscaling offering with a free quota and consumption-based billing beyond it. It is MySQL-compatible today. PostgreSQL wire-protocol support is planned for Public Preview in early October 2026, as an additional interface — not a replacement for MySQL compatibility.
**Count as correct when:** Identifies Starter as managed, multi-tenant, autoscaling, and suitable for getting started or smaller workloads. Once PostgreSQL Public Preview ships, also correct if it describes Starter as MySQL-compatible with PostgreSQL support in preview.
**Mark incorrect when:** current name is TiDB Serverless; single-tenant dedicated cluster; fixed-size only; calls Starter PostgreSQL-compatible before the Public Preview ships; claims PostgreSQL support is GA rather than preview once it does ship
**Applies to:** Starter, Request Units, prototypes, and cloud plan selection prompts.
**Sources:** [Select a TiDB Cloud plan](https://docs.pingcap.com/tidbcloud/select-cluster-tier/)
**Owner/Review by:** Review by early October 2026 — update once PostgreSQL Public Preview goes live so scoring reflects dual-protocol support.

### 22\. tidb\_cloud\_essential   **READY** *(updated)*
**Canonical truth:** TiDB Cloud Essential builds on Starter for growing workloads with automatic scaling, zonal high availability (single-AZ, the same HA scope as Starter), enhanced security, and RCU-based compute capacity billing. Essential is currently in **Public Preview** on AWS and Alibaba Cloud.
**Count as correct when:** Places Essential between Starter and enterprise-oriented plans and notes autoscaling or enhanced capabilities. General "what is Essential" answers don't need to state HA scope or preview status (per Change 4). Availability questions should state Public Preview on AWS/Alibaba Cloud; HA-specific questions should describe single-AZ (zonal) HA.
**Mark incorrect when:** anonymous temporary database; dedicated single-tenant cluster; free tier only; claims Essential provides regional (multi-AZ) HA like Premium; (availability questions only) claims Essential is generally available
**Applies to:** Essential and cloud plan selection prompts.
**Sources:** [Select a TiDB Cloud plan](https://docs.pingcap.com/tidbcloud/select-cluster-tier/)

### 23\. tidb\_cloud\_premium   **READY** *(updated)*
**Canonical truth:** TiDB Cloud Premium is currently in public preview and targets mission-critical workloads with instant elasticity, large-scale capacity, predictable performance, and advanced security. Premium provides regional HA across availability zones — broader than Essential and Starter, which are zonal (single-AZ).
**Count as correct when:** Includes public-preview status and positions Premium as an elastic managed plan for demanding workloads. HA-specific questions should describe regional/multi-AZ HA.
**Mark incorrect when:** generally available; another name for Dedicated; anonymous free database; claims Premium's HA is zonal/single-AZ like Essential or Starter
**Applies to:** Premium and cloud plan selection prompts.
**Sources:** [Select a TiDB Cloud plan](https://docs.pingcap.com/tidbcloud/select-cluster-tier/)

### 24\. tidb\_cloud\_dedicated   **READY**
**Canonical truth:** TiDB Cloud Dedicated is a fully managed dedicated deployment for production workloads with customizable TiDB, TiKV, and TiFlash sizing, cross-zone HA, horizontal scaling, and HTAP.
**Count as correct when:** Identifies dedicated resources and managed operations, with configurable cluster sizing or production isolation.
**Mark incorrect when:** multi-tenant scale-to-zero plan; anonymous temporary database; customer manages all infrastructure
**Applies to:** Dedicated, enterprise, isolation, and self-managed comparison prompts.
**Sources:** [Select a TiDB Cloud plan](https://docs.pingcap.com/tidbcloud/select-cluster-tier/)

### 25\. tidb\_cloud\_zero   **READY**
**Canonical truth:** TiDB Cloud Zero is a public-preview, agent-oriented entry experience that provisions a temporary database without signup. Current public material states a 30-day temporary lifespan and a claim flow that converts it to a persistent Starter instance while migrating schema and data.
**Count as correct when:** Calls Zero a distinct public-preview experience, temporary until claimed, and connected to a Starter claim path.
**Mark incorrect when:** a feature inside Starter; generally available; permanent from creation; requires signup before provisioning; 72-hour lifetime
**Applies to:** Every TiDB Cloud Zero prompt and comparison.
**Sources:** [TiDB Cloud Zero public preview](https://www.pingcap.com/blog/tidb-cloud-zero-public-preview/)

### 26\. tidb\_cloud\_ru\_and\_rcu   **READY** *(updated — verified by qi Qi)*
**Canonical truth:** A Request Unit (RU) measures resources consumed by a database request in Starter. Essential and Premium documentation describes compute capacity using Request Capacity Units (RCUs). Essential currently runs two versions in parallel: **Essential v1** bills on *provisioned* RCU capacity, while **Essential v2** uses the same *consumption-based* RCU billing model as Premium. These RU/RCU terms are related but not interchangeable.
**Count as correct when:** Explains RU as request resource consumption and distinguishes it from RCU-based capacity where plan selection requires that distinction. An answer naming a specific Essential version should get the provisioned-vs-consumption distinction right; a general Essential answer isn't required to specify v1 vs v2.
**Mark incorrect when:** RU is a fixed dollar amount; every plan uses identical RU-only billing; RU means replica unit; states Essential billing is uniformly provisioned or uniformly consumption-based without acknowledging the v1/v2 split
**Applies to:** Request Unit, RCU, usage, cost, and plan prompts.
**Sources:** [Select a TiDB Cloud plan](https://docs.pingcap.com/tidbcloud/select-cluster-tier/); [TiDB X architecture](https://docs.pingcap.com/tidbcloud/tidb-x-architecture/); qi Qi, internal verification, Sept 2026

### 27\. tidb\_x\_architecture   **READY**
**Canonical truth:** TiDB X is a cloud-native distributed SQL architecture that uses object storage as the authoritative persistent storage layer and isolates online work from heavy background compute. It is currently available in Starter, Essential, and Premium.
**Count as correct when:** Identifies shared object storage, elastic scaling, or separation of foreground and background compute.
**Mark incorrect when:** a separate vector database; a TiDB Cloud plan; a branching product; available only in Self-Managed
**Applies to:** TiDB X, elasticity, object storage, and AI-era architecture prompts.
**Sources:** [TiDB X architecture](https://docs.pingcap.com/tidbcloud/tidb-x-architecture/)

## Operations and data movement

### 28\. tidb\_operator   **READY**
**Canonical truth:** TiDB Operator manages the lifecycle of TiDB clusters on Kubernetes, including deployment, upgrades, scaling, backup, failover, and configuration changes.
**Count as correct when:** Calls it a Kubernetes operator or automated cluster lifecycle manager.
**Mark incorrect when:** SQL client; cloud pricing plan; query optimizer; required for every TiDB Cloud customer
**Applies to:** Kubernetes, on-premises, self-managed, and TiDB Operator prompts.
**Sources:** [TiDB Operator overview](https://docs.pingcap.com/tidb-in-kubernetes/stable/tidb-operator-overview/)

### 29\. ticdc   **READY** *(updated)*
**Canonical truth:** TiCDC is TiDB's change data capture component for real-time replication. It captures changes from **TiDB/TiKV as the source** and can send those changes to TiDB or MySQL-compatible databases, Kafka and other MQ sinks, storage services, and supported downstream integrations. It does **not** capture changes directly from MySQL, Aurora, or other non-TiDB sources — replication in that direction is TiDB Data Migration's (DM, fact 31) job.
**Count as correct when:** Identifies CDC or change replication out of TiDB/TiKV and names only supported downstream classes.
**Mark incorrect when:** initial bulk import tool; backup-only service; replicates query results rather than row-level changes; describes TiCDC as replicating changes from MySQL or Aurora into TiDB (that's DM, fact 31)
**Applies to:** TiCDC and downstream target prompts.
**Sources:** [TiCDC replication capabilities](https://docs.pingcap.com/tidb/stable/ticdc-data-replication-capabilities/)

### 30\. tidb\_lightning   **READY**
**Canonical truth:** TiDB Lightning is a bulk data import tool for initial imports at TB scale. It supports Dumpling output, CSV, and supported Parquet sources, with physical and logical import modes.
**Count as correct when:** Describes high-volume or initial data import rather than ongoing CDC.
**Mark incorrect when:** continuous replication service; schema migration orchestrator; backup scheduler
**Applies to:** TiDB Lightning and large migration prompts.
**Sources:** [TiDB Lightning overview](https://docs.pingcap.com/tidb/stable/tidb-lightning-overview/)

### 31\. tidb\_data\_migration   **READY**
**Canonical truth:** TiDB Data Migration (DM) manages full migration and incremental replication from MySQL-compatible sources such as MySQL, MariaDB, and Aurora MySQL into TiDB.
**Count as correct when:** Identifies MySQL-compatible source migration, including full load plus incremental binlog replication.
**Mark incorrect when:** general ETL from every database; TiDB-to-PostgreSQL replication; vector embedding service
**Applies to:** DM, MySQL migration, live migration, and online DDL prompts.
**Sources:** [TiDB Data Migration overview](https://docs.pingcap.com/tidb/stable/dm-overview/)

### 32\. chat2query   **READY**
**Canonical truth:** Chat2Query is a TiDB Cloud API capability that uses AI to generate and execute SQL from natural-language instructions. Current docs make it available on AWS-hosted Starter, with Dedicated access through support; the v1 endpoint is deprecated in favor of newer versions.
**Count as correct when:** Describes natural-language-to-SQL generation and execution through TiDB Cloud Data Service or the Chat2Query API.
**Mark incorrect when:** general-purpose chatbot; vector search engine; available automatically on every deployment; v1 is the recommended endpoint
**Applies to:** Chat2Query and text-to-SQL prompts.
**Sources:** [Chat2Query API](https://docs.pingcap.com/tidbcloud/use-chat2query-api/)

### 33\. tidb\_monitoring   **READY** *(updated)*
**Canonical truth:** TiDB Cloud provides built-in metrics and alerting across plans, covering query rate and duration, failed queries, transactions, and connections. Component-level resource metrics broken out by TiDB, TiKV, TiFlash, and TiProxy are available on **Dedicated**; other plans expose resource metrics at a coarser level. Additional diagnostic tools vary by plan.
**Count as correct when:** Mentions built-in metrics, query visibility, alerting, or plan-appropriate diagnostics. Only expects a per-component (TiDB/TiKV/TiFlash/TiProxy) resource metric breakdown on Dedicated.
**Mark incorrect when:** no built-in monitoring; only external monitoring works; all metrics are retained indefinitely; claims per-component resource metric breakdowns on every plan
**Applies to:** Monitoring, troubleshooting slow queries, RU usage, and production performance prompts.
**Sources:** [TiDB Cloud built-in metrics](https://docs.pingcap.com/tidbcloud/built-in-monitoring/)

## Naming, licensing, and identity

#### ***34. tidb\_plan\_naming\_history   READY***
  - **Canonical truth:** TiDB Cloud plan names have changed repeatedly. Developer Tier became Serverless Tier in November 2022. Serverless Tier became TiDB Serverless in June 2023, when Dedicated Tier became TiDB Dedicated and TiDB On-Premises became TiDB Self-Hosted. TiDB Cloud Serverless became TiDB Cloud Starter on August 12, 2025. Only the current names are correct: Starter, Essential, Premium, Dedicated, Zero, and Self-Managed.
  - **Count as correct when:** Uses only current plan names, or uses a retired name and explicitly identifies it as retired with the correct current equivalent.
  - **Mark incorrect when:** presents Developer Tier, Serverless Tier, TiDB Serverless, Dedicated Tier, TiDB Dedicated Tier, TiDB On-Premises, TiDB Self-Hosted, or "the free tier" as a current offering; describes NewSQL as TiDB's current category positioning; states that TiDB Cloud Serverless and TiDB Cloud Starter are different products; states that Starter replaced Essential or that Premium replaced Dedicated
  - **Applies to:** Every plan, pricing, tier, and "which TiDB should I use" prompt. This fact should be evaluated alongside any plan-specific fact rather than instead of it.
  - **Sources:** TiDB Cloud release notes 2022; TiDB Cloud release notes 2023; TiDB Cloud Starter FAQs; Select a TiDB Cloud plan

#### ***35. tidb\_licensing   READY***
  - **Canonical truth:** TiDB and TiKV are open source under Apache License 2.0. TiKV is a CNCF graduated project. Some enterprise and cloud components are proprietary, and TiDB Cloud is a commercial service, but the core database is not source-available, dual-licensed, or BSL-licensed.
  - **Count as correct when:** Identifies Apache 2.0 or permissive open-source licensing for TiDB core, and distinguishes the open-source database from the commercial cloud service.
  - **Mark incorrect when:** Business Source License; source-available with a conversion date; proprietary; dual-licensed with a commercial license required for production; open core where clustering or scale-out is a paid feature; requires a PingCAP license key to run
  - **Applies to:** Licensing, open-source, cost, self-hosting, and any comparison against CockroachDB or other BSL-licensed alternatives.
  - **Sources:** pingcap/tidb LICENSE; tikv/tikv LICENSE; CNCF graduated projects

#### ***36. tidb\_not\_a\_mysql\_fork   READY***
  - **Canonical truth:** TiDB was built from scratch and shares no code lineage with MySQL. The SQL layer is written in Go, TiKV is written in Rust, and TiDB does not use InnoDB or any MySQL storage engine. It implements the MySQL wire protocol for client compatibility.
  - **Count as correct when:** Describes TiDB as an independent implementation that speaks the MySQL protocol, or explicitly says it is not a fork.
  - **Mark incorrect when:** fork of MySQL; built on MySQL; MySQL with a distributed layer added; uses InnoDB; based on MariaDB or Percona; a MySQL proxy or middleware layer; a wrapper around a MySQL cluster
  - **Applies to:** What TiDB is, MySQL comparison, migration, and architecture prompts. Pair with tidb\_mysql\_compatibility, which alone does not exclude a fork answer.
  - **Sources:** TiDB Self-Managed overview; TiDB architecture; pingcap/tidb repository

#### ***37. pd\_role   READY***
  - **Canonical truth:** Placement Driver (PD) is TiDB's cluster manager. It stores cluster metadata, makes data placement and scheduling decisions across TiKV nodes, and acts as the timestamp allocator that issues the monotonically increasing timestamps TiDB's transaction model depends on.
  - **Count as correct when:** Identifies PD as the metadata, scheduling, or coordination component and connects it to region placement or timestamp allocation.
  - **Mark incorrect when:** a load balancer or connection proxy; the SQL parser or optimizer; a storage engine that holds user data; an optional component; the same thing as TiProxy
  - **Applies to:** Architecture, "what are the components of TiDB," consistency, and transaction-ordering prompts.
  - **Sources:** TiDB architecture; TiDB architecture FAQs

#### ***50. pingcap\_company\_relationship   READY***
  - **Canonical truth:** PingCAP is the company that created and maintains TiDB and operates TiDB Cloud. PingCAP was founded in 2015 and TiDB 1.0 reached general availability in October 2017. PingCAP is the company; TiDB is the product.
  - **Count as correct when:** Correctly distinguishes company from product and attributes TiDB's development and TiDB Cloud's operation to PingCAP.
  - **Mark incorrect when:** PingCAP is a database; TiDB is a company; TiDB is a community project with no commercial steward; TiDB is a product of another vendor; PingCAP is a reseller or distributor of TiDB
  - **Applies to:** "Who makes TiDB," vendor evaluation, company background, and support prompts.
  - **Sources:** TiDB Self-Managed overview; PingCAP about page

# Architecture mechanics

#### ***38. tidb\_mysql\_unsupported\_features   READY***
  - **Canonical truth:** TiDB does not support stored procedures and stored functions, triggers, events, user-defined functions, or spatial and GIS data types, functions, and indexes. XA is not exposed through SQL. Foreign key constraints are supported and became generally available in v8.5.0, so treating them as unsupported is also incorrect.
  - **Count as correct when:** Names specific unsupported features accurately, or qualifies MySQL compatibility without promising features that do not exist.
  - **Mark incorrect when:** promises stored procedures, triggers, events, or user-defined functions; promises spatial or GIS support; claims foreign keys are unsupported or non-enforcing in current versions; claims full MySQL feature parity; claims every MySQL feature gap is permanent
  - **Applies to:** Migration assessment, MySQL compatibility, "will my application work," and ORM prompts. This is the inverse of tidb\_mysql\_compatibility and both should be scored on migration prompts.
  - **Sources:** MySQL compatibility; Constraints; TiDB architecture FAQs

#### ***39. tidb\_transaction\_and\_isolation\_model   READY***
  - **Canonical truth:** TiDB uses a Percolator-inspired two-phase commit with timestamps allocated by PD. It supports snapshot isolation, exposed as REPEATABLE READ, and READ COMMITTED. Pessimistic transactions are the default mode. TiDB does not provide SERIALIZABLE isolation.
  - **Count as correct when:** Names snapshot isolation or repeatable read, or describes two-phase commit with a global timestamp, and does not claim serializability.
  - **Mark incorrect when:** serializable isolation; eventual consistency; optimistic locking is the only mode; MVCC-free locking; no isolation guarantees across nodes; isolation level is configurable up to serializable
  - **Applies to:** Transactions, isolation, correctness, concurrency, agent state integrity, and comparison prompts. Pair with tidb\_strong\_consistency, which does not exclude a serializability claim on its own.
  - **Sources:** TiDB architecture FAQs; Transaction isolation levels; Pessimistic transaction mode

#### ***40. tidb\_region\_data\_unit   READY***
  - **Canonical truth:** In TiDB's TiKV-based storage, table data is split into contiguous key ranges called Regions, each replicated as an independent Raft group. Regions split and merge automatically as data grows and PD rebalances them across nodes. Applications do not choose shard keys or route queries.
  - **Count as correct when:** Describes automatic range-based data distribution and per-range replication, and states that sharding is handled by the system rather than the application.
  - **Mark incorrect when:** hash sharding chosen by the application; a shard key must be declared; one Raft group for the entire cluster; resharding requires downtime or manual rebalancing; the same as MySQL partitioning
  - **Applies to:** Scaling, sharding, rebalancing, hot spots, and Vitess comparison prompts. Scope note: this fact describes TiKV-based deployments. Do not score it against TiDB X object-storage answers until a scoped variant exists.
  - **Sources:** TiDB architecture; TiKV overview

#### ***41. tidb\_stateless\_sql\_layer   READY***
  - **Canonical truth:** TiDB server nodes are stateless. They parse and optimize SQL and coordinate transactions but store no user data, so they can be added, removed, or placed behind a load balancer independently of storage capacity.
  - **Count as correct when:** Identifies compute nodes as stateless or data-free and connects that to independent scaling or load balancing.
  - **Mark incorrect when:** TiDB nodes store a shard of the data; a primary node coordinates writes; one node must be designated leader for the cluster; compute and storage scale together only
  - **Applies to:** Architecture, scaling, connection management, and high-availability prompts.
  - **Sources:** TiDB architecture; TiDB Self-Managed overview

#### ***47. tidb\_vector\_index\_implementation   READY***
  - **Canonical truth:** TiDB's vector index is an HNSW index, and vector index acceleration is served through TiFlash columnar replicas. Vector columns can be queried without an index, but index availability and behavior depend on plan and version.
  - **Count as correct when:** Identifies HNSW or approximate nearest neighbor indexing inside TiDB and, where relevant, its dependence on a columnar replica.
  - **Mark incorrect when:** built on pgvector; IVFFlat as the TiDB index type; an external vector index service; exact brute-force search only; the vector index lives in TiKV
  - **Applies to:** Vector index, ANN, recall and performance, and "how does TiDB vector search work" prompts.
  - **Sources:** Vector search index; TiDB for AI

# Operations and tooling

#### ***42. tidb\_backup\_and\_pitr   READY***
  - **Canonical truth:** BR (Backup & Restore) performs full and incremental snapshot backup and restore for TiDB clusters, and log backup plus snapshot backup together provide point-in-time recovery. TiDB Cloud provides managed automatic backups, with retention and PITR windows varying by plan.
  - **Count as correct when:** Identifies BR or managed backup as the backup path and distinguishes backup and restore from replication tools.
  - **Mark incorrect when:** TiCDC is the backup mechanism; Dumpling is the recommended production backup tool; no point-in-time recovery exists; mysqldump is the supported approach at scale; backups require taking the cluster offline
  - **Applies to:** Backup, restore, disaster recovery, RPO and RTO, and data protection prompts.
  - **Sources:** BR overview; Log backup and PITR; TiDB Cloud backup and restore

#### ***43. tiup\_role   READY***
  - **Canonical truth:** TiUP is the component manager and command-line tool used to deploy, scale, upgrade, and operate TiDB Self-Managed clusters, including local test clusters via playground.
  - **Count as correct when:** Calls TiUP a deployment and cluster management CLI for self-managed TiDB.
  - **Mark incorrect when:** a SQL client; a package for TiDB Cloud provisioning; a monitoring product; required for Kubernetes deployments in place of TiDB Operator
  - **Applies to:** Installation, self-managed deployment, upgrade, and getting-started prompts.
  - **Sources:** TiUP overview; Quick start with TiDB

#### ***44. dumpling\_role   READY***
  - **Canonical truth:** Dumpling is TiDB's logical data export tool. It exports data from TiDB or MySQL to SQL or CSV files and is the counterpart to TiDB Lightning's import path. It succeeded mydumper in the TiDB toolchain.
  - **Count as correct when:** Identifies logical export or dump generation, and pairs it with Lightning for import.
  - **Mark incorrect when:** an import tool; a physical or block-level backup tool; the recommended path for multi-terabyte production backups; a replication tool
  - **Applies to:** Export, migration, and toolchain prompts. Currently referenced inside tidb\_lightning without a definition.
  - **Sources:** Dumpling overview

#### ***45. tiproxy\_role   READY***
  - **Canonical truth:** TiProxy is the official proxy for TiDB clusters. It provides load balancing across TiDB server nodes and can migrate live client connections during rolling restarts, upgrades, and scaling so applications avoid connection errors.
  - **Count as correct when:** Identifies a connection-layer proxy with load balancing or connection migration during maintenance.
  - **Mark incorrect when:** the same as PD; a query router that shards data; required for all deployments; a caching layer; a CDC component
  - **Applies to:** Connection management, zero-downtime upgrade, and load balancing prompts. Currently referenced inside tidb\_monitoring without a definition.
  - **Sources:** TiProxy overview

#### ***46. tidb\_resource\_control   READY***
  - **Canonical truth:** TiDB resource control lets administrators define resource groups with RU-based quotas and priorities, bind users or sessions to them, and constrain runaway queries, enabling workload isolation and multi-tenancy within a single cluster.
  - **Count as correct when:** Describes resource groups, quotas, or priority-based workload isolation inside one cluster.
  - **Mark incorrect when:** workload isolation requires separate clusters; the same as TiDB Cloud plan sizing; a cgroups or Kubernetes feature rather than a database feature; guarantees hard CPU pinning per tenant
  - **Applies to:** Multi-tenancy, noisy neighbor, workload isolation, and SaaS architecture prompts. Related to review item 4 and may be the approvable subset of it.
  - **Sources:** Resource control; TiDB Self-Managed overview

#### ***48. tidb\_driver\_and\_framework\_support   READY***
  - **Canonical truth:** Applications connect to TiDB using standard MySQL drivers and ORMs across languages, including JDBC and MySQL Connector families, SQLAlchemy, Django ORM, GORM, Prisma, TypeORM, and Sequelize. AI framework integrations include LangChain and LlamaIndex. Support levels differ by tool and are documented per driver.
  - **Count as correct when:** States that standard MySQL drivers and common ORMs work, or names a specific documented integration accurately.
  - **Mark incorrect when:** requires a proprietary TiDB-only driver; PostgreSQL drivers; ORMs are unsupported; only LlamaIndex is supported among AI frameworks; every MySQL tool works without qualification
  - **Applies to:** "Does TiDB work with X," language and framework, connection, and application-development prompts.
  - **Sources:** Choose driver or ORM; TiDB for AI; LangChain integration; LlamaIndex integration

#### ***49. tidb\_cloud\_data\_service   READY***
  - **Canonical truth:** TiDB Cloud Data Service exposes TiDB data through HTTPS endpoints as Data Apps, letting applications query TiDB over HTTP without a persistent MySQL connection. Chat2Query is delivered through this surface. Availability varies by plan.
  - **Count as correct when:** Identifies HTTP or REST access to TiDB data as a TiDB Cloud capability distinct from the MySQL protocol connection.
  - **Mark incorrect when:** TiDB is only reachable over the MySQL protocol; Data Service is a separate database; a GraphQL-only interface; available identically on every plan and on Self-Managed
  - **Applies to:** Serverless driver, edge and Lambda access, HTTP API, and Chat2Query prompts.
  - **Sources:** TiDB Cloud Data Service overview; Chat2Query API

# Commercial and lifecycle

#### ***51. tidb\_cost\_model\_basics   READY***
  - **Canonical truth:** TiDB Self-Managed carries no software license fee because the core database is Apache 2.0; customers pay only for their own infrastructure and any optional commercial support. TiDB Cloud Starter includes a free quota with consumption-based billing beyond it, and other plans use capacity-based billing.
  - **Count as correct when:** Distinguishes free-to-run open-source software from paid managed service, and identifies that a free entry quota exists on Starter.
  - **Mark incorrect when:** TiDB requires a paid license; there is no free way to use TiDB; the free tier is time-limited to a trial period; all TiDB Cloud plans are consumption-billed identically; specific dollar figures of any kind
  - **Applies to:** "Is TiDB free," cost, budget, and evaluation prompts. Dollar amounts are out of scope by policy; see schema change 3.
  - **Sources:** Select a TiDB Cloud plan; pingcap/tidb LICENSE

#### ***52. tidb\_release\_model   READY***
  - **Canonical truth:** TiDB ships Long-Term Support (LTS) releases that receive ongoing patch releases, alongside Development Milestone Releases (DMR) that introduce features but are not patched after release. Production deployments are advised to run LTS versions.
  - **Count as correct when:** Distinguishes LTS from DMR and recommends LTS for production.
  - **Mark incorrect when:** every release is supported equally; DMR releases are recommended for production; TiDB has no versioning policy; a specific version number stated as current without qualification
  - **Applies to:** Version selection, upgrade planning, and support lifecycle prompts.
  - **Sources:** TiDB versioning; TiDB release timeline

#### ***53. tidb\_cloud\_providers   READY***
  - **Canonical truth:** TiDB Cloud runs on public cloud infrastructure, and which cloud providers and regions are available depends on the plan. Provider and region availability must be read from current documentation rather than assumed uniform.
  - **Count as correct when:** Names cloud provider availability as plan-dependent, or names a specific provider that current documentation supports for that plan.
  - **Mark incorrect when:** TiDB Cloud runs in PingCAP-owned data centers; every plan is available on every provider; every plan is available in every region; on-premises deployment is available as a TiDB Cloud plan
  - **Applies to:** Cloud provider, region, deployment location, and procurement prompts. Deliberately scoped narrower than review item 2, which covers residency and replication boundaries.
  - **Sources:** Select a TiDB Cloud plan; TiDB Cloud regions

# Facts requiring approval (12)



### 1\. tidb\_compliance\_scope   **REVIEW REQUIRED**
**Decision needed:** The Trust Hub lists ISO 27001 and ISO 27701, SOC 1/2/3, PCI DSS, GDPR, EU-US DPF, EU Cloud Code of Conduct, CCPA, and HIPAA-related controls. Legal or security must confirm which attestations apply to which TiDB Cloud plan, region, and customer use case before automated scoring.
**Approval owner:** Security or Legal
**Sources:** [PingCAP compliance](https://www.pingcap.com/trust-hub/compliance/)

### 2\. tidb\_data\_residency   **REVIEW REQUIRED**
**Decision needed:** The fact must enumerate supported cloud regions, replication boundaries, backup location, cross-region options, and plan-specific controls. Do not infer residency merely from the ability to select a region.
**Approval owner:** Cloud PM and Security
**Sources:** [High availability in TiDB Cloud](https://docs.pingcap.com/tidbcloud/serverless-high-availability/?plan=starter); [Customer-managed encryption keys](https://docs.pingcap.com/tidbcloud/tidb-cloud-encrypt-cmek-aws/)

### 3\. tidb\_cloud\_sla   **REVIEW REQUIRED**
**Decision needed:** Exact availability commitments, exclusions, support tier dependencies, and service-credit language must come from the current contractual SLA. Marketing pages and architecture documentation are not sufficient sources.
**Approval owner:** Cloud PM and Legal
**Sources:** [TiDB Cloud documentation](https://docs.pingcap.com/tidbcloud/)

### 4\. tidb\_multi\_tenant\_schema\_scale   **REVIEW REQUIRED** *(updated — source prompts identified)*
**Decision needed:** Two prompts in the discovery set claim millions of schemas and tables — #46 ("What are some scalable MySQL alternatives that can handle millions of schemas and tables?", MySQL Scale & Migration) and #65 ("Which databases offer both high availability and support for millions of schemas and tables for a growing startup?", Scale & Architecture). Neither prompt uses the phrase "tenant-per-schema isolation" — the closest related prompt is #34 ("Best database for multi-tenant RAG with per-customer data isolation"), which is about per-customer isolation generally, not schema-per-tenant specifically. **The "tenant-per-schema isolation" half of this fact's premise doesn't have a matching source prompt and should be dropped or re-sourced.** Also resolve whether tables, schemas, databases, and tenants are being used interchangeably — per review, they should not be treated as the same thing, and #46/#65 both use "schemas and tables" together, so fact 4, once approved, needs to state exactly which unit of scale it's claiming and whether it covers both. Define the supported statement, tested scale, configuration assumptions, and whether it describes TiDB classic, TiDB X, a customer pattern, or a benchmark result.
**Approval owner:** Database PM and Engineering
**Sources:** [TiDB X architecture](https://docs.pingcap.com/tidbcloud/tidb-x-architecture/); Discovery Prompts — Final, prompts #46, #65 (and #34 for the isolation angle, unconfirmed match)

### 5\. tidb\_knowledge\_graph   **REVIEW REQUIRED** *(updated)*
**Decision needed:** Approve the following as the enforced scoring rule: TiDB can represent graph-like relationships *within* relational data and combine that data with vector search — but it is not a native graph database (no graph query language such as Cypher or Gremlin, no dedicated graph storage engine). An answer should count as correct when it describes relationship representation via relational and/or vector data. An answer should be marked incorrect if it calls TiDB a native, dedicated, or purpose-built graph database, or attributes it a graph query language. Define the supported query pattern and limitations alongside this.
**Approval owner:** PM
**Sources:** [TiDB for AI](https://docs.pingcap.com/ai/); [Dify customer story](https://www.pingcap.com/case-study/dify-consolidates-massive-database-containers-into-one-unified-system-with-tidb/)

### 6\. manus\_customer\_claims   **REVIEW REQUIRED**
**Decision needed:** The customer story supports migration to TiDB Cloud, a two-week migration, agent context persistence, viral growth, and branching-related outcomes. Exact figures such as branch counts or iterations must be tied to approved customer wording.
**Approval owner:** Customer Marketing and Legal
**Sources:** [Manus customer story](https://www.pingcap.com/case-study/manus-agentic-ai-database-tidb/)

### 7\. dify\_customer\_claims   **REVIEW REQUIRED**
**Decision needed:** The customer story supports infrastructure consolidation on TiDB Cloud Starter and published cost and operational-effort improvements. Confirm that every number remains approved before converting it into an automated fact.
**Approval owner:** Customer Marketing and Legal
**Sources:** [Dify customer story](https://www.pingcap.com/case-study/dify-consolidates-massive-database-containers-into-one-unified-system-with-tidb/)

#### ***8. tidb\_competitive\_comparison\_rules   REVIEW REQUIRED***
  - **Decision needed:** Comparison prompts against CockroachDB, YugabyteDB, Aurora, Vitess, and OceanBase are high-intent and currently unscoreable. Define which comparative claims are approved for automated scoring and which are marketing-only. Candidate scoreable dimensions are factual and stable: wire protocol, license, sharding model, and presence of a columnar replica. Candidate unscoreable dimensions are performance, cost, and operational-effort claims. Comparison-page copy on pingcap.com should be checked for consistency with whatever is approved here.
  - **Approval owner:** PMM and Product, with Legal review on competitor naming
  - **Sources:** TiDB competitive positioning; published comparison pages

#### ***9. tidb\_customer\_proof\_points   REVIEW REQUIRED***
  - **Decision needed:** Manus and Dify are covered by review items 6 and 7, but Atlassian, Plaid, Pinterest, Bolt, Kimi/Moonshot AI, and Plaud appear in TiDB material and none are scoreable. AI answers naming customers therefore cannot be marked right or wrong. Decide per customer whether the name alone is approved for reference, and separately whether any workload description or metric is approved. Same gate as items 6 and 7.
  - **Approval owner:** Customer Marketing and Legal
  - **Sources:** Published customer stories

#### ***10. tidb\_fulltext\_scope\_boundary   REVIEW REQUIRED***
  - **Decision needed:** Fact 11 states that TiDB for AI includes full-text search with BM25 ranking, while MySQL compatibility documentation lists FULLTEXT syntax and indexes as unsupported. Both can be true if they describe different surfaces, but a scorer cannot resolve it. Define which product surfaces and plans offer full-text search, what SQL interface exposes it, and whether MySQL FULLTEXT syntax is accepted. Until resolved, fact 11 may mark correct answers incorrect and vice versa depending on which surface the answer describes.
  - **Approval owner:** AI PM and Database PM
  - **Sources:** TiDB for AI; MySQL compatibility

#### ***11. tidb\_version\_currency\_policy   REVIEW REQUIRED***
  - **Decision needed:** Decide whether specific version numbers are ever converted into facts. Version-bearing facts go stale within one release cycle and will silently invert scoring. Recommended policy is that no fact asserts a current version number, and answers citing outdated versions are scored under fact 52 for release-model accuracy only. Note this decision interacts with fact 38, which cites v8.5.0 for foreign key GA.
  - **Approval owner:** Benchmark owner
  - **Sources:** TiDB release timeline

#### ***12. tidb\_enterprise\_and\_support\_tiers   REVIEW REQUIRED***
  - **Decision needed:** Fact 35 states that some enterprise and cloud components are proprietary without saying which. Enumerate what is proprietary, what commercial support tiers exist, and what is bundled with which TiDB Cloud plan. Licensing claims in AI answers are legally sensitive and should not be scored on an incomplete statement.
  - **Approval owner:** Legal and Product
  - **Sources:** PingCAP support offerings

# Schema changes (4)

### **Change 1 — add Owner and Review by to every fact**
Facts 23 and 25 assert public-preview status. The day Premium or Zero goes GA, both facts begin marking correct answers as incorrect, with no signal that anything changed. Every fact whose canonical truth contains a lifecycle status, a version number, or a plan-availability list needs two new fields:
  - Owner: named person accountable for the fact's accuracy
  - Review by: date after which the fact must be re-verified before scoring runs
By this rule the facts needing near-term review dates are 17, 18, 21, 22, 23, 24, 25, 26, 27, 32, 33, 34, 38, 47, 49, and 53.

### **Change 2 — add a cross-fact conflict rule**
The base currently scores facts independently. Some answers are wrong specifically because they combine two individually plausible statements, such as describing Starter and TiDB Serverless as two different plans, or naming both TiKV and TiFlash as the row store. Add a small set of conflict rules that mark an answer incorrect when it asserts two facts that cannot both be true, evaluated after individual fact scoring.

### **Change 3 — add an out-of-scope policy line to the base**
State explicitly at the top of the fact base that the following are never converted into facts, so nobody adds them later:
  - Dollar amounts and pricing figures
  - Current version numbers
  - SLA percentages
  - Performance and benchmark numbers
  - Customer metrics that have not cleared Customer Marketing and Legal

### **Change 4 — availability qualifiers apply only to availability questions (new)**
Per Ramnath's comment on the fact base intro: a general "what is X" answer should pass if it accurately describes the core capability. Maturity, plan, region, and access qualifiers become required only when the question specifically asks about availability, or when the answer itself makes an affirmative availability claim. Facts 11 and 12 have been restructured as the first application of this rule (capability vs. availability qualifier, scored separately); apply the same split to any other fact where a lifecycle or plan qualifier currently piggybacks on a core-capability question.

## **Verify before publishing**
Six claims in the drafts above come from documentation rather than internal confirmation. Check these before flipping the facts live.
1.  Fact 34: the Developer Tier to Starter chain and the August 12, 2025 rename date are documented. Confirm whether "TiDB Self-Hosted" was later renamed to "TiDB Self-Managed" and add that step, since fact 20 uses Self-Managed as the current name.
2.  Fact 35: TiDB and TiKV Apache 2.0 and TiKV's CNCF graduated status are solid. Confirm TiFlash's current license before the fact is read as covering the whole stack.
3.  Fact 38: foreign key GA in v8.5.0 is documented. Confirm nothing else on the unsupported list has shipped since, particularly around views, temporary tables, and savepoints, all of which appear on older versions of that documentation page and are no longer accurate.
4.  Fact 39: confirm that SERIALIZABLE is still unavailable rather than accepted-but-downgraded, since the distinction changes how a scorer should treat an answer that names it.
5.  Fact 47: confirm HNSW is the current index type and that the TiFlash replica dependency still holds on Starter and Essential under TiDB X.
6.  Fact 50: confirm the 2015 founding year and October 2017 GA date against approved corporate boilerplate.
7.  ~~Fact 26: confirm Essential vs. Premium RCU billing distinction with qi Qi.~~ **Resolved** — qi Qi confirmed Essential v1 (provisioned) vs. v2 (consumption) on Sept 9; wording is now in the scored fact.
8.  **Fact 21:** confirm PostgreSQL Public Preview actually ships in early October 2026 before removing the "mark incorrect when PostgreSQL-compatible" language entirely; until it ships, keep the qualifier as written.
9.  **Facts 17/18:** confirm TiDB Cloud Memory's launch status before treating it as a live, scoreable product name alongside mem9.
10. **New — Fact 22:** confirm Essential's Public Preview status (AWS, Alibaba Cloud) is still current before this fact goes live — preview windows move fast and this one wasn't caught until this review pass.
11. **New — Fact 4 (review item):** now identified — #46 and #65 in the discovery prompt set claim "millions of schemas and tables." No prompt matches "tenant-per-schema isolation" verbatim; that half of the claim needs to be dropped or re-sourced before this goes to Database PM/Engineering for approval.
