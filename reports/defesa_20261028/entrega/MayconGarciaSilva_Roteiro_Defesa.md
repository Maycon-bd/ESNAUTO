# Roteiro de apresentação — defesa da monografia

Maycon Garcia Silva · Engenharia de Software · UniRV

**Duração planejada: 25 minutos, incluindo demonstração breve.** Os tempos são metas de ensaio, não uma garantia da duração da leitura. O roteiro fornece a fala principal. Use o tempo restante de cada slide para explicar os dados apontados, fazer pausas e trocar de tela. Ensaiar com cronômetro antes da gravação.

O aplicativo é apoio experimental. Deixe-o iniciado e prepare um resultado cuja procedência seja conhecida. Não execute buscas ou treinamentos durante a apresentação. Se houver falha, explique o fluxo pelo slide 18.

## Slide 1 — Aplicação de fator de correção para previsão de preços de ações na bolsa de valores com rede neural de estados de eco

**Tempo: 00:00–00:45 (45 s)**

Boa tarde. Meu nome é Maycon Garcia Silva e apresento a pesquisa sobre previsão do preço ajustado da PETR4 com redes neurais de estados de eco, sob orientação do professor Fabian Corrêa Cardoso. O trabalho investiga o desempenho preditivo dessas redes, a escolha das distribuições dos pesos e o custo computacional do processo. Ao longo da apresentação, vou explicar o protocolo, discutir os principais resultados e mostrar brevemente o ESNAUTO, aplicação que desenvolvi como apoio aos experimentos. A contribuição principal está na pesquisa experimental, com o software como infraestrutura de execução e organização.

## Slide 2 — Problema e delimitação

**Tempo: 00:45–01:50 (65 s)**

O problema de pesquisa é investigar em que medida distribuições não gaussianas, combinadas à otimização dos hiperparâmetros, alteram o desempenho de uma ESN. A tarefa é bem delimitada: prever o próximo preço de fechamento ajustado da PETR4 a partir do contexto temporal disponível. O estudo usa dados diários de 2000 a 2020 e avalia erro fora da amostra. Essa delimitação é importante porque a conclusão se refere a um ativo, a um horizonte e às arquiteturas especificadas. Também comparo custo computacional, distinguindo o esforço para descobrir uma configuração do esforço para ajustar sua camada de saída. O trabalho não avaliou uma estratégia de negociação, portanto as métricas apresentadas descrevem previsão, sem demonstrar rentabilidade.

## Slide 3 — Objetivo e dimensões investigadas

**Tempo: 01:50–02:55 (65 s)**

O objetivo geral é investigar o desempenho de ESNs na previsão de um passo à frente, com ênfase nas distribuições de entrada e do reservatório e na otimização conjunta dos hiperparâmetros. Organizei a avaliação em cinco hipóteses, aqui resumidas por tema. H1 compara desempenho preditivo. H2 examina eficiência computacional. H3 considera se distribuições não gaussianas produzem melhores resultados que o controle Normal por Normal. H4 trata da integração da amostragem por hipercubo latino e do mecanismo cataclísmico. H5 avalia distribuições ajustadas empiricamente. Essas hipóteses não receberam o mesmo tipo de evidência: algumas têm apoio descritivo, H1 tem análise inferencial complementar, e o efeito causal dos mecanismos de otimização permaneceu sem confirmação por falta de ablação.

## Slide 4 — Rede neural de estados de eco

**Tempo: 02:55–04:15 (80 s)**

Uma ESN é uma rede recorrente com um reservatório de estados. A matriz Win leva a entrada para esse reservatório. A matriz W conecta os seus estados ao longo do tempo. A saída depende desses estados e dos pesos Wout. A característica central para esta pesquisa é que Win e W permanecem fixas durante o ajuste da camada de saída. Estimo Wout por regressão Ridge, que inclui regularização para estabilizar a solução. Assim, não ajusto iterativamente todos os pesos como nas redes recorrentes treinadas por retropropagação. Isso ajuda a explicar o baixo custo de ajuste da configuração escolhida. Entretanto, a qualidade dos estados depende da inicialização e de parâmetros como raio espectral e taxa de vazamento. Por isso, o estudo investiga essas escolhas em conjunto, em vez de supor que qualquer reservatório aleatório será adequado.

## Slide 5 — Dados e partição cronológica

**Tempo: 04:15–05:35 (80 s)**

A base contém cinco mil cento e noventa e oito observações diárias do preço ajustado. A divisão mantém a ordem temporal: duas mil e seiscentas observações para treino, mil duzentas e noventa e nove para validação e o mesmo número para teste. O treino termina em primeiro de julho de 2010, a validação em 28 de setembro de 2015, e o teste vai de 29 de setembro de 2015 a 30 de dezembro de 2020. O Fator de Ajuste busca lidar com descontinuidades de eventos corporativos. Nesta pesquisa, ele integra o pré-processamento fixo. Como não executei uma comparação controlada com e sem esse fator, não atribuo a ele um ganho causal isolado de acurácia. A ESN recebeu a série ajustada sem normalização adicional. GRU e LSTM usaram Min-Max calculado apenas sobre o treino.

## Slide 6 — Otimização dos hiperparâmetros

**Tempo: 05:35–07:00 (85 s)**

Utilizei um algoritmo genético binário com um cromossomo de cinquenta e cinco bits. Ele representa cinco hiperparâmetros: taxa de vazamento, raio espectral, descarte inicial, tamanho do reservatório e regularização Ridge. A função de aptidão combina quarenta por cento do MAE de treino e sessenta por cento do MAE de validação. O sinal negativo permite maximizar o fitness enquanto se reduz o erro. A população inicial emprega amostragem por hipercubo latino. O algoritmo usa seleção por torneio, cruzamento de um ponto, elitismo e mutação. Quando ocorre estagnação, um mecanismo cataclísmico aumenta a mutação. Esse mecanismo é inspirado no CHC, mas não implementa o CHC completo. As buscas principais tiveram limite de dez mil gerações e interrupção por estagnação. Todo esse esforço de busca precisa entrar na interpretação do custo computacional.

## Slide 7 — Cinco ondas experimentais

**Tempo: 07:00–08:10 (70 s)**

As quarenta e cinco execuções históricas estão organizadas em cinco ondas. A primeira investiga caudas pesadas. A segunda considera choques e assimetria. A terceira trabalha com esparsidade e razão de variâncias. A quarta oferece os controles canônicos, incluindo Normal por Normal. A quinta usa distribuições ajustadas empiricamente pelo EasyFit, com quinze execuções. Na notação de cada combinação, a primeira distribuição se aplica a Win e a segunda a W. Cada combinação passa por otimização dos hiperparâmetros. Por isso, uma diferença entre duas execuções expressa o efeito conjunto da distribuição, da configuração e da realização do reservatório. O lote de duzentas gerações usado em ilustrações da monografia pertence a outro protocolo e não entra nessa contagem.

## Slide 8 — Comparações e critérios de avaliação

**Tempo: 08:10–09:20 (70 s)**

A avaliação inclui uma ESN de controle com inicialização Normal por Normal e duas redes recorrentes de comparação: GRU e LSTM. Os modelos profundos usam cinquenta unidades, janela de dez passos, dropout de zero vírgula dois e oitenta épocas. O MAE mede o erro absoluto médio. O RMSE penaliza mais os erros elevados. O R quadrado descreve a aderência global, mas preços em nível podem produzir valores altos por sua persistência temporal. Há uma limitação importante: a ESN recebeu uma busca extensa, enquanto os baselines históricos têm um resultado oficial por arquitetura. Portanto, a comparação não representa igualdade completa de orçamento de otimização. Vou apresentar primeiro os resultados históricos e depois uma rodada controlada separada, que preservou as previsões necessárias ao teste estatístico.

## Slide 9 — Resultados históricos no teste

**Tempo: 09:20–10:45 (85 s)**

Nos resultados históricos, Laplace por Normal apresentou o menor MAE, zero vírgula três dois sete dois dois quatro. Laplace por Cauchy apresentou o menor RMSE e o maior R quadrado. Portanto, as métricas não apontam uma única configuração vencedora. O controle Normal por Normal ficou próximo das melhores alternativas. Os valores de GRU e LSTM aqui são os resultados históricos documentados e não devem ser confundidos com os da rodada controlada que apresentarei adiante. Segundo a consolidação da monografia, quarenta e quatro das quarenta e cinco execuções tiveram MAE inferior aos dois baselines. Esse é um resultado descritivo do conjunto estudado. Como os vetores e matrizes históricos não ficaram integralmente preservados, a inferência estatística precisou de uma execução complementar própria.

## Slide 10 — Ganho incremental das distribuições

**Tempo: 10:45–11:55 (70 s)**

Quando comparo as melhores configurações com o controle Normal por Normal, o ganho é incremental. A redução relativa do MAE foi de aproximadamente zero vírgula trezentos e quarenta e sete por cento. No RMSE, a redução foi de aproximadamente zero vírgula setecentos e trinta e dois por cento. Esses valores são menores que as diferenças observadas frente aos baselines profundos. Isso recomenda cautela na interpretação do papel das distribuições. As configurações também diferem em hiperparâmetros e realização aleatória do reservatório, então os resultados não isolam causalmente a distribuição. Além disso, ajustar uma distribuição à série de preços não implica que essa mesma distribuição seja ideal para os pesos: o reescalamento espectral e a função de ativação alteram a dinâmica resultante.

## Slide 11 — Estabilidade e falhas de generalização

**Tempo: 11:55–13:10 (75 s)**

A análise das falhas é tão relevante quanto a dos melhores valores. Na combinação t assimétrica por Cauchy, o MAE de teste chegou a zero vírgula cinco cinco oito e o RMSE a três vírgula oito quatro nove, apesar de a validação ter valores próximos das demais configurações. Essa foi a exceção na comparação histórica com os baselines em MAE. A segunda onda concentrou, assim, tanto os melhores resultados quanto a maior deterioração fora da amostra. Na quinta onda, as quinze execuções apresentaram MAEs muito próximos, entre zero vírgula três dois oito três nove cinco e zero vírgula três dois oito três nove oito. Isso descreve estabilidade no conjunto observado, mas não prova robustez universal ou menor erro. Também mostra por que a avaliação em um período temporal posterior precisa acompanhar a otimização.

## Slide 12 — Custo de ajuste e custo de descoberta

**Tempo: 13:10–14:25 (75 s)**

O custo computacional precisa ser separado em etapas. Depois de selecionar uma configuração, o ajuste da camada de saída da ESN demandou cerca de cinco centésimos de segundo. Os treinamentos históricos documentados para GRU e LSTM foram de aproximadamente vinte e oito vírgula oito e trinta e cinco vírgula quatro segundos. Porém, antes do ajuste da ESN houve uma exploração extensa: as quarenta e cinco buscas genéticas totalizaram aproximadamente trinta e sete vírgula nove horas. Assim, a vantagem de custo se refere especificamente ao ajuste posterior à seleção. Não seria correto apresentar os cinco centésimos de segundo como custo total para descobrir o modelo. O ESNAUTO contribuiu ao automatizar essas buscas e organizar os resultados, reduzindo a intervenção manual durante execuções prolongadas.

## Slide 13 — Rodada controlada para análise inferencial

**Tempo: 14:25–15:50 (85 s)**

Para testar formalmente diferenças de acurácia, eu precisava dos erros ponto a ponto alinhados por data. Como os artefatos históricos da execução de referência não estavam integralmente preservados, conduzi uma rodada controlada complementar, com semente fixa vinte milhões, duzentos e sessenta mil, novecentos e vinte e seis. Ela usa a configuração de referência Laplace por Normal, mas gera novas matrizes. A camada de saída usa estritamente alvos de treino e os estados mantêm continuidade cronológica ao atravessar validação e teste. Os modelos produziram mil duzentas e noventa e nove previsões, das quais a janela previamente definida utiliza mil duzentas e noventa e oito datas comuns. Executei quatro testes bilaterais de Diebold–Mariano: ESN contra GRU e contra LSTM, com perdas absoluta e quadrática. Os resultados pertencem exclusivamente a essa rodada, sem validar retrospectivamente os números históricos.

## Slide 14 — Erro na janela controlada

**Tempo: 15:50–17:05 (75 s)**

Este gráfico apresenta os erros da rodada controlada, calculados nas mesmas mil duzentas e noventa e oito datas. A ESN teve MAE de aproximadamente zero vírgula três dois nove, contra zero vírgula quatro um oito da GRU e zero vírgula quatro seis sete da LSTM. No RMSE, os valores foram aproximadamente zero vírgula quatro nove oito, zero vírgula cinco nove dois e zero vírgula seis três cinco. As duas métricas favorecem a ESN nesta execução. Os valores estão na escala do preço ajustado e menores valores representam menor erro. Como a configuração histórica de referência recebeu novas matrizes e o protocolo controlado impôs fronteira estrita de treino, é esperado que seus números não coincidam com a tabela histórica. A comparação estatística a seguir usa exatamente os vetores desta janela.

## Slide 15 — Teste de Diebold–Mariano

**Tempo: 17:05–18:25 (80 s)**

O teste de Diebold–Mariano avalia a hipótese nula de diferença média de perda igual a zero. Defini o diferencial como perda da ESN menos perda do baseline. Por isso, os valores negativos indicam a direção favorável à ESN. Nos quatro contrastes, o p-valor ficou abaixo de cinco por cento e a ESN apresentou menor perda média. Isso oferece apoio inferencial complementar para H1, dentro da execução e das arquiteturas estudadas. Utilizei horizonte de um passo e estimação ACF da variância de longo prazo. O protocolo manteve significância individual de cinco por cento, sem correção de multiplicidade, uma escolha registrada como limitação. Os p-valores pequenos não transformam uma única semente em evidência de superioridade universal. Repetições independentes continuam necessárias para estudar a variabilidade entre inicializações.

## Slide 16 — Síntese das hipóteses

**Tempo: 18:25–19:30 (65 s)**

Retomando as hipóteses, H1 recebeu apoio descritivo nos resultados históricos e apoio inferencial na rodada complementar. H2 recebeu apoio para o custo de ajuste de uma configuração já selecionada. H3 teve apoio pontual: distribuições não gaussianas produziram os melhores erros observados, mas com melhoria pequena sobre o controle. Para H4, integrei LHS e o mecanismo cataclísmico ao otimizador, porém não realizei a ablação necessária para atribuir a eles um ganho causal. H5 recebeu apoio parcial quanto à estabilidade observada da quinta onda, sem demonstrar superioridade no erro. Essa síntese evita transformar todos os componentes implementados em hipóteses automaticamente confirmadas. A conclusão acompanha o tipo de evidência disponível para cada questão.

## Slide 17 — Contribuição de Engenharia de Software

**Tempo: 19:30–20:35 (65 s)**

O ESNAUTO surgiu da necessidade de organizar os experimentos. O núcleo de cálculo está em R, com rotinas auxiliares em Python e uma interface R Shiny. A estrutura separa preparação de dados, modelos, otimização, métricas e histórico. Essa organização permite reutilizar funções na interface e nas execuções em lote. A contribuição de Engenharia de Software está na automação do processo, na modularização e nos mecanismos de acompanhamento e recuperação. A auditoria também revelou uma limitação: a política histórica de persistência não preservou todos os vetores e matrizes das execuções oficiais. A rodada controlada tratou essa lacuna com persistência dos artefatos necessários à análise. Vou mostrar brevemente como o aplicativo apresenta o fluxo experimental, mantendo o foco da defesa na pesquisa.

## Slide 18 — Demonstração breve do ESNAUTO

**Tempo: 20:35–22:35 (120 s)**

[0:00–0:20] Abrir o aplicativo previamente iniciado e mostrar a série PETR4. Dizer: esta interface organiza as decisões do protocolo experimental que acabei de apresentar. [0:20–0:50] Mostrar a seleção de distribuições de Win e W e os campos dos hiperparâmetros. Dizer: a configuração reúne escolhas probabilísticas e dinâmicas do reservatório, que precisam ser registradas em conjunto. [0:50–1:25] Abrir um resultado já disponível, indicando sua procedência. Dizer: as métricas e os gráficos permitem inspecionar o desempenho de uma execução, sempre com identificação do conjunto de dados e do protocolo. Não atribuir um resultado exibido a uma rodada histórica sem verificar sua identidade. [1:25–1:50] Mostrar histórico ou comparação, caso estejam disponíveis. Dizer: o objetivo do software é reduzir trabalho manual e organizar a experimentação. [1:50–2:00] Retornar aos slides. Se a aplicação falhar, manter este slide e explicar o fluxo com as mesmas falas. Preparar a aplicação e os resultados antes da gravação. Não iniciar busca genética ou treinamento ao vivo.

## Slide 19 — Limitações e continuidade

**Tempo: 22:35–23:50 (75 s)**

As conclusões têm limites. O estudo considera um ativo e um horizonte de um passo, com divisão temporal estática. As arquiteturas receberam orçamentos diferentes de otimização. Os artefatos históricos não permitem reconstruir integralmente todas as execuções. Também faltaram ablações para isolar o efeito do Fator de Ajuste, do LHS e do mecanismo cataclísmico. A análise controlada utiliza uma única semente, então não estima toda a variabilidade entre inicializações. Como continuidade, considero repetições independentes, validação em janelas temporais, comparação explícita com persistência e testes que isolem componentes do método. A ampliação para VALE3 pertence ao desdobramento da pesquisa e não compõe estes resultados centrais. A evolução do aplicativo para JANUS também é futura, preservando a identidade ESNAUTO da versão estudada.

## Slide 20 — Conclusão

**Tempo: 23:50–25:00 (70 s)**

Concluo que ESNs pequenas e otimizadas foram uma alternativa competitiva para prever o preço ajustado da PETR4 sob o protocolo adotado. Laplace por Normal apresentou o melhor MAE histórico, enquanto Laplace por Cauchy apresentou o melhor RMSE. As melhorias sobre o controle Normal por Normal foram incrementais e não isolam um efeito causal da distribuição. A rodada controlada complementar apresentou menor perda média para a ESN e diferenças estatisticamente significativas frente às arquiteturas GRU e LSTM especificadas, nas duas funções de perda. O ajuste posterior à seleção teve baixo custo, mas a busca de configurações foi extensa. Por fim, o ESNAUTO contribuiu como infraestrutura de Engenharia de Software para executar e organizar os experimentos. Obrigado pela atenção. Fico à disposição para as perguntas da banca.

## Perguntas prováveis da banca

**O título permite atribuir ganho ao Fator de Ajuste?**
O fator integra o pré-processamento. Sem ablação com e sem ajuste, a pesquisa não isola sua contribuição causal para o erro.

**Por que usar ESN?**
Ela permite ajustar a saída por Ridge mantendo o reservatório fixo. O protocolo investigou se essa arquitetura, depois de configurada, produziria erro competitivo com baixo custo de ajuste.

**Os p-valores se aplicam às 45 execuções históricas?**
Não. Os testes usam exclusivamente a rodada controlada com novas matrizes, semente 20260926 e 1.298 datas comuns.

**O GA torna injusta a comparação com GRU e LSTM?**
O orçamento de otimização foi assimétrico. A evidência vale para as configurações estudadas, sem provar superioridade arquitetural sob orçamento igual. Uma continuação deve controlar esse orçamento.

**LHS e cataclismo melhoraram o resultado?**
Foram implementados, mas não houve ablação para medir seu efeito isolado. O mecanismo é inspirado no CHC e não corresponde à implementação integral do algoritmo.

**Qual a diferença entre 1.299 e 1.298 previsões?**
O teste completo contém 1.299 previsões por modelo. A janela DM previamente definida usa 1.298 datas comuns, de 30/09/2015 a 30/12/2020.

**O resultado produz lucro?**
Não houve avaliação de estratégia, retorno líquido ou custos de transação. As métricas descrevem erro de previsão de preços.

**Qual a referência simples que falta ampliar?**
A comparação sistemática com persistência é uma continuação importante, especialmente porque preços em nível têm forte dependência temporal.

**O sistema é o resultado principal?**
O resultado central é a avaliação experimental descrita na monografia. O ESNAUTO é a contribuição de software que organiza e automatiza esse processo.

## Referências para consulta durante o ensaio

- Silva, Maycon Garcia. Monografia PETR4 padronizada FASOFT, 2026, capítulos 1, 3–6.
- Jaeger, H. Echo state network. Scholarpedia, 2007. Referência conceitual citada na monografia.
- Diebold, F. X.; Mariano, R. S. Comparing Predictive Accuracy. Journal of Business & Economic Statistics, 1995. Método citado na monografia.
- Registros primários da rodada controlada: manifesto, métricas da janela DM, previsões datadas e resultados DM, semente 20260926.

## Procedência dos números

Os resultados históricos dos slides 7 e 9–12 seguem a consolidação da monografia e os documentos das ondas. O CSV histórico atual não contém as 45 execuções, portanto não foi possível reconferir integralmente essa consolidação em registros primários. Os slides 13–15 usam os arquivos preservados da rodada controlada. Nenhum experimento foi reexecutado para preparar esta apresentação. As fontes específicas também estão nas notas de cada slide.
