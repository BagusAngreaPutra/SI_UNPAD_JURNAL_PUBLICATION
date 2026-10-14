<?php
// Router for the local PHP server. Private runtime data lives outside this root.
$path = rawurldecode(parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH) ?: '/');
if (str_contains($path, "\0") || str_contains($path, '\\') || preg_match('~(?:^|/)\.\.(?:/|$)~', $path)) {
    http_response_code(400); exit;
}
header('Cache-Control: no-cache, must-revalidate');
if ($path === '/ojs' || $path === '/ojs/') {
    header('Location: /ojs/index.php/jbmh'); exit;
}
if (preg_match('~^/ojs/index\.php(?:/|$)~', $path)) { return false; }
if ($path === '/article-stats.php') { require __DIR__ . '/article-stats.php'; return true; }
if ($path === '/') { header('Location: /index.php/jbmh', true, 302); return true; }
if (strcasecmp($path, '/voluem10view') === 0 || strcasecmp($path, '/voluem10view/') === 0) {
    header('Location: /issue/voluem10view.html', true, 302); return true;
}
$routes = [
    '~^/index\.php/(?:JBMH|jbmh)/?$~i' => 'index.html',
    '~^/index\.php/jbmh/article/view/([^/]+)/?$~i' => 'pages/article/view/$1.html',
    '~^/index\.php/jbmh/issue/view/([^/]+)/?$~i' => 'pages/issue/view/$1.html',
    '~^/index\.php/jbmh/issue/archive/?$~i' => 'issue/arcive.html',
    '~^/index\.php/jbmh/search/?$~i' => 'search.html',
];
foreach ($routes as $pattern => $target) {
    if (preg_match($pattern, $path, $matches)) {
        $target = isset($matches[1]) ? str_replace('$1', $matches[1], $target) : $target;
        $routeFile = __DIR__ . '/' . $target;
        if (is_file($routeFile)) { readfile($routeFile); return true; }
    }
}
$extensionless = __DIR__ . $path . '.html';
if (is_file($extensionless)) { readfile($extensionless); return true; }
$file = realpath(__DIR__ . $path);
$root = realpath(__DIR__) . DIRECTORY_SEPARATOR;
$allowed = ['html', 'css', 'js', 'png', 'jpg', 'jpeg', 'gif', 'svg', 'ico', 'woff', 'woff2', 'ttf', 'eot', 'webp', 'pdf', 'ris', 'bib'];
if ($file && str_starts_with($file, $root) && is_file($file)
    && !preg_match('~^/(?:scripts|\.git)(?:/|$)~', $path)
    && in_array(strtolower(pathinfo($file, PATHINFO_EXTENSION)), $allowed, true)) {
    return false;
}
http_response_code(404);
echo 'Not Found';
