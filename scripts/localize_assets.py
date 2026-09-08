"""Vendor public display assets and CSS dependencies without changing page content."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urlsplit, urljoin, urldefrag, quote
from urllib.request import Request, urlopen
from html import unescape
import hashlib
import json
import mimetypes
import os
import re
from sync_pages import ROOT, public_html, ATTR

ASSETS = ROOT / 'assets' / 'vendor'
REPORT = ROOT / 'assets' / 'asset-report.json'
TAG = re.compile(r'<(?:img|script|link|source)\b[^>]*>', re.I | re.S)
CSS_URL = re.compile(r'''url\(\s*(["']?)(.*?)\1\s*\)''', re.I)
CSS_IMPORT = re.compile(r'''(@import\s+)(["'])(.*?)\2''', re.I)
BASE = 'https://jurnal.fh.unpad.ac.id/'
BOOTSTRAP = BASE + 'index.php/jbmh/$$$call$$$/page/page/css?name=bootstrap'
FALLBACK = 'https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/css/bootstrap.min.css'

def canonical(value, base=BASE):
    value = unescape(value.strip())
    if not value or value.startswith(('data:', '#', 'javascript:')):
        return None
    url = urldefrag(urljoin(base, value))[0]
    return url if urlsplit(url).scheme in ('http', 'https') else None

def kind(tag):
    if tag.lower().startswith('<link'):
        rel = re.search(r'''\brel=["']([^"']+)["']''', tag, re.I)
        if not rel or not set(rel.group(1).lower().split()) & {'stylesheet', 'icon', 'shortcut'}:
            return None
        return 'css' if 'stylesheet' in rel.group(1).lower() else 'image'
    if tag.lower().startswith('<script'):
        return 'js'
    return 'image'

def display_assets(text):
    for tag in TAG.findall(text):
        asset_kind = kind(tag)
        if not asset_kind:
            continue
        for key, _, value in ATTR.findall(tag):
            if key.lower() not in ('src', 'href') or not value.strip().startswith(('https://', 'http://', '//')):
                continue
            url = canonical(value)
            if url and not any(host in urlsplit(url).netloc for host in ('google-analytics.com', 'googletagmanager.com', 'statcounter.com', 'clustrmaps.com')):
                yield url, asset_kind

def fetch(item):
    url, asset_kind = item
    source = url.replace('https://sinta.kemdikbud.go.id/badge/', 'https://sinta.kemdiktisaintek.go.id/badge/')
    try:
        for attempt in range(2):
            request_url = quote(source, safe=':/?&=%+$,;@!()*[]~')
            request = Request(request_url, headers={'User-Agent': 'Mozilla/5.0', 'Referer': BASE})
            with urlopen(request, timeout=25) as response:
                data = response.read()
                mime = response.headers.get_content_type()
                actual = response.url
            if not data and url == BOOTSTRAP and attempt == 0:
                source = FALLBACK
                continue
            if not data or mime == 'text/html':
                raise ValueError('Empty response or HTML instead of asset')
            break
        extension = '.css' if asset_kind == 'css' else '.js' if asset_kind == 'js' else Path(urlsplit(actual).path).suffix.lower()
        if not extension or len(extension) > 8:
            extension = mimetypes.guess_extension(mime) or '.bin'
        filename = hashlib.sha256(url.encode()).hexdigest()[:20] + extension
        path = ASSETS / filename
        path.write_bytes(data)
        return url, {'file': path.relative_to(ROOT).as_posix(), 'kind': asset_kind, 'source': actual, 'bytes': len(data)}, None
    except Exception as error:
        return url, None, str(error)

def main():
    ASSETS.mkdir(parents=True, exist_ok=True)
    existing = json.loads(REPORT.read_text()) if REPORT.exists() else {}
    downloaded = {u: entry for u, entry in existing.get('downloaded', {}).items() if (ROOT / entry['file']).is_file()}
    pages = list(public_html())
    pending = dict(item for path in pages for item in display_assets(path.read_text(encoding='utf-8')))
    failed = {}
    seen = set(downloaded)
    raw_css = {}
    while set(pending) - seen:
        batch = [(u, pending[u]) for u in sorted(set(pending) - seen)]
        seen.update(u for u, _ in batch)
        print(f'Downloading {len(batch)} display assets...', flush=True)
        with ThreadPoolExecutor(max_workers=4) as pool:
            for url, entry, error in pool.map(fetch, batch):
                if error:
                    failed[url] = error
                    print(f'Unavailable: {url}: {error}', flush=True)
                    continue
                downloaded[url] = entry
                if entry['kind'] == 'css':
                    css = (ROOT / entry['file']).read_text(encoding='utf-8-sig')
                    raw_css[url] = css
                    for match in CSS_URL.finditer(css):
                        dep = canonical(match.group(2), entry['source'])
                        if dep:
                            pending[dep] = 'css' if '/css?' in dep or dep.endswith('.css') else 'image'
                    for match in CSS_IMPORT.finditer(css):
                        dep = canonical(match.group(3), entry['source'])
                        if dep:
                            pending[dep] = 'css'
    for url, css in raw_css.items():
        entry = downloaded[url]
        def css_target(value):
            absolute = canonical(value, entry['source'])
            if not absolute:
                return value
            fragment = urlsplit(unescape(value)).fragment
            return (Path(downloaded[absolute]['file']).name if absolute in downloaded else absolute) + ('#' + fragment if fragment else '')
        css = CSS_URL.sub(lambda m: 'url("' + css_target(m.group(2)) + '")', css)
        css = CSS_IMPORT.sub(lambda m: m.group(1) + '"' + css_target(m.group(3)) + '"', css)
        (ROOT / entry['file']).write_text(css, encoding='utf-8')
    count = 0
    for path in pages:
        text = path.read_bytes().decode('utf-8')
        def replace_tag(match):
            tag = match.group(0)
            if not kind(tag):
                return tag
            def replace_attr(m):
                nonlocal count
                key, q, value = m.groups()
                if not value.strip().startswith(('https://', 'http://', '//')):
                    return m.group(0)
                url = canonical(value)
                if url not in downloaded:
                    return m.group(0)
                target = os.path.relpath(ROOT / downloaded[url]['file'], path.parent).replace('\\', '/')
                count += 1
                return key + '=' + q + target + q
            return ATTR.sub(replace_attr, tag)
        updated = TAG.sub(replace_tag, text)
        assert ATTR.sub('', updated) == ATTR.sub('', text), path
        if 'theme-compat.css' not in updated:
            compat = os.path.relpath(ROOT / 'assets/theme-compat.css', path.parent).replace('\\', '/')
            updated = updated.replace('</head>', f'<link rel="stylesheet" href="{compat}">\n</head>')
        path.write_bytes(updated.encode('utf-8'))
    REPORT.write_text(json.dumps({'downloaded': downloaded, 'unavailable': failed, 'updated_attributes': count}, indent=2), encoding='utf-8')
    print(f'Completed: {len(downloaded)} local assets, {len(failed)} unavailable, {count} references updated.', flush=True)

if __name__ == '__main__':
    main()
