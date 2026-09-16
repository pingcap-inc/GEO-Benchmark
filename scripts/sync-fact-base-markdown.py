#!/usr/bin/env python3
"""Synchronize the semantic TiDB fact-base artifacts from a reviewed Markdown file."""

from __future__ import annotations

import argparse
import csv
import json
import re
from datetime import date, timedelta
from pathlib import Path


FACT_FIELDS = [
    "fact_id", "category", "status", "owner", "verified_on", "review_by",
    "review_cadence", "canonical_truth", "correct_when", "incorrect_when",
    "applies_to", "source_urls", "judge_prompt", "decision_needed",
]
REVIEW_FIELDS = ["review_id", "status", "owner", "decision_needed", "source_urls"]
ID_ALIASES = {
    "mem9_definition": "tidb_cloud_memory_definition",
    "drive9_definition": "tidb_cloud_filesystem_definition",
}
# The review copy explicitly says these details still need verification before publishing.
VERIFY_BEFORE_PUBLISHING = {
    "tidb_plan_naming_history",
    "tidb_licensing",
    "tidb_mysql_unsupported_features",
    "tidb_transaction_and_isolation_model",
    "tidb_vector_index_implementation",
    "pingcap_company_relationship",
}
# The review queue says this capability remains unsafe to score until its product surface is resolved.
REMAINING_REVIEW_GATES = {"tidb_full_text_search"}
REVIEW_SOURCE_FALLBACKS = {
    "tidb_competitive_comparison_rules": ["https://www.pingcap.com/tidb/", "https://www.pingcap.com/compare/"],
    "tidb_customer_proof_points": ["https://www.pingcap.com/customers/"],
    "tidb_fulltext_scope_boundary": ["https://docs.pingcap.com/ai/", "https://docs.pingcap.com/tidb/stable/mysql-compatibility/"],
    "tidb_version_currency_policy": ["https://docs.pingcap.com/tidb/stable/release-timeline/"],
    "tidb_enterprise_and_support_tiers": ["https://www.pingcap.com/support/"],
}
SPECIFIC_SOURCE_OVERRIDES = {
    "tidb_vector_search": [
        "https://docs.pingcap.com/ai/vector-search-overview/",
        "https://docs.pingcap.com/ai/vector-search-index/",
        "https://docs.pingcap.com/ai/vector-search-limitations/",
    ],
    "tidb_full_text_search": ["https://docs.pingcap.com/ai/vector-search-full-text-search-sql/"],
    "pytidb_definition": ["https://docs.pingcap.com/ai/pytidb/"],
}
SCOPE_RULE = (
    "Scope rule: For a broad definition or core-capability question, judge the answer on the relevant "
    "core capability only. Do not require the answer to repeat maturity, plan, region, version, or access "
    "qualifiers merely because they appear in canonical truth. Those qualifiers become required when the "
    "prompt asks about availability, support, eligibility, maturity, plans, regions, versions, or access, "
    "or when the answer makes a specific claim about any of those dimensions. When activated, verify the "
    "specific claim against canonical truth. Omission is not an error when the qualifier check is not activated."
)


def clean(value: str) -> str:
    value = re.sub(r"\[([^]]+)]\([^)]+\)", r"\1", value)
    value = value.replace("\\_", "_").replace("**", "").replace("*", "")
    value = re.sub(r"\s+", " ", value)
    return value.strip(" -\n")


def extract_raw_field(body: str, label: str, next_labels: list[str]) -> str:
    labels = "|".join(re.escape(item) for item in next_labels)
    match = re.search(
        rf"(?:^|\n)\s*(?:-\s*)?\*\*{re.escape(label)}:\*\*\s*(.*?)(?=\n\s*(?:-\s*)?\*\*(?:{labels}):\*\*|\Z)",
        body,
        flags=re.DOTALL,
    )
    return match.group(1).strip() if match else ""


def extract_field(body: str, label: str, next_labels: list[str]) -> str:
    return clean(extract_raw_field(body, label, next_labels))


def source_urls(body: str) -> list[str]:
    source_text = extract_raw_field(body, "Sources", ["Owner/Review by", "Approval owner"])
    linked = re.findall(r"https://[^)\s;]+", source_text)
    return [url.rstrip(".,") for url in linked]


def parse_sections(markdown: str) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    heading = re.compile(
        r"^(#{3,4})\s+(?:\*{3})?(\d+)\\?\.\s+([a-zA-Z0-9_\\]+)\s+(?:\*{0,3})\s*(READY|REVIEW REQUIRED)[^\n]*$",
        flags=re.MULTILINE,
    )
    matches = list(heading.finditer(markdown))
    facts: list[dict[str, str]] = []
    reviews: list[dict[str, str]] = []
    category = ""
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(markdown)
        body = markdown[start:end]
        between = markdown[matches[index - 1].end() if index else 0 : match.start()]
        category_matches = re.findall(r"^#{1,2}\s+(.+)$", between, flags=re.MULTILINE)
        if category_matches:
            candidate = clean(category_matches[-1])
            if candidate not in {"Approved facts (53)", "Facts requiring approval (12)", "Schema changes (4)"}:
                category = candidate
        raw_id = match.group(3).replace("\\_", "_")
        item_id = ID_ALIASES.get(raw_id, raw_id)
        if match.group(4) == "REVIEW REQUIRED":
            reviews.append({
                "review_id": item_id,
                "owner": extract_field(body, "Approval owner", ["Sources"]),
                "decision_needed": extract_field(body, "Decision needed", ["Approval owner", "Sources"]),
                "source_urls": source_urls(body),
                "status": "OPEN",
            })
            continue
        facts.append({
            "fact_id": item_id,
            "category": category,
            "canonical_truth": extract_field(body, "Canonical truth", ["Availability qualifier", "Count as correct when", "Mark incorrect when", "Applies to", "Sources"]),
            "availability_qualifier": extract_field(body, "Availability qualifier", ["Count as correct when", "Mark incorrect when", "Applies to", "Sources"]),
            "correct_when": extract_field(body, "Count as correct when", ["Mark incorrect when", "Applies to", "Sources", "Owner/Review by"]),
            "incorrect_when": extract_field(body, "Mark incorrect when", ["Applies to", "Sources", "Owner/Review by"]),
            "applies_to": extract_field(body, "Applies to", ["Sources", "Owner/Review by"]),
            "source_urls": source_urls(body),
            "review_note": extract_field(body, "Owner/Review by", ["Sources"]),
        })
    return facts, reviews


def judge_prompt(fact: dict[str, object]) -> str:
    return (
        "Judge only this mapped fact against the prompt and answer. Do not state or imply that unrelated "
        "claims in the answer are accurate or inaccurate; separate fact and conflict checks evaluate them. "
        "Return one of correct, incorrect, not_enough_information, or not_applicable, plus a short reason and "
        f"supporting answer excerpt. Canonical truth: {fact['canonical_truth']} "
        f"Count as correct when: {fact['correct_when']} Mark incorrect when: {fact['incorrect_when']} "
        f"Apply only to: {fact['applies_to']} Do not require exact wording. If the answer does not make a claim "
        "about this fact, return not_applicable. If it addresses the fact but lacks enough detail to decide, "
        f"return not_enough_information. {SCOPE_RULE}"
    )


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            flat = dict(row)
            flat["source_urls"] = " | ".join(row.get("source_urls", []))
            writer.writerow({field: flat.get(field, "") for field in fields})


def update_coverage(config: Path, facts: list[dict[str, object]], reviews: list[dict[str, object]]) -> None:
    replacements = {
        "tidb_vector_search_production_status": "tidb_vector_search",
        "tidb_cloud_memory_launch_and_rename": "tidb_cloud_memory_definition",
        "tidb_ru_rcu_definition": "tidb_cloud_ru_and_rcu",
    }
    fact_status = {str(fact["fact_id"]): fact["status"] for fact in facts}
    review_ids = {str(item["review_id"]) for item in reviews}
    fields = [
        "prompt_id", "prompt_type", "prompt_text", "coverage_disposition",
        "fact_or_review_ids", "note", "mapping_status",
    ]
    for path in config.glob("tidb_fact_coverage_????-??.csv"):
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        for row in rows:
            if row.get("coverage_disposition") == "comparison_metric_only":
                continue
            old_disposition = row.get("coverage_disposition")
            old_ids = row.get("fact_or_review_ids", "")
            ids = [part.strip() for part in row.get("fact_or_review_ids", "").split("|") if part.strip()]
            ids = [replacements.get(item, item) for item in ids]
            ids = list(dict.fromkeys(ids))
            row["fact_or_review_ids"] = " | ".join(ids)
            held = any(item in review_ids or fact_status.get(item) != "READY_FOR_JUDGE" for item in ids)
            new_disposition = "review_required" if held else "fact_covered"
            row["coverage_disposition"] = new_disposition
            if old_disposition != new_disposition or old_ids != row["fact_or_review_ids"]:
                row["note"] = (
                    "At least one required fact or approval is still open."
                    if held else "All mapped facts are approved and judge-ready."
                )
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("markdown", type=Path)
    parser.add_argument("--config", type=Path, default=Path("geo-benchmark/config"))
    parser.add_argument("--verified-on", required=True, type=date.fromisoformat)
    args = parser.parse_args()

    json_path = args.config / "tidb_fact_base_v2.json"
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    existing = {fact["fact_id"]: fact for fact in payload["facts"]}
    parsed_facts, reviews = parse_sections(args.markdown.read_text(encoding="utf-8"))
    today = args.verified_on

    updated: list[dict[str, object]] = []
    for parsed in parsed_facts:
        fact_id = parsed["fact_id"]
        if fact_id not in existing:
            raise SystemExit(f"Unknown fact in Markdown: {fact_id}")
        fact = dict(existing[fact_id])
        for field in ("category", "canonical_truth", "correct_when", "incorrect_when", "applies_to"):
            if parsed.get(field):
                fact[field] = parsed[field]
        if parsed.get("availability_qualifier"):
            fact["canonical_truth"] += " Availability qualifier: " + parsed["availability_qualifier"]
        if fact_id in SPECIFIC_SOURCE_OVERRIDES:
            fact["source_urls"] = SPECIFIC_SOURCE_OVERRIDES[fact_id]
        elif parsed.get("source_urls"):
            fact["source_urls"] = parsed["source_urls"]
        hold = fact_id in VERIFY_BEFORE_PUBLISHING | REMAINING_REVIEW_GATES
        fact["status"] = "REVIEW_REQUIRED" if hold else "READY_FOR_JUDGE"
        if hold:
            preview = "public preview" in fact["canonical_truth"].lower()
            fact["review_cadence"] = "quarterly" if preview else fact.get("review_cadence", "annual")
            fact["verified_on"] = today.isoformat() if preview else None
            fact["review_by"] = (today + timedelta(days=92)).isoformat() if preview else None
            fact["decision_needed"] = parsed.get("review_note") or fact.get("decision_needed") or "Verify the flagged detail before activating this fact."
        else:
            fact.pop("decision_needed", None)
            fact["verified_on"] = today.isoformat()
            changing = any(term in fact["canonical_truth"].lower() for term in ("public preview", "planned", "currently available", "not yet launched"))
            fact["review_cadence"] = "quarterly" if changing else fact.get("review_cadence", "annual")
            days = 92 if fact["review_cadence"] == "quarterly" else 365
            fact["review_by"] = (today + timedelta(days=days)).isoformat()
        fact["judge_prompt"] = judge_prompt(fact)
        updated.append(fact)

    # Keep the two prompt-driven additions that post-date the numbered review sheet.
    for fact_id in ("tidb_langchain_integration", "tidb_agent_memory_storage"):
        if fact_id not in existing:
            raise SystemExit(
                f"Required prompt-driven fact is missing from the existing fact base: {fact_id}"
            )
        fact = dict(existing[fact_id])
        fact["judge_prompt"] = judge_prompt(fact)
        updated.append(fact)

    payload["schema_version"] = "2.1-draft"
    payload["verified_on"] = today.isoformat()
    payload["facts"] = updated
    for review in reviews:
        if not review["source_urls"]:
            review["source_urls"] = REVIEW_SOURCE_FALLBACKS.get(str(review["review_id"]), [])
    payload["review_queue"] = reviews
    rules = {rule["conflict_id"]: rule for rule in payload.get("conflict_rules", [])}
    rules["tidb_serverless_current_name"] = {
        "conflict_id": "tidb_serverless_current_name",
        "description": "The answer presents TiDB Serverless or TiDB Cloud Serverless as a current product name.",
        "result": "incorrect",
    }
    rules["cloud_zero_false_positioning"] = {
        "conflict_id": "cloud_zero_false_positioning",
        "description": "The answer incorrectly presents TiDB Cloud Zero as scale-to-zero, pay-per-use, or a production service.",
        "result": "incorrect",
    }
    payload["conflict_rules"] = list(rules.values())
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_csv(args.config / "tidb_fact_base_v2.csv", updated, FACT_FIELDS)
    write_csv(args.config / "tidb_fact_base_review_queue.csv", reviews, REVIEW_FIELDS)
    update_coverage(args.config, updated, reviews)


if __name__ == "__main__":
    main()
