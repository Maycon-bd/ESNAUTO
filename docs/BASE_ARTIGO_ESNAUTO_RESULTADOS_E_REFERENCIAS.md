# Dossiê técnico-científico para redação do artigo ESNAUTO

## Echo State Networks otimizadas por GA + LHS + mutação cataclísmica para previsão da PETR4

**Autor do projeto e do software:** Maycon Garcia Silva  
**Finalidade deste documento:** servir como base crítica, técnica e bibliográfica para a redação do artigo científico.  
**Objeto empírico:** previsão de um passo à frente do preço de fechamento ajustado da PETR4, de 3 de janeiro de 2000 a 30 de dezembro de 2020.  
**Estado da evidência:** resultados experimentais documentados no repositório; ainda precisam de testes estatísticos, repetições controladas e revisão final do protocolo antes da submissão.

---

## 1. A mensagem central que pode orientar o artigo

O resultado mais defensável desta pesquisa não é afirmar que “a ESN é universalmente melhor que LSTM e GRU”. A conclusão cientificamente sólida é mais específica e, justamente por isso, mais forte:

> **No protocolo experimental adotado para a série ajustada da PETR4, ESNs pequenas, com reservatórios estocásticos otimizados por um algoritmo genético híbrido, alcançaram menor erro fora da amostra que os baselines LSTM e GRU documentados, ao mesmo tempo que o ajuste analítico da camada de saída foi centenas de vezes mais rápido. O ganho incremental das distribuições não gaussianas sobre a ESN Normal foi pequeno em MAE, mas consistente nos melhores casos e acompanhado por resultados particularmente interessantes com Laplace, Pearson V e Cauchy.**

Essa formulação preserva quatro achados importantes:

1. a ESN foi superior **neste conjunto de dados e neste protocolo**;
2. a vantagem de custo é muito forte quando se compara o ajuste de uma ESN já configurada com o treinamento por gradiente das redes profundas;
3. o custo da busca genética não pode ser omitido da análise econômica;
4. as distribuições não gaussianas produziram os recordes, mas o ganho contra a melhor ESN gaussiana foi relativamente pequeno e ainda não foi submetido a teste de significância.

### Números que resumem o argumento

| Comparação no teste cego | ESN campeã | GRU | LSTM | Redução de erro da ESN |
|---|---:|---:|---:|---:|
| MAE | **0,327224** | 0,356600 | 0,452100 | **8,238% vs. GRU; 27,621% vs. LSTM** |
| RMSE da ESN campeã por MAE | **0,498527** | 0,589800 | 0,816600 | **15,475% vs. GRU; 38,951% vs. LSTM** |
| $R^2$ | **0,9940** | 0,9912 | 0,9839 | +0,0028 e +0,0101 ponto absoluto |
| Tempo documentado de ajuste/execução | **0,05 s** | 28,80 s | 35,40 s | **576× e 708× mais rápida** |

**Cuidado interpretativo:** os tempos de 0,05 s, 28,80 s e 35,40 s não incluem uma busca de hiperparâmetros equivalente para os três modelos. As execuções do GA da ESN consumiram de 21,1 a 102 minutos por cenário nas ondas documentadas. Portanto, “576×/708×” descreve o ajuste/execução do modelo selecionado, não o custo total de descoberta da arquitetura.

---

## 2. O que foi desenvolvido no projeto

O ESNAUTO não é apenas um script de treinamento. O projeto resultou em um ecossistema experimental reproduzível, composto por:

- uma implementação de **Echo State Network** com treinamento analítico da camada de leitura por regressão Ridge;
- um **Algoritmo Genético binário** para otimizar cinco hiperparâmetros da ESN;
- uma inicialização estratificada da população por **Latin Hypercube Sampling (LHS)**;
- um mecanismo antiestagnação inspirado na **mutação cataclísmica do CHC**;
- um catálogo de distribuições probabilísticas para $W_{in}$ e $W$;
- automação em Python e R para executar cenários, registrar matrizes, ranquear configurações e avaliar o teste fora da amostra;
- uma aplicação **R Shiny**, o ESNAUTO Benchmark Studio, para executar e comparar ESN, LSTM e GRU;
- persistência de histórico, preservação das matrizes campeãs, geração de gráficos e empacotamento dos resultados;
- documentação técnica, artigo preliminar em Markdown/LaTeX, monografia e relatórios experimentais.

### 2.1 Componentes com valor científico e de engenharia

| Componente | Papel na pesquisa | Valor para o artigo |
|---|---|---|
| ESN com Ridge | Treina apenas $W_{out}$, mantendo $W_{in}$ e $W$ fixas | Fundamenta a hipótese de baixo custo computacional |
| GA | Busca $a$, $sr$, `initLen`, $N_x$ e $lambda$ | Evita escolha manual dos hiperparâmetros |
| LHS | Estratifica a população inicial em cinco dimensões | Aumenta a cobertura inicial do espaço de busca |
| Mutação cataclísmica | Aumenta diversidade após estagnação | Procura escapar de platôs e ótimos locais |
| Ondas estocásticas | Organizam famílias de distribuições por hipótese | Transforma uma lista de testes em desenho experimental interpretável |
| EasyFit/Onda 5 | Usa distribuições ajustadas aos dados de treino | Testa se aderência marginal aos dados melhora a dinâmica do reservatório |
| Fator de Ajuste | Corrige descontinuidades de eventos corporativos | Reduz a chance de o modelo aprender saltos artificiais |
| Shiny Studio | Integra execução, comparação, histórico e visualização | Demonstra contribuição de software e reprodutibilidade operacional |

### 2.2 Rastreabilidade no repositório

Os principais artefatos que sustentam este dossiê são:

- [`README.md`](../README.md): visão geral do software e do protocolo;
- [`08_comparativo_quatro_ondas_estocasticas.md`](08_comparativo_quatro_ondas_estocasticas.md): 30 execuções das Ondas 1 a 4;
- [`09_onda_5_ajustes_empiricos_easyfit.md`](09_onda_5_ajustes_empiricos_easyfit.md): 15 execuções da Onda 5;
- [`resultados_validacao_teste.md`](../resultados_validacao_teste.md): experimento preliminar com 12 cenários;
- [`ga_engine.R`](../app/utils/ga_engine.R): implementação atual de GA, LHS e mutação cataclísmica;
- [`data_prep.R`](../app/utils/data_prep.R): distribuições e preparação temporal dos dados;
- [`mod_lstm.R`](../app/modules/mod_lstm.R) e [`mod_gru.R`](../app/modules/mod_gru.R): baselines profundos;
- [`metrics.R`](../app/utils/metrics.R): MAE, RMSE, MAPE, $R^2$ e score multicritério;
- [`history_tracker.R`](../app/utils/history_tracker.R): persistência dos resultados e baselines oficiais;
- [`artigo_completo_tfc_esn_petr4.md`](artigo_completo_tfc_esn_petr4.md): versão preliminar do artigo;
- [`MayconGarciaSilva_monografia.docx`](../reports/MayconGarciaSilva_monografia.docx): fundamentação e revisão da literatura.

---

## 3. Problema, pergunta e hipóteses de pesquisa

### 3.1 Problema científico

Séries financeiras apresentam não linearidade, mudanças de regime, agrupamento de volatilidade, assimetria e eventos extremos. Ao mesmo tempo, as redes recorrentes profundas que tratam dependências temporais, como LSTM e GRU, exigem treinamento iterativo por retropropagação no tempo. A ESN oferece uma alternativa: projeta a entrada em um reservatório recorrente fixo e ajusta apenas uma leitura linear.

Entretanto, o reservatório é sensível à realização aleatória das matrizes $W_{in}$ e $W$. A literatura frequentemente informa apenas que os pesos foram “gerados aleatoriamente”, sem justificar a distribuição. Isso abre uma questão relevante: a lei probabilística usada na inicialização altera a qualidade dos estados internos e a capacidade de generalização?

### 3.2 Pergunta principal sugerida

> **Em que medida a escolha de distribuições não gaussianas para as matrizes $W_{in}$ e $W$, combinada à otimização GA + LHS e a um mecanismo antiestagnação cataclísmico, melhora a acurácia e o custo computacional de uma ESN na previsão fora da amostra da PETR4 em comparação com inicializações canônicas, LSTM e GRU?**

### 3.3 Hipóteses sugeridas

**H1 — desempenho:** a ESN otimizada apresentará MAE e/ou RMSE fora da amostra menores que os baselines LSTM e GRU sob o protocolo definido.

**H2 — eficiência:** depois de selecionada a configuração, o ajuste da leitura Ridge da ESN exigirá menos tempo computacional que o treinamento iterativo de LSTM e GRU.

**H3 — inicialização:** ao menos uma distribuição não gaussiana em $W_{in}$ ou $W$ produzirá erro menor que a inicialização Normal × Normal.

**H4 — exploração evolutiva:** a combinação LHS + mutação cataclísmica manterá maior cobertura/diversidade da busca que um GA com população aleatória e mutação convencional.

**H5 — ajuste empírico:** distribuições ajustadas aos dados de treino por EasyFit produzirão melhor desempenho ou menor variabilidade que distribuições canônicas.

### 3.4 Situação atual das hipóteses

| Hipótese | Evidência atual | Veredito provisório |
|---|---|---|
| H1 | ESN campeã tem MAE 0,327224; GRU 0,356600; LSTM 0,452100 | **Suportada no experimento**, ainda sem repetição/semente e teste estatístico |
| H2 | 0,05 s contra 28,80 s e 35,40 s | **Suportada para ajuste do modelo selecionado**, não para custo total de otimização |
| H3 | Laplace × Normal reduz o MAE em 0,347% frente a Normal × Normal; Laplace × Cauchy reduz o RMSE em 0,732% | **Suportada em termos pontuais**, significância não demonstrada |
| H4 | O mecanismo foi implementado, mas não existe ablação GA vs. GA+LHS vs. GA+LHS+cataclismo | **Ainda não testada causalmente** |
| H5 | Onda 5 é extremamente estável, mas não supera a campeã nem claramente o baseline Normal | **Estabilidade apoiada; superioridade não apoiada** |

---

## 4. Dados e protocolo experimental

### 4.1 Série analisada

- ativo: PETROBRAS PN, ticker PETR4;
- frequência: observações diárias;
- intervalo: 03/01/2000 a 30/12/2020;
- total: **5.198 observações**;
- variável: preço de fechamento com Fator de Ajuste;
- partição temporal: **2.600 treino (50%)**, **1.299 validação (25%)** e **1.299 teste (25%)**;
- tarefa implementada pela ESN: previsão autorregressiva de um passo à frente;
- baselines LSTM/GRU: janelas de 10 passos, normalização Min–Max calculada apenas no treino, uma camada recorrente com 50 unidades, dropout 0,2, saída densa escalar e otimizador Adam no preset oficial.

### 4.2 Por que o Fator de Ajuste é relevante

Eventos corporativos como desdobramentos, grupamentos e distribuição de proventos podem introduzir descontinuidades contábeis que não representam um choque econômico equivalente. Treinar diretamente sobre preços não ajustados pode levar o modelo a interpretar esses saltos artificiais como dinâmica de mercado. A monografia associa o procedimento ao conjunto BovDB de Cardoso et al. (2022).

Esse ponto pode ser apresentado como contribuição metodológica de qualidade de dados: antes de discutir a arquitetura, o trabalho procura garantir que a série usada na aprendizagem represente uma trajetória economicamente comparável ao longo do tempo.

### 4.3 Formulação da ESN

Uma ESN com taxa de vazamento $a$ pode ser descrita por:

$$
\tilde{\mathbf{x}}(t)=\tanh\left(\mathbf{W}_{in}[1;u(t)]+\mathbf{W}\mathbf{x}(t-1)\right)
$$

$$
\mathbf{x}(t)=(1-a)\mathbf{x}(t-1)+a\tilde{\mathbf{x}}(t)
$$

$$
\hat{y}(t+1)=\mathbf{W}_{out}[1;u(t);\mathbf{x}(t)]
$$

A matriz interna é reescalada pelo raio espectral desejado:

$$
\mathbf{W}_{escalada}=sr\frac{\mathbf{W}}{\rho(\mathbf{W})}.
$$

Depois do período de lavagem `initLen`, a leitura é ajustada por Ridge:

$$
\mathbf{W}_{out}=\mathbf{Y}\mathbf{X}^{T}
\left(\mathbf{X}\mathbf{X}^{T}+\lambda\mathbf{I}\right)^{-1}.
$$

É essa solução fechada, sem BPTT, que explica a velocidade de ajuste da ESN.

### 4.4 Hiperparâmetros otimizados pelo GA atual

| Parâmetro | Bits | Faixa efetiva aproximada | Papel |
|---|---:|---:|---|
| taxa de vazamento $a$ | 17 | $(0,1]$ | controla a inércia/memória temporal |
| raio espectral $sr$ | 17 | $(0,1]$ | controla estabilidade e persistência dos estados |
| `initLen` | 7 | 2 a 129 | descarta transientes iniciais |
| tamanho $N_x$ | 5 | 2 a 33 | dimensão do reservatório |
| regularização $lambda$ | 9 | cerca de $9,9\times10^{-9}$ a $9,9\times10^{-5}$ | estabiliza a leitura Ridge |
| **Total** | **55 bits** | — | cromossomo implementado |

A função de aptidão implementada é:

$$
F=-\left(0{,}4\,MAE_{treino}+0{,}6\,MAE_{validação}\right).
$$

O maior peso da validação busca favorecer generalização e reduzir a seleção de soluções excessivamente ajustadas ao treino.

---

## 5. GA + LHS + cataclismo: origem, implementação e inovação

### 5.1 Quem criou o LHS e qual fonte citar

O **Latin Hypercube Sampling** foi introduzido por **Michael D. McKay, Richard J. Beckman e William J. Conover** no artigo de 1979:

> McKAY, M. D.; BECKMAN, R. J.; CONOVER, W. J. A comparison of three methods for selecting values of input variables in the analysis of output from a computer code. *Technometrics*, v. 21, n. 2, p. 239–245, 1979. DOI: [10.1080/00401706.1979.10489755](https://doi.org/10.1080/00401706.1979.10489755).

No ESNAUTO, cada uma das cinco dimensões é estratificada em $P$ intervalos equiprováveis, sendo $P$ o tamanho da população. Uma permutação diferente dos estratos é usada em cada dimensão e um valor uniforme é sorteado dentro de cada estrato. Os valores contínuo-discretos são então convertidos para os 55 bits do cromossomo.

O benefício esperado é simples: com a mesma população, a geração inicial cobre melhor cada eixo do espaço de busca do que uma amostra puramente aleatória. Isso não garante o ótimo global, mas reduz regiões completamente ignoradas na largada.

### 5.2 Quem criou o mecanismo cataclísmico e qual fonte citar

A **mutação cataclísmica** é um componente do algoritmo **CHC**, proposto por **Larry J. Eshelman** em 1991. CHC significa *Cross-generational elitist selection, Heterogeneous recombination and Cataclysmic mutation*.

> ESHELMAN, L. J. The CHC Adaptive Search Algorithm: How to Have Safe Search When Engaging in Nontraditional Genetic Recombination. In: RAWLINS, G. J. E. (ed.). *Foundations of Genetic Algorithms 1*. San Mateo: Morgan Kaufmann, 1991. p. 265–283. DOI: [10.1016/B978-0-08-050684-5.50020-3](https://doi.org/10.1016/B978-0-08-050684-5.50020-3).

No CHC original, a busca combina seleção elitista entre gerações, prevenção de cruzamento entre indivíduos muito semelhantes, recombinação HUX e uma reinicialização cataclísmica quando a população converge. A reinicialização preserva o melhor indivíduo e cria uma nova população por forte perturbação desse recordista; a literatura sobre CHC normalmente reporta mutação de cerca de 35% dos bits nessa reinicialização.

### 5.3 O que exatamente o ESNAUTO implementa

A versão atual do `ga_engine.R` é **inspirada no CHC**, mas não é uma implementação integral do CHC original. Ela usa:

- seleção por torneio;
- crossover de um ponto com probabilidade 0,85;
- elitismo de aproximadamente 10% da população;
- mutação binária de 12% em regime normal;
- detecção de estagnação adaptada ao número total de gerações;
- ativação de uma mutação alta de **40%** quando o limite de estagnação é atingido;
- população inicial gerada por LHS;
- preservação do melhor estado e das matrizes que produziram o recorde.

Ela **não implementa atualmente** o HUX, a prevenção de incesto por distância de Hamming e a reconstrução explícita de toda a população a partir do melhor indivíduo, que caracterizam o CHC clássico.

Por isso, a nomenclatura mais precisa para o artigo é:

> **“Algoritmo Genético com inicialização LHS e operador antiestagnação por mutação cataclísmica inspirado no CHC.”**

Evite escrever “foi utilizado o algoritmo CHC” sem essa qualificação, pois um revisor pode comparar o pseudocódigo com Eshelman (1991) e identificar as diferenças.

### 5.4 Onde está a inovação da pesquisa

LHS, GA e CHC não foram criados neste projeto. A contribuição está na **adaptação e composição** desses mecanismos para o problema específico:

1. LHS é usado para cobrir, na geração inicial, o espaço misto de hiperparâmetros de uma ESN;
2. a mutação cataclísmica é acionada por estagnação para renovar a diversidade da busca;
3. o GA otimiza simultaneamente memória, estabilidade, dimensão, lavagem e regularização;
4. cada cromossomo é avaliado dentro de um reservatório cujas matrizes são geradas segundo uma combinação probabilística específica;
5. a mesma infraestrutura é usada para comparar ondas conceituais de distribuições e preservar as matrizes campeãs.

Uma formulação adequada de originalidade é:

> **“A inovação não reside na criação isolada do GA, do LHS ou da mutação cataclísmica, mas na sua integração em um mecanismo híbrido de otimização de ESNs, acoplado a uma investigação sistemática de distribuições não gaussianas e empiricamente ajustadas para pesos de reservatório em uma série financeira brasileira.”**

### 5.5 O experimento de ablação que falta

Para demonstrar que LHS e cataclismo realmente causaram melhoria, recomenda-se executar, com as mesmas sementes e orçamento de avaliações:

1. GA convencional com população aleatória e mutação fixa;
2. GA + LHS;
3. GA + cataclismo;
4. GA + LHS + cataclismo.

Para cada variante, registrar em pelo menos 20 ou 30 repetições:

- melhor fitness final;
- MAE/RMSE de validação e teste;
- número de avaliações até o melhor resultado;
- diversidade média de Hamming por geração;
- quantidade de cataclismos;
- tempo total;
- taxa de execuções que convergem para uma solução dentro de uma tolerância do recorde.

Sem essa ablação, pode-se apresentar o mecanismo como contribuição de projeto, mas não afirmar que ele superou um GA convencional.

---

## 6. As cinco ondas de distribuições

### 6.1 Organização conceitual

| Onda | Hipótese | Distribuições/estruturas principais | Execuções documentadas |
|---|---|---|---:|
| 1 — Caudas pesadas | pesos com eventos mais extremos podem enriquecer a resposta do reservatório | Pearson V, t de Student, Laplace | 9 |
| 2 — Choques e assimetria | distribuições impulsivas/assimétricas podem responder melhor a rupturas | Cauchy, t Assimétrica, Laplace | 9 |
| 3 — Esparsidade e razão de variâncias | desconexões e heterogeneidade podem filtrar ruído e regimes | Normal Esparsa, GED, F de Snedecor | 6 |
| 4 — Controles canônicos | medir o ganho contra inicializações usuais | Normal, Uniforme, Normal Esparsa | 6 |
| 5 — Ajustes empíricos | distribuições com boa aderência marginal aos dados podem produzir reservatórios adaptados | Power Function, Dagum 4P, Johnson SB | 15 |
| **Total** | — | — | **45** |

### 6.2 Onda 5 e os parâmetros do EasyFit

Os parâmetros documentados, estimados na partição de treino, são:

- **Power Function:** $\alpha=0{,}50339$, $a=2{,}4759$, $b=34{,}548$;
- **Dagum (4P):** $k=0{,}30596$, $\alpha=2{,}0664$, $\beta=17{,}968$, $\gamma=2{,}4775$;
- **Johnson SB:** $\gamma=0{,}56742$, $\delta=0{,}49965$, $\lambda=27{,}881$, $\xi=1{,}9165$.

O argumento teórico da Onda 5 deve ser usado com cuidado. Ajustar uma distribuição à **marginal dos preços** não implica automaticamente que essa distribuição seja ideal para pesos de uma transformação dinâmica. O reservatório ainda passa os pesos por reescalamento espectral e não linearidade `tanh`, o que pode apagar diferenças de escala e tornar a forma da distribuição menos influente que os hiperparâmetros globais.

---

## 7. Resultados experimentais

### 7.1 Experimento preliminar de 12 cenários

O relatório inicial avaliou três repetições de quatro combinações: Normal × Normal, Uniforme × Uniforme, GED × Uniforme e GED × Normal.

Os destaques foram:

- menor MAE de teste: **Normal × Normal, Run 3 — 0,327472**;
- menor RMSE de teste: **Uniforme × Uniforme, Run 3 — 0,497529**;
- menor MAE/RMSE de validação: **GED × Uniforme, Run 2 — 0,262317/0,352963**;
- melhor fitness ponderado: **GED × Normal, Run 2 — −0,237537**.

Esse primeiro bloco já mostrava algo importante: o melhor resultado de validação não era necessariamente o melhor no teste. Essa divergência justificou preservar uma partição final fora da amostra e expandir a investigação para as ondas estocásticas.

### 7.2 Resultados campeões das Ondas 1 a 5

| Destaque | Configuração $W_{in}\times W$ | MAE val. | RMSE val. | MAE teste | RMSE teste | $R^2$ teste | Observação |
|---|---|---:|---:|---:|---:|---:|---|
| **Melhor MAE global** | **Laplace × Normal** | 0,262630 | 0,354092 | **0,327224** | 0,498527 | 0,9940 | campeã geral por MAE |
| **Melhor RMSE e $R^2$** | **Laplace × Cauchy** | 0,262352 | 0,353158 | 0,328949 | **0,495386** | **0,9941** | melhor controle de erros grandes |
| Melhor Onda 1 por MAE | Pearson V × Uniforme | 0,262957 | 0,353898 | **0,327657** | 0,498257 | 0,9940 | reservatório de apenas 4 neurônios |
| Melhor validação | t Assimétrica × Normal | **0,262232** | 0,353478 | 0,331070 | 0,501005 | 0,9939 | pior generalização que as campeãs de teste |
| Melhor Onda 3 por MAE | GED × GED | 0,262734 | 0,353502 | **0,327850** | 0,498536 | 0,9940 | ligeiramente melhor que GED × F em MAE |
| Controle Normal | Normal × Normal | 0,262674 | 0,353434 | 0,328365 | 0,499037 | 0,9940 | baseline canônico |
| Onda 5 | várias combinações | ≈0,262773 | ≈0,353253 | **0,328395–0,328398** | 0,498785–0,498787 | 0,9940 | extrema homogeneidade |
| **Falha crítica** | **t Assimétrica × Cauchy** | 0,262822 | 0,354279 | **0,558151** | **3,849416** | **0,6412** | colapso fora da amostra |

### 7.3 Ranking das melhores configurações por MAE de teste

| Posição | ID | $W_{in}$ | $W$ | MAE teste | RMSE teste |
|---:|---|---|---|---:|---:|
| 1 | `GA_RUN_0030` | Laplace | Normal | **0,327224** | 0,498527 |
| 2 | `GA_RUN_0022` | Pearson V | Uniforme | **0,327657** | 0,498257 |
| 3 | `GA_RUN_0019` | Pearson V | Normal | **0,327694** | 0,498256 |
| 4 | `GA_RUN_0026` | t de Student | t de Student | **0,327706** | 0,498818 |
| 5 | `GA_RUN_0034` | Cauchy | Laplace | **0,327713** | 0,498587 |

O ranking mostra que quatro das cinco primeiras posições usam ao menos uma distribuição de cauda pesada ou impulsiva. Isso é compatível com a hipótese do artigo, mas não prova que a distribuição “modelou os choques” causalmente. Para sustentar essa explicação, seria necessário analisar estados internos, sensibilidade a eventos extremos e desempenho por regime de volatilidade.

### 7.4 Estatísticas agregadas por onda

| Onda | $n$ | MAE médio | MAE mínimo–máximo | RMSE médio | Tempo total de GA |
|---|---:|---:|---:|---:|---:|
| 1 | 9 | **0,328125** | 0,327657–0,328865 | 0,498891 | 5,882 h |
| 2 | 9 | 0,354105 | 0,327224–0,558151 | 0,871363 | 7,197 h |
| 3 | 6 | 0,328570 | 0,327850–0,329494 | 0,499798 | 5,430 h |
| 4 | 6 | 0,328537 | 0,327938–0,329187 | 0,499803 | 5,250 h |
| 5 | 15 | **0,328395** | 0,328395–0,328398 | **0,498785** | 14,167 h |
| **Total** | **45** | — | — | — | **37,925 h** |

A média da Onda 2 é distorcida pela falha de `GA_RUN_0032`. Sem essa execução, o MAE médio da onda cai para **0,328599** e o RMSE médio para **0,499106**; a mediana é 0,328565. A interpretação correta é que a Onda 2 possui **alto potencial e maior risco**: contém os dois principais recordes, mas também a única falha severa.

### 7.5 Quantas ESNs superaram os baselines profundos

Considerando as 45 execuções documentadas:

- **44/45 (97,78%)** tiveram MAE menor que a GRU;
- **44/45 (97,78%)** tiveram MAE menor que a LSTM;
- a única exceção foi `t Assimétrica × Cauchy`;
- todas as 15 configurações da Onda 5 superaram os dois baselines em MAE.

Portanto, substitua a frase antiga “todas as 30 configurações superaram LSTM e GRU” por:

> **“Das 45 execuções documentadas nas cinco ondas, 44 (97,78%) apresentaram MAE fora da amostra inferior aos baselines LSTM e GRU; uma configuração, t Assimétrica × Cauchy, apresentou falha severa de generalização.”**

### 7.6 Ganho das não gaussianas sobre a ESN Normal

A comparação mais importante para avaliar a contribuição das distribuições é contra `Normal × Normal`, não apenas contra LSTM e GRU.

- MAE do controle Normal × Normal: **0,328365**;
- MAE de Laplace × Normal: **0,327224**;
- redução relativa de MAE: **0,347%**;
- RMSE do controle Normal × Normal: **0,499037**;
- RMSE de Laplace × Cauchy: **0,495386**;
- redução relativa de RMSE: **0,732%**.

Esses ganhos são reais nos valores pontuais, mas pequenos. O artigo ficará mais convincente se evitar adjetivos como “amplamente superior” ao comparar distribuições de ESN e usar “ganho incremental”, “melhoria pontual” ou “vantagem observada”.

### 7.7 O resultado mais intrigante da Onda 5

As 15 execuções da Onda 5 produziram resultados praticamente idênticos apesar de hiperparâmetros e distribuições diferentes:

- amplitude do MAE de teste: apenas **0,000003**;
- amplitude do RMSE: apenas **0,000002**;
- todas convergiram para regularização próxima de $9,9\times10^{-9}$;
- `initLen` ficou entre 2 e 5 na maioria das configurações;
- o tamanho do reservatório variou de 17 a 33 sem alterar materialmente o erro.

Esse achado admite pelo menos três interpretações:

1. **robustez:** diferentes distribuições empíricas levam à mesma região funcional de solução;
2. **dominância do reescalamento:** o ajuste do raio espectral e a `tanh` neutralizam grande parte das diferenças marginais;
3. **degeneração ou saturação:** a busca pode estar convergindo a uma solução quase linear/persistente, pouco sensível à distribuição.

Não é seguro chamar a Onda 5 de “superior”. Ela foi muito estável, mas seu MAE de aproximadamente 0,328395 é ligeiramente pior que o controle Normal × Normal (0,328365) e claramente pior que Laplace × Normal (0,327224). O valor científico está na **invariância observada**, que merece investigação própria.

---

## 8. A hipótese de que a ESN pode ser melhor e mais barata

### 8.1 Por que a hipótese é plausível

Na LSTM e na GRU, os pesos internos são atualizados iterativamente ao longo de múltiplas épocas por gradiente. Na ESN, o reservatório é fixado após a inicialização; somente a leitura é estimada por álgebra linear. Para conjuntos relativamente pequenos, como as 5.198 observações deste estudo, uma arquitetura profunda pode ter capacidade excessiva e maior variância de estimação, enquanto uma ESN pequena funciona como uma expansão dinâmica regularizada.

Os melhores resultados reforçam esse argumento:

- a ESN campeã usou apenas **22 neurônios de reservatório**;
- Pearson V × Uniforme obteve MAE 0,327657 com apenas **4 neurônios**;
- t de Student × t de Student obteve MAE 0,327706 com apenas **3 neurônios**;
- o baseline LSTM/GRU usa 50 unidades recorrentes e 80 épocas no resultado oficial documentado.

O ponto mais elegante para o artigo é que a ESN não venceu por ser maior: configurações muito pequenas foram competitivas. Isso sugere que, para essa tarefa univariada de um passo à frente, a geometria dinâmica do reservatório e a regularização podem importar mais que profundidade ou grande quantidade de parâmetros treináveis.

### 8.2 “Mais barata” em qual sentido

A afirmação deve ser dividida em três custos:

1. **custo de ajuste do modelo selecionado:** forte vantagem da ESN; 0,05 s contra 28,80/35,40 s;
2. **custo de inferência/reajuste recorrente:** provavelmente favorável à ESN, especialmente para reestimativas frequentes da leitura;
3. **custo de seleção/otimização:** desfavorável no protocolo atual, pois cada GA de 10.000 gerações consumiu dezenas de minutos e as 45 execuções somaram cerca de 37,9 horas.

Uma defesa equilibrada é:

> **A busca evolutiva é um custo offline amortizável. Depois de identificada e preservada uma configuração robusta, o retreinamento da leitura Ridge é extremamente barato, tornando a ESN atraente quando o modelo precisa ser atualizado repetidamente.**

Para uma comparação econômica completa, registre separadamente:

- tempo de preparação dos dados;
- tempo de otimização de hiperparâmetros;
- tempo de ajuste final;
- tempo por previsão;
- pico de memória e consumo energético;
- CPU/GPU e versões de software;
- número total de configurações avaliadas em cada família.

### 8.3 O que os resultados permitem afirmar hoje

**Permitido:** “A hipótese foi apoiada pelos resultados obtidos no conjunto PETR4 sob o protocolo adotado.”

**Não recomendado:** “Foi comprovado que ESN é melhor que LSTM e GRU.”

A segunda frase extrapola um ativo, um horizonte, uma partição temporal e uma configuração de baseline. A primeira comunica evidência empírica sem transformar um estudo de caso em lei geral.

---

## 9. Leituras científicas especialmente interessantes

### 9.1 Onda 2: maior recompensa, maior risco

Laplace × Normal produziu o menor MAE, e Laplace × Cauchy produziu o menor RMSE e maior $R^2$. No mesmo bloco, t Assimétrica × Cauchy colapsou no teste. Isso sugere que distribuições muito extremas podem aumentar a expressividade do reservatório, mas também sua sensibilidade a mudança de regime ou a uma realização aleatória desfavorável.

Uma discussão produtiva é relacionar esse comportamento ao compromisso **memória–estabilidade**: após o reescalamento espectral, poucos pesos extremos ainda podem alterar direções dominantes e a saturação da `tanh`. Isso pode criar estados úteis para choques, mas também trajetórias frágeis. Essa explicação deve ser apresentada como hipótese mecanística a ser testada, não como fato comprovado.

### 9.2 Validação não garantiu o melhor teste

A t Assimétrica × Normal teve o menor MAE de validação (0,262232), mas MAE de teste 0,331070, pior que diversas alternativas. A discrepância mostra que escolher o “campeão” apenas pela validação pode favorecer particularidades de um regime temporal.

Esse achado apoia:

- teste final estritamente preservado;
- validação walk-forward ou rolling-origin;
- seleção robusta por múltiplas janelas, não por um único corte;
- comparação das distribuições em regimes de baixa e alta volatilidade.

### 9.3 MAE e RMSE escolheram campeões diferentes

Laplace × Normal foi melhor em MAE; Laplace × Cauchy foi melhor em RMSE. A diferença é substantiva:

- MAE mede erro típico de forma linear;
- RMSE penaliza mais fortemente erros grandes;
- Laplace × Cauchy pode ser preferível quando grandes erros têm custo operacional desproporcional;
- Laplace × Normal pode ser preferível quando se quer minimizar o desvio absoluto médio.

O artigo deve evitar declarar um vencedor único sem definir antes a função de custo do problema.

### 9.4 $R^2$ alto em preços não basta

Valores de $R^2$ próximos de 0,994 parecem excelentes, mas séries de preços em nível são altamente persistentes. Um preditor ingênuo do tipo $\hat{y}_{t+1}=y_t$ pode obter alta aderência. Por isso, o artigo deveria acrescentar:

- baseline de persistência/random walk;
- erro escalado MASE;
- acurácia direcional;
- erro em retornos ou diferenças;
- teste Diebold–Mariano contra o random walk e entre os modelos;
- eventual avaliação econômica com custos de transação, se houver proposta de uso em trading.

Essa inclusão não enfraquece a ESN; ela torna a evidência compatível com padrões de publicação em previsão financeira.

### 9.5 Score multicritério é ferramenta de decisão, não teste estatístico

O software combina MAE/RMSE de validação e teste, $R^2$ e tempo com pesos definidos pelo projeto. Como cada variável é normalizada pelo mínimo e máximo dos modelos presentes, o score muda quando um concorrente é adicionado ou removido. Ele é útil para decisão operacional, mas não deve ser apresentado como prova de superioridade estatística.

---

## 10. Limitações e inconsistências que precisam ser resolvidas antes da submissão

### 10.1 Divergências entre documentação e código

1. **55 versus 59 bits:** o motor atual usa 55 bits. Textos antigos descrevem 59 bits e quatro bits de reserva. O artigo deve acompanhar o código executado em produção ou registrar explicitamente a versão histórica.
2. **35% versus 40%:** a documentação antiga informa cataclismo de 35%; o código atual aplica 40% e mutação normal de 12%.
3. **CHC completo versus inspiração:** o código não implementa HUX, prevenção de incesto e reinicialização integral da população; use “inspirado no CHC”.
4. **Onda 5:** o relatório documenta 15 execuções de 10.000 gerações, mas o script atual `onda5_easyfit_simulations.R` contém 12 cenários e está configurado para 200 gerações. É necessário localizar/taguear o código usado para gerar `GA_RUN_0053` a `GA_RUN_0067`.
5. **Baselines profundos:** se não existe CSV em disco, `history_tracker.R` retorna números hard-coded denominados “Oficial TCC”. Os artefatos brutos desses treinamentos, sementes, logs e curvas de perda precisam ser preservados.

### 10.2 Comparabilidade ESN × LSTM × GRU

- o resultado oficial menciona 80 épocas, mas a interface atual usa 50 como padrão;
- o código dos baselines não fixa sementes de R, TensorFlow e inicializadores;
- existe apenas um resultado oficial por baseline no fallback;
- não há busca de hiperparâmetros equivalente para LSTM/GRU;
- o tempo de GA não está incluído nos 0,05 s da ESN;
- os modelos não usam exatamente a mesma representação temporal: LSTM/GRU recebem janelas de 10 passos, enquanto a ESN opera recorrentemente sobre a sequência;
- a construção `treina_testa` concatena treino e teste pulando a validação, o que cria uma fronteira artificial nas janelas/estado usados para iniciar o teste. É necessário justificar ou corrigir para usar o contexto temporal imediatamente anterior ao teste sem treinar com seus alvos.

### 10.3 Validade estatística

- não há intervalos de confiança;
- não há múltiplas sementes controladas para cada arquitetura;
- não há Diebold–Mariano nos resultados consolidados;
- não há correção para múltiplas comparações entre 45 configurações;
- a seleção das melhores configurações e a análise do teste devem ser separadas para evitar uso indireto do teste na escolha do modelo;
- afirmações como “resíduos homocedásticos” exigem teste/diagnóstico formal; um gráfico de dispersão sozinho não basta.

### 10.4 Validade externa

O estudo cobre um ativo, um mercado, um horizonte e um período histórico. Para generalização, recomenda-se replicar em outros ativos da B3, índices e janelas posteriores a 2020, incluindo períodos de crise e regimes distintos.

---

## 11. Experimentos adicionais com maior retorno científico

### Prioridade alta

1. **Repetições com sementes:** 30 execuções de cada configuração principal e dos baselines.
2. **Random walk:** incluir $y_t$ como previsão de $y_{t+1}$.
3. **Diebold–Mariano:** comparar séries de perdas, não apenas médias agregadas.
4. **Ablation GA/LHS/cataclismo:** demonstrar a contribuição de cada mecanismo.
5. **Custo completo:** separar otimização, ajuste e inferência.
6. **Walk-forward:** repetir os testes em várias origens temporais.

### Prioridade média

7. comparar preços, diferenças e log-retornos;
8. analisar desempenho por quantis de volatilidade;
9. medir saturação da `tanh`, distribuição dos estados e memória do reservatório;
10. testar se a Onda 5 permanece invariável sem reescalamento ou com outras ativações;
11. incluir distribuição Normal com o mesmo orçamento de repetições que cada família não gaussiana;
12. registrar energia, memória, CPU/GPU e número total de avaliações.

### Experimento particularmente interessante para a Onda 2

Repetir Laplace × Cauchy e t Assimétrica × Cauchy em muitas sementes e medir:

- frequência de falha;
- condição numérica de $\mathbf{X}\mathbf{X}^T+\lambda I$;
- proporção de neurônios saturados;
- maior valor absoluto dos pesos antes/depois do reescalamento;
- expoentes de Lyapunov aproximados ou medidas de estabilidade;
- erro em dias de grandes variações.

Isso pode transformar o outlier de um problema em um resultado científico sobre fronteiras de estabilidade de reservatórios de cauda extrema.

---

## 12. Contribuições que podem ser declaradas no artigo

### Contribuições metodológicas

- integração de GA, inicialização LHS e mutação cataclísmica inspirada no CHC para otimização de ESNs;
- codificação binária conjunta de cinco hiperparâmetros contínuos e discretos;
- função de aptidão com maior peso para validação;
- preservação das matrizes exatas associadas ao melhor estado.

### Contribuições experimentais

- avaliação sistemática de 45 combinações/execuções organizadas em cinco ondas;
- comparação de distribuições canônicas, pesadas, assimétricas, esparsas e ajustadas empiricamente;
- identificação de Laplace × Normal como melhor MAE e Laplace × Cauchy como melhor RMSE/$R^2$;
- evidência de que 44/45 execuções superaram os baselines profundos em MAE;
- identificação de uma falha extrema que revela risco de instabilidade em combinações pesadas.

### Contribuições de software

- pipeline automatizado de execução, análise, reinjeção das matrizes e teste fora da amostra;
- Benchmark Studio em R Shiny para ESN/LSTM/GRU;
- histórico persistente, gestão de recordes, geração de gráficos e empacotamento;
- arquitetura extensível para novas distribuições, metaheurísticas e ativos.

### Contribuições para a literatura aplicada

- foco em PETR4/B3, contexto menos representado que mercados norte-americanos e europeus;
- discussão explícita da distribuição de inicialização, frequentemente omitida nos trabalhos de ESN;
- combinação de integridade de dados por Fator de Ajuste com investigação probabilística dos pesos;
- evidência de que uma arquitetura pequena pode competir com redes profundas em uma tarefa financeira univariada.

---

## 13. Trechos-base para adaptação no artigo

### 13.1 Possível parágrafo de contribuição

> Este trabalho propõe uma infraestrutura híbrida de otimização para Echo State Networks aplicada à previsão de preços ajustados da PETR4. A metodologia combina inicialização da população por Latin Hypercube Sampling, busca genética binária em cinco hiperparâmetros e um operador antiestagnação por mutação cataclísmica inspirado no algoritmo CHC. Sobre essa infraestrutura, foram organizadas cinco ondas experimentais que investigam distribuições canônicas, de cauda pesada, assimétricas, esparsas e empiricamente ajustadas para as matrizes de entrada e do reservatório. A contribuição central não consiste na criação isolada desses mecanismos, mas na sua integração a um protocolo reproduzível de seleção, preservação de matrizes e avaliação fora da amostra em uma série financeira brasileira.

### 13.2 Possível parágrafo de resultados

> Entre as 45 execuções documentadas, a configuração $W_{in}$ Laplace e $W$ Normal alcançou o menor MAE de teste (0,327224), enquanto Laplace × Cauchy atingiu o menor RMSE (0,495386) e o maior $R^2$ (0,9941). Em comparação, os baselines GRU e LSTM apresentaram MAE de 0,356600 e 0,452100, respectivamente, correspondendo a reduções relativas de 8,238% e 27,621% para a ESN campeã. Quarenta e quatro das 45 execuções (97,78%) superaram ambos os baselines em MAE. A exceção, t Assimétrica × Cauchy, apresentou MAE 0,558151 e $R^2$ 0,6412, evidenciando que distribuições extremas podem ampliar tanto o potencial quanto a instabilidade do reservatório.

### 13.3 Possível parágrafo de custo computacional

> Após a seleção dos hiperparâmetros, a ESN realizou seu ajuste analítico em aproximadamente 0,05 s, contra 28,80 s da GRU e 35,40 s da LSTM, speedups de 576× e 708×. Essa comparação deve ser interpretada como custo de ajuste do modelo selecionado: a busca genética das ESNs consumiu dezenas de minutos por cenário. Assim, a vantagem econômica da ESN é particularmente relevante em aplicações nas quais o custo offline de seleção pode ser amortizado por múltiplos reajustes rápidos da camada de leitura.

### 13.4 Possível parágrafo sobre a Onda 5

> As distribuições ajustadas pelo EasyFit não produziram o menor erro global, mas apresentaram estabilidade incomum: as 15 execuções registraram MAE entre 0,328395 e 0,328398. Essa quase invariância sugere que o reescalamento espectral, a saturação não linear ou a região de hiperparâmetros selecionada pelo GA podem dominar as diferenças entre as distribuições marginais. O resultado desloca a hipótese da superioridade por aderência para uma questão mais interessante sobre equivalência funcional de reservatórios após normalização dinâmica.

### 13.5 Possível conclusão equilibrada

> Os resultados apoiam a hipótese de que ESNs otimizadas podem oferecer uma combinação favorável de acurácia e eficiência para previsão univariada da PETR4. A vantagem observada frente a LSTM e GRU, contudo, deve ser restrita ao protocolo estudado. A confirmação da generalidade do achado requer múltiplas sementes, validação walk-forward, baselines ingênuos, testes de Diebold–Mariano e contabilização simétrica do custo de busca de hiperparâmetros. Ainda assim, a predominância das ESNs em 44 de 45 execuções e os recordes obtidos por distribuições não gaussianas fornecem uma base empírica promissora para investigação posterior.

---

## 14. Referências fundamentais e como usá-las

### Fundamentos dos mecanismos

**Algoritmos Genéticos**  
HOLLAND, J. H. *Adaptation in Natural and Artificial Systems: An Introductory Analysis with Applications to Biology, Control, and Artificial Intelligence*. Ann Arbor: University of Michigan Press, 1975. Edição posterior: MIT Press, 1992. DOI da edição MIT: [10.7551/mitpress/1090.001.0001](https://doi.org/10.7551/mitpress/1090.001.0001).  
**Uso:** fundamento histórico do GA, seleção, recombinação e evolução de populações.

**Latin Hypercube Sampling**  
McKAY, M. D.; BECKMAN, R. J.; CONOVER, W. J. A comparison of three methods for selecting values of input variables in the analysis of output from a computer code. *Technometrics*, v. 21, n. 2, p. 239–245, 1979. DOI: [10.1080/00401706.1979.10489755](https://doi.org/10.1080/00401706.1979.10489755).  
**Uso:** fonte original da amostragem LHS.

**CHC e mutação cataclísmica**  
ESHELMAN, L. J. The CHC Adaptive Search Algorithm: How to Have Safe Search When Engaging in Nontraditional Genetic Recombination. In: RAWLINS, G. J. E. (ed.). *Foundations of Genetic Algorithms 1*. San Mateo: Morgan Kaufmann, 1991. p. 265–283. DOI: [10.1016/B978-0-08-050684-5.50020-3](https://doi.org/10.1016/B978-0-08-050684-5.50020-3).  
**Uso:** fonte original do CHC e da reinicialização por mutação cataclísmica.

### Arquiteturas neurais

**Echo State Network**  
JAEGER, H. *The “Echo State” Approach to Analysing and Training Recurrent Neural Networks*. GMD Report 148. Sankt Augustin: GMD Forschungszentrum Informationstechnik, 2001. DOI do registro Fraunhofer: [10.24406/publica-fhg-291111](https://doi.org/10.24406/publica-fhg-291111).  
**Uso:** formulação original da ESN. Deve-se consultar também a versão com errata de 2010 ao discutir formalmente a Echo State Property.

**LSTM**  
HOCHREITER, S.; SCHMIDHUBER, J. Long Short-Term Memory. *Neural Computation*, v. 9, n. 8, p. 1735–1780, 1997. DOI: [10.1162/neco.1997.9.8.1735](https://doi.org/10.1162/neco.1997.9.8.1735).  
**Uso:** fonte original da arquitetura LSTM.

**GRU**  
CHO, K. et al. Learning Phrase Representations using RNN Encoder–Decoder for Statistical Machine Translation. In: *Proceedings of EMNLP 2014*. Doha: ACL, 2014. p. 1724–1734. DOI: [10.3115/v1/D14-1179](https://doi.org/10.3115/v1/D14-1179).  
**Uso:** fonte original do RNN Encoder–Decoder que introduz a unidade posteriormente conhecida como GRU.

### Reservoir computing e finanças

WANG, W.; TANG, Y.; XIONG, J.; ZHANG, Y. Stock market index prediction based on reservoir computing models. *Expert Systems with Applications*, v. 178, art. 115022, 2021. DOI: [10.1016/j.eswa.2021.115022](https://doi.org/10.1016/j.eswa.2021.115022).  
**Uso:** evidência externa de RC competitivo com métodos profundos em índices financeiros.

RIBEIRO, G. T.; SANTOS, A. A. P.; MARIANI, V. C.; COELHO, L. S. Novel hybrid model based on echo state neural network applied to the prediction of stock price return volatility. *Expert Systems with Applications*, v. 184, art. 115490, 2021. DOI: [10.1016/j.eswa.2021.115490](https://doi.org/10.1016/j.eswa.2021.115490).  
**Uso:** ESN híbrida aplicada à volatilidade de retornos.

ARAÚJO, H. V. et al. Comparing MAE and RMSE as fitness of genetic algorithm for optimizing echo state network hyperparameters with different probabilistic distributions. In: *IDEAL 2024*. LNCS 15347. Cham: Springer, 2024. p. 314–325. DOI: [10.1007/978-3-031-77738-7_26](https://doi.org/10.1007/978-3-031-77738-7_26).  
**Uso:** antecedente próximo sobre fitness, GA, ESN e distribuições probabilísticas.

CARDOSO, F. C. et al. BovDB: a data set of stock prices of all companies in B3 from 1995 to 2020. *Journal of Information and Data Management*, v. 13, n. 1, p. 77–94, 2022.  
**Uso:** origem dos dados e do tratamento de eventos corporativos/Fator de Ajuste, conforme a monografia do projeto. Antes da versão final, completar DOI ou URL editorial oficial se disponível.

---

## 15. Checklist antes de converter este dossiê em artigo

- [ ] Definir uma única versão do protocolo e tag/commit dos códigos executados.
- [ ] Corrigir 55/59 bits em todos os textos.
- [ ] Descrever o operador como “inspirado no CHC”, salvo se o código for alterado para CHC completo.
- [ ] Preservar CSVs, sementes e logs brutos de LSTM/GRU.
- [ ] Reexecutar baselines com múltiplas sementes e orçamento de busca comparável.
- [ ] Incluir random walk/persistência.
- [ ] Executar Diebold–Mariano e intervalos de confiança por bootstrap temporal apropriado.
- [ ] Executar a ablação de LHS e cataclismo.
- [ ] Justificar/corrigir a construção da fronteira treino–teste.
- [ ] Separar custo de otimização, ajuste e inferência.
- [ ] Evitar “comprovou”, “sempre”, “todas” e “significativamente” sem teste formal.
- [ ] Apresentar o outlier da Onda 2, não removê-lo silenciosamente.
- [ ] Explicar por que MAE e RMSE indicam campeões diferentes.
- [ ] Tratar a homogeneidade da Onda 5 como achado a investigar, não como superioridade.
- [ ] Replicar em outros ativos e períodos posteriores a 2020.

---

## 16. Síntese final

O projeto produziu evidência convincente de que uma ESN pequena e cuidadosamente configurada pode ser uma alternativa muito competitiva a redes recorrentes profundas na previsão de curto prazo da PETR4. O resultado mais expressivo é a combinação de três propriedades: **erro baixo fora da amostra, leitura analítica extremamente rápida e flexibilidade para explorar geometrias de reservatório não gaussianas**.

As distribuições Laplace, Pearson V e Cauchy oferecem os melhores pontos de discussão. Laplace × Normal é a campeã em erro típico; Laplace × Cauchy controla melhor erros grandes; Pearson V alcança desempenho de ponta com reservatórios mínimos. A Onda 2 mostra, ao mesmo tempo, o potencial e o risco de distribuições extremas. A Onda 5, em vez de confirmar superioridade por ajuste marginal, revela uma invariância inesperada que pode indicar robustez, neutralização pelo reescalamento espectral ou degeneração da solução.

O principal cuidado para o artigo é não confundir **treinamento barato da ESN** com **otimização barata da ESN**, nem transformar resultados de um estudo de caso em uma afirmação universal. Com repetição por sementes, ablação do GA híbrido, baseline de persistência, validação walk-forward e testes de significância, o ESNAUTO tem potencial para oferecer uma contribuição tanto metodológica quanto de software: uma investigação reproduzível sobre como distribuição, dinâmica e otimização evolutiva interagem em reservatórios aplicados ao mercado de capitais brasileiro.

