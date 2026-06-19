# DedupeCSV GUI exe ビルドスクリプト
$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root

Write-Host "Installing dependencies..."
pip install -q -r requirements.txt -r requirements-dev.txt
pip install -e .

Write-Host "Building GUI exe with PyInstaller..."
pyinstaller --onefile --name dedupcsv-gui `
  --paths src `
  --windowed `
  --collect-all customtkinter `
  src/dedupcsv/gui.py

Write-Host "Done: dist\dedupcsv-gui.exe"
