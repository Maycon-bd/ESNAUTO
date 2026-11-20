# Reescrita da declaração de responsabilidade coletiva

Data: 2026-11-02. Base v011: `6ce846aec1d02f0ab1c6e575f822f082920331f8d7b6c444914bb45d0563ce4a`.
Cópia conferida: `reports/monografia/trabalho/declaracao_ia_reescrita_20261102.docx`, SHA256 `37feaaa77a3257c9e0b2dbc414dfbbaef55db0a14f24e50d8532aa44d0a3a398`.

O autor pediu redação diferente da declaração do colega e informou: “Modelos usados sempre foram do Claude Opus 5.5 e do Codex foi o Sol 5.6”. Esses nomes foram registrados como relato do autor, sem inferência de identificadores de API ou verificação independente por logs. A informação anterior “Somente Codex nos testes” foi mantida. Gemini 2.5 Flash, temperatura 0, continua associado à extração por script Python.

Foram reescritos os dois parágrafos de responsabilidade e as descrições das quatro atividades, ferramentas, finalidades e conferências humanas. A estrutura de quatro colunas, os compromissos de responsabilidade humana e respeito à integridade e aos direitos de terceiros, os nomes dos declarantes e os campos de data/assinatura foram preservados. A reescrita dos parágrafos institucionais é uma adaptação expressamente solicitada pelo autor: não é transcrição literal do formulário fornecido nem aprovação de sua aceitação institucional. A referência à Portaria foi mantida do formulário, sem auditoria jurídica nesta tarefa.

O parágrafo de 3.1 foi ajustado para refletir os modelos informados. O Anexo A e a declaração separada têm a mesma redação substantiva. A nova redação registra a conferência de artigos pelo autor e as correções textuais do orientador, sem atribuir ao orientador execução de testes ou validações técnicas não informadas.

## Conferências realizadas

Somente `word/document.xml` mudou na monografia. A comparação de todos os elementos de corpo identifica quatro elementos alterados: parágrafo de 3.1, dois parágrafos de abertura da declaração e sua tabela. Os outros elementos, incluindo as 14 tabelas científicas, permanecem idênticos em XML. Os resultados e as referências não foram alterados. Não foram repetidos treinamentos, buscas genéticas ou testes DM.

O Word repaginou a cópia em 81 páginas. Todos os 81 localizadores registrados (incluindo entradas das listas) preservaram título e paginação. As 81 páginas foram renderizadas; 79 imagens são idênticas à v011. As duas páginas diferentes, físicas 43 e 81 (impressas 42 e 80), foram inspecionadas, assim como a declaração separada de uma página. Não há cortes ou sobreposições, e os campos de assinatura cabem na página. O itálico do parágrafo metodológico ficou restrito à palavra script após correção na iteração de QA. As imagens foram processadas também pelo renderizador da skill de documentos, usando a renderização atual do Word como origem.

Evidências finais: `conferencia_final.json`, `inspecao_visual.json`, `alteracoes.json`; imagens em `word_final`, `render_final` e `render_decl`. PDFs por imagem são intermediários internos de QA, não uma edição PDF textual para entrega.

## Pendências e alcance

A identificação dos modelos não é mais desconhecida: foi preenchida conforme o relato do autor. Data e assinaturas continuam vazias para os declarantes. As demais limitações científicas e formalidades registradas na base permanecem; esta revisão pontual não é nova auditoria integral de fontes ou do Guia nem certificação de integridade/autoria por IA.

Fontes de apresentação: Anexo 14 fornecido em Downloads, modelo na página 4; Guia FASOFT em `output/skills-docx/GUIA-FASOFT-UniRV.pdf`, abertura e identificação de anexo nas páginas 65–66. O arquivo do colega é somente exemplo histórico; não fornece ferramentas ou validações para Maycon.
