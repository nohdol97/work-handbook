"""Exercise real corpus extraction, counting, and stale-output detection."""
import json
from pathlib import Path
import tempfile
import unittest
from scripts import english_study as study


class EnglishStudyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root/'docs/en').mkdir(parents=True)
        (self.root/'learning').mkdir()
        self.page = self.root/'docs/en/topic.md'
        self.page.write_text('---\nid: hidden\n---\n# Set up\n\nWe set up a service. **Set up** again.\n')
        self.entry = dict(id='set-up',category='phrasal-verbs',term='set up',forms=['set up','sets up','setting up'],meaning_ko='설정하다',usage_ko='환경을 준비할 때.',usage_en='Use this when preparing an environment.',example_en='I will set up a test environment.',example_ko='테스트 환경을 준비하겠습니다.',register='neutral')
        self.save([self.entry])

    def save(self, entries):
        (self.root/'learning/english-entries.json').write_text(json.dumps({'entries':entries}))

    def test_corpus_excludes_code_metadata_comments_urls_and_self(self):
        self.page.write_text('---\nsecret: hidden\n---\n# Visible\n\nKeep **visible words** and [link text](https://example.com/secret). `inline_hidden`\n\n```text\nfenced_hidden\n```\n\n    indented_hidden\n\n<!-- comment_hidden -->\n\nhttps://example.com/url_hidden\n\n| Term | Meaning |\n|---|---|\n| tableword | tabletext |\n')
        directory=self.root/'docs/en/english-study';directory.mkdir()
        (directory/'index.md').write_text('self_hidden')
        before=self.page.read_bytes(); data=study.corpus(self.root)
        words=[token for blocks in data['blocks'].values() for block in blocks for token in block]
        for word in ['visible','words','link','text','tableword','tabletext']: self.assertIn(word,words)
        for word in ['secret','hidden','inline','fenced','indented','comment','url','self']: self.assertNotIn(word,words)
        self.assertEqual(list(data['hashes']),['topic.md'])
        self.assertEqual(self.page.read_bytes(),before)

    def test_counts_inflections_boundaries_documents_and_longest_form(self):
        self.page.write_text('Set up. Sets up. Setting up. SET UP. Upset update.\n\nSet\n\nup.\n\nWe’ll set it up.\n')
        (self.root/'docs/en/other.md').write_text('Set up a test.')
        entry={**self.entry,'forms':['set up','sets up','setting up','set it up','we\'ll set it up']}
        result=study.rank(study.corpus(self.root),[entry])[0]
        self.assertEqual(result['count'],6)
        self.assertEqual(result['documents'],2)
        self.assertEqual(result['sources'],['other.md','topic.md'])

    def test_frequency_sort_is_deterministic_and_zero_is_last(self):
        entries=[self.entry,{**self.entry,'id':'zero','term':'absent','forms':['absent']},{**self.entry,'id':'also','term':'again','forms':['again']}]
        rows=study.rank(study.corpus(self.root),entries)
        self.assertEqual([x['id'] for x in rows],['set-up','also','zero'])
        self.assertEqual(rows[0]['count'],3)

    def test_candidates_are_frequency_ranked(self):
        result=study.candidates(study.corpus(self.root))
        self.assertEqual(result['phrases'][0]['term'],'set up')
        self.assertEqual(result['phrases'][0]['count'],3)

    def test_soft_wrapping_preserves_phrases_but_code_is_a_boundary(self):
        self.page.write_text('We set\nup a service.\n\nSet `code` up.\n\nSet https://example.com up.')
        self.assertEqual(study.rank(study.corpus(self.root),[self.entry])[0]['count'],1)

    def test_identifiers_do_not_become_partial_word_matches(self):
        self.page.write_text('model2 model_name model')
        entry={**self.entry,'forms':['model']}
        self.assertEqual(study.rank(study.corpus(self.root),[entry])[0]['count'],1)

    def test_nested_html_blocks_do_not_recombine_parent_text(self):
        self.page.write_text('<div>set <p>nested text</p> up</div>')
        self.assertEqual(study.rank(study.corpus(self.root),[self.entry])[0]['count'],0)

    def test_reference_url_cannot_inject_markdown_links(self):
        self.save([{**self.entry,'sources':['https://example.com/)[unexpected](https://example.org']}])
        with self.assertRaises(ValueError):study.load_entries(self.root)

    def test_write_rejects_symlink_destinations_before_writing(self):
        outside=self.root/'outside';outside.mkdir()
        (self.root/'reviews').symlink_to(outside,target_is_directory=True)
        self.assertTrue(study.run(self.root,write=True))
        self.assertFalse(list(outside.iterdir()))
        self.assertFalse((self.root/'docs/ko').exists())

    def test_rejects_invalid_curated_data(self):
        for entries in [[self.entry,self.entry],[{**self.entry,'forms':[]}],[{**self.entry,'category':'other'}],[{**self.entry,'example_en':'line\nbreak'}],[{**self.entry,'forms':['set up','SET UP']}],[{**self.entry,'id':'../escape'}]]:
            with self.subTest(entries=entries):
                self.save(entries)
                with self.assertRaises(ValueError): study.load_entries(self.root)

    def test_write_and_check_detect_corpus_entry_and_output_changes(self):
        self.assertTrue(study.run(self.root))
        before=self.page.read_bytes();self.assertEqual(study.run(self.root,write=True),[])
        self.assertEqual(study.run(self.root),[])
        page=self.root/'docs/ko/english-study/phrasal-verbs.md'
        body=page.read_text(); self.assertIn('set up',body);self.assertIn('설정하다',body)
        self.assertIn('../topic.md',body);self.assertIn('3',body)
        self.assertEqual(self.page.read_bytes(),before)
        page.write_text(body+'edited');self.assertTrue(study.run(self.root))
        study.run(self.root,write=True)
        self.page.write_text('New corpus.');self.assertTrue(study.run(self.root))
        study.run(self.root,write=True)
        self.save([{**self.entry,'meaning_ko':'준비하다'}]);self.assertTrue(study.run(self.root))
        study.run(self.root,write=True)
        self.page.unlink();self.assertTrue(study.run(self.root))
        self.assertFalse((self.root/'reviews/bilingual.json').exists())

    def test_zero_frequency_supplement_and_escaping(self):
        self.save([{**self.entry,'term':'set | up','forms':['not present'],'example_en':'Use <input> & [context].'}])
        outputs=study.build(self.root)
        for lang in ['ko','en']:
            body=outputs[f'docs/{lang}/english-study/phrasal-verbs.md']
            self.assertIn('0',body);self.assertIn('&lt;input&gt;',body)
            self.assertIn('Supplement' if lang=='en' else '보충',body)

    def test_generated_english_uses_singular_frequency_labels(self):
        self.page.write_text('Set up a test.')
        body=study.build(self.root)['docs/en/english-study/phrasal-verbs.md']
        self.assertIn('1 occurrence · 1 document ·',body)


if __name__=='__main__': unittest.main()
