from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "build_prompts.py"
SPEC = importlib.util.spec_from_file_location("build_prompts", MODULE_PATH)
assert SPEC and SPEC.loader
build_prompts = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(build_prompts)


class BuildPromptsTests(unittest.TestCase):
    def test_retired_row_reserves_prompt_id(self):
        rows = [
            ["1", "First active prompt", "Non-branded", "AI Agent Infrastructure", "Consideration", "Engineer", "10"],
            ["2", "Retired prompt", "Non-branded", "AI Agent Infrastructure", "Consideration", "Engineer", "9", "retired", "No longer used"],
            ["3", "Next active prompt", "Non-branded", "AI Agent Infrastructure", "Consideration", "Engineer", "8"],
        ]

        prompts = build_prompts.build(rows, "2026-09")

        self.assertEqual(
            [prompt["prompt_id"] for prompt in prompts],
            ["stable_agentinfra_001", "stable_agentinfra_003"],
        )

    def test_update_status_and_note_are_preserved(self):
        rows = [[
            "217", "New approved prompt", "Non-branded", "Scale & Architecture",
            "Decision", "Backend / App Engineer", "30", "new", "Validated addition",
        ]]

        prompt = build_prompts.build(rows, "2026-09")[0]

        self.assertEqual(prompt["source"]["update_status"], "new")
        self.assertEqual(prompt["source"]["update_note"], "Validated addition")


if __name__ == "__main__":
    unittest.main()
