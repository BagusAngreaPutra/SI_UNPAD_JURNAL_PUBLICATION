const fs = require('fs');
const path = require('path');
const root = path.resolve(__dirname, '..');
let count = 0;
function scan(directory) {
  for (const entry of fs.readdirSync(directory, {withFileTypes: true})) {
    if (['.git', 'lib', 'node_modules', 'vendor'].includes(entry.name)) continue;
    const file = path.join(directory, entry.name);
    if (entry.isDirectory()) { scan(file); continue; }
    if (!entry.name.endsWith('.html')) continue;
    const original = fs.readFileSync(file, 'utf8');
    const fallback = path.relative(path.dirname(file), path.join(root, 'assets/visitor-map-fallback.svg')).replaceAll('\\', '/');
    const text = original.replace(/<img\b[^>]*src="https?:\/\/(?:www\.)?clustrmaps\.com\/map_v2\.png[^\"]*"[^>]*>/g, tag => {
      if (tag.includes('onerror=')) return tag;
      return tag.replace(/\s*\/?\s*>$/, ` alt="Peta pengunjung ClustrMaps" width="320" height="150" style="max-width:100%;height:auto" onerror="this.onerror=null;this.src='${fallback}'">`);
    });
    if (text !== original) { fs.writeFileSync(file, text); count++; }
  }
}
scan(root);
console.log(`Repaired visitor image fallback in ${count} pages.`);
