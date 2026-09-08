<?php
declare(strict_types=1);
@set_time_limit(300);

$article = $_GET['article'] ?? '';
$galley = $_GET['galley'] ?? '';
if (!preg_match('/^[A-Za-z0-9._%-]+$/', $article) || !preg_match('/^[A-Za-z0-9._%-]+$/', $galley)) {
    http_response_code(400);
    exit('Invalid PDF identifier.');
}

$cacheDir = __DIR__ . '/assets/pdfs';
$cacheFile = $cacheDir . '/' . $article . '-' . $galley . '.pdf';
if (is_file($cacheFile) && filesize($cacheFile) > 5) {
    header('Content-Type: application/pdf');
    header('Content-Disposition: inline; filename="jbmh-' . $article . '.pdf"');
    header('Content-Length: ' . filesize($cacheFile));
    readfile($cacheFile);
    exit;
}

if (!is_dir($cacheDir)) {
    @mkdir($cacheDir, 0755, true);
}
$source = 'https://jurnal.fh.unpad.ac.id/index.php/jbmh/article/download/' . rawurlencode($article) . '/' . rawurlencode($galley);
$temp = $cacheFile . '.part';
$handle = @fopen($temp, 'wb');
if (!$handle || !function_exists('curl_init')) {
    http_response_code(503);
    exit('PDF service is unavailable.');
}
$curl = curl_init($source);
curl_setopt_array($curl, [
    CURLOPT_FILE => $handle,
    CURLOPT_FOLLOWLOCATION => true,
    CURLOPT_CONNECTTIMEOUT => 20,
    CURLOPT_TIMEOUT => 240,
    CURLOPT_IPRESOLVE => CURL_IPRESOLVE_V4,
    CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
    CURLOPT_USERAGENT => 'JBMH PDF archive',
    CURLOPT_FAILONERROR => true,
]);
$ok = curl_exec($curl);
$contentType = (string) curl_getinfo($curl, CURLINFO_CONTENT_TYPE);
curl_close($curl);
fclose($handle);

$header = is_file($temp) ? (string) file_get_contents($temp, false, null, 0, 5) : '';
if (!$ok || $header !== '%PDF-') {
    @unlink($temp);
    http_response_code(502);
    exit('PDF could not be retrieved. Please try again.');
}
@rename($temp, $cacheFile);
header('Content-Type: application/pdf');
header('Content-Disposition: inline; filename="jbmh-' . $article . '.pdf"');
header('Content-Length: ' . filesize($cacheFile));
readfile($cacheFile);
