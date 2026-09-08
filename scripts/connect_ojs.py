"""Connect public pages to OJS and build a theme shell from existing markup."""
from pathlib import Path
from urllib.parse import urlsplit
import re
import os
import json
from sync_pages import public_html, ATTR

ROOT = Path(__file__).resolve().parents[1]
mapping = {'login': 'login', 'register': 'user/register', 'user/register': 'user/register',
           'submission': 'submission', 'user': 'user', 'search/search': 'search', 'search': 'search'}
count = 0
for path in public_html():
    text = path.read_bytes().decode('utf-8')
    def rewrite(m):
        global count
        key, quote, value = m.groups()
        u = urlsplit(value.strip())
        prefix = '/index.php/jbmh/'
        if key.lower() == 'href' and u.hostname == 'jurnal.fh.unpad.ac.id' and u.path.startswith(prefix):
            route = u.path[len(prefix):].strip('/')
            if route in mapping:
                if mapping[route] == 'search':
                    target = os.path.relpath(ROOT / 'search.html', path.parent).replace('\\', '/')
                    count += 1
                    return key + '=' + quote + target + quote
                target = os.path.relpath(ROOT / 'ojs/index.php', path.parent).replace('\\', '/')
                count += 1
                return key + '=' + quote + target + '/jbmh/' + mapping[route] + quote
        return m.group(0)
    updated = ATTR.sub(rewrite, text)
    updated = re.sub(r'(href=["\'][^"\']*/jbmh/)login(["\']><span class="title">Article Submit)', r'\1submission\2', updated)
    search_target = os.path.relpath(ROOT / 'search.html', path.parent).replace('\\', '/')
    updated = re.sub(r'href=(["\'])[^"\']*ojs/index\.php/jbmh/search\1',
                     lambda match: 'href=' + match.group(1) + search_target + match.group(1),
                     updated)
    updated = updated.replace('http://jurnal.fh.unpad.ac.id/index.php/jbmh/',
                              'https://jurnal.fh.unpad-law.site/UNPAD/')
    # Any remaining absolute JBMH URL is an online OJS service (PDF, feed,
    # citation export, or metadata endpoint). Point it at this installation.
    # A relative target also works when the project is deployed in a subfolder.
    ojs = os.path.relpath(ROOT / 'ojs/index.php', path.parent).replace('\\', '/') + '/jbmh'
    for old in ('https://jurnal.fh.unpad.ac.id/index.php/jbmh',
                'http://jurnal.fh.unpad.ac.id/index.php/jbmh'):
        replacements = updated.count(old)
        if replacements:
            updated = updated.replace(old, ojs)
            count += replacements
    updated = updated.replace('?domain=https://jurnal.fh.unpad.ac.id',
                              '?domain=https://jurnal.fh.unpad-law.site')
    visitor_image = os.path.relpath(ROOT / 'assets/visitor-counter.png', path.parent).replace('\\', '/')
    updated = updated.replace('https://c.statcounter.com/11097330/0/95cfe2d4/0/', visitor_image)
    updated = updated.replace('http://c.statcounter.com/11097330/0/95cfe2d4/0/', visitor_image)
    # Keep the DOI label, but open this mirrored article on the new website.
    public_article_url = path.name
    updated = re.sub(r'(<a\b[^>]*class=["\'][^"\']*\bdoi_link\b[^"\']*["\'][^>]*\bhref=["\'])[^"\']+',
                     lambda match: match.group(1) + public_article_url,
                     updated, flags=re.I)
    path.write_bytes(updated.encode('utf-8'))

shell = (ROOT / 'peerreviewprocess.html').read_text(encoding='utf-8')
header = shell[:shell.index('<div id="main-content"')]
footer = shell[shell.index('</main>'):]
def absolute(m):
    key, quote, value = m.groups()
    value = value.strip()
    if value and not value.startswith(('#', '/')) and not urlsplit(value).scheme:
        value = '@@PUBLICROOT@@/' + value
    return key + '=' + quote + value + quote
header = ATTR.sub(absolute, header)
footer = ATTR.sub(absolute, footer)
footer = re.sub(r'<script\b[^>]*src=["\'][^"\']*ajax\.googleapis\.com/[^"\']*["\'][^>]*>\s*</script>', '', footer)
asset_report = ROOT / 'assets/asset-report.json'
if asset_report.exists():
    asset_map = json.loads(asset_report.read_text(encoding='utf-8')).get('downloaded', {})
    for source, entry in asset_map.items():
        if 'ajax.googleapis.com/' in source and entry['kind'] == 'js':
            footer = re.sub(r'<script\b[^>]*src=["\'][^"\']*' + re.escape(entry['file']) + r'["\'][^>]*>\s*</script>', '', footer)
footer = footer.replace('<script', '@@SCRIPTS@@<script', 1)
header = re.sub(r'<title>.*?</title>', '<title>@@TITLE@@ | Jurnal Bina Mulia Hukum</title>', header, flags=re.S)
header = header.replace('<h1>About Journal </h1>', '<h1>@@TITLE@@</h1>')
header = header.replace('<link rel="stylesheet"', '@@STYLES@@<link rel="stylesheet"', 1)
header = header.replace('</head>', '<link rel="stylesheet" href="@@PUBLICROOT@@/ojs/plugins/themes/unpad/forms.css"></head>')
header = header.replace('role="main">', 'role="main" id="pkp_content_main">')
header = '{assign var="unpadPublicUrl" value=$baseUrl|regex_replace:"~/ojs/?$~":""}\n{if !$pageTitleTranslated}{capture assign="pageTitleTranslated"}{translate key=$pageTitle}{/capture}{/if}\n{literal}' + header + '{/literal}'
header = header.replace('@@TITLE@@', '{/literal}{$pageTitleTranslated|escape}{literal}')
header = header.replace('@@STYLES@@', '{/literal}{load_stylesheet context="frontend"}{literal}')
footer = '{literal}' + footer + '{/literal}'
footer = footer.replace('@@SCRIPTS@@', '{/literal}{load_script context="frontend"}{call_hook name="Templates::Common::Footer::PageFooter"}{literal}')
header = header.replace('@@PUBLICROOT@@', '{/literal}{$unpadPublicUrl|escape}{literal}')
footer = footer.replace('@@PUBLICROOT@@', '{/literal}{$unpadPublicUrl|escape}{literal}')
target = ROOT / 'ojs/plugins/themes/unpad/templates/frontend/components'
target.mkdir(parents=True, exist_ok=True)
(target / 'header.tpl').write_text(header, encoding='utf-8')
(target / 'footer.tpl').write_text(footer, encoding='utf-8')
print(f'Connected {count} links; generated original public theme shell.')
