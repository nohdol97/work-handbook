from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]


class ThemeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.output = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.output.cleanup)
        result = subprocess.run(
            [sys.executable, '-m', 'mkdocs', 'build', '--strict',
             '--config-file', str(ROOT / 'mkdocs.yml'),
             '--site-dir', cls.output.name],
            cwd=ROOT, capture_output=True, text=True,
        )
        if result.returncode:
            raise AssertionError(result.stdout + result.stderr)

    def test_bilingual_home_and_document_offer_connected_theme_controls(self):
        for page in ('index.html', 'en/index.html',
                     'data-platform/ai-evaluation/index.html',
                     'en/data-platform/ai-evaluation/index.html'):
            with self.subTest(page=page):
                soup = BeautifulSoup(
                    (Path(self.output.name) / page).read_text(), 'html.parser',
                )
                palette = soup.select_one('[data-md-component="palette"]')
                self.assertIsNotNone(palette, 'Site header needs a theme selector')
                options = palette.select('input[type="radio"]')
                self.assertEqual(len(options), 3, 'Need system, light and dark modes')
                self.assertEqual(
                    [option.get('data-md-color-media') for option in options],
                    ['(prefers-color-scheme)', '(prefers-color-scheme: light)',
                     '(prefers-color-scheme: dark)'],
                    'System preference must be the first-visit default',
                )
                self.assertEqual(options[1]['data-md-color-scheme'], 'default')
                self.assertEqual(options[2]['data-md-color-scheme'], 'slate')
                labels = palette.select('label')
                self.assertEqual(len(labels), 3)
                for index, (option, label) in enumerate(zip(options, labels)):
                    self.assertTrue(option.get('aria-label', '').strip())
                    self.assertEqual(label['title'], option['aria-label'])
                    self.assertEqual(label['for'], options[(index + 1) % 3]['id'])
                    self.assertIsNotNone(label.select_one('svg'), 'Visible toggle icon')

    def test_language_runtime_and_floating_styles_are_loaded_in_both_languages(self):
        for page in ('index.html', 'en/index.html', 'data-platform/foundations/index.html', 'en/data-platform/foundations/index.html'):
            with self.subTest(page=page):
                soup = BeautifulSoup((Path(self.output.name) / page).read_text(), 'html.parser')
                scripts = [item['src'] for item in soup.select('script[src]')]
                for name in ('reading-position.js', 'language-button.js'):
                    self.assertTrue(any(src.endswith('/' + name) for src in scripts), name)
                self.assertTrue(any(item['href'].endswith('/language-button.css') for item in soup.select('link[rel="stylesheet"]')))
