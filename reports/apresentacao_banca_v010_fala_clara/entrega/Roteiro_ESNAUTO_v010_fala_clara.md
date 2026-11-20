# Roteiro ESNAUTO com fala clara

Base editorial v010. Planejamento de 25 minutos. Fontes e orientações ficam fora da fala. A duração real depende do ensaio.

## 01 Previsão do preço de fechamento ajustado da PETR4

00:00–00:40 · 40 segundos reservados

Olá, eu sou Maycon Garcia Silva, do curso de Engenharia de Software da Universidade de Rio Verde. Neste trabalho, orientado pelo professor doutor Fabian Corrêa Cardoso, eu estudei uma forma de prever o preço de fechamento ajustado da ação PETR4.

Para isso, usei uma rede neural chamada rede de estados de eco e um algoritmo genético para procurar boas configurações dessa rede. Também trabalhei na adaptação e na interface do sistema ESNAUTO. Vou mostrar como organizei os testes, o que os resultados indicam e até onde podemos chegar com essas conclusões.

Consulta fora da fala: Monografia v010, capa e resumo

## 02 Problema de pesquisa

00:40–01:45 · 65 segundos reservados

A pergunta que guiou o trabalho foi: usando os preços anteriores da PETR4, como essa rede se sai ao prever o próximo fechamento? Além de olhar o erro da previsão, eu quis saber quanto tempo o computador leva para ajustar o modelo.

O gráfico mostra como o preço mudou ao longo dos anos. Há períodos de alta, de queda e de mudanças mais fortes. Esse comportamento ajuda a entender por que vale a pena testar diferentes configurações, em vez de assumir que uma única escolha vai funcionar bem em qualquer situação.

Eu comparei a rede de estados de eco com duas outras redes usadas para sequências de dados: GRU e LSTM. O foco foi avaliar previsões. Não testei uma estratégia de compra e venda de ações.

Consulta fora da fala: Monografia v010, Introdução, p. 17–19; gráfico com último fechamento disponível de cada mês extraído da série local, sem agregar resultados experimentais

## 03 Objetivo e hipóteses

01:45–02:50 · 65 segundos reservados

O objetivo foi estudar se essas configurações da rede poderiam produzir boas previsões para a PETR4. Organizei essa investigação em cinco hipóteses, que aparecem aqui como H1 até H5.

A primeira pergunta se a rede consegue competir com GRU e LSTM. A segunda olha para o tempo necessário para ajustar uma configuração já escolhida. A terceira investiga se mudar a forma de gerar os pesos iniciais pode trazer resultados melhores que a distribuição Normal usada como referência.

A quarta trata dos recursos do algoritmo genético para explorar diferentes soluções. A quinta considera distribuições ajustadas aos próprios dados de treino. Mais adiante, vou voltar a cada uma para mostrar o que os testes sustentaram e o que ainda precisa ser investigado.

Consulta fora da fala: Monografia v010, Introdução, H1–H5, p. 17–19

## 04 Fundamentação e trabalhos relacionados

02:50–03:50 · 60 segundos reservados

O trabalho se apoia em três assuntos: redes de estados de eco, busca genética e preparação de dados financeiros. Na proposta de Jaeger, uma característica da rede de estados de eco é manter as conexões internas fixas durante o ajuste e calcular os pesos da saída. Vou explicar esse funcionamento no próximo conjunto de slides.

Os trabalhos de Araújo e colaboradores ajudaram a fundamentar o estudo das distribuições e da busca genética. O BovDB, de Cardoso e colaboradores, dá o contexto do ajuste dos preços por eventos corporativos. O trabalho de Lampugnani também aparece como referência relacionada, com testes organizados de outra forma.

Ao todo, a revisão reuniu trinta e quatro documentos e buscas complementares. Essa coleção ajudou a orientar a pesquisa, mas os registros disponíveis não permitem dizer que ela cobre toda a literatura do tema.

Consulta fora da fala: Monografia v010, cap. 2, p. 20–40, e seção 3.8.3, p. 51–53. Jaeger (2007), Araújo et al. (2025), Cardoso et al. (2022b), Lampugnani (2026); 24 documentos com palavras-chave entre os 34 da coleção

## 05 Dados e divisão temporal

03:50–05:10 · 80 segundos reservados

Usei cinco mil cento e noventa e oito observações diárias da PETR4, entre os anos de dois mil e dois mil e vinte. Os arquivos vieram do orientador com os preços já ajustados. Isso significa que o estudo parte dessa série recebida; eu não reconstruí todo o processo original do ajuste.

A divisão respeitou a ordem das datas. A primeira parte, com duas mil e seiscentas observações, serviu para treino. A parte seguinte serviu para validação, ou seja, para ajudar a escolher as configurações. A última ficou para teste, para avaliar o resultado em dados posteriores. Validação e teste tiveram mil duzentas e noventa e nove observações cada.

Essa ordem é importante porque a tarefa é prever o futuro a partir do passado. Na rodada controlada, até a preparação da escala dos dados de GRU e LSTM usou somente o treino.

Consulta fora da fala: Monografia v010, seção 3.2, p. 42–43

## 06 Rede neural de estados de eco

05:10–06:30 · 80 segundos reservados

Aqui está a estrutura da rede de estados de eco, que vou chamar de ESN. Podemos acompanhar o funcionamento da esquerda para a direita: a informação entra, passa pelo reservatório e chega à saída, que produz a previsão.

O reservatório é uma rede de conexões internas. Como essas conexões são recorrentes, o estado atual também depende do estado anterior. Por isso, ele consegue carregar informação da sequência. No slide, Win representa as conexões de entrada, W representa as conexões internas e Wout representa os pesos da saída.

Durante o ajuste, Win e W ficam fixas. O cálculo se concentra em Wout, usando regressão Ridge, que ajuda a controlar os valores dos pesos. Isso torna o ajuste final rápido. Ainda assim, precisamos escolher bem o tamanho do reservatório e outras configurações para que a rede funcione bem.

Consulta fora da fala: Monografia v010, seção 3.3, p. 44–45. Jaeger (2007)

## 07 Busca genética de hiperparâmetros

06:30–07:50 · 80 segundos reservados

Para procurar essas configurações, usei um algoritmo genético. Ele trabalha com várias opções, avalia o erro de cada uma e produz novas opções a partir das que foram selecionadas. Esse processo se repete ao longo das gerações.

No motor atual do sistema, cada opção é representada por cinquenta e cinco bits. Esses bits guardam cinco escolhas: quanto do estado anterior a rede mantém, a escala das conexões internas, quantos estados iniciais são descartados, o tamanho do reservatório e a regularização da saída.

A avaliação combina o erro de treino com o de validação, dando mais peso à validação. O sistema também usa o hipercubo latino para distribuir as opções iniciais e um mecanismo cataclísmico para renovar soluções quando a busca para de avançar. Esse mecanismo é inspirado no CHC, mas não corresponde ao CHC completo. Esses detalhes descrevem o motor atual; os registros históricos não preservam tudo de cada execução.

Consulta fora da fala: Monografia v010, seção 3.4, p. 46–47, e Quadro 3, p. 45; repartição em bits 17,17,7,5,9 conferida no Quadro 3

## 08 Cinco ondas experimentais

07:50–08:55 · 65 segundos reservados

Os resultados históricos estão organizados em cinco grupos de testes, chamados de ondas. Somando os grupos, são quarenta e cinco execuções.

As duas primeiras ondas tiveram nove execuções cada e exploraram famílias de distribuições com comportamentos diferentes. A terceira teve seis configurações relacionadas à esparsidade, isto é, à presença de conexões com peso zero. A quarta teve seis controles de referência. A quinta reuniu quinze configurações com distribuições ajustadas aos dados de treino.

Quando aparece uma combinação como Laplace com Normal, o primeiro nome indica como foram gerados os pesos da entrada. O segundo indica os pesos do reservatório. É essa ordem que vou usar nos resultados. Cada execução também envolve outras configurações e um sorteio dos pesos; por isso, uma diferença no erro não pode ser atribuída somente ao nome da distribuição.

Consulta fora da fala: Monografia v010, Quadro 2 e seção 3.3, p. 44–45

## 09 Três blocos de evidência

08:55–09:50 · 55 segundos reservados

Antes dos resultados, é importante separar três conjuntos que aparecem na apresentação. O primeiro é o histórico das quarenta e cinco execuções, que permite comparar os resultados das ondas.

O segundo é uma rodada complementar para comparar os modelos nas mesmas datas e aplicar um teste estatístico. Nela, os pesos foram gerados novamente, com uma semente fixa. A semente é o número que controla o sorteio e permite repeti-lo.

O terceiro é um lote de duzentas gerações, usado apenas para ilustrar o funcionamento e as previsões. Ele fica fora das quarenta e cinco execuções. Portanto, os números do histórico, o teste estatístico e a figura ilustrativa vêm de conjuntos diferentes. Vou manter essa separação ao explicar cada resultado.

Consulta fora da fala: Monografia v010, seções 3.6–3.8, p. 47–53, e 4.2, p. 55–57; procedencia.json do lote ilustrativo

## 10 ESNAUTO como artefato de software

09:50–10:55 · 65 segundos reservados

O ESNAUTO é o sistema que reúne essas atividades. Por ele, é possível configurar os modelos, acompanhar as execuções e consultar os erros, os gráficos e o histórico. Isso facilita trabalhar com várias configurações e depois localizar os resultados para comparação.

Os códigos em R foram fornecidos pelo orientador. Minha participação foi adaptar essas rotinas ao contexto da pesquisa e desenvolver a interface. A contribuição de Engenharia de Software está nessa integração e na organização do processo de uso do sistema.

Também organizei os registros da rodada complementar, incluindo previsões, modelos e informações das execuções. Assim, essa rodada ficou com material mais completo para conferência. Essa distinção de autoria é importante: os métodos já existem na literatura; o trabalho os aplica e os organiza no ESNAUTO.

Consulta fora da fala: Monografia v010, seções 3.1, p. 41–42, e 4.10, p. 65–66; Quadro 6, p. 72

## 11 Critérios de avaliação

10:55–11:45 · 50 segundos reservados

Usei três medidas para avaliar as previsões. O MAE mostra o tamanho médio do erro, tanto para previsões acima quanto abaixo do preço observado. Quanto menor, melhor. Por exemplo, um MAE de trinta centavos significa um desvio médio desse valor na escala do preço.

O RMSE dá mais peso aos erros grandes. O R quadrado descreve quanto as previsões acompanham os preços observados, mas exige cuidado: preços próximos no tempo já podem ser parecidos.

Também medi o tempo de procurar uma configuração e o tempo de ajustar a rede já escolhida.

Consulta fora da fala: Monografia v010, seção 3.6, p. 47–49, e Tabela 5, p. 60

## 12 Resultados históricos de previsão

11:45–13:00 · 75 segundos reservados

Começando pelo histórico, este gráfico compara o MAE da ESN Laplace com Normal com os valores registrados para GRU e LSTM. Como erros menores são melhores, as barras mais baixas indicam resultados melhores nessa medida.

A ESN ficou com um erro médio de aproximadamente trinta e três centavos. A GRU ficou perto de trinta e seis centavos, e a LSTM, de quarenta e cinco centavos. Olhando as cinco ondas, quarenta e quatro das quarenta e cinco execuções da ESN tiveram MAE menor que os valores históricos desses comparadores.

Esse é um resultado favorável nos registros, mas há dois cuidados. A ESN passou por uma busca extensa de configurações, e os comparadores tiveram escolhas de arquitetura definidas no trabalho. Além disso, parte dos arquivos completos das execuções antigas não foi preservada. Por isso, o teste estatístico vem da rodada complementar, que vou mostrar depois.

Consulta fora da fala: Monografia v010, resumo e Tabela 3, p. 55; registro_GA_RUN_0030.csv

## 13 Inicializações e ganhos observados

13:00–14:05 · 65 segundos reservados

Agora a comparação é entre duas configurações da própria ESN. A referência usa Normal na entrada e no reservatório. A outra usa Laplace na entrada e Normal no reservatório.

As barras são muito próximas: os dois erros médios ficam perto de trinta e três centavos. Usando os valores completos, que estão na tela, a redução foi de cerca de zero vírgula trinta e cinco por cento. Então houve uma melhora registrada, mas ela foi pequena. Vale olhar a escala do gráfico para não dar a essa diferença um tamanho maior do que ela tem.

Outra combinação, Laplace com Cauchy, apresentou o menor RMSE. Isso mostra que a escolha da melhor configuração também depende da medida usada. Esses testes favorecem algumas configurações, mas não mostram que uma distribuição será sempre melhor que as outras.

Consulta fora da fala: Monografia v010, Tabela 4, p. 58, resumo e seção 5.1, p. 67–68

## 14 Exemplo visual preservado

14:05–15:00 · 55 segundos reservados

Este gráfico ajuda a visualizar uma previsão. Uma curva representa o preço observado, e a outra, o preço previsto. A parte de baixo amplia os últimos cem pregões.

A figura veio do lote ilustrativo de duzentas gerações, na combinação GED com Uniforme. Esse cenário foi escolhido pelo desempenho no treino e na validação daquele lote. Ele fica fora do histórico das quarenta e cinco execuções e da rodada estatística.

As curvas próximas ajudam a enxergar o comportamento da rede. Mas essa aparência não basta: preços de dias próximos já tendem a ser parecidos. Por isso, considero o gráfico junto com as medidas de erro, sempre identificando o teste de onde ele veio.

Consulta fora da fala: Monografia v010, Figura 6 e seção 4.2, p. 55–57; reports/revisao_orientador_petr4/procedencia.json

## 15 Rodada controlada complementar

15:00–16:15 · 75 segundos reservados

Para fazer a comparação estatística, preparei uma rodada complementar com os arquivos necessários para conferir as previsões de cada modelo. A ESN usou a configuração de referência Laplace com Normal, com vinte e dois neurônios no reservatório. Mantive essas escolhas e gerei novos pesos, usando a semente indicada no slide.

Essa rodada não repetiu a busca genética. A saída da rede foi ajustada com os dados de treino, e o processamento seguiu a ordem das datas pela validação e pelo teste.

Cada modelo produziu mil duzentas e noventa e nove previsões. Depois de alinhar os arquivos pelas datas, a comparação usou mil duzentas e noventa e oito datas comuns, entre setembro de dois mil e quinze e dezembro de dois mil e vinte. Assim, os erros dos três modelos foram comparados nos mesmos dias.

Consulta fora da fala: Monografia v010, seção 3.7, p. 49–50; execution_manifest.json e previsoes_dm.csv do PETR4-DM

## 16 Erros na janela comum controlada

16:15–17:25 · 70 segundos reservados

Aqui estão os erros dessa rodada complementar. No gráfico da esquerda, o MAE da ESN ficou perto de trinta e três centavos. O da GRU ficou em cerca de quarenta e dois, e o da LSTM, em quarenta e sete centavos.

No gráfico da direita, que mostra o RMSE, a ordem foi a mesma: a ESN teve o menor erro, seguida pela GRU e pela LSTM. A altura das barras facilita ver essa diferença, e os valores mais precisos estão acima delas.

Esses números já são da nova execução, com os novos pesos. Eles não substituem os valores históricos apresentados antes. O resultado que podemos afirmar aqui é que, nessa comparação com as mesmas datas, a ESN selecionada teve menor erro nas duas medidas. O próximo passo foi examinar essa diferença com um teste estatístico.

Consulta fora da fala: Monografia v010, seção 4.8, p. 62–63; resultados_dm.csv e previsoes_dm.csv do PETR4-DM

## 17 Comparação estatística de acurácia

17:25–18:40 · 75 segundos reservados

Usei o teste de Diebold–Mariano para comparar os erros dos modelos. A pergunta do teste é se eles têm a mesma acurácia média, considerando a forma de medir o erro escolhida.

Fiz quatro comparações: ESN com GRU e ESN com LSTM, tanto com erro absoluto quanto com erro ao quadrado. Em todas, o teste rejeitou a igualdade ao nível individual de cinco por cento. Como a ESN teve menor perda média nas quatro comparações, o resultado foi favorável a ela nessa rodada. A tabela mostra os valores de p obtidos no teste.

Há limites nessa análise: foi usado um único sorteio controlado, sem correção para as quatro comparações, e o cálculo considerou a defasagem zero. A configuração também veio da busca histórica. Portanto, o teste apoia o resultado dessa rodada, mas não demonstra superioridade em qualquer situação.

Consulta fora da fala: Monografia v010, seção 3.7, p. 49–50, e Tabela 6, p. 63; resultados_dm.csv. Diebold e Mariano (1995)

## 18 Custo de ajuste e custo da busca

18:40–19:45 · 65 segundos reservados

O resultado de tempo tem duas partes. Depois de escolher a configuração, ajustar a ESN levou cerca de cinco centésimos de segundo. Os tempos registrados para GRU e LSTM foram, respectivamente, cerca de vinte e nove e trinta e cinco segundos.

Essa etapa da ESN foi rápida porque o ajuste se concentra nos pesos de saída. Mas, antes dela, foi preciso encontrar uma boa configuração. A busca genética levou de vinte e um a cento e dois minutos por cenário. Somando as quarenta e cinco buscas, foram aproximadamente trinta e oito horas.

Portanto, quando eu digo que a ESN teve baixo custo de ajuste, estou falando da rede já selecionada. Para avaliar o esforço completo do trabalho, também precisamos considerar o tempo gasto na busca. São etapas diferentes e os dois tempos estão apresentados aqui.

Consulta fora da fala: Monografia v010, Tabela 5 e seção 4.6, p. 60–61

## 19 Avaliação das cinco hipóteses

19:45–20:55 · 70 segundos reservados

Voltando às cinco hipóteses, a primeira recebeu apoio nos resultados históricos e na rodada estatística: a ESN foi competitiva com os modelos comparados, dentro dessas condições. A segunda recebeu apoio para o ajuste rápido da configuração já escolhida.

A terceira teve apoio em algumas combinações, que apresentaram erro menor que a referência Normal com Normal. Isso não significa que qualquer mudança de distribuição vai melhorar o resultado.

Na quarta, os mecanismos para explorar soluções existem no sistema, mas faltou compará-los ligados e desligados para medir sua contribuição. Então esse efeito não ficou demonstrado. Na quinta, os erros ficaram próximos entre as configurações do último grupo. Porém, não fiz repetições com diferentes sementes para mostrar que elas seriam mais estáveis. Cada hipótese, portanto, precisa ser respondida de acordo com o que foi realmente medido.

Consulta fora da fala: Monografia v010, Quadro 5, p. 63, e Conclusão, p. 70–72

## 20 Contribuições do trabalho

20:55–21:55 · 60 segundos reservados

Vejo duas contribuições principais neste trabalho. A primeira é a avaliação das configurações de ESN para a PETR4, com seus resultados e as condições em que foram obtidos. Ela mostra onde apareceram diferenças de erro e ajuda a orientar os próximos testes.

A segunda é o trabalho no ESNAUTO: adaptar as rotinas recebidas, desenvolver a interface e organizar o acesso às configurações, aos gráficos e ao histórico. Isso reúne em um sistema atividades que fazem parte da pesquisa.

A rodada complementar também deixou previsões, modelos e informações mais completas para conferência. Os métodos de rede e de otimização vêm de trabalhos anteriores. Minha contribuição está na adaptação, na interface e na organização da aplicação e dos testes, respeitando essa origem e deixando claros os limites dos registros disponíveis.

Consulta fora da fala: Monografia v010, seção 4.10, p. 65–66, Quadro 6, p. 72, e Conclusão, p. 70–72

## 21 Limitações e alcance das conclusões

21:55–23:15 · 80 segundos reservados

Os resultados precisam ser lidos dentro do alcance da pesquisa. Estudei uma ação, em um período definido, com previsão do próximo passo. Isso não garante o mesmo comportamento em outras ações ou em outros períodos.

Também houve diferença no esforço de escolha das configurações dos modelos, e a rodada estatística usou uma única semente. Parte dos arquivos históricos não está completa. Na revisão da literatura, os registros de seleção também são parciais.

Outra limitação é que não separei, em testes próprios, o efeito de cada componente: o ajuste dos preços, a distribuição dos pesos e os recursos da busca genética. E não demonstrei vantagem sobre uma previsão simples que apenas repete o último preço observado. Ter curvas próximas ou R quadrado alto não resolve essa comparação. Por fim, eu não avaliei lucro, custos de negociação ou estratégias de investimento. O que avaliei foi erro de previsão e tempo computacional.

Consulta fora da fala: Monografia v010, seções 3.8, p. 50–53, e 5.1–5.2, p. 67–69; Conclusão, p. 70–72

## 22 Continuidade da pesquisa

23:15–24:15 · 60 segundos reservados

Os próximos passos vêm dessas limitações. Um deles é comparar a ESN com a previsão simples que repete o último preço. Outro é repetir as configurações com diferentes sementes para saber quanto os resultados mudam quando os pesos são sorteados novamente.

Também seria importante dar um esforço de otimização comparável aos modelos e testar os componentes da busca separadamente. Por exemplo, comparar o funcionamento com e sem determinado mecanismo, mantendo as outras condições iguais.

No software, a evolução prevista é o JANUS, com melhorias na interface e na organização dos arquivos das execuções. A VALE3 aparece como uma extensão experimental, fora dos resultados principais desta apresentação. Essas frentes precisam de testes próprios; elas não ampliam automaticamente as conclusões obtidas aqui para a PETR4.

Consulta fora da fala: Monografia v010, seção 5.3, p. 69; persistência e ablações também discutidas nas seções 5.1–5.2, p. 67–69

## 23 Conclusão

24:15–25:00 · 45 segundos reservados

Para concluir, nas condições que eu estudei, as redes de estados de eco com as configurações selecionadas foram uma alternativa competitiva para prever o fechamento ajustado da PETR4.

Os testes históricos mostraram pequenas melhorias em algumas combinações, e a rodada complementar apresentou menor erro para a ESN em relação à GRU e à LSTM avaliadas. O ajuste final foi rápido, mas encontrar a configuração exigiu uma busca demorada.

Com o ESNAUTO, o trabalho também reuniu a adaptação das rotinas, a interface e a organização dos testes. Esses resultados, junto com os limites que apresentei, são a base para a discussão na defesa. Agradeço a atenção da banca.

Consulta fora da fala: Monografia v010, Conclusão, p. 70–72
