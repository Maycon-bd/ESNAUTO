$videoRoot = $PSScriptRoot
$ffmpegExe = Get-ChildItem -LiteralPath (Join-Path $videoRoot 'bin/ffmpeg-dist') -Filter ffmpeg.exe -Recurse | Select-Object -First 1
if (-not $ffmpegExe) { throw 'FFmpeg não encontrado.' }
$env:PATH = "$($ffmpegExe.DirectoryName);$(Join-Path $videoRoot '.venv/Scripts');$(Join-Path $videoRoot 'node_modules/.bin');$env:PATH"
$chromePath = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
if (Test-Path -LiteralPath $chromePath) { $env:HYPERFRAMES_BROWSER_PATH = $chromePath }
Write-Host 'Ferramentas de vídeo disponíveis nesta sessão: ffmpeg, ffprobe, whisper, remotion, hyperframes.'
