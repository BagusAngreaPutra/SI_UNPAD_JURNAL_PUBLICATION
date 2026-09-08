<?php
// CLI-only bootstrap of the isolated local OJS instance.
if (PHP_SAPI !== 'cli') { http_response_code(404); exit; }
$root = dirname(__DIR__);
$runtime = dirname($root) . '/UNPAD-runtime';
$secrets = json_decode(file_get_contents($runtime . '/local-secrets.json'), true, 512, JSON_THROW_ON_ERROR);
$config = $root . '/ojs/config.inc.php';
if (file_exists($config) && preg_match('/^installed\s*=\s*On/m', file_get_contents($config))) {
    exit("OJS is already installed.\n");
}
$pdo = new PDO('mysql:host=127.0.0.1;port=3308;charset=utf8mb4', 'root', $secrets['database_password'], [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
$pdo->exec('CREATE DATABASE IF NOT EXISTS unpad_ojs CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci');
$pdo->exec("CREATE USER IF NOT EXISTS 'unpad_ojs'@'127.0.0.1' IDENTIFIED BY " . $pdo->quote($secrets['database_password']));
$pdo->exec("GRANT ALL ON unpad_ojs.* TO 'unpad_ojs'@'127.0.0.1'");
@mkdir($runtime . '/files', 0700, true);
$contents = file_get_contents($root . '/ojs/config.TEMPLATE.inc.php');
$settings = ['app_key' => 'base64:' . base64_encode(random_bytes(32)),
    'base_url' => 'http://127.0.0.1:8000/ojs', 'host' => '127.0.0.1',
    'username' => 'unpad_ojs', 'password' => $secrets['database_password'], 'name' => 'unpad_ojs',
    'files_dir' => str_replace('\\', '/', $runtime . '/files'), 'time_zone' => 'Asia/Jakarta'];
foreach ($settings as $key => $value) {
    $contents = preg_replace('/^' . preg_quote($key, '/') . '\s*=.*$/m', $key . ' = "' . $value . '"', $contents);
}
$contents = str_replace('; port = 3306', 'port = 3308', $contents);
$contents = str_replace('default = sendmail', 'default = smtp', $contents);
$contents = str_replace('; smtp_server = mail.example.com', 'smtp_server = 127.0.0.1', $contents);
$contents = str_replace('; smtp_port = 25', 'smtp_port = 1025', $contents);
$contents = str_replace('task_runner = On', 'task_runner = Off', $contents);
$contents = preg_replace('/^allowed_hosts\s*=.*$/m', 'allowed_hosts = \'["127.0.0.1", "localhost"]\'', $contents);
file_put_contents($config, $contents);
require $root . '/ojs/tools/bootstrap.php';
$tool = new class([]) extends \PKP\cliTool\CommandLineTool {};
$installer = new \APP\install\Install([
    'locale' => 'en', 'additionalLocales' => ['en', 'id'],
    'filesDir' => str_replace('\\', '/', $runtime . '/files'),
    'adminUsername' => 'admin', 'adminPassword' => $secrets['admin_password'],
    'adminPassword2' => $secrets['admin_password'], 'adminEmail' => 'admin@localhost.test',
    'databaseDriver' => 'mysqli', 'databaseHost' => '127.0.0.1', 'databasePort' => 3308,
    'databaseUsername' => 'unpad_ojs', 'databasePassword' => $secrets['database_password'],
    'databaseName' => 'unpad_ojs', 'timeZone' => 'Asia/Jakarta',
    'oaiRepositoryId' => 'jbmh.local', 'enableBeacon' => false,
]);
if (!$installer->execute()) { fwrite(STDERR, $installer->getErrorString() . "\n"); exit(1); }
if (!$installer->wroteConfig()) { file_put_contents($config, $installer->getConfigContents()); }
echo "OJS installed successfully.\n";
