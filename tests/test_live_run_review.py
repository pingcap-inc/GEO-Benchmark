"""Offline regressions for the September live-run review (synthetic answers only)."""
from __future__ import annotations

import csv
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from geo_benchmark.fact_judge import CoverageValidationError, JudgeSettings, JudgeUsage, SemanticFactJudge
from geo_benchmark.prompt_metadata import apply_metadata_overrides
from geo_benchmark.semantic_coverage import export_fields, write_coverage_report
from geo_benchmark.scoring import competitive_winner, competitive_breakdown, score_answer
from geo_benchmark.cli import load_prompts

REPO = Path(__file__).resolve().parents[1]
OVERRIDES = REPO / 'geo-benchmark/config/prompt_metadata_overrides.json'


def semantic_row(disposition='fact_covered', accuracy=None, selected=1, **counts):
    return {'target': 'TiDB', 'target_in_prompt': True, 'prompt_id': 'test',
            'answer_id': 'answer', 'model_surface': 'mock',
            'accuracy_checked_facts': 4,
            'semantic_fact_judge': {'mode': 'mock', 'coverage_disposition': disposition,
                                    'accuracy': accuracy, 'selected_facts': selected, **counts}}


class CoverageExplanationTests(unittest.TestCase):
    def test_processed_is_not_the_same_as_decided(self):
        row = semantic_row(not_enough_information_facts=1, checked_facts=0)
        result = export_fields(row)
        self.assertEqual(result['semantic_coverage_status'], 'not_enough_information')
        self.assertEqual(result['semantic_selected_facts'], 1)

    def test_comparison_disposition_not_topic_or_legacy_count_controls_exclusion(self):
        for topic in ['Competitive Comparisons', 'Hybrid Search & RAG', 'Deployment & Cloud']:
            row = semantic_row('comparison_metric_only', selected=0)
            row['prompt_type'] = topic
            self.assertEqual(export_fields(row)['semantic_coverage_status'], 'comparison_metric_only')

    def test_zero_accuracy_is_a_decisive_score(self):
        self.assertEqual(export_fields(semantic_row(accuracy=0))['semantic_coverage_status'], 'scored')

    def test_empty_approved_fact_mapping_is_not_reported_as_success(self):
        self.assertEqual(export_fields(semantic_row(selected=0))['semantic_coverage_status'], 'coverage_gap')

    def test_unknown_historical_csv_is_not_invented_as_review_required(self):
        row = {'target': 'TiDB', 'target_in_prompt': True, 'accuracy_checked_facts': 4,
               'semantic_checked_facts': 0, 'semantic_unavailable_facts': 0}
        self.assertEqual(export_fields(row)['semantic_coverage_status'], 'not_recorded')

    def test_review_pending_inconclusive_failure_and_not_applicable_remain_distinct(self):
        cases = [
            (semantic_row('review_required', selected=0, pending_fact_ids=['needs_owner']), 'review_required'),
            (semantic_row(unavailable_facts=1), 'judge_unavailable'),
            (semantic_row(not_applicable_facts=1), 'not_applicable'),
        ]
        for row, status in cases:
            self.assertEqual(export_fields(row)['semantic_coverage_status'], status)
        self.assertEqual(export_fields(cases[0][0])['semantic_pending_fact_ids'], 'needs_owner')

    def test_synthetic_276_answer_reconciliation(self):
        groups = [(152, semantic_row(accuracy=1)),
                  (96, semantic_row('comparison_metric_only', selected=0)),
                  (17, semantic_row('review_required', selected=0)),
                  (10, semantic_row(not_enough_information_facts=1)),
                  (1, semantic_row(unavailable_facts=1))]
        rows = []
        for count, row in groups:
            rows += [dict(row, answer_id=f'answer-{len(rows)+i}') for i in range(count)]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_coverage_report(root, rows)
            summary = json.loads((root / 'semantic-coverage-summary.json').read_text())
            with (root / 'semantic-coverage-audit.csv').open() as handle:
                audit = list(csv.DictReader(handle))
            self.assertEqual(len(audit), 276)
            self.assertEqual(summary['decisive_answers'], 152)
            self.assertEqual(sum(summary['status_counts'].values()), 276)
            self.assertEqual(summary['unexplained_answers'], 0)
            self.assertEqual(summary['status_counts']['comparison_metric_only'], 96)


class RuntimeCoverageGuardTests(unittest.TestCase):
    def judge(self, disposition='fact_covered', facts='ready'):
        judge = SemanticFactJudge.__new__(SemanticFactJudge)
        judge.settings = JudgeSettings(mode='mock')
        judge.coverage = {'p': {'coverage_disposition': disposition, 'fact_or_review_ids': facts,
                                'mapping_status': 'approved'}}
        judge.facts = {'ready': {'fact_id': 'ready', 'status': 'READY_FOR_JUDGE'},
                       'held': {'fact_id': 'held', 'status': 'REVIEW_REQUIRED'}}
        judge.payload = {'facts': list(judge.facts.values())}
        judge.fact_base_version = 'test'
        judge.conflict_rules = []
        judge.cache = {}
        judge.usage = JudgeUsage()
        judge._cache_dirty = False
        return judge

    def test_missing_branded_mapping_fails_before_call(self):
        judge = self.judge()
        with patch.object(judge, '_judge_fact') as request:
            with self.assertRaises(CoverageValidationError):
                judge.judge_answer({'prompt_id': 'missing', 'brand_class': 'branded'}, 'Answer', 'hash')
            request.assert_not_called()

    def test_non_branded_unmapped_answer_is_intentionally_unmapped(self):
        result = self.judge().judge_answer({'prompt_id': 'missing', 'brand_class': 'non_branded'}, 'Answer', 'hash')
        self.assertEqual(result['coverage_disposition'], 'unmapped')
        self.assertEqual(result['selected_facts'], 0)

    def test_unapproved_and_empty_or_held_fact_covered_mappings_fail(self):
        for facts in ['', 'held', 'unknown']:
            judge = self.judge(facts=facts)
            with self.assertRaises(CoverageValidationError):
                judge.judge_answer({'prompt_id': 'p'}, 'Answer', 'hash')
        judge = self.judge()
        judge.coverage['p']['mapping_status'] = 'needs_review'
        with self.assertRaises(CoverageValidationError):
            judge.judge_answer({'prompt_id': 'p'}, 'Answer', 'hash')

    def test_held_review_items_stay_held(self):
        judge = self.judge('review_required', 'held|review_item')
        with patch.object(judge, '_judge_fact') as request:
            result = judge.judge_answer({'prompt_id': 'p'}, 'Answer', 'hash')
            request.assert_not_called()
        self.assertEqual(result['pending_fact_ids'], ['held', 'review_item'])
        self.assertIsNone(result['accuracy'])

    def test_ready_facts_are_processed_even_when_result_is_inconclusive(self):
        judge = self.judge('review_required', 'ready|held')
        with patch.object(judge, '_judge_fact', return_value={'fact_id': 'ready', 'verdict': 'not_enough_information'}) as request:
            result = judge.judge_answer({'prompt_id': 'p'}, 'Answer', 'hash')
        self.assertEqual(request.call_count, 1)
        self.assertEqual(result['selected_facts'], 1)
        self.assertEqual(result['checked_facts'], 0)
        self.assertEqual(result['pending_fact_ids'], ['held'])


class PromptMetadataTests(unittest.TestCase):
    def test_exact_seven_retags_without_changing_identity_or_eligibility(self):
        original = json.loads((REPO / 'geo-benchmark/prompts/2026-09/prompts.json').read_text())
        revised = apply_metadata_overrides(original, OVERRIDES)
        changed = [b for a, b in zip(original, revised) if a['prompt_type'] != b['prompt_type']]
        self.assertEqual({p['prompt_id'] for p in changed}, {f'stable_branddef_{n:03d}' for n in [6,7,8,9,10,11,13]})
        self.assertEqual(sum(p['use_case'] == 'agentinfra' for p in changed), 5)
        self.assertEqual(sum(p['use_case'] == 'hybridrag' for p in changed), 2)
        for a, b in zip(original, revised):
            for key in ['prompt_id', 'prompt_text', 'brand_class', 'group', 'intent_weight']:
                self.assertEqual(a[key], b[key])
        self.assertEqual(apply_metadata_overrides(revised, OVERRIDES), revised)
        self.assertEqual(load_prompts(REPO / 'geo-benchmark', '2026-09'), revised)
        self.assertEqual(original, json.loads((REPO / 'geo-benchmark/prompts/2026-09/prompts.json').read_text()))

    def test_modified_question_does_not_inherit_old_review_exclusion(self):
        prompt = {'prompt_id': 'stable_compcomp_018', 'prompt_text': 'A different comparison'}
        self.assertEqual(apply_metadata_overrides([prompt], OVERRIDES), [prompt])

    def test_regeneration_preserves_frozen_ids_then_corrects_reporting_cluster(self):
        spec = importlib.util.spec_from_file_location('review_build_prompts', REPO / 'tools/build_prompts.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        rows = [[str(i), f'Filler {i}', 'Branded', 'TiDB Brand & Definitions', 'Awareness', 'Engineer', '1'] for i in range(1,6)]
        rows += [['6', 'Best database for AI agent platforms serving millions of users.', 'Non-branded', 'TiDB Brand & Definitions', 'Decision', 'Engineer', '1']]
        prompt = module.build(rows, '2026-10')[-1]
        self.assertEqual(prompt['prompt_id'], 'stable_branddef_006')
        self.assertEqual(prompt['prompt_type'], 'AI Agent Infrastructure')


class ComparisonRegressionTests(unittest.TestCase):
    def prompt(self, left='TiDB', right='Aurora'):
        return {'group': 'comparison', 'prompt_text': f'{left} vs {right} for SaaS.'}

    def test_final_shortlist_beats_earlier_conditional_product_profile_symmetrically(self):
        for preferred, other in [('TiDB','Aurora'), ('Aurora','TiDB'), ('CockroachDB','TiDB')]:
            answer = f'Choose {other} when an earlier condition applies.\n\n**Recommendation:** If write scale matters, shortlist **{preferred}** first, **{other}** if a hard constraint applies.'
            self.assertEqual(competitive_winner(answer, self.prompt(preferred, other)), preferred)

    def test_markdown_links_and_headings(self):
        answer = 'Choose Aurora if you need AWS.\n\n## Recommendation\n\n[TiDB](https://example.test/aurora)'
        self.assertEqual(competitive_winner(answer, self.prompt()), 'TiDB')

    def test_final_ambiguous_guidance_does_not_fall_back_to_earlier_choice(self):
        answer = 'Choose Aurora for AWS.\n\nRecommendation: It depends on the workload.'
        self.assertIsNone(competitive_winner(answer, self.prompt()))

    def test_conditional_tie_and_negation_do_not_manufacture_winners(self):
        for answer in ['Recommendation: Choose TiDB if X; choose Aurora if Y.',
                       'Recommendation: Shortlist TiDB first if X; shortlist Aurora first if Y.',
                       'Recommendation: Do not recommend TiDB.',
                       'Recommendation: Do not shortlist TiDB first.',
                       'Neither product is a clear winner.']:
            self.assertIsNone(competitive_winner(answer, self.prompt()))

    def test_genuine_aurora_verdict_is_preserved(self):
        self.assertEqual(competitive_winner('Recommendation: Choose Aurora.', self.prompt()), 'Aurora')

    def test_mismatched_prompt_keeps_detected_loss_but_leaves_competitive_kpi(self):
        prompts = load_prompts(REPO / 'geo-benchmark', '2026-09')
        prompt = next(p for p in prompts if p['prompt_id'] == 'stable_compcomp_018')
        raw = {'answer_id':'test','run_id':'test','month':'2026-09','prompt_id':prompt['prompt_id'],
               'model_surface':'mock','raw_answer':'TiDB Cloud Zero is for prototypes. Recommendation: Choose Aurora.'}
        row = score_answer(raw, prompt, {}, {}, 'TiDB')
        self.assertEqual(row['competitive_winner'], 'Aurora')
        self.assertFalse(row['comparison_eligible'])
        self.assertEqual(row['comparison_review_status'], 'needs_review')
        result = competitive_breakdown([row])
        self.assertEqual(result['excluded_comparison_answers'], 1)
        self.assertEqual(result['valid_comparison_answers'], 0)
        self.assertIsNone(result['target_win_rate'])
        approved = dict(row, comparison_eligible=True)
        self.assertEqual(competitive_breakdown([approved])['target_win_rate'], 0)


if __name__ == '__main__':
    unittest.main()
