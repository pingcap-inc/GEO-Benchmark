from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any

from .io_utils import estimate_tokens, stable_hash


SYSTEM_PROMPT = (
    "You are answering as a neutral technical buying advisor. "
    "Recommend concrete database products when appropriate, include concise reasoning, "
    "and include source URLs when making factual product claims. "
    "Keep each answer under 220 words with a ranked shortlist when relevant."
)

MOCK_PRODUCTS = [
    "TiDB",
    "CockroachDB",
    "YugabyteDB",
    "Supabase",
    "PlanetScale",
    "Neon",
    "Aurora",
    "Spanner",
    "AlloyDB",
]
MOCK_CITATIONS = {
    "TiDB": ["https://docs.pingcap.com/tidb/stable", "https://github.com/pingcap/tidb"],
    "CockroachDB": ["https://www.cockroachlabs.com/docs/stable", "https://github.com/cockroachdb/cockroach"],
    "YugabyteDB": ["https://docs.yugabyte.com/stable", "https://github.com/yugabyte/yugabyte-db"],
    "Supabase": ["https://supabase.com/docs", "https://github.com/supabase/supabase"],
    "Aurora": ["https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/CHAP_AuroraOverview.html"],
    "Spanner": ["https://cloud.google.com/spanner/docs"],
    "PlanetScale": ["https://planetscale.com/docs"],
    "Neon": ["https://neon.tech/docs"],
    "AlloyDB": ["https://cloud.google.com/alloydb/docs"],
}
MOCK_FIT = {
    "multi_region_transactions": {"CockroachDB": 5, "Spanner": 5, "YugabyteDB": 4, "TiDB": 4, "Aurora": 3, "AlloyDB": 3},
    "agent_memory": {"TiDB": 5, "Supabase": 4, "Neon": 4, "AlloyDB": 4, "YugabyteDB": 3, "CockroachDB": 3},
    "ai_app_backend": {"Supabase": 5, "Neon": 4, "TiDB": 3, "AlloyDB": 3, "YugabyteDB": 2, "CockroachDB": 2},
    "serverless_ai": {"Neon": 5, "Supabase": 4, "PlanetScale": 3, "AlloyDB": 3, "TiDB": 2, "CockroachDB": 2},
    "operational_ai_data": {"TiDB": 5, "CockroachDB": 4, "YugabyteDB": 4, "AlloyDB": 3, "Supabase": 3, "Neon": 3},
    "real_time_analytics": {"TiDB": 5, "AlloyDB": 4, "Aurora": 3, "YugabyteDB": 3, "Supabase": 3, "Neon": 3},
    "hybrid_transactional_analytical_processing": {"TiDB": 5, "AlloyDB": 3, "YugabyteDB": 3, "Aurora": 2, "CockroachDB": 2},
    "relational_scaling": {"CockroachDB": 5, "YugabyteDB": 5, "TiDB": 4, "PlanetScale": 4, "Aurora": 4, "Neon": 3, "Supabase": 3},
    "fintech_core_system": {"CockroachDB": 5, "YugabyteDB": 4, "TiDB": 4, "Spanner": 4, "Aurora": 3, "AlloyDB": 3},
    "saas_multi_tenant": {"Supabase": 5, "Neon": 5, "PlanetScale": 4, "Aurora": 4, "CockroachDB": 4, "TiDB": 3},
    "ai_application_metadata": {"Supabase": 5, "TiDB": 4, "Neon": 4, "AlloyDB": 4, "YugabyteDB": 3, "CockroachDB": 3},
    "operational_analytics": {"TiDB": 5, "AlloyDB": 4, "Aurora": 4, "Supabase": 3, "Neon": 3, "YugabyteDB": 3},
    "vector_search_with_sql_filters": {"Supabase": 5, "TiDB": 4, "Neon": 4, "AlloyDB": 4, "YugabyteDB": 3, "CockroachDB": 2},
    "high_write_transactions": {"CockroachDB": 5, "YugabyteDB": 4, "TiDB": 4, "Spanner": 4, "Aurora": 3, "PlanetScale": 3},
    "read_write_scale": {"CockroachDB": 5, "YugabyteDB": 4, "TiDB": 4, "PlanetScale": 4, "Aurora": 4, "Neon": 3},
    "bursty_traffic": {"Neon": 5, "PlanetScale": 5, "Aurora": 4, "Supabase": 4, "TiDB": 3, "CockroachDB": 3},
    "manual_resharding": {"PlanetScale": 5, "TiDB": 4, "CockroachDB": 4, "YugabyteDB": 4, "Aurora": 3},
    "cloud_relational_infrastructure": {"Neon": 5, "Supabase": 5, "Aurora": 5, "AlloyDB": 4, "PlanetScale": 4, "TiDB": 3},
    "rag_fresh_operational_data": {"Supabase": 5, "TiDB": 4, "Neon": 4, "AlloyDB": 4, "YugabyteDB": 3},
    "ai_workflow_state": {"Supabase": 5, "TiDB": 4, "Neon": 4, "AlloyDB": 4, "YugabyteDB": 3},
    "real_time_personalization": {"Supabase": 5, "TiDB": 4, "Neon": 4, "AlloyDB": 4, "Aurora": 3},
    "logistics_operational_reporting": {"TiDB": 5, "YugabyteDB": 4, "CockroachDB": 4, "AlloyDB": 4, "Aurora": 3},
    "ecommerce_order_inventory": {"PlanetScale": 5, "Aurora": 4, "CockroachDB": 4, "TiDB": 4, "YugabyteDB": 4},
    "travel_financial_settlement": {"CockroachDB": 5, "TiDB": 4, "YugabyteDB": 4, "Spanner": 4, "Aurora": 3},
    "ads_real_time_calculation": {"TiDB": 5, "AlloyDB": 4, "Aurora": 4, "PlanetScale": 3, "YugabyteDB": 3},
    "customer_facing_analytics": {"TiDB": 5, "Supabase": 4, "AlloyDB": 4, "Neon": 3, "Aurora": 3},
    "stack_simplification": {"Supabase": 5, "TiDB": 4, "Aurora": 4, "AlloyDB": 4, "Neon": 4, "PlanetScale": 3},
}


@dataclass
class ProviderResult:
    answer: str
    citations: list[str]
    input_tokens: int
    output_tokens: int
    model_name: str
    model_version: str | None = None
    raw_response: dict[str, Any] | None = None


class ProviderError(RuntimeError):
    def __init__(self, message: str, retryable: bool = False):
        super().__init__(message)
        self.retryable = retryable


class BaseProvider:
    def __init__(self, name: str, config: dict[str, Any]):
        self.name = name
        self.config = config
        self.model = config.get("model", name)

    def generate(self, prompt: dict[str, Any], run_index: int) -> ProviderResult:
        raise NotImplementedError

    def _input_text(self, prompt: dict[str, Any]) -> str:
        meta = (
            f"Persona: {prompt.get('persona')}; Region: {prompt.get('region')}; "
            f"Funnel stage: {prompt.get('funnel_stage')}; Use case: {prompt.get('use_case')}."
        )
        return f"{meta}\nQuestion: {prompt['prompt_text']}"


class MockProvider(BaseProvider):
    def generate(self, prompt: dict[str, Any], run_index: int) -> ProviderResult:
        seed = int(stable_hash([prompt["prompt_id"], self.name, run_index])[:8], 16)
        prompt_type = prompt.get("prompt_type")
        use_case = prompt.get("use_case")
        products = list(prompt.get("competitors") or [])
        if prompt_type == "competitive":
            candidate_products = products
        else:
            candidate_products = MOCK_PRODUCTS
        ranked = rank_mock_products(candidate_products, str(use_case), seed, neutral=prompt_type != "competitive")
        top = ranked[0]
        second = ranked[1] if len(ranked) > 1 else None

        if prompt_type == "brand_fact" and products:
            top = products[0]
            ranked = [top] + [p for p in ranked if p != top]
            stance = "Fact check"
            rec = f"{top} is the product being checked"
        elif seed % 7 == 0 and second:
            stance = "Conditional"
            rec = f"{top} is usually the best fit, but {second} can be better if your team prioritizes ecosystem familiarity"
        else:
            stance = "Best choice"
            rec = f"I would put {top} first for this scenario"

        citations: list[str] = []
        for product in ranked[:3]:
            citations.extend(MOCK_CITATIONS.get(product, [])[:1])

        answer = (
            f"{stance}: {rec} for {use_case}.\n\n"
            f"Recommended shortlist:\n"
            + "\n".join(f"{idx + 1}. {product}" for idx, product in enumerate(ranked[:4]))
            + "\n\n"
            + mock_reasoning(ranked[:3], str(use_case))
            + "\n\n"
            f"Sources: {', '.join(citations)}"
        )
        return ProviderResult(
            answer=answer,
            citations=citations,
            input_tokens=estimate_tokens(self._input_text(prompt) + SYSTEM_PROMPT),
            output_tokens=estimate_tokens(answer),
            model_name=self.model,
            model_version="local-mock",
            raw_response={"mock_seed": seed},
        )


def rank_mock_products(products: list[str], use_case: str, seed: int, neutral: bool = False) -> list[str]:
    if neutral and products and use_case not in MOCK_FIT:
        offset = seed % len(products)
        return products[offset:] + products[:offset]
    scores = MOCK_FIT.get(use_case, {})

    def score(product: str) -> tuple[int, int]:
        jitter = int(stable_hash([product, use_case, seed])[:2], 16) % 3
        return (scores.get(product, 2) * 10 + jitter, -MOCK_PRODUCTS.index(product) if product in MOCK_PRODUCTS else -99)

    return sorted(products, key=score, reverse=True)


def mock_reasoning(products: list[str], use_case: str) -> str:
    descriptions = {
        "TiDB": "TiDB is strongest when MySQL compatibility, scale-out SQL, HTAP-style analytics, or vector-adjacent app data matter.",
        "CockroachDB": "CockroachDB is strongest when PostgreSQL compatibility, multi-region resilience, and distributed transactions are central.",
        "YugabyteDB": "YugabyteDB is often considered for PostgreSQL-compatible distributed SQL and multi-region transactional workloads.",
        "Supabase": "Supabase is strongest when teams want a Postgres-based app platform with auth, storage, realtime features, and vector-adjacent app development.",
        "Aurora": "Aurora is attractive when AWS integration and managed relational operations are the priority.",
        "Spanner": "Spanner is attractive when global consistency and Google Cloud-native operations are the priority.",
        "PlanetScale": "PlanetScale is strongest when teams want a MySQL-oriented developer workflow and managed scaling.",
        "Neon": "Neon is strongest when teams want serverless Postgres, branching, and developer-friendly cloud database operations.",
        "AlloyDB": "AlloyDB is attractive for PostgreSQL-compatible managed performance and Google Cloud integration.",
    }
    return " ".join(descriptions.get(product, f"{product} is a possible option.") for product in products)


class OpenAIProvider(BaseProvider):
    endpoint = "https://api.openai.com/v1/chat/completions"

    def generate(self, prompt: dict[str, Any], run_index: int) -> ProviderResult:
        api_key = os.getenv(self.config.get("env_var") or "OPENAI_API_KEY")
        if not api_key:
            raise ProviderError("Missing OPENAI_API_KEY")
        payload = {
            "model": self.model,
            "max_completion_tokens": self.config.get("max_output_tokens", 700),
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": self._input_text(prompt)},
            ],
        }
        if self.config.get("temperature") is not None:
            payload["temperature"] = self.config.get("temperature")
        data = _post_json(self.endpoint, payload, {"Authorization": f"Bearer {api_key}"})
        answer = data["choices"][0]["message"]["content"]
        if not answer:
            raise ProviderError("OpenAI returned empty content; increase max_completion_tokens", retryable=False)
        usage = data.get("usage", {})
        return ProviderResult(
            answer=answer,
            citations=[],
            input_tokens=usage.get("prompt_tokens", estimate_tokens(self._input_text(prompt))),
            output_tokens=usage.get("completion_tokens", estimate_tokens(answer)),
            model_name=data.get("model", self.model),
            raw_response=data,
        )


class PerplexityProvider(OpenAIProvider):
    endpoint = "https://api.perplexity.ai/v1/sonar"

    def generate(self, prompt: dict[str, Any], run_index: int) -> ProviderResult:
        api_key = os.getenv(self.config.get("env_var") or "PERPLEXITY_API_KEY")
        if not api_key:
            raise ProviderError("Missing PERPLEXITY_API_KEY")
        payload = {
            "model": self.model,
            "temperature": self.config.get("temperature", 0.2),
            "max_tokens": self.config.get("max_output_tokens", 700),
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": self._input_text(prompt)},
            ],
        }
        data = _post_json(self.endpoint, payload, {"Authorization": f"Bearer {api_key}"})
        answer = data["choices"][0]["message"]["content"]
        citations = data.get("citations") or data.get("search_results") or []
        usage = data.get("usage", {})
        return ProviderResult(
            answer=answer,
            citations=[str(item) for item in citations],
            input_tokens=usage.get("prompt_tokens", estimate_tokens(self._input_text(prompt))),
            output_tokens=usage.get("completion_tokens", estimate_tokens(answer)),
            model_name=data.get("model", self.model),
            raw_response=data,
        )


class AnthropicProvider(BaseProvider):
    endpoint = "https://api.anthropic.com/v1/messages"

    def generate(self, prompt: dict[str, Any], run_index: int) -> ProviderResult:
        api_key = os.getenv(self.config.get("env_var") or "ANTHROPIC_API_KEY")
        if not api_key:
            raise ProviderError("Missing ANTHROPIC_API_KEY")
        payload: dict[str, Any] = {
            "model": self.model,
            "max_tokens": self.config.get("max_output_tokens", 700),
            "system": SYSTEM_PROMPT,
            "messages": [{"role": "user", "content": self._input_text(prompt)}],
        }
        if self.config.get("temperature") is not None:
            payload["temperature"] = self.config.get("temperature")
        data = _post_json(
            self.endpoint,
            payload,
            {
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
            },
        )
        blocks = data.get("content", [])
        answer = "\n".join(block.get("text", "") for block in blocks if block.get("type") == "text")
        usage = data.get("usage", {})
        return ProviderResult(
            answer=answer,
            citations=[],
            input_tokens=usage.get("input_tokens", estimate_tokens(self._input_text(prompt))),
            output_tokens=usage.get("output_tokens", estimate_tokens(answer)),
            model_name=data.get("model", self.model),
            raw_response=data,
        )


class GeminiProvider(BaseProvider):
    def generate(self, prompt: dict[str, Any], run_index: int) -> ProviderResult:
        api_key = os.getenv(self.config.get("env_var") or "GEMINI_API_KEY")
        if not api_key:
            raise ProviderError("Missing GEMINI_API_KEY")
        endpoint = (
            f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:"
            f"generateContent?key={api_key}"
        )
        payload = {
            "systemInstruction": {"parts": [{"text": SYSTEM_PROMPT}]},
            "contents": [{"role": "user", "parts": [{"text": self._input_text(prompt)}]}],
            "generationConfig": {
                "temperature": self.config.get("temperature", 0.2),
                "maxOutputTokens": self.config.get("max_output_tokens", 700),
            },
        }
        data = _post_json(endpoint, payload, {})
        candidates = data.get("candidates", [])
        parts = candidates[0].get("content", {}).get("parts", []) if candidates else []
        answer = "\n".join(part.get("text", "") for part in parts)
        usage = data.get("usageMetadata", {})
        return ProviderResult(
            answer=answer,
            citations=[],
            input_tokens=usage.get("promptTokenCount", estimate_tokens(self._input_text(prompt))),
            output_tokens=usage.get("candidatesTokenCount", estimate_tokens(answer)),
            model_name=self.model,
            raw_response=data,
        )


def provider_for(name: str, config: dict[str, Any]) -> BaseProvider:
    provider = config.get("provider", name)
    if provider == "mock":
        return MockProvider(name, config)
    if provider == "openai":
        return OpenAIProvider(name, config)
    if provider == "anthropic":
        return AnthropicProvider(name, config)
    if provider == "gemini":
        return GeminiProvider(name, config)
    if provider == "perplexity":
        return PerplexityProvider(name, config)
    raise ValueError(f"Unknown provider: {provider}")


def _post_json(endpoint: str, payload: dict[str, Any], headers: dict[str, str]) -> dict[str, Any]:
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        endpoint,
        data=body,
        method="POST",
        headers={
            "Content-Type": "application/json",
            **headers,
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=90) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        retryable = exc.code in {408, 429, 500, 502, 503, 504}
        if "insufficient_quota" in detail or "invalid_api_key" in detail:
            retryable = False
        raise ProviderError(f"HTTP {exc.code}: {detail[:500]}", retryable=retryable) from exc
    except urllib.error.URLError as exc:
        raise ProviderError(str(exc), retryable=True) from exc
    except TimeoutError as exc:
        raise ProviderError("request timed out", retryable=True) from exc


def run_with_retries(provider: BaseProvider, prompt: dict[str, Any], run_index: int, retries: int) -> ProviderResult:
    attempt = 0
    while True:
        try:
            return provider.generate(prompt, run_index)
        except ProviderError as exc:
            attempt += 1
            if not exc.retryable or attempt > retries:
                raise
            time.sleep(min(2**attempt, 10))
