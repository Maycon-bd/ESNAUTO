# ⚡ ESNAUTO — Automação ESN & GA + Benchmark Studio (PETR4)

[![R](https://img.shields.io/badge/R-4.6%2B-blue.svg)](https://www.r-project.org/)
[![Python](https://img.shields.io/badge/Python-3.8%2B-green.svg)](https://www.python.org/)
[![Shiny](https://img.shields.io/badge/Shiny-Studio-orange.svg)](https://shiny.posit.co/)
[![Keras](https://img.shields.io/badge/Keras-3.0%2B-red.svg)](https://keras.io/)
[![License](https://img.shields.io/badge/License-MIT-brightgreen.svg)]()

> **Trabalho de Conclusão de Curso (TCC) — Maycon Garcia Silva**  
> Previsão de Séries Temporais Financeiras (Ações PETR4 2000–2020) utilizando **Echo State Networks (ESN)** otimizadas por **Algoritmo Genético (GA)**, comparadas a modelos de Deep Learning Recorrente (**LSTM** e **GRU**) com interface gráfica interativa em **R Shiny**.

---

## 📌 Sumário
- [Visão Geral](#-visão-geral)
- [✨ Principais Recursos](#-principais-recursos)
- [📚 Documentação por Componente (`docs/`)](#-documentação-por-componente-docs)
- [📁 Arquitetura do Workspace](#-arquitetura-do-workspace)
- [⚙️ Pré-requisitos e Instalação](#️-pré-requisitos-e-instalação)
- [🚀 Como Executar](#-como-executar)
  - [1. Estúdio de Benchmark (R Shiny App)](#1-estúdio-de-benchmark-r-shiny-app)
  - [2. Automação de Simulações Batch (Python / Bat)](#2-automação-de-simulações-batch-python--bat)
  - [3. Pipeline de Resultados em 4 Fases](#3-pipeline-de-resultados-em-4-fases)
- [📊 Cenários e Hiperparâmetros Otimizados](#-cenários-e-hiperparâmetros-otimizados)
- [🏆 Resultados do Benchmark](#-resultados-do-benchmark)
- [📜 Licença e Créditos](#-licença-e-créditos)

---

## 🔍 Visão Geral

O projeto **ESNAUTO** foi desenvolvido para investigar e otimizar a capacidade preditiva da **Echo State Network (ESN)** — um paradigma de *Reservoir Computing* — aplicada ao mercado de ações brasileiro (PETR4 no período de 2000 a 2020). 

Para superar a sensibilidade da inicialização aleatória dos pesos do reservatório ($W$) e da matriz de entrada ($W_{in}$), o sistema utiliza um **Algoritmo Genético (GA)** para calibrar simultaneamente os hiperparâmetros globais da rede (taxa de vazão $a$, raio espectral $sr$, regularização Ridge $reg$, período de lavagem $initLen$ e tamanho do reservatório $tam\_reservoir$).

O repositório inclui:
1. **Pipeline de Automação Batch**: Orquestração end-to-end em Python e R para simulações com até 10.000 gerações em 12 cenários experimentais (3 Rodadas × 4 Combinações de Distribuição de Pesos).
2. **Pipeline de Pós-Processamento e Teste**: Análise estatística automatizada, extração das melhores matrizes e avaliação *out-of-sample* na partição de teste (25%).
3. **ESNAUTO Benchmark Studio**: Aplicação Web interativa desenvolvida em **R Shiny** com UI/UX moderna para comparação em tempo real entre **ESN**, **LSTM** e **GRU**.

---

## ✨ Principais Recursos

- 🧠 **Reservoir Computing Otimizado**: Suporte a distribuições de pesos **Normal**, **Uniforme** e **GED** (*Generalized Error Distribution*) para as matrizes $W_{in}$ e $W$.
- 🧬 **Otimização via Algoritmo Genético**: Ajuste automático dos hiperparâmetros vitais da ESN via pacote `GA` do R.
- 📈 **Deep Learning Benchmarking (LSTM & GRU)**: Implementação completa com `keras3` e backend `TensorFlow` para comparação rigorosa de acurácia (MAE, RMSE, MAPE, $R^2$) e custo computacional (tempo de treinamento).
- 📊 **Particionamento Temporal Rigoroso**: Divisão temporal da série PETR4 em **Treino (50% = 2.600 amostras)**, **Validação (25% = 1.299 amostras)** e **Teste Out-of-Sample (25% = 1.299 amostras)**.
- 🖥️ **ESNAUTO Studio (R Shiny)**: Interface com 6 abas (Dados, ESN, LSTM, GRU, Comparativo Custo-Benefício e Catálogo de Distribuições).
- 🛠️ **Arquitetura Orientada a Fases**: Pipeline modular em Python para ranqueamento JSON, reinjeção de matrizes ótimas e empacotamento de relatórios.

---

## 📚 Documentação por Componente (`docs/`)

Para facilitar o entendimento de cada módulo do sistema, o projeto conta com uma pasta unificada de documentação em [`docs/`](docs/INDEX.md):

| Componente | Documento | Conteúdo / Arquivos Explicados |
| :--- | :--- | :--- |
| 📌 **Índice Geral** | [`docs/INDEX.md`](docs/INDEX.md) | Mapa geral da documentação e navegação rápida. |
| ⚙️ **Orquestração & Simulação** | [`docs/01_orquestracao_e_simulacao.md`](docs/01_orquestracao_e_simulacao.md) | Explicação de `automate_simulations.py`, `run_simulations.bat`, `acoes_petr4_esn.R` e scripts de gráficos. |
| 🛠️ **Pipeline & Pós-Processamento** | [`docs/02_pipeline_pos_processamento.md`](docs/02_pipeline_pos_processamento.md) | Explicação do pipeline em 4 fases (`analyze_results.py`, `inject_and_test.py`, `package_results.py` e `scratch_*.py`). |
| 🖥️ **ESNAUTO Studio (Shiny)** | [`docs/03_app_shiny_studio.md`](docs/03_app_shiny_studio.md) | Explicação de `app/app.R`, módulos ESN/LSTM/GRU/Comparação, utilitários e CSS. |
| 📊 **Dados & Resultados** | [`docs/04_dados_e_resultados.md`](docs/04_dados_e_resultados.md) | Estrutura de dados PETR4 (`Scripts/data/`), sessões de resultado (`Scripts/results/`) e gráficos consolidados (`resultados_tcc/`). |
| 📄 **Relatórios & Monografia** | [`docs/05_relatorios_e_monografia.md`](docs/05_relatorios_e_monografia.md) | Detalhamento da monografia do TCC, relatório de arquitetura e tabelas de validação/teste. |

---

## 📁 Arquitetura do Workspace

```
ESNAUTO/
├── README.md                            # Documentação principal do projeto
├── automate_simulations.py              # Orquestrador central em Python (Simulações Batch)
├── run_simulations.bat                  # Script de atalho interativo no Windows
├── resultados_validacao_teste.md        # Relatório consolidado dos 12 cenários experimentais
├── resultados_validacao_teste2.md       # Cópia/Espelho de backup do relatório de validação
│
├── app/                                 # 🖥️ ESNAUTO Benchmark Studio (R Shiny)
│   ├── app.R                            # Arquivo principal da aplicação Shiny
│   ├── modules/                         # Módulos Shiny (mod_esn.R, mod_lstm.R, mod_gru.R, mod_comparacao.R)
│   ├── utils/                           # Funções auxiliares (data_prep.R, metrics.R)
│   └── www/                             # Estilos CSS customizados (custom.css)
│
├── docs/                                # 📚 Documentação Técnica por Componente
│   ├── INDEX.md
│   ├── 01_orquestracao_e_simulacao.md
│   ├── 02_pipeline_pos_processamento.md
│   ├── 03_app_shiny_studio.md
│   ├── 04_dados_e_resultados.md
│   └── 05_relatorios_e_monografia.md
│
├── reports/                             # 📄 Relatórios Acadêmicos e TCC
│   ├── Relatorio_Automacao_ESN.md       # Relatório de arquitetura e automação das simulações
│   ├── Relatorio_Automacao_ESN.docx     # Versão formatada em MS Word
│   └── MayconGarciaSilva_monografia.docx# Monografia completa do TCC
│
├── Scripts/                             # ⚙️ Scripts de Execução e Pipeline
│   ├── acoes_petr4_esn.R                # Script R parametrizado de treino ESN + GA
│   ├── analyze_results.py               # Fase 2: Análise de CSVs e geração do ranking.json
│   ├── inject_and_test.py               # Fase 3: Extração de matrizes ótimas e teste out-of-sample
│   ├── package_results.py               # Fase 4: Consolidação dos resultados na pasta entrega/
│   ├── gerar_graficos_corrigidos.R      # Script R para geração de gráficos estatísticos
│   │
│   ├── data/                            # 📊 Base de Dados Histórica PETR4 (2000-2020)
│   │   ├── PETR4_close com factor_2000-2020.txt
│   │   └── PETR4_close com factor_2000-2020_com data.csv
│   │
│   └── results/                         # 📂 Resultados das Execuções
│       └── Run_YYYYMMDD_HHMMSS_{Mode}/  # Sessão de simulação gerada automaticamente
│           ├── pdfs/                    # PDFs compilados de cada cenário
│           ├── zips/                    # Pacotes compactados para envio
│           ├── scenarios/               # Dados brutos dos cenários (CSVs, logs, matrizes)
│           └── entrega/                 # Pacote final com ranking, relatórios e gráficos
│
└── resultados_tcc/                      # 🖼️ Gráficos e resultados oficiais consolidados
    ├── grafico_teste_corrigido.png
    ├── grafico_validacao_corrigido.png
    └── resultados_ESN_PETR4.txt
```

---

## ⚙️ Pré-requisitos e Instalação

### 1. Ambiente R (v4.0 ou superior — Testado com R 4.6.0)
Instale os pacotes R necessários através do console do R:
```R
install.packages(c(
  "shiny", "ggplot2", "PerformanceAnalytics", "GA", 
  "pracma", "fitdistrplus", "MASS", "PearsonDS", "fGarch",
  "StockDistFit", "keras3"
))
```

### 2. Backend Deep Learning (Keras 3 / TensorFlow)
Para habilitar o treinamento interativo de LSTM e GRU no Shiny:
```R
# No console R:
keras3::install_keras()
```

### 3. Ambiente Python (v3.8 ou superior — Testado com Python 3.13)
O orquestrador Python utiliza apenas bibliotecas padrão (`os`, `sys`, `json`, `subprocess`, `shutil`, `argparse`, `datetime`, `random`). Não requer instalações adicionais via `pip`.

---

## 🚀 Como Executar

### 1. Estúdio de Benchmark (R Shiny App)
Para abrir a interface gráfica interativa do **ESNAUTO Studio**:

```powershell
# Pelo PowerShell / Terminal:
& 'C:\Program Files\R\R-4.6.0\bin\Rscript.exe' -e "shiny::runApp('app')"
```
Ou abra o arquivo `app/app.R` no RStudio e clique em **Run App**.

#### Abas disponíveis no Shiny Studio:
* 📊 **Dados PETR4**: Visualização da série histórica (5.198 amostras) e configuração de splits (Treino: 2.600, Validação: 1.299, Teste: 1.299).
* 🧠 **ESN (Reservoir)**: Ajuste de hiperparâmetros ($a$, $sr$, $initLen$, $tam\_reservoir$, $reg$) ou seleção de presets do GA, com projeção instantânea de resíduos.
* 📈 **LSTM Network**: Configuração de arquitetura recorrente (neurônios, timesteps, dropout, épocas, batch size) e treino via Keras 3 com curva de perda (*loss*).
* 📉 **GRU Network**: Treinamento de célula GRU sob os mesmos parâmetros para comparação direta.
* ⚖️ **Comparativo & Custo-Benefício**: Tabela lado a lado, gráficos de barras de MAE/RMSE de teste, gráfico de tempo de treinamento (speedup) e conclusão automática.
* 🎲 **Distribuições da ESN**: Catálogo e visualizador de amostragem teórica (Normal, Uniforme, GED, Cauchy, Laplace).

---

### 2. Automação de Simulações Batch (Python / Bat)

Você pode disparar a bateria completa de testes de duas maneiras:

#### Método A: Menu Interativo Windows
Dê dois cliques no arquivo `run_simulations.bat`:
- Opção `1`: **Modo Teste Rápido** (200 gerações GA para verificação do fluxo).
- Opção `2`: **Modo Produção Oficial** (10.000 gerações GA para o TCC).
- Opção `3`: Sair.

#### Método B: Linha de Comando (CLI)
```bash
# Rodar Modo Teste Rápido (200 gerações GA nos 12 cenários)
python automate_simulations.py --test

# Rodar Modo Produção Oficial (10.000 gerações GA em todas as 3 rodadas)
python automate_simulations.py

# Rodar apenas a rodada 2 em produção
python automate_simulations.py --run 2

# Definir número customizado de gerações do GA (ex: 5000)
python automate_simulations.py --itera 5000
```

---

### 3. Pipeline de Resultados em 4 Fases

Caso deseje reprocessar os resultados de uma pasta de execução (`Run_YYYYMMDD_HHMMSS`), execute a sequência de pós-processamento:

```bash
# Fase 2: Analisar logs/CSVs e gerar ranking.json
python Scripts/analyze_results.py Scripts/results/Run_YYYYMMDD_HHMMSS_Mode

# Fase 3: Reinjetar matrizes ótimas de todos os cenários e testar na partição Out-of-Sample
python Scripts/inject_and_test.py Scripts/results/Run_YYYYMMDD_HHMMSS_Mode

# Fase 4: Empacotar gráficos e relatórios finais na pasta /entrega
python Scripts/package_results.py Scripts/results/Run_YYYYMMDD_HHMMSS_Mode
```

---

## 📊 Cenários e Hiperparâmetros Otimizados

O Algoritmo Genético otimiza 5 hiperparâmetros fundamentais do reservatório:

| Hiperparâmetro | Símbolo | Intervalo / Descrição |
| :--- | :---: | :--- |
| **Taxa de Vazão** | $a$ | $[0.01, 1.00]$ — Inércia dos neurônios do reservatório |
| **Raio Espectral** | $sr$ | $[0.01, 0.99]$ — Escalamento dos autovalores da matriz $W$ |
| **Período de Lavagem** | $initLen$ | $[1, 200]$ — Passos iniciais descartados para estabilização do estado |
| **Tamanho do Reservatório** | $tam\_reservoir$ | $[3, 50]$ — Número de neurônios internos no reservatório |
| **Regularização Ridge** | $reg$ | $[10^{-7}, 10^{-2}]$ — Penalização Ridge na regressão de saída ($W_{out}$) |

As simulações comparam 4 combinações de distribuição de pesos para as matrizes $W_{in}$ e $W$:
1. **Win Normal** & **W Normal**
2. **Win Uniforme** & **W Uniforme**
3. **Win GED** & **W Uniforme**
4. **Win GED** & **W Normal**

---

## 🏆 Resultados do Benchmark

Abaixo estão resumidos os destaques experimentais obtidos nos 12 cenários de simulação (3 Rodadas × 4 Combinações):

| Categoria | Cenário Selecionado | Época GA | MAE Validação | RMSE Validação | MAE Teste | RMSE Teste |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **🥇 Menor MAE de Teste** | Run 3 \| Win Normal / W Normal | 125 | 0.2627 | 0.3538 | **0.3272** | **0.4980** |
| **🥇 Menor RMSE de Teste** | Run 3 \| Win Normal / W Normal | 125 | 0.2627 | 0.3538 | 0.3272 | **0.4980** |
| **🎯 Menor MAE de Validação** | Run 1 \| Win GED / W Uniforme | 66 | **0.2624** | **0.3534** | 0.3283 | 0.4988 |
| **⚡ Melhor Fitness GA** | Run 2 \| Win GED / W Uniforme | 123 | 0.2627 | 0.3533 | 0.3279 | 0.4987 |

> Para o relatório estatístico detalhado de todos os 12 cenários, consulte o arquivo [`resultados_validacao_teste.md`](resultados_validacao_teste.md).

---

## 📜 Licença e Créditos

Este projeto é parte integrante do Trabalho de Conclusão de Curso (TCC) de **Maycon Garcia Silva**.  
Desenvolvido com apoio das bibliotecas open-source R e Python.

Licença: [MIT License](LICENSE).
