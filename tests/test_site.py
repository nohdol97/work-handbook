import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

MODULE = Path(__file__).resolve().parents[1] / 'scripts' / 'check_site.py'
class SiteTests(unittest.TestCase):
    def audit_bilingual_fixture(self, ko_content, en_content):
        spec = importlib.util.spec_from_file_location('sitecheck', MODULE)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root/'docs/ko').mkdir(parents=True)
            (root/'docs/ko/index.md').write_text('# 홈')
            (root/'site/en').mkdir(parents=True)
            (root/'site/index.html').write_text(
                '<a hreflang="en" href="en/">English</a>' + ko_content)
            (root/'site/en/index.html').write_text(
                '<a hreflang="ko" href="../">한국어</a>' + en_content)
            return module.audit_site(root)

    def test_bilingual_heading_order_or_count_mismatch_fails(self):
        ko = '<article class="md-content__inner"><h1>제목</h1><h2>절</h2><h3>하위</h3></article>'
        for headings in ('<h1>Title</h1><h3>Subsection</h3><h2>Section</h2>',
                         '<h1>Title</h1><h2>Section</h2>'):
            with self.subTest(headings=headings):
                errors = self.audit_bilingual_fixture(
                    ko, '<article class="md-content__inner">' + headings + '</article>')
                self.assertTrue(any('heading structure' in error for error in errors), errors)

    def test_translated_heading_ids_and_tab_panel_headings_pass(self):
        ko = ('<h4>Navigation</h4><article class="md-content__inner">'
              '<h1 id="home">홈</h1><h2 id="section">절</h2>'
              '<div class="tabbed-content"><h3>탭 제목</h3></div></article>')
        en = ('<h5>Navigation</h5><article class="md-content__inner">'
              '<h1 id="title">Home</h1><h2 id="translated">Section</h2>'
              '<div class="tabbed-content"><h4>Tab title</h4></div></article>')
        self.assertEqual(self.audit_bilingual_fixture(ko, en), [])

    def test_missing_bilingual_article_fails(self):
        article = '<article class="md-content__inner"><h1>Title</h1></article>'
        for ko, en in ((article, '<main><h1>Title</h1></main>'),
                       ('<main><h1>제목</h1></main>', article)):
            with self.subTest(ko=ko):
                errors = self.audit_bilingual_fixture(ko, en)
                self.assertTrue(any('missing article' in error for error in errors), errors)

    def test_shared_target_is_parsed_once_per_link_audit(self):
        spec = importlib.util.spec_from_file_location('sitecheck', MODULE)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root/'index.html').write_text('<a href="topic.html#a">A</a><a href="topic.html#b">B</a>')
            (root/'other.html').write_text('<a href="topic.html#a">Again</a>')
            (root/'topic.html').write_text('<h2 id="a">A</h2><h2 id="b">B</h2>')
            with patch.object(module, 'BeautifulSoup', wraps=module.BeautifulSoup) as parser:
                self.assertEqual(module.audit_links(root), [])
                self.assertLessEqual(parser.call_count, 3)

    def test_broken_local_link_fails(self):
        self.assertTrue(MODULE.exists(), 'site checker is missing')
        spec = importlib.util.spec_from_file_location('sitecheck', MODULE)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root/'index.html').write_text('<a href="missing/">broken</a>')
            self.assertTrue(any('missing' in e for e in module.audit_links(root)))

    def test_missing_fragment_fails(self):
        self.assertTrue(MODULE.exists(), 'site checker is missing')
        spec = importlib.util.spec_from_file_location('sitecheck', MODULE)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root/'index.html').write_text('<a href="#lost">broken</a>')
            self.assertTrue(any('fragment' in e for e in module.audit_links(root)))
