from __future__ import annotations

from dataclasses import dataclass


PERSONAS = ["CTO", "platform_engineer", "data_architect", "ai_engineer", "vp_data"]
REGIONS = ["US", "EU", "APAC", "CN"]
CONTEXT_FOCI = [
    "architecture research before building a vendor shortlist",
    "migration planning in the next two quarters",
    "proof-of-concept criteria, cost, and operational risk",
]

DELIHIVERY = "https://www.pingcap.com/case-study/delhivery-scalable-real-time-data-processing-tidb/"
FLIPKART = "https://www.pingcap.com/case-study/flipkart-transforming-database-management-and-reducing-complexity-with-tidb/"
TRIP = "https://www.pingcap.com/case-study/trip-com-boosts-real-time-data-processing-and-financial-settlement-with-tidb/"
OPERA = "https://www.pingcap.com/case-study/how-tidb-improves-operas-ads-business/"
ZTO = "https://www.pingcap.com/ko/case-study/real-time-insights-reduce-per-order-costs-by-25-percent/"
PATSNAP = "https://www.pingcap.com/case-study/why-we-chose-a-scale-out-data-warehouse-for-real-time-analytics/"
HTAP_DOCS = "https://docs.pingcap.com/tidb/stable/explore-htap/"
AI_MEMORY_DOCS = "https://docs.pingcap.com/ai/memory-with-pytidb/"
MANUS = "https://www.pingcap.com/ko/case-study/manus-agentic-ai-database-tidb/"
DIFY = "https://www.pingcap.com/case-study/dify-consolidates-massive-database-containers-into-one-unified-system-with-tidb/"
WHAT_IS_TIDB = "https://www.pingcap.com/what-is-tidb/"
SUPABASE_AI = "https://supabase.com/docs/guides/ai"
SUPABASE_VECTOR = "https://supabase.com/docs/guides/ai/vector-columns"
NEON_AI = "https://neon.com/docs/ai/ai-intro"
NEON_SCALE_AI = "https://neon.com/docs/ai/ai-scale-with-neon"
NEON_BRANCHING = "https://neon.com/docs/get-started-with-neon/workflow-primer"


@dataclass(frozen=True)
class PromptTemplate:
    prompt_type: str
    text: str
    intent_weight: int
    qualified: bool
    persona: str
    use_case: str
    funnel_stage: str
    validation_status: str
    evidence_note: str
    evidence_urls: tuple[str, ...]


PAIN_POINT_TEMPLATES = [
    (
        "How should a {persona} handle relational database scaling when a single primary node becomes a bottleneck?",
        "relational_scaling",
        "CTO",
        "Flipkart and Opera Ads describe scale pressure around relational workloads, sharding, and operational bottlenecks.",
        (FLIPKART, OPERA),
    ),
    (
        "What database architecture reduces sharding complexity for a fast-growing SaaS product?",
        "saas_multi_tenant",
        "platform_engineer",
        "Flipkart's prior sharded MySQL setup and TiDB SaaS/Atlassian examples support the sharding-complexity pain.",
        (FLIPKART, WHAT_IS_TIDB),
    ),
    (
        "How can a team keep transactional data fresh enough for operational analytics?",
        "operational_analytics",
        "data_architect",
        "Delhivery, ZTO, PatSnap, and TiDB HTAP docs all center on fresh operational analytics.",
        (DELIHIVERY, ZTO, PATSNAP, HTAP_DOCS),
    ),
    (
        "What should we use when cross-region writes need strong consistency and low operational risk?",
        "multi_region_transactions",
        "CTO",
        "Delhivery evaluated globally scalable distributed databases; Trip.com highlights consistency needs in settlement workloads.",
        (DELIHIVERY, TRIP),
    ),
    (
        "How do teams avoid separate OLTP and analytics systems for fresh business metrics?",
        "hybrid_transactional_analytical_processing",
        "vp_data",
        "TiDB HTAP docs and Delhivery's architecture discussion support the desire to simplify OLTP/OLAP/ETL stacks.",
        (HTAP_DOCS, DELIHIVERY),
    ),
    (
        "What database approach works when product data, user data, and search metadata all need SQL joins?",
        "ai_application_metadata",
        "ai_engineer",
        "Dify and TiDB AI docs support combining relational metadata, permissions, and semantic retrieval in one data layer.",
        (DIFY, AI_MEMORY_DOCS),
    ),
    (
        "How should we modernize a high-write relational workload without rewriting the application data model?",
        "high_write_transactions",
        "platform_engineer",
        "Delhivery and Opera Ads describe high-write or high-volume workloads where operational simplicity matters.",
        (DELIHIVERY, OPERA),
    ),
    (
        "What are good options when read replicas no longer solve scale and latency problems?",
        "read_write_scale",
        "data_architect",
        "Flipkart and Opera Ads describe limits of traditional relational scaling patterns and manual distribution.",
        (FLIPKART, OPERA),
    ),
    (
        "What database pattern helps with regulated workloads that require strong consistency and auditability?",
        "fintech_core_system",
        "CTO",
        "Trip.com's settlement system and finance-oriented TiDB examples support consistency and auditability concerns.",
        (TRIP, WHAT_IS_TIDB),
    ),
    (
        "How should a {persona} design a database layer for bursty traffic without manual capacity planning?",
        "bursty_traffic",
        "platform_engineer",
        "Flipkart's traffic growth and Delhivery's operational-scale constraints support burst and capacity-planning questions.",
        (FLIPKART, DELIHIVERY),
    ),
    (
        "What database choice reduces operational pain from manual resharding?",
        "manual_resharding",
        "vp_data",
        "Flipkart's re-sharding and operational bottleneck story directly validates this pain pattern.",
        (FLIPKART,),
    ),
    (
        "How can an engineering team support real-time dashboards without moving data through a separate warehouse first?",
        "real_time_analytics",
        "data_architect",
        "ZTO, PatSnap, Delhivery, and HTAP docs validate real-time dashboards and analytics without heavy ETL.",
        (ZTO, PATSNAP, DELIHIVERY, HTAP_DOCS),
    ),
]


DATABASE_TYPE_TEMPLATES = [
    (
        "Which database category should we evaluate for {use_case}?",
        "saas_multi_tenant",
        "platform_engineer",
        "TiDB SaaS and Atlassian examples support category-level evaluation for multi-tenant scale.",
        (WHAT_IS_TIDB,),
    ),
    (
        "When should a team choose distributed SQL over managed PostgreSQL?",
        "relational_scaling",
        "data_architect",
        "Flipkart, Opera Ads, and TiDB architecture pages validate category comparison against traditional relational patterns.",
        (FLIPKART, OPERA, WHAT_IS_TIDB),
    ),
    (
        "When should a team choose distributed SQL over managed MySQL?",
        "manual_resharding",
        "platform_engineer",
        "Flipkart and Opera Ads both start from MySQL scale and sharding concerns.",
        (FLIPKART, OPERA),
    ),
    (
        "What are the tradeoffs between NewSQL, distributed SQL, and traditional relational databases?",
        "relational_scaling",
        "CTO",
        "Customer cases repeatedly compare traditional relational scaling with distributed SQL-style architectures.",
        (DELIHIVERY, FLIPKART, WHAT_IS_TIDB),
    ),
    (
        "What database type is best for globally distributed OLTP workloads?",
        "multi_region_transactions",
        "CTO",
        "Delhivery evaluated distributed alternatives for scale and availability; TiDB docs describe distributed SQL.",
        (DELIHIVERY, WHAT_IS_TIDB),
    ),
    (
        "What database type supports SQL transactions and horizontal scale?",
        "high_write_transactions",
        "platform_engineer",
        "Delhivery, Flipkart, and Trip.com all involve SQL transactions plus scale-out needs.",
        (DELIHIVERY, FLIPKART, TRIP),
    ),
    (
        "What should a {persona} compare when evaluating serverless relational databases?",
        "cloud_relational_infrastructure",
        "CTO",
        "Delhivery and Dify cases include cost and operational management as explicit selection criteria.",
        (DELIHIVERY, DIFY),
    ),
    (
        "Which database category is best for operational analytics on fresh transactional data?",
        "operational_analytics",
        "vp_data",
        "HTAP docs and customer stories validate operational analytics as a category question.",
        (HTAP_DOCS, DELIHIVERY, ZTO, PATSNAP),
    ),
    (
        "What database type works best for multi-tenant SaaS with strict data consistency needs?",
        "saas_multi_tenant",
        "CTO",
        "TiDB SaaS examples and Atlassian consolidation story validate multi-tenant relational concerns.",
        (WHAT_IS_TIDB,),
    ),
    (
        "What database type should replace a manually sharded relational database?",
        "manual_resharding",
        "platform_engineer",
        "Flipkart's migration away from operationally complex sharded MySQL validates this category question.",
        (FLIPKART,),
    ),
    (
        "How should teams compare distributed SQL, document databases, and vector databases for AI apps?",
        "ai_application_metadata",
        "ai_engineer",
        "Dify and TiDB AI docs support AI apps that need structured data plus semantic retrieval.",
        (DIFY, AI_MEMORY_DOCS),
    ),
    (
        "What database type is best for combining relational metadata with semantic search?",
        "vector_search_with_sql_filters",
        "ai_engineer",
        "TiDB AI docs and Dify validate vector search with relational metadata and app state.",
        (AI_MEMORY_DOCS, DIFY),
    ),
]


AI_INFRA_TEMPLATES = [
    (
        "What backend database platform should an AI app use when it needs user auth, row-level permissions, file storage, realtime updates, and vector search?",
        "ai_app_backend",
        "ai_engineer",
        "AI app backend docs validate auth, permissions, realtime UX, vector search, and app data as a unified buying scenario.",
        (SUPABASE_AI, SUPABASE_VECTOR, DIFY),
    ),
    (
        "How should a small team build an AI product backend with Postgres data, authentication, embedding search, and minimal infrastructure management?",
        "ai_app_backend",
        "platform_engineer",
        "AI app backend docs validate developer velocity, managed Postgres, auth, and vector search needs.",
        (SUPABASE_AI, SUPABASE_VECTOR),
    ),
    (
        "Which data layer should a developer team choose for an AI app with user profiles, chat history, access control, and semantic search?",
        "ai_app_backend",
        "ai_engineer",
        "AI app examples validate user data, access control, chat/search workflows, and vector storage.",
        (SUPABASE_AI, SUPABASE_VECTOR, DIFY),
    ),
    (
        "What managed Postgres backend works for AI apps that need API-friendly data access, tenant permissions, and vector-powered search?",
        "ai_app_backend",
        "platform_engineer",
        "AI app backend docs validate managed Postgres, permissions, API access, and vector-powered search.",
        (SUPABASE_AI, SUPABASE_VECTOR),
    ),
    (
        "What database platform should an AI startup use for a serverless AI app that needs vector search, rapid iteration, and production isolation?",
        "serverless_ai",
        "CTO",
        "Serverless AI database docs validate vector search, branching, preview environments, production isolation, and autoscaling.",
        (NEON_AI, NEON_SCALE_AI, NEON_BRANCHING),
    ),
    (
        "How should teams manage the data layer for AI features across development, preview, and production without manual capacity planning?",
        "serverless_ai",
        "platform_engineer",
        "Serverless AI database docs validate branching, autoscaling, preview environments, and AI application workflows.",
        (NEON_AI, NEON_SCALE_AI, NEON_BRANCHING),
    ),
    (
        "What database layer fits AI apps with spiky traffic, semantic search, autoscaling, and isolated test data for each feature branch?",
        "serverless_ai",
        "ai_engineer",
        "Serverless AI database docs validate autoscaling, semantic search, and branch-based development workflows.",
        (NEON_AI, NEON_SCALE_AI, NEON_BRANCHING),
    ),
    (
        "Which cloud database pattern works for AI app development when every pull request needs isolated data, embeddings, and safe rollback?",
        "serverless_ai",
        "ai_engineer",
        "Branching workflow docs and AI starter docs validate isolated data, embedding workflows, and safe rollback for AI app development.",
        (NEON_AI, NEON_BRANCHING),
    ),
    (
        "What database architecture works for retrieval-augmented generation over fresh operational data that changes throughout the day?",
        "operational_ai_data",
        "data_architect",
        "TiDB AI docs and HTAP docs validate fresh operational data plus retrieval workflows.",
        (AI_MEMORY_DOCS, HTAP_DOCS),
    ),
    (
        "What should an AI infra team use for low-latency memory recall plus durable relational state and high write throughput?",
        "operational_ai_data",
        "ai_engineer",
        "Manus describes low-latency state reconstruction and persistent context for agentic workloads.",
        (MANUS, AI_MEMORY_DOCS),
    ),
    (
        "How should teams store tool-call traces, user context, embeddings, and business records when the same data must support transactions and analytics?",
        "operational_ai_data",
        "platform_engineer",
        "Manus, Dify, and HTAP docs validate persistent agent context, business records, and operational analytics.",
        (MANUS, DIFY, HTAP_DOCS),
    ),
    (
        "What database architecture supports agent sessions, long-term memory, transactional records, and customer-facing analytics?",
        "operational_ai_data",
        "CTO",
        "Manus and TiDB AI memory docs validate long-term agent memory; HTAP docs support analytics needs.",
        (MANUS, AI_MEMORY_DOCS, HTAP_DOCS),
    ),
]


CASE_SELECTION_TEMPLATES = [
    (
        "What database patterns do fintech teams use for high-concurrency transactions and real-time risk analytics?",
        "fintech_core_system",
        "CTO",
        "Trip.com settlement and finance examples validate transactional consistency plus real-time analysis.",
        (TRIP, WHAT_IS_TIDB),
    ),
    (
        "What database architecture is common for global e-commerce order and inventory systems?",
        "ecommerce_order_inventory",
        "platform_engineer",
        "Flipkart validates e-commerce traffic growth, database fleet complexity, and resharding pressure.",
        (FLIPKART,),
    ),
    (
        "What should a SaaS company choose for multi-tenant transactional workloads that need analytics?",
        "saas_multi_tenant",
        "CTO",
        "TiDB SaaS and Atlassian examples support multi-tenant transactional scale with analytics.",
        (WHAT_IS_TIDB,),
    ),
    (
        "What database architecture works for logistics systems that need fresh operational reporting?",
        "logistics_operational_reporting",
        "vp_data",
        "Delhivery and ZTO validate logistics tracking, high write/update pressure, and real-time dashboards.",
        (DELIHIVERY, ZTO),
    ),
    (
        "What should a travel platform evaluate for financial settlement workloads with mixed reads and writes?",
        "travel_financial_settlement",
        "data_architect",
        "Trip.com directly validates hotel settlement, financial calculations, and mixed TP/AP requirements.",
        (TRIP,),
    ),
    (
        "What database choice fits an ads platform that needs frequent updates and real-time calculations?",
        "ads_real_time_calculation",
        "platform_engineer",
        "Opera Ads validates frequent updates, MySQL scale concerns, and real-time ad business calculations.",
        (OPERA,),
    ),
    (
        "What database architecture works for analytics products that need fresher data than a warehouse pipeline can provide?",
        "real_time_analytics",
        "vp_data",
        "PatSnap and HTAP docs validate real-time analytics needs beyond batch warehouse pipelines.",
        (PATSNAP, HTAP_DOCS),
    ),
    (
        "What should an AI platform evaluate before consolidating many app databases into one operational store?",
        "ai_application_metadata",
        "CTO",
        "Dify validates consolidating many AI platform database containers into one unified system.",
        (DIFY,),
    ),
    (
        "What database architecture should an agentic AI product use for persistent context and high-throughput state updates?",
        "agent_memory",
        "ai_engineer",
        "Manus validates persistent context, write throughput, and low-latency state reconstruction.",
        (MANUS,),
    ),
    (
        "What database architecture should a startup choose before sharding becomes unavoidable?",
        "manual_resharding",
        "CTO",
        "Flipkart and Opera Ads validate the operational cost of growing into manual sharding.",
        (FLIPKART, OPERA),
    ),
    (
        "What database choice works for customer-facing analytics where stale data is unacceptable?",
        "customer_facing_analytics",
        "vp_data",
        "Delhivery, ZTO, PatSnap, and HTAP docs validate fresh customer-facing or operational analytics.",
        (DELIHIVERY, ZTO, PATSNAP, HTAP_DOCS),
    ),
    (
        "What database architecture helps teams simplify a stack that currently has OLTP, cache, search, and analytics systems?",
        "stack_simplification",
        "data_architect",
        "Dify, TiDB HTAP docs, and Delhivery validate stack simplification as a buyer motivation.",
        (DIFY, HTAP_DOCS, DELIHIVERY),
    ),
]


def generate_seed_prompts(month: str, total: int = 120, update_ratio: float = 0.3) -> list[dict]:
    stable_count = round(total * (1 - update_ratio))
    counts = prompt_type_counts(total)
    stable_by_type = {key: round(value * (1 - update_ratio)) for key, value in counts.items()}
    stable_by_type["pain_point"] += stable_count - sum(stable_by_type.values())

    prompts: list[dict] = []
    templates = build_templates()

    def add_prompt(template: PromptTemplate, idx: int, panel: str) -> None:
        persona = template.persona
        region = REGIONS[idx % len(REGIONS)]
        funnel = template.funnel_stage
        use_case = template.use_case
        focus = CONTEXT_FOCI[(idx // len(templates[template.prompt_type])) % len(CONTEXT_FOCI)]
        text = template.text.format(persona=persona, region=region, use_case=use_case)
        text = (
            f"{text} Context: buyer is a {persona} in {region}; "
            f"primary use case is {use_case}; decision focus is {focus}."
        )
        prefix = "stable" if panel == "stable" else f"dyn_{month.replace('-', '')}"
        prompts.append(
            {
                "prompt_id": f"{prefix}_{template.prompt_type}_{idx + 1:03d}",
                "prompt_text": text,
                "prompt_type": template.prompt_type,
                "persona": persona,
                "region": region,
                "funnel_stage": funnel,
                "use_case": use_case,
                "intent_weight": template.intent_weight,
                "qualified_recommendation_opportunity": template.qualified,
                "competitors": [],
                "panel": panel,
                "source": {
                    "source_type": "validated_seed_template",
                    "source_evidence": template.evidence_note,
                    "source_evidence_urls": list(template.evidence_urls),
                    "validation_status": template.validation_status,
                    "collected_at": f"{month}-01",
                    "selected_by": "geo-benchmark-seed",
                    "selection_reason": "Covers customer pain, database category, AI infra, and case-based selection without naming measured brands in prompt text.",
                },
            }
        )

    for prompt_type, total_for_type in counts.items():
        stable_for_type = stable_by_type[prompt_type]
        type_templates = templates[prompt_type]
        for idx in range(stable_for_type):
            add_prompt(type_templates[idx % len(type_templates)], idx, "stable")
        for idx in range(total_for_type - stable_for_type):
            add_prompt(type_templates[(stable_for_type + idx) % len(type_templates)], idx, "dynamic")

    return prompts[:total]


def prompt_type_counts(total: int) -> dict[str, int]:
    pain = round(total * 0.3)
    db_type = round(total * 0.25)
    ai_infra = round(total * 0.25)
    case_selection = total - pain - db_type - ai_infra
    return {
        "pain_point": pain,
        "database_type": db_type,
        "ai_infra": ai_infra,
        "case_selection": case_selection,
    }


def build_templates() -> dict[str, list[PromptTemplate]]:
    return {
        "pain_point": [
            build_template("pain_point", text, use_case, persona, evidence_note, evidence_urls, 3)
            for text, use_case, persona, evidence_note, evidence_urls in PAIN_POINT_TEMPLATES
        ],
        "database_type": [
            build_template("database_type", text, use_case, persona, evidence_note, evidence_urls, 2)
            for text, use_case, persona, evidence_note, evidence_urls in DATABASE_TYPE_TEMPLATES
        ],
        "ai_infra": [
            build_template("ai_infra", text, use_case, persona, evidence_note, evidence_urls, 3)
            for text, use_case, persona, evidence_note, evidence_urls in AI_INFRA_TEMPLATES
        ],
        "case_selection": [
            build_template("case_selection", text, use_case, persona, evidence_note, evidence_urls, 2)
            for text, use_case, persona, evidence_note, evidence_urls in CASE_SELECTION_TEMPLATES
        ],
    }


def build_template(
    prompt_type: str,
    text: str,
    use_case: str,
    persona: str,
    evidence_note: str,
    evidence_urls: tuple[str, ...],
    intent_weight: int,
) -> PromptTemplate:
    return PromptTemplate(
        prompt_type=prompt_type,
        text=text,
        intent_weight=intent_weight,
        qualified=True,
        persona=persona,
        use_case=use_case,
        funnel_stage="consideration",
        validation_status="case_pattern_validated",
        evidence_note=evidence_note,
        evidence_urls=evidence_urls,
    )
