# Andamento da correção do parecer

Objetivo ativo: resolver F01–F25 e R01–R13. Não concluído; nenhuma promoção de versão.

## Estado mais recente: fidelidade e Quadro6

- Registro oficial continua v001. Conferir `Scripts/versao_monografia.py atual --json` em cada retomada. Base/hash do parecer preservados.
- Rascunho: reports/monografia/trabalho/revisao_parecer_integridade.docx. Estado/hash atual em estado_fidelidade_quadro6.json e lote1_alteracoes.json.
- Construtor cumulativo Scripts/revisar_parecer_integridade_lote1.py:110 parágrafos originais do corpo e196 de tabelas alterados; Figura1, largurasQuadro1 e remoção explícita da linha Cardoso2022a. NOVO:Quadro6 (6linhas/3colunas), legenda, fonte e entrada na lista. São14 tabelas OOXML. Nunca editar o Word e depois reconstruir sem conciliar o script.
- Inserções são aplicadas depois da validação da base: a remoção dos quatro nós novos devolve exatamente a árvore anterior por C14N. IDs de clones removidos; largura9071dxa, corpo11pt, legenda/fonte10pt, cabeçalho repetível e linhas sem altura fixa.
- Os identificadores P nos logs e CSV são DA BASE V001. A entrada de lista acrescenta um parágrafo apósP0058 e legenda/fonte acrescentam mais dois antes deP0504; índices da cópia corrente não podem ser usados diretamente como IDs de origem.

## O que avançou nesta etapa

1. F14: corrigidos P0197/P0204 (Xiao, ausência de valores faltantes e inconsistências MSE/RMSE), P0208 (Behera é survey, não prova geral de ganho), P0215 (WangF compara melhor ML por índice; não toda discrepância é LSTM nem elimina atrasos), P0217 (Zhang comprime estados, não comprova preservação geral de picos), P0254 (Ribeiro HAR-PSO-ESN, maioria dos casos) e P0255 (WangW: entradaUniforme/reservatórioadjacência e saída iterativa; sem superlativo bibliográfico). P0214/P0239 foram rechecados no contexto. Cortesi P0204 delimitado a volatilidade/S&P500; definição NMSE preservada.
2. F21 RESOLVIDO NO ESCOPO: Jaeger2001 consultado em versão pública do autor com errata26/01/2010 (47páginas). Introdução e treino/preparação, não leitura integral ou teoremas da errata. P0210 usa seu fundamento de treinamento de saída; P0531 distingue versão. Cardoso2025/tese foi usado substantivamente em P0267 para delimitar antecedente ARIMA-ESN/AG, estudos de caso e volatilidade; não transporta números para este protocolo.
3. R13: P0306/P0500 deixam de atribuir criação integral das rotinas; Quadro6 diferencia fundamentos anteriores, métodos próximos, integração LHS/cataclismo, organização/auditoria e procedência ainda incompleta. Foi inserido ao fim da conclusão, antes das referências, com chamadas no método e na conclusão.
4. Siglas/itálicos dos trechos novos: mantidas definições de DL, MSE, NMSE, CS, HONNs e PSO; estrangeirismos receberam itálico real. Títulos bibliográficos de Araújo, Jaeger2001 e Soltani têm destaque apropriado à referência, sem tratar apenas a palavra fitness como estrangeirismo no título.
5. Evidências em evidencia_fidelidade_atribuicoes.json: oito PDFs locais conferidos por hash contra o manifesto original; registro do acesso primário Jaeger e localizadores. Não se declara leitura integral de todos os PDFs.

## PDF e inspeção desta aplicação

Último: revisao_fidelidade_quadro6.pdf,77páginas, hash em estado_fidelidade_quadro6.json. Outros PDFs da etapa (revisao_atribuicoes.pdf, revisao_fidelidade_atribuicoes.pdf e _atual.pdf) são intermediários. Imagens em qa_fidelidade_quadro6/. Foram examinadas físicas11/12/22–26/72/73/75/76; reaplicações tipográficas das referências73/75/76 inspecionadas novamente. Quadro6 inteiro na física72/impressa71. Entrada da lista corrigida após QA: título, tabulação e página são construídos em runs separados; não usar diff de texto achatado que reposiciona algarismos através do tab. RC no P0210 está em itálico na reaplicação.

Não confundir PageMap Word com página física PDF. Inspeção integral ainda pendente; paginação cresceu e sumário/listas antigos precisam atualização final. Exportador sem -AtualizarListas não salva o Word, mas fixa recuos em memória. Na etapa final planejar atualização/salvamento nativo e sua conciliação com hash/construtor; não reconstruir depois apagando atualizações.

## Próximas ações necessárias

1. Revalidar os38 itens do CSV contra escopo do parecer e fontes/rascunho atuais; encerrar individualmente por evidência os que já foram resolvidos. F14 tem correções substantivas, ainda falta fechamento global das atribuições comparativas.
2. Concluir metadados remanescentes F20 (Deng/Kumar e correspondências) e confronto autor–ano/referências. Não confundir ano do evento com ano bibliográfico, nem prova/preprint com edição final não lida.
3. Refazer comparação textual local de integridade para O RASCUNHO ATUAL, com relatório e hashes separados. O script/auditoria anterior pode estar preso ao Word original; inspecionar antes de executar para não sobrescrever evidência histórica. Não certificar ausência universal de plágio.
4. Auditar siglas/itálicos/quadros/tabelas/guia no conjunto; atualizar listas/campos, renderizar e inspecionar todas as páginas finais. Resumo ainda contém a expressão gramatical antiga “o menor raiz” (pode corrigir sem mudar números). Não regredir destaques bibliográficos ao normalizar estrangeirismos.
5. Pendências documentais para apresentar ao autor APÓS avançar o restante: cadeia original de ajuste; exportações primárias Onda5/IDs0053–0067 ausentes no CSV atual; original RBras2022a para atribuição do Quadro3/P0328; planilhas bibliográficas ausentes; autoria/origem de rotinas legadas. Não repetir GA, treino ou DM nem restaurar arquivos históricos para preencher lacunas.
6. Registrar revisão pelo controle somente após conferência final, com estado em_revisao e pendências precisas. A ausência de um original não é prova de resultado errado ou de plágio. Não marcar objetivo completo ainda.

Históricos anteriores em andamento_historico_ate_metadados_comparadores.md e andamento_historico_ate_matriz170.md. Etapas da matriz, procedência, H4/H5, título e comparação quantitativa permanecem aplicadas; consultar estados/evidências correspondentes sem reutilizar hashes antigos como se fossem do rascunho atual.
