# 配布用 zip 作成スクリプト
$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root

$releaseDir = Join-Path $root "release"
$staging = Join-Path $releaseDir "DedupeCSV-v1.0.0"
if (Test-Path $staging) { Remove-Item $staging -Recurse -Force }
New-Item -ItemType Directory -Path $staging | Out-Null

Copy-Item dist\dedupcsv.exe $staging\
Copy-Item README.md $staging\
Copy-Item LICENSE $staging\
Copy-Item tests\fixtures\sample.csv $staging\sample-input.csv

$zipPath = Join-Path $releaseDir "DedupeCSV-v1.0.0-win64.zip"
if (Test-Path $zipPath) { Remove-Item $zipPath -Force }
Compress-Archive -Path "$staging\*" -DestinationPath $zipPath

Write-Host "Created: $zipPath"
