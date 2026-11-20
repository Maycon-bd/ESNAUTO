# Links internos do sumário

Base editorial v013, SHA256 `ff4f2978111152c4b1d2dea38b066f0b549b5fc34d13d49a674f559d0c59a47b`. Cópia conferida SHA256 `b93979a24f68abb962e0ae36871990b791d7916bcf8229b001f6d20e09e0f539`. Revisão em 2 de novembro de 2026.

O usuário relatou que clicar nas entradas não abria as páginas respectivas. A auditoria da v013 confirmou zero elementos hyperlink e zero campos de sumário: títulos e páginas eram texto estático. Foram adicionados 42 hyperlinks internos, um por entrada do sumário, e 42 marcadores exclusivos nos títulos de destino. Referências e abertura de anexos também estão vinculadas. Os títulos repetidos de análise inferencial foram associados às respectivas entradas pela ordem e título, com páginas conferidas no Word.

Não foi alterado o texto, a numeração, a aparência ou a posição das entradas. Não foram adicionados botões, barras de navegação ou links visíveis extras. As listas de figuras, quadros e tabelas não fazem parte desta alteração. O sumário continua com paginação estática: futuras mudanças de conteúdo exigem conferir seus números novamente.

Validação funcional: o Word abriu a cópia somente para leitura e executou Hyperlink.Follow em cada um dos 42 links. Para todos, o início da seleção coincidiu com o marcador esperado e a página impressa coincidiu com a entrada. Resultados em teste_links_word.json; destinos em links.json. O documento foi fechado sem salvar alterações feitas pelo Word.

Validação estrutural: somente word/document.xml foi alterado. A remoção dos novos links/marcadores recupera exatamente o XML original; texto, propriedades e 15 tabelas preservados. Os 81 localizadores anteriores mantêm a paginação. São 81 páginas renderizadas com corpo e cabeçalho pixel a pixel idênticos à v013. As páginas do sumário foram inspecionadas após renderização para confirmar aparência preservada. O renderizador da skill de documentos processou as imagens atuais do Word; os PDFs por imagem são QA interno, não entrega PDF textual.

Uso: no Word em modo de edição, normalmente Ctrl + clique segue o link. O comportamento de um visualizador de prévia pode ser diferente. A validação funcional foi realizada no Word local, sem certificar o comportamento de todos os aplicativos ou conversores de PDF. Não houve experimentos nem alteração de conteúdo científico, e permanecem as pendências da base.
