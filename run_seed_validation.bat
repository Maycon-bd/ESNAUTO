@echo off
setlocal
cd /d "%~dp0"

where Rscript >nul 2>nul
if %errorlevel%==0 (
  set "RSCRIPT=Rscript"
) else (
  if exist "C:\Program Files\R\R-4.6.0\bin\Rscript.exe" (
    set "RSCRIPT=C:\Program Files\R\R-4.6.0\bin\Rscript.exe"
  ) else (
    echo ERRO: Rscript nao encontrado no PATH nem em C:\Program Files\R\R-4.6.0\bin.
    echo Abra o terminal com R instalado ou ajuste este arquivo.
    pause
    exit /b 1
  )
)

echo ============================================================
echo ESNAUTO - Validacao estatistica por sementes
echo 3 cenarios x 30 seeds = 90 execucoes
echo ============================================================
echo.

"%RSCRIPT%" Scripts\run_seed_validation.R --asset PETR4 --seeds 30 --seed-base 202700

echo.
echo Execucao finalizada. Confira Scripts\results\seed_validation\
pause
