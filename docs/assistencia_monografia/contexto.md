# Contexto da assistência à monografia ESNAUTO

Configuração inicial em 23 de outubro de 2026, a partir dos arquivos locais. Esta
assistência apoia a revisão e conclusão do trabalho existente. A base editorial
selecionada é a revisão PETR4 preparada para o orientador. Novas decisões do autor
e do orientador devem ser registradas abaixo e prevalecem sobre esta configuração.

## Identidade e escopo

- Autor: Maycon Garcia Silva.
- Instituição e curso: Universidade de Rio Verde, Engenharia de Software.
- Orientador: Prof. Dr. Fabian Corrêa Cardoso.
- Título atual: Aplicação de fator de correção para previsão de preços de ações na
  bolsa de valores com rede neural de estados de eco.
- Objeto: previsão de um passo à frente do preço ajustado da PETR4, 2000–2020.
- Método: ESN com leitura Ridge; distribuições em Win e W; GA binário de 55 bits,
  inicialização LHS e mecanismo cataclísmico inspirado no CHC; comparação com ESN
  Normal × Normal, GRU e LSTM.
- Contribuição de software: infraestrutura ESNAUTO em R/Python e aplicação Shiny.
- Estágio: manuscrito completo; revisão de coerência e rastreabilidade em curso.

## Hierarquia por finalidade

O arquivo `fontes.json` é o catálogo de caminhos. A prioridade depende da pergunta:

1. **Redação vigente:** Word PETR4 revisado para o orientador. Não juntar trechos de
   versões anteriores sem verificar se houve mudança de escopo ou de hipóteses.
2. **Resultados e protocolo:** previsões, métricas, manifesto e código preservados
   da execução em questão. Um relatório ou o Word não sobrepõe esses registros.
3. **Literatura:** versão efetivamente consultada do PDF; metadados e decisões de
   reconstrução ajudam a identificar a versão, sem comprovar apoio a uma afirmação.
4. **Formatação:** manual institucional vigente, quando localizado, e decisões
   explícitas do orientador. O Word atual é referência de apresentação, não prova
   de conformidade com todas as normas da UniRV.
5. **Contextualização:** README, dossiê de artigo e documentação técnica. Podem
   estar desatualizados em relação ao manuscrito e aos resultados mais recentes.

## Blocos de evidência

| ID | Objeto | Uso e limite |
|---|---|---|
| PETR4-HIST | 45 execuções, cinco ondas | Comparações descritivas históricas; preservação incompleta de vetores e matrizes |
| PETR4-DM | Rodada controlada, seed 20260926 | Novos pesos; 1.298 datas comuns; quatro contrastes; não é reprodução dos vetores históricos |
| PETR4-ILUST | Lote legado de 200 gerações | Figuras 5 e 6; execução GED × Uniforme selecionada por fitness; fora das 45 execuções |
| LIT-34 | Coleção bibliográfica reconstruída | 34 documentos, 24 com palavras-chave; não é exportação original Scopus |
| VALE3-EXT | 12 execuções ESN | Material de continuidade; fora dos resultados principais da base PETR4 atual |

Não combinar numeradores e denominadores entre esses blocos. Nos resultados DM,
1.299 previsões por modelo e 1.298 datas da janela comparativa são populações
distintas e devem ser identificadas. O lote ilustrativo também avalia 1.298 alvos,
mas seus números não pertencem à rodada DM.

## Limites para redação

- H1: separar comparação histórica de inferência na rodada controlada. Ausência de
  significância não demonstra equivalência ou não inferioridade.
- H2: distinguir tempo de ajuste da configuração escolhida e custo da busca GA.
- H3: ganhos observados entre distribuições são pontuais; não declarar efeito
  causal da distribuição isolada, pois os demais hiperparâmetros também variam.
- H4: implementação de LHS e cataclismo não demonstra ganho causal nem diversidade
  superior sem medidas e controles correspondentes. Não chamar de CHC completo.
- H5: baixa dispersão observada na Onda 5 não implica superioridade universal.
- Fator de Ajuste: etapa fixa de pré-processamento; não houve ablação que isole seu
  ganho de acurácia. O carregamento de dados já ajustados não comprova autoria da
  aplicação do fator nem sua cadeia de processamento.
- R² alto em preços em nível não demonstra utilidade econômica. Não acrescentar
  alegações de lucro, negociação ou generalização não avaliadas.
- A extensão VALE3 registra ausência de ganho de MAE sobre persistência nas 12
  execuções. Preservar isso em eventual artigo futuro.

## Situação documental pendente

Não foi localizado manual institucional separado nem as planilhas
`methodi_ordinatio.xlsx` e `extracao_completa.xlsx` mencionadas no Word. Isso é uma
lacuna do acervo examinado, não prova de que os materiais nunca existiram.
O Word vigente não contém parte OOXML `word/comments.xml`; o nome do arquivo não
comprova, sozinho, aprovação ou autoria das alterações pelo orientador.

## Decisões registradas

| Data | Decisão | Origem |
|---|---|---|
| 2026-10-23 | Configurar assistência local e executar primeira auditoria, sem alterar os Word | Pedido do usuário nesta conversa |
| 2026-10-23 | Adotar revisão PETR4 como base inicial; manter versões anteriores | Proposta apresentada e autorizada pelo usuário |

Este registro não atesta aprovação do manuscrito pela banca ou pelo orientador.
