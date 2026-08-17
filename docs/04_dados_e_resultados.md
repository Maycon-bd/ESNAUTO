# 📊 Componente 4: Gestão de Dados e Estrutura de Resultados

Este componente compreende a **base de dados histórica de entrada imutável** (ações da PETR4 entre 2000 e 2020) e a **arquitetura física de pastas e arquivos de saída** onde são gravados os logs, matrizes, relatórios, histórico persistente em CSV e pacotes de entrega de cada simulação.

---

## 📂 Arquivos Integrantes do Componente

```
ESNAUTO/
├── Scripts/
│   ├── data/                                  # Bases de dados históricas
│   │   ├── PETR4_close com factor_2000-2020.txt
│   │   └── PETR4_close com factor_2000-2020_com data.csv
│   │
│   └── results/                               # Resultados das sessões de simulação
│       ├── historico_otimizacoes_ga.csv       # Histórico permanente de todas as rodadas do GA
│       ├── melhor_recorde_global/             # Matrizes (Win, W, Wout) do recorde histórico mundial
│       │   ├── matriz_Win_recorde.txt
│       │   ├── matriz_W_recorde.txt
│       │   └── matriz_Wout_recorde.txt
│       │
│       ├── archive/                           # Histórico antigo de execuções
│       └── Run_YYYYMMDD_HHMMSS_{Mode}/        # Sessão gerada dinamicamente
│           ├── pdfs/                          # PDFs compilados por cenário
│           ├── zips/                          # Arquivos compactados por cenário
│           ├── scenarios/                     # Dados brutos dos 12 cenários
│           └── entrega/                       # Resultados e ZIP final consolidado
│
└── resultados_tcc/                            # Gráficos e txt oficiais consolidados
    ├── grafico_teste_corrigido.png
    ├── grafico_validacao_corrigido.png
    └── resultados_ESN_PETR4.txt
```

---

## 📜 Histórico Permanente do GA (`Scripts/results/historico_otimizacoes_ga.csv`)

Cada execução realizada pelo motor de Algoritmo Genético (seja pelo Studio ou scripts) grava automaticamente uma linha neste arquivo CSV para comparação contínua de recordes:

### Colunas do Arquivo CSV:
| Coluna | Tipo | Descrição |
|---|---|---|
| `id_execucao` | Texto | Identificador sequencial único (`GA_RUN_0001`, `GA_RUN_0002`, etc.) |
| `timestamp` | Data/Hora | Carimbo de data e hora do término da execução |
| `geracoes` | Inteiro | Número total de gerações configuradas no GA |
| `pop_size` | Inteiro | Tamanho da população de cromossomos |
| `dist_win` | Texto | Distribuição estocástica da matriz $W_{in}$ (`GED`, `Normal`, `Uniforme`) |
| `dist_w` | Texto | Distribuição estocástica do reservatório $W$ (`Normal`, `Uniforme`) |
| `a` | Numérico | Taxa de vazão ótima descoberta ($a \in (0, 1]$) |
| `sr` | Numérico | Raio espectral ótimo descoberto ($sr \in (0, 1]$) |
| `initLen` | Inteiro | Período de lavagem (*washout*) ótimo ($initLen \in [2, 129]$) |
| `tam_reservoir` | Inteiro | Número de neurônios do reservatório ($tam\_reservoir \in [2, 33]$) |
| `reg` | Numérico | Parâmetro de regularização Ridge ($reg \in [10^{-9}, 10^{-4}]$) |
| `fitness` | Numérico | Fitness atingido ($-0.4 \times \text{MAE}_{\text{treino}} - 0.6 \times \text{MAE}_{\text{valida}}$) |
| `mae_valida` | Numérico | Erro Médio Absoluto na partição de Validação |
| `rmse_valida` | Numérico | Raiz do Erro Quadrático Médio na Validação |
| `mae_teste` | Numérico | Erro Médio Absoluto na partição de Teste Out-of-Sample |
| `rmse_teste` | Numérico | Raiz do Erro Quadrático Médio no Teste Out-of-Sample |
| `r2_teste` | Numérico | Coeficiente de Determinação ($R^2$) no Teste Out-of-Sample |
| `tempo_segundos`| Numérico | Duração total da busca evolutiva em segundos |
| `delta_anterior_pct`| Texto | Variação percentual do MAE de validação em relação à execução anterior |
| `delta_recorde_pct` | Texto | Variação percentual em relação ao melhor recorde histórico de todos os tempos |
| `eh_novo_recorde` | Lógico | `TRUE` se estabeleceu um novo recorde mundial de precisão |

---

## 🏆 Pasta do Campeão Histórico (`Scripts/results/melhor_recorde_global/`)

Quando uma nova rodada do GA supera o melhor MAE de validação de toda a história do projeto:
- **`matriz_Win_recorde.txt`**: Matriz de pesos de entrada do recordista.
- **`matriz_W_recorde.txt`**: Matriz de pesos internos do reservatório do recordista.
- **`matriz_Wout_recorde.txt`**: Matriz analítica de pesos de saída ($W_{out}$) calculada via regularização Ridge.

---

## 📝 Detalhamento das Bases de Dados (`Scripts/data/`)

### 1. `Scripts/data/PETR4_close com factor_2000-2020.txt`
- **Caminho**: [`Scripts/data/PETR4_close com factor_2000-2020.txt`](../Scripts/data/PETR4_close%20com%20factor_2000-2020.txt)
- **Formato**: Arquivo texto plano (vetor numérico de 5.198 valores por linha)
- **Conteúdo**: Preços diários de fechamento das ações da Petrobras (PETR4) ajustados por proventos, dividendos e desdobramentos (fator) no período de **03/01/2000 a 28/12/2020**.
- **Utilidade**: Utilizado como entrada numérica direta nas simulações batch e pela aplicação interativa.

### 2. `Scripts/data/PETR4_close com factor_2000-2020_com data.csv`
- **Caminho**: [`Scripts/data/PETR4_close com factor_2000-2020_com data.csv`](../Scripts/data/PETR4_close%20com%20factor_2000-2020_com%20data.csv)
- **Formato**: CSV indexado por data (`Data`, `Fechamento_Ajustado`).
