# Incorporação dos esclarecimentos do autor

Base editorial: **v003**, SHA256 `eb31ed353550c8d13e388a7f51995917c1d20f52acdd946aa15a8908e0381785`, resolvida pelo registro vigente antes da edição. Os quatro esclarecimentos do autor foram preservados literalmente em `declaracoes_autor.json`, com identificação das anotações e limites de interpretação.

## Seleção dos artigos — anotação 1, F18/R01

O autor confirmou que realizou buscas externas à string inicial para complementar a fundamentação e que os registros nas planilhas não acompanharam adequadamente toda a seleção. O processo passou a ser descrito como revisão de literatura com buscas complementares, sem sustentar que os 34 documentos tenham resultado exclusivamente da consulta inicial ou de um ranking InOrdinatio concluído.

As planilhas originais e suas contagens foram preservadas. As 48 decisões vazias não foram preenchidas por inferência. O Methodi permanece citado como referência considerada na organização inicial, sem atribuir ao método a seleção final ou um ranking validado. A fonte original recuperada não é confundida com uma aplicação completa do procedimento.

**Resultado:** esclarecido o procedimento efetivamente relatado pelo autor e corrigida sua descrição. A trilha histórica continua parcial; não há necessidade de inventar um fluxo sistemático para justificar a coleção utilizada. As conferências de fidelidade das citações e da matriz permanecem independentes dessa caracterização.

## Fornecimento da série ajustada — anotação 2, R03

O autor confirmou que recebeu os dados já ajustados do orientador. Resumo, abstract, metodologia e conclusão foram alinhados a essa procedência. O texto atribui o fornecimento da série ao Prof. Dr. Fabian Corrêa Cardoso e situa o início da modelagem nos arquivos recebidos.

**Resultado:** a dúvida sobre de quem o autor recebeu a série foi esclarecida. A declaração não é ampliada para afirmar que o orientador executou pessoalmente cada transformação do BovDB. A cadeia técnica completa dos eventos e do ajuste continua não reconstruída, como limite de reprodução do processamento anterior ao recebimento. Não se atribui a aplicação original do fator ao autor nem um ganho causal não testado ao ajuste.

## Resultados por onda — anotação 3, R08

O relatório local `docs/09_onda_5_ajustes_empiricos_easyfit.md` contém, de fato, as **15 linhas GA_RUN_0053–GA_RUN_0067**, incluindo configurações, métricas e tempos compilados. Para facilitar sua localização, essas linhas foram transcritas, sem recalcular ou completar valores, em `onda5_resultados_compilados_localizados.csv`. Esse CSV derivado **não é uma exportação original de execução**.

As primeiras quatro ondas também possuem relatório local: `docs/08_comparativo_quatro_ondas_estocasticas.md`, com 30 linhas de execuções tabeladas. A localização foi registrada em `localizacao_ondas_1_4.json`. Isso confirma onde estão os resultados compilados das cinco ondas, sem equiparar os relatórios às saídas primárias de cada execução.

A busca adicional examinou **616 arquivos ou membros textuais e 45 ZIPs**, contando cópias e objetos históricos Git. Procurou os IDs, as distribuições empíricas e valores característicos de MAE/RMSE, incluindo situações em que o arquivo não contivesse o ID. As únicas ocorrências nos arquivos de resultados examinados foram índices de menções históricas (`ocorrencias_historicas.csv`), que não constituem as saídas das execuções. Arquivos RDS/RData foram inventariados por nome e contexto, sem desserialização; não foram executados códigos científicos.

**Resultado:** confirmada a existência dos resultados compilados de cada execução da Onda 5 no projeto. Ainda não foi estabelecida a ligação de cada linha com sua saída original de execução, matrizes e previsões correspondentes. A ressalva é sobre o nível de comprovação, não sobre inexistência de resultados ou conclusão de que sejam falsos. Essa expectativa do autor não foi convertida em uma validação primária que a busca não produziu.

## Base em R e contribuição do autor — anotação 4, R13

O autor confirmou que recebeu códigos em R do orientador, adaptou-os ao contexto da pesquisa e construiu a interface. A revisão atribui expressamente a base recebida ao orientador e caracteriza a contribuição do autor como adaptação e desenvolvimento da interface. A atribuição foi incorporada ao resumo, abstract, metodologia, discussão, conclusão e Quadro 6.

**Resultado:** esclarecida a divisão de contribuição no nível declarado. Não se apresenta toda a implementação matemática como criação original do autor. A declaração não foi usada para atribuir individualmente cada arquivo, alteração, técnica ou rotina de terceiros além do que foi informado.

## Preservação e alcance

Foram alterados **12 parágrafos e duas células do Quadro 6**, registrados com antes/depois em `alteracoes_editoriais.json`. Os tokens numéricos dos resumos foram preservados. Os dados, scripts experimentais e resultados não foram restaurados, regenerados ou modificados. Não houve treino, GA, DM ou transformação de preços.

A revisão incorpora esclarecimentos diretos do pesquisador, que são identificados como tais, e não como evidência independente datada da execução original. Os snapshots e relatórios anteriores continuam preservados. O objetivo de auditoria integral de citações/plágio não é declarado concluído por essas alterações de procedência e redação.

## Verificação para entrega

A revisão manteve **76 páginas** e passou pelas **45 verificações estruturais**. As **60 entradas de listas/sumário** correspondem ao mapa do Word. Permanecem **50 referências e 151 ocorrências autor–ano reconhecidas**, sem referências órfãs nos padrões examinados. Os resumos têm 331 palavras em português e 273 em inglês e preservam os números anteriores.

Na comparação sem máscaras, **62 páginas apresentam pixels idênticos à v003**. As outras **14 páginas foram examinadas novamente em três folhas de contato**; páginas 8, 50 e 71 foram também abertas integralmente para conferir resumo, seleção bibliográfica e Quadro 6. Não foram identificados cortes ou sobreposição nos elementos examinados. `inspecao_visual.json` registra o alcance da conferência, sem convertê-la em aprovação acadêmica.

A matriz dos 38 achados foi atualizada em `resolucao_achados_atualizada.csv`, preservando os diagnósticos anteriores como históricos. O fornecimento da série e a divisão geral de contribuição deixaram de ser perguntas sem resposta. Permanecem como limites documentais a trilha histórica parcial das buscas e a falta de ligação integral dos resultados da Onda 5 com suas saídas primárias; a transformação original anterior ao recebimento dos dados não foi reconstituída.
