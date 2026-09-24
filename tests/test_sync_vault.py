import importlib.util
import json
import subprocess
import sys
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location('sync_vault', Path(__file__).resolve().parents[1] / 'scripts/sync_vault.py')
sync = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(sync)


class VaultTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'repo'
        self.vault = Path(self.tmp.name) / 'vault'
        self.root.mkdir()

    def source(self, name, content='source'):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        return path

    def target(self, name):
        return self.vault / 'work-handbook' / name

    def test_first_copy_and_update(self):
        source = self.source('docs/ko/index.md')
        result = sync.run_sync(self.root, self.vault)
        self.assertEqual(result['copied'], 1)
        self.assertEqual(self.target('docs/ko/index.md').read_text(), 'source')
        source.write_text('updated')
        sync.run_sync(self.root, self.vault)
        self.assertEqual(self.target('docs/ko/index.md').read_text(), 'updated')

    def test_conflict_prevents_all_writes(self):
        self.source('z.md')
        sync.run_sync(self.root, self.vault)
        self.target('z.md').write_text('vault edit')
        self.source('a.md', 'new file')
        with self.assertRaises(sync.SyncError):
            sync.run_sync(self.root, self.vault)
        self.assertFalse(self.target('a.md').exists())
        self.assertEqual(self.target('z.md').read_text(), 'vault edit')

    def test_adopts_equal_unowned_but_blocks_unequal(self):
        self.source('a.md')
        self.target('a.md').parent.mkdir(parents=True)
        self.target('a.md').write_text('different')
        with self.assertRaises(sync.SyncError):
            sync.run_sync(self.root, self.vault)
        self.target('a.md').write_text('source')
        self.assertEqual(sync.run_sync(self.root, self.vault)['adopted'], 1)
        self.assertTrue((self.root / '_workspace/vault-state.json').is_file())

    def test_source_deletion_keeps_vault_copy(self):
        source = self.source('a.md')
        sync.run_sync(self.root, self.vault)
        source.unlink()
        sync.run_sync(self.root, self.vault)
        self.assertEqual(self.target('a.md').read_text(), 'source')

    def test_scope_includes_hidden_and_ignored_sources(self):
        self.source('.agents/rule.md')
        self.source('sources/sample/source.md')
        self.source('.gitignore', 'sources/')
        for name in ['.git', '.venv', 'node_modules', 'site', '_workspace', 'project', 'third_party', 'private', '.private', '.obsidian', 'sources-private']:
            self.source(name + '/excluded.md')
        (self.root / 'link.md').symlink_to(self.root / '.agents/rule.md')
        result = sync.run_sync(self.root, self.vault)
        self.assertEqual(result['copied'], 2)
        self.assertFalse(self.target('link.md').exists())

    def test_check_is_read_only_and_reports_pending(self):
        self.source('a.md')
        result = sync.run_sync(self.root, self.vault, check=True)
        self.assertEqual(result['pending'], 1)
        self.assertFalse(self.vault.exists())
        self.assertFalse((self.root / '_workspace').exists())
        sync.run_sync(self.root, self.vault)
        self.assertEqual(sync.run_sync(self.root, self.vault, check=True)['pending'], 0)

    def test_no_overlap_or_unsafe_folder(self):
        self.source('a.md')
        for vault, folder in [(self.root, 'copy'), (self.root.parent, 'repo'), (self.vault, '../escape'), (self.vault, '.')]:
            with self.subTest(vault=vault, folder=folder):
                with self.assertRaises(sync.SyncError):
                    sync.run_sync(self.root, vault, folder)

    def test_symlink_destination_and_state_rejected(self):
        self.source('docs/a.md')
        outside = Path(self.tmp.name) / 'outside'
        outside.mkdir()
        self.target('docs').parent.mkdir(parents=True)
        self.target('docs').symlink_to(outside, target_is_directory=True)
        with self.assertRaises(sync.SyncError):
            sync.run_sync(self.root, self.vault)
        self.target('docs').unlink()
        (self.root / '_workspace').symlink_to(outside, target_is_directory=True)
        with self.assertRaises(sync.SyncError):
            sync.run_sync(self.root, self.vault)
        self.assertEqual(list(outside.iterdir()), [])

    def test_state_bound_to_destination(self):
        self.source('a.md')
        sync.run_sync(self.root, self.vault)
        with self.assertRaises(sync.SyncError):
            sync.run_sync(self.root, self.vault.parent / 'another-vault')

    def test_cli_check_exit_code_and_no_identity_output(self):
        self.source('a.md')
        script = Path(__file__).resolve().parents[1] / 'scripts/sync_vault.py'
        command = [sys.executable, str(script), '--root', str(self.root), '--vault', str(self.vault)]
        pending = subprocess.run(command + ['--check'], capture_output=True, text=True)
        self.assertEqual(pending.returncode, 1)
        self.assertIn('pending=1', pending.stdout)
        self.assertNotIn(self.tmp.name, pending.stdout + pending.stderr)
        copied = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(copied.returncode, 0)
        clean = subprocess.run(command + ['--check'], capture_output=True, text=True)
        self.assertEqual(clean.returncode, 0)
        self.assertIn('pending=0', clean.stdout)

    def test_cli_loads_local_config_when_vault_omitted(self):
        self.source('a.md')
        self.source('_workspace/vault.json', json.dumps({'vault': str(self.vault), 'folder': 'notes'}))
        script = Path(__file__).resolve().parents[1] / 'scripts/sync_vault.py'
        result = subprocess.run([sys.executable, str(script), '--root', str(self.root)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual((self.vault / 'notes/a.md').read_text(), 'source')
        self.assertNotIn(self.tmp.name, result.stdout + result.stderr)

    def test_cli_folder_overrides_config(self):
        self.source('a.md')
        self.source('_workspace/vault.json', json.dumps({'vault': str(self.vault), 'folder': 'notes'}))
        script = Path(__file__).resolve().parents[1] / 'scripts/sync_vault.py'
        result = subprocess.run([sys.executable, str(script), '--root', str(self.root), '--folder', 'explicit'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertTrue((self.vault / 'explicit/a.md').exists())
        self.assertFalse((self.vault / 'notes').exists())

    def test_cli_invalid_config_fails_without_paths(self):
        self.source('_workspace/vault.json', 'not json')
        script = Path(__file__).resolve().parents[1] / 'scripts/sync_vault.py'
        result = subprocess.run([sys.executable, str(script), '--root', str(self.root)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn('Invalid vault configuration', result.stdout)
        self.assertNotIn(self.tmp.name, result.stdout + result.stderr)

    def test_cli_missing_config_fails_without_paths(self):
        script = Path(__file__).resolve().parents[1] / 'scripts/sync_vault.py'
        result = subprocess.run([sys.executable, str(script), '--root', str(self.root)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn('Vault configuration is missing', result.stdout)
        self.assertNotIn(self.tmp.name, result.stdout + result.stderr)

    def test_cli_explicit_vault_does_not_read_config(self):
        self.source('a.md')
        self.source('_workspace/vault.json', 'invalid json')
        script = Path(__file__).resolve().parents[1] / 'scripts/sync_vault.py'
        result = subprocess.run([sys.executable, str(script), '--root', str(self.root), '--vault', str(self.vault)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertTrue(self.target('a.md').exists())

    def test_symlink_destination_leaf_rejected(self):
        self.source('a.md')
        outside = Path(self.tmp.name) / 'untouched.md'
        outside.write_text('untouched')
        self.target('a.md').parent.mkdir(parents=True)
        self.target('a.md').symlink_to(outside)
        with self.assertRaises(sync.SyncError):
            sync.run_sync(self.root, self.vault)
        self.assertEqual(outside.read_text(), 'untouched')

    def test_missing_owned_copy_is_restored(self):
        self.source('a.md')
        sync.run_sync(self.root, self.vault)
        self.target('a.md').unlink()
        self.assertEqual(sync.run_sync(self.root, self.vault)['copied'], 1)
        self.assertEqual(self.target('a.md').read_text(), 'source')

    def test_malformed_state_fails_closed(self):
        self.source('a.md')
        self.source('_workspace/vault-state.json', '{"files": []}')
        with self.assertRaises(sync.SyncError):
            sync.run_sync(self.root, self.vault)
        self.assertFalse(self.vault.exists())


if __name__ == '__main__':
    unittest.main()
