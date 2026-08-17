# 🖥️ Componente 3: ESNAUTO Benchmark Studio (R Shiny Web App)

O **ESNAUTO Benchmark Studio** é uma aplicação web interativa desenvolvida em **R Shiny** com uma interface moderna (UI/UX premium) para visualização, otimização genética em tempo real, ajuste de parâmetros e comparação simultânea entre a **Echo State Network (ESN)** e modelos clássicos de Deep Learning Recorrente (**LSTM** e **GRU**).

---

## 📂 Arquivos Integrantes do Componente

```
ESNAUTO/
└── app/
    ├── app.R                          # Orquestrador Master (UI + Server + Botão Universal)
    │
    ├── modules/                       # Módulos isolados por responsabilidade
    │   ├── mod_esn.R                  # Módulo interativo da ESN (Presets, Custom e GA Live)
    │   ├── mod_lstm.R                 # Módulo interativo da rede LSTM (Keras 3 / TensorFlow)
    │   ├── mod_gru.R                  # Módulo interativo da rede GRU (Keras 3 / TensorFlow)
    │   └── mod_comparacao.R           # Módulo de comparação unificada, custo-benefício e histórico CSV
    │
    ├── utils/                         # Funções e Motores de IA
    │   ├── ga_engine.R                # Motor Live GA (Cromossomo 59-bits + LHS + Cataclismo)
    │   ├── history_tracker.R          # Gerenciador persistente de histórico em CSV e recordes globais
    │   ├── data_prep.R                # Carregamento, particionamento e catálogo de distribuições
    │   └── metrics.R                  # Cálculo de métricas financeiras (MAE, RMSE, MAPE, R², tempo)
    │
    └── www/                           # Recursos estáticos de design
        └── custom.css                 # CSS customizado (botões 52px, navbar 72px, tema dark/light)
```

---

## 🚀 Como Executar o App R Shiny

Abra o console do R ou terminal PowerShell e execute:

```powershell
& 'C:\Program Files\R\R-4.6.0\bin\Rscript.exe' -e "shiny::runApp('app', port = 8080, host = '127.0.0.1')"
```
Ou abra o arquivo `app/app.R` no RStudio e clique no botão **Run App**.

---

## ⚡ Botão Universal Unificado de Benchmark

No topo da aplicação, o **Hero Banner Global** disponibiliza o botão master:
> **`⚡ EXECUTAR BENCHMARK COMPLETO (ESN + GA + LSTM + GRU)`**

Ao clicar, abre-se um modal de configuração permitindo escolher:
1. **⚡ Modo Preset (Rápido — ~30s)**: Carrega o melhor conjunto de matrizes e hiperparâmetros já otimizados da ESN e treina sequencialmente a LSTM e a GRU sob as mesmas condições.
2. **🧬 Modo Otimização Live com Algoritmo Genético (GA Live)**:
   - Executa a busca evolutiva do zero via `ga_engine.R`.
   - **Inicialização por Hipercubo Latino (LHS)** na Geração 0.
   - **Mecanismo Anti-Estagnação por Cataclismo**: renova a população mantendo o campeão para escapar de mínimos locais.
   - Grava cada rodada no arquivo permanente `Scripts/results/historico_otimizacoes_ga.csv`.
   - Salva as matrizes $W_{in}$, $W$ e $W_{out}$ em `Scripts/results/melhor_recorde_global/` caso um novo recorde mundial seja batido.
   - Em seguida, treina LSTM e GRU e direciona automaticamente o usuário para a aba de **Comparativo & Custo-Benefício**.

---

## 📝 Detalhamento de Cada Arquivo

### 1. `app/app.R`
- **Caminho**: [`app/app.R`](../app/app.R)
- **Função**: Orquestrador central da aplicação. Gerencia o estado reativo compartilhado dos dados da PETR4, dispara o Benchmark Universal e conecta os módulos e abas de navegação.

---

### 2. Motores de IA e Utilitários (`app/utils/`)

#### A. `app/utils/ga_engine.R` (Novo Motor Live GA)
- **Caminho**: [`app/utils/ga_engine.R`](../app/utils/ga_engine.R)
- **Função**: Executa a otimização dinâmica dos hiperparâmetros da ESN via Algoritmo Genético.
- **Destaques**:
  - **Cromossomo de 59 bits**: $a$ (17 bits), $sr$ (17 bits), $initLen$ (7 bits), $tam\_reservoir$ (5 bits) e $reg$ (9 bits).
  - **Função de Aptidão (Fitness)**: $F = -0.4 \times \text{MAE}_{\text{treino}} - 0.6 \times \text{MAE}_{\text{valida}}$.
  - **Hipercubo Latino (LHS)**: Garante amostragem uniforme na geração 0 para cobrir todo o hipercubo de busca.
  - **Cataclismo Anti-Estagnação**: Se o GA ficar $N$ gerações sem superar o melhor fitness, ele ativa uma hipermutação controlada (40%) mantendo o indivíduo de elite, permitindo saltar bacias de atração e buscar o **ótimo global**.

#### B. `app/utils/history_tracker.R` (Novo Rastreamento em CSV)
- **Caminho**: [`app/utils/history_tracker.R`](../app/utils/history_tracker.R)
- **Função**: Mantém a persistência histórica de todas as rodadas do GA.
- **Recursos**:
  - Salva em `Scripts/results/historico_otimizacoes_ga.csv`.
  - Calcula a variação percentual ($\Delta\%$) contra a execução imediatamente anterior e contra o recorde de todos os tempos.
  - Exporta automaticamente as matrizes numéricas do campeão histórico em `Scripts/results/melhor_recorde_global/`.

#### C. `app/utils/data_prep.R`
- **Caminho**: [`app/utils/data_prep.R`](../app/utils/data_prep.R)
- **Função**: Carregamento da série PETR4 (2000–2020), separação nos índices oficiais (Treino: 2.600, Validação: 1.299, Teste: 1.299) e catálogo de distribuições estocásticas (`Normal`, `Uniforme`, `GED`, `Cauchy`, `Laplace`).

#### D. `app/utils/metrics.R`
- **Caminho**: [`app/utils/metrics.R`](../app/utils/metrics.R)
- **Função**: Cálculo rigoroso de MAE, RMSE, MAPE, $R^2$ e tempos de execução.

---

### 3. Módulos da Aplicação (`app/modules/`)

#### A. `app/modules/mod_esn.R`
- **Caminho**: [`app/modules/mod_esn.R`](../app/modules/mod_esn.R)
- **Função**: Interface e execução da **Echo State Network**.
- **Abas Internas**:
  - 📊 **Métricas de Desempenho**: Tabela de treino, validação e teste out-of-sample com banner de recorde histórico.
  - 📈 **Validação (In-sample)**: Gráfico de aderência da série real vs prevista.
  - 📉 **Teste (Out-of-sample)**: Gráfico de predição cega fora da amostra.
  - 📜 **Histórico CSV do GA**: Tabela interativa com o histórico permanente de execuções salvas.

#### B. `app/modules/mod_lstm.R` & `app/modules/mod_gru.R`
- **Caminhos**: [`app/modules/mod_lstm.R`](../app/modules/mod_lstm.R) e [`app/modules/mod_gru.R`](../app/modules/mod_gru.R)
- **Função**: Treinamento interativo com Keras 3 / TensorFlow, barras de progresso e curvas de convergência de perda (*Loss*).

#### C. `app/modules/mod_comparacao.R`
- **Caminho**: [`app/modules/mod_comparacao.R`](../app/modules/mod_comparacao.R)
- **Função**: Consolidação do benchmark unificado com análise de custo-benefício computacional, gráficos comparativos de MAE/RMSE no teste e tabela histórica do GA.
