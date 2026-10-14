// Align the local Volume 10 No. 2 edition with the requested September 2026 label.
const fs = require('fs');
const path = require('path');
const root = path.resolve(__dirname, '..');
const read = file => fs.readFileSync(path.join(root, file), 'utf8');
const write = (file, text) => fs.writeFileSync(path.join(root, file), text);
for (const file of ['index.html', 'home.html', 'pages/issue/view/143.html', 'issue/arcive.html']) {
  write(file, read(file).replace('Mar 31, 2026', 'September 2026'));
}
let articles = 0;
for (const name of fs.readdirSync(path.join(root, 'pages/article/view'))) {
  const file = 'pages/article/view/' + name;
  let text = read(file);
  if (!text.includes('Volume 10 Number 2 September 2026')) continue;
  text = text.replace(/<meta\b[^>]*>/g, tag => {
    if (/name="DC.Date.issued"/i.test(tag)) return tag.replace(/content="[^"]*"/, 'content="2026-09"');
    if (/name="citation_date"/i.test(tag)) return tag.replace(/content="[^"]*"/, 'content="2026/09"');
    return tag;
  });
  if (name === '2534.html') {
    text = text.replace(/<meta\b[^>]*>/g, tag => {
      if (/name="DC.Date.(created|dateSubmitted|modified)"/i.test(tag)) return '';
      if (/name="(?:DC.Creator.PersonalName|citation_author)"/i.test(tag) && /content=""/.test(tag)) return '';
      if (/name="generator"/i.test(tag) && tag.includes('Sarak Opat')) return '';
      if (/name="DC.Identifier.pageNumber"/i.test(tag)) return tag.replace(/content="[^"]*"/, 'content="179-186"');
      if (/name="citation_firstpage"/i.test(tag)) return tag.replace(/content="[^"]*"/, 'content="179"');
      if (/name="citation_lastpage"/i.test(tag)) return tag.replace(/content="[^"]*"/, 'content="186"');
      if (/name="DC.Rights"/i.test(tag) && tag.includes('Copyright')) return tag.replace(/content="[^"]*"/, 'content="Copyright (c) 2026 Fitri Anita, Muhammad Amri Bintang"');
      if (/name="(?:DC.Language|citation_language)"/i.test(tag)) return tag.replace('content="en"', 'content="id"');
      if (/name="citation_journal_abbrev"/i.test(tag)) return tag.replace('content="1"', 'content="JBMH"');
      return tag;
    });
    if (!text.includes('name="citation_firstpage"')) {
      text = text.replace('</head>', '<meta name="DC.Identifier.pageNumber" content="179-186">\n<meta name="citation_firstpage" content="179">\n<meta name="citation_lastpage" content="186">\n</head>');
    }
    text = text.replace(/10\(2\)(?:, 166-178)?\./g, '10(2), 179-186.');
    // Remove citation format requests pointing to a different OJS submission.
    text = text.replace(/<div class="btn-group">[\s\S]*?<\/div>/, match => {
      if (!match.includes('submissionId=1997')) return match;
      return '';
    });
    text = text.replace(/href="[^\"]*citationstylelanguage\/download\/ris\?submissionId=1997"/g, 'href="/assets/citations/2534.ris" download');
    text = text.replace(/href="[^\"]*citationstylelanguage\/download\/bibtex\?submissionId=1997"/g, 'href="/assets/citations/2534.bib" download');
    const seen = new Set();
    text = text.replace(/<meta\b[^>]*>/g, tag => {
      const key = tag.match(/name="([^"]+)"/i)?.[1]?.toLowerCase();
      if (!['citation_keywords', 'citation_firstpage', 'citation_lastpage', 'citation_journal_abbrev'].includes(key)) return tag;
      if (seen.has(key)) return '';
      seen.add(key); return tag;
    });
  }
  write(file, text);
  articles++;
}
console.log(`Aligned publication metadata for ${articles} articles.`);
for (const file of ['index.html', 'home.html', 'pages/issue/view/143.html']) {
  write(file, read(file).replace(/(<div class="article-summary media fitri-bintang-article">[\s\S]*?)<span class="pull-left pages">[^\r\n]*/, '$1<span class="pull-left pages"><i class="fa fa-file-text-o" aria-hidden="true"></i> <span class="page_number">179-186</span></span>'));
}
