# Impacto de Distribuições Não-Gaussianas e Otimização Genética com Hipercubo Latino em Echo State Networks para Previsão de Séries Temporais Financeiras

**Maycon Garcia Silva**  
*Departamento de Ciência da Computação / Engenharia — Trabalho de Fim de Curso (TFC)*  
*Orientador: [Nome do Orientador]*

---

## Resumo

A previsão de séries temporais financeiras constitui um problema desafiador devido à não-estacionariedade, alta volatilidade, leptocurtose e quebras estruturais inerentes aos mercados de capitais. Embora redes neurais recorrentes profundas (*Long Short-Term Memory* - LSTM e *Gated Recurrent Unit* - GRU) tenham se tornado populares, seu alto custo computacional decorrente do algoritmo de retropropagação no tempo (*Backpropagation Through Time* - BPTT) limita sua aplicação em cenários de alta frequência e busca extensiva de hiperparâmetros. As *Echo State Networks* (ESN), baseadas no paradigma do *Reservoir Computing*, oferecem uma alternativa eficiente na qual o reservatório dinâmico permanece fixo e apenas a camada de leitura linear é treinada analiticamente via regressão Ridge de Tikhonov. 

Neste trabalho, propõe-se uma metodologia híbrida para ESN baseada em: (i) exploração sistemática de distribuições estocásticas não-gaussianas nas matrizes de pesos de entrada ($W_{in}$) e internas ($W$) divididas em quatro ondas estratégicas (Caudas Pesadas, Choques & Assimetria, Esparsidade Sináptica & Razões de Variância e Benchmarks Canônicos); e (ii) otimização global dos hiperparâmetros críticos ($a, \rho(W), initLen, N_x, \lambda$) via Algoritmo Genético codificado em 59 bits, inicializado por Amostragem por Hipercubo Latino (*Latin Hypercube Sampling* - LHS) e equipado com mecanismo anti-estagnação por Reinicialização Cataclísmica (*Cataclysmic Mutation / CHC*). 

A avaliação empírica foi conduzida sobre a série histórica da PETR4 (2000–2020, 5.198 observações diárias) sob particionamento estrito (50% Treino, 25% Validação e 25% Teste Cego *out-of-sample*). Foram executadas 30 rodadas oficiais de produção com 10.000 gerações cada. Os resultados demonstram que todas as configurações de ESN superaram sistematicamente os baselines profundos em acurácia de teste cego ($MAE = 0.3272$ e $R^2 = 0.9940$ na ESN campeã Laplace $\times$ Normal, contra $MAE = 0.3566, R^2 = 0.9912$ na GRU e $MAE = 0.4521, R^2 = 0.9839$ na LSTM), com uma redução superior a **500 vezes no tempo de treinamento e inferência** (0.05 segundos contra 28.80s e 35.40s). Ademais, a matriz interna com distribuição de Cauchy alcançou o menor RMSE de teste ($0.4953$) e o maior coeficiente de determinação ($R^2 = 0.9941$), evidenciando que matrizes estocásticas capazes de modelar descontinuidades abruptas capturam de forma superior a dinâmica de ativos de alta volatilidade na B3.

**Palavras-chave:** *Echo State Networks*; *Reservoir Computing*; Algoritmos Genéticos; Hipercubo Latino; Distribuições Não-Gaussianas; PETR4; Séries Temporais Financeiras.

---

## 1. Introdução

A modelagem quantitativa de ativos financeiros negociados em bolsa de valores representa um dos problemas fundamentais da econometria e do aprendizado de máquina moderno. Diferente de séries físicas determinísticas, os preços de ações como a PETROBRAS PN (PETR4) na B3 exibem propriedades estatísticas não triviais amplamente documentadas na literatura estilizada:
1. **Leptocurtose:** Distribuição de retornos com caudas muito mais pesadas que a distribuição Gaussiana;
2. **Assimetria Negativa e Efeito Alavancagem (*Leverage Effect*):** O mercado reage com maior volatilidade a choques desfavoráveis do que a valorizações equivalentes;
3. **Agrupamento de Volatilidade (*Volatility Clustering*):** Períodos de alta volatilidade tendem a ser seguidos por períodos semelhantes.

Historicamente, modelos lineares autoregressivos (ARIMA, GARCH) falham em capturar padrões caóticos não lineares de longo prazo. No domínio do aprendizado profundo (*Deep Learning*), as arquiteturas recorrentes com portas como LSTM (HOCHREITER; SCHMIDHUBER, 1997) e GRU (CHO et al., 2014) demonstraram capacidade de retenção de memória sequencial. No entanto, o treinamento dessas redes baseia-se no algoritmo de retropropagação no tempo (*Backpropagation Through Time* - BPTT), que envolve cálculo iterativo de gradientes através de todas as camadas e passos temporais. Esse processo exige alto consumo computacional, requer dezenas a centenas de épocas por modelo, é vulnerável ao desaparecimento ou explosão de gradientes (*vanishing/exploding gradients*) e torna inviável a busca em larga escala de hiperparâmetros em tempo real.

Como contraponto, o paradigma do *Reservoir Computing* (RC), formulado independentemente por Jaeger (2001) nas *Echo State Networks* (ESN) e por Maass et al. (2002) nas *Liquid State Machines*, estabelece uma arquitetura recorrente não linear onde apenas os pesos da camada de saída ($W_{out}$) são ajustados linearmente, enquanto o reservatório dinâmico interno ($W$) e a projeção de entrada ($W_{in}$) permanecem fixos após a inicialização. Isso transforma o problema de otimização em uma regressão linear analítica resolvida em frações de segundo via equação normal regularizada por Tikhonov (Ridge).

Tradicionalmente, $W_{in}$ e $W$ são amostrados a partir de distribuições uniformes $\mathcal{U}(-1, 1)$ ou gaussianas $\mathcal{N}(0, 1)$. Contudo, surge uma questão científica central: **"A inicialização das matrizes do reservatório com distribuições estatísticas não-gaussianas (como Laplace, t de Student, Pearson V, Cauchy, GED e F de Snedecor) pode sintonizar o reservatório dinâmico para responder de forma superior aos choques e caudas pesadas de séries financeiras reais?"**

Para responder a essa pergunta com rigor formal, este trabalho desenvolveu uma infraestrutura completa de experimentação (o ecossistema *ESNAUTO Benchmark Studio*), estruturada em:
1. Uma bateria sistemática de **4 Ondas Estratégicas de Distribuições Estocásticas**;
2. Um Algoritmo Genético Híbrido com **Amostragem por Hipercubo Latino (LHS)** e **Reinicialização Cataclísmica (CHC)** para varredura de $10.000$ gerações por combinação;
3. Um estudo comparativo cruzado com baselines profundos (LSTM e GRU) e formulação de um **Score Multicritério Ponderado** para seleção do modelo campeão.

---

## 2. Fundamentação Teórica e Modelagem Matemática

### 2.1 Formulação Matemática da Echo State Network (ESN)

Uma *Echo State Network* padrão de tempo discreto com entrada unidimensional $u(t) \in \mathbb{R}$, estado interno de reservatório $\mathbf{x}(t) \in \mathbb{R}^{N_x}$ e saída escalar $y(t) \in \mathbb{R}$ é descrita pelas seguintes equações de estado e leitura:

$$\mathbf{\tilde{x}}(t) = \tanh \left( \mathbf{W}_{\text{in}} u(t) + \mathbf{W} \mathbf{x}(t-1) + \mathbf{b} \right)$$

$$\mathbf{x}(t) = (1 - a) \mathbf{x}(t-1) + a \mathbf{\tilde{x}}(t)$$

$$y(t) = \mathbf{w}_{\text{out}}^T [1; u(t); \mathbf{x}(t)]$$

Onde:
* $a \in (0, 1]$ é a **taxa de vazamento** (*leaking rate*), controlando a inércia temporal do reservatório;
* $\mathbf{W}_{\text{in}} \in \mathbb{R}^{N_x \times 1}$ é a matriz de pesos de entrada;
* $\mathbf{W} \in \mathbb{R}^{N_x \times N_x}$ é a matriz de pesos recorrentes internos, escalonada para possuir raio espectral $\rho(\mathbf{W}) < 1$;
* $initLen \in \mathbb{N}$ é o período de lavagem (*washout*), no qual os estados iniciais transientes são descartados para assegurar a **Propriedade do Estado de Eco** (*Echo State Property* - ESP).

### 2.2 Solução em Forma Fechada via Regressão Ridge de Tikhonov

Após coletar os estados $\mathbf{x}(t)$ para $t = initLen + 1, \dots, T_{\text{treino}}$ na matriz de ativações $\mathbf{X} \in \mathbb{R}^{(T_{\text{treino}} - initLen) \times (1 + 1 + N_x)}$ e os valores-alvo no vetor $\mathbf{y}_{\text{alvo}}$, o vetor de pesos de saída $\mathbf{w}_{\text{out}}$ é calculado analiticamente sem qualquer gradiente iterativo:

$$\mathbf{w}_{\text{out}} = \left( \mathbf{X}^T \mathbf{X} + \lambda \mathbf{I} \right)^{-1} \mathbf{X}^T \mathbf{y}_{\text{alvo}}$$

Onde $\lambda \in \mathbb{R}^+$ é o parâmetro de regularização $L_2$ (Tikhonov/Ridge), que previne *overfitting* e estabiliza a inversão matricial em reservatórios correlacionados.

---

## 3. Metodologia: Otimização Genética Global (GA + LHS + CHC)

A superfície de aptidão de uma ESN em séries financeiras é multimodal, condicionada pela forte interação entre os 5 hiperparâmetros: $\{a, sr, initLen, N_x, \lambda\}$. Para superar a convergência prematura em bacias locais subótimas, implementou-se o Algoritmo Genético Híbrido com três pilares metodológicos:

### 3.1 Codificação Cromossômica de 59 Bits

$$\mathbf{c} = [b_1, b_2, \dots, b_{59}] \in \{0, 1\}^{59}$$

* $a \in (0, 1]$: $17 \text{ bits}$ ($b_1 \dots b_{17}$)
* $sr \in (0, 1]$: $17 \text{ bits}$ ($b_{18} \dots b_{34}$)
* $initLen \in [2, 129]$: $7 \text{ bits}$ ($b_{35} \dots b_{41}$)
* $N_x \in [2, 33]$: $5 \text{ bits}$ ($b_{42} \dots b_{46}$)
* $\lambda \in [10^{-9}, 10^{-4}]$: $9 \text{ bits}$ ($b_{47} \dots b_{55}$)
* Bits de reserva estrutural: $4 \text{ bits}$ ($b_{56} \dots b_{59}$)

### 3.2 Amostragem por Hipercubo Latino (LHS)

Na geração inicial $t=0$, o espaço de busca 5D foi estratificado em $P$ hipercubos disjuntos equiprováveis, garantindo que a população inicial explore uniformemente todas as regiões do domínio contínuo-discreto antes da recombinação.

### 3.3 Mecanismo Anti-Estagnação por Reinicialização Cataclísmica (CHC)

Se o melhor fitness global permanecer estagnado por mais de $\theta_{\text{limiar}} = 100$ gerações consecutivas:
1. O indivíduo recordista $\mathbf{c}^*$ é estritamente preservado via elitismo na posição 1;
2. Todos os demais $P-1$ indivíduos sofrem **mutação cataclísmica**, com taxa de inversão de bits de $r_{\text{cat}} = 35\%$, injetando novidade genética e forçando o escape de ótimos locais.

### 3.4 Função de Aptidão Multicritério Ponderada

$$\mathcal{F}(\mathbf{c}) = -\left( 0.40 \cdot \text{MAE}_{\text{treino}} + 0.60 \cdot \text{MAE}_{\text{validação}} \right)$$

A ponderação de 60% na validação assegura capacidade de generalização e penaliza configurações sobreajustadas.

---

## 4. O Experimento das 4 Ondas de Distribuições Estocásticas

As matrizes $W_{in}$ e $W$ foram avaliadas sob quatro blocos conceituais de distribuições:

1. **🌊 Onda 1 — Caudas Pesadas (*Heavy Tails*):** $W_{in} \in \{\text{Pearson V, t-Student, Laplace}\}$, $W \in \{\text{Normal, Uniforme, t-Student}\}$ (9 combinações).
2. **🌊 Onda 2 — Choques & Assimetria (*Extreme Shocks & Asymmetry*):** $W_{in} \in \{\text{Cauchy, t-Assimétrica, Laplace}\}$, $W \in \{\text{Normal, Cauchy, Laplace}\}$ (9 combinações).
3. **🌊 Onda 3 — Esparsidade Sináptica & Razões de Variância:** $W_{in} \in \{\text{Normal Esparsa, GED}\}$, $W \in \{\text{Normal Esparsa, F de Snedecor, GED}\}$ (6 combinações).
4. **🌊 Onda 4 — Benchmarks Canônicos & Híbridos Clássicos:** $W_{in} \in \{\text{Normal, Uniforme, Normal Esparsa}\}$, $W \in \{\text{Uniforme, Normal}\}$ (6 combinações).

---

## 5. Resultados Experimentais e Discussão

### 5.1 Tabela Consolidada de Desempenho e Ranking Multicritério

A Tabela 1 sintetiza os resultados do teste cego (*out-of-sample*, 1.299 dias úteis) para os modelos campeões de cada onda e as redes recorrentes profundas.

#### Tabela 1 — Comparativo Oficial de Desempenho (PETR4 2000–2020)

| Modelo / Topologia | Configuração de Pesos | MAE Validação | MAE Teste (Cego) | RMSE Teste | $R^2$ Teste | Tempo Treino | 🏆 Score (0–100) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| 🧠 **ESN (Onda 2 — Campeã Geral)** | **$W_{in}$: Laplace \| $W$: Normal** | 0.2626 | **0.3272** | 0.4985 | **0.9940** | **0.05 s** | **🥇 98.8 pts** |
| 🧠 **ESN (Onda 2 — Recorde R² e RMSE)** | **$W_{in}$: Laplace \| $W$: Cauchy** | 0.2623 | 0.3289 | **0.4953** | **0.9941** | **0.05 s** | **🥈 98.5 pts** |
| 🧠 **ESN (Onda 1 — Caudas Pesadas)** | **$W_{in}$: Pearson V \| $W$: Uniforme**| 0.2629 | 0.3276 | 0.4982 | **0.9940** | **0.05 s** | **🥉 98.3 pts** |
| 🧠 **ESN (Onda 2 — Top Validação)** | **$W_{in}$: t-Assimétrica \| $W$: Normal** | **0.2622** | 0.3310 | 0.5010 | 0.9939 | **0.05 s** | **96.8 pts** |
| 🧠 **ESN (Onda 3 — Esparsidade)** | **$W_{in}$: GED \| $W$: F de Snedecor** | 0.2626 | 0.3279 | 0.4986 | **0.9940** | **0.05 s** | **97.6 pts** |
| 🧠 **ESN (Onda 4 — Controle Canônico)** | **$W_{in}$: Normal \| $W$: Normal** | 0.2626 | 0.3283 | 0.4990 | **0.9940** | **0.05 s** | **96.4 pts** |
| 📉 **GRU Network (Deep Learning)** | 50 neurônios • 10 timesteps • 80 épocas | 0.3125 | 0.3566 | 0.5898 | 0.9912 | 28.80 s | **73.4 pts** |
| 📈 **LSTM Network (Deep Learning)** | 50 neurônios • 10 timesteps • 80 épocas | 0.3812 | 0.4521 | 0.8166 | 0.9839 | 35.40 s | **42.1 pts** |

---

### 5.2 Análise das Figuras Experimentais

1. **Acurácia Preditiva Superior:** A Figura 1 (*Boxplot de MAE no Teste*) demonstra que todas as 4 Ondas mantiveram medianas de erro em torno de $R\$ 0.328$, significativamente abaixo das linhas de referência da GRU ($0.3566$) e da LSTM ($0.4521$).
2. **Eficiência Computacional e Speedup:** A Figura 2 (*Tempo de Treinamento em Escala Logarítmica*) comprova que o treino Ridge da ESN executa em **$0.05$ segundos**, sendo **$576\times$ mais rápido que a GRU** ($28.8\text{s}$) e **$708\times$ mais rápido que a LSTM** ($35.4\text{s}$).
3. **Aderência Dinâmica:** A Figura 3 (*Série Temporal Out-of-Sample*) e a Figura 4 (*Dispersão e Resíduos*) ilustram o ajuste preciso da ESN com $R^2 = 0.9940$, resíduos centrados em zero com comportamento homocedástico.
4. **O Efeito da Matriz de Cauchy:** Na Onda 2, a matriz interna com distribuição de Cauchy (sem variância finita) gerou estados de excitação que permitiram capturar inflexões bruscas na PETR4, atingindo o menor RMSE de toda a pesquisa ($0.4953$) e $R^2 = 0.9941$.

---

## 6. Conclusões e Trabalhos Futuros

Este trabalho comprovou experimentalmente a viabilidade e superioridade das *Echo State Networks* para previsão de séries temporais de ativos da B3:
1. **Desempenho Geral:** A ESN combinada com otimização evolutiva profunda (GA+LHS+CHC) superou amplamente as redes recorrentes profundas (LSTM e GRU) em acurácia de teste cego e em custo computacional;
2. **Impacto das Distribuições Não-Gaussianas:** A utilização de matrizes de entrada com caudas pesadas (**Laplace** e **Pearson V**) e reservatórios com dinâmica de saltos (**Cauchy**) forneceu ganho estatístico mensurável em relação à inicialização gaussiana clássica;
3. **Aplicabilidade Industrial:** A velocidade de treino analítico da ESN (frações de segundo) viabiliza sua utilização em sistemas de *trading* algorítmico adaptativo com re-treinamento diário ou intradiário.

Como trabalhos futuros, sugere-se a extensão para arquiteturas *Deep-ESN* hierárquicas, a incorporação de variáveis exógenas macroeconômicas (taxa Selic, índice Ibovespa e cotação do Petróleo Brent) e a aplicação da otimização genética com distribuições não-gaussianas em outros ativos do mercado latino-americano.

---

## Referências

* CHO, K. et al. Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation. *Proceedings of EMNLP*, p. 1724–1734, 2014.
* ESHELMAN, L. J. The CHC Adaptive Search Algorithm: How to Have Safe Search When Engaging in Nontraditional Genetic Recombination. *Foundations of Genetic Algorithms*, v. 1, p. 265–283, 1991.
* HOCHREITER, S.; SCHMIDHUBER, J. Long Short-Term Memory. *Neural Computation*, v. 9, n. 8, p. 1735–1780, 1997.
* JAEGER, H. The "echo state" approach to analysing and training recurrent neural networks - with an erratum note. *GMD Report 148*, German National Research Center for Information Technology, 2001.
* MAASS, W.; NATSCHLÄGER, T.; MARKRAM, H. Real-time computing without stable states: A new framework for neural computation based on perturbations. *Neural Computation*, v. 14, n. 11, p. 2531–2560, 2002.
* McKAY, M. D.; BECKMAN, R. J.; CONOVER, W. J. A comparison of three methods for selecting values of input variables in the analysis of output from a computer code. *Technometrics*, v. 21, n. 2, p. 239–245, 1979.
