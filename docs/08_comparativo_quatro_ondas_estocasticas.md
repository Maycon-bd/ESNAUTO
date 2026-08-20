# 🌊 Documento de Pesquisa: As 4 Ondas Estratégicas de Otimização Estocástica da ESN
## *Análise Comparativa de Distribuições Não-Gaussianas em Matrizes de Entrada ($W_{in}$) e Reservatório ($W$) para Previsão de Séries Temporais Financeiras (PETR4)*

> **Destinação**: Este documento serve como base formal para a escrita da **Seção de Resultados e Discussão** do Artigo Científico e da Monografia do TFC. Contém a fundamentação teórica, hipóteses financeiras, grade de experimentos e consolidação das 4 Ondas.

---

# 1. ENQUADRAMENTO METODOLÓGICO EXPERIMENTAL

Nas redes *Echo State Networks* (ESN), as matrizes $W_{in}$ (pesos de entrada) e $W$ (pesos internos do reservatório) são tradicionalmente inicializadas por distribuições uniformes $\mathcal{U}(-1, 1)$ ou gaussianas $\mathcal{N}(0, 1)$ (JAEGER, 2001). Contudo, retornos e volatilidades de ativos do mercado de capitais brasileiro (como a série histórica PETR4 2000–2020, com 5.198 observações diárias) violam severamente a hipótese de normalidade, exibindo **curtose excessiva (leptocurtose)**, **assimetria negativa** e **agrupamento de volatilidade** (*volatility clustering*).

Para avaliar o impacto da topologia estocástica na dinâmica do reservatório, estruturou-se uma **bateria experimental em 4 Ondas Estratégicas**, otimizadas pelo Algoritmo Genético com Hipercubo Latino e Cataclismo (GA+LHS+CHC) sob particionamento estrito:
* **Treino:** 2.600 amostras (50.0%)
* **Validação:** 1.299 amostras (25.0%)
* **Teste Cego (*Out-of-Sample*):** 1.299 amostras (25.0%)
* **Parâmetros do GA:** $10.000$ Gerações Máximas, População $P=10$, Parada sem melhora $run = 3.500$ iterações.

---

# 2. DEFINIÇÃO DAS 4 ONDAS E HIPÓTESES CIENTÍFICAS

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        ESTRATÉGIA DAS 4 ONDAS ESTOCÁSTICAS (ESN)                       │
├─────────────────────────┬──────────────────────────┬───────────────────────────────────┤
│ Onda                    │ Distribuições Testadas   │ Hipótese Financeira / Mecânica    │
├─────────────────────────┼──────────────────────────┼───────────────────────────────────┤
│ 🌊 Onda 1: Caudas       │ Win: Pearson V, t, Lap   │ Captura de eventos extremos,      │
│    Pesadas (Heavy Tails)│ W:   Normal, Unif, t     │ leptocurtose e caudas gordas.     │
├─────────────────────────┼──────────────────────────┼───────────────────────────────────┤
│ 🌊 Onda 2: Shocks &     │ Win: Cauchy, Skew-t, Lap │ Resposta a quedas bruscas         │
│    Assimetrias          │ W:   Normal, Cauchy, Lap │ (leverage effect) e super-choques.│
├─────────────────────────┼──────────────────────────┼───────────────────────────────────┤
│ 🌊 Onda 3: Esparsidade  │ Win: Normal Esparsa, GED │ Filtragem de ruído de mercado e   │
│    & Razão de Variâncias│ W:   Esparsa, Snedecor,  │ transição de regimes de variância.│
│                         │      GED                 │                                   │
├─────────────────────────┼──────────────────────────┼───────────────────────────────────┤
│ 🌊 Onda 4: Híbridos &   │ Win: Normal, Unif, Esp   │ Baseline de controle e validação  │
│    Benchmarks Clássicos │ W:   Unif, Normal        │ canônica de Jaeger (2001).        │
└─────────────────────────┴──────────────────────────┴───────────────────────────────────┘
```

---

## 🌊 ONDA 1: CAUDAS PESADAS (*HEAVY-TAILED REGIME*) — [CONCLUÍDA]

### Hipótese Teórica
A distribuição $t$ de Student e a Pearson Tipo V possuem caudas mais espessas que a Gaussiana, permitindo ao reservatório reter estados de memória sensíveis a choques de preços que não decaem exponencialmente.

### Grade de Combinações ($3 \times 3 = 9$ Rodadas)
* **$W_{in}$**: `Pearson V`, `t de Student`, `Laplace`
* **$W$**: `Normal`, `Uniforme`, `t de Student`

### Resultados Oficiais Obtidos (Modo Produção — $10.000$ Gerações)

| ID Execução | $W_{in}$ (Entrada) | $W$ (Reservatório) | Tempo GA | MAE Validação | RMSE Validação | MAE Teste (Cego) | RMSE Teste | $R^2$ Teste | Status |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `GA_RUN_0019` | Pearson V | Normal | 28.6 min | 0.262876 | 0.353813 | 0.327694 | 0.498256 | 0.9940 | Concluído |
| `GA_RUN_0020` | t de Student | Normal | 41.7 min | 0.263102 | 0.354229 | 0.328740 | 0.499512 | 0.9940 | Concluído |
| `GA_RUN_0021` | Laplace | Normal | 34.7 min | 0.262928 | 0.354004 | 0.327881 | 0.498419 | 0.9940 | Concluído |
| `GA_RUN_0022` | Pearson V | Uniforme | 21.1 min | 0.262957 | 0.353898 | **0.327657** | **0.498257** | **0.9940** | **Melhor Teste** |
| `GA_RUN_0023` | t de Student | Uniforme | 34.4 min | 0.262891 | 0.353862 | 0.328417 | 0.499808 | 0.9940 | Concluído |
| `GA_RUN_0024` | Laplace | Uniforme | 55.5 min | 0.263004 | 0.354066 | 0.328447 | 0.498463 | 0.9940 | Concluído |
| `GA_RUN_0025` | Pearson V | t de Student | 52.6 min | 0.262879 | 0.353801 | 0.327714 | 0.498274 | 0.9940 | Concluído |
| `GA_RUN_0026` | **t de Student** | **t de Student** | 50.6 min | **0.262601** | **0.353623** | 0.327706 | 0.498818 | **0.9940** | **Campeã Validação** |
| `GA_RUN_0027` | Laplace | t de Student | 33.7 min | 0.262863 | 0.354294 | 0.328865 | 0.500213 | 0.9939 | Concluído |

* **Tempo Total de Computação da Onda 1**: 5h 53m 15s (21.195 segundos de GA intensivo).

---

## 🌊 ONDA 2: CHOQUES BRUSCOS & ASSIMETRIAS (*SHOCKS & ASYMMETRY*) — [EM EXECUÇÃO]

### Hipótese Teórica
O mercado acionário reage com maior intensidade a notícias negativas do que positivas (efeito alavancagem de Black / assimetria direcional). A distribuição **$t$ de Student Assimétrica (*Skew-t*)** permite viés direcional no reservatório, enquanto a distribuição de **Cauchy** (sem momentos finitos de primeira e segunda ordem) introduz saltos discretos capazes de mapear *circuit breakers* e cisnes negros.

### Grade de Combinações ($3 \times 3 = 9$ Rodadas)
* **$W_{in}$**: `Cauchy`, `t de Student Assimétrica`, `Laplace`
* **$W$**: `Normal`, `Cauchy`, `Laplace`

### Tabela de Monitoramento da Onda 2

| ID | $W_{in}$ (Entrada) | $W$ (Reservatório) | MAE Validação | RMSE Validação | MAE Teste | RMSE Teste | $R^2$ Teste | Tempo | Status |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `GA_RUN_0028` | Cauchy | Normal | *...* | *...* | *...* | *...* | *...* | *...* | ⏳ Em execução |
| `GA_RUN_0029` | t Assimétrica | Normal | *...* | *...* | *...* | *...* | *...* | *...* | ⏳ Pendente |
| `GA_RUN_0030` | Laplace | Normal | *...* | *...* | *...* | *...* | *...* | *...* | ⏳ Pendente |
| `GA_RUN_0031` | Cauchy | Cauchy | *...* | *...* | *...* | *...* | *...* | *...* | ⏳ Pendente |
| `GA_RUN_0032` | t Assimétrica | Cauchy | *...* | *...* | *...* | *...* | *...* | *...* | ⏳ Pendente |
| `GA_RUN_0033` | Laplace | Cauchy | *...* | *...* | *...* | *...* | *...* | *...* | ⏳ Pendente |
| `GA_RUN_0034` | Cauchy | Laplace | *...* | *...* | *...* | *...* | *...* | *...* | ⏳ Pendente |
| `GA_RUN_0035` | t Assimétrica | Laplace | *...* | *...* | *...* | *...* | *...* | *...* | ⏳ Pendente |
| `GA_RUN_0036` | Laplace | Laplace | *...* | *...* | *...* | *...* | *...* | *...* | ⏳ Pendente |

---

## 🌊 ONDA 3: ESPARSIDADE & ESTRUTURAS DE RAZÃO DE VARIÂNCIAS (*SPARSITY & SNEDECOR*)

### Hipótese Teórica
Reservatórios com conectividade densa podem propagar ruído estocástico de microestrutura. A **Normal Esparsa** desconecta até 80% das sinapses não essenciais. A distribuição **$F$ de Snedecor** (razão entre duas variáveis qui-quadrado independentes) atua simulando alterações estruturais na razão de volatilidade entre períodos de euforia e pânico.

### Grade de Combinações ($2 \times 3 = 6$ Rodadas)
* **$W_{in}$**: `Normal Esparsa`, `GED (Generalized Error Distribution)`
* **$W$**: `Normal Esparsa`, `F de Snedecor`, `GED`

### Grade Planejada:
1. Normal Esparsa $\times$ Normal Esparsa
2. Normal Esparsa $\times$ F de Snedecor
3. Normal Esparsa $\times$ GED
4. GED $\times$ Normal Esparsa
5. GED $\times$ F de Snedecor
6. GED $\times$ GED

---

## 🌊 ONDA 4: HÍBRIDOS & BENCHMARKS CLÁSSICOS (*CANONICAL BENCHMARK*)

### Hipótese Teórica
Constitui o grupo de controle experimental canônico para contrastar as distribuições Gaussianas e Uniformes puras (JAEGER, 2001) contra as distribuições exóticas das Ondas 1, 2 e 3, demonstrando formalmente o ganho estatístico obtido pela customização estocástica.

### Grade de Combinações ($3 \times 2 = 6$ Rodadas)
* **$W_{in}$**: `Normal`, `Uniforme`, `Normal Esparsa`
* **$W$**: `Uniforme`, `Normal`

### Grade Planejada:
1. Normal $\times$ Uniforme
2. Normal $\times$ Normal
3. Uniforme $\times$ Uniforme
4. Uniforme $\times$ Normal
5. Normal Esparsa $\times$ Uniforme
6. Normal Esparsa $\times$ Normal

---

# 3. TABELA CONSOLIDADA GERAL: AS 4 ONDAS vs. DEEP LEARNING (LSTM & GRU)

Tabela para inserção na seção de **Resultados e Discussão do Artigo**:

$$\text{Score} = \left( 0.30 \cdot S_{\text{MAE, teste}} + 0.20 \cdot S_{\text{RMSE, teste}} + 0.20 \cdot S_{R^2} + 0.10 \cdot S_{\text{MAE, val}} + 0.10 \cdot S_{\text{RMSE, val}} + 0.10 \cdot S_{\text{Tempo}} \right) \times 100$$

| Arquitetura | Detalhamento / Distribuição | MAE Validação | RMSE Validação | MAE Teste (Cego) | RMSE Teste | $R^2$ Teste | Tempo Treinamento | 🏆 Score Ponderado | Classificação |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 🧠 **ESN — Onda 1** | $W_{in}$: Pearson V \| $W$: Uniforme | 0.2629 | 0.3538 | **0.3276** | **0.4982** | **0.9940** | **0.05 s** | **98.6 pts** | 🥇 **Líder Atual** |
| 🧠 **ESN — Onda 1** | $W_{in}$: t-Student \| $W$: t-Student | **0.2626** | **0.3536** | 0.3277 | 0.4988 | **0.9940** | **0.05 s** | **98.4 pts** | 🥈 **Top Validação** |
| 🧠 **ESN — Onda 2** | *Em processamento ao vivo...* | *...* | *...* | *...* | *...* | *...* | *...* | *...* | ⏳ Em execução |
| 🧠 **ESN — Onda 3** | *Aguardando disparo da Onda 3* | *...* | *...* | *...* | *...* | *...* | *...* | *...* | ⏳ Na fila |
| 🧠 **ESN — Onda 4** | *Aguardando disparo da Onda 4* | *...* | *...* | *...* | *...* | *...* | *...* | *...* | ⏳ Na fila |
| 📉 **GRU Network** | 50 neurônios • 10 timesteps • 80 épocas | 0.3125 | 0.4418 | 0.3566 | 0.5898 | 0.9912 | 28.80 s | **73.4 pts** | 🎖️ Baseline DL |
| 📈 **LSTM Network** | 50 neurônios • 10 timesteps • 80 épocas | 0.3812 | 0.5241 | 0.4521 | 0.8166 | 0.9839 | 35.40 s | **42.1 pts** | 🎖️ Baseline DL |

---

# 4. ROTEIRO DE REDAÇÃO DO ARTIGO CIENTÍFICO

1. **Introdução**: Justificativa da não-linearidade dos mercados financeiros e do alto custo de BPTT em LSTMs.
2. **Fundamentação Teórica**: Propriedade de Estado de Eco (*Echo State Property*), Álgebra do Reservatório e Regressão Ridge Analítica.
3. **Metodologia**: Otimização Genética Híbrida com Amostragem por Hipercubo Latino (LHS) e Mutação Cataclísmica (CHC).
4. **Análise das 4 Ondas Estocásticas**:
   * *Onda 1*: Comportamento sob caudas pesadas (Pearson V vs t de Student).
   * *Onda 2*: Resposta dinâmica a choques infinitos e assimetrias direcionais.
   * *Onda 3*: Esparsidade sináptica e razões de variância de Snedecor.
   * *Onda 4*: Comparação direta com o padrão canônico Gaussiano.
5. **Custo-Benefício Computacional**: Demonstração de que a ESN atinge precisão preditiva superior ($R^2 > 0.99$, $MAE < 0.33$) com redução de até **700x** no tempo de treinamento frente à LSTM/GRU.
6. **Conclusão**: Recomendação prática da topologia estocástica campeã para sistemas de negociação algorítmica de alta frequência.
