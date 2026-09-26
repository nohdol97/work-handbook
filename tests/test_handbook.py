import importlib.util
import tempfile
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location('check_handbook', Path(__file__).parents[1] / 'scripts/check_handbook.py')
checker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(checker)

class HandbookTests(unittest.TestCase):
    def test_missing_counterpart_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'docs/ko').mkdir(parents=True)
            (root / 'docs/ko/index.md').write_text('# Test\n')
            self.assertTrue(any('counterpart' in error for error in checker.audit(root)))

class ValidFixtureTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.write_pair('index.md', 'handbook-home')
        self.write('mkdocs.yml', 'nav:\n  - Home: index.md\n')
        self.reviews()

    def write(self, relative, text):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')
        return path

    def write_pair(self, relative, page_id, extra=''):
        for lang in ['ko', 'en']:
            self.write(f'docs/{lang}/{relative}', f'---\nid: {page_id}\nstatus: overview\nlast_reviewed: 2026-09-24\nknowledge_ids: []\n---\n# Handbook\n\nStart here.\n{extra}')

    def reviews(self):
        import hashlib
        import json
        pages = {}
        for path in (self.root / 'docs/ko').rglob('*.md'):
            relative = path.relative_to(self.root / 'docs/ko').as_posix()
            pages[relative] = {'semantic': 'pass', 'simple_english': 'pass', 'privacy': 'pass', 'reviewer': 'fixture review'}
            for lang in ['ko', 'en']:
                counterpart = self.root / 'docs' / lang / relative
                if counterpart.exists():
                    pages[relative][lang + '_sha256'] = hashlib.sha256(counterpart.read_bytes()).hexdigest()
        self.write('reviews/bilingual.json', json.dumps({'pages': pages}))

    def assert_error(self, expected):
        errors = checker.audit(self.root)
        self.assertTrue(any(expected in error for error in errors), errors)

    def source(self, state='Included', destination='index.md', reason='', ko='Synced', en='Synced'):
        import yaml
        self.write('sources/study/source.md', '# Source\nOne concept.\n')
        self.write('sources/study/mapping.md', '# Mapping\nOne concept to index.\n')
        manifest = {'items': [{'id': 'CONCEPT-001', 'knowledge': 'One concept', 'kind': 'concept'}]}
        matrix = {'items': [{'id': 'CONCEPT-001', 'state': state, 'destination': destination, 'reason': reason, 'ko': ko, 'en': en}]}
        for name, data in [('content-manifest', manifest), ('coverage-matrix', matrix)]:
            self.write(f'sources/study/{name}.md', '---\n' + yaml.safe_dump(data) + '---\n# Items\n')
        checker.write_reports(self.root)
        if state in {'Included', 'Merged'}:
            for lang in ['ko', 'en']:
                path = self.root / 'docs' / lang / 'index.md'
                path.write_text(path.read_text().replace('knowledge_ids: []', 'knowledge_ids: [CONCEPT-001]'))
        self.reviews()

    def test_valid_minimal_handbook(self):
        self.assertEqual(checker.audit(self.root), [])

    def test_stale_review_detects_unreviewed_page_change(self):
        path = self.root / 'docs/en/index.md'
        path.write_text(path.read_text() + '\nNew warning.\n')
        self.assert_error('stale en review hash')

    def test_duplicate_canonical_id(self):
        self.write_pair('other.md', 'handbook-home')
        self.reviews()
        self.assert_error('duplicate canonical ID')

    def test_valid_local_anchor(self):
        self.write_pair('index.md', 'handbook-home', '[Top](#handbook)\n')
        self.reviews()
        self.assertEqual(checker.audit(self.root), [])

    def test_missing_file_and_anchor_and_cross_language_links(self):
        for target, error in [('missing.md', 'broken local link'), ('#absent', 'broken anchor'), ('../en/index.md', 'leaves language tree'), ('../../../escape.md', 'escapes repository')]:
            with self.subTest(target=target):
                self.write_pair('index.md', 'handbook-home', f'[Reference]({target})\n')
                self.reviews()
                self.assert_error(error)

    def test_code_example_links_are_not_checked_as_prose(self):
        self.write_pair('index.md', 'handbook-home', '```markdown\n[Demo](missing.md)\n```\n')
        self.reviews()
        self.assertEqual(checker.audit(self.root), [])

    def test_navigation_orphan_and_missing_target(self):
        self.write('mkdocs.yml', 'nav:\n  - Missing: missing.md\n')
        self.assert_error('orphan page')
        self.assert_error('navigation references missing page')

    def test_metadata_validity_and_equivalence(self):
        for original, replacement, expected in [('status: overview', 'status: invented', 'invalid status'), ('last_reviewed: 2026-09-24', 'last_reviewed: invalid', 'invalid last_reviewed'), ('id: handbook-home', 'id: Other', 'invalid canonical id'), ('knowledge_ids: []', 'knowledge_ids: [A]', 'paired knowledge_ids differ')]:
            with self.subTest(expected=expected):
                self.write_pair('index.md', 'handbook-home')
                path = self.root / 'docs/ko/index.md'
                path.write_text(path.read_text().replace(original, replacement))
                self.reviews()
                self.assert_error(expected)

    def test_empty_heading(self):
        self.write_pair('index.md', 'handbook-home', '\n## \n')
        self.reviews()
        self.assert_error('empty heading')

    def test_complete_source_tracking(self):
        self.source()
        self.assertEqual(checker.audit(self.root), [])

    def test_missing_matrix_item(self):
        self.source()
        self.write('sources/study/coverage-matrix.md', '---\nitems: []\n---\n# Coverage\n')
        self.assert_error('manifest/matrix IDs differ')

    def test_source_destination_requires_knowledge_id(self):
        self.source()
        path = self.root / 'docs/en/index.md'
        path.write_text(path.read_text().replace('[CONCEPT-001]', '[]'))
        self.reviews()
        self.assert_error('missing knowledge ID in en')

    def test_deferred_requires_reason_and_no_publication_claim(self):
        self.source('Deferred')
        self.assert_error('requires reason')
        self.assert_error('unpublished item claims publication')

    def test_accounted_is_distinct_from_published(self):
        self.source('Deferred', '', 'Needs a safe public example', 'Pending', 'Pending')
        self.assertEqual(checker.audit(self.root), [])
        checker.write_reports(self.root)
        report = (self.root / 'sources/study/coverage-report.md').read_text()
        self.assertIn('Accounted knowledge: 1 / 1 (100.0%)', report)
        self.assertIn('Published knowledge: 0 / 1', report)

    def test_empty_source_does_not_claim_full_coverage(self):
        self.source()
        for name in ['content-manifest', 'coverage-matrix']:
            self.write(f'sources/study/{name}.md', '---\nitems: []\n---\n# Empty\n')
        checker.write_reports(self.root)
        report = (self.root / 'sources/study/coverage-report.md').read_text()
        self.assertIn('N/A (no source items)', report)
        self.assertNotIn('100%', report)

    def test_reviews_cannot_claim_pass_without_all_three_reviews(self):
        import json
        path = self.root / 'reviews/bilingual.json'
        data = json.loads(path.read_text())
        data['pages']['index.md']['privacy'] = 'pending'
        path.write_text(json.dumps(data))
        self.assert_error('privacy review must pass')

    def test_malformed_metadata_is_error_not_exception(self):
        path = self.root / 'docs/ko/index.md'
        path.write_text(path.read_text().replace('status: overview', 'status: [overview]'))
        self.assert_error('invalid status')

    def test_malformed_matrix_state_is_error_not_exception(self):
        self.source()
        path = self.root / 'sources/study/coverage-matrix.md'
        path.write_text(path.read_text().replace('state: Included', 'state: [Included]'))
        self.assert_error('invalid state')

    def test_source_only_knowledge_cannot_be_marked_as_published_page_knowledge(self):
        self.source('Deferred', '', 'Private example requires redaction', 'Pending', 'Pending')
        for lang in ['ko', 'en']:
            path = self.root / 'docs' / lang / 'index.md'
            path.write_text(path.read_text().replace('knowledge_ids: []', 'knowledge_ids: [CONCEPT-001]'))
        self.reviews()
        self.assert_error('knowledge ID is not mapped to this published page')

    def test_mkdocs_callable_tag_is_read_as_inert_data(self):
        self.write('mkdocs.yml', 'nav:\n  - Home: index.md\nmarkdown_extensions:\n  - pymdownx.superfences:\n      custom_fences:\n        - name: mermaid\n          format: !!python/name:pymdownx.superfences.fence_code_format\n')
        self.assertEqual(checker.audit(self.root), [])

    def test_stale_coverage_report_fails_until_regenerated(self):
        self.source()
        self.write('sources/study/coverage-report.md', '# Report\nPublished knowledge: 999 / 999\n')
        self.assert_error('stale coverage report')
        checker.write_reports(self.root)
        self.assertEqual(checker.audit(self.root), [])

    def test_report_separates_bilingual_sync_from_semantic_review(self):
        self.source()
        report = (self.root / 'sources/study/coverage-report.md').read_text()
        self.assertIn('Bilingual synchronization: 1 / 1 (100.0%)', report)
        self.assertIn('실제 의미·개인정보 검토가 별도로 필요하다', report)
        self.source('Deferred', '', 'Needs redaction', 'Pending', 'Pending')
        report = (self.root / 'sources/study/coverage-report.md').read_text()
        self.assertIn('Bilingual synchronization: 0 / 0 (N/A (no published items))', report)

    def normalized_source(self, ledger=None):
        import hashlib
        import json
        self.source()
        raw = '원문  \r\nsecond\t\n'.encode()
        if ledger is None:
            ledger = [{'line': 1, 'removed': '  '}, {'line': 2, 'removed': '\t'}]
        header = ('<!-- 반입 기록\n원본 bytes: ' + str(len(raw)) + '; SHA-256: ' + hashlib.sha256(raw).hexdigest()
                  + '\nwhitespace_restoration: ' + json.dumps(ledger) + '\n-->\n<!-- ORIGINAL SOURCE START -->\n')
        path = self.root / 'sources/study/source.md'
        path.write_bytes(header.encode() + '원문\r\nsecond\n'.encode())
        return path

    def test_restored_source_bytes_match_recorded_upload(self):
        self.normalized_source()
        self.assertEqual(checker.audit(self.root), [])

    def test_source_content_drift_with_same_byte_length_is_rejected(self):
        path = self.normalized_source()
        path.write_bytes(path.read_bytes().replace(b'second', b'edited'))
        self.assert_error('source integrity')

    def test_invalid_source_restoration_ledger_is_rejected(self):
        for ledger in [[{'line': 99, 'removed': ' '}],
                       [{'line': True, 'removed': ' '}],
                       [{'line': 1, 'removed': 'x'}],
                       [{'line': 1, 'removed': ' '}, {'line': 1, 'removed': ' '}]]:
            with self.subTest(ledger=ledger):
                self.normalized_source(ledger)
                self.assert_error('source integrity')

    def test_incomplete_source_integrity_record_is_rejected(self):
        path = self.normalized_source()
        path.write_bytes(path.read_bytes().replace(b'whitespace_restoration:', b'missing_ledger:'))
        self.assert_error('source integrity')

    def test_duplicate_source_integrity_metadata_is_rejected(self):
        for extra in ['whitespace_restoration: INVALID_JSON',
                      '원본 bytes: 0; SHA-256: ' + '0' * 64]:
            with self.subTest(extra=extra):
                path = self.normalized_source()
                path.write_bytes(path.read_bytes().replace(b'-->\n', extra.encode() + b'\n-->\n', 1))
                self.assert_error('source integrity')
