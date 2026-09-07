from __future__ import annotations

import csv
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .io_utils import canonical_data_root, ensure_dir, estimate_tokens, read_json, read_jsonl, stable_hash, write_jsonl
from .providers import ProviderError, _post_json, extract_openai_response_text


VERDICTS = {"correct", "incorrect", "not_enough_information", "not_applicable", "judge_unavailable"}
COVERAGE_FIELDS = [
    "prompt_id",
    "prompt_type",
    "prompt_text",
    "coverage_disposition",
    "fact_or_review_ids",
    "note",
    "mapping_status",
]
COVERAGE_DISPOSITIONS = {"fact_covered", "review_required", "comparison_metric_only"}


class CoverageValidationError(ValueError):
    pass


@dataclass
class JudgeSettings:
    mode: str = "off"
    provider: str = "openai"
    model: str = "gpt-5-mini"
    retries: int = 1


@dataclass
class JudgeUsage:
    calls: int = 0
    cache_hits: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    unavailable: int = 0


class SemanticFactJudge:
    def __init__(self, root: Path, month: str, settings: JudgeSettings):
        self.root = root
        self.month = month
        self.settings = settings
        self.usage = JudgeUsage()
        self.fact_base_path, self.coverage_path = fact_base_paths(root, month)
        self.payload = read_json(self.fact_base_path)
        self.fact_base_version = str(self.payload.get("schema_version") or "unknown")
        self.facts = {fact["fact_id"]: fact for fact in self.payload.get("facts", [])}
        self.conflict_rules = self.payload.get("conflict_rules", [])
        self.coverage = load_coverage(self.coverage_path)
        self.cache_path = root / "runs" / month / "fact_judge_cache.jsonl"
        self.cache = {
            row["cache_key"]: row
            for row in read_jsonl(self.cache_path)
            if row.get("cache_key")
        }
        self._cache_dirty = False

    def judge_answer(self, prompt: dict[str, Any], answer: str, answer_hash: str) -> dict[str, Any]:
        coverage = self.coverage.get(prompt["prompt_id"])
        base = {
            "mode": self.settings.mode,
            "provider": self.settings.provider if self.settings.mode == "live" else self.settings.mode,
            "model": self.settings.model if self.settings.mode == "live" else "local-mock-v1",
            "fact_base_version": self.fact_base_version,
            "coverage_disposition": coverage.get("coverage_disposition") if coverage else "unmapped",
            "results": [],
        }
        if self.settings.mode == "off" or not coverage:
            return summarize(base)
        if coverage.get("coverage_disposition") == "comparison_metric_only":
            return summarize(base)

        base["results"].extend(detect_conflicts(answer, self.conflict_rules))

        fact_ids = split_fact_ids(coverage.get("fact_or_review_ids", ""))
        selected = [
            self.facts[fact_id]
            for fact_id in fact_ids
            if fact_id in self.facts and self.facts[fact_id].get("status") == "READY_FOR_JUDGE"
        ]
        for fact in selected:
            dimensions = activated_qualifier_dimensions(prompt.get("prompt_text", ""), answer)
            cache_key = stable_hash(
                [
                    answer_hash,
                    prompt["prompt_id"],
                    fact["fact_id"],
                    self.fact_base_version,
                    self.settings.mode,
                    self.settings.provider,
                    self.settings.model,
                    dimensions,
                ]
            )
            cached = self.cache.get(cache_key)
            if cached:
                self.usage.cache_hits += 1
                result = dict(cached["result"])
                result["cached"] = True
            else:
                result = self._judge_fact(prompt, answer, fact, dimensions)
                if result.get("verdict") != "judge_unavailable":
                    self.cache[cache_key] = {"cache_key": cache_key, "result": result}
                    self._cache_dirty = True
            base["results"].append(result)
        return summarize(base)

    def _judge_fact(
        self,
        prompt: dict[str, Any],
        answer: str,
        fact: dict[str, Any],
        dimensions: list[str],
    ) -> dict[str, Any]:
        if self.settings.mode == "mock":
            self.usage.calls += 1
            return mock_verdict(answer, fact, dimensions)
        if self.settings.mode != "live":
            raise ValueError(f"Unsupported fact judge mode: {self.settings.mode}")
        return self._live_verdict(prompt, answer, fact, dimensions)

    def _live_verdict(
        self,
        prompt: dict[str, Any],
        answer: str,
        fact: dict[str, Any],
        dimensions: list[str],
    ) -> dict[str, Any]:
        if self.settings.provider != "openai":
            self.usage.unavailable += 1
            return unavailable_result(fact, dimensions, f"Unsupported judge provider: {self.settings.provider}")
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            self.usage.unavailable += 1
            return unavailable_result(fact, dimensions, "Missing OPENAI_API_KEY")
        judge_input = build_judge_input(prompt, answer, fact, dimensions)
        payload = {
            "model": self.settings.model,
            "max_output_tokens": 500,
            "input": [
                {
                    "role": "system",
                    "content": (
                        "You are a strict product-fact evaluator. Return only one JSON object with keys "
                        "verdict, reason, answer_excerpt. verdict must be correct, incorrect, "
                        "not_enough_information, or not_applicable."
                    ),
                },
                {"role": "user", "content": judge_input},
            ],
        }
        last_error = "judge request failed"
        for _ in range(max(1, self.settings.retries + 1)):
            try:
                data = _post_json(
                    "https://api.openai.com/v1/responses",
                    payload,
                    {"Authorization": f"Bearer {api_key}"},
                )
                self.usage.calls += 1
                usage = data.get("usage", {})
                self.usage.input_tokens += int(usage.get("input_tokens", estimate_tokens(judge_input)))
                output = extract_openai_response_text(data)
                self.usage.output_tokens += int(usage.get("output_tokens", estimate_tokens(output)))
                parsed = parse_judge_json(output)
                return normalize_result(parsed, fact, dimensions)
            except ProviderError as exc:
                last_error = str(exc)
                if not exc.retryable:
                    break
            except (ValueError, json.JSONDecodeError) as exc:
                last_error = str(exc)
        self.usage.unavailable += 1
        return unavailable_result(fact, dimensions, last_error)

    def flush_cache(self) -> None:
        if self._cache_dirty:
            write_jsonl(self.cache_path, self.cache.values())
            self._cache_dirty = False


def fact_base_paths(root: Path, month: str) -> tuple[Path, Path]:
    config = canonical_data_root(root) / "config"
    fact_base = config / "tidb_fact_base_v2.json"
    coverage = config / f"tidb_fact_coverage_{month}.csv"
    if not fact_base.exists():
        raise CoverageValidationError(f"Semantic fact base not found: {fact_base}")
    if not coverage.exists():
        raise CoverageValidationError(
            f"Fact coverage for {month} has not been prepared. Run `./geo-bench --data-dir {root} "
            f"prepare-fact-coverage --month {month}`, then review and approve the generated mappings."
        )
    return fact_base, coverage


def load_coverage(path: Path) -> dict[str, dict[str, str]]:
    return {row["prompt_id"]: row for row in load_coverage_rows(path)}


def load_coverage_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def prepare_fact_coverage(root: Path, month: str, from_month: str | None = None) -> dict[str, Any]:
    canonical = canonical_data_root(root)
    prompts_path = canonical / "prompts" / month / "prompts.json"
    if not prompts_path.exists():
        raise CoverageValidationError(
            f"Prompt set for {month} does not exist: {prompts_path}. Prepare the monthly prompts first."
        )
    prompts = [prompt for prompt in read_json(prompts_path) if prompt.get("brand_class") == "branded"]
    config = canonical / "config"
    current_path = config / f"tidb_fact_coverage_{month}.csv"
    current_rows = load_coverage_rows(current_path) if current_path.exists() else []

    previous_path = previous_coverage_path(config, month, from_month)
    previous_rows = load_coverage_rows(previous_path) if previous_path else []
    sources = [
        {row.get("prompt_id"): row for row in rows}
        for rows in [current_rows, previous_rows]
    ]

    output: list[dict[str, str]] = []
    reused = 0
    needs_review = 0
    for prompt in prompts:
        source = next(
            (
                rows[prompt["prompt_id"]]
                for rows in sources
                if prompt["prompt_id"] in rows
                and rows[prompt["prompt_id"]].get("prompt_text") == prompt.get("prompt_text")
            ),
            None,
        )
        if source:
            output.append(
                {
                    "prompt_id": prompt["prompt_id"],
                    "prompt_type": str(prompt.get("prompt_type", "")),
                    "prompt_text": str(prompt.get("prompt_text", "")),
                    "coverage_disposition": source.get("coverage_disposition", ""),
                    "fact_or_review_ids": source.get("fact_or_review_ids", ""),
                    "note": source.get("note", ""),
                    "mapping_status": source.get("mapping_status") or "approved",
                }
            )
            reused += 1
            if (source.get("mapping_status") or "approved") != "approved":
                needs_review += 1
        else:
            output.append(
                {
                    "prompt_id": prompt["prompt_id"],
                    "prompt_type": str(prompt.get("prompt_type", "")),
                    "prompt_text": str(prompt.get("prompt_text", "")),
                    "coverage_disposition": "review_required",
                    "fact_or_review_ids": "",
                    "note": "AUTO-GENERATED: select the appropriate fact or review IDs and approve this mapping.",
                    "mapping_status": "needs_review",
                }
            )
            needs_review += 1

    if not current_path.exists() or not coverage_rows_equivalent(current_rows, output):
        ensure_dir(current_path.parent)
        with current_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=COVERAGE_FIELDS, lineterminator="\n")
            writer.writeheader()
            writer.writerows(output)
    return {
        "path": str(current_path),
        "source_path": str(previous_path) if previous_path else None,
        "total": len(output),
        "reused": reused,
        "needs_review": needs_review,
    }


def previous_coverage_path(config: Path, month: str, from_month: str | None) -> Path | None:
    if from_month:
        path = config / f"tidb_fact_coverage_{from_month}.csv"
        if not path.exists():
            raise CoverageValidationError(f"Requested source coverage does not exist: {path}")
        return path
    candidates = []
    for path in config.glob("tidb_fact_coverage_????-??.csv"):
        match = re.fullmatch(r"tidb_fact_coverage_(\d{4}-\d{2})\.csv", path.name)
        if match and match.group(1) < month:
            candidates.append((match.group(1), path))
    return max(candidates, default=(None, None))[1]


def coverage_rows_equivalent(current: list[dict[str, str]], generated: list[dict[str, str]]) -> bool:
    if len(current) != len(generated):
        return False
    for old, new in zip(current, generated):
        if any((old.get(field) or ("approved" if field == "mapping_status" else "")) != new.get(field, "") for field in COVERAGE_FIELDS):
            return False
    return True


def validate_fact_coverage(root: Path, month: str) -> dict[str, Any]:
    canonical = canonical_data_root(root)
    prompts_path = canonical / "prompts" / month / "prompts.json"
    coverage_path = canonical / "config" / f"tidb_fact_coverage_{month}.csv"
    fact_base_path = canonical / "config" / "tidb_fact_base_v2.json"
    if not prompts_path.exists():
        raise CoverageValidationError(f"Prompt set for {month} does not exist: {prompts_path}")
    if not coverage_path.exists():
        raise CoverageValidationError(
            f"Fact coverage for {month} has not been prepared. Run `./geo-bench --data-dir {root} "
            f"prepare-fact-coverage --month {month}`, then review and approve the generated mappings."
        )
    if not fact_base_path.exists():
        raise CoverageValidationError(f"Semantic fact base not found: {fact_base_path}")

    prompts = {
        prompt["prompt_id"]: prompt
        for prompt in read_json(prompts_path)
        if prompt.get("brand_class") == "branded"
    }
    rows = load_coverage_rows(coverage_path)
    row_counts: dict[str, int] = {}
    for row in rows:
        prompt_id = row.get("prompt_id", "")
        row_counts[prompt_id] = row_counts.get(prompt_id, 0) + 1
    by_id = {row.get("prompt_id", ""): row for row in rows}
    payload = read_json(fact_base_path)
    facts = {fact["fact_id"]: fact for fact in payload.get("facts", [])}
    review_ids = {item["review_id"] for item in payload.get("review_queue", [])}
    known_ids = set(facts) | review_ids
    errors: list[str] = []

    for prompt_id, count in row_counts.items():
        if count > 1:
            errors.append(f"{prompt_id}: duplicate coverage rows")
    missing = sorted(set(prompts) - set(by_id))
    extra = sorted(set(by_id) - set(prompts))
    if missing:
        errors.append("missing branded prompts: " + ", ".join(missing))
    if extra:
        errors.append("coverage rows without current branded prompts: " + ", ".join(extra))

    for prompt_id, prompt in prompts.items():
        row = by_id.get(prompt_id)
        if not row:
            continue
        if row.get("prompt_text") != prompt.get("prompt_text"):
            errors.append(f"{prompt_id}: prompt text changed and the mapping must be reviewed")
        if row.get("prompt_type") != str(prompt.get("prompt_type", "")):
            errors.append(f"{prompt_id}: prompt type does not match the current prompt set")
        mapping_status = row.get("mapping_status") or "approved"
        if mapping_status != "approved":
            errors.append(f"{prompt_id}: mapping_status is {mapping_status}; review and set it to approved")
        disposition = row.get("coverage_disposition", "")
        if disposition not in COVERAGE_DISPOSITIONS:
            errors.append(f"{prompt_id}: invalid coverage_disposition {disposition!r}")
            continue
        fact_ids = split_fact_ids(row.get("fact_or_review_ids", ""))
        unknown = [item for item in fact_ids if item not in known_ids]
        if unknown:
            errors.append(f"{prompt_id}: unknown fact or review IDs: {', '.join(unknown)}")
        if disposition == "comparison_metric_only" and fact_ids:
            errors.append(f"{prompt_id}: comparison_metric_only must not list fact or review IDs")
        if disposition != "comparison_metric_only" and not fact_ids:
            errors.append(f"{prompt_id}: select at least one fact or review ID")
        if disposition == "fact_covered":
            non_fact_ids = [item for item in fact_ids if item not in facts]
            held_facts = [item for item in fact_ids if item in facts and facts[item].get("status") != "READY_FOR_JUDGE"]
            if non_fact_ids:
                errors.append(f"{prompt_id}: fact_covered contains review IDs: {', '.join(non_fact_ids)}")
            if held_facts:
                errors.append(f"{prompt_id}: fact_covered contains non-ready facts: {', '.join(held_facts)}")

    if errors:
        details = "\n".join(f"- {error}" for error in errors)
        raise CoverageValidationError(
            f"Fact coverage for {month} is not ready:\n{details}\n"
            f"Review {coverage_path} before running the semantic judge."
        )
    return {"path": str(coverage_path), "total": len(prompts), "approved": len(prompts)}


def split_fact_ids(value: str) -> list[str]:
    return [item.strip() for item in value.split("|") if item.strip()]


def detect_conflicts(answer: str, rules: list[dict[str, Any]]) -> list[dict[str, Any]]:
    lower = answer.lower()
    active_ids = {rule.get("conflict_id") for rule in rules}
    retired_context = r"(?:former(?:ly)?|old name|previously|renamed|now called|became|replaced)"
    patterns = {
        "drive9_current_name": r"\bdrive9\b\s+(?:is|provides|offers|serves as)\b",
        "mem9_current_name": r"\bmem9\b\s+(?:is|provides|offers|serves as)\b",
        "starter_serverless_double_product": r"\btidb cloud starter\b[^.\n]{0,100}\b(?:and|or|versus|vs\.?)\b[^.\n]{0,100}\btidb cloud serverless\b",
        "tikv_tiflash_role_swap": r"\b(?:tikv[^.\n]{0,50}(?:columnar|analytics store)|tiflash[^.\n]{0,50}(?:row store|transactional row))\b",
    }
    results = []
    for conflict_id, pattern in patterns.items():
        if conflict_id not in active_ids:
            continue
        match = re.search(pattern, lower)
        if not match:
            continue
        context = lower[max(0, match.start() - 45) : min(len(lower), match.end() + 45)]
        if conflict_id in {"drive9_current_name", "mem9_current_name", "starter_serverless_double_product"} and re.search(
            retired_context, context
        ):
            continue
        results.append(
            {
                "fact_id": f"conflict:{conflict_id}",
                "verdict": "incorrect",
                "reason": "The answer violates an approved cross-fact conflict rule.",
                "answer_excerpt": answer[match.start() : match.end()][:500],
                "qualifier_check_activated": False,
                "qualifier_dimensions": [],
                "cached": False,
            }
        )
    return results


PROMPT_QUALIFIER_PATTERNS = {
    "maturity": r"\b(?:availability|available|ga|generally available|public preview|preview|beta|experimental|production.ready|maturity|supported)\b",
    "plan": r"\b(?:which|what|available on|supported on|included in|limited to)\s+(?:\w+\s+){0,3}plans?\b|\bplan availability\b",
    "region": r"\b(?:which|what|available in|supported in|deploy in)\s+(?:\w+\s+){0,3}regions?\b|\bdata residency\b",
    "version": r"\b(?:which|what|since)\s+(?:\w+\s+){0,2}versions?\b|\brelease availability\b",
    "access": r"\b(?:who can|how (?:do|can) .* access|access requirements?|eligibility|invite|allowlist|sign.?up)\b",
}

ANSWER_QUALIFIER_PATTERNS = {
    "maturity": r"\b(?:is|isn't|is not|remains|became)\s+(?:generally available|ga|in public preview|a preview|beta|experimental|production.ready)\b",
    "plan": r"\b(?:available|supported|included|limited|exclusive|only|requires?)\b[^.\n]{0,60}\b(?:starter|essential|premium|dedicated|self.managed|cloud zero|serverless|plans?)\b",
    "region": r"\b(?:available|supported|hosted|deployed|limited)\b[^.\n]{0,60}\b(?:regions?|countries|us|usa|eu|europe|asia|aws|gcp|azure)\b",
    "version": r"\b(?:since|as of|introduced in|available in|supported in|requires?)\b[^.\n]{0,40}\b(?:v\d+(?:\.\d+){0,2}|version|release|stable branch)\b",
    "access": r"\b(?:access requires?|available to|limited to|invite.only|allowlist|eligible|eligibility|sign.?up)\b",
}


def activated_qualifier_dimensions(prompt: str, answer: str) -> list[str]:
    question = prompt.lower()
    response = answer.lower()
    return [
        name
        for name in PROMPT_QUALIFIER_PATTERNS
        if re.search(PROMPT_QUALIFIER_PATTERNS[name], question)
        or re.search(ANSWER_QUALIFIER_PATTERNS[name], response)
    ]


def mock_verdict(answer: str, fact: dict[str, Any], dimensions: list[str]) -> dict[str, Any]:
    fact_id = fact["fact_id"]
    marker = re.search(rf"\[\[fact:{re.escape(fact_id)}:(correct|incorrect|not_enough_information|not_applicable)\]\]", answer)
    verdict = marker.group(1) if marker else "correct"
    excerpt = marker.group(0) if marker else answer[:160]
    return {
        "fact_id": fact_id,
        "verdict": verdict,
        "reason": "Deterministic mock verdict for pipeline validation.",
        "answer_excerpt": excerpt,
        "qualifier_check_activated": bool(dimensions),
        "qualifier_dimensions": dimensions,
        "cached": False,
    }


def build_judge_input(prompt: dict[str, Any], answer: str, fact: dict[str, Any], dimensions: list[str]) -> str:
    active = ", ".join(dimensions) if dimensions else "none"
    return (
        f"Question: {prompt.get('prompt_text', '')}\n\n"
        f"Answer: {answer}\n\n"
        f"Fact instructions: {fact.get('judge_prompt', '')}\n\n"
        f"Pre-detected qualifier dimensions: {active}. The fact instructions remain authoritative."
    )


def parse_judge_json(value: str) -> dict[str, Any]:
    text = value.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.IGNORECASE)
    return json.loads(text)


def normalize_result(value: dict[str, Any], fact: dict[str, Any], dimensions: list[str]) -> dict[str, Any]:
    verdict = str(value.get("verdict", "")).lower()
    if verdict not in VERDICTS - {"judge_unavailable"}:
        raise ValueError(f"Invalid judge verdict: {verdict}")
    return {
        "fact_id": fact["fact_id"],
        "verdict": verdict,
        "reason": str(value.get("reason", ""))[:500],
        "answer_excerpt": str(value.get("answer_excerpt", ""))[:500],
        "qualifier_check_activated": bool(dimensions),
        "qualifier_dimensions": dimensions,
        "cached": False,
    }


def unavailable_result(fact: dict[str, Any], dimensions: list[str], reason: str) -> dict[str, Any]:
    return {
        "fact_id": fact["fact_id"],
        "verdict": "judge_unavailable",
        "reason": reason[:500],
        "answer_excerpt": "",
        "qualifier_check_activated": bool(dimensions),
        "qualifier_dimensions": dimensions,
        "cached": False,
    }


def summarize(payload: dict[str, Any]) -> dict[str, Any]:
    counts = {verdict: 0 for verdict in VERDICTS}
    for result in payload["results"]:
        counts[result["verdict"]] += 1
    decided = counts["correct"] + counts["incorrect"]
    payload.update(
        {
            "selected_facts": len(payload["results"]),
            "checked_facts": decided,
            "correct_facts": counts["correct"],
            "incorrect_facts": counts["incorrect"],
            "not_enough_information_facts": counts["not_enough_information"],
            "not_applicable_facts": counts["not_applicable"],
            "unavailable_facts": counts["judge_unavailable"],
            "accuracy": round(counts["correct"] / decided, 4) if decided else None,
        }
    )
    return payload
