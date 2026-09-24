"""Check prompt structure and cross-page text parity, not semantic truth."""
from pathlib import Path
import re

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]


def inspect_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    errors, groups = [], []
    all_codes = soup.select('.prompt pre code')
    grouped_count = 0
    for tab in soup.select('.tabbed-set'):
        if not tab.select('.prompt'):
            continue
        labels = [label.get_text(strip=True) for label in tab.select('.tabbed-labels label')]
        blocks = tab.select('.tabbed-block')
        if len(labels) != 2 or set(labels) != {'한국어', 'English'} or len(blocks) != 2:
            errors.append('prompt language group must contain Korean and English exactly once')
            continue
        group = {}
        for label, block in zip(labels, blocks):
            codes = block.select('.prompt pre code')
            if len(codes) != 1:
                errors.append('each prompt language needs one marked code block')
                continue
            grouped_count += 1
            text = codes[0].get_text()
            if len([line for line in text.splitlines() if line.strip()]) < 4:
                errors.append('prompt must remain multiline')
            markers = (['[맥락]', '[요청]', '[출력]', '[검증]'] if label == '한국어'
                       else ['[Context]', '[Task]', '[Output]', '[Checks]'])
            lines = [line.strip() for line in text.splitlines()]
            if any(lines.count(marker) != 1 for marker in markers):
                errors.append('prompt needs each language-specific section exactly once')
            else:
                positions = [lines.index(marker) for marker in markers]
                if positions != sorted(positions):
                    errors.append('prompt sections must follow context, task, output, checks order')
                elif any(not any(lines[start + 1:end]) for start, end in
                         zip(positions, positions[1:] + [len(lines)])):
                    errors.append('prompt sections must contain instructions')
            group[label] = text
        groups.append(group)
    if grouped_count != len(all_codes):
        errors.append('prompt code is outside a complete language group')
    return errors, groups


def audit(root):
    root = Path(root)
    errors, total, new_total = [], 0, 0
    for source in sorted((root / 'docs/ko').rglob('*.md')):
        relative = source.relative_to(root / 'docs/ko')
        text = source.read_text()
        library = relative.parts[0] == 'prompts' and relative.name != 'index.md'
        existing = bool(re.search(r'^## .*LLM', text, re.M))
        if not (library or existing):
            continue
        html_relative = relative.with_suffix('') / 'index.html'
        pairs, anchors = {}, {}
        for language, prefix in [('ko', Path()), ('en', Path('en'))]:
            page = root / 'site' / prefix / html_relative
            if not page.is_file():
                errors.append(f'{language}/{relative}: missing rendered prompt page')
                continue
            html = page.read_text()
            found, pairs[language] = inspect_html(html)
            errors.extend(f'{language}/{relative}: {error}' for error in found)
            if not pairs[language]:
                errors.append(f'{language}/{relative}: no bilingual prompts rendered')
            soup = BeautifulSoup(html, 'html.parser')
            ids = [h['id'] for h in soup.select('h2[id]') if re.fullmatch(r'[a-z][a-z0-9-]*-\d{2}', h['id'])]
            anchors[language] = ids
            if library and len(ids) != len(pairs[language]):
                errors.append(f'{language}/{relative}: scenario anchors and prompt groups differ')
            if len(ids) != len(set(ids)):
                errors.append(f'{language}/{relative}: duplicate scenario anchor')
        if pairs.get('ko') != pairs.get('en'):
            errors.append(f'{relative}: prompt translations differ between localized pages')
        if anchors.get('ko') != anchors.get('en'):
            errors.append(f'{relative}: scenario anchors differ between languages')
        count = len(pairs.get('ko', []))
        total += count
        if library:
            new_total += count
    if new_total < 100:
        errors.append(f'expected at least 100 new scenarios, found {new_total}')
    return errors, total, new_total


if __name__ == '__main__':
    errors, total, new_total = audit(ROOT)
    for error in errors:
        print('ERROR:', error)
    print(f'Prompts: {total} bilingual examples ({new_total} new), {len(errors)} errors')
    raise SystemExit(bool(errors))
