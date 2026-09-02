from __future__ import annotations

import re
from collections import Counter, defaultdict
from statistics import mean
from typing import Any
from urllib.parse import urlparse

from .io_utils import estimate_tokens


PRODUCT_ALIASES = {
    # --- PingCAP -------------------------------------------------------
    "TiDB": [
        "tidb", "tidb cloud", "tidb serverless", "pingcap tidb", "pingcap",
        "tidb cloud zero", "tidb cloud starter", "tidb cloud essential",
        "tidb cloud premium", "tidb cloud dedicated", "tidb cloud filesystem",
        "tidb x", "pytidb", "tikv", "tiflash", "ticdc", "tidb operator",
        "tidb lightning", "chat2query", "mem9", "drive9",
    ],

    # --- Distributed SQL -----------------------------------------------
    "CockroachDB": ["cockroachdb", "cockroach"],
    "YugabyteDB": ["yugabytedb", "yugabyte"],
    "Spanner": ["spanner", "cloud spanner", "google spanner"],
    "AlloyDB": ["alloydb"],
    "OceanBase": ["oceanbase", "ocean base"],
    "SingleStore": ["singlestore", "single store"],
    "AuroraDSQL": ["aurora dsql", "amazon aurora dsql"],

    # --- MySQL ecosystem -----------------------------------------------
    "Aurora": ["aurora", "amazon aurora", "aws aurora", "aurora mysql"],
    "RDS": ["amazon rds", "aws rds"],
    "MariaDB": ["mariadb", "maria db"],
    "Percona": ["percona", "percona server"],
    "Vitess": ["vitess"],
    "PlanetScale": ["planetscale", "planet scale"],

    # --- Serverless / app backend --------------------------------------
    "Supabase": ["supabase"],
    "Neon": ["neon", "neon.tech"],

    # --- Vector and retrieval ------------------------------------------
    "Pinecone": ["pinecone"],
    "Weaviate": ["weaviate"],
    "Qdrant": ["qdrant"],
    "Milvus": ["milvus", "zilliz"],
    "Chroma": ["chroma", "chromadb", "chroma db"],
    "Vespa": ["vespa"],
    "pgvector": ["pgvector"],
    "Redis": ["redis", "redisearch"],

    # --- Search ---------------------------------------------------------
    "Elasticsearch": ["elasticsearch", "elastic search"],
    "OpenSearch": ["opensearch"],

    # --- Real-time analytics / OLAP -------------------------------------
    "ClickHouse": ["clickhouse", "click house"],
    "Druid": ["apache druid", "druid"],
    "Pinot": ["apache pinot", "pinot"],
    "TimescaleDB": ["timescaledb", "timescale"],
    "StarRocks": ["starrocks", "star rocks"],

    # --- Data platform ---------------------------------------------------
    "MongoDB": ["mongodb", "mongo db", "mongodb atlas"],
    "Snowflake": ["snowflake"],
    "Databricks": ["databricks"],

    # --- Incumbents: report separately, not in the competitor cohort ------
    "MySQL": ["mysql", "my sql"],
    "PostgreSQL": ["postgresql", "postgres", "pgsql"],
}

PRODUCT_URL_MARKERS = {
    # --- PingCAP -------------------------------------------------------
    "TiDB": [
        "pingcap.com", "github.com/pingcap", "mem9.ai", "drive9.ai",
        "tidb.io", "docs.pingcap.com",
    ],

    # --- Distributed SQL -----------------------------------------------
    "CockroachDB": ["cockroachlabs.com", "github.com/cockroachdb"],
    "YugabyteDB": ["docs.yugabyte.com", "yugabyte.com", "github.com/yugabyte"],
    "Spanner": ["cloud.google.com/spanner"],
    "AlloyDB": ["cloud.google.com/alloydb"],
    "OceanBase": ["oceanbase.com", "en.oceanbase.com"],
    "SingleStore": ["singlestore.com"],
    "AuroraDSQL": [
        "docs.aws.amazon.com/aurora-dsql/",
        "aws.amazon.com/rds/aurora/dsql/",
    ],

    # --- MySQL ecosystem -----------------------------------------------
    "Aurora": ["docs.aws.amazon.com/amazonrds/latest/aurorauserguide/"],
    "RDS": ["docs.aws.amazon.com/amazonrds/latest/userguide/"],
    "MariaDB": ["mariadb.org", "mariadb.com"],
    "Percona": ["percona.com"],
    "Vitess": ["vitess.io", "github.com/vitessio"],
    "PlanetScale": ["planetscale.com"],

    # --- Serverless / app backend --------------------------------------
    "Supabase": ["supabase.com", "github.com/supabase"],
    "Neon": ["neon.tech"],

    # --- Vector and retrieval ------------------------------------------
    "Pinecone": ["pinecone.io"],
    "Weaviate": ["weaviate.io", "github.com/weaviate"],
    "Qdrant": ["qdrant.tech", "github.com/qdrant"],
    "Milvus": ["milvus.io", "zilliz.com", "github.com/milvus-io"],
    "Chroma": ["trychroma.com", "github.com/chroma-core"],
    "Vespa": ["vespa.ai", "github.com/vespa-engine"],
    "pgvector": ["github.com/pgvector"],
    "Redis": ["redis.io", "github.com/redis"],

    # --- Search ---------------------------------------------------------
    "Elasticsearch": ["elastic.co", "github.com/elastic"],
    "OpenSearch": ["opensearch.org"],

    # --- Real-time analytics / OLAP -------------------------------------
    "ClickHouse": ["clickhouse.com", "github.com/clickhouse"],
    "Druid": ["druid.apache.org"],
    "Pinot": ["pinot.apache.org", "startree.ai"],
    "TimescaleDB": ["docs.tigerdata.com", "timescale.com", "github.com/timescale"],
    "StarRocks": ["starrocks.io", "github.com/starrocks"],

    # --- Data platform ---------------------------------------------------
    "MongoDB": ["mongodb.com", "github.com/mongodb"],
    "Snowflake": ["docs.snowflake.com", "snowflake.com"],
    "Databricks": ["docs.databricks.com", "databricks.com"],

    # --- Incumbents: report separately, not in the competitor cohort ----
    "MySQL": ["dev.mysql.com", "mysql.com"],
    "PostgreSQL": ["postgresql.org"],
}

RECOMMEND_WORDS = [
    "recommend",
    "recommended",
    "best",
    "choose",
    "shortlist",
    "top option",
    "strong option",
    "first",
    "\u9996\u9009",
    "\u63a8\u8350",
]

URL_RE = re.compile(r"https?://[^\s)\]>,]+", re.IGNORECASE)


def score_answers(
    raw_answers: list[dict[str, Any]],
    prompts: list[dict[str, Any]],
    source_authority: dict[str, Any],
    facts: dict[str, Any],
    targets: list[str] | None = None,
) -> list[dict[str, Any]]:
    prompt_by_id = {prompt["prompt_id"]: prompt for prompt in prompts}
    targets = targets or ["TiDB", "CockroachDB"]
    rows: list[dict[str, Any]] = []
    for row in raw_answers:
        if row.get("status") != "ok":
            continue
        prompt = prompt_by_id[row["prompt_id"]]
        for target in targets:
            rows.append(score_answer(row, prompt, source_authority, facts, target))
    return rows


def score_answer(
    row: dict[str, Any],
    prompt: dict[str, Any],
    source_authority: dict[str, Any],
    facts: dict[str, Any],
    target: str = "TiDB",
) -> dict[str, Any]:
    answer = row.get("raw_answer", "")
    positions = product_positions(answer)
    target_positions = positions.get(target, [])
    mentioned_target = bool(target_positions)
    mention_position = target_mention_position(positions, target)
    presence_score = {"first": 1.0, "top3": 0.6, "other": 0.2, "none": 0.0}[mention_position]

    urls = sorted(set(extract_urls(answer) + extract_raw_citation_urls(row.get("raw_citations", []))))
    citation_rows = classify_citations(urls, source_authority)
    target_citations = [item for item in citation_rows if is_product_related_url(target, item["url"])]
    citation_presence = bool(target_citations)
    source_score = mean([item["weight"] for item in target_citations]) if target_citations else 0.0
    grounding_score = grounding(answer, citation_presence)
    accuracy_score, checked_facts, correct_facts = accuracy(answer, facts, target)
    freshness_score = freshness(target_citations)
    citation_authority_answer = (
        (1.0 if citation_presence else 0.0)
        * source_score
        * grounding_score
        * accuracy_score
        * freshness_score
    )

    rec_class, rec_score, rec_reasons = recommendation(answer, mention_position, target)
    winner = competitive_winner(answer, prompt)
    target_in_prompt = product_in_prompt(prompt, target)

    return {
        "answer_id": row["answer_id"],
        "target_answer_id": f"{row['answer_id']}::{target}",
        "target": target,
        "run_id": row["run_id"],
        "month": row["month"],
        "prompt_id": row["prompt_id"],
        "model_surface": row["model_surface"],
        "model_name": row.get("model_name"),
        "web_search_mode": row.get("web_search_mode", "off"),
        "web_search_requests": row.get("web_search_requests", 0),
        "panel": prompt.get("panel", "stable"),
        "prompt_type": prompt.get("prompt_type"),
        "persona": prompt.get("persona"),
        "region": prompt.get("region"),
        "funnel_stage": prompt.get("funnel_stage"),
        "use_case": prompt.get("use_case"),
        "intent_weight": prompt.get("intent_weight", 1),
        "qualified_recommendation_opportunity": prompt.get("qualified_recommendation_opportunity", False),
        "target_in_prompt": target_in_prompt,
        "brand_class": "branded" if target_in_prompt else "non_branded",
        "mentioned_target": mentioned_target,
        "mention_position": mention_position,
        "presence_score": round(presence_score, 4),
        "citations": citation_rows,
        "citation_presence": citation_presence,
        "source_authority": round(source_score, 4),
        "grounding_score": round(grounding_score, 4),
        "accuracy": round(accuracy_score, 4),
        "accuracy_checked_facts": checked_facts,
        "accuracy_correct_facts": correct_facts,
        "freshness": round(freshness_score, 4),
        "citation_authority_answer": round(citation_authority_answer, 4),
        "recommendation_class": rec_class,
        "recommendation_score": rec_score,
        "classification_reason": rec_reasons,
        "competitive_winner": winner,
        "input_tokens": row.get("input_tokens", estimate_tokens(row.get("prompt_text", ""))),
        "output_tokens": row.get("output_tokens", estimate_tokens(answer)),
    }


def product_positions(text: str) -> dict[str, list[int]]:
    lower = text.lower()
    result: dict[str, list[int]] = {}
    for product, aliases in PRODUCT_ALIASES.items():
        positions: list[int] = []
        for alias in aliases:
            pattern = r"\b" + re.escape(alias.lower()) + r"\b"
            positions.extend(match.start() for match in re.finditer(pattern, lower))
        if positions:
            result[product] = sorted(set(positions))
    return result


def target_mention_position(positions: dict[str, list[int]], target: str) -> str:
    if target not in positions:
        return "none"
    ordered_products = sorted(
        ((min(pos), product) for product, pos in positions.items() if pos),
        key=lambda item: item[0],
    )
    rank = [product for _, product in ordered_products].index(target) + 1
    if rank == 1:
        return "first"
    if rank <= 3:
        return "top3"
    return "other"


def extract_urls(text: str) -> list[str]:
    return [url.rstrip(".,") for url in URL_RE.findall(text)]


def extract_raw_citation_urls(raw_citations: Any) -> list[str]:
    if isinstance(raw_citations, str):
        return extract_urls(raw_citations)
    if isinstance(raw_citations, list):
        urls: list[str] = []
        for item in raw_citations:
            if isinstance(item, str):
                if item.startswith(("http://", "https://")):
                    urls.append(item)
                else:
                    urls.extend(extract_urls(item))
            elif isinstance(item, dict):
                url = item.get("url")
                if isinstance(url, str):
                    urls.append(url)
        return urls
    return []


def classify_citations(urls: list[str], source_authority: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    rules = source_authority.get("rules", [])
    default = source_authority.get("default_weight", 0.2)
    for url in urls:
        normalized = url.lower()
        weight = default
        label = "unknown"
        for rule in rules:
            if rule["contains"].lower() in normalized:
                weight = float(rule["weight"])
                label = rule.get("label", label)
                break
        rows.append({"url": url, "domain": urlparse(url).netloc, "weight": weight, "label": label})
    return rows


def is_product_related_url(target: str, url: str) -> bool:
    lower = url.lower()
    markers = PRODUCT_URL_MARKERS.get(target, [target.lower()])
    return any(marker in lower for marker in markers)


def grounding(answer: str, citation_presence: bool) -> float:
    if not citation_presence:
        return 0.0
    lower = answer.lower()
    if "sources:" in lower or "source:" in lower:
        return 1.0
    if "http" in lower and any(word in lower for word in ["because", "supports", "recommended", "distributed"]):
        return 0.8
    return 0.5


def accuracy(answer: str, facts: dict[str, Any], target: str) -> tuple[float, int, int]:
    lower = answer.lower()
    fact_rows = facts.get("targets", {}).get(target, facts.get("facts", []))
    checked = 0
    correct = 0
    for fact in fact_rows:
        triggers = [item.lower() for item in fact.get("triggers", [])]
        if triggers and not any(trigger in lower for trigger in triggers):
            continue
        checked += 1
        wrong = any(item.lower() in lower for item in fact.get("wrong_any", []))
        expected = any(item.lower() in lower for item in fact.get("expected_any", []))
        if expected and not wrong:
            correct += 1
    if checked == 0:
        return 1.0, 0, 0
    return correct / checked, checked, correct


def freshness(citations: list[dict[str, Any]]) -> float:
    if not citations:
        return 0.0
    scores = []
    for citation in citations:
        url = citation["url"].lower()
        if any(marker in url for marker in ["stable", "latest", "current", "2026", "2025"]):
            scores.append(1.0)
        elif citation["label"] in {"official_docs", "official_site", "github"}:
            scores.append(0.9)
        else:
            scores.append(0.7)
    return mean(scores)


def recommendation(answer: str, mention_position: str, target: str) -> tuple[str, float, list[str]]:
    lower = answer.lower()
    if mention_position == "none":
        return "not_mentioned", 0.0, ["not_mentioned"]

    target_context = target_context_window(lower, target, 140)
    target_lower = target.lower()
    negative_patterns = [
        f"not recommend {target_lower}",
        f"avoid {target_lower}",
        f"{target_lower} is not a good fit",
        f"better than {target_lower}",
        "not my first recommendation",
        "may be easier operationally",
    ]
    if any(pattern in target_context for pattern in negative_patterns):
        return "negative", -0.5, ["negative_language"]

    has_recommend = any(word in lower for word in RECOMMEND_WORDS)
    has_context_recommend = any(word in target_context for word in RECOMMEND_WORDS)
    conditional = any(word in target_context for word in ["if you", "good if", "when you", "depending", "conditional"])

    if mention_position == "first" and (has_context_recommend or has_recommend):
        return "best", 1.0, ["first_mention", "recommended"]
    if mention_position in {"first", "top3"} and has_context_recommend:
        return "strong", 0.75, [mention_position, "recommended"]
    if conditional:
        return "conditional", 0.5, ["conditional_fit"]
    return "listed", 0.2, ["listed_without_clear_recommendation"]


def target_context_window(text: str, target: str, size: int) -> str:
    aliases = PRODUCT_ALIASES.get(target, [target])
    indexes = [text.find(alias.lower()) for alias in aliases if text.find(alias.lower()) >= 0]
    if not indexes:
        return ""
    idx = min(indexes)
    return text[max(0, idx - size) : idx + size]


def competitive_winner(answer: str, prompt: dict[str, Any]) -> str | None:
    if prompt.get("prompt_type") != "competitive":
        return None
    positions = product_positions(answer)
    if not positions:
        return None
    ranked = sorted((min(pos), product) for product, pos in positions.items() if pos)
    return ranked[0][1] if ranked else None


def product_in_prompt(prompt: dict[str, Any], product: str) -> bool:
    if product in prompt.get("competitors", []):
        return True
    lower = prompt.get("prompt_text", "").lower()
    return any(alias.lower() in lower for alias in PRODUCT_ALIASES.get(product, [product]))


def aggregate_scores(scored: list[dict[str, Any]]) -> dict[str, Any]:
    targets = sorted({row.get("target", "TiDB") for row in scored})
    target_summaries = {
        target: aggregate_target([row for row in scored if row.get("target", "TiDB") == target])
        for target in targets
    }
    first_target = targets[0] if targets else None
    result: dict[str, Any] = {
        "target_order": targets,
        "targets": target_summaries,
    }
    if first_target:
        result.update(target_summaries[first_target])
    else:
        result.update(aggregate_target([]))
    return result


def aggregate_target(rows: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "overall": aggregate_slice(rows),
        "unchanged": aggregate_slice([row for row in rows if row.get("panel") == "stable"]),
        "by_model": aggregate_by(rows, "model_surface"),
        "by_use_case": aggregate_by(rows, "use_case"),
        "by_prompt_type": aggregate_by(rows, "prompt_type"),
        "competitive": competitive_breakdown(rows),
    }


def aggregate_by(scored: list[dict[str, Any]], field: str) -> dict[str, Any]:
    buckets: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in scored:
        buckets[str(row.get(field, "unknown"))].append(row)
    return {key: aggregate_slice(rows) for key, rows in sorted(buckets.items())}


def aggregate_slice(rows: list[dict[str, Any]]) -> dict[str, Any]:
    if not rows:
        return empty_metrics()

    visible_rows = [row for row in rows if not row.get("target_in_prompt")]
    branded_rows = [row for row in rows if row.get("target_in_prompt")]
    if not visible_rows:
        metrics = empty_metrics()
        metrics["answer_count"] = len(rows)
        metrics.update(brand_metrics(branded_rows))
        return metrics

    prompt_groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in visible_rows:
        prompt_groups[row["prompt_id"]].append(row)

    weight_sum = 0.0
    presence_sum = 0.0
    citation_sum = 0.0
    rec_weight_sum = 0.0
    rec_sum = 0.0
    qualified_answers = 0
    recommended_answers = 0
    negative_answers = 0
    mention_counts = Counter(row["mention_position"] for row in visible_rows)
    recommendation_counts = Counter(row["recommendation_class"] for row in visible_rows)

    for prompt_rows in prompt_groups.values():
        weight = float(prompt_rows[0].get("intent_weight", 1))
        weight_sum += weight
        presence_sum += mean(row["presence_score"] for row in prompt_rows) * weight
        citation_sum += mean(row["citation_authority_answer"] for row in prompt_rows) * weight
        if prompt_rows[0].get("qualified_recommendation_opportunity"):
            rec_weight_sum += weight
            rec_sum += mean(row["recommendation_score"] for row in prompt_rows) * weight

    for row in visible_rows:
        if row.get("qualified_recommendation_opportunity"):
            qualified_answers += 1
            if row["recommendation_class"] in {"best", "strong", "conditional"}:
                recommended_answers += 1
            if row["recommendation_class"] == "negative":
                negative_answers += 1

    checked = [row for row in visible_rows if row.get("accuracy_checked_facts", 0) > 0]
    weighted_rec_avg = rec_sum / rec_weight_sum if rec_weight_sum else 0.0
    metrics = {
        "prompt_count": len(prompt_groups),
        "answer_count": len(rows),
        "answer_share": round((presence_sum / weight_sum) * 100, 2) if weight_sum else 0.0,
        "citation_authority": round((citation_sum / weight_sum) * 100, 2) if weight_sum else 0.0,
        "qualified_recommendation_rate": round((recommended_answers / qualified_answers) * 100, 2)
        if qualified_answers
        else 0.0,
        "weighted_recommendation_score": round(max(0.0, min(1.0, weighted_rec_avg)) * 100, 2),
        "negative_recommendation_rate": round((negative_answers / qualified_answers) * 100, 2)
        if qualified_answers
        else 0.0,
        "mention_counts": dict(mention_counts),
        "recommendation_counts": dict(recommendation_counts),
        "avg_source_authority": round(mean(row["source_authority"] for row in visible_rows), 4),
        "avg_accuracy": round(mean(row["accuracy"] for row in checked), 4) if checked else None,
        "accuracy_coverage": round(len(checked) / len(visible_rows), 4),
        "avg_freshness": round(mean(row["freshness"] for row in visible_rows), 4),
    }
    metrics.update(brand_metrics(branded_rows))
    return metrics


def brand_metrics(branded_rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Accuracy-oriented metrics for prompts that name the target themselves.

    These prompts ("What is TiDB Cloud Zero?") cannot measure visibility, so
    they are scored on whether the answer is correct, grounded, and cites us.
    """
    if not branded_rows:
        return {
            "branded_prompt_count": 0,
            "branded_answer_count": 0,
            "brand_accuracy": None,
            "brand_accuracy_coverage": 0.0,
            "brand_citation_rate": None,
            "brand_negative_rate": None,
        }
    checked = [row for row in branded_rows if row.get("accuracy_checked_facts", 0) > 0]
    cited = sum(1 for row in branded_rows if row.get("citation_presence"))
    negative = sum(1 for row in branded_rows if row.get("recommendation_class") == "negative")
    return {
        "branded_prompt_count": len({row["prompt_id"] for row in branded_rows}),
        "branded_answer_count": len(branded_rows),
        "brand_accuracy": round(mean(row["accuracy"] for row in checked) * 100, 2) if checked else None,
        "brand_accuracy_coverage": round(len(checked) / len(branded_rows), 4),
        "brand_citation_rate": round((cited / len(branded_rows)) * 100, 2),
        "brand_negative_rate": round((negative / len(branded_rows)) * 100, 2),
    }


def empty_metrics() -> dict[str, Any]:
    return {
        "prompt_count": 0,
        "answer_count": 0,
        "answer_share": 0.0,
        "citation_authority": 0.0,
        "qualified_recommendation_rate": 0.0,
        "weighted_recommendation_score": 0.0,
        "negative_recommendation_rate": 0.0,
        "mention_counts": {},
        "recommendation_counts": {},
        "avg_source_authority": 0.0,
        "avg_accuracy": None,
        "accuracy_coverage": 0.0,
        "avg_freshness": 0.0,
        "branded_prompt_count": 0,
        "branded_answer_count": 0,
        "brand_accuracy": None,
        "brand_accuracy_coverage": 0.0,
        "brand_citation_rate": None,
        "brand_negative_rate": None,
    }


def competitive_breakdown(scored: list[dict[str, Any]]) -> dict[str, Any]:
    if not scored:
        return {}
    target = scored[0].get("target")
    rows = [
        row
        for row in scored
        if row.get("prompt_type") == "competitive"
        and row.get("target_in_prompt")
        and row.get("competitive_winner")
    ]
    if not rows:
        return {}
    totals: Counter[str] = Counter()
    wins = 0
    for row in rows:
        winner = row.get("competitive_winner") or "unknown"
        totals[winner] += 1
        if winner == target:
            wins += 1
    return {
        "valid_comparison_answers": len(rows),
        "target_win_rate": round((wins / len(rows)) * 100, 2),
        "winner_counts": dict(totals),
    }
