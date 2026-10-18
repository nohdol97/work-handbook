#!/usr/bin/env python3
"""Build source-traced learning slide schemas and offline HTML from MkDocs nav."""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
import hashlib
import html
import importlib.util
import json
from pathlib import Path
import posixpath
import re
import shutil
import sys
from urllib.parse import quote, urlsplit

import markdown
from bs4 import BeautifulSoup
import yaml


try:
    from scripts.slide_explanations import reviewed_design
except ModuleNotFoundError:
    from slide_explanations import reviewed_design


ENGINE_VERSION = '2'
SUPPORTED_INTERACTIONS = {'none', 'parameter'}
INTERACTION_PLUGINS = []
PLUGIN_FILES = []
HEADING = re.compile(r'^(#{1,6})\s+(.+?)\s*#*\s*$')
LINK = re.compile(r'(?<!!)\[([^]]+)\]\(([^)]+)\)')
FENCE = re.compile(r'^\s*(`{3,}|~{3,})')


@dataclass(frozen=True)
class Page:
    language: str
    relative_path: Path
    document_id: str
    title: str
    nav: tuple[str, ...]


def _config(root: Path) -> dict:
    return yaml.load((root / 'mkdocs.yml').read_text(encoding='utf-8'), Loader=yaml.BaseLoader)


def _nav_entries(entries, parents=()):
    for entry in entries:
        if isinstance(entry, str):
            yield parents, entry
        elif isinstance(entry, dict):
            for label, value in entry.items():
                if isinstance(value, list):
                    yield from _nav_entries(value, parents + (label,))
                elif isinstance(value, str):
                    yield parents + (label,), value


def _frontmatter(raw: str) -> tuple[dict, str, int]:
    if not raw.startswith('---\n'):
        raise ValueError('missing YAML front matter')
    parts = raw.split('---\n', 2)
    if len(parts) != 3:
        raise ValueError('unclosed YAML front matter')
    meta = yaml.safe_load(parts[1])
    if not isinstance(meta, dict) or not meta.get('id'):
        raise ValueError('missing document id')
    return meta, parts[2], parts[1].count('\n') + 3


def _title(body: str) -> str:
    for line in body.splitlines():
        match = HEADING.match(line)
        if match and len(match[1]) == 1:
            return re.sub(r'\s*\{#[^}]+\}\s*$', '', match[2]).strip()
    raise ValueError('missing document title')


def discover(root: Path, selection: str | None = None, tolerate_errors: bool = False) -> list[Page]:
    """Use public MkDocs nav, never a raw docs glob, as publication authority."""
    nav = list(_nav_entries(_config(root).get('nav', [])))
    if not nav:
        raise ValueError('MkDocs nav is empty')
    selected = []
    for labels, name in nav:
        rel = Path(name)
        if rel.is_absolute() or '..' in rel.parts or rel.suffix != '.md':
            raise ValueError(f'invalid public nav path: {name}')
        if selection and not (rel.as_posix() == selection or
                              rel.as_posix().startswith(selection.rstrip('/') + '/')):
            continue
        selected.append((labels, rel))
    if selection and not selected:
        raise ValueError(f'no public page selected: {selection}')
    pages = []
    for labels, rel in selected:
        ids = []
        for lang in ('ko', 'en'):
            source = root / 'docs' / lang / rel
            try:
                if not source.is_file():
                    raise ValueError(f'missing {lang} source: {rel}')
                meta, body, _ = _frontmatter(source.read_text(encoding='utf-8'))
                ids.append(meta['id'])
                pages.append(Page(lang, rel, meta['id'], _title(body), labels))
            except (OSError, ValueError, yaml.YAMLError):
                if not tolerate_errors:
                    raise
                ids.append('')
                pages.append(Page(lang, rel, '', '', labels))
        if ids[0] != ids[1] and not tolerate_errors:
            raise ValueError(f'bilingual id mismatch: {rel}')
    if not tolerate_errors and len({(p.language, p.document_id) for p in pages}) != len(pages):
        raise ValueError('duplicate public document id')
    return pages


def _source_path(rel: Path, lang: str) -> str:
    base = '/work-handbook/' + ('en/' if lang == 'en' else '')
    if rel.name == 'index.md':
        tail = rel.parent.as_posix()
    else:
        tail = rel.with_suffix('').as_posix()
    return base + ('' if tail == '.' else quote(tail) + '/')


def _slide_path(rel: Path, lang: str) -> Path:
    return Path(lang) / (rel.parent if rel.name == 'index.md' else rel.with_suffix('')) / 'index.html'


def _slide_url(rel: Path, lang: str) -> str:
    return '/work-handbook/slides/' + _slide_path(rel, lang).parent.as_posix() + '/'


def _safe_markdown(source: str, page: Page | None = None) -> str:
    # Canonical Markdown is public but never allowed to inject active HTML in slides.
    rendered = markdown.markdown(source, extensions=[
        'tables', 'attr_list', 'admonition', 'pymdownx.superfences', 'pymdownx.tabbed'])
    soup = BeautifulSoup(rendered, 'html.parser')
    # Tabs become labeled static sections: no hidden language, quiz controls or
    # mandatory selection. Superfences parses indented prompt fences correctly.
    for control in soup.select('.tabbed-set > input'):
        control.decompose()
    for label in soup.select('.tabbed-set > label'):
        label.name = 'h4'
    for wrapper in list(soup.select('.tabbed-content, .tabbed-set, .highlight')):
        wrapper.unwrap()
    for tag in list(soup.find_all(['script', 'iframe', 'object', 'embed', 'style', 'form'])):
        tag.decompose()
    for tag in soup.find_all(True):
        for attr in list(tag.attrs):
            if attr.startswith('on') or attr not in ('href', 'src', 'alt', 'title', 'class', 'id'):
                del tag.attrs[attr]
        for attr in ('href', 'src'):
            value = tag.get(attr)
            if value and (value.strip().lower().startswith(('javascript:', 'data:', 'vbscript:')) or
                          value.startswith('//')):
                del tag.attrs[attr]
        if page and tag.name == 'a' and tag.get('href'):
            href = urlsplit(tag['href'])
            if not href.scheme and not href.netloc and not href.path and href.fragment:
                tag['href'] = _source_path(page.relative_path, page.language) + '#' + href.fragment
            elif not href.scheme and not href.netloc and href.path.endswith('.md') and not href.path.startswith('/'):
                relative = posixpath.normpath(posixpath.join(page.relative_path.parent.as_posix(), href.path))
                if not relative.startswith('../') and relative != '..':
                    tag['href'] = _source_path(Path(relative), page.language) + (('#' + href.fragment) if href.fragment else '')
    return str(soup)


def _sections(body: str, offset: int):
    """Keep every source line in one section; fenced headings are data."""
    sections = []
    current = {'heading': '', 'anchor': '', 'lines': [], 'line_start': offset}
    fence = None
    for number, line in enumerate(body.splitlines(), offset):
        fm = FENCE.match(line)
        if fm:
            if fence is None:
                fence = fm[1][0]
            elif fence == fm[1][0]:
                fence = None
        match = HEADING.match(line) if fence is None else None
        if match:
            if current['lines']:
                current['line_end'] = number - 1
                sections.append(current)
            current = {'heading': re.sub(r'\s*\{#[^}]+\}\s*$', '', match[2]).strip(),
                       'anchor': (re.search(r'\{#([^}]+)\}', match[2]).group(1) if re.search(r'\{#([^}]+)\}', match[2]) else ''),
                       'lines': [line], 'line_start': number}
        else:
            current['lines'].append(line)
    if current['lines']:
        current['line_end'] = offset + len(body.splitlines()) - 1
        sections.append(current)
    return sections


def source_anchors(body, sections):
    """Resolve anchors with canonical Markdown TOC semantics, including suffixes."""
    rendered = markdown.markdown(body, extensions=[
        'admonition', 'tables', 'attr_list', 'toc', 'pymdownx.highlight',
        'pymdownx.inlinehilite', 'pymdownx.tabbed', 'pymdownx.superfences'])
    headings = BeautifulSoup(rendered, 'html.parser').find_all(re.compile(r'^h[1-6]$'))
    expected = [section for section in sections if section['heading']]
    if len(headings) != len(expected):
        raise ValueError('source heading parser disagrees with canonical Markdown TOC')
    anchors = iter(tag.get('id', '') for tag in headings)
    return [next(anchors) if section['heading'] else '' for section in sections]


def section_keys(sections):
    """Locate a source section by heading ancestry, independently per language."""
    stack, occurrences, keys = [], Counter(), []
    for section in sections:
        first = section['lines'][0] if section['lines'] else ''
        match = HEADING.match(first)
        depth = len(match[1]) if match else 0
        while stack and stack[-1][0] >= depth:
            stack.pop()
        stack.append((depth, section['heading']))
        path = json.dumps(stack, ensure_ascii=False)
        occurrences[path] += 1
        # Repeated same-named siblings are distinguished in the source registry,
        # never by a rendered slide index.
        key = hashlib.sha256((path + ':' + str(occurrences[path])).encode()).hexdigest()[:20]
        keys.append(key)
    return keys


def _plain(raw: str) -> str:
    text = re.sub(r'(?m)^\s*(?:`{3,}|~{3,}).*$', '', raw)
    text = re.sub(r'(?m)^\s*<!--.*?-->\s*$', '', text)
    text = re.sub(r'!?\[([^]]+)\]\([^)]+\)', r'\1', text)
    text = re.sub(r'(?m)^\s*(?:#{1,6}\s+|[-+*]\s+|\d+[.)]\s+|>\s*)', '', text)
    return re.sub(r'[`*_{}]', '', text).strip()


def register_interaction(name, matches, create, priority=0):
    """Register a source-grounded activity without branching on document paths."""
    if any(rule[1] == name for rule in INTERACTION_PLUGINS):
        raise ValueError(f'duplicate interaction plugin: {name}')
    INTERACTION_PLUGINS.append((priority, name, matches, create))
    INTERACTION_PLUGINS.sort(key=lambda rule: rule[0], reverse=True)


def unregister_interaction(name):
    INTERACTION_PLUGINS[:] = [rule for rule in INTERACTION_PLUGINS if rule[1] != name]


def load_plugins(paths: list[Path]):
    for path in paths:
        path = path.resolve()
        if not path.is_file() or path.suffix != '.py':
            raise ValueError(f'invalid interaction plugin: {path}')
        name = f'handbook_slide_plugin_{len(PLUGIN_FILES)}'
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if not callable(getattr(module, 'register', None)):
            raise ValueError(f'interaction plugin needs register(register_interaction): {path}')
        module.register(register_interaction)
        PLUGIN_FILES.append(path)


def _interaction(raw: str, heading: str, language: str) -> dict:
    for _, name, matches, create in INTERACTION_PLUGINS:
        if matches(raw, heading, language):
            result = create(raw, heading, language)
            if not isinstance(result, dict) or not isinstance(result.get('data'), dict) or not result.get('type') or not result.get('model_note'):
                raise ValueError(f'invalid interaction plugin result: {name}')
            return result
    limits = re.search(r'(?mi)^\s*([A-Za-z_][\w]*)\s*\n\s*min\s*=\s*(-?\d+(?:\.\d+)?)\s*\n\s*max\s*=\s*(-?\d+(?:\.\d+)?)\s*$', raw)
    query = re.search(r'(?i)\bWHERE\s+([A-Za-z_][\w]*)\s*(>=|<=|>|<)\s*(-?\d+(?:\.\d+)?)', raw)
    if limits and query and limits[1] == query[1] and float(limits[2]) <= float(limits[3]) and re.search(r'prun|skip|건너뛰|읽을 필요', raw, re.I):
        number = lambda value: int(value) if float(value).is_integer() else float(value)
        return {'type': 'parameter', 'data': {'field': limits[1], 'minimum': number(limits[2]),
                'maximum': number(limits[3]), 'operator': query[2], 'threshold': number(query[3])},
                'model_note': ('원문의 최소·최대·필터 값만 사용한 범위 판정입니다. 실제 Reader는 통계 존재와 설정에 따라 다릅니다.'
                               if language == 'ko' else
                               'This checks only the source min/max and filter. A real reader depends on available statistics and configuration.')}
    return {'type': 'none', 'data': {}, 'model_note': ''}


def build_schema(root: Path, page: Page) -> dict:
    path = root / 'docs' / page.language / page.relative_path
    raw = path.read_text(encoding='utf-8')
    meta, body, offset = _frontmatter(raw)
    if meta['id'] != page.document_id:
        raise ValueError(f'document id changed: {path}')
    sections = _sections(body, offset)
    slides = []
    mapped = set()
    registry_path = Path(__file__).with_name('slide_sections.json')
    registry = json.loads(registry_path.read_text()) if registry_path.is_file() else {}
    section_registry = registry.get(page.document_id, {}).get(page.language, {})
    source_keys = section_keys(sections)
    source_anchor_ids = source_anchors(body, sections)
    for section_index, section in enumerate(sections):
        heading = section['heading'] or page.title
        content = '\n'.join(section['lines'])
        content = re.sub(r'(?m)^\s*<!--[^\n]*-->\s*\n?', '', content)
        content = re.sub(r'^#{1,6}\s+[^\n]*\n?', '', content).strip()
        if not _plain(content):
            continue
        anchor = section.get('anchor', '')
        design = reviewed_design(page.document_id, heading, anchor, page.language, content, full_source=raw)
        registered_id = section_registry.get(source_keys[section_index])
        section_id = anchor or registered_id or 'unpaired-' + source_keys[section_index]
        if design:
            section_id = design['id']
            units = design['units']
        else:
            units = [{'key': 'source', 'title': heading, 'body': content}]
        for unit in units:
            visible = unit['body']
            interaction = _interaction(content, heading, page.language) if not design else {'type': 'none', 'data': {}, 'model_note': ''}
            unit_id = section_id + ':' + unit['key']
            body_html = _safe_markdown(visible, page)
            soup = BeautifulSoup(body_html, 'html.parser')
            refs = [{'label': label, 'href': href} for label, href in LINK.findall(content)
                    if not href.lower().startswith(('javascript:', 'data:'))]
            slides.append({
                'id': unit_id, 'unit_id': unit_id, 'section_id': section_id,
                'title': unit['title'], 'section': heading, 'objective': '',
                'position_mapping': 'paired' if design or anchor or registered_id else 'unpaired',
                'concepts': [], 'visualization': interaction['type'], 'interaction': interaction,
                'parameters': interaction['data'], 'example_data': interaction['data'],
                'design': {'status': 'reviewed' if design else 'static-source',
                           'rationale': design['rationale'] if design else 'Unreviewed explanation design: preserve static source structure.',
                           'assumptions': design['assumptions'] if design else '',
                           'interaction_benefit': ('Changing the predicate shows why min/max can exclude a range, but cannot prove a match.' if interaction['type'] == 'parameter' else '')},
                'validation_rules': {'model_note': interaction['model_note'],
                                     'visible_semantic_review': bool(design),
                                     'source_traceability_is_not_quality': True},
                'body_html': body_html,
                'content_blocks': [str(node) for node in soup.children if str(node).strip()],
                'notes_html': _safe_markdown(interaction['model_note'] or ('원문 링크에서 전체 문맥을 확인할 수 있습니다.' if page.language == 'ko' else 'The source link provides the full document context.'), page),
                'source': {'path': f'docs/{page.language}/{page.relative_path.as_posix()}',
                           'heading': heading, 'anchor': source_anchor_ids[section_index],
                           'url': _source_path(page.relative_path, page.language) + ('#' + source_anchor_ids[section_index] if source_anchor_ids[section_index] else ''),
                           'line_start': section['line_start'], 'line_end': section['line_end']},
                'references': refs,
            })
        mapped.update(range(section['line_start'], section['line_end'] + 1))
    if not slides:
        raise ValueError(f'no slide content: {path}')
    source_lines = {offset + index for index, line in enumerate(body.splitlines())
                    if line.strip() and not line.lstrip().startswith('<!--')
                    and not HEADING.match(line)
                    and not re.fullmatch(r'\s*[-*_]{3,}\s*', line)}
    unmapped = sorted(source_lines - mapped)
    if unmapped:
        raise ValueError(f'unmapped source lines: {unmapped[:8]}')
    public = {rel for _, rel in _nav_entries(_config(root).get('nav', []))}
    related = []
    seen = set()
    for slide in slides:
        for ref in slide['references']:
            href = ref['href'].split('#', 1)[0]
            if not href.endswith('.md'):
                continue
            resolved = posixpath.normpath(posixpath.join(page.relative_path.parent.as_posix(), href))
            if resolved in public and resolved != page.relative_path.as_posix() and resolved not in seen:
                related.append({'label': ref['label'], 'href': _slide_url(Path(resolved), page.language)})
                seen.add(resolved)
    return {
        'schema_version': 1, 'document_id': page.document_id,
        'source_path': f'docs/{page.language}/{page.relative_path.as_posix()}',
        'language': page.language, 'title': page.title, 'nav': list(page.nav),
        'knowledge_ids': meta.get('knowledge_ids') or [],
        'outline': [{'heading': section['heading'], 'line_start': section['line_start']}
                    for section in sections if section['heading']],
        'source_hash': hashlib.sha256(raw.encode()).hexdigest(),
        'source_url': _source_path(page.relative_path, page.language),
        'alternate_url': _slide_url(page.relative_path, 'en' if page.language == 'ko' else 'ko'),
        'related': related[:6], 'slides': slides,
        'coverage': {'source_lines': len(source_lines), 'mapped_lines': len(source_lines & mapped),
                     'unmapped_lines': []},
    }


def validate_schema(schema: dict):
    if schema.get('schema_version') != 1 or not schema.get('document_id') or schema.get('language') not in ('ko', 'en'):
        raise ValueError('invalid slide schema identity')
    slides = schema.get('slides')
    if not isinstance(slides, list) or not slides:
        raise ValueError('empty slide schema')
    ids = set()
    for slide in slides:
        slide_id = slide.get('id')
        if not slide_id or slide_id in ids:
            raise ValueError('duplicate or empty slide id')
        ids.add(slide_id)
        source = slide.get('source') or {}
        if (not slide.get('body_html') or not slide.get('section_id') or
                source.get('path') != schema['source_path'] or
                not isinstance(source.get('line_start'), int) or
                not isinstance(source.get('line_end'), int) or
                source['line_start'] > source['line_end']):
            raise ValueError(f'invalid source mapping: {slide_id}')
        activity = slide.get('interaction') or {}
        activity_type = activity.get('type')
        data = activity.get('data')
        if activity_type not in SUPPORTED_INTERACTIONS or not isinstance(data, dict):
            raise ValueError(f'unsupported interaction: {slide_id}')
        if activity_type != 'none' and not activity.get('model_note'):
            raise ValueError(f'missing interaction boundary: {slide_id}')
        if activity_type == 'parameter':
            minimum, maximum = data.get('minimum'), data.get('maximum')
            if (not isinstance(minimum, (int, float)) or not isinstance(maximum, (int, float))
                    or minimum > maximum or data.get('operator') not in ('>', '>=', '<', '<=')):
                raise ValueError(f'invalid parameter: {slide_id}')
    coverage = schema.get('coverage') or {}
    if coverage.get('source_lines') != coverage.get('mapped_lines') or coverage.get('unmapped_lines'):
        raise ValueError('incomplete source coverage')


def _html_page(schema: dict, js: str, css: str) -> str:
    safe = lambda value: html.escape(str(value), quote=True)
    data = json.dumps(schema, ensure_ascii=False).replace('<', '\\u003c').replace('>', '\\u003e')
    source = safe(schema['source_url'])
    alternate = safe(schema['alternate_url'])
    return (f'<!doctype html><html lang="{safe(schema["language"])}"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<meta name="handbook-source-id" content="{safe(schema["document_id"])}">'
            f'<title>{safe(schema["title"])} · Interactive slides</title><style>{css}</style></head>'
            f'<body><div id="root"></div><nav class="source-links" aria-label="Source links">'
            f'<a data-source-link href="{source}">Source</a>'
            f'<a data-language-link href="{alternate}">Language</a></nav>'
            f'<script>window.__HANDBOOK_SLIDES__={data};</script><script>{js}</script></body></html>')


def _index(pages: list[Page], successes: set[str]) -> str:
    items = []
    for page in pages:
        key = f'{page.language}/{page.relative_path.as_posix()}'
        if key in successes:
            href = _slide_path(page.relative_path, page.language).parent.as_posix() + '/'
            items.append(f'<li><a href="{html.escape(href, quote=True)}">'
                         f'{html.escape(page.language.upper() + " · " + " / ".join(page.nav))}</a></li>')
    return ('<!doctype html><html lang="ko"><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>Work Handbook · Interactive Slides</title>'
            '<style>body{font:1.1rem system-ui;max-width:64rem;margin:3rem auto;padding:1rem;'
            'background:#f6f8fc;color:#17233a}a{color:#2457aa}li{margin:.6rem 0}</style>'
            '<h1>Work Handbook · Interactive Slides</h1><ul>' + ''.join(items) + '</ul></html>')


def build(root: Path, output: Path, bundle: Path, selection: str | None = None,
          force: bool = False) -> dict:
    """Build independent pages atomically; leave last good output on a page failure."""
    pages = discover(root, selection, tolerate_errors=True)
    output.mkdir(parents=True, exist_ok=True)
    js = bundle.read_text(encoding='utf-8')
    css_path = bundle.with_suffix('.css')
    css = css_path.read_text(encoding='utf-8') if css_path.is_file() else ''
    engine_hash = hashlib.sha256(Path(__file__).read_bytes() +
                                 Path(__file__).with_name('slide_explanations.py').read_bytes() +
                                 Path(__file__).with_name('slide_sections.json').read_bytes() +
                                 b''.join(path.read_bytes() for path in PLUGIN_FILES)).hexdigest()
    renderer_hash = hashlib.sha256((js + css + engine_hash + ENGINE_VERSION).encode()).hexdigest()
    manifest_path = output / 'manifest.json'
    old = json.loads(manifest_path.read_text()) if manifest_path.is_file() else {'pages': {}}
    current = dict(old.get('pages', {})) if selection else {}
    report = {'schema_version': 1, 'generated': 0, 'skipped': 0, 'failures': [],
              'pages': {}, 'renderer_hash': renderer_hash}
    activity_counts = Counter()
    successes = set()
    for page in pages:
        key = f'{page.language}/{page.relative_path.as_posix()}'
        target = output / _slide_path(page.relative_path, page.language)
        schema_target = output / 'schema' / page.language / page.relative_path.with_suffix('.json')
        try:
            if not page.document_id:
                raise ValueError('missing or invalid public source')
            peer = next((p for p in pages if p.relative_path == page.relative_path and
                         p.language != page.language), None)
            if peer is None or peer.document_id != page.document_id:
                raise ValueError('bilingual document id mismatch')
            schema = build_schema(root, page)
            validate_schema(schema)
            digest = hashlib.sha256((schema['source_hash'] + renderer_hash).encode()).hexdigest()
            if (not force and old.get('pages', {}).get(key, {}).get('build_hash') == digest
                    and target.is_file() and schema_target.is_file()):
                report['skipped'] += 1
            else:
                rendered = _html_page(schema, js, css)
                target.parent.mkdir(parents=True, exist_ok=True)
                schema_target.parent.mkdir(parents=True, exist_ok=True)
                schema_pending = schema_target.with_suffix('.tmp')
                schema_pending.write_text(json.dumps(schema, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
                schema_pending.replace(schema_target)
                pending = target.with_suffix('.tmp')
                pending.write_text(rendered, encoding='utf-8')
                pending.replace(target)
                report['generated'] += 1
            current[key] = {'build_hash': digest, 'source_hash': schema['source_hash'],
                            'document_id': page.document_id, 'slide_count': len(schema['slides']),
                            'knowledge_ids': schema['knowledge_ids'],
                            'source_url': schema['source_url'],
                            'slide_url': _slide_url(page.relative_path, page.language),
                            'schema_path': schema_target.relative_to(output).as_posix(),
                            'coverage': schema['coverage'],
                            'activities': dict(Counter(s['interaction']['type'] for s in schema['slides'])),
                            'sections': [s['source'] for s in schema['slides']]}
            activity_counts.update(s['interaction']['type'] for s in schema['slides'])
            successes.add(key)
            report['pages'][key] = {'status': 'ok', 'slide_count': len(schema['slides'])}
        except Exception as exc:
            report['failures'].append({'page': key, 'reason': str(exc)})
            report['pages'][key] = {'status': 'failed', 'reason': str(exc)}
            current.pop(key, None)
    if selection is None and not report['failures']:
        for key in old.get('pages', {}).keys() - current.keys():
            lang, relative = key.split('/', 1)
            stale = output / _slide_path(Path(relative), lang)
            if stale.is_file():
                stale.unlink()
                report.setdefault('removed', []).append(key)
            stale_schema = output / 'schema' / lang / Path(relative).with_suffix('.json')
            if stale_schema.is_file():
                stale_schema.unlink()
    report['summary'] = {
        'public_pages': len(pages), 'successful_pages': len(successes),
        'failed_pages': len(report['failures']),
        'slides': sum(current[key]['slide_count'] for key in successes),
        'source_lines': sum(current[key]['coverage']['source_lines'] for key in successes),
        'mapped_lines': sum(current[key]['coverage']['mapped_lines'] for key in successes),
        'activities': dict(sorted(activity_counts.items())),
    }
    (output / 'index.html').write_text(_index(pages, successes), encoding='utf-8')
    manifest_path.write_text(json.dumps({'schema_version': 1, 'pages': current}, ensure_ascii=False, indent=2) + '\n')
    (output / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    return report


def publish(root: Path, output: Path, site: Path):
    """Copy validated results after MkDocs build and inject reciprocal source links."""
    report = json.loads((output / 'report.json').read_text())
    if report['failures']:
        raise ValueError(f'{len(report["failures"])} slide pages failed; site not changed')
    manifest = json.loads((output / 'manifest.json').read_text())['pages']
    destination = site / 'slides'
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(output, destination, ignore=shutil.ignore_patterns('schema', '*.json', '*.tmp'))
    for entry in manifest.values():
        source_rel = entry['source_url'].removeprefix('/work-handbook/')
        source_html = site / source_rel / 'index.html'
        if not source_html.is_file():
            raise ValueError(f'missing MkDocs page: {source_html}')
        soup = BeautifulSoup(source_html.read_text(encoding='utf-8'), 'html.parser')
        article = soup.select_one('article.md-content__inner')
        if article is None:
            raise ValueError(f'missing article: {source_html}')
        link = soup.new_tag('a', href=entry['slide_url'])
        link['data-slide-link'] = ''
        link['class'] = 'md-button'
        link.string = '인터랙티브 슬라이드' if '/en/' not in entry['source_url'] else 'Interactive slides'
        article.insert(0, link)
        source_html.write_text(str(soup), encoding='utf-8')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['build', 'publish'])
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--output', type=Path)
    parser.add_argument('--bundle', type=Path)
    parser.add_argument('--site', type=Path)
    parser.add_argument('--select', help='Public nav .md path or directory')
    parser.add_argument('--force', action='store_true')
    parser.add_argument('--plugin', action='append', type=Path, default=[],
                        help='Python module that registers a source-grounded interaction')
    args = parser.parse_args(argv)
    root = args.root.resolve()
    output = args.output or root / '_workspace' / 'handbook-slides'
    if args.action == 'build':
        if not args.bundle:
            parser.error('build requires --bundle')
        load_plugins(args.plugin)
        report = build(root, output, args.bundle, args.select, args.force)
        print(json.dumps({k: report[k] for k in ('generated', 'skipped', 'failures')}, ensure_ascii=False))
        return bool(report['failures'])
    publish(root, output, args.site or root / 'site')
    return False


if __name__ == '__main__':
    sys.exit(main())
