(() => {
  const reads = document.querySelectorAll('[data-vis-read]');
  const downloads = document.querySelectorAll('[data-vis-download]');
  if (!reads.length && !downloads.length) return;
  const update = async (countRead = false) => {
    try {
      const response = await fetch('/article-stats.php?action=' + (countRead ? 'read' : 'stats'), {
        method: countRead ? 'POST' : 'GET', cache: 'no-store'
      });
      if (!response.ok) return;
      const counts = await response.json();
      reads.forEach(node => { node.textContent = counts.read; });
      downloads.forEach(node => { node.textContent = counts.download; });
    } catch (error) { console.error('Could not load article statistics', error); }
  };
  update(document.body.hasAttribute('data-vis-article'));
  window.addEventListener('focus', () => update());
  document.querySelectorAll('a[href^="/article-stats.php?action=download"]').forEach(link => {
    link.addEventListener('click', () => setTimeout(() => update(), 1000));
  });
})();
