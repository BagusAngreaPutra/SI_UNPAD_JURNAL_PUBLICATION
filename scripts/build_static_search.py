"""Build the static article search page and its browser-side index."""
from html import escape
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]


def meta(text, name):
    match = re.search(
        r'<meta\s+(?:name|property)=["\']' + re.escape(name) +
        r'["\']\s+content=["\'](.*?)["\']\s*/?>', text, re.I | re.S)
    return re.sub(r'<[^>]+>', ' ', match.group(1)).strip() if match else ''


articles = []
for path in sorted((ROOT / 'pages/article/view').glob('*.html')):
    text = path.read_text(encoding='utf-8', errors='ignore')
    title = meta(text, 'citation_title') or meta(text, 'DC.Title')
    if not title:
        continue
    authors = re.findall(r'<meta\s+name=["\']citation_author["\']\s+content=["\'](.*?)["\']', text, re.I)
    articles.append({
        'title': title,
        'authors': ', '.join(authors),
        'doi': meta(text, 'citation_doi'),
        'abstract': meta(text, 'DC.Description'),
        'keywords': meta(text, 'DC.Subject'),
        'url': path.relative_to(ROOT).as_posix(),
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
