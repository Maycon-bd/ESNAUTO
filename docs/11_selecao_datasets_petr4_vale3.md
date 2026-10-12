# Seleção de datasets e resultados PETR4 × VALE3

O Studio permite escolher PETR4 ou VALE3 no seletor **Ação para previsão**, acima das abas. A ação é carregada imediatamente. O botão **Recarregar Ação Selecionada** restaura o arquivo do projeto e as partições padrão. A troca limpa os resultados dos modelos, o comparativo em memória e o resumo da última execução. A seleção é bloqueada enquanto um modelo estiver executando.

## Dados e protocolo

Os arquivos em `Scripts/data/` contêm uma coluna de preços de fechamento com fator, sem cabeçalho. O arquivo VALE3 fornecido foi copiado integralmente para o projeto. O carregador valida preços numéricos, finitos e positivos; preserva a ordem das observações e não preenche pregões ausentes.

| Dataset | Total | Treino | Validação | Teste |
|---|---:|---:|---:|---:|
| PETR4 | 5.198 | 2.600 | 1.299 | 1.299 |
| VALE3 | 5.192 | 2.596 | 1.298 | 1.298 |

A divisão de PETR4 mantém o protocolo histórico. Para VALE3, utiliza-se 50%/25%/25%, calculado pelo tamanho da série. A configuração da aba Dados é transmitida à ESN, ao GA e aos modelos LSTM/GRU. Não é necessário cortar VALE3 ou completar artificialmente sua série para igualar os tamanhos.

O arquivo VALE3 não inclui datas. Por isso, seus gráficos utilizam índices de observação. O intervalo 2000–2020 vem do nome do arquivo; as datas dos pregões não foram verificadas individualmente. As duas séries não foram alinhadas por datas.

Os presets ESN reaproveitam hiperparâmetros e matrizes do reservatório, mas treinam novamente a matriz de saída com o treino da ação escolhida. Para a análise principal da monografia, execute uma otimização GA própria para cada ação. Os parâmetros EasyFit da Onda 5 continuam sendo os ajustes originalmente obtidos em PETR4; a seleção de VALE3 não estima novos ajustes dessas distribuições.

## Execução e persistência

```powershell
python automate_simulations.py --acao VALE3 --test --run 1
python automate_simulations.py --acao VALE3 --itera 10000
python automate_simulations.py --acao PETR4 --itera 10000
```

O modo `--test` ainda executa 200 gerações por cenário, portanto pode demorar. Sem `--acao`, o batch usa PETR4. O script R recebe a ação no sexto argumento, após o diretório de saída.

O histórico GA de VALE3 fica em `Scripts/results/VALE3/historico_otimizacoes_ga.csv`, o histórico DL em `Scripts/results/VALE3/historico_dl_benchmark.csv` e as matrizes recordistas em `Scripts/results/VALE3/melhor_recorde_global/`. Os caminhos históricos de PETR4 são preservados. Comparações de recordes usam apenas o histórico da mesma ação. A interface não cria métricas de referência quando não há um resultado treinado disponível.

Sessões batch usam o sufixo da ação no nome da pasta. O manifesto `dataset.json` registra ação, nome do arquivo, quantidade de observações, partições e hash SHA-256. O pipeline respeita o dataset da sessão nos gráficos e nos relatórios; o pacote final inclui esse manifesto. Sessões antigas sem manifesto continuam sendo interpretadas como PETR4.

## Registro para a monografia

Execute as baterias de produção separadamente, mantendo o mesmo orçamento do GA, distribuições, número de rodadas e hiperparâmetros de Deep Learning. Registre também sementes aleatórias, versões e hardware. Preserve os diretórios das sessões e os arquivos de histórico junto dos resultados publicados.

Apresente por ação e por modelo: MAE e RMSE de validação e teste, R² de teste, tempo de execução, configurações e variabilidade entre rodadas. Como os ativos possuem escalas de preços diferentes, interprete os erros em reais dentro de cada ação e use métricas relativas calculadas nas execuções quando for comparar ativos.

Texto metodológico inicial, a complementar depois das baterias:

> O sistema foi ampliado para permitir a seleção de duas séries de preços de fechamento com fator, PETR4 e VALE3. Os dados foram divididos em ordem temporal, com aproximadamente 50% das observações destinadas ao treinamento, 25% à validação e 25% ao teste. Para PETR4 foram preservadas as partições do experimento original, enquanto para VALE3 os tamanhos foram calculados a partir das 5.192 observações disponíveis. Cada modelo foi executado sobre a série selecionada, com persistência separada dos históricos e recordes por ativo.

Esse texto descreve a adaptação do software. Os testes de integração e de inferência não substituem os resultados das baterias científicas. A monografia existente não foi alterada nesta implementação.

## Verificação da implementação

```powershell
Rscript Scripts/test_dataset_selection.R
python Scripts/test_dataset_selection.py
```

Os testes R verificam leitura, partições, alternância de ação, limpeza de resultados, bloqueio durante execução, isolamento dos históricos e inferência ESN real nas duas séries com um reservatório pequeno. Os testes Python verificam o manifesto e a passagem da ação ao batch com o subprocesso de treinamento simulado, além da geração do script de avaliação da ação selecionada. As baterias completas de GA e treinamento LSTM/GRU não fazem parte desses testes.
