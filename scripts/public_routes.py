"""Give the static mirror stable, OJS-compatible public URLs."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

for path in ROOT.rglob("*.html"):
    if any(part in {".git", "ojs"} for part in path.parts):
        continue
    text = path.read_text(encoding="utf-8")
    if "<base href=" not in text:
        text = text.replace("<head>", '<head>\n\t<base href="/">', 1)

    text = re.sub(
        r'(?:\.\./)*pages/article/view/([^"\'?#/]+)\.html',
        r'/index.php/jbmh/article/view/\1', text,
    )
    text = re.sub(
        r'(?:\.\./)*pages/issue/view/([^"\'?#/]+)\.html',
        r'/index.php/jbmh/issue/view/\1', text,
    )
    text = re.sub(
        r'(?:\.\./)*issue/arcive\.html',
        r'/index.php/jbmh/issue/archive', text,
    )
    text = re.sub(r'(?:\.\./)*home\.html', '/', text)
    text = re.sub(
        r'(href=["\'])([^"\']+?)\.html((?:[?#][^"\']*)?)(["\'])',
        lambda match: match.group(1) + match.group(2) + match.group(3) + match.group(4),
        text,
        flags=re.I,
    )

    if path.parent == ROOT / "pages" / "article" / "view":
        article_url = f"/index.php/jbmh/article/view/{path.stem}"
        text = re.sub(
            r'(?:\.\./)*ojs/index\.php/jbmh/article/view/[^"\'< ]+',
            article_url, text,
        )

    path.write_text(text, encoding="utf-8", newline="\n")
