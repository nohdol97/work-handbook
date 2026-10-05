"""Use the actual MkDocs hook and site Markdown renderer for source lists."""
import importlib.util
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest

from mkdocs.structure.files import File
from test_prompts import render

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('source_markdown', ROOT / 'scripts/source_markdown.py')
hook = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(hook)


class SourceMarkdownTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'reviews').mkdir()
        (self.root / 'reviews/source-preservation.json').write_text(json.dumps({'spans': [
            {'page': 'topic.md', 'marker': 'SOURCE CORE'},
            {'page': 'topic.md', 'marker': 'SOURCE INTRO'},
        ]}))
        self.config = {'docs_dir': str(self.root / 'docs')}

    def apply(self, text, language='ko', name='topic.md'):
        path = self.root / 'docs' / language / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(text.encode())
        file = File(f'{language}/{name}', self.config['docs_dir'], str(self.root / 'site'), True)
        output = hook.on_page_markdown(text, page=SimpleNamespace(file=file), config=self.config, files=[])
        self.assertEqual(path.read_bytes(), text.encode(), 'canonical file bytes must not change')
        return output

    def core(self, body, marker='SOURCE CORE'):
        return f'<!-- {marker} START -->\n\n{body}\n\n<!-- {marker} END -->\n'

    def test_adjacent_source_lists_render_as_lists_in_both_languages(self):
        for lang, label in [('ko', '대표 용도:'), ('en', 'Common uses:')]:
            with self.subTest(language=lang):
                source = self.core(f'{label}\n- LLM Inference\n- Model Training\n\nCompleted:\n1. Chapter 1\n2. Chapter 2')
                soup = render(self.apply(source, language=lang))
                self.assertEqual([x.get_text() for x in soup.select('ul > li')], ['LLM Inference', 'Model Training'])
                self.assertEqual([x.get_text() for x in soup.select('ol > li')], ['Chapter 1', 'Chapter 2'])

    def test_blockquote_lists_render_without_losing_the_quote(self):
        source = self.core('> 원칙:\n> - 원문 보존\n> - 보완 분리', 'SOURCE INTRO')
        soup = render(self.apply(source))
        self.assertEqual([x.get_text() for x in soup.select('blockquote ul > li')], ['원문 보존', '보완 분리'])
        self.assertIn('원칙:', soup.select_one('blockquote').get_text())

    def test_fenced_code_and_fake_markers_remain_literal(self):
        for fence in ['```', '~~~~']:
            with self.subTest(fence=fence):
                code = 'Label:\n- literal\n1. literal\n<!-- SOURCE CORE START -->\nText:\n- literal too\n<!-- SOURCE CORE END -->'
                source = self.core(f'{fence}text\n{code}\n{fence}')
                output = self.apply(source)
                self.assertEqual(output, source)
                self.assertEqual(render(output).select_one('pre code').get_text().strip(), code)

    def test_quoted_fence_text_does_not_close_an_unquoted_code_block(self):
        code = '> ```\nLabel:\n- literal\n1. literal'
        source = self.core(f'Items:\n- real item\n\n```text\n{code}\n```')
        output = self.apply(source)
        soup = render(output)
        self.assertEqual([x.get_text() for x in soup.select('li')], ['real item'])
        self.assertEqual(soup.select_one('pre code').get_text().strip(), code)

    def test_blockquote_fences_remain_literal(self):
        source = self.core('> ```text\n> Label:\n> - literal\n> 1. literal\n> ```')
        self.assertEqual(self.apply(source), source)

    def test_existing_nested_and_indented_content_remains_unchanged(self):
        source = self.core('Ready:\n\n- parent\n    - child\n- sibling\n\n    Code:\n    - literal\n    1. literal\n\n> Ready:\n>\n> - quoted')
        self.assertEqual(self.apply(source), source)
        self.assertEqual(len(render(source).select('ul')), 3)

    def test_tight_lists_keep_lazy_continuations_tight(self):
        for prefix in ['', '> ']:
            with self.subTest(prefix=prefix):
                body = '\n'.join(prefix + line for line in ['- first', 'continuation', '- second'])
                source = self.core(body)
                output = self.apply(source)
                self.assertEqual(output, source)
                soup = render(output)
                self.assertEqual(len(soup.select('li')), 2)
                self.assertEqual(soup.select('li p'), [])

    def test_indented_and_inline_backticks_do_not_hide_following_lists(self):
        for literal in ['    ```', '```inline```']:
            with self.subTest(literal=literal):
                source = self.core(f'{literal}\n\nItems:\n- real item')
                soup = render(self.apply(source))
                self.assertEqual([x.get_text() for x in soup.select('li')], ['real item'])
                self.assertIn('```' if literal.startswith(' ') else 'inline', soup.get_text())

    def test_nested_list_fences_keep_literal_markers_and_lists(self):
        source = self.core('- parent\n\n    ```text\n    Label:\n    - literal\n    <!-- SOURCE CORE END -->\n    ```\n\nItems:\n- real item')
        soup = render(self.apply(source))
        self.assertEqual(len(soup.select('li')), 2)
        self.assertEqual(soup.select('li')[-1].get_text(), 'real item')
        self.assertEqual(soup.select_one('pre code').get_text().strip(), 'Label:\n- literal\n<!-- SOURCE CORE END -->')

    def test_outside_and_unregistered_sources_are_unchanged(self):
        outside = 'Outside:\n- literal\n'
        registered = self.core('Inside:\n- list')
        unknown = self.core('Unregistered:\n- literal', 'SOURCE OTHER')
        output = self.apply(outside + registered + unknown + outside)
        self.assertTrue(output.startswith(outside))
        self.assertTrue(output.endswith(unknown + outside))
        self.assertEqual(self.apply(registered, name='unregistered.md'), registered)

    def test_incomplete_and_duplicate_boundaries_are_unchanged(self):
        for source in ['<!-- SOURCE CORE START -->\nProse:\n- item\n',
                       self.core('Prose:\n- item') * 2]:
            with self.subTest(source=source):
                self.assertEqual(self.apply(source), source)

    def test_all_bullet_markers_and_idempotence(self):
        for marker in ['-', '+', '*']:
            with self.subTest(marker=marker):
                source = self.core(f'Items:\n{marker} one\n{marker} two')
                output = self.apply(source)
                self.assertEqual([x.get_text() for x in render(output).select('li')], ['one', 'two'])
                self.assertEqual(self.apply(output), output)


if __name__ == '__main__':
    unittest.main()
