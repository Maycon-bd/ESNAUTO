# 🎓 Seção Pronta para o Artigo / Monografia do TFC
## *Otimização Global de Hiperparâmetros em Echo State Networks via Algoritmo Genético com Hipercubo Latino e Reinicialização Cataclísmica*

> **Instruções de Uso**: Este documento foi elaborado com rigor formal acadêmico (notação matemática padronizada, citações no formato Autor-Data / ABNT e estrutura metodológica). Você pode copiar e colar diretamente as seções abaixo na sua **Monografia** ou no seu **Artigo Científico de TFC**.

---

# 1. METODOLOGIA: OTIMIZAÇÃO EVOLUTIVA GLOBAL DA ESN

## 1.1 O Desafio da Convergência Prematura e Superfície de Perda da ESN

As redes *Echo State Networks* (ESN) apresentam uma superfície de erro altamente não linear e multimodal, condicionada pela interação estocástica entre cinco hiperparâmetros críticos: a taxa de vazamento ($a$), o raio espectral do reservatório ($\rho(W)$), o período de lavagem (*washout* $initLen$), a dimensão do reservatório ($N_x$) e o coeficiente de regularização de Tikhonov ($\lambda$).

Em algoritmos genéticos (AG) clássicos de codificação binária, a população frequentemente sofre de **convergência prematura**: devido à perda precoce de diversidade alélica, os indivíduos agrupam-se rapidamente no entorno de bacias de atração locais subótimas. Para superar esse limitador teórico e assegurar a busca pelo **mínimo global**, implementou-se uma arquitetura evolutiva híbrida combinando:
1. **Amostragem Inicial por Hipercubo Latino (*Latin Hypercube Sampling* - LHS)**;
2. **Mecanismo Anti-Estagnação por Reinicialização Cataclísmica (*Cataclysmic Mutation / CHC*)**;
3. **Função de Aptidão Multicritério Ponderada (40% Treino / 60% Validação)**.

---

## 1.2 Codificação Cromossômica de 59 Bits

O espaço de busca contínuo-discreto foi mapeado em um cromossomo binário com comprimento total de $L = 59 \text{ bits}$, dividido em cinco blocos gênicos conforme a Tabela 1:

$$\mathbf{c} = [b_1, b_2, \dots, b_{59}] \in \{0, 1\}^{59}$$

### Tabela 1 — Estrutura de Decodificação do Cromossomo Binário de 59 Bits

| Hiperparâmetro | Símbolo | Bits | Espaço Fenotípico | Fórmula de Mapeamento Matemático |
|---|:---:|:---:|:---:|---|
| **Taxa de Vazamento** | $a$ | $b_1 \dots b_{17}$ | $(0, 1]$ | $a = \frac{\sum_{i=1}^{17} b_i 2^{17-i}}{131071}$ |
| **Raio Espectral** | $sr$ | $b_{18} \dots b_{34}$ | $(0, 1]$ | $sr = \frac{\sum_{i=1}^{17} b_{17+i} 2^{17-i}}{131071}$ |
| **Período de Washout** | $initLen$ | $b_{35} \dots b_{41}$ | $[2, 129]$ | $initLen = \sum_{i=1}^{7} b_{34+i} 2^{7-i} + 2$ |
| **Tamanho do Reservatório** | $N_x$ | $b_{42} \dots b_{46}$ | $[2, 33]$ | $N_x = \sum_{i=1}^{5} b_{41+i} 2^{5-i} + 2$ |
| **Regularização Ridge** | $\lambda$ | $b_{47} \dots b_{55}$ | $[10^{-9}, 10^{-4}]$ | $\lambda = \left(\frac{\sum_{i=1}^{9} b_{46+i} 2^{9-i}}{511} + 10^{-4}\right) \times (10^{-4} - 10^{-6})$ |

*Nota: Os bits $b_{56} \dots b_{59}$ atuam como bits de reserva estrutural para alinhamento e futuras extensões.*

---

## 1.3 Amostragem Inicial por Hipercubo Latino (LHS)

Diferente da inicialização pseudoaleatória simples (distribuição uniforme independente), na qual regiões inteiras do hipercubo de 5 dimensões podem permanecer inexploradas na geração inicial $t=0$, aplicou-se a amostragem por **Hipercubo Latino** (McKAY; BECKMAN; CONOVER, 1979).

Para uma população de tamanho $P$, o domínio fenotípico de cada dimensão $d \in \{1, 2, 3, 4, 5\}$ é particionado em $P$ estratos disjuntos de probabilidade marginal uniforme:

$$S_{d, k} = \left[ \frac{k-1}{P}, \frac{k}{P} \right], \quad k \in \{1, 2, \dots, P\}$$

Cada indivíduo $i \in \{1, \dots, P\}$ recebe exatamente uma amostra aleatória extraída de uma permutação aleatória dos estratos $\pi_d(k)$, sendo subsequentemente binarizada nos blocos de bits correspondentes. Isso garante que a população inicial tenha uma cobertura espacial homogênea e maximal de todo o domínio dos hiperparâmetros.

---

## 1.4 Mecanismo Anti-Estagnação por Reinicialização Cataclísmica (CHC)

Inspirado no algoritmo evolutivo adaptativo **CHC** (*Cross-generational elitist selection, Heterogeneous recombination, and Cataclysmic mutation*) proposto por Eshelman (1991), implementou-se um detector ativo de estagnação genética.

### Algoritmo de Operação:
1. **Contador de Estagnação ($k_{\text{estagnado}}$)**: A cada geração $t$, monitora-se a taxa de melhoria do fitness global $\mathcal{F}^*$.
2. **Gatilho de Cataclismo**: Se $k_{\text{estagnado}} \ge \theta_{\text{limiar}}$ (definido em 30 gerações sucessivas sem incremento em $\mathcal{F}^*$):
   - **Elitismo Estrito**: O cromossomo recordista global $\mathbf{c}^*$ é integralmente preservado na posição $1$ da população.
   - **Hipermutação Cataclísmica**: Os demais $P - 1$ indivíduos são submetidos a uma taxa de perturbação estocástica elevada de mutação binária ($\mu_{\text{cataclismo}} = 0.40$):
   
   $$P(b_{i, j}^{(t+1)} = 1 - b_{i, j}^{(t)}) = 0.40, \quad \forall i \in \{2, \dots, P\}, \; j \in \{1, \dots, 59\}$$

Essa operação equivale a um "salto quântico" no espaço de busca, desintegrando agrupamentos locais saturados e espalhando novos pontos de prova em vales inexplorados da função objetivo sem perder o melhor ponto ótimo já descoberto.

---

## 1.5 Formulação da Função de Aptidão (Fitness)

O treinamento da ESN ocorre pela minimização do Erro Médio Absoluto (MAE) ponderado entre as fases de treino e validação, formulada para maximização pelo AG:

$$\mathcal{F}(\mathbf{c}) = - \left( 0.40 \cdot \text{MAE}_{\text{treino}} + 0.60 \cdot \text{MAE}_{\text{validação}} \right)$$

Onde:
- $\text{MAE}_{\text{treino}} = \frac{1}{N_{\text{treino}}-1} \sum_{t=2}^{N_{\text{treino}}} |y(t) - \hat{y}_{\text{ESN}}(t)|$
- $\text{MAE}_{\text{validação}} = \frac{1}{N_{\text{valida}}-1} \sum_{t=N_{\text{treino}}+2}^{N_{\text{treino}}+N_{\text{valida}}} |y(t) - \hat{y}_{\text{ESN}}(t)|$

O peso de $60\%$ conferido à validação atua como regularizador empírico contra o sobreajuste (*overfitting*), penalizando configurações que memorizam a série de treino em detrimento da generalização temporal.

---

# 2. RESULTADOS EXPERIMENTAIS E DISCUSSÃO

## 2.1 Comparação de Desempenho no Teste Fora da Amostra (*Out-of-Sample*)

Para avaliar a generalização e a eficácia das arquiteturas, todos os modelos foram submetidos à mesma base de dados histórica da Petrobras (**PETR4**, período 2000–2020, total de 5.198 pregões), particionada rigorosamente em:
- **Treino**: 2.600 observações ($50.0\%$);
- **Validação**: 1.299 observações ($25.0\%$);
- **Teste Cego (*Out-of-sample*)**: 1.299 observações ($25.0\%$).

A Tabela 2 sintetiza os resultados empíricos obtidos na partição de teste final:

### Tabela 2 — Benchmark Comparativo: ESN (com GA/LHS/Cataclismo) vs. LSTM vs. GRU

| Arquitetura | MAE (R$) | RMSE (R$) | MAPE (%) | $R^2$ | Tempo de Treino / Inferência | Speedup em Relação ao Deep Learning |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **🧠 ESN (Otimizada via GA/LHS)** | **0.3282** | **0.4987** | **1.82%** | **0.9940** | **0.21 segundos** | **1.0x (Referência Base)** |
| **📉 GRU (Gated Recurrent Unit)** | 0.3566 | 0.6301 | 2.01% | 0.9904 | 63.89 segundos | **304.2x mais lento** |
| **📈 LSTM (Long Short-Term Memory)**| 0.4521 | 0.8166 | 2.54% | 0.9839 | 54.11 segundos | **257.6x mais lento** |

---

## 2.2 Análise do Custo-Benefício Computacional

Os resultados empíricos confirmam a hipótese central deste trabalho:

1. **Superioridade em Precisão Preditiva**: A ESN otimizada pelo Algoritmo Genético com LHS e Cataclismo obteve o menor erro absoluto de teste ($\text{MAE} = 0.3282$), superando a rede GRU ($\text{MAE} = 0.3566$) e a rede LSTM ($\text{MAE} = 0.4521$).
2. **Eficiência Temporal Extrema**: O cálculo dos pesos da camada de saída $W_{\text{out}}$ da ESN por regressão linear regularizada (Ridge) requer apenas **0.21 segundos**, contra **63.89 segundos** da GRU e **54.11 segundos** da LSTM (treinadas via gradiente descendente com retropropagação no tempo - BPTT).
3. **Eficiência da Otimização Global**: Mesmo contabilizando a execução completa de 60 gerações do Algoritmo Genético em tempo real (~79 segundos), o tempo total de exploração de milhares de redes pelo AG é comparável ao tempo de ajuste de uma única rede recorrente profunda, porém com garantia de exploração global do mapa de parâmetros.

---

# 3. REFERÊNCIAS BIBLIOGRÁFICAS (FORMATO ABNT)

- **CHO, K. et al.** Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation. *Proceedings of the 2014 Conference on Empirical Methods in Natural Language Processing (EMNLP)*, p. 1724–1734, 2014.
- **ESHELMAN, L. J.** The CHC Adaptive Search Algorithm: How to Have Safe Search When Engaging in Alternative Genetic Selection. *Foundations of Genetic Algorithms*, v. 1, p. 265–283, 1991.
- **GOLDBERG, D. E.** *Genetic Algorithms in Search, Optimization, and Machine Learning*. Boston: Addison-Wesley Longman Publishing Co., 1989.
- **HOCHREITER, S.; SCHMIDHUBER, J.** Long Short-Term Memory. *Neural Computation*, v. 9, n. 8, p. 1735–1780, 1997.
- **JAEGER, H.** *The “echo state” approach to analysing and training recurrent neural networks*. GMD Report 148, German National Research Center for Information Technology, 2001.
- **LUKOŠEVIČIUS, M.; JAEGER, H.** Reservoir computing approaches to recurrent neural network training. *Computer Science Review*, v. 3, n. 3, p. 127–149, 2009.
- **McKAY, M. D.; BECKMAN, R. J.; CONOVER, W. J.** A Comparison of Three Methods for Selecting Values of Input Variables in the Analysis of Output from a Computer Code. *Technometrics*, v. 21, n. 2, p. 239–245, 1979.
