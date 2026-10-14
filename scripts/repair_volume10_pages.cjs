// Insert the eight-page VIS article at 179-186 in the local edition.
const fs = require('fs');
const path = require('path');
const root = path.resolve(__dirname, '..');
const ranges = {
  '2533': [179, 195], '2426': [196, 212], '2360': [213, 234],
  '1621': [235, 251], '2245': [252, 275], '2405': [276, 293],
  '2445': [294, 308], '2448': [309, 326], '2525': [327, 344]
};
const read = file => fs.readFileSync(path.join(root, file), 'utf8');
const write = (file, text) => fs.writeFileSync(path.join(root, file), text);
for (const [id, [first, last]] of Object.entries(ranges)) {
  const file = `pages/article/view/${id}.html`;
  let text = read(file);
  text = text.replace(/<meta\b[^>]*>/g, tag => {
    if (/name="citation_firstpage"/i.test(tag)) return tag.replace(/content="[^"]*"/, `content="${first + 8}"`);
    if (/name="citation_lastpage"/i.test(tag)) return tag.replace(/content="[^"]*"/, `content="${last + 8}"`);
    if (/name="DC.Identifier.pageNumber"/i.test(tag)) return tag.replace(/content="[^"]*"/, `content="${first + 8}-${last + 8}"`);
    return tag;
  });
  // Change only this article's displayed citation, not reference-list pages.
  text = text.replace(/(<div class="csl-entry">)[\s\S]*?<\/div>/g, block => block.replace(`${first}-${last}`, `${first + 8}-${last + 8}`));
  write(file, text);
}
const replacements = new Map(Object.values(ranges).map(([first, last]) => [`${first}-${last}`, `${first + 8}-${last + 8}`]));
for (const file of ['index.html', 'home.html', 'pages/issue/view/143.html']) {
  write(file, read(file).replace(/(<span class="page_number">\s*)(\d+-\d+)(\s*<\/span>)/g,
    (match, before, range, after) => before + (replacements.get(range) ?? range) + after));
}
// Verify that every article in this edition occupies a distinct page range.
const actual = [...Object.keys(ranges), '1997', '2534'].map(id => {
  const text = read(`pages/article/view/${id}.html`);
  const tags = [...text.matchAll(/<meta\b[^>]*>/g)].map(match => match[0]);
  const value = name => Number(tags.find(tag => tag.includes(`name="${name}"`)).match(/content="([^"]*)"/)[1]);
  return {id, first: value('citation_firstpage'), last: value('citation_lastpage')};
}).sort((a, b) => a.first - b.first);
for (let i = 1; i < actual.length; i++) {
  if (actual[i].first !== actual[i - 1].last + 1) throw new Error('Page ranges overlap or contain a gap');
}
console.log(actual.map(article => `${article.id}: ${article.first}-${article.last}`).join('\n'));
