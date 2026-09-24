import importlib.util
from pathlib import Path
import tempfile
import unittest

MODULE = Path(__file__).resolve().parents[1] / 'scripts' / 'check_site.py'
class SiteTests(unittest.TestCase):
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
