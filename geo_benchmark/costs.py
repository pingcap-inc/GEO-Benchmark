from __future__ import annotations

from collections import defaultdict
from typing import Any

from .io_utils import estimate_tokens
from .providers import SYSTEM_PROMPT


def estimate_planned_cost(
    prompts: list[dict[str, Any]],
    providers: list[str],
    runs: int,
    models_config: dict[str, Any],
    pricing_config: dict[str, Any],
    assumed_output_tokens: int,
) -> dict[str, Any]:
    rows = []
    total = 0.0
    for provider_name in providers:
        model_name = models_config[provider_name]["model"]
        price = pricing_config["models"].get(model_name, {})
        input_rate = float(price.get("input_per_1m", 0.0))
        output_rate = float(price.get("output_per_1m", 0.0))
        request_fee = float(price.get("request_fee", 0.0))
        input_tokens = 0
        output_tokens = 0
        request_count = len(prompts) * runs
        for prompt in prompts:
            prompt_text = f"{SYSTEM_PROMPT}\n{prompt.get('prompt_text', '')}"
            input_tokens += estimate_tokens(prompt_text) * runs
            output_tokens += assumed_output_tokens * runs
        cost = (
            input_tokens / 1_000_000 * input_rate
            + output_tokens / 1_000_000 * output_rate
            + request_count * request_fee
        )
        total += cost
        rows.append(
            {
                "provider": provider_name,
                "model": model_name,
                "requests": request_count,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "input_rate_per_1m": input_rate,
                "output_rate_per_1m": output_rate,
                "request_fee": request_fee,
                "estimated_cost_usd": round(cost, 4),
                "pricing_source": price.get("source"),
            }
        )
    return {
        "mode": "planned",
        "runs_per_prompt": runs,
        "prompt_count": len(prompts),
        "assumed_output_tokens": assumed_output_tokens,
        "total_estimated_cost_usd": round(total, 4),
        "providers": rows,
        "pricing_version": pricing_config.get("pricing_version"),
    }


def estimate_actual_cost(
    raw_answers: list[dict[str, Any]],
    pricing_config: dict[str, Any],
) -> dict[str, Any]:
    grouped: dict[tuple[str, str], dict[str, Any]] = defaultdict(
        lambda: {"requests": 0, "input_tokens": 0, "output_tokens": 0}
    )
    for row in raw_answers:
        if row.get("status") != "ok":
            continue
        key = (row["model_surface"], row.get("model_name") or "")
        grouped[key]["requests"] += 1
        grouped[key]["input_tokens"] += int(row.get("input_tokens", 0))
        grouped[key]["output_tokens"] += int(row.get("output_tokens", 0))

    rows = []
    total = 0.0
    for (provider, model), usage in sorted(grouped.items()):
        price = price_for_model(pricing_config, model, provider)
        input_rate = float(price.get("input_per_1m", 0.0))
        output_rate = float(price.get("output_per_1m", 0.0))
        request_fee = float(price.get("request_fee", 0.0))
        cost = (
            usage["input_tokens"] / 1_000_000 * input_rate
            + usage["output_tokens"] / 1_000_000 * output_rate
            + usage["requests"] * request_fee
        )
        total += cost
        rows.append(
            {
                "provider": provider,
                "model": model,
                **usage,
                "estimated_cost_usd": round(cost, 4),
                "pricing_source": price.get("source"),
            }
        )
    return {
        "mode": "actual_or_usage_estimated",
        "total_estimated_cost_usd": round(total, 4),
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
