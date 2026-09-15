import csv
import contextlib
import io
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from geo_benchmark.io_utils import write_json, write_jsonl
from geo_benchmark.cli import main
from geo_benchmark.prompt_research import (
    DATAFORSEO_TRENDS_ENDPOINT,
    PromptResearchError,
    ResearchSettings,
    assign_themes,
    build_candidates,
    build_theme_profiles,
    extract_paa_questions,
    extract_trend_stats,
    collect_external_signals,
    fetch_semrush_metrics,
    request_json,
    run_prompt_research,
    signal,
)


class PromptResearchTests(unittest.TestCase):
    def test_cli_preserves_fan_out_text_and_warns_about_missing_offline_sources(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            month = '2026-10'
            (root / 'config').mkdir()
            (root / 'config/prompt_research_seeds.csv').write_text(
                'theme,seed_query,brand_class,match_terms,status\n'
                'tidb_htap,TiDB HTAP,branded,HTAP,approved\n')
            internal = root / 'prompt-research' / month / 'internal_signals.csv'
            internal.parent.mkdir(parents=True)
            internal.write_text('query,source,frequency\nTiDB HTAP,support,2\n')
            write_json(root / 'prompts' / month / 'prompts.json', [])
            question = "How does TiDB's HTAP work?"
            write_jsonl(root / 'runs' / month / 'raw_answers.jsonl', [
                {'status': 'ok', 'fan_out_status': 'captured', 'model_surface': provider,
                 'fan_out_queries': [text]} for provider, text in
                [('openai', question), ('gemini', 'how does tidb s htap work')]])
            before = (root / 'prompts' / month / 'prompts.json').read_bytes()
            output = io.StringIO()
            with contextlib.redirect_stdout(output), patch('socket.socket', side_effect=AssertionError('Network forbidden')):
                self.assertEqual(main(['--data-dir', str(root), 'research-prompts',
                                       '--month', month, '--offline']), 0)
            report = root / 'reports' / month / 'prompt-research'
            with (report / 'prompt_research_evidence.csv').open() as handle:
                model = next(r for r in csv.DictReader(handle) if r['signal_group'] == 'model')
            self.assertEqual(model['text'], question)
            self.assertEqual(model['frequency'], '2')
            self.assertEqual(json.loads(model['metadata'])['providers'], ['gemini', 'openai'])
            with (report / 'top_20_prompt_candidates.csv').open() as handle:
                candidate = next(csv.DictReader(handle))
            self.assertEqual(candidate['candidate_prompt'], question)
            self.assertEqual(candidate['source_question'], question)
            self.assertIn(question, (report / 'prompt-research.md').read_text())
            summary = json.loads((report / 'prompt_research_summary.json').read_text())
            for source in ['PAA', 'Semrush', 'Trends']:
                self.assertTrue(any(source + ' cache unavailable' in w for w in summary['warnings']))
                self.assertIn(source + ' cache unavailable', output.getvalue())
            self.assertEqual(summary['usage_this_invocation']['dataforseo_calls'], 0)
            self.assertEqual(summary['usage_this_invocation']['semrush_calls'], 0)
            self.assertEqual(before, (root / 'prompts' / month / 'prompts.json').read_bytes())

    def test_offline_refresh_conflict_is_rejected_before_writes_or_fetches(self):
        with tempfile.TemporaryDirectory() as tmp, patch('socket.socket', side_effect=AssertionError('Network forbidden')):
            with self.assertRaisesRegex(SystemExit, '--offline and --refresh'):
                main(['--data-dir', tmp, 'research-prompts', '--month', '2026-10', '--offline', '--refresh'])
            self.assertEqual(list(Path(tmp).iterdir()), [])
            with self.assertRaisesRegex(PromptResearchError, '--offline and --refresh'):
                collect_external_signals([], Path(tmp), ResearchSettings(offline=True, refresh=True))

    def test_semrush_direct_call_without_key_has_clear_error(self):
        with patch.dict(os.environ, {}, clear=True), patch('socket.socket', side_effect=AssertionError('Network forbidden')):
            with self.assertRaisesRegex(PromptResearchError, 'Set SEMRUSH_API_KEY'):
                fetch_semrush_metrics('TiDB', ResearchSettings())

    def test_extract_paa_questions_handles_nested_dataforseo_items(self):
        response = {
            "tasks": [{
                "status_code": 20000,
                "result": [{
                    "items": [{
                        "type": "people_also_ask",
                        "items": [
                            {"type": "people_also_ask_element", "title": "Which database supports vector transactions?", "rank_group": 1},
                            {"type": "people_also_ask_element", "title": "How do AI agents store memory?", "rank_group": 2},
                        ],
                    }]
                }],
            }]
        }

        questions = extract_paa_questions(response)

        self.assertEqual([item["question"] for item in questions], [
            "Which database supports vector transactions?",
            "How do AI agents store memory?",
        ])

    def test_assign_themes_uses_approved_seed_vocabulary(self):
        seeds = [{
            "theme": "agent_memory",
            "seed_query": "database for persistent AI agent memory",
            "brand_class": "non_branded",
            "match_terms": ["agent memory", "persistent memory"],
        }]
        profiles = build_theme_profiles(seeds)

        self.assertEqual(assign_themes("How should an agent store persistent memory?", profiles), ["agent_memory"])
        self.assertEqual(assign_themes("best bicycle for commuting", profiles), [])

    def test_candidates_require_two_signal_groups(self):
        seeds = [{
            "theme": "agent_memory", "seed_query": "database for AI agent memory",
            "brand_class": "non_branded", "match_terms": ["agent memory"],
        }]
        external = signal("external", "people_also_ask", "Which database is best for persistent agent memory?", "agent_memory", 1, {})

        self.assertEqual(build_candidates([external], [], seeds), [])

        model = signal("model", "fan_out", "best persistent agent memory database", "agent_memory", 3, {})
        candidates = build_candidates([external, model], [], seeds)
        self.assertEqual(len(candidates), 1)
        self.assertEqual(candidates[0]["signal_group_count"], 2)
        self.assertEqual(candidates[0]["review_status"], "pending")

    def test_trend_stats_reports_direction(self):
        response = {"tasks": [{"result": [{"items": [{
            "type": "google_trends_graph",
            "keywords": ["agent memory"],
            "data": [{"values": [10]}, {"values": [12]}, {"values": [30]}, {"values": [35]}],
        }]}]}]}

        stats = extract_trend_stats(response, ["agent memory"])

        self.assertEqual(stats["agent memory"]["trend_direction"], "rising")
        self.assertEqual(stats["agent memory"]["points"], 4)

    def test_uses_google_trends_endpoint(self):
        self.assertEqual(
            DATAFORSEO_TRENDS_ENDPOINT,
            "https://api.dataforseo.com/v3/keywords_data/google_trends/explore/live",
        )

    def test_dataforseo_task_error_is_rejected(self):
        response = {
            "status_code": 20000,
            "tasks": [{"status_code": 40501, "status_message": "Invalid Field"}],
        }
        fake_http_response = MagicMock()
        fake_http_response.__enter__.return_value.read.return_value = json.dumps(response).encode("utf-8")
        with patch("urllib.request.urlopen", return_value=fake_http_response):
            with self.assertRaisesRegex(PromptResearchError, "Invalid Field"):
                request_json(
                    "https://api.dataforseo.com/v3/example",
                    "POST",
                    [{}],
                    {"Authorization": "Basic redacted"},
                )

    def test_end_to_end_writes_review_files_and_reuses_cache(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "benchmark"
            month = "2026-10"
            (root / "config").mkdir(parents=True)
            seed_path = root / "config" / "prompt_research_seeds.csv"
            seed_path.write_text(
                "theme,seed_query,brand_class,match_terms,status\n"
                "agent_memory,database for persistent AI agent memory,non_branded,agent memory|persistent memory,approved\n",
                encoding="utf-8",
            )
            internal_path = root / "prompt-research" / month / "internal_signals.csv"
            internal_path.parent.mkdir(parents=True)
            internal_path.write_text(
                "query,source,frequency,notes\n"
                "How do teams store persistent agent memory?,gsc,4,\n",
                encoding="utf-8",
            )
            prompts = [{"prompt_id": "existing", "prompt_text": "What is an AI agent?"}]
            write_json(root / "prompts" / month / "prompts.json", prompts)
            write_jsonl(root / "runs" / month / "raw_answers.jsonl", [{
                "status": "ok",
                "model_surface": "gemini",
                "fan_out_status": "captured",
                "fan_out_queries": ["persistent agent memory database options"],
            }])
            paa_response = {
                "status_code": 20000,
                "tasks": [{"status_code": 20000, "cost": 0.003, "result": [{"items": [{
                    "type": "people_also_ask",
                    "items": [{
                        "type": "people_also_ask_element",
                        "title": "Which database is best for persistent agent memory?",
                        "rank_group": 1,
                    }],
                }]}]}],
            }
            settings = ResearchSettings(include_semrush=False, include_trends=False, max_candidates=20)
            env = {"DATAFORSEO_LOGIN": "login", "DATAFORSEO_PASSWORD": "password"}
            with patch.dict(os.environ, env, clear=False), patch(
                "geo_benchmark.prompt_research.fetch_dataforseo_paa", return_value=paa_response
            ) as fetch:
                result = run_prompt_research(root, month, settings)
                self.assertEqual(fetch.call_count, 1)

            self.assertEqual(result["candidate_count"], 1)
            report_dir = root / "reports" / month / "prompt-research"
            self.assertTrue((report_dir / "top_20_prompt_candidates.csv").exists())
            self.assertTrue((report_dir / "prompt_research_evidence.csv").exists())
            self.assertTrue((report_dir / "prompt_research_summary.json").exists())
            self.assertTrue((report_dir / "prompt-research.md").exists())
            self.assertEqual(json.loads((root / "prompts" / month / "prompts.json").read_text()), prompts)
            with (report_dir / "top_20_prompt_candidates.csv").open(newline="", encoding="utf-8") as handle:
                row = next(csv.DictReader(handle))
            self.assertEqual(row["review_status"], "pending")
            self.assertEqual(row["signal_group_count"], "3")

            with patch.dict(os.environ, env, clear=False), patch(
                "geo_benchmark.prompt_research.fetch_dataforseo_paa", side_effect=AssertionError("cache was not reused")
            ) as fetch:
                cached_result = run_prompt_research(root, month, settings)
                self.assertEqual(fetch.call_count, 0)
            self.assertEqual(cached_result["candidate_count"], 1)


if __name__ == "__main__":
    unittest.main()
