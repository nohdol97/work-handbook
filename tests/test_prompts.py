"""Exercise prompt rendering with the site's actual Markdown configuration."""
import importlib.util
from pathlib import Path
import unittest
import tempfile

from bs4 import BeautifulSoup
import markdown

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('handbook_config', ROOT / 'scripts/check_handbook.py')
handbook = importlib.util.module_from_spec(spec)
spec.loader.exec_module(handbook)


def render(text):
    errors = []
    config = handbook._load_yaml(ROOT / 'mkdocs.yml', errors)
    if errors:
        raise AssertionError(errors)
    extensions, options = [], {}
    for item in config['markdown_extensions']:
        if isinstance(item, str):
            extensions.append(item)
        else:
            for name, settings in item.items():
                extensions.append(name)
                # This fixture has no Mermaid; do not execute named YAML callables.
                options[name] = {k: v for k, v in (settings or {}).items() if k != 'custom_fences'}
    return BeautifulSoup(markdown.markdown(text, extensions=extensions,
                                          extension_configs=options), 'html.parser')


class PromptRenderingTests(unittest.TestCase):
    def test_language_tabs_keep_prompt_lines_and_literal_placeholders(self):
        source = '''=== "한국어"

    ```text {.prompt}
    [맥락]
    SQL: [익명화 SQL]
    [요청]
    관찰과 가설을 구분해 주세요.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    SQL: [sanitized SQL]
    [Task]
    Separate observations from hypotheses.
    ```
'''
        soup = render(source)
        tabs = soup.select('.tabbed-set')
        self.assertEqual(len(tabs), 1, 'prompts must render as one language tab group')
        labels = [x.get_text(strip=True) for x in tabs[0].select('.tabbed-labels label')]
        self.assertEqual(labels, ['한국어', 'English'])
        codes = tabs[0].select('.tabbed-block .prompt pre code')
        self.assertEqual(len(codes), 2)
        self.assertEqual(codes[0].get_text(), '[맥락]\nSQL: [익명화 SQL]\n[요청]\n관찰과 가설을 구분해 주세요.\n')
        self.assertEqual(codes[1].get_text(), '[Context]\nSQL: [sanitized SQL]\n[Task]\nSeparate observations from hypotheses.\n')

    def test_regular_code_is_not_marked_as_a_prompt(self):
        soup = render('```sql\nSELECT a, b FROM example;\n```')
        self.assertIsNone(soup.select_one('.prompt'))
        self.assertIn('SELECT a, b FROM example;', soup.get_text())


class PromptAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        audit_spec = importlib.util.spec_from_file_location('prompt_audit', ROOT / 'scripts/check_prompts.py')
        cls.audit = importlib.util.module_from_spec(audit_spec)
        audit_spec.loader.exec_module(cls.audit)

    def group(self, ko='[맥락]\n입력\n[요청]\n비교\n[출력]\n표\n[검증]\n근거', en='[Context]\nInput\n[Task]\nCompare\n[Output]\nTable\n[Checks]\nEvidence'):
        return '<div class="tabbed-set"><div class="tabbed-labels"><label>한국어</label><label>English</label></div><div class="tabbed-content">' + ''.join(
            '<div class="tabbed-block"><div class="prompt"><pre><code>' + text + '</code></pre></div></div>' for text in [ko, en]) + '</div></div>'

    def test_rejects_single_line_prompt(self):
        errors, _ = self.audit.inspect_html(self.group(en='Review everything in one long line.'))
        self.assertTrue(any('multiline' in e for e in errors))

    def test_rejects_missing_language(self):
        errors, _ = self.audit.inspect_html(self.group().replace('<label>English</label>', ''))
        self.assertTrue(any('language' in e for e in errors))

    def test_compares_translations_independently_of_tab_order(self):
        errors, groups = self.audit.inspect_html(self.group())
        self.assertEqual(errors, [])
        self.assertEqual(set(groups[0]), {'한국어', 'English'})
        self.assertIn('[맥락]', groups[0]['한국어'])
        self.assertIn('[Task]', groups[0]['English'])
        soup = BeautifulSoup(self.group(), 'html.parser')
        for selector in ['.tabbed-labels', '.tabbed-content']:
            parent = soup.select_one(selector)
            children = list(parent.children)
            for child in reversed(children):
                parent.append(child.extract())
        reverse_errors, reversed_groups = self.audit.inspect_html(str(soup))
        self.assertEqual(reverse_errors, [])
        self.assertEqual(reversed_groups, groups)

    def test_rejects_missing_task_output_and_checks(self):
        errors, _ = self.audit.inspect_html(self.group(en='[Context]\nInput\nMore input\nMore context'))
        self.assertTrue(any('section' in e for e in errors))

    def test_rejects_wrong_language_section_markers(self):
        errors, _ = self.audit.inspect_html(self.group(en='[맥락]\nInput\n[Task]\nCompare\n[Output]\nTable\n[Checks]\nEvidence'))
        self.assertTrue(any('section' in e for e in errors))

    def test_rejects_empty_or_reordered_sections(self):
        for en in ['[Context]\nInput\n[Task]\n[Output]\nTable\n[Checks]\nEvidence',
                   '[Task]\nCompare\n[Context]\nInput\n[Output]\nTable\n[Checks]\nEvidence']:
            with self.subTest(en=en):
                errors, _ = self.audit.inspect_html(self.group(en=en))
                self.assertTrue(any('section' in e for e in errors))

    def test_audit_detects_prompt_drift_between_localized_pages(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / 'docs/ko/prompts/example.md'
            source.parent.mkdir(parents=True)
            source.write_text('# Example')
            for prefix, html in [('', self.group()), ('en/', self.group().replace('Evidence', 'Different evidence'))]:
                page = root / f'site/{prefix}prompts/example/index.html'
                page.parent.mkdir(parents=True)
                page.write_text(html)
            errors, _, _ = self.audit.audit(root)
            self.assertTrue(any('translations differ' in e for e in errors))


if __name__ == '__main__':
    unittest.main()
