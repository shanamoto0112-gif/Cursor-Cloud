# DedupeCSV exe ビルドスクリプト
$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root

Write-Host "Installing dependencies..."
pip install -q -r requirements.txt -r requirements-dev.txt
pip install -q -e .

Write-Host "Building exe with PyInstaller..."
pyinstaller --onefile --name dedupcsv `
  --paths src `
  --console `
  src/dedupcsv/cli.py

Write-Host "Done: dist\dedupcsv.exe"
