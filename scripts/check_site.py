#!/usr/bin/env python3
"""Check rendered local links, language alternates and publication boundaries."""
from pathlib import Path
from urllib.parse import urlsplit, unquote
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
BASE = '/work-handbook/'

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
            documents[path] = BeautifulSoup(path.read_text(), 'html.parser')
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

def audit_site(root):
    site = root/'site'
    errors = audit_links(site)
    pages = sorted((root/'docs/ko').rglob('*.md'))
    expected = set()
    for source in pages:
        rel = source.relative_to(root/'docs/ko')
        html = rel.with_suffix('.html') if rel.name == 'index.md' else rel.with_suffix('')/'index.html'
        for lang, prefix, other_prefix, other in [('ko',Path(),Path('en'),'en'),('en',Path('en'),Path(),'ko')]:
            page = site/prefix/html
            expected.add((prefix/html).as_posix())
            if not page.is_file():
                errors.append(f'missing rendered {lang} page: {rel}')
                continue
            soup = BeautifulSoup(page.read_text(), 'html.parser')
            alternatives = soup.select(f'a[hreflang="{other}"]')
            target = (site/other_prefix/html).resolve()
            if not any(resolve_url(site,page,a['href'])[0] == target for a in alternatives):
                errors.append(f'wrong language switch: {lang}/{rel}')
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
