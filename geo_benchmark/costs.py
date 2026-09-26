from __future__ import annotations

from collections import defaultdict
from typing import Any

from .io_utils import estimate_tokens
from .providers import SYSTEM_PROMPT


WEB_SEARCH_OPTIONAL_PROVIDERS = {"openai", "anthropic", "gemini"}


def estimate_planned_cost(
    prompts: list[dict[str, Any]],
    providers: list[str],
    runs: int,
    models_config: dict[str, Any],
    pricing_config: dict[str, Any],
    assumed_output_tokens: int | None,
    web_search_mode: str = "off",
    previous_cost_summary: dict[str, Any] | None = None,
) -> dict[str, Any]:
    rows = []
    total = 0.0
    pricing_complete = True
    observed = observed_provider_averages(previous_cost_summary or {})
    for provider_name in providers:
        provider_config = models_config[provider_name]
        model_name = provider_config["model"]
        price = price_for_model(pricing_config, model_name, provider_name)
        known = all(key in price for key in ("input_per_1m", "output_per_1m"))
        pricing_complete = pricing_complete and known
        input_rate = float(price.get("input_per_1m", 0.0))
        output_rate = float(price.get("output_per_1m", 0.0))
        request_fee = float(price.get("request_fee", 0.0))
        web_search_fee = (
            float(price.get("web_search_fee", 0.0))
            if provider_name in WEB_SEARCH_OPTIONAL_PROVIDERS
            else 0.0
        )
        history = observed.get(provider_name)
        if assumed_output_tokens is not None:
            output_tokens_per_answer = float(assumed_output_tokens)
            output_assumption_source = "command-line override"
        elif history:
            output_tokens_per_answer = history["output_tokens_per_answer"]
            output_assumption_source = "previous cost_summary.json"
        else:
            output_tokens_per_answer = float(
                provider_config.get("assumed_output_tokens", provider_config.get("max_output_tokens", 700))
            )
            output_assumption_source = "models config"
        if history:
            searches_per_answer = history["searches_per_answer"]
            search_assumption_source = "previous cost_summary.json"
        else:
            searches_per_answer = float(provider_config.get("searches_per_answer", 1.0))
            search_assumption_source = "models config"

        input_tokens = 0
        request_count = len(prompts) * runs
        web_search_requests = (
            request_count * searches_per_answer
            if web_search_mode == "on" and provider_name in WEB_SEARCH_OPTIONAL_PROVIDERS
            else 0.0
        )
        for prompt in prompts:
            prompt_text = f"{SYSTEM_PROMPT}\n{prompt.get('prompt_text', '')}"
            input_tokens += estimate_tokens(prompt_text) * runs
        output_tokens = round(request_count * output_tokens_per_answer)
        input_cost = input_tokens / 1_000_000 * input_rate
        output_cost = output_tokens / 1_000_000 * output_rate
        request_cost = request_count * request_fee
        web_search_cost = web_search_requests * web_search_fee
        token_cost = input_cost + output_cost
        cost = token_cost + request_cost + web_search_cost
        total += cost
        rows.append(
            {
                "provider": provider_name,
                "model": model_name,
                "requests": request_count,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "assumed_output_tokens_per_answer": round(output_tokens_per_answer, 4),
                "assumed_output_tokens_source": output_assumption_source,
                "input_rate_per_1m": input_rate,
                "output_rate_per_1m": output_rate,
                "request_fee": request_fee,
                "web_search_mode": (
                    web_search_mode if provider_name in WEB_SEARCH_OPTIONAL_PROVIDERS else "off"
                ),
                "web_search_requests": web_search_requests,
                "searches_per_answer": round(searches_per_answer, 4),
                "searches_per_answer_source": search_assumption_source,
                "web_search_fee": web_search_fee,
                "input_cost_usd": round(input_cost, 4),
                "output_cost_usd": round(output_cost, 4),
                "token_cost_usd": round(token_cost, 4),
                "request_cost_usd": round(request_cost, 4),
                "web_search_cost_usd": round(web_search_cost, 4),
                "estimated_cost_usd": round(cost, 4) if known else None,
                "pricing_known": known,
                "pricing_source": price.get("source"),
            }
        )
    return {
        "mode": "planned",
        "runs_per_prompt": runs,
        "prompt_count": len(prompts),
        "assumed_output_tokens": assumed_output_tokens,
        "web_search_mode": web_search_mode,
        "total_estimated_cost_usd": round(total, 4) if pricing_complete else None,
        "pricing_complete": pricing_complete,
        "scope": "Selected prompts and providers, assuming fresh collection; excludes fact judging, retries and fallback. Not an incremental bill for rerunning cached answers.",
        "assumptions": "Input tokens are approximated from prompt text. Output tokens and searches per answer use previous saved usage when available, otherwise provider config; explicit output-token overrides take precedence.",
        "providers": rows,
        "pricing_version": pricing_config.get("pricing_version"),
    }


def observed_provider_averages(cost_summary: dict[str, Any]) -> dict[str, dict[str, float]]:
    """Calculate per-provider averages from a saved actual-cost summary."""
    totals: dict[str, dict[str, float]] = defaultdict(
        lambda: {"requests": 0.0, "output_tokens": 0.0, "web_search_requests": 0.0}
    )
    for row in cost_summary.get("providers", []):
        provider = str(row.get("provider") or "")
        requests = float(row.get("requests") or 0)
        if not provider or requests <= 0:
            continue
        totals[provider]["requests"] += requests
        totals[provider]["output_tokens"] += float(row.get("output_tokens") or 0)
        totals[provider]["web_search_requests"] += float(row.get("web_search_requests") or 0)
    return {
        provider: {
            "output_tokens_per_answer": values["output_tokens"] / values["requests"],
            "searches_per_answer": values["web_search_requests"] / values["requests"],
        }
        for provider, values in totals.items()
        if values["requests"] > 0
    }


def estimate_actual_cost(
    raw_answers: list[dict[str, Any]],
    pricing_config: dict[str, Any],
) -> dict[str, Any]:
    grouped: dict[tuple[str, str], dict[str, Any]] = defaultdict(
        lambda: {"requests": 0, "input_tokens": 0, "output_tokens": 0, "web_search_requests": 0}
    )
    for row in raw_answers:
        # A provider bills a token-limited response even though it is excluded
        # from scoring and must be retried.
        if row.get("status") not in {"ok", "incomplete"}:
            continue
        key = (row["model_surface"], row.get("model_name") or "")
        grouped[key]["requests"] += 1
        grouped[key]["input_tokens"] += int(row.get("input_tokens", 0))
        grouped[key]["output_tokens"] += int(row.get("output_tokens", 0))
        grouped[key]["web_search_requests"] += int(row.get("web_search_requests", 0))

    rows = []
    total = 0.0
    pricing_complete = True
    for (provider, model), usage in sorted(grouped.items()):
        price = price_for_model(pricing_config, model, provider)
        known = all(key in price for key in ("input_per_1m", "output_per_1m"))
        pricing_complete = pricing_complete and known
        input_rate = float(price.get("input_per_1m", 0.0))
        output_rate = float(price.get("output_per_1m", 0.0))
        request_fee = float(price.get("request_fee", 0.0))
        web_search_fee = float(price.get("web_search_fee", 0.0))
        input_cost = usage["input_tokens"] / 1_000_000 * input_rate
        output_cost = usage["output_tokens"] / 1_000_000 * output_rate
        request_cost = usage["requests"] * request_fee
        web_search_cost = usage["web_search_requests"] * web_search_fee
        token_cost = input_cost + output_cost
        cost = token_cost + request_cost + web_search_cost
        total += cost
        rows.append(
            {
                "provider": provider,
                "model": model,
                **usage,
                "input_cost_usd": round(input_cost, 4),
                "output_cost_usd": round(output_cost, 4),
                "token_cost_usd": round(token_cost, 4),
                "request_cost_usd": round(request_cost, 4),
                "web_search_cost_usd": round(web_search_cost, 4),
                "estimated_cost_usd": round(cost, 4) if known else None,
                "pricing_known": known,
                "pricing_source": price.get("source"),
            }
        )
    return {
        "mode": "actual_or_usage_estimated",
        "total_estimated_cost_usd": round(total, 4) if pricing_complete else None,
        "pricing_complete": pricing_complete,
        "scope": "Usage estimate for successful saved answers in this report's search mode. Not a billing ledger; excludes failed or overwritten attempts and may include answers collected previously.",
        "providers": rows,
        "pricing_version": pricing_config.get("pricing_version"),
    }


def price_for_model(pricing_config: dict[str, Any], model: str, provider: str) -> dict[str, Any]:
    prices = pricing_config.get("models", {})
    if model in prices:
        return prices[model]
    matching = [key for key in prices if model.startswith(f"{key}-")]
    if matching:
        return prices[max(matching, key=len)]
    return prices.get(provider, {})
