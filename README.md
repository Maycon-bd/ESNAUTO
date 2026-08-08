# ⚡ ESNAUTO — Automação ESN & GA + Benchmark Studio (PETR4)

[![R](https://img.shields.io/badge/R-4.0%2B-blue.svg)](https://www.r-project.org/)
[![Python](https://img.shields.io/badge/Python-3.8%2B-green.svg)](https://www.python.org/)
[![Shiny](https://img.shields.io/badge/Shiny-Studio-orange.svg)](https://shiny.posit.co/)
[![License](https://img.shields.io/badge/License-MIT-brightgreen.svg)]()

> **Trabalho de Conclusão de Curso (TCC) — Maycon Garcia Silva**  
> Previsão de Séries Temporais Financeiras (Ações PETR4 2000–2020) utilizando **Echo State Networks (ESN)** otimizadas por **Algoritmo Genético (GA)**, comparadas a modelos de Deep Learning (**LSTM** e **GRU**) com interface interativa R Shiny.

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

Para superar a sensibilidade da inicialização aleatória dos pesos do reservatório ($W$) e da matriz de entrada ($W_{in}$), o sistema utiliza um **Algoritmo Genético (GA)** para calibrar simultaneamente os hiperparâmetros globais da rede (taxa de vazão, raio espectral, regularização Ridge, período de lavagem e tamanho do reservatório).

O repositório inclui:
1. **Pipeline de Automação Batch**: Orquestração end-to-end em Python e R para simulações com 10.000 gerações em 12 cenários experimentais.
2. **Pipeline de Pós-Processamento e Teste**: Análise estatística automatizada, extração das melhores matrizes e avaliação *out-of-sample* na partição de teste.
3. **ESNAUTO Benchmark Studio**: Aplicação Web desenvolvida em **R Shiny** com UI/UX moderna para comparação visual em tempo real entre ESN, LSTM e GRU.

---

## ✨ Principais Recursos

- 🧠 **Reservoir Computing Otimizado**: Suporte a distribuições de pesos **Normal**, **Uniforme** e **GED** (*Generalized Error Distribution*) para as matrizes $W_{in}$ e $W$.
- 🧬 **Otimização via Algoritmo Genético**: Ajuste automático dos hiperparâmetros vitais da ESN via pacote `GA` do R.
- 📊 **Particionamento Rigoroso**: Divisão temporal da série PETR4 em **Treino (50%)**, **Validação (25%)** e **Teste Out-of-Sample (25%)**.
- 🖥️ **ESNAUTO Studio (R Shiny)**: Interface com KPIs dinâmicos, métricas financeiras (MAE, RMSE, MAPE, $R^2$), projeção de gráficos e comparação de resíduos ESN vs. Deep Learning (LSTM/GRU).
- 🛠️ **Arquitetura Orientada a Fases**: Pipeline modular em Python para ranqueamento JSON, reinjeção de matrizes ótimas e empacotamento de relatórios.

---

## 📚 Documentação por Componente (`docs/`)

Para facilitar o entendimento de cada módulo do sistema, o projeto conta com uma pasta unificada de documentação em [`docs/`](file:///g:/Outros%20computadores/Meu%20computador/TFC1/ESNAUTO/docs/INDEX.md), dividida por componente:

| Componente | Documento | Conteúdo / Arquivos Explicados |
| :--- | :--- | :--- |
| 📌 **Índice Geral** | [docs/INDEX.md](file:///g:/Outros%20computadores/Meu%20computador/TFC1/ESNAUTO/docs/INDEX.md) | Mapa geral da documentação e navegação rápida. |
| ⚙️ **Orquestração & Simulação** | [docs/01_orquestracao_e_simulacao.md](file:///g:/Outros%20computadores/Meu%20computador/TFC1/ESNAUTO/docs/01_orquestracao_e_simulacao.md) | Explicação de `automate_simulations.py`, `run_simulations.bat`, `acoes_petr4_esn.R` e scripts de gráficos. |
| 🛠️ **Pipeline & Pós-Processamento** | [docs/02_pipeline_pos_processamento.md](file:///g:/Outros%20computadores/Meu%20computador/TFC1/ESNAUTO/docs/02_pipeline_pos_processamento.md) | Explicação do pipeline em 4 fases (`analyze_results.py`, `inject_and_test.py`, `package_results.py` e `scratch_*.py`). |
| 🖥️ **ESNAUTO Studio (Shiny)** | [docs/03_app_shiny_studio.md](file:///g:/Outros%20computadores/Meu%20computador/TFC1/ESNAUTO/docs/03_app_shiny_studio.md) | Explicação de `app/app.R`, módulos ESN/LSTM/GRU/Comparação, utilitários e CSS. |
| 📊 **Dados & Resultados** | [docs/04_dados_e_resultados.md](file:///g:/Outros%20computadores/Meu%20computador/TFC1/ESNAUTO/docs/04_dados_e_resultados.md) | Estrutura de dados PETR4 (`Scripts/data/`), sessões de resultado (`Scripts/results/`) e gráficos consolidados (`resultados_tcc/`). |
| 📄 **Relatórios & Monografia** | [docs/05_relatorios_e_monografia.md](file:///g:/Outros%20computadores/Meu%20computador/TFC1/ESNAUTO/docs/05_relatorios_e_monografia.md) | Detalhamento da monografia do TCC, relatório de arquitetura e tabelas de validação/teste. |

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
│       ├── archive/                     # Histórico de execuções anteriores
│       └── Run_YYYYMMDD_HHMMSS_{Mode}/  # Sessão de simulação gerada automaticamente
│           ├── pdfs/                    # PDFs compilados de cada cenário
│           ├── zips/                    # Pacotes compactados para envio
│           └── scenarios/               # Dados brutos dos cenários (CSVs, logs, matrizes)
│
└── resultados_tcc/                      # 🖼️ Gráficos e resultados oficiais consolidados
    ├── grafico_teste_corrigido.png
    ├── grafico_validacao_corrigido.png
    └── resultados_ESN_PETR4.txt
```

---

## ⚙️ Pré-requisitos e Instalação

### 1. Ambiente R (v4.0 ou superior)
Instale os pacotes R necessários através do console do R:
```R
install.packages(c(
  "shiny", "ggplot2", "PerformanceAnalytics", "GA", 
  "pracma", "fitdistrplus", "MASS", "PearsonDS", "fGarch"
))
```

### 2. Ambiente Python (v3.8 ou superior)
O orquestrador Python utiliza apenas bibliotecas padrão (`os`, `sys`, `json`, `subprocess`, `shutil`, `argparse`, `datetime`). Não requer instalações adicionais no `pip`.

---

## 🚀 Como Executar

### 1. Estúdio de Benchmark (R Shiny App)
Para abrir a interface gráfica interativa do **ESNAUTO Studio**:

```bash
# Pelo terminal R ou PowerShell:
Rscript -e "shiny::runApp('app')"
```
Ou abra o arquivo `app/app.R` no RStudio e clique em **Run App**.

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
# Rodar Modo Teste Rápido (200 gerações GA)
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
python Scripts/analyze_results.py Scripts/results/Run_20260623_150000_Prod

# Fase 3: Reinjetar matrizes ótimas do 1º colocado e testar na partição Out-of-Sample
python Scripts/inject_and_test.py Scripts/results/Run_20260623_150000_Prod

# Fase 4: Empacotar gráficos e relatórios finais na pasta /entrega
python Scripts/package_results.py Scripts/results/Run_20260623_150000_Prod
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
| **🥇 Menor MAE de Teste** | Run 3 \| Win Normal / W Normal | 2754 | 0.2625 | 0.3534 | **0.3275** | 0.4996 |
| **🥇 Menor RMSE de Teste** | Run 3 \| Win Uniforme / W Uniforme | 3658 | 0.2631 | 0.3542 | 0.3284 | **0.4975** |
| **🎯 Menor MAE de Validação** | Run 2 \| Win GED / W Uniforme | 2000 | **0.2623** | **0.3530** | 0.3284 | 0.4989 |
| **⚡ Melhor Fitness GA** | Run 2 \| Win GED / W Normal | 117 | 0.2626 | 0.3533 | 0.3280 | 0.4987 |

> Para o relatório estatístico detalhado de todos os 12 cenários, consulte o arquivo [resultados_validacao_teste.md](file:///g:/Outros%20computadores/Meu%20computador/TFC1/ESNAUTO/resultados_validacao_teste.md).

---

## 📜 Licença e Créditos

Este projeto é parte integrante do Trabalho de Conclusão de Curso (TCC) de **Maycon Garcia Silva**.  
Desenvolvido com apoio das bibliotecas open-source R e Python.

Licença: [MIT License](LICENSE).
uagem gera uma análise comparativa profunda detalhando como a distribuição GED (Generalized Error Distribution) ou Uniforme impactou a representação do espaço de estados no reservatório.
   * O texto gerado é salvo em `reports/analise_resultados_llm.md` e convertido diretamente para Word, pronto para ser revisado e incorporado à sua monografia.
