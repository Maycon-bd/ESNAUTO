# Roteiro de apresentação da monografia

Maycon Garcia Silva · Base editorial v010

Duração planejada: **25 minutos**, em 23 slides. Aproximadamente 2.950 palavras. A duração real depende do ritmo de fala: faça um ensaio cronometrado. As janelas incluem pausas curtas e troca de slides. As fontes e orientações não fazem parte da fala.

## Cronograma

| Slide | Intervalo | Tema |
|---|---|---|
| 01 | 00:00–00:40 | Previsão do preço de fechamento ajustado da PETR4 |
| 02 | 00:40–01:45 | Problema de pesquisa |
| 03 | 01:45–02:50 | Objetivo e hipóteses |
| 04 | 02:50–03:50 | Fundamentação e trabalhos relacionados |
| 05 | 03:50–05:10 | Dados e divisão temporal |
| 06 | 05:10–06:30 | Rede neural de estados de eco |
| 07 | 06:30–07:50 | Busca genética de hiperparâmetros |
| 08 | 07:50–08:55 | Cinco ondas experimentais |
| 09 | 08:55–09:50 | Três blocos de evidência |
| 10 | 09:50–10:55 | ESNAUTO como artefato de software |
| 11 | 10:55–11:45 | Critérios de avaliação |
| 12 | 11:45–13:00 | Resultados históricos de previsão |
| 13 | 13:00–14:05 | Inicializações e ganhos observados |
| 14 | 14:05–15:00 | Exemplo visual preservado |
| 15 | 15:00–16:15 | Rodada controlada complementar |
| 16 | 16:15–17:25 | Erros na janela comum controlada |
| 17 | 17:25–18:40 | Comparação estatística de acurácia |
| 18 | 18:40–19:45 | Custo de ajuste e custo da busca |
| 19 | 19:45–20:55 | Avaliação das cinco hipóteses |
| 20 | 20:55–21:55 | Contribuições do trabalho |
| 21 | 21:55–23:15 | Limitações e alcance das conclusões |
| 22 | 23:15–24:15 | Continuidade da pesquisa |
| 23 | 24:15–25:00 | Conclusão |

## 01 Previsão do preço de fechamento ajustado da PETR4

**00:00–00:40 · 40 segundos**

### Fala

Olá, integrantes da banca. Eu sou Maycon Garcia Silva e apresento minha monografia sobre previsão do preço de fechamento ajustado da PETR4 com redes neurais de estados de eco e otimização genética. O trabalho foi desenvolvido no curso de Engenharia de Software da Universidade de Rio Verde, sob orientação do professor doutor Fabian Corrêa Cardoso. Nesta apresentação, vou explicar a questão investigada, a organização dos experimentos, os principais resultados e a contribuição do software ESNAUTO. Ao final, delimito o que as evidências permitem concluir e as possibilidades de continuidade.

*Apoio para consulta: Monografia v010, capa e resumo*

## 02 Problema de pesquisa

**00:40–01:45 · 65 segundos**

### Fala

O problema parte de uma tarefa concreta: utilizar a informação disponível na série para prever o fechamento ajustado do próximo passo temporal. Preços financeiros apresentam mudanças de comportamento, e uma configuração de rede pode funcionar de maneira diferente conforme a inicialização e os hiperparâmetros. A questão do trabalho é investigar como configurações de redes de estados de eco, combinando distribuições dos pesos e otimização genética, se comportam na PETR4. Eu avaliei a acurácia fora da amostra e o custo computacional, usando uma ESN com inicialização Normal como referência e modelos GRU e LSTM como comparadores. A pergunta é experimental e delimitada. Ela busca identificar o comportamento dessas configurações nas condições adotadas. A avaliação de uma estratégia de negociação ou de rentabilidade exigiria outro desenho de pesquisa.

*Apoio para consulta: Monografia v010, Introdução, p. 17–19; gráfico com último fechamento disponível de cada mês extraído da série local, sem agregar resultados experimentais*

## 03 Objetivo e hipóteses

**01:45–02:50 · 65 segundos**

### Fala

O objetivo geral foi investigar o desempenho de redes de estados de eco na previsão de um passo à frente do preço ajustado da PETR4. Para isso, o trabalho considerou cinco hipóteses. A primeira trata do desempenho da ESN em relação à GRU e à LSTM especificadas no protocolo. A segunda examina o custo do ajuste depois que a configuração já foi selecionada. A terceira pergunta se alguma inicialização não gaussiana apresenta erro menor que a referência Normal com Normal. A quarta trata da exploração evolutiva com inicialização por hipercubo latino e mutação cataclísmica. A quinta examina configurações baseadas em distribuições ajustadas empiricamente aos dados de treino. Essas hipóteses receberam níveis diferentes de apoio. Vou retomar a avaliação de cada uma depois de apresentar os resultados.

*Apoio para consulta: Monografia v010, Introdução, H1–H5, p. 17–19*

## 04 Fundamentação e trabalhos relacionados

**02:50–03:50 · 60 segundos**

### Fala

A fundamentação reúne computação de reservatório, otimização genética e preparação de séries financeiras. A ESN segue o princípio descrito por Jaeger: manter os pesos internos fixos durante o ajuste de cada modelo e estimar a camada de saída. Trabalhos como o de Araújo e colaboradores motivam o estudo de distribuições e busca genética. O BovDB, de Cardoso e colaboradores, fornece o contexto metodológico do ajuste de eventos corporativos. A monografia de Lampugnani aparece como referência correlata, com comparação descritiva e protocolo distinto. A revisão utilizou uma coleção de trinta e quatro documentos e buscas complementares. Seu papel foi fundamentar as escolhas e situar o experimento. Os registros de seleção são parciais, de modo que o trabalho não apresenta essa coleção como uma revisão sistemática exaustiva.

*Apoio para consulta: Monografia v010, cap. 2, p. 20–40, e seção 3.8.3, p. 51–53. Jaeger (2007), Araújo et al. (2025), Cardoso et al. (2022b), Lampugnani (2026); 24 documentos com palavras-chave entre os 34 da coleção*

## 05 Dados e divisão temporal

**03:50–05:10 · 80 segundos**

### Fala

A série contém cinco mil cento e noventa e oito observações diárias, de três de janeiro de dois mil a trinta de dezembro de dois mil e vinte. A variável-alvo é o preço de fechamento ajustado da PETR4. O orientador forneceu os arquivos já ajustados, e a pesquisa partiu desses valores. A divisão foi cronológica: duas mil e seiscentas observações para treino, mil duzentas e noventa e nove para validação e a mesma quantidade para teste. O treino termina em julho de dois mil e dez, a validação em setembro de dois mil e quinze, e o teste termina em dezembro de dois mil e vinte. A busca combina erros de treino e validação. Na rodada controlada, o escalonamento de GRU e LSTM usa somente o treino, e a continuidade temporal entre os blocos foi verificada. A pesquisa não comparou a série bruta com a ajustada em condições idênticas, portanto não estima o ganho isolado do ajuste corporativo.

*Apoio para consulta: Monografia v010, seção 3.2, p. 42–43*

## 06 Rede neural de estados de eco

**05:10–06:30 · 80 segundos**

### Fala

A rede de estados de eco utiliza um reservatório recorrente para transformar a sequência de entrada em estados internos. Há três componentes importantes. A matriz Win conecta a entrada ao reservatório. A matriz W define as conexões recorrentes que dão memória à dinâmica. A matriz Wout produz a saída prevista a partir da informação disponível nos estados e na entrada. Durante o ajuste de cada modelo, Win e W permanecem fixas. A parte estimada é Wout, por regressão Ridge, que inclui regularização. Na pesquisa, as distribuições geram os elementos de Win e W, e o reservatório recebe reescalamento pelo raio espectral. A taxa de vazamento controla quanto do estado anterior permanece na atualização. Essa organização permite um ajuste final rápido, mas a escolha de uma boa configuração ainda exige busca. Também é importante observar que controlar o raio espectral, por si só, não garante todas as propriedades desejadas para qualquer reservatório.

*Apoio para consulta: Monografia v010, seção 3.3, p. 44–45. Jaeger (2007)*

## 07 Busca genética de hiperparâmetros

**06:30–07:50 · 80 segundos**

### Fala

O algoritmo genético seleciona configurações da ESN. No motor atual, cada indivíduo usa um cromossomo de cinquenta e cinco bits para representar cinco hiperparâmetros: taxa de vazamento, raio espectral, descarte dos estados iniciais, tamanho do reservatório e regularização Ridge. A função de aptidão corresponde ao negativo de uma combinação de erros: quarenta por cento do MAE de treino e sessenta por cento do MAE de validação. O sinal permite maximizar a aptidão enquanto se procura reduzir o erro. O motor integra amostragem por hipercubo latino, ou LHS, na inicialização populacional e um mecanismo cataclísmico para reagir à estagnação. Esse mecanismo é inspirado no CHC, sem implementar o algoritmo CHC completo. As execuções principais tiveram limite de dez mil gerações por cenário, com possibilidade de parada por estagnação. A correspondência de todos os detalhes do motor atual com cada execução histórica permanece condicionada aos registros preservados.

*Apoio para consulta: Monografia v010, seção 3.4, p. 46–47, e Quadro 3, p. 45; repartição em bits 17,17,7,5,9 conferida no Quadro 3*

## 08 Cinco ondas experimentais

**07:50–08:55 · 65 segundos**

### Fala

As quarenta e cinco execuções históricas foram organizadas em cinco ondas. A primeira avaliou famílias de caudas pesadas, com nove execuções. A segunda examinou choques e assimetria, também com nove. A terceira concentrou seis configurações relacionadas à esparsidade, e a quarta reuniu seis controles canônicos. A quinta incluiu quinze configurações com distribuições ajustadas empiricamente ao treino. A notação usada nos resultados identifica primeiro a distribuição de Win e depois a de W. Por exemplo, Laplace com Normal significa entrada gerada por Laplace e reservatório gerado por Normal. Cada resultado combina distribuição, hiperparâmetros e uma realização estocástica. Assim, a comparação descreve configurações avaliadas e não isola automaticamente o efeito causal de trocar uma única distribuição. Essa distinção será importante para interpretar os pequenos ganhos observados.

*Apoio para consulta: Monografia v010, Quadro 2 e seção 3.3, p. 44–45*

## 09 Três blocos de evidência

**08:55–09:50 · 55 segundos**

### Fala

A apresentação distingue três blocos de evidência. O primeiro contém as quarenta e cinco execuções históricas e sustenta as comparações descritivas entre configurações. O segundo é uma rodada complementar controlada, com novos pesos e semente fixa, que permite comparar erros datados com o teste de Diebold–Mariano. O terceiro é um lote legado de doze cenários com duzentas gerações, usado para ilustrar a evolução da aptidão e as previsões. O cenário ilustrativo foi selecionado pelo maior fitness de treino e validação nesse lote. Ele permanece fora das quarenta e cinco execuções históricas. Essa organização evita atribuir os valores do teste estatístico ao histórico ou interpretar uma figura ilustrativa como se representasse o melhor resultado das cinco ondas.

*Apoio para consulta: Monografia v010, seções 3.6–3.8, p. 47–53, e 4.2, p. 55–57; procedencia.json do lote ilustrativo*

## 10 ESNAUTO como artefato de software

**09:50–10:55 · 65 segundos**

### Fala

O ESNAUTO organiza a execução do protocolo em um artefato de software. A aplicação permite preparar a entrada recebida, configurar os modelos, acompanhar execuções e consultar métricas e visualizações. O histórico ajuda a comparar configurações e identificar resultados de interesse. A contribuição de Engenharia de Software aparece na integração dessas atividades em um fluxo utilizável e na organização dos artefatos experimentais. Os códigos em R foram fornecidos pelo orientador. Minha contribuição compreendeu sua adaptação ao contexto da pesquisa e o desenvolvimento da interface. Essa atribuição é importante para delimitar a autoria: os fundamentos da ESN e as técnicas de otimização têm antecedentes, enquanto o trabalho aplica e organiza esses elementos no ESNAUTO. A rodada complementar também tornou mais completa a preservação de previsões, modelos, matrizes e metadados para auditoria.

*Apoio para consulta: Monografia v010, seções 3.1, p. 41–42, e 4.10, p. 65–66; Quadro 6, p. 72*

## 11 Critérios de avaliação

**10:55–11:45 · 50 segundos**

### Fala

A avaliação usa três métricas de previsão. O MAE mede a média do erro em módulo e permite interpretar o desvio médio na escala do preço. O RMSE atribui maior peso a erros elevados. O R quadrado descreve a aderência global, mas exige cautela quando se prevê uma série de preços com forte persistência. Um R quadrado alto pode coexistir com pouca vantagem sobre um comparador simples. O tempo computacional aparece separado em busca de hiperparâmetros, ajuste da configuração escolhida e treinamento dos modelos de comparação. Essa separação permite avaliar a eficiência da etapa de ajuste sem esconder o custo necessário para descobrir a configuração.

*Apoio para consulta: Monografia v010, seção 3.6, p. 47–49, e Tabela 5, p. 60*

## 12 Resultados históricos de previsão

**11:45–13:00 · 75 segundos**

### Fala

Nos resultados históricos, Laplace com Normal apresentou o menor MAE, aproximadamente zero vírgula trezentos e vinte e sete. Os gráficos mostram os valores documentados para essa configuração, para a GRU e para a LSTM. O RMSE da ESN foi aproximadamente zero vírgula quatrocentos e noventa e nove, e o R quadrado foi zero vírgula novecentos e noventa e quatro. Considerando o conjunto das ondas, quarenta e quatro das quarenta e cinco execuções apresentaram MAE menor que os valores históricos documentados para GRU e LSTM. Essa é uma comparação descritiva: resume o que foi observado nos registros disponíveis. Os vetores completos dessas execuções não foram integralmente preservados, por isso os testes estatísticos apresentados adiante pertencem à rodada complementar. Também houve diferença de orçamento, pois a ESN recebeu uma busca extensa e os modelos de comparação utilizaram arquiteturas definidas no protocolo.

*Apoio para consulta: Monografia v010, resumo e Tabela 3, p. 55; registro_GA_RUN_0030.csv*

## 13 Inicializações e ganhos observados

**13:00–14:05 · 65 segundos**

### Fala

Quando a comparação se concentra nas inicializações da ESN, o controle Normal com Normal apresentou MAE de aproximadamente zero vírgula três dois oito quatro. Laplace com Normal apresentou aproximadamente zero vírgula três dois sete dois. A redução relativa é de aproximadamente zero vírgula trezentos e quarenta e sete por cento. Portanto, o ganho existe nos registros, mas sua magnitude é pequena. Outro resultado importante é que a configuração de menor MAE não coincide com a de menor RMSE. Laplace com Cauchy apresentou o menor RMSE, aproximadamente zero vírgula quatro nove cinco quatro, e o maior R quadrado. A interpretação considera também os hiperparâmetros e o sorteio do reservatório. O trabalho oferece evidência pontual favorável a configurações não gaussianas, sem estabelecer uma distribuição universalmente superior.

*Apoio para consulta: Monografia v010, Tabela 4, p. 58, resumo e seção 5.1, p. 67–68*

## 14 Exemplo visual preservado

**14:05–15:00 · 55 segundos**

### Fala

Este gráfico permite visualizar como uma previsão acompanha a série observada no conjunto de teste. Ele foi extraído da própria monografia e pertence ao cenário GED com Uniforme do lote ilustrativo de duzentas gerações. A escolha desse cenário considerou a aptidão de treino e validação dentro do lote preservado. O gráfico ajuda a compreender a saída produzida pelo sistema, mas sua aparência não substitui as métricas e os testes. Além disso, a proximidade entre curvas de preços deve ser interpretada com cautela por causa da persistência temporal da série. Os números apresentados para as quarenta e cinco execuções e para a rodada Diebold–Mariano permanecem associados aos seus próprios protocolos. Aqui, a função da imagem é ilustrar o comportamento de uma execução identificada.

*Apoio para consulta: Monografia v010, Figura 6 e seção 4.2, p. 55–57; reports/revisao_orientador_petr4/procedencia.json*

## 15 Rodada controlada complementar

**15:00–16:15 · 75 segundos**

### Fala

A rodada controlada foi necessária porque não havia vetores históricos completos para um teste retrospectivo. Ela utilizou uma única semente previamente fixada, identificada no slide por dois zero dois seis zero nove dois seis. A ESN manteve os hiperparâmetros documentados da configuração de referência Laplace com Normal, incluindo um reservatório de vinte e dois neurônios, e recebeu novos pesos. Não houve uma nova busca genética nessa rodada. A saída foi ajustada exclusivamente com alvos de treino, e os estados seguiram cronologicamente pela validação e pelo teste. Cada modelo gerou mil duzentas e noventa e nove previsões. O alinhamento por data produziu a janela comum previamente definida de mil duzentas e noventa e oito observações, de trinta de setembro de dois mil e quinze a trinta de dezembro de dois mil e vinte. Os arquivos e os modelos dessa rodada foram preservados.

*Apoio para consulta: Monografia v010, seção 3.7, p. 49–50; execution_manifest.json e previsoes_dm.csv do PETR4-DM*

## 16 Erros na janela comum controlada

**16:15–17:25 · 70 segundos**

### Fala

Na janela comum da rodada controlada, a ESN apresentou MAE de aproximadamente zero vírgula trezentos e vinte e nove, contra zero vírgula quatrocentos e dezoito da GRU e zero vírgula quatrocentos e sessenta e sete da LSTM. No RMSE, os valores foram aproximadamente zero vírgula quatrocentos e noventa e oito, zero vírgula quinhentos e noventa e dois e zero vírgula seiscentos e trinta e cinco, respectivamente. Os gráficos mostram o mesmo ordenamento nas duas métricas, sempre com menor erro para a ESN. A comparação usa a mesma janela de datas e a mesma escala de avaliação. Esses valores pertencem aos novos pesos da rodada controlada e diferem dos números históricos. A conclusão é que a ESN selecionada apresentou melhor desempenho entre os três modelos avaliados nessa execução. Para avaliar a diferença de acurácia, o passo seguinte aplica o teste de Diebold–Mariano.

*Apoio para consulta: Monografia v010, seção 4.8, p. 62–63; resultados_dm.csv e previsoes_dm.csv do PETR4-DM*

## 17 Comparação estatística de acurácia

**17:25–18:40 · 75 segundos**

### Fala

O teste de Diebold–Mariano avalia a hipótese de igualdade da acurácia preditiva sob uma função de perda definida. Foram estabelecidos quatro contrastes: ESN contra GRU e ESN contra LSTM, usando perda absoluta e quadrática. Os quatro testes rejeitaram a hipótese nula ao nível individual de cinco por cento. A direção da comparação foi determinada pelo diferencial médio de perda, que favoreceu a ESN em todos os casos. Isso apoia a primeira hipótese dentro da rodada controlada. Há condições importantes para interpretar os valores de p: foi usada uma única semente, sem correção para múltiplas comparações. Com horizonte de um passo, o estimador utilizado considera a defasagem zero e não incorpora eventual dependência em outras defasagens. Além disso, a configuração foi escolhida a partir da exploração histórica. A inferência é complementar e restrita à execução analisada.

*Apoio para consulta: Monografia v010, seção 3.7, p. 49–50, e Tabela 6, p. 63; resultados_dm.csv. Diebold e Mariano (1995)*

## 18 Custo de ajuste e custo da busca

**18:40–19:45 · 65 segundos**

### Fala

O custo computacional precisa ser lido por etapa. Depois da seleção da configuração, o ajuste analítico da ESN demandou cerca de cinco centésimos de segundo. Os tempos documentados de treinamento foram de vinte e oito vírgula oito segundos para a GRU e trinta e cinco vírgula quatro para a LSTM. Essa comparação apoia o baixo custo do ajuste final da ESN nas condições avaliadas. Entretanto, a descoberta da configuração exigiu uma busca genética com custo bem maior. Por cenário, as buscas levaram aproximadamente de vinte e um a cento e dois minutos. Somadas, as quarenta e cinco buscas totalizaram cerca de trinta e sete vírgula nove horas. Portanto, a vantagem observada no ajuste posterior convive com um custo de exploração relevante. A hipótese de eficiência se refere à etapa de ajuste da configuração escolhida.

*Apoio para consulta: Monografia v010, Tabela 5 e seção 4.6, p. 60–61*

## 19 Avaliação das cinco hipóteses

**19:45–20:55 · 70 segundos**

### Fala

Retomando as hipóteses, H1 recebeu apoio descritivo no histórico e apoio inferencial complementar nos quatro contrastes da rodada controlada. H2 recebeu apoio quanto ao custo de ajuste da configuração selecionada, mantendo a busca genética em separado. H3 recebeu apoio pontual, porque algumas configurações não gaussianas apresentaram erros menores que o controle Normal com Normal. H4 não teve seu efeito demonstrado. O software integra LHS e mecanismo cataclísmico, mas a pesquisa não mediu diversidade nem realizou uma ablação para isolar a contribuição desses mecanismos. Em H5, a quinta onda mostrou baixa dispersão entre configurações, sem demonstrar menor variabilidade entre repetições de sementes ou superioridade geral de erro. A avaliação distingue a presença de um recurso no software da demonstração experimental de seu efeito. Essa distinção mantém as conclusões proporcionais às evidências produzidas.

*Apoio para consulta: Monografia v010, Quadro 5, p. 63, e Conclusão, p. 70–72*

## 20 Contribuições do trabalho

**20:55–21:55 · 60 segundos**

### Fala

A contribuição experimental está na avaliação documentada das configurações para a PETR4 e na apresentação das condições de comparação. A contribuição de Engenharia de Software está na adaptação das rotinas recebidas e no desenvolvimento da interface do ESNAUTO, organizando configurações, métricas, histórico e visualizações. A rodada controlada acrescentou uma forma mais completa de preservar previsões, matrizes, modelos e metadados necessários à auditoria. Os fundamentos da rede e os métodos de otimização têm antecedentes na literatura. O trabalho reconhece esses antecedentes e delimita a participação do autor. A principal entrega é uma aplicação e uma avaliação experimental com resultados e limites identificados. Essa organização também permite distinguir aquilo que está documentado no histórico daquilo que pode ser reproduzido a partir dos artefatos completos da rodada complementar.

*Apoio para consulta: Monografia v010, seção 4.10, p. 65–66, Quadro 6, p. 72, e Conclusão, p. 70–72*

## 21 Limitações e alcance das conclusões

**21:55–23:15 · 80 segundos**

### Fala

As limitações ajudam a definir onde as conclusões se aplicam. O estudo considerou um único ativo, um período histórico e previsão de um passo à frente. Os modelos tiveram orçamentos distintos de seleção, e a rodada estatística utilizou uma semente. A preservação parcial dos vetores e matrizes históricos restringe a reprodução exata de cada execução. Na revisão bibliográfica, os registros parciais de seleção limitam a alegação de cobertura do campo. Também faltam comparações controladas para separar o efeito do ajuste dos preços, das distribuições e dos mecanismos evolutivos. Por fim, o trabalho não demonstrou vantagem sobre a previsão que repete o último preço observado. Um R quadrado alto não resolve essa questão. Não foram avaliados custos de transação, estratégias de compra e venda ou retorno de carteira. As conclusões dizem respeito ao erro preditivo e ao custo das etapas medidas, dentro do protocolo adotado.

*Apoio para consulta: Monografia v010, seções 3.8, p. 50–53, e 5.1–5.2, p. 67–69; Conclusão, p. 70–72*

## 22 Continuidade da pesquisa

**23:15–24:15 · 60 segundos**

### Fala

A continuidade pode ampliar os controles experimentais e a rastreabilidade. Uma comparação com persistência, na mesma escala e janela, ajudaria a avaliar o ganho em relação a um referencial simples. Repetições com diferentes sementes permitiriam caracterizar a variabilidade de cada configuração. Ablações e orçamentos comparáveis ajudariam a examinar a contribuição dos componentes e a comparação entre arquiteturas. No software, a monografia prevê persistência mais estruturada de previsões, matrizes e metadados, além de melhorias na interface e no acompanhamento dos modelos. Essa evolução está prevista sob o nome JANUS. A extensão à VALE3 permanece como continuidade experimental, fora dos resultados principais apresentados. Essas possibilidades decorrem dos limites identificados e exigem protocolos próprios para produzir novas evidências.

*Apoio para consulta: Monografia v010, seção 5.3, p. 69; persistência e ablações também discutidas nas seções 5.1–5.2, p. 67–69*

## 23 Conclusão

**24:15–25:00 · 45 segundos**

### Fala

Concluo que, para a PETR4 e sob o protocolo adotado, redes de estados de eco pequenas e otimizadas constituíram uma alternativa competitiva para a tarefa investigada. Os resultados históricos mostraram ganhos pontuais de configurações não gaussianas, e a rodada controlada apresentou menor perda para a ESN frente às arquiteturas GRU e LSTM definidas no trabalho. O ajuste da configuração selecionada foi rápido, com um custo de busca que deve permanecer explícito. O ESNAUTO contribuiu ao integrar a aplicação e organizar o processo experimental. Agradeço a atenção da banca e encerro esta apresentação, deixando os resultados, as contribuições e os limites como base para a discussão na defesa.

*Apoio para consulta: Monografia v010, Conclusão, p. 70–72*
