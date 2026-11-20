param(
    [Parameter(Mandatory = $true)][string]$Arquivo,
    [ValidateSet('tiny', 'base', 'small', 'medium', 'large', 'turbo')][string]$Modelo = 'base'
)
$ErrorActionPreference = 'Stop'
$arquivoResolvido = (Resolve-Path -LiteralPath $Arquivo).Path
. (Join-Path $PSScriptRoot 'ativar.ps1')
& (Join-Path $PSScriptRoot '.venv/Scripts/python.exe') -m whisper $arquivoResolvido --model $Modelo --model_dir (Join-Path $PSScriptRoot 'modelos') --language pt --task transcribe --device cpu --threads 2 --fp16 False --output_format all --output_dir (Join-Path $PSScriptRoot 'exportados')
if ($LASTEXITCODE -ne 0) { throw 'Falha na transcrição.' }
