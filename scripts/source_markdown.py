"""Render adjacent lists in registered source spans; never write source files.

This is a narrow adapter for top-level and blockquote lists, not a Markdown
parser. Indented content is left alone; backtick/tilde fences are skipped.
"""
import json
from pathlib import Path
import re


LIST = re.compile(r'(?:[-+*]|\d+\.)[ \t]+\S')
QUOTE = re.compile(r'((?:>[ \t]?)*)(.*)')
FENCE = re.compile(r'^([ \t]*(?:>[ \t]*)*)(`{3,}|~{3,})(.*)$')


def _outside_fences(lines):
    outside, fence = [], None
    list_context, blank = None, True
    for line in lines:
        text = line.rstrip('\r\n').expandtabs(4)
        match = FENCE.match(text)
        prefix, body = QUOTE.fullmatch(text.lstrip(' ')).groups()
        depth = prefix.count('>')
        indent = len(text) - len(text.lstrip(' ')) + len(body) - len(body.lstrip(' '))
        if fence:
            outside.append(False)
            if (match and match[2][0] == fence[0] and len(match[2]) >= fence[1]
                    and match[1].count('>') == fence[2] and not match[3].strip()):
                fence = None
            continue
        # Four-space fences belong to a list only in an existing list context.
        if list_context and (depth != list_context[0] or
                             (body.strip() and blank and indent <= list_context[1])):
            list_context = None
        nested = list_context and depth == list_context[0] and indent >= list_context[1] + 4
        opener = (match and (indent < 4 or nested)
                  and (match[2][0] != '`' or '`' not in match[3]))
        if opener:
            outside.append(False)
            fence = (match[2][0], len(match[2]), depth)
        else:
            outside.append(True)
            if LIST.match(body.lstrip(' ')):
                list_context = (depth, indent)
            elif body.lstrip().startswith(('#', '<!--')):
                list_context = None
        blank = not body.strip()
    return outside


def on_page_markdown(markdown, *, page, config, files):
    """Adapt only complete, registered source markers in a localized page."""
    docs = Path(config['docs_dir']).resolve()
    try:
        relative = Path(page.file.abs_src_path).resolve().relative_to(docs)
    except ValueError:
        return markdown
    if relative.parts[0] not in ('ko', 'en') or '<!-- SOURCE ' not in markdown:
        return markdown
    records = json.loads((docs.parent / 'reviews/source-preservation.json').read_text())['spans']
    markers = {record.get('marker', 'SOURCE CORE') for record in records
               if record['page'] == Path(*relative.parts[1:]).as_posix()}
    if not markers:
        return markdown

    lines = markdown.splitlines(keepends=True)
    outside = _outside_fences(lines)
    eligible = set()
    for marker in markers:
        boundaries = []
        for edge in ('START', 'END'):
            token = f'<!-- {marker} {edge} -->'
            boundaries.append([i for i, line in enumerate(lines)
                               if outside[i] and line.rstrip('\r\n') == token])
        start, end = boundaries
        if len(start) == len(end) == 1 and start[0] < end[0]:
            eligible.update(range(start[0] + 1, end[0]))

    output = []
    list_depth = None
    for i, line in enumerate(lines):
        prefix, body = QUOTE.fullmatch(line.rstrip('\r\n')).groups()
        depth = prefix.count('>')
        if (i not in eligible or not outside[i] or not body.strip()
                or depth != list_depth or body.startswith(('#', '<!--'))):
            list_depth = None
        if i in eligible and i - 1 in eligible and outside[i] and outside[i - 1]:
            previous_prefix, previous = QUOTE.fullmatch(lines[i - 1].rstrip('\r\n')).groups()
            # Only prose at the same quote level can require a separator.
            prose = (previous and not previous[0].isspace()
                     and not previous.startswith(('#', '|', '<!--'))
                     and not LIST.match(previous)
                     and not re.fullmatch(r'[-*_ ]{3,}', previous))
            if LIST.match(body) and list_depth is None and depth == previous_prefix.count('>') and prose:
                newline = '\r\n' if line.endswith('\r\n') else '\n'
                output.append(prefix.rstrip() + newline)
        if i in eligible and outside[i] and LIST.match(body):
            list_depth = depth
        output.append(line)
    return ''.join(output)
