from __future__ import annotations

import base64
import csv
import datetime as dt
import difflib
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from .io_utils import canonical_data_root, ensure_dir, read_json, read_jsonl, stable_hash, write_json
from .scoring import PRODUCT_ALIASES


DATAFORSEO_PAA_ENDPOINT = "https://api.dataforseo.com/v3/serp/google/organic/live/advanced"
DATAFORSEO_TRENDS_ENDPOINT = "https://api.dataforseo.com/v3/keywords_data/google_trends/explore/live"
SEMRUSH_KEYWORD_ENDPOINT = "https://api.semrush.com/apis/v4/keywords/v1/metrics"

SEED_COLUMNS = ["theme", "seed_query", "brand_class", "match_terms", "status"]
INTERNAL_COLUMNS = ["query", "source", "frequency", "notes"]
QUESTION_WORDS = {"what", "which", "how", "why", "when", "where", "who", "can", "does", "do", "is", "are", "should"}
STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "best", "by", "can", "database", "databases",
    "do", "does", "for", "from", "how", "i", "in", "is", "it", "of", "on", "or", "should",
    "the", "to", "use", "versus", "vs", "what", "when", "where", "which", "with",
}
HIGH_INTENT_TERMS = {
    "best", "recommend", "recommended", "choose", "choice", "compare", "comparison", "versus", "vs",
    "alternative", "alternatives", "migrate", "migration", "pricing", "price", "cost", "buy", "adopt",
}
EVALUATION_TERMS = {
    "support", "supports", "suitable", "production", "ready", "scale", "scaling", "architecture",
    "integrate", "integration", "performance", "reliability", "security", "compliance", "difference",
    "transactions", "transactional", "latency", "throughput",
}
COMPARISON_TERMS = {" vs ", " versus ", "compare", "comparison", "alternative", "alternatives", "difference between"}


class PromptResearchError(RuntimeError):
    pass


@dataclass
class ResearchSettings:
    max_candidates: int = 20
    country: str = "US"
    location_code: int = 2840
    language_code: str = "en"
    refresh: bool = False
    offline: bool = False
    include_paa: bool = True
    include_trends: bool = True
    include_semrush: bool = True
    workers: int = 4
    max_seeds: int | None = None
    internal_signals_path: Path | None = None
    seed_file: Path | None = None


def run_prompt_research(root: Path, month: str, settings: ResearchSettings) -> dict[str, Any]:
    """Collect monthly research signals and write review-only prompt candidates."""
    canonical_root = canonical_data_root(root)
    seed_path = settings.seed_file or canonical_root / "config" / "prompt_research_seeds.csv"
    bundled_seed_path = Path(__file__).resolve().parent.parent / "geo-benchmark" / "config" / "prompt_research_seeds.csv"
    if not seed_path.exists() and settings.seed_file is None and bundled_seed_path.exists():
        ensure_dir(seed_path.parent)
        seed_path.write_bytes(bundled_seed_path.read_bytes())
    if not seed_path.exists():
        raise PromptResearchError(f"Prompt research seed file not found: {seed_path}")
    seeds = load_seed_queries(seed_path)
    if settings.max_seeds is not None:
        seeds = seeds[: settings.max_seeds]
    if not seeds:
        raise PromptResearchError("No approved prompt research seeds were found.")

    report_dir = root / "reports" / month / "prompt-research"
    cache_dir = report_dir / "raw"
    ensure_dir(cache_dir)
    internal_path = settings.internal_signals_path or canonical_root / "prompt-research" / month / "internal_signals.csv"
    ensure_internal_template(internal_path)

    warnings: list[str] = []
    signals: list[dict[str, Any]] = []
    profiles = build_theme_profiles(seeds)
    signals.extend(load_internal_signals(internal_path, profiles, warnings))
    signals.extend(load_fan_out_signals(root, month, profiles))

    external, usage, external_warnings = collect_external_signals(seeds, cache_dir, settings)
    signals.extend(external)
    warnings.extend(external_warnings)
    signals.sort(key=lambda item: (item["theme"], item["signal_group"], item["source"], item["normalized_text"]))

    prompts_path = canonical_root / "prompts" / month / "prompts.json"
    prompts = read_json(prompts_path, default=[])
    candidates = build_candidates(signals, prompts, seeds, settings.max_candidates)
    write_research_outputs(report_dir, month, candidates, signals, usage, warnings, len(prompts), seed_path, internal_path)
    return {
        "month": month,
        "candidate_count": len(candidates),
        "candidates": candidates,
        "signal_count": len(signals),
        "warnings": warnings,
        "usage": usage,
        "report_dir": str(report_dir),
    }


def load_seed_queries(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = set(SEED_COLUMNS) - set(reader.fieldnames or [])
        if missing:
            raise PromptResearchError(f"Seed file is missing columns: {', '.join(sorted(missing))}")
        for row in reader:
            if row.get("status", "").strip().lower() != "approved":
                continue
            theme = row.get("theme", "").strip()
            query = row.get("seed_query", "").strip()
            brand_class = row.get("brand_class", "").strip().lower()
            if not theme or not query or brand_class not in {"branded", "non_branded"}:
                raise PromptResearchError(f"Invalid approved seed row: {row}")
            rows.append({
                "theme": theme,
                "seed_query": query,
                "brand_class": brand_class,
                "match_terms": [term.strip().lower() for term in row.get("match_terms", "").split("|") if term.strip()],
            })
    return rows


def ensure_internal_template(path: Path) -> None:
    if path.exists():
        return
    ensure_dir(path.parent)
    with path.open("w", encoding="utf-8", newline="") as handle:
        csv.DictWriter(handle, fieldnames=INTERNAL_COLUMNS).writeheader()


def load_internal_signals(
    path: Path,
    profiles: dict[str, dict[str, Any]],
    warnings: list[str] | None = None,
) -> list[dict[str, Any]]:
    warnings = warnings if warnings is not None else []
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if "query" not in (reader.fieldnames or []):
            raise PromptResearchError(f"Internal signals file must contain a query column: {path}")
        for row in reader:
            text = str(row.get("query", "")).strip()
            if not text:
                continue
            themes = assign_themes(text, profiles)
            if not themes:
                warnings.append(f"Internal signal could not be mapped to an approved theme: {text}")
                continue
            try:
                frequency = max(1, int(float(row.get("frequency") or 1)))
            except ValueError:
                frequency = 1
            for theme in themes:
                rows.append(signal("internal", row.get("source") or "internal", text, theme, frequency, {"notes": row.get("notes", "")}))
    return rows


def load_fan_out_signals(root: Path, month: str, profiles: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    counts: Counter[tuple[str, str]] = Counter()
    providers: defaultdict[tuple[str, str], set[str]] = defaultdict(set)
    for row in read_jsonl(root / "runs" / month / "raw_answers.jsonl"):
        if row.get("status") != "ok" or row.get("fan_out_status") != "captured":
            continue
        for query in row.get("fan_out_queries") or []:
            text = str(query).strip()
            for theme in assign_themes(text, profiles):
                key = (theme, normalize_text(text))
                counts[key] += 1
                providers[key].add(str(row.get("model_surface", "unknown")))
    return [
        signal("model", "fan_out", text, theme, frequency, {"providers": sorted(providers[(theme, text)])})
        for (theme, text), frequency in sorted(counts.items())
    ]


def collect_external_signals(
    seeds: list[dict[str, Any]],
    cache_dir: Path,
    settings: ResearchSettings,
) -> tuple[list[dict[str, Any]], dict[str, Any], list[str]]:
    signals: list[dict[str, Any]] = []
    warnings: list[str] = []
    usage = {"dataforseo_calls": 0, "dataforseo_cost_usd": 0.0, "semrush_calls": 0, "semrush_api_units_estimate": 0}
    if settings.offline:
        missing_ok = True
    else:
        missing_ok = False
        if (settings.include_paa or settings.include_trends) and not dataforseo_credentials():
            raise PromptResearchError("Set DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD, or use --offline/skip the DataForSEO sources.")
        if settings.include_semrush and not os.getenv("SEMRUSH_API_KEY"):
            raise PromptResearchError("Set SEMRUSH_API_KEY, or use --offline/--skip-semrush.")

    if settings.include_paa:
        results = parallel_seed_fetch(
            seeds,
            settings.workers,
            lambda seed: cached_external_call(
                cache_dir / f"paa-{stable_hash([seed['seed_query'], settings.location_code, settings.language_code])[:16]}.json",
                lambda: fetch_dataforseo_paa(seed["seed_query"], settings),
                settings.refresh,
                settings.offline,
            ),
        )
        for seed, response, cached, error in results:
            if error:
                warnings.append(f"PAA failed for '{seed['seed_query']}': {error}")
                continue
            if response is None:
                if not missing_ok:
                    warnings.append(f"PAA cache unavailable for '{seed['seed_query']}'.")
                continue
            if not cached:
                usage["dataforseo_calls"] += 1
                usage["dataforseo_cost_usd"] += dataforseo_cost(response)
            for item in extract_paa_questions(response):
                signals.append(signal("external", "people_also_ask", item["question"], seed["theme"], 1, {
                    "seed_query": seed["seed_query"], "position": item.get("position"), "source_url": item.get("source_url"),
                }))

    if settings.include_semrush:
        results = parallel_seed_fetch(
            seeds,
            settings.workers,
            lambda seed: cached_external_call(
                cache_dir / f"semrush-{stable_hash([seed['seed_query'], settings.country])[:16]}.json",
                lambda: fetch_semrush_metrics(seed["seed_query"], settings),
                settings.refresh,
                settings.offline,
            ),
        )
        for seed, response, cached, error in results:
            if error:
                warnings.append(f"Semrush failed for '{seed['seed_query']}': {error}")
                continue
            if response is None:
                continue
            if not cached:
                usage["semrush_calls"] += 1
                usage["semrush_api_units_estimate"] += 20
            data = response.get("data") or {}
            volume = numeric(data.get("search_volume"))
            if volume > 0:
                signals.append(signal("external", "semrush", seed["seed_query"], seed["theme"], max(1, int(volume)), {
                    "search_volume": volume,
                    "intents": data.get("intents") or [],
                    "keyword_difficulty": numeric(data.get("keyword_difficulty")),
                    "trends": data.get("trends") or [],
                    "serp_features": data.get("serp_features") or [],
                }))

    if settings.include_trends:
        for batch in chunks(seeds, 5):
            queries = [seed["seed_query"] for seed in batch]
            cache_path = cache_dir / f"trends-{stable_hash([queries, settings.location_code])[:16]}.json"
            try:
                response, cached = cached_external_call(
                    cache_path,
                    lambda queries=queries: fetch_dataforseo_trends(queries, settings),
                    settings.refresh,
                    settings.offline,
                )
            except PromptResearchError as exc:
                warnings.append(f"Trends failed for {queries}: {exc}")
                continue
            if response is None:
                continue
            if not cached:
                usage["dataforseo_calls"] += 1
                usage["dataforseo_cost_usd"] += dataforseo_cost(response)
            trend_stats = extract_trend_stats(response, queries)
            for seed in batch:
                stats = trend_stats.get(seed["seed_query"])
                if stats and stats.get("points", 0) > 0:
                    signals.append(signal("external", "google_trends", seed["seed_query"], seed["theme"], 1, stats))

    usage["dataforseo_cost_usd"] = round(float(usage["dataforseo_cost_usd"]), 6)
    return signals, usage, warnings


def parallel_seed_fetch(
    seeds: list[dict[str, Any]],
    workers: int,
    fetcher: Callable[[dict[str, Any]], tuple[dict[str, Any] | None, bool]],
) -> list[tuple[dict[str, Any], dict[str, Any] | None, bool, str | None]]:
    results: list[tuple[dict[str, Any], dict[str, Any] | None, bool, str | None]] = []
    with ThreadPoolExecutor(max_workers=max(1, workers)) as executor:
        futures = {executor.submit(fetcher, seed): seed for seed in seeds}
        for future in as_completed(futures):
            seed = futures[future]
            try:
                response, cached = future.result()
                results.append((seed, response, cached, None))
            except Exception as exc:  # Per-seed failures are reported without losing the completed benchmark.
                results.append((seed, None, False, str(exc)))
    return results


def cached_external_call(
    path: Path,
    fetcher: Callable[[], dict[str, Any]],
    refresh: bool,
    offline: bool,
) -> tuple[dict[str, Any] | None, bool]:
    if path.exists() and not refresh:
        return read_json(path), True
    if offline:
        return None, False
    response = fetcher()
    write_json(path, response)
    return response, False


def fetch_dataforseo_paa(query: str, settings: ResearchSettings) -> dict[str, Any]:
    return request_json(
        DATAFORSEO_PAA_ENDPOINT,
        "POST",
        [{
            "keyword": query,
            "location_code": settings.location_code,
            "language_code": settings.language_code,
            "device": "desktop",
            "depth": 10,
        }],
        {"Authorization": dataforseo_auth_header()},
    )


def fetch_dataforseo_trends(queries: list[str], settings: ResearchSettings) -> dict[str, Any]:
    return request_json(
        DATAFORSEO_TRENDS_ENDPOINT,
        "POST",
        [{"keywords": queries, "location_code": settings.location_code, "time_range": "past_12_months", "type": "web"}],
        {"Authorization": dataforseo_auth_header()},
    )


def fetch_semrush_metrics(query: str, settings: ResearchSettings) -> dict[str, Any]:
    url = SEMRUSH_KEYWORD_ENDPOINT + "?" + urllib.parse.urlencode({"keyword": query, "country": settings.country})
    return request_json(url, "GET", None, {"Authorization": f"Apikey {os.environ['SEMRUSH_API_KEY']}"})


def request_json(url: str, method: str, payload: Any, headers: dict[str, str]) -> dict[str, Any]:
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    request = urllib.request.Request(url, data=body, method=method, headers={"Content-Type": "application/json", **headers})
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            result = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:500]
        raise PromptResearchError(f"HTTP {exc.code}: {detail}") from exc
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise PromptResearchError(str(exc)) from exc
    if not isinstance(result, dict):
        raise PromptResearchError("API returned a non-object response.")
    if url.startswith("https://api.dataforseo.com"):
        if int(result.get("status_code", 0)) != 20000:
            raise PromptResearchError(str(result.get("status_message") or "DataForSEO request failed"))
        failed_tasks = [
            task for task in result.get("tasks") or []
            if int(task.get("status_code", 0)) != 20000
        ]
        if failed_tasks:
            message = failed_tasks[0].get("status_message") or "DataForSEO task failed"
            raise PromptResearchError(str(message))
    if url.startswith(SEMRUSH_KEYWORD_ENDPOINT) and not (result.get("meta") or {}).get("success", False):
        raise PromptResearchError(str((result.get("error") or {}).get("message") or "Semrush request failed"))
    return result


def dataforseo_credentials() -> tuple[str, str] | None:
    login = os.getenv("DATAFORSEO_LOGIN")
    password = os.getenv("DATAFORSEO_PASSWORD")
    return (login, password) if login and password else None


def dataforseo_auth_header() -> str:
    credentials = dataforseo_credentials()
    if not credentials:
        raise PromptResearchError("Missing DataForSEO credentials.")
    return "Basic " + base64.b64encode(f"{credentials[0]}:{credentials[1]}".encode()).decode()


def dataforseo_cost(response: dict[str, Any]) -> float:
    return sum(numeric(task.get("cost")) for task in response.get("tasks") or [])


def extract_paa_questions(response: dict[str, Any]) -> list[dict[str, Any]]:
    found: dict[str, dict[str, Any]] = {}

    def visit(value: Any) -> None:
        if isinstance(value, list):
            for item in value:
                visit(item)
            return
        if not isinstance(value, dict):
            return
        item_type = str(value.get("type", ""))
        if item_type in {"people_also_ask", "people_also_ask_element"}:
            question = str(value.get("title") or value.get("question") or "").strip()
            if question and looks_like_question(question):
                key = normalize_text(question)
                found.setdefault(key, {
                    "question": question,
                    "position": value.get("rank_group") or value.get("rank_absolute") or value.get("position"),
                    "source_url": value.get("url"),
                })
        for child in value.values():
            visit(child)

    visit(response.get("tasks") or [])
    return list(found.values())


def extract_trend_stats(response: dict[str, Any], queries: list[str]) -> dict[str, dict[str, Any]]:
    values: defaultdict[str, list[float]] = defaultdict(list)

    def visit(value: Any) -> None:
        if isinstance(value, list):
            for item in value:
                visit(item)
            return
        if not isinstance(value, dict):
            return
        if value.get("type") == "google_trends_graph":
            keywords = value.get("keywords") or queries
            for point in value.get("data") or []:
                point_values = point.get("values") or point.get("value") or []
                if isinstance(point_values, (int, float)) and len(keywords) == 1:
                    point_values = [point_values]
                if isinstance(point_values, list):
                    for index, number in enumerate(point_values[: len(keywords)]):
                        if isinstance(number, (int, float)):
                            values[str(keywords[index])].append(float(number))
        for child in value.values():
            visit(child)

    visit(response.get("tasks") or [])
    output: dict[str, dict[str, Any]] = {}
    for query in queries:
        series = values.get(query, [])
        if not series:
            continue
        width = max(1, len(series) // 3)
        early = sum(series[:width]) / width
        recent = sum(series[-width:]) / width
        if recent > early * 1.1:
            direction = "rising"
        elif recent < early * 0.9:
            direction = "falling"
        else:
            direction = "steady"
        output[query] = {"points": len(series), "trend_direction": direction, "recent_interest": round(recent, 2)}
    return output


def signal(group: str, source: str, text: str, theme: str, frequency: int, metadata: dict[str, Any]) -> dict[str, Any]:
    return {
        "signal_group": group,
        "source": source,
        "text": text.strip(),
        "normalized_text": normalize_text(text),
        "theme": theme,
        "frequency": max(1, int(frequency)),
        "metadata": metadata,
    }


def build_theme_profiles(seeds: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    profiles: dict[str, dict[str, Any]] = {}
    for seed in seeds:
        profile = profiles.setdefault(seed["theme"], {"tokens": set(), "phrases": set(), "brand_classes": set()})
        profile["tokens"].update(tokens(seed["seed_query"]))
        profile["phrases"].update(seed["match_terms"])
        profile["brand_classes"].add(seed["brand_class"])
    return profiles


def assign_themes(text: str, profiles: dict[str, dict[str, Any]]) -> list[str]:
    normalized = normalize_text(text)
    text_tokens = tokens(text)
    scores: list[tuple[float, str]] = []
    for theme, profile in profiles.items():
        phrase_hits = sum(1 for phrase in profile["phrases"] if phrase in normalized)
        overlap = len(text_tokens & profile["tokens"])
        denominator = max(1, min(len(text_tokens), len(profile["tokens"]), 5))
        score = phrase_hits * 2 + overlap / denominator
        if score >= 0.34:
            scores.append((score, theme))
    if not scores:
        return []
    scores.sort(reverse=True)
    best = scores[0][0]
    return [theme for score, theme in scores if score >= max(0.5, best * 0.72)][:2]


def build_candidates(
    signals: list[dict[str, Any]],
    existing_prompts: list[dict[str, Any]],
    seeds: list[dict[str, Any]],
    limit: int = 20,
) -> list[dict[str, Any]]:
    by_theme: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in signals:
        by_theme[item["theme"]].append(item)
    seed_by_theme: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
    for seed in seeds:
        seed_by_theme[seed["theme"]].append(seed)

    ranked: list[dict[str, Any]] = []
    for theme, theme_signals in by_theme.items():
        groups = sorted({item["signal_group"] for item in theme_signals})
        if len(groups) < 2:
            continue
        candidate_sources = [item for item in theme_signals if item["source"] == "people_also_ask"]
        candidate_sources += [item for item in theme_signals if item["signal_group"] == "model"]
        candidate_sources += [item for item in theme_signals if item["signal_group"] == "internal"]
        seen_texts: list[str] = []
        for item in candidate_sources:
            text = candidate_prompt_text(item["text"])
            if not usable_candidate(text):
                continue
            if any(text_similarity(text, seen) >= 0.86 for seen in seen_texts):
                continue
            seen_texts.append(text)
            maximum_similarity = max((text_similarity(text, str(prompt.get("prompt_text", ""))) for prompt in existing_prompts), default=0.0)
            if maximum_similarity >= 0.86:
                continue
            if maximum_similarity >= 0.58:
                coverage_label, coverage_score = "partially_covered", 50
            else:
                coverage_label, coverage_score = "new", 100
            intent_label, intent_score = buyer_intent(text)
            support_score = 100 if len(groups) == 3 else 67
            priority = round(0.50 * support_score + 0.30 * intent_score + 0.20 * coverage_score, 1)
            brand_class = infer_brand_class(text, seed_by_theme[theme])
            group = infer_prompt_group(text, brand_class)
            evidence = evidence_summary(theme_signals)
            ranked.append({
                "candidate_prompt": text,
                "theme": theme,
                "brand_class": brand_class,
                "group": group,
                "suggested_prompt_type": prompt_type_for_theme(theme),
                "signal_groups_matched": "|".join(groups),
                "signal_group_count": len(groups),
                "internal_support": evidence["internal"],
                "external_support": evidence["external"],
                "fan_out_support": evidence["model"],
                "buyer_intent": intent_label,
                "buyer_intent_score": intent_score,
                "coverage_gap": coverage_label,
                "nearest_existing_similarity": round(maximum_similarity, 3),
                "priority_score": priority,
                "source_question": item["text"],
                "source": item["source"],
                "review_status": "pending",
                "reviewer_notes": "",
                "recurrence": len(theme_signals),
            })

    ranked.sort(key=lambda row: (-row["priority_score"], -row["signal_group_count"], -row["recurrence"], row["candidate_prompt"]))
    selected: list[dict[str, Any]] = []
    theme_counts: Counter[str] = Counter()
    for row in ranked:
        if theme_counts[row["theme"]] >= 2:
            continue
        if any(text_similarity(row["candidate_prompt"], chosen["candidate_prompt"]) >= 0.86 for chosen in selected):
            continue
        selected.append(row)
        theme_counts[row["theme"]] += 1
        if len(selected) >= limit:
            break
    for rank, row in enumerate(selected, start=1):
        row["rank"] = rank
    return selected


def evidence_summary(signals: list[dict[str, Any]]) -> dict[str, str]:
    grouped: defaultdict[str, list[str]] = defaultdict(list)
    for item in signals:
        label = f"{item['source']}: {item['text']}"
        if label not in grouped[item["signal_group"]]:
            grouped[item["signal_group"]].append(label)
    return {group: " || ".join(grouped.get(group, [])[:5]) for group in ["internal", "external", "model"]}


def buyer_intent(text: str) -> tuple[str, int]:
    words = tokens(text, remove_stop_words=False)
    normalized = f" {normalize_text(text)} "
    if words & HIGH_INTENT_TERMS or normalized.startswith((" which ", " should ")):
        return "decision", 100
    if words & EVALUATION_TERMS:
        return "evaluation", 67
    return "education", 33


def infer_brand_class(text: str, theme_seeds: list[dict[str, Any]]) -> str:
    lower = normalize_text(text)
    for aliases in PRODUCT_ALIASES.values():
        if any(re.search(rf"(?<![a-z0-9]){re.escape(alias.lower())}(?![a-z0-9])", lower) for alias in aliases):
            return "branded"
    if theme_seeds and all(seed["brand_class"] == "branded" for seed in theme_seeds):
        return "branded"
    return "non_branded"


def infer_prompt_group(text: str, brand_class: str) -> str:
    normalized = f" {normalize_text(text)} "
    product_count = sum(
        1 for aliases in PRODUCT_ALIASES.values()
        if any(re.search(rf"(?<![a-z0-9]){re.escape(alias.lower())}(?![a-z0-9])", normalized) for alias in aliases)
    )
    if product_count >= 2 or any(term in normalized for term in COMPARISON_TERMS):
        return "comparison"
    return "accuracy" if brand_class == "branded" else "discovery"


def prompt_type_for_theme(theme: str) -> str:
    if theme.startswith("tidb_") or theme == "pytidb":
        return "TiDB Brand & Definitions"
    if theme in {"agent_memory", "agent_state", "ai_app_backend"}:
        return "AI Agent Infrastructure"
    if theme in {"transactional_vector_search", "hybrid_search_rag", "knowledge_graph"}:
        return "Hybrid Search & RAG"
    if theme in {"mysql_scaling", "mysql_migration"}:
        return "MySQL Scale & Migration"
    if theme in {"cloud_deployment", "serverless_database"}:
        return "Deployment & Cloud"
    if theme == "mcp_database":
        return "MCP & Developer Tooling"
    if theme == "database_observability":
        return "Observability"
    if theme == "database_comparison":
        return "Competitive Comparisons"
    return "Scale & Architecture"


def candidate_prompt_text(text: str) -> str:
    value = re.sub(r"\s+", " ", text).strip()
    if value and not value.endswith(("?", ".", "!")):
        value += "?"
    return value


def usable_candidate(text: str) -> bool:
    word_count = len(text.split())
    return 4 <= word_count <= 35 and looks_like_question(text)


def looks_like_question(text: str) -> bool:
    stripped = text.strip().lower()
    return stripped.endswith("?") or (stripped.split() and stripped.split()[0] in QUESTION_WORDS)


def text_similarity(left: str, right: str) -> float:
    left_normalized, right_normalized = normalize_text(left), normalize_text(right)
    if not left_normalized or not right_normalized:
        return 0.0
    left_tokens, right_tokens = tokens(left), tokens(right)
    union = left_tokens | right_tokens
    jaccard = len(left_tokens & right_tokens) / len(union) if union else 0.0
    containment = len(left_tokens & right_tokens) / max(1, min(len(left_tokens), len(right_tokens)))
    sequence = difflib.SequenceMatcher(None, left_normalized, right_normalized).ratio()
    return max(jaccard, containment * 0.9, sequence)


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9+#.]+", " ", str(text).lower())).strip()


def tokens(text: str, remove_stop_words: bool = True) -> set[str]:
    values = set(normalize_text(text).split())
    return values - STOP_WORDS if remove_stop_words else values


def chunks(items: list[Any], size: int) -> list[list[Any]]:
    return [items[index:index + size] for index in range(0, len(items), size)]


def numeric(value: Any) -> float:
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0


def write_research_outputs(
    report_dir: Path,
    month: str,
    candidates: list[dict[str, Any]],
    signals: list[dict[str, Any]],
    usage: dict[str, Any],
    warnings: list[str],
    prompt_count: int,
    seed_path: Path,
    internal_path: Path,
) -> None:
    ensure_dir(report_dir)
    candidate_columns = [
        "rank", "candidate_prompt", "theme", "brand_class", "group", "suggested_prompt_type",
        "signal_groups_matched", "signal_group_count", "internal_support", "external_support", "fan_out_support",
        "buyer_intent", "buyer_intent_score", "coverage_gap", "nearest_existing_similarity", "priority_score",
        "source", "source_question", "review_status", "reviewer_notes",
    ]
    write_csv(report_dir / "top_20_prompt_candidates.csv", candidates, candidate_columns)
    evidence_rows = [
        {**{key: item[key] for key in ["signal_group", "source", "theme", "text", "frequency"]},
         "metadata": json.dumps(item.get("metadata") or {}, ensure_ascii=False, sort_keys=True)}
        for item in signals
    ]
    write_csv(report_dir / "prompt_research_evidence.csv", evidence_rows,
              ["signal_group", "source", "theme", "text", "frequency", "metadata"])
    summary = {
        "month": month,
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "benchmark_prompt_count": prompt_count,
        "candidate_count": len(candidates),
        "signal_count": len(signals),
        "signal_counts": dict(Counter(item["signal_group"] for item in signals)),
        "source_counts": dict(Counter(item["source"] for item in signals)),
        "usage_this_invocation": usage,
        "warnings": warnings,
        "seed_file": str(seed_path),
        "internal_signals_file": str(internal_path),
        "policy": {
            "minimum_signal_groups": 2,
            "priority_formula": "50% cross-source support + 30% buyer intent + 20% coverage gap",
            "relevance": "Human-controlled pass/fail scope gate; not a numeric score.",
            "publication": "Review-only. This command never modifies prompts.json.",
        },
    }
    write_json(report_dir / "prompt_research_summary.json", summary)
    lines = [
        f"# Monthly Prompt Research - {month}", "",
        f"Benchmark prompts reviewed for coverage: {prompt_count}",
        f"Signals processed: {len(signals)}", f"Candidates proposed: {len(candidates)}", "",
        "Candidates require human review. This report does not modify the approved benchmark prompt set.", "",
        "| Rank | Candidate prompt | Theme | Signal groups | Buyer intent | Coverage | Priority |",
        "| ---: | --- | --- | --- | --- | --- | ---: |",
    ]
    for row in candidates:
        safe_prompt = row["candidate_prompt"].replace("|", "\\|")
        lines.append(
            f"| {row['rank']} | {safe_prompt} | {row['theme']} | {row['signal_groups_matched']} | "
            f"{row['buyer_intent']} | {row['coverage_gap']} | {row['priority_score']} |"
        )
    if warnings:
        lines.extend(["", "## Warnings", "", *[f"- {warning}" for warning in warnings]])
    (report_dir / "prompt-research.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, Any]], columns: list[str]) -> None:
    ensure_dir(path.parent)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
