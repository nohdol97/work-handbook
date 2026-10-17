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
            self.assertTrue(all(s['objective'] and s['notes_html'] for s in schema['slides']))
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
                lambda raw, heading, language: {'type': 'scenario',
                    'data': {'items': [{'label': 'input', 'detail': 'First input.'}]},
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

    def test_schema_rejects_invalid_quiz_answer(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.fixture(root)
            schema = slides.build_schema(root, slides.discover(root)[0])
            schema['slides'][0]['interaction'] = {
                'type': 'quiz', 'data': {'question': 'Q', 'options': ['A'], 'correctIndex': 4},
                'model_note': 'source'}
            with self.assertRaisesRegex(ValueError, 'quiz'):
                slides.validate_schema(schema)

    def test_linear_source_diagram_explains_neighboring_states(self):
        activity = slides._interaction('```text\nInput\n↓\nProcess\n↓\nOutput\n```', 'Flow', 'en')
        self.assertEqual(activity['type'], 'architecture')
        self.assertIn('Input', activity['data']['items'][1]['detail'])
        self.assertIn('Output', activity['data']['items'][1]['detail'])
        self.assertEqual(slides._plain('4-bit Quantization'), '4-bit Quantization')


if __name__ == '__main__':
    unittest.main()
