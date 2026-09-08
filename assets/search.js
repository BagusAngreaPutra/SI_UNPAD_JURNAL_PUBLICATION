(function () {
  'use strict';
  var form = document.getElementById('local-search-form');
  var input = document.getElementById('local-search-query');
  var status = document.getElementById('search-status');
  var results = document.getElementById('search-results');
  var index = window.JBMH_SEARCH_INDEX || [];

  function safe(value) {
    var node = document.createElement('div');
    node.textContent = value || '';
    return node.innerHTML;
  }

  function run(query) {
    query = (query || '').trim();
    var words = query.toLocaleLowerCase().split(/\s+/).filter(Boolean);
    if (!words.length) {
      status.textContent = 'Enter a title, author, DOI, or keyword.';
      results.innerHTML = '';
      return;
    }
    var found = index.filter(function (article) {
      var haystack = [article.title, article.authors, article.doi, article.abstract, article.keywords].join(' ').toLocaleLowerCase();
      return words.every(function (word) { return haystack.indexOf(word) !== -1; });
    });
    status.textContent = found.length + ' article(s) found.';
    results.innerHTML = found.map(function (article) {
      return '<article class="search-result" style="margin:0 0 24px">' +
        '<h3><a href="' + safe(article.url) + '">' + safe(article.title) + '</a></h3>' +
        (article.authors ? '<p>' + safe(article.authors) + '</p>' : '') +
        (article.doi ? '<p><strong>DOI:</strong> ' + safe(article.doi) + '</p>' : '') +
        '</article>';
    }).join('');
  }

  form.addEventListener('submit', function (event) {
    event.preventDefault();
    run(input.value);
    history.replaceState(null, '', '?q=' + encodeURIComponent(input.value.trim()));
  });
  var initial = new URLSearchParams(location.search).get('q') || '';
  if (initial) { input.value = initial; run(initial); }
}());
