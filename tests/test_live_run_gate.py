import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from geo_benchmark.cli import confirm_live_run, prepare


PLANNED = {
    "total_estimated_cost_usd": 1.23,
    "scope": "scope",
    "assumptions": "assumptions",
    "providers": [
        {
            "provider": "openai",
            "model": "gpt-5-mini",
            "requests": 120,
            "input_tokens": 1000,
            "output_tokens": 2000,
            "estimated_cost_usd": 1.23,
        }
    ],
}


class LiveRunGateTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        with contextlib.redirect_stdout(io.StringIO()):
            prepare(self.root, "2026-09", 10, 0.3, force=False)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_free_providers_never_prompt(self) -> None:
        with patch("builtins.input", side_effect=AssertionError("must not prompt")):
            with contextlib.redirect_stdout(io.StringIO()):
                confirm_live_run(self.root, ["mock"], PLANNED, assume_yes=False)

    def test_assume_yes_skips_prompt_for_paid_providers(self) -> None:
        with patch("builtins.input", side_effect=AssertionError("must not prompt")):
            with contextlib.redirect_stdout(io.StringIO()):
                confirm_live_run(self.root, ["openai"], PLANNED, assume_yes=True)

    def test_non_interactive_paid_run_aborts_without_yes(self) -> None:
        with patch("sys.stdin.isatty", return_value=False):
            with contextlib.redirect_stdout(io.StringIO()):
                with self.assertRaises(SystemExit):
                    confirm_live_run(self.root, ["openai"], PLANNED, assume_yes=False)

    def test_interactive_decline_aborts(self) -> None:
        with patch("sys.stdin.isatty", return_value=True), patch("builtins.input", return_value="n"):
            with contextlib.redirect_stdout(io.StringIO()):
                with self.assertRaises(SystemExit):
                    confirm_live_run(self.root, ["openai"], PLANNED, assume_yes=False)

    def test_interactive_accept_proceeds(self) -> None:
        with patch("sys.stdin.isatty", return_value=True), patch("builtins.input", return_value="y"):
            with contextlib.redirect_stdout(io.StringIO()):
                confirm_live_run(self.root, ["openai"], PLANNED, assume_yes=False)


if __name__ == "__main__":
    unittest.main()
