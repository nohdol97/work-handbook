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


ENGINE_VERSION = '1'
SUPPORTED_INTERACTIONS = {'none', 'steps', 'architecture', 'comparison', 'scenario',
                          'reveal', 'quiz', 'flashcard', 'practice', 'parameter'}
INTERACTION_PLUGINS = []
PLUGIN_FILES = []
HEADING = re.compile(r'^(#{1,6})\s+(.+?)\s*#*\s*$')
LINK = re.compile(r'(?<!!)\[([^]]+)\]\(([^)]+)\)')
FENCE = re.compile(r'^\s*(`{3,}|~{3,})')
SENTENCE = re.compile(r'(?<=[.!?。])\s+|\n+')


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
    rendered = markdown.markdown(source, extensions=['fenced_code', 'tables', 'attr_list', 'admonition'])
    soup = BeautifulSoup(rendered, 'html.parser')
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
    current = {'heading': '', 'lines': [], 'line_start': offset}
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
                       'lines': [line], 'line_start': number}
        else:
            current['lines'].append(line)
    if current['lines']:
        current['line_end'] = offset + len(body.splitlines()) - 1
        sections.append(current)
    return sections


def _chunks(section):
    lines = section['lines']
    start = section['line_start']
    # Break at blank lines, keeping fenced examples together and every line mapped.
    blocks, active, fence, block_start = [], [], None, start
    for index, line in enumerate(lines):
        fm = FENCE.match(line)
        if fm:
            if fence is None:
                fence = fm[1][0]
            elif fence == fm[1][0]:
                fence = None
        if not line.strip() and fence is None and active:
            blocks.append((block_start, start + index - 1, '\n'.join(active)))
            active = []
        else:
            if not active:
                block_start = start + index
            active.append(line)
    if active:
        blocks.append((block_start, start + len(lines) - 1, '\n'.join(active)))
    chunks, group = [], []
    for block in blocks:
        lead_only = group and all(HEADING.match(x[2].strip()) or x[2].strip().startswith('<!--')
                                  for x in group)
        if group and not lead_only and sum(len(x[2]) for x in group) + len(block[2]) > 1100:
            chunks.append(group)
            group = []
        group.append(block)
    if group:
        chunks.append(group)
    return chunks


def _plain(raw: str) -> str:
    text = re.sub(r'(?m)^\s*(?:`{3,}|~{3,}).*$', '', raw)
    text = re.sub(r'(?m)^\s*<!--.*?-->\s*$', '', text)
    text = re.sub(r'!?\[([^]]+)\]\([^)]+\)', r'\1', text)
    text = re.sub(r'(?m)^\s*(?:#{1,6}\s+|[-+*]\s+|\d+[.)]\s+|>\s*)', '', text)
    return re.sub(r'[`*_{}]', '', text).strip()


def _items(raw: str) -> list[dict]:
    found = []
    for line in raw.splitlines():
        match = re.match(r'^\s*(?:[-+*]|\d+[.)])\s+(.+)', line)
        if match:
            label = _plain(match[1])
            if label:
                found.append({'label': label[:160], 'detail': label})
    return found[:16]


def _table_items(raw: str) -> list[dict]:
    rows = []
    for line in raw.splitlines():
        if line.strip().startswith('|'):
            cells = [x.strip() for x in line.strip().strip('|').split('|')]
            if cells and not all(re.fullmatch(r':?-{2,}:?', x) for x in cells):
                rows.append(cells)
    if len(rows) < 3:
        return []
    return [{'label': _plain(row[0])[:160], 'detail': _plain(' · '.join(row[1:]))}
            for row in rows[1:17] if len(row) > 1]


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
    prompt = re.search(r'(?ms)^\s*```[^\n]*\.prompt[^\n]*\n(.*?)^\s*```', raw)
    if prompt:
        guidance = _plain(raw[prompt.end():])
        return {'type': 'practice', 'data': {'prompt': prompt[1].strip(), 'guidance': guidance},
                'model_note': '원문의 예시 요청을 수정해 연습합니다. 외부 서비스에 전송하지 않습니다.' if language == 'ko' else
                'Edit the source example locally. It is not sent to a service.'}
    quote_lines = [re.sub(r'^\s*>\s?', '', line).strip() for line in raw.splitlines()
                   if re.match(r'^\s*>\s*\S', line)]
    if quote_lines and (len(quote_lines) >= 2 or re.search(r'\*\*[^*]+\*\*', raw)):
        detail = ' / '.join(quote_lines[:4])
        return {'type': 'flashcard', 'data': {'items': [{'label': heading, 'detail': detail}]},
                'model_note': '원문 인용 예문을 앞뒤로 확인합니다.' if language == 'ko' else
                'Flip to reveal the source example.'}
    table = _table_items(raw)
    bullets = _items(raw)
    lower = (raw + ' ' + heading).lower()
    if table:
        return {'type': 'comparison', 'data': {'items': table},
                'model_note': '원문 표의 행을 선택해 확인합니다.' if language == 'ko' else 'Explore rows from the source table.'}
    if len(bullets) >= 2:
        terms = ('failure', 'recover', '장애', '복구', '오류', 'incident')
        typ = 'scenario' if any(word in lower for word in terms) else 'steps'
        return {'type': typ, 'data': {'items': bullets},
                'model_note': '원문 항목의 순서를 탐색합니다. 실제 시스템 실행은 아닙니다.' if language == 'ko' else
                'Explore the source item order. This does not execute a real system.'}
    diagram = re.search(r'(?ms)^\s*```(?:text|mermaid)?[^\n]*\n(.*?)^\s*```', raw)
    diagram_text = diagram[1] if diagram and re.search(r'[→│▼↓]|-->|flowchart|graph ', diagram[1]) else ''
    if diagram_text:
        lines = []
        for line in diagram_text.splitlines():
            cleaned = re.sub(r'[│─┌┐└┘┬┴├┤┼▼↓→]+', ' ', line)
            cleaned = _plain(cleaned)
            if cleaned and len(cleaned) <= 80 and cleaned.lower() not in ('예:', 'example:', '대표:') and cleaned not in lines:
                lines.append(cleaned)
        lines = lines[:14]
        if len(lines) >= 2:
            prose = raw.replace(diagram[0], '') if diagram else ''
            sentences = [s.strip() for s in SENTENCE.split(_plain(prose)) if s.strip()]
            linear = bool(re.search(r'[→▼↓]', diagram_text)) and not bool(re.search(r'[┬┴├┤┼]', diagram_text))
            items = []
            for index, label in enumerate(lines):
                explained = next((sentence for sentence in sentences
                                  if label.casefold() in sentence.casefold() and len(sentence) > len(label) + 10), '')
                if explained:
                    detail = explained
                elif linear:
                    neighbors = lines[max(0, index - 1): min(len(lines), index + 2)]
                    detail = ('원문 흐름: ' if language == 'ko' else 'Source flow: ') + ' → '.join(neighbors)
                else:
                    detail = ('원문 도식 요소: ' if language == 'ko' else 'Source diagram element: ') + label
                items.append({'label': label, 'detail': detail})
            return {'type': 'architecture', 'data': {'items': items},
                    'model_note': '원문 도식과 설명의 연결만 보여줍니다. 실제 시스템을 실행하지 않습니다.' if language == 'ko' else
                    'This explores the source diagram and prose. It does not run a real system.'}
    return {'type': 'none', 'data': {}, 'model_note': ''}


def _visible_content(content: str, interaction_type: str) -> str:
    """Keep a short setup visible; complete source stays in expandable notes."""
    if interaction_type == 'none':
        return content
    if interaction_type == 'quiz':
        return ''
    setup = []
    for line in content.splitlines():
        if re.match(r'^\s*(?:```|~~~|\||>|===|[-+*]\s|\d+[.)]\s|예\s*:|Example\s*:)', line, re.I):
            break
        setup.append(line)
    paragraphs = '\n'.join(setup).strip().split('\n\n')
    visible = '\n\n'.join(paragraphs[:2]).strip()
    return visible if len(visible) <= 500 else paragraphs[0][:500]


def build_schema(root: Path, page: Page) -> dict:
    path = root / 'docs' / page.language / page.relative_path
    raw = path.read_text(encoding='utf-8')
    meta, body, offset = _frontmatter(raw)
    if meta['id'] != page.document_id:
        raise ValueError(f'document id changed: {path}')
    sections = _sections(body, offset)
    slides = []
    mapped = set()
    for section_index, section in enumerate(sections):
        heading = section['heading'] or page.title
        for chunk_index, blocks in enumerate(_chunks(section)):
            content = '\n\n'.join(x[2] for x in blocks)
            content = re.sub(r'(?m)^\s*<!--[^\n]*-->\s*\n?', '', content)
            content = re.sub(r'^#{1,6}\s+[^\n]*\n?', '', content)
            plain = _plain(content)
            if not plain:
                continue
            short = plain[:240].strip()
            refs = [{'label': label, 'href': href} for label, href in LINK.findall(content)
                    if not href.lower().startswith(('javascript:', 'data:'))]
            interaction = _interaction(content, heading, page.language)
            visible = _visible_content(content, interaction['type'])
            objective = (f'{heading}의 핵심을 설명하고 원문 근거를 확인한다' if page.language == 'ko' else
                         f'Explain the key idea in {heading} using source evidence')
            slides.append({
                'id': f'{section_index + 1}-{chunk_index + 1}', 'title': heading,
                'section': heading, 'objective': objective,
                'concepts': [{'term': heading, 'explanation': short}],
                'visualization': interaction['type'], 'interaction': interaction,
                'parameters': interaction['data'], 'example_data': interaction['data'],
                'validation_rules': {'source_grounded': True, 'model_note': interaction['model_note']},
                'body_html': _safe_markdown(visible, page), 'notes_html': _safe_markdown(content, page),
                'source': {'path': f'docs/{page.language}/{page.relative_path.as_posix()}',
                           'heading': heading, 'line_start': blocks[0][0], 'line_end': blocks[-1][1]},
                'references': refs,
            })
            mapped.update(range(blocks[0][0], blocks[-1][1] + 1))
            if interaction['type'] == 'comparison' and len(interaction['data']['items']) >= 3:
                rows = interaction['data']['items'][:4]
                if len({row['detail'] for row in rows}) >= 3:
                    first = rows[0]
                    alternatives = [row['detail'] for row in rows[1:3]]
                    position = int(hashlib.sha256((page.document_id + heading).encode()).hexdigest(), 16) % 3
                    options = alternatives.copy()
                    options.insert(position, first['detail'])
                    question = (f"원문 표에서 '{first['label']}'에 해당하는 설명은?" if page.language == 'ko' else
                                f"Which source-table description matches '{first['label']}'?")
                    slides.append({
                        'id': f'{section_index + 1}-{chunk_index + 1}-quiz',
                        'title': heading, 'section': heading,
                        'objective': (f'{heading}의 표를 확인하고 선택 근거를 설명한다' if page.language == 'ko' else
                                      f'Apply the source table in {heading}'),
                        'concepts': [{'term': first['label'], 'explanation': first['detail']}],
                        'visualization': 'quiz',
                        'interaction': {'type': 'quiz', 'data': {'question': question,
                                         'options': options, 'correctIndex': position,
                                         'explanation': first['detail']},
                                        'model_note': '정답은 원문 표의 해당 행입니다.' if page.language == 'ko' else
                                        'The answer is the matching source-table row.'},
                        'parameters': {}, 'example_data': rows,
                        'validation_rules': {'source_grounded': True, 'correct_index': position},
                        'body_html': '', 'notes_html': _safe_markdown(content, page),
                        'source': {'path': f'docs/{page.language}/{page.relative_path.as_posix()}',
                                   'heading': heading, 'line_start': blocks[0][0], 'line_end': blocks[-1][1]},
                        'references': refs,
                    })
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
        if (not slide.get('objective') or not slide.get('notes_html') or
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
        if activity_type == 'quiz':
            options = data.get('options')
            correct = data.get('correctIndex')
            if (not isinstance(options, list) or len(options) < 2 or
                    not isinstance(correct, int) or not 0 <= correct < len(options)):
                raise ValueError(f'invalid quiz: {slide_id}')
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
