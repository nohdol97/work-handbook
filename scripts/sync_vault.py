#!/usr/bin/env python3
"""Copy first-party Markdown to a vault without overwriting external edits."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile

EXCLUDED = {'.git', '.venv', 'venv', 'node_modules', 'site', '_workspace',
            'project', 'third_party', 'sources-private', 'private', '.private', '.obsidian', '__pycache__'}


class SyncError(RuntimeError):
    """A safe sync could not be completed."""


def digest(data):
    return hashlib.sha256(data).hexdigest()


def reject_links(path, boundary):
    """Reject symlinks below a trusted resolved boundary, including the leaf."""
    current = boundary
    for part in path.relative_to(boundary).parts:
        current = current / part
        if current.is_symlink():
            raise SyncError('Symlink in destination or state path.')
        if current != path and current.exists() and not current.is_dir():
            raise SyncError('A parent path is not a directory.')


def atomic_write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix='.vault-copy-', delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def read_state(path, destination):
    if not path.exists():
        return {}
    if not path.is_file():
        raise SyncError('State is not a regular file.')
    try:
        state = json.loads(path.read_text(encoding='utf-8'))
        if not isinstance(state, dict) or state.get('version') != 1:
            raise ValueError
        if state.get('destination') != str(destination):
            raise SyncError('State belongs to a different vault destination.')
        files = state.get('files')
        if not isinstance(files, dict):
            raise ValueError
        for name, value in files.items():
            if (not isinstance(name, str) or Path(name).is_absolute()
                    or '..' in Path(name).parts or not name.endswith('.md')
                    or not isinstance(value, str) or not re.fullmatch(r'[a-f0-9]{64}', value)):
                raise ValueError
        return files
    except (ValueError, UnicodeError, TypeError) as error:
        raise SyncError('Invalid vault state.') from error


def run_sync(root, vault, folder='work-handbook', check=False):
    """Preflight every file; return copied, unchanged, adopted and pending counts."""
    root = Path(root).expanduser().resolve()
    vault_input = Path(vault).expanduser().absolute()
    if vault_input.is_symlink():
        raise SyncError('Vault root must not be a symlink.')
    vault = vault_input.resolve()
    if not root.is_dir():
        raise SyncError('Source root is not a directory.')
    if vault.exists() and not vault.is_dir():
        raise SyncError('Vault root is not a directory.')
    if not isinstance(folder, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]*', folder):
        raise SyncError('Folder must be a single safe path component.')
    destination = vault / folder
    if destination == root or root in destination.parents or destination in root.parents:
        raise SyncError('Source and destination overlap.')
    reject_links(destination, vault)
    if destination.exists() and not destination.is_dir():
        raise SyncError('Destination is not a directory.')
    state_path = root / '_workspace' / 'vault-state.json'
    reject_links(state_path, root)
    previous = read_state(state_path, destination)
    next_state = dict(previous)
    writes = []
    counts = {'copied': 0, 'unchanged': 0, 'adopted': 0, 'pending': 0}
    conflicts = 0
    for parent, directories, files in os.walk(root, followlinks=False):
        parent = Path(parent)
        directories[:] = sorted(name for name in directories
                                if name not in EXCLUDED and not (parent / name).is_symlink())
        for name in sorted(files):
            source = parent / name
            if source.suffix != '.md' or source.is_symlink() or not source.is_file():
                continue
            relative = source.relative_to(root).as_posix()
            target = destination / relative
            reject_links(target, vault)
            if target.exists() and not target.is_file():
                raise SyncError('A destination file is not a regular file.')
            data = source.read_bytes()
            source_hash = digest(data)
            target_hash = digest(target.read_bytes()) if target.exists() else None
            owned_hash = previous.get(relative)
            if target_hash is not None:
                if owned_hash is not None and target_hash != owned_hash:
                    conflicts += 1
                    continue
                if owned_hash is None and target_hash != source_hash:
                    conflicts += 1
                    continue
            next_state[relative] = source_hash
            if target_hash == source_hash:
                counts['unchanged'] += 1
                if owned_hash is None:
                    counts['adopted'] += 1
            else:
                writes.append((target, data, target_hash))
    if conflicts:
        raise SyncError(f'Vault conflicts: {conflicts}. No files were written.')
    counts['pending'] = len(writes)
    if check:
        return counts
    for target, data, expected_hash in writes:
        reject_links(target, vault)
        actual_hash = digest(target.read_bytes()) if target.exists() else None
        if actual_hash != expected_hash:
            raise SyncError('Vault changed during sync; retry after reviewing it.')
        atomic_write(target, data)
        counts['copied'] += 1
    reject_links(state_path, root)
    state = {'version': 1, 'destination': str(destination), 'files': next_state}
    atomic_write(state_path, (json.dumps(state, indent=2, sort_keys=True) + '\n').encode())
    return counts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--vault', type=Path)
    parser.add_argument('--folder')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    try:
        folder = args.folder
        vault = args.vault
        if vault is None:
            config_root = args.root.expanduser().resolve()
            config_path = config_root / '_workspace' / 'vault.json'
            reject_links(config_path, config_root)
            if not config_path.exists():
                raise SyncError('Vault configuration is missing; provide --vault or local vault.json.')
            try:
                config = json.loads(config_path.read_text(encoding='utf-8'))
                if (not isinstance(config, dict) or not isinstance(config.get('vault'), str)
                        or not config['vault'].strip()
                        or ('folder' in config and not isinstance(config['folder'], str))):
                    raise ValueError
            except (ValueError, UnicodeError, TypeError) as error:
                raise SyncError('Invalid vault configuration.') from error
            vault = Path(config['vault']).expanduser()
            if not vault.is_absolute():
                vault = config_root / vault
            if folder is None:
                folder = config.get('folder', 'work-handbook')
        if folder is None:
            folder = 'work-handbook'
        result = run_sync(args.root, vault, folder, args.check)
    except SyncError as error:
        print(f'Vault sync blocked: {error}')
        return 1
    except OSError:
        print('Vault sync failed: filesystem access error.')
        return 1
    print(' '.join(f'{name}={value}' for name, value in result.items()))
    return 1 if args.check and result['pending'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
