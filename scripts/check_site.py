#!/usr/bin/env python3
"""Check rendered local links, language alternates and publication boundaries."""
from pathlib import Path
import re
from urllib.parse import urlsplit, unquote
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
BASE = '/work-handbook/'

def rendered_markup(path):
    """The standalone runtime is inline JS; link metadata is before its marker."""
    content = path.read_text()
    return content.split('<script>window.__HANDBOOK_SLIDES__=', 1)[0]

def resolve_url(site, page, href):
    url = urlsplit(href)
    if url.scheme or url.netloc:
        if url.netloc != 'nohdol97.github.io' or not url.path.startswith(BASE):
            return None
        name = site / unquote(url.path.removeprefix(BASE))
    elif url.path.startswith('/'):
        name = site / unquote(url.path.removeprefix(BASE).lstrip('/'))
    else:
        name = page.parent / unquote(url.path) if url.path else page
    name = name.resolve()
    if not name.is_relative_to(site.resolve()):
        return name, url.fragment
    if name.is_dir() or url.path.endswith('/'):
        name = name/'index.html'
    return name, unquote(url.fragment)

def audit_links(site):
    site = Path(site).resolve()
    errors = []
    documents = {}

    def document(path):
        if path not in documents:
            documents[path] = BeautifulSoup(rendered_markup(path), 'html.parser')
        return documents[path]

    for page in site.rglob('*.html'):
        soup = document(page)
        for link in soup.select('a[href], link[rel="alternate"]'):
            target = resolve_url(site, page, link.get('href', ''))
            if target is None:
                continue
            name, fragment = target
            if not name.is_relative_to(site) or not name.is_file():
                errors.append(f'{page.relative_to(site)}: missing local link {link.get("href")}')
            elif fragment and name.suffix == '.html':
                dest = document(name)
                if not dest.find(id=fragment) and not dest.find('a', attrs={'name':fragment}):
                    errors.append(f'{page.relative_to(site)}: missing fragment {fragment}')
    return errors

def reading_heading_structure(soup):
    """Match the runtime's heading order, independent of translated IDs."""
    article = soup.select_one('article.md-content__inner')
    if article is None:
        return None
    return [heading.name for heading in article.select('h1,h2,h3,h4,h5,h6')
            if not heading.find_parent(class_='tabbed-content')]

def source_id(source):
    """Read the canonical ID only from the Markdown front matter."""
    content = source.read_text(encoding='utf-8')
    if not content.startswith('---\n'):
        return None
    end = content.find('\n---', 4)
    if end < 0:
        return None
    match = re.search(r'(?m)^id:\s*([a-z][a-z0-9-]*)\s*$', content[4:end])
    return match.group(1) if match else None

def points_to(site, page, soup, selector, target):
    for link in soup.select(selector):
        href = link.get('href')
        resolved = resolve_url(site, page, href) if href else None
        if resolved is not None and resolved[0] == target.resolve():
            return True
    return False

def audit_site(root):
    site = root/'site'
    errors = audit_links(site)
    pages = sorted((root/'docs/ko').rglob('*.md'))
    ko_paths = {page.relative_to(root/'docs/ko') for page in pages}
    en_paths = {page.relative_to(root/'docs/en') for page in (root/'docs/en').rglob('*.md')}
    errors.extend(f'unpaired English source: {rel}' for rel in sorted(en_paths - ko_paths))
    expected = {'slides/index.html'}
    slide_index = site/'slides/index.html'
    if not slide_index.is_file():
        errors.append('missing slide index: slides/index.html')
        index_soup = None
    else:
        index_soup = BeautifulSoup(rendered_markup(slide_index), 'html.parser')
    for source in pages:
        rel = source.relative_to(root/'docs/ko')
        html = rel.with_suffix('.html') if rel.name == 'index.md' else rel.with_suffix('')/'index.html'
        heading_structures = {}
        canonical_id = source_id(source)
        if canonical_id is None:
            errors.append(f'missing source id: ko/{rel}')
        for lang, prefix, other_prefix, other in [('ko',Path(),Path('en'),'en'),('en',Path('en'),Path(),'ko')]:
            localized_source = root/'docs'/lang/rel
            if not localized_source.is_file():
                errors.append(f'missing {lang} source: {rel}')
            elif source_id(localized_source) != canonical_id:
                errors.append(f'wrong source id: {lang}/{rel}')
            page = site/prefix/html
            expected.add((prefix/html).as_posix())
            slide = site/'slides'/lang/html
            expected.add(slide.relative_to(site).as_posix())
            if not slide.is_file():
                errors.append(f'missing slide: {lang}/{rel}')
            else:
                slide_soup = BeautifulSoup(rendered_markup(slide), 'html.parser')
                id_tag = slide_soup.select_one('meta[name="handbook-source-id"]')
                if id_tag is None or id_tag.get('content') != canonical_id:
                    errors.append(f'wrong slide source id: {lang}/{rel}')
                if not points_to(site, slide, slide_soup, 'a[data-source-link][href]', page):
                    errors.append(f'wrong slide source link: {lang}/{rel}')
                other_slide = site/'slides'/other/html
                if not points_to(site, slide, slide_soup, 'a[data-language-link][href]', other_slide):
                    errors.append(f'wrong slide language link: {lang}/{rel}')
                if index_soup is not None and not points_to(site, slide_index, index_soup, 'a[href]', slide):
                    errors.append(f'missing slide index link: {lang}/{rel}')
            if not page.is_file():
                errors.append(f'missing rendered {lang} page: {rel}')
                continue
            soup = BeautifulSoup(rendered_markup(page), 'html.parser')
            if not points_to(site, page, soup, 'a[data-slide-link][href]', slide):
                errors.append(f'wrong source slide link: {lang}/{rel}')
            headings = reading_heading_structure(soup)
            if headings is None:
                errors.append(f'missing article for reading position: {lang}/{rel}')
            else:
                heading_structures[lang] = headings
            alternatives = soup.select(f'a[hreflang="{other}"]')
            target = (site/other_prefix/html).resolve()
            if not any(resolve_url(site,page,a['href'])[0] == target for a in alternatives):
                errors.append(f'wrong language switch: {lang}/{rel}')
        if len(heading_structures) == 2 and heading_structures['ko'] != heading_structures['en']:
            errors.append(f'bilingual heading structure mismatch: {rel}')
    actual = {p.relative_to(site).as_posix() for p in site.rglob('*.html')}
    unexpected = actual - expected - {'404.html','en/404.html'}
    errors.extend(f'unexpected public HTML: {name}' for name in sorted(unexpected))
    for directory in ('sources','adr','specs','proposals','reviews'):
        if (site/directory).exists() or (site/'en'/directory).exists():
            errors.append(f'private control/source directory published: {directory}')
    return errors

if __name__ == '__main__':
    errors = audit_site(ROOT)
    for error in errors: print(error)
    print(f'Rendered site: {len(errors)} errors')
    raise SystemExit(bool(errors))
