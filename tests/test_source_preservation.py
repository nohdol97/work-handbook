import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location('preservation', Path(__file__).parents[1] / 'scripts/check_source_preservation.py')
checker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(checker)


class PreservationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.core = '## 6.1 Definition\n\nOriginal paragraph.\n\n### Example\n\n- one\n- two\n\n```text\n## 99.1 not a heading\n```\n\n## 6.2 Ordering\n\nKeep order.\n\n---'
        self.write('sources/study/source.md', '# Chapter 6\n\n' + self.core + '\n\n# Chapter 7\n')
        self.record = {'page': 'topic.md', 'source': 'sources/study/source.md', 'start': '# Chapter 6', 'end': '# Chapter 7', 'verbatim_language': 'ko'}
        self.config()
        self.pair(self.core)

    def write(self, path, text):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text)

    def config(self, records=None):
        self.write('reviews/source-preservation.json', json.dumps({'spans': records if records is not None else [self.record]}))

    def pair(self, core, lang=None):
        for language in ([lang] if lang else ['ko', 'en']):
            self.write(f'docs/{language}/topic.md', '# Topic\n\n<!-- SOURCE CORE START -->\n\n' + core + '\n\n<!-- SOURCE CORE END -->\n\n## Supplements\n\nAdditional explanation.\n')

    def test_preserved_source_and_translated_structure_pass(self):
        self.pair(self.core.replace('Original paragraph.', 'Translated paragraph.'), 'en')
        self.assertEqual(checker.audit(self.root), [])

    def test_source_rewriting_fails_even_with_all_numbers_present(self):
        self.pair(self.core.replace('Original paragraph.', 'Shortened summary.'), 'ko')
        self.assertTrue(any('verbatim' in x for x in checker.audit(self.root)))

    def test_translated_prose_omission_fails_with_all_numbers_present(self):
        self.pair(self.core.replace('Original paragraph.', ''), 'en')
        self.assertTrue(any('structure' in x for x in checker.audit(self.root)))

    def test_translated_paragraph_merging_fails(self):
        expanded = self.core.replace('Original paragraph.', 'First paragraph.\n\nSecond paragraph.')
        self.write('sources/study/source.md', '# Chapter 6\n\n' + expanded + '\n\n# Chapter 7\n')
        self.pair(expanded)
        self.pair(expanded.replace('First paragraph.\n\nSecond paragraph.', 'First and second merged.'), 'en')
        self.assertTrue(any('structure' in x for x in checker.audit(self.root)))

    def test_missing_or_reordered_numbered_sections_fail(self):
        for text in [self.core.replace('## 6.2 Ordering', 'Ordering'), self.core.replace('6.1 Definition', '6.2 Definition').replace('6.2 Ordering', '6.1 Ordering')]:
            with self.subTest(text=text):
                self.pair(text, 'en')
                self.assertTrue(any('structure' in x for x in checker.audit(self.root)))

    def test_replacing_original_text_diagram_with_mermaid_fails(self):
        self.pair(self.core.replace('```text', '```mermaid'), 'en')
        self.assertTrue(any('structure' in x for x in checker.audit(self.root)))

    def test_compressing_translated_text_diagram_fails(self):
        self.core = self.core.replace('## 99.1 not a heading', 'A\n  ↓\nB')
        self.write('sources/study/source.md', '# Chapter 6\n\n' + self.core + '\n\n# Chapter 7\n')
        self.pair(self.core)
        self.pair(self.core.replace('A\n  ↓\nB', 'A → B'), 'en')
        self.assertTrue(any('structure' in x for x in checker.audit(self.root)))

    def test_missing_and_duplicate_core_markers_fail(self):
        for value in ['# Topic\n', '<!-- SOURCE CORE START -->\n<!-- SOURCE CORE START -->\n<!-- SOURCE CORE END -->']:
            self.write('docs/en/topic.md', value)
            self.assertTrue(any('boundary' in x for x in checker.audit(self.root)))

    def test_invalid_or_ambiguous_source_boundary_fails(self):
        self.record['start'] = '# Absent'
        self.config()
        self.assertTrue(checker.audit(self.root))
        self.record['start'] = '# Chapter 6'
        self.config()
        self.write('sources/study/source.md', '# Chapter 6\n# Chapter 6\n# Chapter 7\n')
        self.assertTrue(checker.audit(self.root))

    def test_paths_cannot_escape_expected_roots(self):
        for field, value in [('source', '../outside.md'), ('page', '../outside.md'), ('source', 'docs/ko/topic.md')]:
            with self.subTest(field=field):
                record = {**self.record, field: value}
                self.config([record])
                self.assertTrue(checker.audit(self.root))

    def test_malformed_or_duplicate_records_fail(self):
        for records in [[self.record, self.record], [None], [], 'invalid']:
            self.config(records)
            self.assertTrue(checker.audit(self.root))

    def test_english_original_supported(self):
        self.record['verbatim_language'] = 'en'
        self.config()
        self.pair(self.core.replace('Original paragraph.', '번역 문단.'), 'ko')
        self.assertEqual(checker.audit(self.root), [])

    def test_final_source_span_can_end_at_eof(self):
        self.record['end'] = None
        self.config()
        self.write('sources/study/source.md', '# Chapter 6\n\n' + self.core + '\n')
        self.assertEqual(checker.audit(self.root), [])

    def test_extra_source_span_uses_distinct_markers(self):
        second = {**self.record, 'marker': 'SOURCE APPENDIX'}
        self.config([self.record, second])
        for lang in ['ko', 'en']:
            path = self.root / f'docs/{lang}/topic.md'
            path.write_text(path.read_text() + '\n<!-- SOURCE APPENDIX START -->\n' + self.core + '\n<!-- SOURCE APPENDIX END -->\n')
        self.assertEqual(checker.audit(self.root), [])

    def test_list_table_and_separator_removal_fail(self):
        for before, after in [('- one\n- two', 'one and two'), ('\n---', '')]:
            self.pair(self.core.replace(before, after), 'en')
            self.assertTrue(any('structure' in x for x in checker.audit(self.root)))

    def test_table_column_loss_fails(self):
        table = '\n\n| A | B |\n|---|---|\n| One | Two |'
        self.core += table
        self.write('sources/study/source.md', '# Chapter 6\n\n' + self.core + '\n\n# Chapter 7\n')
        self.pair(self.core)
        self.pair(self.core.replace('| One | Two |', '| One |'), 'en')
        self.assertTrue(any('structure' in x for x in checker.audit(self.root)))


if __name__ == '__main__':
    unittest.main()
