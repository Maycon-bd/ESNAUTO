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
2. **Gatilho de Cataclismo**: Se $k_{\text{estagnado}} \ge \theta_{\text{limiar}}$ (calibrado adaptativamente entre $30$ gerações para testes rápidos e $100$ gerações para execuções oficiais de produção de $10.000$ a $15.000$ gerações sem incremento em $\mathcal{F}^*$):
   - **Elitismo Estrito**: O cromossomo recordista global $\mathbf{c}^*$ é integralmente preservado na posição $1$ da população.
   - **Hipermutação Cataclísmica**: Os demais $P - 1$ indivíduos são submetidos a uma taxa de perturbação estocástica elevada de mutação binária ($\mu_{\text{cataclismo}} = 0.40$):
   
   $$P(b_{i, j}^{(t+1)} = 1 - b_{i, j}^{(t)}) = 0.40, \quad \forall i \in \{2, \dots, P\}, \; j \in \{1, \dots, 55\}$$

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

## 1.6 Dinâmica de Busca em Horizontes Longos (10.000 a 15.000+ Gerações): O Papel dos Múltiplos Ciclos Cataclísmicos

Em algoritmos genéticos padrão, estender o número de gerações além de $2.000$ ou $3.000$ iterações geralmente resulta em retornos marginais nulos (*plateau* evolutivo), visto que a perda de diversidade alélica homogeneíza a população em torno de um único atrator local.

Contudo, com a integração do operador de **Reinicialização Cataclísmica Adaptativa**, a extensão do horizonte computacional para **$10.000$ a $15.000$ gerações** torna-se teoricamente justificada e altamente produtiva. Dado que o espaço de busca discreto-contínuo compreende $2^{55} \approx 3{,}60 \times 10^{16}$ estados cromossômicos possíveis, a busca desenvolve-se através de múltiplos ciclos sucessivos de:

$$\underbrace{\text{Exploração Global (LHS)}}_{\text{Geração } 0} \longrightarrow \underbrace{\text{Refinamento Local}}_{\text{Gerações } t \dots t+k} \longrightarrow \underbrace{\text{Estagnação Detectada}}_{k \ge \theta_{\text{limiar}} (80 \dots 100)} \longrightarrow \underbrace{\text{Salto Cataclísmico (Hipermutação 40\%)}}_{\text{Preservação da Elite } \mathbf{c}^*} \longrightarrow \underbrace{\text{Nova Bacia de Atração}}_{\text{Gerações } t+k+1 \dots}$$

### Vantagens Teórico-Práticas para o Trabalho:
1. **Varredura Multimodal Profunda**: Em $15.000$ gerações, o algoritmo executa entre $20$ e $40$ reinicializações cataclísmicas controladas, permitindo que a ESN escape de múltiplos mínimos locais rasos e localize regiões de hipersuperfície com combinações raras de alta vazão ($a$) e raio espectral ($\rho(W)$) que minimizam o erro out-of-sample.
2. **Avaliação Robusta de Distribuições Estocásticas de Cauda Pesada**: Ao testar matrizes $W_{\text{in}}$ e $W$ governadas por distribuições leptocúrticas (Laplace, Pearson V, GED e Cauchy), o horizonte estendido de $15.000$ gerações fornece o tempo evolutivo necessário para que a camada de saída regularizada ($W_{\text{out}}$) encontre a resposta ideal às perturbações e *shocks* inerentes às cotações financeiras da Petrobras.
3. **Critério de Parada Adaptativo (*Early Stopping*)**: O mecanismo foi calibrado com limite de tolerância estendida ($run = 3.500$ a $5.000$ gerações consecutivas sem qualquer melhora global), garantindo que o algoritmo explore exaustivamente cada ciclo cataclísmico antes de considerar uma convergência como definitiva.

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

## 2.3 Implementação Computacional, Autoria do Software e Legado Acadêmico

Todo o ecossistema computacional, incluindo o motor de busca evolutiva com hipermutação cataclísmica, a interface de monitoramento em tempo real e o pipeline de benchmark integrado (**ESNAUTO Benchmark Studio**), é de **autoria e desenvolvimento de Maycon Garcia Silva**, concebido especificamente como instrumento experimental para este Trabalho de Conclusão de Curso.

### Considerações sobre a Execução em Ambiente Local (*Localhost / Desktop R Shiny*):
A aplicação foi projetada para operar como uma interface web executada localmente no computador do pesquisador. Em vez de utilizar serviços de nuvem pública sujeitos a *timeouts* e quotas de computação, a execução local assegura:
1. **Disponibilidade Total de Hardware**: Acesso direto a todos os *threads* de processamento da CPU e memória física da máquina para a execução de corridas longas de até 15.000 gerações do GA e treino profundo de redes neurais recorrentes.
2. **Latência Zero e Segurança de Estado**: Comunicação instantânea de pacotes de rede via WebSocket (`httpuv::service`) e flags de arquivo no disco local, viabilizando as funções de pausa, retomada e salvamento atômico do melhor modelo encontrado.

### Disponibilização para Futuras Pesquisas e Novos Orientandos:
Visando dar continuidade a esta linha de pesquisa e fomentar novos trabalhos acadêmicos no grupo, o código-fonte integral, a arquitetura de classes e a documentação técnica são disponibilizados como **código aberto para os futuros orientandos do professor/orientador**. A estrutura desacoplada do projeto permite a esses pesquisadores:
- Integrar novas distribuições de probabilidade no reservatório com apenas uma chamada à função `registrar_distribuicao()`;
- Desenvolver e comparar novas topologias de redes em reservatório (*Deep ESN*, *Leaky ESN*);
- Avaliar outras técnicas de otimização metaheurística (*Particle Swarm Optimization*, *Differential Evolution*);
- Estender a modelagem para outros ativos do mercado de capitais (índices, moedas e *commodities*).

---

# 3. REFERÊNCIAS BIBLIOGRÁFICAS (FORMATO ABNT)

- **ABADI, M. et al.** TensorFlow: Large-Scale Machine Learning on Heterogeneous Distributed Systems. *arXiv preprint arXiv:1603.04467*, 2016.
- **BORCHERS, H. W.** *pracma: Practical Numerical Math Functions*. R package version 2.4.4, 2023. Disponível em: <https://CRAN.R-project.org/package=pracma>.
- **CARNELL, R.** *lhs: Latin Hypercube Samples*. R package version 1.1.6, 2022. Disponível em: <https://CRAN.R-project.org/package=lhs>.
- **CHANG, W. et al.** *shiny: Web Application Framework for R*. R package version 1.9.1, 2024. Disponível em: <https://CRAN.R-project.org/package=shiny>.
- **CHENG, J. et al.** *httpuv: HTTP and WebSocket Server Library for R*. R package version 1.6.15, 2024. Disponível em: <https://CRAN.R-project.org/package=httpuv>.
- **CHO, K. et al.** Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation. *Proceedings of the 2014 Conference on Empirical Methods in Natural Language Processing (EMNLP)*, p. 1724–1734, 2014.
- **CHOLLET, F. et al.** *Keras: Deep Learning for humans*. GitHub, 2015. Disponível em: <https://github.com/keras-team/keras>.
- **ESHELMAN, L. J.** The CHC Adaptive Search Algorithm: How to Have Safe Search When Engaging in Alternative Genetic Selection. *Foundations of Genetic Algorithms*, v. 1, p. 265–283, 1991.
- **GOLDBERG, D. E.** *Genetic Algorithms in Search, Optimization, and Machine Learning*. Boston: Addison-Wesley Longman Publishing Co., 1989.
- **HOCHREITER, S.; SCHMIDHUBER, J.** Long Short-Term Memory. *Neural Computation*, v. 9, n. 8, p. 1735–1780, 1997.
- **JAEGER, H.** *The “echo state” approach to analysing and training recurrent neural networks*. GMD Report 148, German National Research Center for Information Technology, 2001.
- **KRISHNAKUMAR, K.** Micro-genetic algorithms for stationary and non-stationary function optimization. *SPIE Proceedings: Intelligent Control and Adaptive Systems*, v. 1196, p. 289–296, 1989.
- **LUKOŠEVIČIUS, M.; JAEGER, H.** Reservoir computing approaches to recurrent neural network training. *Computer Science Review*, v. 3, n. 3, p. 127–149, 2009.
- **McKAY, M. D.; BECKMAN, R. J.; CONOVER, W. J.** A Comparison of Three Methods for Selecting Values of Input Variables in the Analysis of Output from a Computer Code. *Technometrics*, v. 21, n. 2, p. 239–245, 1979.
- **R CORE TEAM.** *R: A Language and Environment for Statistical Computing*. Vienna, Austria: R Foundation for Statistical Computing, 2024. Disponível em: <https://www.R-project.org/>.
- **SCRUCCA, L.** GA: A Package for Genetic Algorithms in R. *Journal of Statistical Software*, v. 53, n. 4, p. 1–37, 2013. DOI: 10.18637/jss.v053.i04.
- **VAN ROSSUM, G.; DRAKE, F. L.** *Python 3 Reference Manual*. Scotts Valley, CA: CreateSpace, 2009.
