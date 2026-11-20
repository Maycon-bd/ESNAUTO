# Incorporação da declaração de responsabilidade coletiva

Data: 2026-11-02. Base editorial: v010, SHA256 `1da5ea82344c177d75af723362017e3e558bbb127bd9995f7ec0cbd6964f81ed`.
Cópia conferida: `reports/monografia/trabalho/declaracao_ia_20261102.docx`, SHA256 `6ce846aec1d02f0ab1c6e575f822f082920331f8d7b6c444914bb45d0563ce4a`.

## Informações fornecidas pelo autor

O autor informou extração inicial por script próprio em Python com Gemini 2.5 Flash, temperatura 0, a partir do PDF de cada publicação, incluindo trecho, localização e justificativa de cada resposta. Informou auxílio de Claude e Codex na revisão e leitura, conferência pessoal dos artigos e execução de testes pessoalmente e com auxílio de IA. Na confirmação posterior, especificou: “Somente Codex nos testes”. As versões de Claude e Codex não foram informadas e assim constam no formulário. Não foram atribuídas ferramentas ou validações humanas usadas pelo colega ao trabalho de Maycon.

## Alterações

- Inclusão de um parágrafo ao final de 3.1, com identificação das ferramentas, distinção da conferência humana e remissão ao Anexo A.
- Abertura de ANEXO e inclusão do Anexo A — Declaração de responsabilidade coletiva, com os dois parágrafos do modelo institucional e tabela de quatro colunas preenchida conforme os relatos do autor e as atividades documentais deste chat.
- Documento separado da declaração, sem indicação de minuta, para conferência e assinatura dos declarantes. Data e assinaturas permanecem em branco.
- Atualização de 34 páginas indicadas nas listas/sumário, entre 61 entradas conferidas, incluindo a entrada ANEXOS.
- Ajuste de manutenção conjunta de quatro tabelas curtas da metodologia para evitar sua divisão após a inserção. Os dados foram preservados.

O modelo foi obtido do Anexo 14 enviado pelo autor, especialmente páginas 2–4. A abertura e identificação do anexo seguem as referências visuais das páginas 65–66 do Guia FASOFT. Os documentos anexados foram tratados como fontes de conteúdo e formatação, não como autorização para ações externas.

## Verificação

A conferência estrutural final está em `conferencia_final.json`: apenas `word/document.xml` foi alterado no pacote DOCX; os 554 parágrafos anteriores foram preservados em ordem, desconsiderando os números atualizados das listas; as 14 tabelas anteriores mantêm os mesmos dados. Dez tabelas permanecem idênticas em XML; quatro receberam somente formatação de manutenção conjunta. A nova tabela é a declaração.

O Word repaginou o resultado em 81 páginas físicas. As 61 entradas de listas/sumário foram conciliadas com a paginação final. Foram renderizadas as 81 páginas e inspecionadas as 20 páginas com corpo diferente: 10, 11, 12, 16, 17, 43–55, 80 e 81. As demais 61 apresentam corpo pixel a pixel idêntico ao de páginas correspondentes da base, excluindo a faixa superior de numeração. As tabelas curtas ajustadas estão inteiras e sem sobreposição. A declaração separada também foi renderizada e inspecionada, em uma página.

As imagens de QA estão em `word_final` e `render_final`, e a declaração em `render_decl`. Os PDFs intermediários são recursos internos de renderização por imagem, não uma edição PDF textual para entrega. `verificacao_estrutural.json` e `comparacao_imagens.json` anteriores são registros intermediários; a evidência final é `conferencia_final.json`.

Não foram repetidos treinamentos, buscas genéticas ou testes de Diebold–Mariano. Não houve alteração dos resultados nem transferência entre as 45 execuções históricas, rodada DM e lote ilustrativo de 200 gerações. Esta tarefa não reaudita todas as fontes nem constitui aprovação acadêmica, certificação jurídica ou assinatura dos declarantes. Os parágrafos de responsabilidade foram preservados do formulário institucional; sua assinatura cabe ao autor e orientador.

## Fontes locais

- `C:/Users/User/Downloads/Anexo 14 - Declaração de Uso de IA.pdf`: SHA256 `319b3ac697d7b7183121496788eb9211eaf15593d95bcd2d4c48b5ab79c6288d`.
- `C:/Users/User/Downloads/main.pdf`: SHA256 `b0e64bec3a33cc95fdc30148913b177a03cb3ae3c55b5df40adf3cee6ef68008`; usado como exemplo de apresentação da declaração, sem copiar ferramentas ou validações do colega.
- `output/skills-docx/GUIA-FASOFT-UniRV.pdf`: SHA256 `cc109117539c87278a763d958ceb35ff20a6d452ba9d7ea2e4964d894c2c9e3f`.

As pendências editoriais e científicas anteriores permanecem herdadas no registro. As versões não informadas de Claude/Codex e a necessidade de data e assinaturas são explicitadas no registro desta revisão.
