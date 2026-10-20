param([string]$Python = 'python', [string]$BrowserPath = '', [string]$DistPath = 'release', [string]$WorkPath = 'build')
$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
if (-not $BrowserPath) { $BrowserPath = Join-Path $PSScriptRoot 'build-browsers' }
$BrowserPath = [System.IO.Path]::GetFullPath($BrowserPath)
$env:PLAYWRIGHT_BROWSERS_PATH = $BrowserPath
& $Python -m playwright install chromium --no-shell
if ($LASTEXITCODE -ne 0) { throw 'Chromium installation failed' }
$BrowserData = @()
Get-ChildItem -LiteralPath $BrowserPath -Directory | Where-Object { $_.Name -match '^(chromium-|ffmpeg-|winldd-)' } | ForEach-Object { $BrowserData += @('--add-data', "$($_.FullName);browsers/$($_.Name)") }
& $Python -m PyInstaller --noconfirm --onedir --console --name PublicWebAdDetector --distpath $DistPath --workpath $WorkPath --specpath $WorkPath --add-data "$PSScriptRoot/detector/dom.js;detector" @BrowserData --collect-all playwright "$PSScriptRoot/main.py"
if ($LASTEXITCODE -ne 0) { throw 'Packaging failed' }
& $Python -m tests.fix_windows_icu $DistPath
if ($LASTEXITCODE -ne 0) { throw 'Windows ICU validation failed' }
Write-Output 'Build complete. Distribute the whole PublicWebAdDetector directory, including _internal.'
