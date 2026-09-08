$ErrorActionPreference = 'Stop'
$projectPath = $PSScriptRoot
$runtimePath = Join-Path (Split-Path $projectPath -Parent) 'UNPAD-runtime'
$databasePath = Join-Path $runtimePath 'database'
if (-not (Test-Path -LiteralPath $databasePath)) { throw 'Database lokal belum disiapkan.' }
function Test-LocalPort([int]$Port) {
    $client = New-Object System.Net.Sockets.TcpClient
    try { $client.Connect('127.0.0.1', $Port); return $true } catch { return $false } finally { $client.Dispose() }
}
if (-not (Test-LocalPort 3308)) {
    Start-Process -FilePath 'C:\xampp\mysql\bin\mysqld.exe' -ArgumentList @('--no-defaults', ('--datadir="' + $databasePath + '"'), '--port=3308', '--bind-address=127.0.0.1', '--max-allowed-packet=64M') -WindowStyle Hidden -RedirectStandardOutput (Join-Path $runtimePath 'mysql-out.log') -RedirectStandardError (Join-Path $runtimePath 'mysql-error.log')
}
if (-not (Test-LocalPort 1025)) {
    $pythonPath = (Get-Command python.exe).Source
    Start-Process -FilePath $pythonPath -WorkingDirectory $projectPath -ArgumentList @('scripts/local_mail.py') -WindowStyle Hidden -RedirectStandardOutput (Join-Path $runtimePath 'mail-out.log') -RedirectStandardError (Join-Path $runtimePath 'mail-error.log')
}
if (-not (Test-LocalPort 8000)) {
    Start-Process -FilePath 'C:\xampp\php\php.exe' -WorkingDirectory $projectPath -ArgumentList @('-d', 'extension=intl', '-d', 'memory_limit=512M', '-d', 'upload_max_filesize=25M', '-d', 'post_max_size=30M', '-d', 'display_errors=Off', '-S', '127.0.0.1:8000', 'router.php') -WindowStyle Hidden -RedirectStandardOutput (Join-Path $runtimePath 'php-out.log') -RedirectStandardError (Join-Path $runtimePath 'php-error.log')
}
Write-Host 'Web: http://127.0.0.1:8000'
Write-Host 'Login OJS: http://127.0.0.1:8000/ojs/index.php/jbmh/login'
