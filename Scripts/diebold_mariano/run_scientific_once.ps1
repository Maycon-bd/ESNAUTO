$ErrorActionPreference = 'Stop'
$runRelative = 'Scripts/results/diebold_mariano/controlled_runs/seed_20260926'
$runPath = Join-Path $PWD $runRelative
if (Test-Path -LiteralPath $runPath) { throw 'Run already exists. No overwrite or automatic retraining allowed.' }
$rscript = 'C:\Program Files\R\R-4.6.0\bin\Rscript.exe'
$configPath = Join-Path $PWD 'Scripts/results/diebold_mariano/configuracao_experimento.json'
$config = Get-Content -LiteralPath $configPath -Raw | ConvertFrom-Json
if (-not $config.apto_para_execucao_controlada -or $config.seed_base -ne 20260926) { throw 'Invalid frozen protocol' }
New-Item -ItemType Directory -Path $runPath | Out-Null
foreach ($name in @('logs','models','predictions','validation','metrics','scripts')) {
    New-Item -ItemType Directory -Path (Join-Path $runPath $name) | Out-Null
}
Copy-Item -LiteralPath $configPath -Destination (Join-Path $runPath 'global_config_before.json')
$config.scientific_execution_authorized = $true
$config | ConvertTo-Json -Depth 40 | Set-Content -LiteralPath (Join-Path $runPath 'run_config.json') -Encoding utf8NoBOM
$env:ESNAUTO_CONFIG_PATH = Join-Path $runPath 'run_config.json'
$env:ESNAUTO_AUTHORIZE_SCIENTIFIC = 'YES'
$env:ESNAUTO_AUTHORIZE_DM = 'NO'
$start = [DateTime]::UtcNow.ToString('o')
@{ started_utc=$start; seed=20260926; scientific_execution=$true; dm_executed=$false; automatic_retries=0 } |
    ConvertTo-Json | Set-Content -LiteralPath (Join-Path $runPath 'run_start.json') -Encoding utf8NoBOM
Get-ChildItem 'Scripts/diebold_mariano' -File | ForEach-Object {
    Copy-Item -LiteralPath $_.FullName -Destination (Join-Path $runPath "scripts/$($_.Name)")
}
Get-ChildItem 'Scripts/diebold_mariano' -File | ForEach-Object { Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256 } |
    Export-Csv (Join-Path $runPath 'validation/scripts_before.csv') -NoTypeInformation
function Invoke-Stage($name, $script, $scriptArgs) {
    $event = [ordered]@{stage=$name; start_utc=[DateTime]::UtcNow.ToString('o'); seed=20260926; attempt=1}
    & $rscript "Scripts/diebold_mariano/$script" @scriptArgs *> (Join-Path $runPath "logs/$name.log")
    $code = $LASTEXITCODE
    $event['end_utc'] = [DateTime]::UtcNow.ToString('o')
    $event['exit_code'] = $code
    $event | ConvertTo-Json -Compress | Add-Content (Join-Path $runPath 'logs/execution_events.jsonl') -Encoding utf8
    if ($code -ne 0) { throw "Technical failure in $name (exit $code). Stopped; no automatic retry." }
    Write-Output "PASS $name"
}
Invoke-Stage 'train_esn' '02_esn_controlled.R' @('--scientific', "$runRelative/esn")
Invoke-Stage 'train_gru' '03_gru_controlled.R' @('--scientific', "$runRelative/gru")
Invoke-Stage 'train_lstm' '04_lstm_controlled.R' @('--scientific', "$runRelative/lstm")
Invoke-Stage 'package_models' '08_package_scientific.R' @('--models', $runRelative)
foreach ($model in @('esn','gru','lstm')) {
    Invoke-Stage "reload_$model" '07_reload_scientific.R' @($model, $runRelative)
}
Invoke-Stage 'freeze_predictions' '08_package_scientific.R' @('--freeze', $runRelative)
Write-Output 'All model/prediction stages complete. DM was not executed. Global configuration unchanged pending manifest/report.'
