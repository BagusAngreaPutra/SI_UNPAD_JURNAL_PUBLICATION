<?php
declare(strict_types=1);
$articles = require __DIR__ . '/config.php';
header('Cache-Control: no-store');
header('X-Content-Type-Options: nosniff');
header('X-Robots-Tag: noindex, nofollow');
$path = trim(rawurldecode(parse_url($_SERVER['REQUEST_URI'] ?? '/', PHP_URL_PATH) ?: '/'), '/');
if ($path === 'index.php') { $path = ''; }
elseif (strpos($path, 'index.php/') === 0) { $path = substr($path, 10); }
if ($path !== '') {
    if (!isset($articles[$path])) {
        http_response_code(404);
        header('Content-Type: text/plain; charset=utf-8');
        exit('Kode simulasi tidak ditemukan.');
    }
    $destination = $articles[$path];
    if (!filter_var($destination, FILTER_VALIDATE_URL) || parse_url($destination, PHP_URL_SCHEME) !== 'https') {
        http_response_code(500); exit('Alamat tujuan belum valid.');
    }
    header('Location: ' . $destination, true, 302); exit;
}
header('Content-Type: text/html; charset=utf-8');
?>
<!doctype html><html lang="id"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>DOI Reg — Simulasi</title><style>body{font:17px/1.6 system-ui;max-width:760px;margin:60px auto;padding:24px;background:#f6f8fb;color:#172d40}main{background:white;padding:32px;border-radius:16px}a{overflow-wrap:anywhere;color:#075bb4}</style></head><body><main><h1>DOI Reg</h1><p>Resolver simulasi artikel jurnal. Kode ini bukan DOI terdaftar.</p><h2>Reformulasi Pengaturan Victim Impact Statement (VIS) sebagai Penguatan Hak Korban dalam Sistem Peradilan Pidana Indonesia</h2><p>Fitri Anita &amp; Muhammad Amri Bintang</p><a href="/10.2498.jbmh.v10i2.2330">doi-reg.org/10.2498.jbmh.v10i2.2330</a></main></body></html>
