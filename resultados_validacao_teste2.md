# 📊 Resultados de Validação e Teste — ESN PETR4 (TCC Maycon G Silva)

**Relatório Gerado em:** `2026-06-23 15:35:18`  
**Série Temporal:** PETR4 (Preços de Fechamento com Fator 2000–2020)  
**Particionamento:** Treino (50% — ~2.600 obs), Validação (25% — ~1.299 obs), Teste Out-of-Sample (25% — ~1.299 obs)

---

## 📌 Definições das Métricas e Hiperparâmetros

### Métricas Avaliadas:
* **MAE (Mean Absolute Error)**: $\text{MAE} = \frac{1}{N} \sum_{t=1}^{N} |y_t - \hat{y}_t|$
* **RMSE (Root Mean Squared Error)**: $\text{RMSE} = \sqrt{\frac{1}{N} \sum_{t=1}^{N} (y_t - \hat{y}_t)^2}$

### Hiperparâmetros Otimizados pelo Algoritmo Genético (GA):
* $a$ (**Leaking Rate / Taxa de Vazão**): Define a inércia do reservatório $[0.01, 1.00]$.
* $sr$ (**Spectral Radius / Raio Espectral**): Escala os autovalores da matriz $W$ $[0.01, 0.99]$.
* $initLen$ (**Período de Lavagem**): Número de passos iniciais descartados para eliminar estados transientes $[1, 200]$.
* $tam\_reservoir$ (**Tamanho do Reservatório**): Número de neurônios da camada oculta $[3, 50]$.
* $reg$ (**Regularização Ridge**): Penalização na regressão de saída $W_{out}$.

---

## 📋 Tabela Comparativa dos 12 Cenários

| Run | Distribuição $W_{in}$ | Distribuição $W$ | MAE (Validação) | RMSE (Validação) | MAE (Teste) | RMSE (Teste) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | Normal | Normal | 0,262989 | 0,354089 | 0,327753 | 0,498237 |
| 2 | Normal | Normal | 0,262678 | 0,353766 | 0,329319 | 0,500719 |
| **3** | **Normal** | **Normal** | **0,262530** | **0,353380** | 🥇 **0,327472** | **0,499604** |
| 1 | Uniforme | Uniforme | 0,262587 | 0,354005 | 0,329109 | 0,500850 |
| 2 | Uniforme | Uniforme | 0,262754 | 0,353715 | 0,327522 | 0,498210 |
| **3** | **Uniforme** | **Uniforme** | **0,263092** | **0,354226** | **0,328366** | 🥇 **0,497529** |
| 1 | GED | Uniforme | 0,262616 | 0,353289 | 0,328019 | 0,498720 |
| **2** | **GED** | **Uniforme** | 🎯 **0,262317** | 🎯 **0,352963** | **0,328367** | **0,498909** |
| 3 | GED | Uniforme | 0,262679 | 0,353419 | 0,327917 | 0,498610 |
| 1 | GED | Normal | 0,262636 | 0,353440 | 0,327816 | 0,498587 |
| **2** | **GED** | **Normal** | ⚡ **0,262599** | **0,353327** | **0,327953** | **0,498714** |
| 3 | GED | Normal | 0,262567 | 0,353550 | 0,328017 | 0,498591 |

---

## 🏆 Cenários Destaques

### 🥇 1. MELHOR CENÁRIO DE TESTE (Menor MAE de Teste)
- **Cenário:** `Run 3 | Win Normal | W Normal`
- **Época GA:** `2754`
- **Hiperparâmetros Ótimos:**
  - $a = 0{,}768843$
  - $sr = 0{,}682584$
  - $initLen = 98$
  - $tam\_reservoir = 3$
  - $reg = 9{,}455393 \times 10^{-5}$
- **Resultados:**
  - **MAE Validação:** `0.262530` | **RMSE Validação:** `0.353380`
  - **MAE Teste:** `0.327472` | **RMSE Teste:** `0.499604`

---

### 🥇 2. MELHOR CENÁRIO DE TESTE (Menor RMSE de Teste)
- **Cenário:** `Run 3 | Win Uniforme | W Uniforme`
- **Época GA:** `3658`
- **Hiperparâmetros Ótimos:**
  - $a = 0{,}879409$
  - $sr = 0{,}427593$
  - $initLen = 112$
  - $tam\_reservoir = 27$
  - $reg = 1{,}531518 \times 10^{-5}$
- **Resultados:**
  - **MAE Validação:** `0.263092` | **RMSE Validação:** `0.354226`
  - **MAE Teste:** `0.328366` | **RMSE Teste:** `0.497529`

---

### 🎯 3. MELHOR CENÁRIO DE VALIDAÇÃO (Menor MAE de Validação)
- **Cenário:** `Run 2 | Win GED | W Uniforme`
- **Época GA:** `2000`
- **Hiperparâmetros Ótimos:**
  - $a = 0{,}379504$
  - $sr = 0{,}128549$
  - $initLen = 67$
  - $tam\_reservoir = 22$
  - $reg = 4{,}883182 \times 10^{-5}$
- **Resultados:**
  - **MAE Validação:** `0.262317` | **RMSE Validação:** `0.352963`
  - **MAE Teste:** `0.328367` | **RMSE Teste:** `0.498909`

---

### ⚡ 4. CENÁRIO SELECIONADO PELO GA (Melhor Fitness GA)
- **Cenário:** `Run 2 | Win GED | W Normal`
- **Fitness GA:** `-0.237537`
- **Época GA:** `117`
- **Hiperparâmetros Ótimos:**
  - $a = 0{,}870902$
  - $sr = 0{,}406802$
  - $initLen = 9$
  - $tam\_reservoir = 27$
  - $reg = 2{,}228974 \times 10^{-5}$
- **Resultados:**
  - **MAE Validação:** `0.262599` | **RMSE Validação:** `0.353327`
  - **MAE Teste:** `0.327953` | **RMSE Teste:** `0.498714`

