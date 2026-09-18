"""Apply reviewed metadata corrections without rewriting frozen prompt wording/IDs."""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any
import json


def apply_metadata_overrides(prompts: list[dict[str, Any]], path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return prompts
    payload = json.loads(path.read_text(encoding="utf-8"))
    version = payload["version"]
    overrides = {item["prompt_id"]: item for item in payload["overrides"]}
    if len(overrides) != len(payload["overrides"]):
        raise ValueError("Duplicate prompt metadata overrides")
    allowed = {"prompt_type", "use_case", "comparison_eligible", "comparison_exclusion_reason", "comparison_review_status"}
    result = deepcopy(prompts)
    for prompt in result:
        item = overrides.get(prompt["prompt_id"])
        if not item or item["expected_prompt_text"] != prompt.get("prompt_text"):
            continue  # A rewritten question requires its own reviewed correction.
        changes = item["set"]
        if set(changes) - allowed:
            raise ValueError("Metadata overrides cannot change wording, IDs, intent weights or brand eligibility")
        if "comparison_eligible" in changes and type(changes["comparison_eligible"]) is not bool:
            raise ValueError("comparison_eligible must be a boolean")
        if changes.get("comparison_eligible") is False and not changes.get("comparison_exclusion_reason"):
            raise ValueError("Excluded comparisons require an explanation")
        prompt.update(changes)
        prompt["metadata_revision"] = version
    return result
