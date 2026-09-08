"""Download missing public JBMH HTML pages and connect successful local copies."""
from concurrent.futures import ThreadPoolExecutor
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit
from urllib.request import Request, urlopen
import json
import os
import re
import time

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://jurnal.fh.unpad.ac.id/index.php/jbmh/'
ROUTES = {'': 'home.html', 'index': 'home.html', 'about_journal': 'About/about_journal.html',
          'about/editorialTeam': 'About/editorialTeam.html', 'reviewers': 'reviewers.html',
          'peerreviewprocess': 'peerreviewprocess.html', 'issue/archive': 'issue/arcive.html',
          'issue/view/105': 'issue/voluem10view.html', 'article/view/1527': 'journal2.html',
          'article/view/1791': 'journal.3.html'}
ATTR = re.compile(r'''\b(href|src|action|poster)\s*=\s*(["'])(.*?)\2''', re.I | re.S)

def public_html():
    yield from ROOT.glob('*.html')
    for folder in ('About', 'issue', 'pages'):
        yield from (ROOT / folder).rglob('*.html')

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.links.extend(v for k, v in attrs if k == 'href' and v)

def route_for(url):
    u = urlsplit(url)
    prefix = '/index.php/jbmh'
    if u.hostname != 'jurnal.fh.unpad.ac.id' or not (u.path == prefix or u.path.startswith(prefix + '/')) or u.query:
        return None
    route = u.path[len(prefix):].strip('/')
    if route in ROUTES:
        return route
    if re.fullmatch(r'(article/view/[^/]+|issue/view/[^/]+|issue/archive(?:/\d+)?|about(?:/[A-Za-z]+)?|information/[A-Za-z]+|[A-Za-z_]+|search/search)', route):
        if route.split('/')[0] not in {'login', 'logout', 'register', 'user', 'management', 'submission', 'search'}:
            return route
    return None

def discover(text, source):
    parser = Links()
    parser.feed(text)
    return {r for link in parser.links if (r := route_for(urljoin(source, link.strip()))) is not None}

def fetch(route):
    url = BASE + route
    for attempt in range(3):
        try:
            with urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0 (JBMH local archive)'}), timeout=30) as response:
                content = response.read()
                if 'text/html' not in response.headers.get('Content-Type', ''):
                    raise ValueError('Response is not HTML')
                text = content.decode(response.headers.get_content_charset() or 'utf-8')
                if '<html' not in text.lower() or re.search(r'<title>\s*(404|Error|Not Found)', text, re.I):
                    raise ValueError('Response is not a valid content page')
                if route_for(response.url) is None:
                    raise ValueError('Redirected outside public content: ' + response.url)
                return route, text, response.url, None
        except Exception as error:
            if attempt == 2:
                return route, None, url, str(error)
            time.sleep(attempt + 1)

def main():
    report_path = ROOT / 'sync-report.json'
    downloaded = {}
    if report_path.exists():
        previous = json.loads(report_path.read_text(encoding='utf-8'))
        downloaded = {r: item for r, item in previous.get('downloaded', {}).items()
                      if (ROOT / item['file']).is_file()}
        ROUTES.update({r: item['file'] for r, item in downloaded.items()})
    original = {p: p.read_bytes() for p in public_html()}
    pending = set()
    for path, raw in original.items():
        pending.update(discover(raw.decode('utf-8'), BASE))
    visited = set(ROUTES)
    failures = {}
    while pending - visited:
        batch = sorted(pending - visited)
        visited.update(batch)
        print(f'Fetching {len(batch)} missing pages...', flush=True)
        with ThreadPoolExecutor(max_workers=4) as pool:
            for route, text, source, error in pool.map(fetch, batch):
                if error:
                    failures[route] = error
                    print(f'FAILED {route}: {error}', flush=True)
                    continue
                filename = 'pages/' + route + '.html'
                target = ROOT / filename
                if target.exists():
                    text = target.read_text(encoding='utf-8')
                else:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(text.encode('utf-8'))
                ROUTES[route] = filename
                downloaded[route] = {'file': filename, 'source': source}
                pending.update(discover(text, source))
                print(f'OK {route}', flush=True)
    sources = {ROOT / item['file']: item['source'] for item in downloaded.values()}
    count = 0
    for path in public_html():
        text = path.read_bytes().decode('utf-8')
        source = sources.get(path, BASE)
        def rewrite(match):
            nonlocal count
            key, quote, value = match.groups()
            v = value.strip()
            if not v or v.startswith(('#', 'javascript:', 'mailto:', 'data:', 'tel:')):
                return match.group(0)
            absolute = urljoin(source, unescape(v))
            if not urlsplit(v).scheme and not v.startswith('/') and (path.parent / urlsplit(unescape(v)).path).is_file():
                return match.group(0)
            route = route_for(absolute)
            if key.lower() == 'href' and route in ROUTES:
                v = os.path.relpath(ROOT / ROUTES[route], path.parent).replace('\\', '/')
                fragment = urlsplit(absolute).fragment
                if fragment:
                    v += '#' + fragment
            elif v.startswith('//'):
                v = 'https:' + v
            elif v.startswith('/') or (path in sources and not urlsplit(v).scheme):
                v = urljoin(source, v)
            if v == value.strip():
                return match.group(0)
            count += 1
            return key + '=' + quote + v + quote
        updated = ATTR.sub(rewrite, text)
        assert ATTR.sub('', text) == ATTR.sub('', updated)
        path.write_bytes(updated.encode('utf-8'))
    report = {'downloaded': downloaded, 'failed': failures, 'url_attributes_updated': count,
              'online_services': ['login', 'register', 'submission', 'search', 'PDF and citation downloads']}
    (ROOT / 'sync-report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(f'Done: {len(downloaded)} downloaded, {len(failures)} failed, {count} URL attributes updated.', flush=True)

if __name__ == '__main__':
    main()
