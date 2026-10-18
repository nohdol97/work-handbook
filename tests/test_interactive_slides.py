import json
import tempfile
import unittest
from pathlib import Path

from scripts import interactive_slides as slides


class InteractiveSlidesTest(unittest.TestCase):
    def fixture(self, root):
        (root / 'docs/ko/topic').mkdir(parents=True)
        (root / 'docs/en/topic').mkdir(parents=True)
        (root / 'mkdocs.yml').write_text('nav:\n  - Topic: topic/demo.md\n')
        for lang, title in [('ko', '흐름'), ('en', 'Flow')]:
            (root / f'docs/{lang}/topic/demo.md').write_text(
                f'---\nid: demo\nstatus: studied\nknowledge_ids:\n  - K-1\n---\n'
                f'# {title}\n\n## Step one\n\nFirst input.\n\n## Step two\n\nSecond output.\n'
            )

    def test_discovery_excludes_internal_and_pairs_languages(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.fixture(root)
            (root / 'docs/README.md').write_text('# internal')
            found = slides.discover(root)
            self.assertEqual([(p.language, p.relative_path.as_posix()) for p in found],
                             [('ko', 'topic/demo.md'), ('en', 'topic/demo.md')])
            self.assertEqual({p.document_id for p in found}, {'demo'})

    def test_schema_has_source_mapping_and_deterministic_steps(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.fixture(root)
            page = slides.discover(root)[0]
            schema = slides.build_schema(root, page)
            self.assertEqual(schema['document_id'], 'demo')
            self.assertEqual(schema['language'], 'ko')
            self.assertTrue(all(s['source']['line_start'] for s in schema['slides']))
            self.assertTrue(all(s['body_html'] and s['section_id'] for s in schema['slides']))
            self.assertEqual(schema['knowledge_ids'], ['K-1'])
            self.assertEqual(json.dumps(schema, ensure_ascii=False),
                             json.dumps(slides.build_schema(root, page), ensure_ascii=False))

    def test_incremental_preserves_unchanged_html_and_reports_failed_page(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.fixture(root)
            bundle = root / 'bundle.js'
            bundle.write_text('document.body.dataset.ready="yes";')
            output = root / 'out'
            first = slides.build(root, output, bundle)
            self.assertEqual(first['generated'], 2)
            self.assertEqual(first['summary']['public_pages'], 2)
            self.assertEqual(first['summary']['source_lines'], first['summary']['mapped_lines'])
            target = output / 'ko/topic/demo/index.html'
            schema_path = output / 'schema/ko/topic/demo.json'
            self.assertTrue(schema_path.is_file())
            self.assertEqual(json.loads(schema_path.read_text())['document_id'], 'demo')
            original = target.read_bytes()
            second = slides.build(root, output, bundle)
            self.assertEqual(second['generated'], 0)
            self.assertEqual(second['skipped'], 2)
            self.assertEqual(target.read_bytes(), original)
            (root / 'docs/en/topic/demo.md').write_text('broken')
            third = slides.build(root, output, bundle)
            self.assertTrue(third['failures'])
            self.assertTrue((output / 'en/topic/demo/index.html').is_file())

    def test_registered_interaction_can_extend_without_document_branch(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.fixture(root)
            slides.register_interaction(
                'test-model', lambda raw, heading, language: 'First input.' in raw,
                lambda raw, heading, language: {'type': 'parameter',
                    'data': {'field': 'x', 'minimum': 1, 'maximum': 3, 'operator': '>', 'threshold': 2},
                    'model_note': 'Source-only model'}, priority=100)
            try:
                schema = slides.build_schema(root, slides.discover(root)[0])
                self.assertTrue(any(s['interaction']['model_note'] == 'Source-only model'
                                    for s in schema['slides']))
            finally:
                slides.unregister_interaction('test-model')

    def test_full_build_removes_stale_published_page(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.fixture(root)
            bundle = root / 'bundle.js'
            bundle.write_text('/* renderer */')
            output = root / 'out'
            slides.build(root, output, bundle)
            stale = output / 'ko/topic/demo/index.html'
            self.assertTrue(stale.is_file())
            (root / 'mkdocs.yml').write_text('nav:\n  - Home: index.md\n')
            for lang in ('ko', 'en'):
                (root / f'docs/{lang}/index.md').write_text(
                    f'---\nid: home\n---\n# Home\n\nPublic content.\n')
            slides.build(root, output, bundle)
            self.assertFalse(stale.exists())

    def test_numeric_range_activity_uses_only_explicit_source_values(self):
        raw = ('A reader can skip a range that cannot match.\n\n'
               '```text\nlatency_ms\nmin = 100\nmax = 500\n```\n\n'
               '```sql\nWHERE latency_ms > 1000\n```')
        activity = slides._interaction(raw, 'Statistics', 'en')
        self.assertEqual(activity['type'], 'parameter')
        self.assertEqual(activity['data'], {
            'field': 'latency_ms', 'minimum': 100, 'maximum': 500,
            'operator': '>', 'threshold': 1000})
        self.assertEqual(slides._interaction('min = 100\nmax = 500', 'Other', 'en')['type'], 'none')

    def test_markdown_links_in_deck_resolve_to_original_site(self):
        page = slides.Page('en', Path('topic/demo.md'), 'demo', 'Demo', ('Topic',))
        result = slides._safe_markdown('[peer](../peer.md#part) [here](#detail)', page)
        self.assertIn('href="/work-handbook/en/peer/#part"', result)
        self.assertIn('href="/work-handbook/en/topic/demo/#detail"', result)

    def test_no_automatic_activity_from_markdown_shape(self):
        samples = ['| A | B |\n|---|---|\n| one | two |\n| three | four |',
                   '- failure\n- recovery', '> **A definition**',
                   '```text\nInput\n↓\nProcess\n↓\nOutput\n```']
        for raw in samples:
            self.assertEqual(slides._interaction(raw, 'Example', 'en')['type'], 'none')

    def test_prompt_tabs_render_as_visible_structured_content(self):
        raw = '=== "English"\n\n    ```text {.prompt}\n    Review only.\n    ```'
        rendered = slides._safe_markdown(raw)
        self.assertNotIn('===', rendered)
        self.assertNotIn('```', rendered)
        self.assertIn('Review only.', rendered)
        self.assertNotIn('type="radio"', rendered)

    def test_reviewed_watermark_has_visible_example_and_limits_in_both_languages(self):
        root = Path(__file__).resolve().parents[1]
        for page in slides.discover(root, 'data-platform/flink.md'):
            schema = slides.build_schema(root, page)
            selected = [s for s in schema['slides'] if s['section_id'] == 'watermark']
            visible = ' '.join(s['body_html'] for s in selected)
            self.assertIn('10:01:05', visible)
            self.assertIn('10:01:03', visible)
            self.assertIn('idleness', visible.lower())
            self.assertTrue(all(s['design']['status'] == 'reviewed' for s in selected))
            self.assertFalse(any(s['interaction']['type'] in ('quiz', 'flashcard', 'practice') for s in schema['slides']))

    def test_qlora_flow_preserves_order_and_explains_training_without_controls(self):
        from bs4 import BeautifulSoup
        root = Path(__file__).resolve().parents[1]
        paired = []
        for page in slides.discover(root, 'ai-model-development/qlora-training.md'):
            deck = slides.build_schema(root, page)
            units = [s for s in deck['slides'] if s['section_id'] == 'qlora-flow']
            self.assertTrue(units, 'The reviewed QLoRA flow must replace the atomic text diagram')
            paired.append([s['unit_id'] for s in units])
            soup = BeautifulSoup(''.join(s['body_html'] for s in units), 'html.parser')
            self.assertIsNone(soup.find('pre'))
            self.assertIsNone(soup.find('button'))
            self.assertTrue(all(s['interaction']['type'] == 'none' for s in units))
            self.assertTrue(all(s['design']['status'] == 'reviewed' for s in units))
            flow = soup.get_text(' ', strip=True)
            nodes = (['문제 정의', 'Training Dataset 준비', 'Base Model 선택', '4-bit Quantization',
                      'LoRA Adapter 구성', 'Training', 'Validation', 'Adapter Artifact 저장',
                      'Golden Dataset Evaluation', 'Promote / Reject'] if page.language == 'ko' else
                     ['Define the problem', 'Prepare the Training Dataset', 'Select the Base Model',
                      '4-bit Quantization', 'Configure the LoRA Adapter', 'Training', 'Validation',
                      'Save the Adapter Artifact', 'Golden Dataset Evaluation', 'Promote / Reject'])
            # An independently specified directed edge set, not generated expected output.
            for left, right in zip(nodes, nodes[1:]):
                self.assertIn(left + ' → ' + right, flow)
            for term in ('Redis', 'Kafka', 'token', 'loss', 'adapter', 'base'):
                self.assertIn(term, flow.lower() if term.islower() else flow)
            self.assertIn('no_grad', flow)
            self.assertIn('4.14', flow)
        self.assertEqual(paired[0], paired[1])

    def test_qlora_supporting_source_change_requires_review(self):
        from scripts.slide_explanations import reviewed_design
        root = Path(__file__).resolve().parents[1]
        page = slides.discover(root, 'ai-model-development/qlora-training.md')[1]
        raw = (root / 'docs/en/ai-model-development/qlora-training.md').read_text()
        import re
        _, body, offset = slides._frontmatter(raw)
        section = next(s for s in slides._sections(body, offset) if s['heading'] == '4.1 Overall Training Flow')
        content = re.sub(r'^#{1,6}\s+[^\n]*\n?', '', '\n'.join(section['lines'])).strip()
        self.assertIsNotNone(reviewed_design(page.document_id, section['heading'], '', 'en', content, full_source=raw))
        self.assertIsNone(reviewed_design(page.document_id, section['heading'], '', 'en', content,
                                         full_source=raw.replace('not contain base model weights', 'contain base model weights')))

    def test_evaluation_types_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.fixture(root)
            schema = slides.build_schema(root, slides.discover(root)[0])
            for kind in ('quiz', 'flashcard', 'practice'):
                schema['slides'][0]['interaction'] = {'type': kind, 'data': {}, 'model_note': 'old'}
                with self.assertRaisesRegex(ValueError, 'unsupported interaction'):
                    slides.validate_schema(schema)

    def test_representatives_have_stable_bilingual_unit_ids(self):
        root = Path(__file__).resolve().parents[1]
        for path, section in [('aws-cloud/networking.md', 'sg-nacl'),
                              ('data-platform/production-operations.md', 'schema-break'),
                              ('english-study/vocabulary.md', 'vocab-check'),
                              ('prompts/flink.md', 'flink-01')]:
            decks = [slides.build_schema(root, page) for page in slides.discover(root, path)]
            units = [[s['unit_id'] for s in deck['slides'] if s['section_id'] == section] for deck in decks]
            self.assertTrue(units[0])
            self.assertEqual(set(units[0]), set(units[1]))

    def test_review_fallback_keeps_bilingual_section_identity(self):
        from unittest.mock import patch
        root = Path(__file__).resolve().parents[1]
        cases = [('data-platform/flink.md', 'watermark'),
                 ('aws-cloud/networking.md', 'sg-nacl'),
                 ('data-platform/production-operations.md', 'schema-break'),
                 ('ai-model-development/qlora-training.md', 'qlora-flow')]
        for path, expected in cases:
            for page in slides.discover(root, path):
                reviewed = slides.build_schema(root, page)
                heading = next(s['source']['heading'] for s in reviewed['slides'] if s['section_id'] == expected)
                with patch.object(slides, 'reviewed_design', return_value=None):
                    fallback = slides.build_schema(root, page)
                actual = next(s for s in fallback['slides'] if s['source']['heading'] == heading)
                self.assertEqual(actual['section_id'], expected, (path, page.language))
                self.assertEqual(actual['design']['status'], 'static-source')

    def test_changed_source_requires_new_semantic_review(self):
        from scripts.slide_explanations import reviewed_design
        self.assertIsNone(reviewed_design('data-platform-flink', '5.5 Watermark', '', 'en',
                                         'Changed watermark assumption.'))

    def test_registry_does_not_depend_on_current_slide_count(self):
        root = Path(__file__).resolve().parents[1]
        pages = slides.discover(root, 'data-platform/flink.md')
        for page in pages:
            deck = slides.build_schema(root, page)
            self.assertTrue(all(s['position_mapping'] == 'paired' for s in deck['slides']))
            self.assertEqual(len({s['unit_id'] for s in deck['slides']}), len(deck['slides']))

    def test_reviewed_prompt_has_readable_semantic_segments_not_atomic_pre(self):
        from bs4 import BeautifulSoup
        root = Path(__file__).resolve().parents[1]
        for page in slides.discover(root, 'prompts/flink.md'):
            deck = slides.build_schema(root, page)
            units = [s for s in deck['slides'] if s['section_id'] == 'flink-01']
            html = ''.join(s['body_html'] for s in units)
            soup = BeautifulSoup(html, 'html.parser')
            self.assertIsNone(soup.find('pre'))
            self.assertIn('Review only; do not apply changes.', soup.get_text())
            self.assertIn('검토만 하고 변경은 실행하지 마.', soup.get_text())
            self.assertIn('Return window membership and expected results for each sample, plus late-event policy questions.', soup.get_text())
            self.assertIn('표본별 window 소속과 기대 결과, 늦은 이벤트 정책 질문을 작성해 줘.', soup.get_text())
            self.assertEqual(len([s for s in units if ':request-' in s['unit_id']]), 4)
            self.assertIn('10:00:20', soup.get_text())
            self.assertIn('[10:00, 10:01)', soup.get_text())

    def test_source_anchor_matches_duplicate_and_formatted_markdown_headings(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.fixture(root)
            for lang in ('ko', 'en'):
                (root / f'docs/{lang}/topic/demo.md').write_text(
                    '---\nid: demo\n---\n# Demo\n\n## **Same** heading\n\nFirst.\n\n## **Same** heading\n\nSecond.\n')
            schema = slides.build_schema(root, slides.discover(root)[1])
            self.assertEqual([s['source']['url'] for s in schema['slides']],
                             ['/work-handbook/en/topic/demo/#same-heading',
                              '/work-handbook/en/topic/demo/#same-heading_1'])

    def test_table_headers_and_links_survive(self):
        rendered = slides._safe_markdown('| Item | SG | NACL |\n|---|---|---|\n| Stateful | O | X |\n| Link | [01](#a) | [02](#b) |')
        self.assertIn('<th>SG</th>', rendered)
        self.assertIn('<th>NACL</th>', rendered)
        self.assertIn('href="#a"', rendered)


if __name__ == '__main__':
    unittest.main()
