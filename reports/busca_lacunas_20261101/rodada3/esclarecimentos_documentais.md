# Esclarecimentos específicos — rascunho, não enviado

Este arquivo registra as perguntas que a evidência atual não responde. Não houve contato com autores e não se solicita novo experimento.

## Abebe e Goshu — preparação do conjunto Cyber

No artigo DOI 10.3389/fams.2024.1398137, a seção 8.2.1 informa 363 semanas; a Tabela 5 apresenta média 5.3810 e quartis 3.9850, 5.1000 e 6.5450. O material de Gjika encaminha ao projeto OSF que contém `cyber_event_binned_data.csv`, com 366 semanas e três zeros na coluna `avg.report.length`.

1. Qual procedimento produziu os 363 valores usados no artigo? Os três zeros foram excluídos ou tratados de outra maneira?
2. Qual escala/conversão foi aplicada? Excluir zeros e dividir por 100 reproduz os quartis, mas gera média 5.381322314, que não coincide com a média publicada a quatro casas.
3. Qual definição e implementação foram utilizadas para os coeficientes γ3 e γ4? Os momentos padronizados calculados sobre essa hipótese de amostra não reproduzem 0.7249 e 3.6930. Essa divergência, isoladamente, não identifica sua causa.
4. É possível disponibilizar o vetor efetivamente usado e o trecho de código de preparação? As chamadas 44/45 de Cyber e heart failure parecem trocadas em relação à lista de referências; confirmar a correspondência das fontes.

A regra de Gjika que substitui zero por 0.01 é documentada no material de origem, mas não foi demonstrado que seja a regra usada por Abebe. A hipótese de exclusão e reescala é reconstrução atual, não um protocolo original recuperado.

## Kumar — inicialização efetiva do modelo

O notebook público vinculado pelo artigo DOI 10.1007/s10614-024-10797-w cria matrizes locais W/Win uniformes na célula 11, mas não as passa ao construtor `Reservoir`. As versões oficiais de ReservoirPy examinadas usam inicializadores normais para W e bipolares para Win, e nenhuma versão foi fixada no notebook.

1. Qual versão/commit de ReservoirPy e qual ambiente foram usados para produzir os resultados do artigo?
2. As matrizes locais eram efetivamente fornecidas ao modelo em outra versão do código, ou o experimento usou os inicializadores da biblioteca?
3. Há um arquivo de dependências e o notebook correspondente à rodada publicada, com a configuração efetiva preservada?

As respostas seriam documentação do que foi realizado; não exigem repetir o treinamento.
