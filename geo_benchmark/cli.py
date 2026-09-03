from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import sys
import uuid
from pathlib import Path
from typing import Any

from .costs import estimate_actual_cost, estimate_planned_cost
from .defaults import DEFAULT_FACTS, DEFAULT_MODELS, DEFAULT_PRICING, DEFAULT_SOURCE_AUTHORITY, DEFAULT_TARGETS
from .io_utils import ensure_dir, previous_month, read_json, read_jsonl, stable_hash, write_json, write_jsonl
from .providers import ProviderError, provider_for, run_with_retries
from .reports import write_reports
from .scoring import aggregate_scores, score_answers
from .seed import generate_seed_prompts


def main(argv: list[str] | None = None) -> int:
    load_env_files([Path.cwd(), Path(__file__).resolve().parent.parent])
    parser = argparse.ArgumentParser(prog="geo-bench", description="Run a GEO benchmark suite.")
    parser.add_argument("--data-dir", default="geo-benchmark", help="Benchmark data directory.")
    sub = parser.add_subparsers(dest="command", required=True)

    prepare_p = sub.add_parser("prepare", help="Prepare config and prompt set.")
    prepare_p.add_argument("--month", required=True)
    prepare_p.add_argument("--prompts", type=int, default=120)
    prepare_p.add_argument("--update-ratio", type=float, default=0.3)
    prepare_p.add_argument("--force", action="store_true")

    run_p = sub.add_parser("run", help="One-command prepare, collect, score, report.")
    run_p.add_argument("--month", required=True)
    run_p.add_argument("--providers", default="mock")
    run_p.add_argument("--targets", default=None)
    run_p.add_argument("--runs", type=int, default=1)
    run_p.add_argument("--prompts", type=int, default=120)
    run_p.add_argument("--update-ratio", type=float, default=0.3)
    run_p.add_argument("--assumed-output-tokens", type=int, default=700)
    run_p.add_argument("--retries", type=int, default=1)
    run_p.add_argument("--web-search", choices=["off", "on"], default="off", help="Enable provider web search in low mode where supported.")
    run_p.add_argument("--force", action="store_true", help="Overwrite raw/scored/report outputs for the month.")
    run_p.add_argument("--no-fallback", action="store_true", help="Do not auto-retry failed answers with configured fallback models.")
    run_p.add_argument("--only-prompt-type", default=None, help="Only collect prompts of this prompt_type, preserving other raw answers.")
    run_p.add_argument("--only-prompt-ids", default=None, help="Comma-separated prompt_ids to collect, preserving other raw answers.")

    retry_p = sub.add_parser("retry-errors", help="Retry failed raw answers without rerunning successes.")
    retry_p.add_argument("--month", required=True)
    retry_p.add_argument("--provider", required=True)
    retry_p.add_argument("--model", default=None, help="Optional model override for the retry.")
    retry_p.add_argument("--max-output-tokens", type=int, default=None)
    retry_p.add_argument("--retries", type=int, default=1)
    retry_p.add_argument("--targets", default=None)
    retry_p.add_argument("--web-search", choices=["off", "on"], default="off")

    estimate_p = sub.add_parser("estimate-cost", help="Estimate planned cost without calling providers.")
    estimate_p.add_argument("--month", required=True)
    estimate_p.add_argument("--providers", default="openai,anthropic,gemini,perplexity")
    estimate_p.add_argument("--runs", type=int, default=3)
    estimate_p.add_argument("--prompts", type=int, default=120)
    estimate_p.add_argument("--assumed-output-tokens", type=int, default=700)
    estimate_p.add_argument("--web-search", choices=["off", "on"], default="off")

    score_p = sub.add_parser("score", help="Score existing raw answers.")
    score_p.add_argument("--month", required=True)
    score_p.add_argument("--targets", default=None)
    score_p.add_argument("--web-search", choices=["off", "on"], default="off")

    report_p = sub.add_parser("report", help="Generate reports from scored answers.")
    report_p.add_argument("--month", required=True)

    compare_p = sub.add_parser("compare", help="Compare two monthly KPI summaries.")
    compare_p.add_argument("--from", "--from-month", dest="from_month", required=True)
    compare_p.add_argument("--to", "--to-month", dest="to_month", required=True)

    audit_p = sub.add_parser("audit-prompts", help="Audit prompt objectivity and brand mentions.")
    audit_p.add_argument("--month", required=True)

    validate_p = sub.add_parser("validate-prompts", help="Validate prompts and fail on benchmark policy violations.")
    validate_p.add_argument("--month", required=True)

    env_p = sub.add_parser("check-env", help="Check configured provider API keys without printing secrets.")
    env_p.add_argument("--providers", default="openai,anthropic,gemini,perplexity")

    args = parser.parse_args(argv)
    root = Path(args.data_dir)

    if args.command == "prepare":
        prepare(root, args.month, args.prompts, args.update_ratio, args.force)
        return 0
    if args.command == "run":
        prepare(root, args.month, args.prompts, args.update_ratio, force=False)
        validate_prompts_or_exit(root, args.month)
        providers = split_csv(args.providers)
        prompt_ids = selected_prompt_ids(root, args.month, args.only_prompt_type, args.only_prompt_ids)
        collect(root, args.month, providers, args.runs, args.retries, args.force, prompt_ids, args.web_search)
        if not args.no_fallback:
            for result in retry_configured_errors(root, args.month, providers, args.retries, args.web_search):
                if result["attempted"]:
                    print(
                        f"Auto fallback for {result['provider']} with {result['model']}: "
                        f"{result['succeeded']}/{result['attempted']} recovered, "
                        f"{result['failed']} still failed."
                    )
        scored, summary, cost = score_and_report(root, args.month, split_csv(args.targets) if args.targets else None, args.web_search)
        planned = planned_cost(root, args.month, providers, args.runs, args.assumed_output_tokens, args.web_search)
        write_json(month_report_dir(root, args.month) / "planned_cost_summary.json", planned)
        print_run_summary(root, args.month, summary, cost, planned, len(scored))
        return 0
    if args.command == "retry-errors":
        result = retry_errors(
            root,
            args.month,
            args.provider,
            args.model,
            args.max_output_tokens,
            args.retries,
            args.web_search,
        )
        scored, summary, cost = score_and_report(root, args.month, split_csv(args.targets) if args.targets else None, args.web_search)
        print(
            f"Retried {result['attempted']} failed answers for {args.provider}: "
            f"{result['succeeded']} succeeded, {result['failed']} still failed."
        )
        if result["backup_path"]:
            print(f"Backup: {result['backup_path']}")
        print(f"Scored answers: {len(scored)}")
        print(f"Cost estimate: ${cost.get('total_estimated_cost_usd', 0)}")
        print(f"Report: {month_report_dir(root, args.month) / 'llm-report.md'}")
        return 0
    if args.command == "estimate-cost":
        prepare(root, args.month, args.prompts, 0.3, force=False)
        estimate = planned_cost(root, args.month, split_csv(args.providers), args.runs, args.assumed_output_tokens, args.web_search)
        write_json(month_report_dir(root, args.month) / "planned_cost_summary.json", estimate)
        print_cost_estimate(estimate)
        return 0
    if args.command == "score":
        scored, summary, cost = score_and_report(root, args.month, split_csv(args.targets) if args.targets else None, args.web_search)
        print(f"Scored {len(scored)} answers. Overall Answer Share: {summary['overall']['answer_share']}")
        print(f"Cost estimate: ${cost.get('total_estimated_cost_usd', 0)}")
        return 0
    if args.command == "report":
        scored_path = month_run_dir(root, args.month) / "scored_answers.jsonl"
        scored = read_jsonl(scored_path)
        summary = aggregate_scores(scored)
        cost_path = month_report_dir(root, args.month) / "cost_summary.json"
        cost = read_json(cost_path, default={})
        write_reports(month_report_dir(root, args.month), args.month, summary, scored, cost)
        print(f"Wrote reports to {month_report_dir(root, args.month)}")
        return 0
    if args.command == "compare":
        compare(root, args.from_month, args.to_month)
        return 0
    if args.command == "audit-prompts":
        audit_prompts(root, args.month)
        return 0
    if args.command == "validate-prompts":
        validate_prompts_or_exit(root, args.month)
        return 0
    if args.command == "check-env":
        check_env(root, split_csv(args.providers))
        return 0
    return 1


ENV_LINE_RE = re.compile(r"^(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)=(.*)$")


def load_env_files(base_dirs: list[Path]) -> None:
    seen: set[Path] = set()
    for base_dir in base_dirs:
        for name in [".env", ".env.local"]:
            path = (base_dir / name).resolve()
            if path in seen:
                continue
            seen.add(path)
            if path.exists():
                load_env_file(path)


def load_env_file(path: Path) -> None:
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        match = ENV_LINE_RE.match(line)
        if not match:
            continue
        key, raw_value = match.groups()
        if os.getenv(key):
            continue
        os.environ[key] = clean_env_value(raw_value)


def clean_env_value(raw_value: str) -> str:
    value = raw_value.strip()
    if value and value[0] in {"'", '"'}:
        quote = value[0]
        if len(value) >= 2 and value[-1] == quote:
            return value[1:-1]
        return value[1:]
    if " #" in value:
        value = value.split(" #", 1)[0].rstrip()
    return value


def prepare(root: Path, month: str, prompt_count: int, update_ratio: float, force: bool) -> None:
    ensure_dir(root)
    config_dir = root / "config"
    ensure_default(config_dir / "models.json", DEFAULT_MODELS)
    ensure_default(config_dir / "pricing.json", DEFAULT_PRICING)
    ensure_default(config_dir / "source_authority.json", DEFAULT_SOURCE_AUTHORITY)
    ensure_default(config_dir / "facts.json", DEFAULT_FACTS)
    ensure_default(config_dir / "targets.json", DEFAULT_TARGETS)

    prompt_dir = prompt_source_root(root) / "prompts" / month
    prompts_path = prompt_dir / "prompts.json"
    if prompts_path.exists() and not force:
        return
    prompts = generate_prompts_with_previous_stable(root, month, prompt_count, update_ratio)
    prompt_hash = stable_hash(prompts)
    write_json(prompts_path, prompts)
    (prompt_dir / "prompt_set_hash.txt").write_text(prompt_hash + "\n", encoding="utf-8")


def generate_prompts_with_previous_stable(
    root: Path,
    month: str,
    prompt_count: int,
    update_ratio: float,
) -> list[dict[str, Any]]:
    prompt_root = prompt_source_root(root)
    stable_count = round(prompt_count * (1 - update_ratio))
    generated = generate_seed_prompts(month, total=prompt_count, update_ratio=update_ratio)
    previous_path = prompt_root / "prompts" / previous_month(month) / "prompts.json"
    if not previous_path.exists():
        return generated

    previous = read_json(previous_path)
    if len(previous) != prompt_count:
        return generated
    previous_types = {prompt.get("prompt_type") for prompt in previous}
    generated_types = {prompt.get("prompt_type") for prompt in generated}
    if previous_types != generated_types:
        return generated
    stable = [prompt for prompt in previous if prompt.get("panel") == "stable"][:stable_count]
    if len(stable) < stable_count:
        stable = [prompt for prompt in generated if prompt.get("panel") == "stable"][:stable_count]
    dynamic = [prompt for prompt in generated if prompt.get("panel") == "dynamic"]
    return stable + dynamic[: prompt_count - len(stable)]


def ensure_default(path: Path, data: dict[str, Any]) -> None:
    if not path.exists():
        write_json(path, data)


def collect(
    root: Path,
    month: str,
    provider_names: list[str],
    runs: int,
    retries: int,
    force: bool,
    prompt_ids: set[str] | None = None,
    web_search_mode: str = "off",
) -> None:
    prompts = load_prompts(root, month)
    if prompt_ids is not None:
        prompts = [prompt for prompt in prompts if prompt["prompt_id"] in prompt_ids]
    models = read_json(root / "config" / "models.json")
    run_dir = month_run_dir(root, month)
    raw_path = run_dir / "raw_answers.jsonl"
    if force and raw_path.exists():
        retained = [
            row
            for row in read_jsonl(raw_path)
            if not (
                row.get("model_surface") in provider_names
                and raw_web_search_mode(row) == web_search_mode
                and (prompt_ids is None or row.get("prompt_id") in prompt_ids)
            )
        ]
        write_jsonl(raw_path, retained)
    existing_ids = {row.get("answer_id") for row in read_jsonl(raw_path)}
    rows: list[dict[str, Any]] = []

    for provider_name in provider_names:
        if provider_name not in models:
            raise SystemExit(f"Unknown provider '{provider_name}' in models.json")
        provider_config = with_web_search_mode(models[provider_name], web_search_mode)
        provider = provider_for(provider_name, provider_config)
        for prompt in prompts:
            for run_index in range(1, runs + 1):
                answer_id = stable_hash([month, prompt["prompt_id"], provider_name, run_index, web_search_mode])[:24]
                if answer_id in existing_ids:
                    continue
                run_id = str(uuid.uuid4())
                timestamp = dt.datetime.now(dt.timezone.utc).isoformat()
                try:
                    result = run_with_retries(provider, prompt, run_index, retries)
                    row = {
                        "answer_id": answer_id,
                        "run_id": run_id,
                        "status": "ok",
                        "month": month,
                        "prompt_id": prompt["prompt_id"],
                        "prompt_text": prompt["prompt_text"],
                        "model_surface": provider_name,
                        "model_name": result.model_name,
                        "model_version": result.model_version,
                        "web_search_mode": web_search_mode,
                        "web_search_requests": result.web_search_requests,
                        "fan_out_queries": result.fan_out_queries or [],
                        "fan_out_status": result.fan_out_status,
                        "run_index": run_index,
                        "timestamp": timestamp,
                        "raw_answer": result.answer,
                        "raw_citations": result.citations,
                        "input_tokens": result.input_tokens,
                        "output_tokens": result.output_tokens,
                        "raw_answer_hash": stable_hash(result.answer),
                    }
                except ProviderError as exc:
                    row = {
                        "answer_id": answer_id,
                        "run_id": run_id,
                        "status": "error",
                        "month": month,
                        "prompt_id": prompt["prompt_id"],
                        "prompt_text": prompt["prompt_text"],
                        "model_surface": provider_name,
                        "model_name": provider_config.get("model"),
                        "web_search_mode": web_search_mode,
                        "web_search_requests": 0,
                        "fan_out_queries": [],
                        "fan_out_status": "request_failed",
                        "run_index": run_index,
                        "timestamp": timestamp,
                        "error": str(exc),
                        "retryable": exc.retryable,
                    }
                rows.append(row)
                if len(rows) >= 1:
                    write_jsonl_append(raw_path, rows)
                    rows = []
    if rows:
        write_jsonl_append(raw_path, rows)


def write_jsonl_append(path: Path, rows: list[dict[str, Any]]) -> None:
    from .io_utils import append_jsonl

    append_jsonl(path, rows)


def selected_prompt_ids(
    root: Path,
    month: str,
    prompt_type: str | None,
    prompt_ids_csv: str | None,
) -> set[str] | None:
    if not prompt_type and not prompt_ids_csv:
        return None
    prompts = load_prompts(root, month)
    selected: set[str] = set()
    if prompt_type:
        selected.update(prompt["prompt_id"] for prompt in prompts if prompt.get("prompt_type") == prompt_type)
    if prompt_ids_csv:
        selected.update(split_csv(prompt_ids_csv))
    if not selected:
        raise SystemExit("No prompts matched the requested filter.")
    return selected


def retry_errors(
    root: Path,
    month: str,
    provider_name: str,
    model_override: str | None,
    max_output_tokens: int | None,
    retries: int,
    web_search_mode: str = "off",
    eligible_only: bool = False,
) -> dict[str, Any]:
    prompts = load_prompts(root, month)
    prompt_by_id = {prompt["prompt_id"]: prompt for prompt in prompts}
    models = read_json(root / "config" / "models.json")
    if provider_name not in models:
        raise SystemExit(f"Unknown provider '{provider_name}' in models.json")

    run_dir = month_run_dir(root, month)
    raw_path = run_dir / "raw_answers.jsonl"
    raw = read_jsonl(raw_path)
    error_indices = [
        index
        for index, row in enumerate(raw)
        if row.get("model_surface") == provider_name and row.get("status") != "ok"
        and raw_web_search_mode(row) == web_search_mode
        and (not eligible_only or fallback_error_is_eligible(row))
    ]
    if not error_indices:
        return {"attempted": 0, "succeeded": 0, "failed": 0, "backup_path": None}

    timestamp_slug = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup_path = run_dir / f"raw_answers.before-retry-{timestamp_slug}.jsonl"
    ensure_dir(backup_path.parent)
    backup_path.write_bytes(raw_path.read_bytes())

    config = dict(models[provider_name])
    if model_override:
        config["model"] = model_override
    if max_output_tokens is not None:
        config["max_output_tokens"] = max_output_tokens
    config = with_web_search_mode(config, web_search_mode)
    provider = provider_for(provider_name, config)

    succeeded = 0
    failed = 0
    for index in error_indices:
        old = raw[index]
        prompt = prompt_by_id.get(old["prompt_id"])
        if not prompt:
            failed += 1
            continue
        run_index = int(old.get("run_index", 1))
        run_id = str(uuid.uuid4())
        timestamp = dt.datetime.now(dt.timezone.utc).isoformat()
        try:
            result = run_with_retries(provider, prompt, run_index, retries)
            raw[index] = {
                "answer_id": old["answer_id"],
                "run_id": run_id,
                "status": "ok",
                "month": month,
                "prompt_id": prompt["prompt_id"],
                "prompt_text": prompt["prompt_text"],
                "model_surface": provider_name,
                "model_name": result.model_name,
                "model_version": result.model_version,
                "web_search_mode": web_search_mode,
                "web_search_requests": result.web_search_requests,
                "fan_out_queries": result.fan_out_queries or [],
                "fan_out_status": result.fan_out_status,
                "run_index": run_index,
                "timestamp": timestamp,
                "raw_answer": result.answer,
                "raw_citations": result.citations,
                "input_tokens": result.input_tokens,
                "output_tokens": result.output_tokens,
                "raw_answer_hash": stable_hash(result.answer),
                "retry_of_run_id": old.get("run_id"),
                "retry_error": old.get("error"),
                "retry_model_override": model_override,
            }
            succeeded += 1
        except ProviderError as exc:
            raw[index] = {
                **old,
                "run_id": run_id,
                "timestamp": timestamp,
                "model_name": config.get("model"),
                "web_search_mode": web_search_mode,
                "web_search_requests": 0,
                "fan_out_queries": [],
                "fan_out_status": "request_failed",
                "error": str(exc),
                "retryable": exc.retryable,
                "retry_of_run_id": old.get("run_id"),
                "retry_error": old.get("error"),
                "retry_model_override": model_override,
            }
            failed += 1
        write_jsonl(raw_path, raw)
        print(f"retry-errors progress: {succeeded + failed}/{len(error_indices)}")

    return {
        "attempted": len(error_indices),
        "succeeded": succeeded,
        "failed": failed,
        "backup_path": str(backup_path),
    }


def retry_configured_errors(
    root: Path,
    month: str,
    provider_names: list[str],
    retries: int,
    web_search_mode: str = "off",
) -> list[dict[str, Any]]:
    models = read_json(root / "config" / "models.json")
    results: list[dict[str, Any]] = []
    for provider_name in provider_names:
        config = models.get(provider_name, {})
        fallback_model = config.get("fallback_model")
        if not fallback_model:
            continue
        fallback_max_output_tokens = config.get("fallback_max_output_tokens")
        fallback_retries = int(config.get("fallback_retries", retries))
        result = retry_errors(
            root,
            month,
            provider_name,
            fallback_model,
            fallback_max_output_tokens,
            fallback_retries,
            web_search_mode,
            eligible_only=True,
        )
        result["provider"] = provider_name
        result["model"] = fallback_model
        results.append(result)
    return results


def fallback_error_is_eligible(row: dict[str, Any]) -> bool:
    error = str(row.get("error", "")).lower()
    blocked_terms = [
        "missing ",
        "invalid_api_key",
        "insufficient_quota",
        "unauthorized",
        "forbidden",
        "billing",
    ]
    return not any(term in error for term in blocked_terms)


def score_and_report(
    root: Path,
    month: str,
    targets: list[str] | None = None,
    web_search_mode: str = "off",
) -> tuple[list[dict[str, Any]], dict[str, Any], dict[str, Any]]:
    prompts = load_prompts(root, month)
    raw = [
        row
        for row in read_jsonl(month_run_dir(root, month) / "raw_answers.jsonl")
        if raw_web_search_mode(row) == web_search_mode
    ]
    source_authority = read_json(root / "config" / "source_authority.json")
    facts = read_json(root / "config" / "facts.json")
    pricing = read_json(root / "config" / "pricing.json")
    targets = targets or read_json(root / "config" / "targets.json", default=DEFAULT_TARGETS)["targets"]
    scored = score_answers(raw, prompts, source_authority, facts, targets)
    summary = aggregate_scores(scored)
    cost = estimate_actual_cost(raw, pricing)
    cost["web_search_mode"] = web_search_mode
    run_dir = month_run_dir(root, month)
    write_jsonl(run_dir / "scored_answers.jsonl", scored)
    write_json(month_report_dir(root, month) / "cost_summary.json", cost)
    write_reports(month_report_dir(root, month), month, summary, scored, cost)
    return scored, summary, cost


def planned_cost(
    root: Path,
    month: str,
    providers: list[str],
    runs: int,
    assumed_output_tokens: int,
    web_search_mode: str = "off",
) -> dict[str, Any]:
    prompts = load_prompts(root, month)
    models = read_json(root / "config" / "models.json")
    pricing = read_json(root / "config" / "pricing.json")
    return estimate_planned_cost(prompts, providers, runs, models, pricing, assumed_output_tokens, web_search_mode)


def load_prompts(root: Path, month: str) -> list[dict[str, Any]]:
    return read_json(prompt_source_root(root) / "prompts" / month / "prompts.json")


def prompt_source_root(root: Path) -> Path:
    """Return the canonical prompt root for a benchmark data directory."""
    if root.name.startswith("geo-benchmark-"):
        return root.parent / "geo-benchmark"
    return root


def month_run_dir(root: Path, month: str) -> Path:
    return root / "runs" / month


def month_report_dir(root: Path, month: str) -> Path:
    return root / "reports" / month


def split_csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def with_web_search_mode(config: dict[str, Any], web_search_mode: str) -> dict[str, Any]:
    updated = dict(config)
    if updated.get("provider") in {"openai", "anthropic", "gemini"}:
        updated["web_search"] = web_search_mode
    return updated


def raw_web_search_mode(row: dict[str, Any]) -> str:
    return str(row.get("web_search_mode") or "off")


def print_run_summary(
    root: Path,
    month: str,
    summary: dict[str, Any],
    cost: dict[str, Any],
    planned: dict[str, Any],
    scored_count: int,
) -> None:
    report_dir = month_report_dir(root, month)
    print(f"GEO benchmark complete for {month}")
    print(f"Scored answers: {scored_count}")
    for target in summary.get("target_order", []):
        metrics = summary["targets"][target]
        print(
            f"{target}: Overall Answer Share {metrics['overall']['answer_share']}, "
            f"Unchanged {metrics['unchanged']['answer_share']}, "
            f"Citation Authority {metrics['overall']['citation_authority']}, "
            f"Recommendation Rate {metrics['overall']['qualified_recommendation_rate']}"
        )
    print(f"Actual/usage-estimated cost: ${cost.get('total_estimated_cost_usd', 0)}")
    print(f"Planned cost estimate: ${planned.get('total_estimated_cost_usd', 0)}")
    print(f"Report: {report_dir / 'llm-report.md'}")


def print_cost_estimate(estimate: dict[str, Any]) -> None:
    print(f"Total estimated cost: ${estimate['total_estimated_cost_usd']}")
    for row in estimate["providers"]:
        print(
            f"- {row['provider']} / {row['model']}: "
            f"{row['requests']} requests, "
            f"{row['input_tokens']} input tokens, "
            f"{row['output_tokens']} output tokens, "
            f"${row['estimated_cost_usd']}"
        )


def compare(root: Path, from_month: str, to_month: str) -> None:
    from_path = month_report_dir(root, from_month) / "kpi_summary.json"
    to_path = month_report_dir(root, to_month) / "kpi_summary.json"
    if not from_path.exists() or not to_path.exists():
        missing = [str(path) for path in [from_path, to_path] if not path.exists()]
        raise SystemExit("Missing monthly report. Run `geo-bench run` first for: " + ", ".join(missing))
    from_summary = read_json(from_path)
    to_summary = read_json(to_path)
    metrics = [
        ("Answer Share", "answer_share"),
        ("Citation Authority", "citation_authority"),
        ("Recommendation Rate", "qualified_recommendation_rate"),
    ]
    print(f"Compare {from_month} -> {to_month}")
    print("Target | Metric | Overall delta | Unchanged delta")
    print("--- | --- | ---: | ---:")
    targets = sorted(set(from_summary.get("targets", {})) & set(to_summary.get("targets", {})))
    if not targets:
        targets = ["TiDB"]
    for target in targets:
        from_metrics = from_summary.get("targets", {}).get(target, from_summary)
        to_metrics = to_summary.get("targets", {}).get(target, to_summary)
        for label, key in metrics:
            overall_delta = to_metrics["overall"][key] - from_metrics["overall"][key]
            unchanged_delta = to_metrics["unchanged"][key] - from_metrics["unchanged"][key]
            print(f"{target} | {label} | {overall_delta:+.2f} | {unchanged_delta:+.2f}")


def audit_prompts(root: Path, month: str) -> None:
    prompts = load_prompts(root, month)
    terms = [
        "tidb",
        "cockroachdb",
        "cockroach",
        "yugabytedb",
        "yugabyte",
        "supabase",
        "planetscale",
        "neon",
        "aurora",
        "spanner",
        "alloydb",
        "mysql",
        "postgres",
    ]
    print(f"Prompt audit for {month}")
    print(f"Total prompts: {len(prompts)}")
    for term in terms:
        count = sum(term in prompt["prompt_text"].lower() for prompt in prompts)
        print(f"- {term}: {count}")
    by_type: dict[str, int] = {}
    by_panel: dict[str, int] = {}
    by_validation_status: dict[str, int] = {}
    for prompt in prompts:
        by_type[prompt["prompt_type"]] = by_type.get(prompt["prompt_type"], 0) + 1
        by_panel[prompt["panel"]] = by_panel.get(prompt["panel"], 0) + 1
        status = prompt.get("source", {}).get("validation_status", "unknown")
        by_validation_status[status] = by_validation_status.get(status, 0) + 1
    print(f"By type: {by_type}")
    print(f"By panel: {by_panel}")
    print(f"By validation status: {by_validation_status}")


MEASURED_PRODUCT_PROMPT_TERMS = [
    "tidb",
    "cockroachdb",
    "cockroach",
    "yugabytedb",
    "yugabyte",
    "supabase",
    "planetscale",
    "neon",
    "aurora",
    "spanner",
    "alloydb",
]

SERVERLESS_AI_BANNED_TERMS = [
    "postgres",
    "postgresql",
    "pgvector",
]


def validate_prompts_or_exit(root: Path, month: str) -> None:
    errors = prompt_validation_errors(load_prompts(root, month))
    if errors:
        print(f"Prompt validation failed for {month}: {len(errors)} issue(s)")
        for error in errors[:50]:
            print(f"- {error}")
        if len(errors) > 50:
            print(f"- ... {len(errors) - 50} more issue(s)")
        raise SystemExit(1)
    print(f"Prompt validation passed for {month}.")


def prompt_validation_errors(prompts: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    seen_texts: dict[str, str] = {}
    seen_ids: set[str] = set()
    for index, prompt in enumerate(prompts, start=1):
        prompt_id = str(prompt.get("prompt_id", f"row_{index}"))
        prompt_text = str(prompt.get("prompt_text", ""))
        lower_text = prompt_text.lower()

        if prompt_id in seen_ids:
            errors.append(f"{prompt_id}: duplicate prompt_id")
        seen_ids.add(prompt_id)

        if lower_text in seen_texts:
            errors.append(f"{prompt_id}: duplicate prompt_text also used by {seen_texts[lower_text]}")
        else:
            seen_texts[lower_text] = prompt_id

        brand_class = str(prompt.get("brand_class", "non_branded")).strip().lower()
        if brand_class not in {"branded", "non_branded"}:
            errors.append(f"{prompt_id}: brand_class must be 'branded' or 'non_branded', got '{brand_class}'")

        # Branded prompts name our products on purpose: they measure whether
        # AI assistants describe TiDB accurately, not whether TiDB is
        # discovered. The ban still applies to non-branded prompts, where a
        # leaked product name would inflate the visibility score.
        if brand_class != "branded":
            for term in MEASURED_PRODUCT_PROMPT_TERMS:
                if contains_term(lower_text, term):
                    errors.append(f"{prompt_id}: prompt_text contains measured product term '{term}'")

        if prompt.get("use_case") == "serverless_ai":
            for term in SERVERLESS_AI_BANNED_TERMS:
                if contains_term(lower_text, term):
                    errors.append(f"{prompt_id}: serverless_ai prompt_text contains banned term '{term}'")

        source = prompt.get("source", {})
        if source.get("validation_status") not in {"case_pattern_validated", "observed_query_validated"}:
            errors.append(f"{prompt_id}: missing approved source.validation_status")
        if not source.get("source_evidence_urls"):
            errors.append(f"{prompt_id}: missing source.source_evidence_urls")
    return errors


def contains_term(text: str, term: str) -> bool:
    return re.search(rf"(?<![a-z0-9]){re.escape(term)}(?![a-z0-9])", text) is not None


def check_env(root: Path, provider_names: list[str]) -> None:
    models = read_json(root / "config" / "models.json", default=DEFAULT_MODELS)
    for provider_name in provider_names:
        if provider_name not in models:
            print(f"{provider_name}: unknown provider")
            continue
        env_var = models[provider_name].get("env_var")
        if not env_var:
            print(f"{provider_name}: no API key required")
            continue
        print(f"{provider_name}: {env_var}={bool(os.getenv(env_var))}")


if __name__ == "__main__":
    sys.exit(main())
