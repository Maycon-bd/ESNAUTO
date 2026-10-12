@echo off
cls
echo ============================================================
echo           Orquestrador de Simulacoes ESN - TCC
echo ============================================================
echo.
set "acao=PETR4"
echo Escolha a acao: 1 - PETR4 / 2 - VALE3
set /p ativo="Digite 1 ou 2 (padrao PETR4): "
if "%ativo%"=="2" set "acao=VALE3"
echo Acao selecionada: %acao%
echo.
echo Escolha o modo de execucao:
echo 1 - Executar MODO TESTE (200 geracoes - Simula os 4 cenarios, Runs 1, 2, 3)
echo 2 - Executar MODO COMPLETO DO TCC (10000 geracoes - Execucao real)
echo 3 - Sair
echo.
set /p opt="Digite a opcao desejada (1, 2 ou 3): "

if "%opt%"=="1" goto TEST
if "%opt%"=="2" goto PROD
if "%opt%"=="3" goto EXIT
goto END

:TEST
echo.
echo Iniciando Modo Teste rapido...
python automate_simulations.py --test --acao %acao%
goto END

:PROD
echo.
echo Iniciando Modo Completo do TCC (10.000 geracoes)...
python automate_simulations.py --acao %acao%
goto END

:EXIT
exit

:END
echo.
echo Execucao finalizada.
pause
