<?php
declare(strict_types=1);

// This endpoint tracks only the locally added VIS article (2534).
$action = $_GET['action'] ?? 'stats';
if (!in_array($action, ['stats', 'read', 'download'], true)) {
    http_response_code(400); exit;
}
$method = $_SERVER['REQUEST_METHOD'] ?? 'GET';
if (($action === 'read' && $method !== 'POST') || ($action !== 'read' && !in_array($method, ['GET', 'HEAD'], true))) {
    http_response_code(405); exit;
}
$pdf = __DIR__ . '/assets/pdfs/Artikel_Fitri_dan_Bintang_JBMH.pdf';
if ($action === 'download' && !is_file($pdf)) {
    http_response_code(404); exit('PDF unavailable.');
}
$directory = getenv('UNPAD_STATS_DIR') ?: dirname(__DIR__) . '/UNPAD-runtime/statistics';
if (!is_dir($directory) && !@mkdir($directory, 0750, true) && !is_dir($directory)) {
    http_response_code(503); exit('Statistics unavailable.');
}
$handle = @fopen($directory . '/2534.json', 'c+');
if (!$handle || !flock($handle, LOCK_EX)) {
    http_response_code(503); exit('Statistics unavailable.');
}
$raw = stream_get_contents($handle);
$counts = $raw === '' ? ['read' => 10, 'download' => 3] : json_decode($raw, true);
if (!is_array($counts) || !isset($counts['read'], $counts['download'])) {
    flock($handle, LOCK_UN); fclose($handle);
    http_response_code(503); exit('Statistics unavailable.');
}
// Keep existing totals when upgrading the earlier counter format.
$counts['visitors'] ??= ['read' => [], 'download' => []];
$counts['ip_salt'] ??= bin2hex(random_bytes(32));
if ($method !== 'HEAD' && $action !== 'stats') {
    // REMOTE_ADDR is supplied by the server; forwarded headers can be spoofed.
    $address = inet_pton($_SERVER['REMOTE_ADDR'] ?? '') ;
    if ($address !== false) {
        $visitor = hash_hmac('sha256', $address, $counts['ip_salt']);
        if (!isset($counts['visitors'][$action][$visitor])) {
            $counts['visitors'][$action][$visitor] = true;
            $counts[$action]++;
        }
    }
}
rewind($handle);
ftruncate($handle, 0);
fwrite($handle, json_encode($counts));
fflush($handle);
flock($handle, LOCK_UN);
fclose($handle);
header('Cache-Control: no-store');
if ($action === 'download') {
    header('Content-Type: application/pdf');
    header('Content-Disposition: attachment; filename="Artikel_Fitri_dan_Bintang_JBMH.pdf"');
    header('Content-Length: ' . filesize($pdf));
    if ($method !== 'HEAD') { readfile($pdf); }
} else {
    header('Content-Type: application/json; charset=utf-8');
    if ($method !== 'HEAD') { echo json_encode(['read' => $counts['read'], 'download' => $counts['download']]); }
}
