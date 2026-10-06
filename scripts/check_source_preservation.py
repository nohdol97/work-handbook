"""Read-only checks for source form preservation; meaning needs human review."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


def structure(text):
    """Describe Markdown structure without treating fenced examples as headings."""
    result = []
    fence = None
    paragraph = False
    for line in text.splitlines():
        if fence:
            if re.fullmatch(r'\s*' + re.escape(fence[0]) + '{' + str(fence[1]) + r',}\s*', line):
                result.append(('fence-end',))
                fence = None
            else:
                result.append(('fence-line', len(line) - len(line.lstrip()), bool(line.strip())))
            continue
        is_prose = False
        match = re.match(r'^\s*(`{3,}|~{3,})(.*)$', line)
        if match:
            fence = (match[1][0], len(match[1]))
            result.append(('fence', match[2].strip()))
        elif match := re.match(r'^(#{1,6})\s+(.+)$', line):
            number = re.match(r'(\d+\.\d+[A-Z]?)(?:\s|$)', match[2])
            result.append(('heading', len(match[1]), number[1] if number else ''))
        elif re.fullmatch(r'\s*(?:-{3,}|\*{3,}|_{3,})\s*', line):
            result.append(('separator',))
        elif match := re.match(r'^(\s*)(?:[-+*]|\d+[.)])\s+', line):
            result.append(('list', len(match[1])))
        elif line.lstrip().startswith('|'):
            result.append(('table', line.count('|')))
        elif line.lstrip().startswith('>'):
            result.append(('quote',))
        elif line.strip():
            is_prose = True
            if not paragraph:
                result.append(('paragraph',))
        paragraph = is_prose
    if fence:
        raise ValueError('unclosed code fence')
    return result


def _file(root, relative, parent):
    if not isinstance(relative, str) or not relative.endswith('.md'):
        raise ValueError('expected Markdown path')
    path = (root / relative).resolve()
    if Path(relative).is_absolute() or not path.is_relative_to(parent.resolve()):
        raise ValueError('path escapes expected source or language root')
    return path


def _span(source, start, end, include_start=False):
    if not isinstance(start, str) or (end is not None and not isinstance(end, str)) or not isinstance(include_start, bool):
        raise ValueError('source boundary must be a heading string')
    lines = source.splitlines(keepends=True)
    positions = []
    for boundary in (start, end):
        if boundary is None:
            positions.append(len(lines))
            continue
        matches = [i for i, line in enumerate(lines) if line.rstrip('\r\n') == boundary]
        if len(matches) != 1 or not re.match(r'^#{1,6} ', boundary):
            raise ValueError('source boundary missing or ambiguous')
        positions.append(matches[0])
    first, last = positions
    if first >= last:
        raise ValueError('source boundaries out of order')
    return ''.join(lines[first if include_start else first + 1:last]).strip('\r\n')


def _without_inline_additions(core, additions, lang):
    """Remove only explicitly registered, hash-bound additions for comparison."""
    if not isinstance(additions, list):
        raise ValueError('inline additions must be a list')
    if core.count('<!-- INLINE ADDITION ') != 2 * len(additions):
        raise ValueError('inline addition markers do not match registration')
    intervals, seen = [], set()
    for addition in additions:
        if not isinstance(addition, dict):
            raise ValueError('invalid inline addition record')
        marker = addition.get('marker')
        request = addition.get('user_request')
        digest = addition.get(lang + '_sha256')
        if not isinstance(marker, str) or not re.fullmatch(r'[A-Z][A-Z ]*', marker) or marker in seen:
            raise ValueError('invalid or duplicate inline addition marker')
        seen.add(marker)
        if not isinstance(request, str) or not request.strip():
            raise ValueError('inline addition requires explicit user request evidence')
        if not isinstance(digest, str) or not re.fullmatch(r'[0-9a-f]{64}', digest):
            raise ValueError('invalid inline addition hash')
        start = f'<!-- INLINE ADDITION {marker} START -->'
        end = f'<!-- INLINE ADDITION {marker} END -->'
        if core.count(start) != 1 or core.count(end) != 1:
            raise ValueError('inline addition boundary missing or duplicate')
        first, last = core.index(start), core.index(end)
        if first >= last or (first and not core[:first].endswith('\n\n')):
            raise ValueError('inline addition boundary out of order or not a block')
        last += len(end) + 2
        block = core[first:last]
        if not block.endswith(end + '\n\n') or hashlib.sha256(block.encode()).hexdigest() != digest:
            raise ValueError('inline addition hash or trailing boundary mismatch')
        intervals.append((first, last))
    intervals.sort()
    if any(left[1] > right[0] for left, right in zip(intervals, intervals[1:])):
        raise ValueError('inline additions overlap or nest')
    for first, last in reversed(intervals):
        core = core[:first] + core[last:]
    if '<!-- INLINE ADDITION ' in core:
        raise ValueError('unregistered inline addition marker')
    return core


def audit(root):
    root = Path(root).resolve()
    errors = []
    try:
        config = json.loads((root / 'reviews/source-preservation.json').read_text())
        spans = config['spans']
        if not isinstance(spans, list) or not spans:
            raise ValueError('spans must be a nonempty list')
    except (OSError, ValueError, KeyError, TypeError) as exc:
        return [f'source preservation config: {exc}']
    seen = set()
    for record in spans:
        label = record.get('page', '?') if isinstance(record, dict) else '?'
        try:
            if not isinstance(record, dict):
                raise ValueError('invalid span record')
            original_language = record['verbatim_language']
            if original_language not in ('ko', 'en'):
                raise ValueError('verbatim_language must be ko or en')
            marker = record.get('marker', 'SOURCE CORE')
            if not isinstance(marker, str) or not re.fullmatch(r'[A-Z][A-Z ]+', marker):
                raise ValueError('invalid marker')
            key = (record['page'], marker)
            if key in seen:
                raise ValueError('duplicate page marker record')
            seen.add(key)
            source_path = _file(root, record['source'], root / 'sources')
            original = _span(source_path.read_text(), record['start'], record['end'], record.get('include_start', False))
            expected_structure = structure(original)
            for lang in ('ko', 'en'):
                relative = record['page']
                if not isinstance(relative, str) or Path(relative).is_absolute():
                    raise ValueError('invalid page path')
                page = _file(root, f'docs/{lang}/{relative}', root / 'docs' / lang)
                text = page.read_bytes().decode('utf-8')
                start, end = f'<!-- {marker} START -->', f'<!-- {marker} END -->'
                if text.count(start) != 1 or text.count(end) != 1 or text.index(start) >= text.index(end):
                    raise ValueError(f'{lang}: page boundary missing, duplicate, or out of order')
                core = text.split(start, 1)[1].split(end, 1)[0]
                core = _without_inline_additions(core, record.get('inline_additions', []), lang)
                # Keep the existing source comparison's universal-newline behavior
                # after checking addition hashes against their exact stored bytes.
                core = core.replace('\r\n', '\n').replace('\r', '\n').strip('\n')
                if lang == original_language and core != original:
                    errors.append(f'{label}: {lang} verbatim source mismatch')
                if structure(core) != expected_structure:
                    errors.append(f'{label}: {lang} source structure mismatch')
        except (OSError, UnicodeError, ValueError, KeyError, TypeError) as exc:
            errors.append(f'{label}: source preservation: {exc}')
    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors = audit(args.root)
    for error in errors:
        print(error)
    print(f'Source preservation: {len(errors)} errors (meaning and readability require direct review)')
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
