# Análise complementar Diebold–Mariano

## Análise inferencial concluída

Os quatro testes bilaterais pré-especificados foram executados exclusivamente sobre o CSV congelado, após validação do SHA-256. As quatro hipóteses nulas foram rejeitadas a 5%, com diferencial médio negativo e menor perda média da ESN. Resultados: `Scripts/results/diebold_mariano/controlled_runs/seed_20260926/dm/`. O complemento acadêmico atualizado está em `docs/10_diebold_mariano_tfc.md`.

## Execução científica controlada concluída — DM ainda não executado

A única rodada pré-especificada com seed 20260926 foi concluída para ESN, GRU e LSTM. Os três modelos produziram 1299 previsões de teste, foram persistidos e recarregados em processos novos com diferença máxima zero. A junção por data e a seleção `data >= 2015-09-30` congelaram 1298 observações em `Scripts/results/diebold_mariano/controlled_runs/seed_20260926/predictions/previsoes_dm.csv`.

Relatório: `Scripts/results/diebold_mariano/controlled_runs/seed_20260926/RELATORIO_EXECUCAO_CONTROLADA.md`. Manifesto e hashes: `execution_manifest.json` no mesmo diretório. **O teste Diebold–Mariano não foi executado.** O próximo passo exige autorização específica e deve consumir somente o CSV congelado validado pelo manifesto.

## Fase I.2 — executor pronto, execução científica pendente

**APTO PARA EXECUÇÃO CIENTÍFICA CONTROLADA: SIM**, após preparação local e dois smoke tests por modelo (uma época por baseline, mesma seed 20260926). Diferenças numéricas entre processos: zero para matrizes/pesos/previsões. Relatório: `Scripts/results/diebold_mariano/preparacao_executor/RELATORIO_EXECUTOR.md`. Dependências e locks: `Scripts/results/diebold_mariano/ambiente/`. Resultados exclusivamente técnicos: `Scripts/results/diebold_mariano/smoke_test/`.

O novo protocolo, determinado pelo usuário na Fase I.2, **corrige** a fronteira de Wout (alvos até 2600) e usa contexto cronológico completo treino→validação→teste. Isso sucede a proposta anterior de preservar o comportamento histórico. Os relatos das fases anteriores abaixo foram mantidos como histórico, não como instruções vigentes.

Os novos executores são `00_environment_check.R`, `01_prepare_data.R`, `02_esn_controlled.R`, `03_gru_controlled.R`, `04_lstm_controlled.R`, `05_validate_predictions.R` e `06_diebold_mariano.R`. O último não foi executado. Scripts 01/02 com nomes em português pertencem à recuperação histórica anterior e não devem ser usados na rodada controlada.

Executar a partir da raiz do repositório. Exemplo exclusivamente técnico, usando nome de saída ainda inexistente:

```powershell
& 'C:\Program Files\R\R-4.6.0\bin\Rscript.exe' Scripts/diebold_mariano/03_gru_controlled.R --smoke Scripts/results/diebold_mariano/smoke_test/NOVO_ID/gru
```

Não executar novamente por rotina: as verificações já passaram. Uma execução científica futura exige autorização separada, registro `scientific_execution_authorized=true` na configuração e variável de processo `ESNAUTO_AUTHORIZE_SCIENTIFIC=YES`. DM exige adicionalmente `ESNAUTO_AUTHORIZE_DM=YES`. Nenhuma dessas autorizações está ativada. As saídas científicas devem usar novos diretórios em `controlled_runs/`; os executores recusam sobrescrita. Nenhum modelo completo ou teste DM foi executado nesta etapa.

## Fase I — protocolo controlado, 26/09/2026

O usuário autorizou planejar uma **nova ESN controlada**, com hiperparâmetros registrados da GA_RUN_0030 e seed-base 20260926, sem executar modelos nesta fase. A configuração vigente está em `Scripts/results/diebold_mariano/configuracao_experimento.json`; a anterior foi preservada em `preflight_fase_I/configuracao_anterior_auditoria.json`. Relatório completo, JSON integral, validações de dados e evidências: `Scripts/results/diebold_mariano/preflight_fase_I/RELATORIO_PRE_FLIGHT.md`.

**APTO PARA EXECUÇÃO CONTROLADA: NÃO**, por ambiente/executor ainda não preparados. A falta dos pesos históricos não impede conceitualmente a nova ESN autorizada. Os scripts 01/02 abaixo continuam correspondendo à recuperação histórica e não devem ser usados para essa nova rodada sem adaptação. Apenas `00_validar_preflight.R` foi executado nesta fase, sem carregar modelos. O relato abaixo permanece como registro da auditoria anterior.

Estado em 26/09/2026: **bloqueada por falta das matrizes/previsões históricas da GA_RUN_0030**. A auditoria foi executada; os quatro testes não foram calculados. Este diretório não constitui uma reprodução concluída nem uma nova execução controlada.

## Execução realizada

Na raiz do projeto, com R 4.6.0:

```powershell
& 'C:\Program Files\R\R-4.6.0\bin\Rscript.exe' Scripts/diebold_mariano/01_gerar_previsoes_dm.R
```

O script depende apenas de R base, inventaria os arquivos e ZIPs, recupera os registros agregados, valida a série e as datas e registra o bloqueio. O código de saída 2 é intencional. Uma repetição exige outro diretório, passado como primeiro argumento: o script recusa sobrescrever saídas. O estágio de reinjeção/treinamento não foi implementado às cegas: depende da recuperação e confirmação dos artefatos históricos. O bloqueio ao final é específico do estado auditado e exige revisão antes de uma retomada.

Três tentativas parciais foram preservadas em `Scripts/results/diebold_mariano_tentativa_*`: duas envolveram configuração de locale/codificação no Windows e uma, fechamento de conexão ZIP. A execução final passou as verificações de integridade, datas e preservação. Esses incidentes não indicam corrupção dos arquivos científicos. Os avisos iniciais de locale do R permanecem registrados no terminal; o script define LC_CTYPE UTF-8 antes da leitura dos nomes.

Resultados da auditoria em `Scripts/results/diebold_mariano/`. Essa árvore já é ignorada pelo `.gitignore` do projeto: os artefatos existem localmente, mas não serão incluídos automaticamente em commits. Nenhum arquivo-base ou monografia foi alterado.

## Evidências e limitações

- ZIP de entrega: registro GA_RUN_0030, Laplace × Normal, a=0.111817, sr=0.215273, initLen=57, reservatório=22, reg=5.71625418786693e-05. MAE/RMSE históricos: 0.327224/0.498527. O registro não contém a seed nem os pesos.
- `melhor_recorde_global`: matrizes 16×2, 16×16 e 1×18, incompatíveis com 22×2, 22×22 e 1×24. O rastreador salva recordes por **validação**, não por teste; `eh_novo_recorde` da campeã é FALSE. Não há vínculo que autorize usar essas matrizes como GA_RUN_0030.
- As sessões/rankings locais são de 15/08/2026 e descrevem Normal, Uniforme e GED; a GA_RUN_0030 é de 20/08/2026. Os scripts R da raiz contêm cenários antigos distintos. O reservatório 22 mencionado em `resultados_validacao_teste.txt` pertence a GED × Uniforme, com outros parâmetros.
- Foram inventariados 39 contêineres ZIP (incluindo aninhados, com repetições) e 399 membros na busca inicial. Dois ZIPs removidos, recuperados de objetos alcançáveis do Git, acrescentam 55 membros: `inventario_git_zips.csv` e `ocorrencias_git.csv`. Também contêm registros agregados, não pesos da campeã. Cópias binárias em `evidencias_git/`, identificadas pelo SHA do objeto Git.
- Não foram localizados pesos/modelos/vetores oficiais de GRU/LSTM. O histórico DL do ZIP tem seis execuções com métricas diferentes das referências fornecidas. Nenhuma foi escolhida como substituta.
- `forecast`, `keras3`, `tensorflow`, `reticulate` e `jsonlite` não estão disponíveis nas bibliotecas R consultadas. Para retomada, instalar e registrar versões em ambiente separado. Não foi feita instalação nem iniciado treinamento sem a ESN recuperada.

## Auditoria temporal

Os arquivos oficiais contêm 5.198 valores finitos, datas únicas e crescentes de 03/01/2000 a 30/12/2020; diferença máxima entre preços dos dois arquivos: aproximadamente 1.02e-14.

Treino: índices 1–2600, até 01/07/2010. Validação: 2601–3899, de 02/07/2010 a 28/09/2015. Teste: 3900–5198, de 29/09/2015 a 30/12/2020. A ESN consome o índice 3900 para prever 3901; seus 1.298 alvos são 3901–5198. Baselines têm alvos 3900–5198. A interseção prevista pelo código é 3901–5198, **não um alinhamento de vetores efetivamente recuperados**.

Os módulos DL concatenam treino e teste, omitindo validação: o primeiro alvo tem última entrada em 01/07/2010 e não representa um passo consecutivo na série original. Ele não pertence à interseção com ESN. As nove janelas seguintes ainda incluem observações antigas do treino; a origem imediata já é t−1, mas a janela de dez observações cruza a lacuna. Corrigir essas janelas mudaria o protocolo histórico e não foi feito. A ESN também reinicializa o estado e percorre treino seguido de teste, pulando validação. O gráfico de teste do injetor usa datas da validação, razão adicional para nunca recuperar datas a partir da figura.

O extrator Python do injetor pode preencher linhas incompletas de W com zeros; não deve ser reutilizado sem validação estrita de completude. Nenhuma matriz foi completada, reajustada ou estimada nesta análise.

## Motor estatístico preparado, ainda não validado com vetores reais

`02_executar_dm.R` chama diretamente `forecast::dm.test`, com correção de Harvey–Leybourne–Newbold da implementação, h=1, power=1/2, bilateral e estimador `acf`. São quatro comparações e decisões individuais a 5%, sem ajuste de multiplicidade; nenhuma conclusão conjunta é autorizada. Referência: [documentação oficial forecast](https://pkg.robjhyndman.com/forecast/reference/dm.test.html).

Interface futura: `Rscript Scripts/diebold_mariano/02_executar_dm.R bundle_auditado.rds NOVO_DIRETORIO`.
O RDS deve conter `run='GA_RUN_0030'`, `esn_source='historical_recovered'`, `gru_source` e `lstm_source` (`historical_recovered` ou `controlled_rerun`), `h=1L`, `provenance_verified=TRUE` e tabelas `esn`, `gru`, `lstm`, com `data,real,previsto,data_origem,h`. A flag é uma declaração de auditoria, não prova automática da origem: anexar pesos, hashes, código de geração, versões, logs e seeds. A primeira previsão DL com origem descontínua deve ser excluída explicitamente desse bundle, conservando-a no arquivo bruto e documentando a exclusão.

O motor valida cada origem, valores reais contra a série, ausência de NA, ordem, datas únicas, 1.298 alvos e MAE/RMSE da ESN com tolerância absoluta 1e-6 antes do DM. É proibido montar esse bundle a partir de métricas agregadas. Sem os dados, foram validados apenas sintaxe e bloqueio de execução sem entrada; o caminho numérico de DM **não foi testado**. Não há promessa de geração automática do documento acadêmico numa futura execução.

## Retomada necessária

Recuperar Win/W/Wout da campeã com proveniência; reinjetar usando a lógica de `esn_core.R` e validar métricas. Se isso permanecer impossível, a reprodução histórica não pode ser concluída. Uma nova ESN exigiria protocolo separado e identificação explícita; não foi escolhida unilateralmente. GRU/LSTM poderão então ter nova rodada controlada (50 unidades, janela 10, dropout 0.2, Adam, 80 épocas, Min-Max só no treino, batch 16 do módulo), com seeds em R/Python/NumPy/TensorFlow/Keras, versões, pesos e logs, sem buscar os MAEs históricos.

