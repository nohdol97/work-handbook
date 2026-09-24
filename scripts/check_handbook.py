"""Fail closed on handbook structure and stale review evidence.

Meaning, privacy, and language quality still require an actual reviewer.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml

STATUSES = {'not-started', 'overview', 'studied', 'deep-dive'}
STATES = {'Included', 'Merged', 'Deferred', 'Excluded'}


def _frontmatter(path, errors):
    try:
        text = path.read_text(encoding='utf-8')
    except (OSError, UnicodeError) as exc:
        errors.append(f'{path}: cannot read: {exc}')
        return {}, ''
    match = re.match(r'\A---\s*\n(.*?)\n---\s*(?:\n|$)', text, re.S)
    if not match:
        errors.append(f'{path}: missing front matter')
        return {}, text
    try:
        data = yaml.safe_load(match.group(1))
        if not isinstance(data, dict):
            raise ValueError('expected mapping')
    except (yaml.YAMLError, ValueError) as exc:
        errors.append(f'{path}: invalid front matter: {exc}')
        return {}, text[match.end():]
    return data, text[match.end():]


def _strings(value):
    return isinstance(value, list) and all(isinstance(x, str) and x.strip() for x in value) and len(value) == len(set(value))


def _inside(path, parent):
    return path.resolve().is_relative_to(parent.resolve())


def _prose(text):
    return re.sub(r'^\s*(`{3,}|~{3,}).*?^\s*\1\s*$', '', text, flags=re.M | re.S)


def _anchors(text):
    used = {}
    result = set()
    for heading in re.findall(r'^#{1,6}\s+(.+?)\s*#*\s*$', _prose(text), re.M):
        explicit = re.search(r'\{#([^}]+)\}', heading)
        if explicit:
            result.add(explicit.group(1))
        else:
            slug = re.sub(r'[^\w\s-]', '', heading.lower()).strip()
            slug = re.sub(r'\s+', '-', slug)
            count = used.get(slug, 0)
            used[slug] = count + 1
            result.add(f'{slug}_{count}' if count else slug)
    return result


def _links(text):
    text = _prose(text)
    inline = re.findall(r'!?\[[^\]]*\]\(\s*(?:<([^>]+)>|([^\s)]+))(?:\s+[^)]*)?\)', text)
    refs = dict(re.findall(r'^\s*\[([^\]]+)\]:\s*<?([^\s>]+)>?', text, re.M))
    result = [a or b for a, b in inline] + list(refs.values())
    for label, ref in re.findall(r'!?\[([^\]]+)\]\[([^\]]*)\]', text):
        key = ref or label
        if key not in refs:
            result.append('__missing_reference__/' + key)
    return result


def _check_links(path, text, root, language_root, errors):
    for url in _links(text):
        parsed = urlsplit(url)
        if parsed.scheme or parsed.netloc:
            continue
        if parsed.path.startswith('/'):
            errors.append(f'{path}: absolute local link is not portable: {url}')
            continue
        target = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path.resolve()
        if not _inside(target, root):
            errors.append(f'{path}: link escapes repository: {url}')
            continue
        if target.is_dir():
            target = target / 'index.md'
        if not target.exists():
            errors.append(f'{path}: broken local link: {url}')
        elif target.suffix == '.md':
            if not _inside(target, language_root):
                errors.append(f'{path}: link leaves language tree: {url}')
            elif parsed.fragment and unquote(parsed.fragment) not in _anchors(target.read_text(encoding='utf-8')):
                errors.append(f'{path}: broken anchor: {url}')


def _nav_leaves(value):
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [x for item in value for x in _nav_leaves(item)]
    if isinstance(value, dict):
        return [x for item in value.values() for x in _nav_leaves(item)]
    return []


class _MkDocsLoader(yaml.SafeLoader):
    """Inspect MkDocs callable names without importing or executing them."""


_MkDocsLoader.add_multi_constructor(
    'tag:yaml.org,2002:python/name:', lambda loader, suffix, node: suffix
)


def _load_yaml(path, errors):
    try:
        data = yaml.load(path.read_text(encoding='utf-8'), Loader=_MkDocsLoader)
        if not isinstance(data, dict):
            raise ValueError('expected mapping')
        return data
    except (OSError, ValueError, yaml.YAMLError) as exc:
        errors.append(f'{path}: invalid YAML: {exc}')
        return {}


def _source_rows(root, pages, errors):
    batches = []
    all_ids = set()
    published_destinations = {}
    for batch in sorted((root / 'sources').glob('*')):
        if not batch.is_dir() or batch.name.startswith('.'):
            continue
        for name in ['source.md', 'content-manifest.md', 'coverage-matrix.md', 'coverage-report.md', 'mapping.md']:
            if not (batch / name).is_file():
                errors.append(f'{batch}: missing {name}')
        manifest, _ = _frontmatter(batch / 'content-manifest.md', errors)
        coverage, _ = _frontmatter(batch / 'coverage-matrix.md', errors)
        entries = {}
        for label, data in [('manifest', manifest), ('matrix', coverage)]:
            rows = data.get('items')
            if not isinstance(rows, list):
                errors.append(f'{batch}: {label} items must be a list')
                rows = []
            index = {}
            for item in rows:
                if not isinstance(item, dict) or not isinstance(item.get('id'), str) or not item['id'].strip():
                    errors.append(f'{batch}: invalid {label} item')
                    continue
                item_id = item['id']
                if item_id in index:
                    errors.append(f'{batch}: duplicate {label} ID {item_id}')
                index[item_id] = item
            entries[label] = index
        manifest_items, matrix = entries['manifest'], entries['matrix']
        if manifest_items.keys() != matrix.keys():
            errors.append(f'{batch}: manifest/matrix IDs differ')
        for item_id, item in manifest_items.items():
            if item_id in all_ids:
                errors.append(f'{batch}: duplicate source ID {item_id}')
            all_ids.add(item_id)
            for field in ['knowledge', 'kind']:
                if not isinstance(item.get(field), str) or not item[field].strip():
                    errors.append(f'{batch}: {item_id} missing {field}')
        for item_id, row in matrix.items():
            state = row.get('state')
            if not isinstance(state, str) or state not in STATES:
                errors.append(f'{batch}: {item_id} invalid state')
            elif state in {'Included', 'Merged'}:
                destination = row.get('destination')
                if not isinstance(destination, str) or destination not in pages:
                    errors.append(f'{batch}: {item_id} invalid destination')
                else:
                    published_destinations[item_id] = destination
                    for lang in ['ko', 'en']:
                        meta = pages[destination].get(lang, {})
                        ids = meta.get('knowledge_ids', [])
                        if not isinstance(ids, list) or item_id not in ids:
                            errors.append(f'{batch}: {item_id} missing knowledge ID in {lang}/{destination}')
                if row.get('ko') != 'Synced' or row.get('en') != 'Synced':
                    errors.append(f'{batch}: {item_id} publication requires ko/en Synced')
            else:
                reason = row.get('reason')
                if not isinstance(reason, str) or not reason.strip():
                    errors.append(f'{batch}: {item_id} {state} requires reason')
                if row.get('ko') == 'Synced' or row.get('en') == 'Synced' or row.get('destination'):
                    errors.append(f'{batch}: {item_id} unpublished item claims publication')
        report_path = batch / 'coverage-report.md'
        try:
            current_report = report_path.read_text(encoding='utf-8')
            if current_report != report_text(manifest_items, matrix):
                errors.append(f'{batch}: stale coverage report; run --write-reports')
        except (OSError, UnicodeError) as exc:
            errors.append(f'{report_path}: cannot read coverage report: {exc}')
        batches.append((batch, manifest_items, matrix))
    for relative, pair in pages.items():
        for lang, metadata in pair.items():
            ids = metadata.get('knowledge_ids')
            if isinstance(ids, list):
                for item_id in ids:
                    if isinstance(item_id, str) and item_id not in all_ids:
                        errors.append(f'{lang}/{relative}: unknown knowledge ID {item_id}')
                    elif isinstance(item_id, str) and published_destinations.get(item_id) != relative:
                        errors.append(f'{lang}/{relative}: knowledge ID is not mapped to this published page: {item_id}')
    return batches


def _reviews(root, pages, errors):
    path = root / 'reviews/bilingual.json'
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
        records = data['pages']
        if not isinstance(records, dict):
            raise ValueError('pages must be an object')
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append(f'{path}: invalid review evidence: {exc}')
        return
    for relative in pages:
        record = records.get(relative)
        if not isinstance(record, dict):
            errors.append(f'{relative}: missing review evidence')
            continue
        for field in ['semantic', 'simple_english', 'privacy']:
            if record.get(field) != 'pass':
                errors.append(f'{relative}: {field} review must pass')
        if not isinstance(record.get('reviewer'), str) or not record['reviewer'].strip():
            errors.append(f'{relative}: reviewer missing')
        for lang in ['ko', 'en']:
            page = root / 'docs' / lang / relative
            if page.is_file() and record.get(lang + '_sha256') != hashlib.sha256(page.read_bytes()).hexdigest():
                errors.append(f'{relative}: stale {lang} review hash; actual review required')
    for relative in records.keys() - pages.keys():
        errors.append(f'{relative}: review references unknown page')


def audit(root):
    root = Path(root).resolve()
    errors = []
    paths = {lang: {p.relative_to(root / 'docs' / lang).as_posix(): p for p in (root / 'docs' / lang).rglob('*.md')} for lang in ['ko', 'en']}
    if not paths['ko'] and not paths['en']:
        errors.append('No handbook pages found')
    for relative in paths['ko'].keys() ^ paths['en'].keys():
        errors.append(f'{relative}: missing language counterpart')
    pages = {}
    seen_ids = {}
    for relative in sorted(paths['ko'].keys() | paths['en'].keys()):
        pair = pages.setdefault(relative, {})
        for lang in ['ko', 'en']:
            if relative not in paths[lang]:
                continue
            path = paths[lang][relative]
            if not _inside(path, root / 'docs' / lang):
                errors.append(f'{path}: page symlink escapes language tree')
                continue
            meta, body = _frontmatter(path, errors)
            pair[lang] = meta
            page_id = meta.get('id')
            if not isinstance(page_id, str) or not re.fullmatch(r'[a-z][a-z0-9]*(?:-[a-z0-9]+)*', page_id):
                errors.append(f'{path}: invalid canonical id')
            if not isinstance(meta.get('status'), str) or meta['status'] not in STATUSES:
                errors.append(f'{path}: invalid status')
            if 'last_reviewed' not in meta:
                errors.append(f'{path}: last_reviewed is required')
            for key in ['last_updated', 'last_reviewed']:
                if key in meta:
                    try:
                        dt.date.fromisoformat(str(meta[key]))
                    except (TypeError, ValueError):
                        errors.append(f'{path}: invalid {key} date')
            if not _strings(meta.get('knowledge_ids')):
                errors.append(f'{path}: knowledge_ids must be a unique string list')
            if not body.strip():
                errors.append(f'{path}: empty page')
            if re.search(r'^#{1,6}\s*$', _prose(body), re.M):
                errors.append(f'{path}: empty heading')
            _check_links(path, body, root, root / 'docs' / lang, errors)
        if 'ko' in pair and 'en' in pair:
            if pair['ko'].get('id') != pair['en'].get('id'):
                errors.append(f'{relative}: paired canonical IDs differ')
            for key in ['knowledge_ids', 'status']:
                ko, en = pair['ko'].get(key), pair['en'].get(key)
                equal = sorted(ko) == sorted(en) if key == 'knowledge_ids' and _strings(ko) and _strings(en) else ko == en
                if not equal:
                    errors.append(f'{relative}: paired {key} differ')
            page_id = pair['ko'].get('id')
            if isinstance(page_id, str):
                if page_id in seen_ids:
                    errors.append(f'{relative}: duplicate canonical ID also used by {seen_ids[page_id]}')
                seen_ids[page_id] = relative
    config = _load_yaml(root / 'mkdocs.yml', errors)
    navigation = set(_nav_leaves(config.get('nav')))
    local_navigation = {x for x in navigation if not urlsplit(x).scheme}
    for relative in pages.keys() - local_navigation:
        errors.append(f'{relative}: orphan page missing from navigation')
    for relative in local_navigation - pages.keys():
        errors.append(f'{relative}: navigation references missing page')
    _source_rows(root, pages, errors)
    _reviews(root, pages, errors)
    return errors


def report_text(manifest_items, rows):
    """Render deterministic counts, without inferring semantic equivalence."""
    ids = set(manifest_items)
    accounted = ids & rows.keys()
    published = {key for key in accounted if rows[key].get('state') in ('Included', 'Merged')}
    total = len(ids)
    percent = f'{len(accounted) / total:.1%}' if total else 'N/A (no source items)'
    lines = ['# 지식 보존 보고서', '', f'Total meaningful source items: {total}', '']
    for state in ['Included', 'Merged', 'Deferred', 'Excluded']:
        lines.append(f'{state}: {sum(rows[key].get("state") == state for key in accounted)}')
    lines += ['', f'Accounted knowledge: {len(accounted)} / {total} ({percent})', f'Published knowledge: {len(published)} / {total}']
    for lang in ['ko', 'en']:
        count = sum(rows[key].get(lang) == 'Synced' for key in published)
        lines.append(f'{lang.upper()} published coverage: {count} / {total}')
    synced = sum(rows[key].get('ko') == 'Synced' and rows[key].get('en') == 'Synced' for key in published)
    sync_percent = f'{synced / len(published):.1%}' if published else 'N/A (no published items)'
    lines.append(f'Bilingual synchronization: {synced} / {len(published)} ({sync_percent})')
    lines += ['', '이 수치는 matrix 상태를 집계한다. audit 통과와 실제 의미·개인정보 검토가 별도로 필요하다.', '']
    return '\n'.join(lines)


def write_reports(root):
    root = Path(root)
    for batch in sorted((root / 'sources').glob('*')):
        if not batch.is_dir() or batch.name.startswith('.'):
            continue
        errors = []
        manifest, _ = _frontmatter(batch / 'content-manifest.md', errors)
        coverage, _ = _frontmatter(batch / 'coverage-matrix.md', errors)
        if errors or not isinstance(manifest.get('items'), list) or not isinstance(coverage.get('items'), list):
            continue
        items = {x['id']: x for x in manifest['items'] if isinstance(x, dict) and isinstance(x.get('id'), str)}
        rows = {x['id']: x for x in coverage['items'] if isinstance(x, dict) and isinstance(x.get('id'), str)}
        (batch / 'coverage-report.md').write_text(report_text(items, rows), encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--write-reports', action='store_true')
    args = parser.parse_args()
    if args.write_reports:
        write_reports(args.root)
    errors = audit(args.root)
    for error in errors:
        print('ERROR:', error)
    print(f'Handbook validation: {"FAIL" if errors else "PASS"} ({len(errors)} errors)')
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
