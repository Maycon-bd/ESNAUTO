# Incorporação de três respostas documentadas

Base: v009, SHA256 `793910fae2daaa2d5dbdcfa0cd76177c6c6a38c353d98d94ecaaaecf118c7b03`.
Cópia revisada: `reports/monografia/trabalho/busca_lacunas_20261101.docx`, SHA256 `1da5ea82344c177d75af723362017e3e558bbb127bd9995f7ec0cbd6964f81ed`.

## Resultado desta etapa

Foram substituídas três das41marcações da matriz. A busca integral solicitada pelo autor permanece em andamento:38células ainda não têm informação suficiente no escopo consultado. Esta entrega intermediária não afirma que todos os sinais foram preenchidos, que todas as fontes foram lidas integralmente nesta rodada ou que não existam alternativas documentais adicionais.

| Fonte e dimensão | Alteração | Sustentação |
|---|---|---|
| Jaeger2007/P1 | ? → D | Código oficial vinculado ao exemplo: Win uniforme em[-1,1); elementos não nulos deWgerados por sprand e deslocados por-0.5antes da normalização espectral. A matriz efetiva é transformada pelo reescalamento; não se confunde a lei inicial com a final. |
| Jaeger2007/P3 | ? → D | Código vinculado constrói canal de viés e canal de entrada e aplica transformações afins às sequências de entrada/alvo do gerador de frequência. Não é tratamento de preços financeiros. |
| Millea2014/P4 | ? → S | Os quatro NRMSE de Evolino na tabela3.1(0.00415,0.00804,0.110,0.166) coincidem com a tabela2de Schmidhuber et al.2007, p.772, que identifica PI-Evolino baseado emLSTM. É resultado importado, sem novo experimentoLSTM porMillea. Tabelas inspecionadas visualmente. |

O suplemento de Jaeger possui revisões posteriores ao artigo2007(inclui revisão2014e nota2015); essa condição está registrada. Sua inclusão documental foi explicitada na prosa. O arquivo foi apenas lido, sem execução. O trabalho original de Evolino e o suplemento verificam duas fontes existentes; não acrescentam itens à coleção de34documentos.

No repositório deKumar, matrizes locais uniformes são construídas mas não entregues ao objeto Reservoir que produz as previsões. Não foi atribuída essa lei ao modelo executado. A ausência de versão fixada da biblioteca mantém a insuficiência dessa célula.

## Conciliação do documento

Atualizados Quadro1, Tabela1, Figura1e o parágrafo de descrição de frequências. Incluídos o parágrafo que explicita o escopo complementar, o endereço do suplemento deJaeger e a referência original deEvolino. O gráfico foi gerado com fonteArial. As contagens foram recalculadas a partir das170células da v009, sem reutilizar totais históricos de versões antigas.

| Dimensão | Direta | Secundária | Insuficiente | Não aplicável |
|---|---:|---:|---:|---:|
| P1 |6|0|12|16|
| P2 |11|5|3|15|
| P3 |27|2|5|0|
| P4 |10|3|15|6|
| P5 |25|3|3|3|

## Verificações

O pacoteDOCX mudou somente em document.xml e na imagem daFigura1. Os14objetos de tabela permanecem, com alterações apenas nas duas tabelas bibliográficas; as outras12tabelas permanecem idênticas. As cinco outras imagens e o XML da introdução e dos capítulos3–6permanecem idênticos à base. As50referências anteriores foram preservadas(com endereço suplementar acrescido à entradaJaeger); há uma referência adicional, totalizando51. Não foram realizados experimentos, treinos, buscasGA ou testesDM.

O Word exportou78páginas. Os41títulos e19legendas foram medidos na paginação real. As60entradas do sumário e das listas foram conciliadas;48referências de página mudaram. As45páginas novas/alteradas foram inspecionadas visualmente, incluindo o fluxo posterior;33páginas têm corpo com pixels idênticos à exportação da v009, excluindo cabeçalho. Nenhum corte ou sobreposição foi observado. A Figura1e a notação matemática do parágrafo foram conferidas após preservar a formatação dos runs originais.

## Continuidade obrigatória

As38insuficiências permanecem listadas individualmente em `decisoes_41_em_consolidacao.json` e `relatorio_em_andamento.md`, com fonte, página e alcance. Falta concluir as alternativas pertinentes e distinguir informações recuperáveis de detalhes não especificados pelas publicações. A presença de um PDF não garante que ele contenha cada informação exigida pela matriz; não foram substituídas lacunas por suposições. A meta geral permanece ativa. Esta revisão não é aprovação acadêmica nem auditoria universal de todas as fontes.
