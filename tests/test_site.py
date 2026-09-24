import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

MODULE = Path(__file__).resolve().parents[1] / 'scripts' / 'check_site.py'
class SiteTests(unittest.TestCase):
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
