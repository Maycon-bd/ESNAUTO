# Links das listas de figuras, quadros e tabelas

Data: 2 de novembro de 2026. Base v014, SHA256 `b93979a24f68abb962e0ae36871990b791d7916bcf8229b001f6d20e09e0f539`. Cópia conferida: `0e6ed169859d1aca3538c291f870053444fec7fb4d5ec58098500de25b869256`.

Foram adicionados 19 hyperlinks internos nas listas: seis figuras, seis quadros e sete tabelas. Cada entrada completa aponta para um novo marcador na legenda correspondente. Os 42 links do sumário foram preservados. As referências visíveis, o conteúdo científico, a declaração e os números de página não foram alterados.

O Word abriu a cópia somente para leitura e executou Hyperlink.Follow nos 61 links: todos chegaram ao início do marcador correto e à página impressa indicada. O teste inclui os 19 links novos e os 42 anteriores. Destinos em links.json e resultados funcionais em teste_links_word.json. O Word foi fechado sem salvar.

A alteração está restrita a word/document.xml. Remover exclusivamente os 19 hyperlinks e marcadores novos recupera exatamente o XML da base. O texto e as 15 tabelas foram preservados; os 81 localizadores mantiveram a mesma paginação. Foram renderizadas 81 páginas, todas pixel a pixel idênticas à v014. As três páginas das listas (físicas 10, 11 e 12) foram inspecionadas após renderização; aparência preservada e sem defeito introduzido. O renderizador da skill de documentos processou as imagens atuais do Word. PDFs por imagem são apenas QA interno.

Conferência estrutural em estrutura.json e conferencia_final.json. No Word em edição, normalmente Ctrl + clique segue o link. A validação funcional é do Word local, sem certificação do comportamento de outros visualizadores ou conversores de PDF. A paginação das listas continua estática e deve ser conferida após futuras alterações editoriais. Não foram executados novos experimentos, treinamentos, buscas genéticas ou testes DM. Pendências científicas e institucionais herdadas da base permanecem.
