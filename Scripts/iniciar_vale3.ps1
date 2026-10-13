$ErrorActionPreference = 'Stop'
$raizProjeto = Split-Path -Parent $PSScriptRoot
$saidaRotina = Join-Path $raizProjeto 'Scripts/results/VALE3/producao_comparacao'
New-Item -ItemType Directory -Path $saidaRotina -Force | Out-Null
$ativos = Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'Rscript.exe' -and $_.CommandLine -like '*vale3_rotina.R*' }
if ($ativos) { Write-Output "Rotina VALE3 já ativa: PID $($ativos.ProcessId)"; exit 0 }
if (Test-Path (Join-Path $saidaRotina 'resultados_consolidados.csv')) { Write-Output 'Rotina VALE3 concluída; resultados disponíveis.'; exit 0 }
$rExecutavel = 'C:/Program Files/R/R-4.6.0/bin/Rscript.exe'
if (-not (Test-Path $rExecutavel)) { throw 'Rscript não encontrado.' }
$scriptRotina = Join-Path $PSScriptRoot 'vale3_rotina.R'
$argumentosRotina = '--vanilla "' + $scriptRotina + '" "' + $raizProjeto + '"'
$sufixoLog = Get-Date -Format 'yyyyMMdd_HHmmss'
$processoRotina = Start-Process -FilePath $rExecutavel -ArgumentList $argumentosRotina -WorkingDirectory $raizProjeto -WindowStyle Hidden -RedirectStandardOutput (Join-Path $saidaRotina "execucao_$sufixoLog.log") -RedirectStandardError (Join-Path $saidaRotina "erros_$sufixoLog.log") -PassThru
$processoRotina.Id | Set-Content (Join-Path $saidaRotina 'pid.txt')
Write-Output "Rotina VALE3 iniciada: PID $($processoRotina.Id). Resultados: $saidaRotina"
