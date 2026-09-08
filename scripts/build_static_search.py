"""Build the static article search page and its browser-side index."""
from html import escape
from pathlib import Path
from bs4 import BeautifulSoup
import json
import re

ROOT = Path(__file__).resolve().parents[1]


def meta(soup, name):
    tag = soup.find('meta', attrs={'name': re.compile(r'^' + re.escape(name) + r'$', re.I)})
    if tag is None:
        tag = soup.find('meta', attrs={'property': re.compile(r'^' + re.escape(name) + r'$', re.I)})
    return str(tag.get('content', '')).strip() if tag else ''


articles = []
for path in sorted((ROOT / 'pages/article/view').glob('*.html')):
    text = path.read_text(encoding='utf-8', errors='ignore')
    soup = BeautifulSoup(text, 'html.parser')
    title = meta(soup, 'citation_title') or meta(soup, 'DC.Title')
    if not title:
        continue
    authors = [str(tag.get('content', '')).strip() for tag in soup.find_all(
        'meta', attrs={'name': re.compile(r'^citation_author$', re.I)}) if tag.get('content')]
    subjects = [str(tag.get('content', '')).strip() for tag in soup.find_all(
        'meta', attrs={'name': re.compile(r'^DC.Subject$', re.I)}) if tag.get('content')]
    articles.append({
        'title': title,
        'authors': ', '.join(authors),
        'doi': meta(soup, 'citation_doi'),
        'abstract': meta(soup, 'DC.Description'),
        'keywords': ', '.join(subjects),
        'url': '/index.php/jbmh/article/view/' + path.stem,
    })

(ROOT / 'assets/search-index.js').write_text(
    'window.JBMH_SEARCH_INDEX=' + json.dumps(articles, ensure_ascii=False) + ';',
    encoding='utf-8')

shell = (ROOT / 'peerreviewprocess.html').read_text(encoding='utf-8')
start = shell.index('<div id="main-content"')
end = shell.index('</main>', start) + len('</main>')
body = '''<div id="main-content" class="page page_search">
<div class="page-header"><h1>Search</h1></div>
<form id="local-search-form" class="search-form" role="search">
<div class="form-group"><label for="local-search-query">Search articles</label>
<input id="local-search-query" class="form-control" type="search" placeholder="Title, author, DOI, keyword..." autocomplete="off"></div>
<button class="btn btn-primary" type="submit"><i class="fa fa-search"></i> Search</button>
</form><p id="search-status" style="margin-top:24px"></p><div id="search-results"></div>
</div><!-- .page -->
</main>'''
page = shell[:start] + body + shell[end:]
page = re.sub(r'<title>.*?</title>', '<title>Search | Jurnal Bina Mulia Hukum</title>', page, count=1, flags=re.S)
page = page.replace('</body>', '<script src="assets/search-index.js"></script><script src="assets/search.js"></script></body>')
(ROOT / 'search.html').write_text(page, encoding='utf-8')
print(f'Built search index for {len(articles)} articles.')
