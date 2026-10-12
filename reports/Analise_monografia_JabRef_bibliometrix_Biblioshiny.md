# Análise da monografia e proposta de uso de ferramentas bibliográficas

Documento analisado: `MayconGarciaSilva_monografia_consolidada (1).docx`, fornecido pelo autor. Análise realizada em 12 de outubro de 2026. O arquivo original não foi alterado.

A inclusão de JabRef, bibliometrix e Biblioshiny faz sentido na organização das referências e na revisão da literatura. A prioridade é conferir a composição do portfólio antes de gerar gráficos. Essas ferramentas trabalham com publicações científicas; as previsões financeiras continuam sendo produzidas pelo ESNAUTO.

## O que significa cada nome

**JabRef** é um gerenciador de referências. Ajuda a organizar autores, títulos, anos, DOI, PDFs e grupos temáticos, trabalhando com bibliotecas BibTeX/BibLaTeX em arquivos `.bib`. O formato armazena informações bibliográficas de maneira estruturada. No seu trabalho, serviria para manter uma biblioteca conferida das fontes utilizadas. [Site oficial](https://www.jabref.org/).

**bibliometrix** é um pacote da linguagem R para análise bibliométrica: análise quantitativa de um conjunto de publicações. Permite estudar distribuição de publicações por ano, fontes, autores, citações e relações entre termos ou referências. No seu trabalho, serviria para descrever e explorar a literatura sobre ESN e previsão financeira. [Descrição oficial](https://www.bibliometrix.org/software/).

**Biblioshiny** é a interface gráfica do bibliometrix, utilizada pelo navegador. Ela permite fazer análises por menus e botões. Bibliometrix e Biblioshiny são, portanto, o pacote e sua interface. A grafia correta é Biblioshiny. [Descrição oficial](https://www.bibliometrix.org/biblioshiny/).

## O que a monografia já oferece

A estrutura distingue fundamentação teórica, métodos, resultados e discussão. O texto explicita limitações relevantes: o efeito do Fator de Ajuste não foi isolado experimentalmente; o custo da busca genética é separado do ajuste analítico; a inferência de Diebold–Mariano pertence a uma execução complementar; a assimetria de orçamento de otimização entre ESN e os baselines é reconhecida. Essa delimitação ajuda a manter conclusões proporcionais à evidência apresentada.

Para a integração bibliográfica, existem dois pontos de entrada diretos: a seção 2.8, **Síntese do portfólio bibliográfico**, e a seção 3.8.3, **Protocolo de revisão sistemática da literatura**. O texto declara 34 estudos no portfólio e buscas em Scopus e Springer Nature Link em 23 de março de 2026, com 41 e 59 registros, respectivamente. A lista final de referências contém 44 entradas; ela inclui fundamentos e fontes metodológicas, além dos estudos do portfólio.

A contagem dos símbolos da Tabela 2 confirma 34 linhas e as coberturas declaradas: P1 = 16, P2 = 16, P3 = 31, P4 = 21 e P5 = 30. Também confirma oito linhas marcadas nas cinco dimensões. Isso verifica a consistência aritmética das tabelas, mas não a adequação das classificações ao conteúdo de cada fonte.

## Pontos a corrigir antes da bibliometria

1. **Separar o portfólio formal das referências de apoio.** O protocolo informa recorte 2021–2026, mas a Tabela 2 inclui Ecer (2020), Jaeger (2007), Millea (2014), Nelson (1991) e Timbó (2016). Essas fontes podem permanecer na fundamentação; sua presença no denominador do portfólio precisa ser explicada ou revista.

2. **Explicitar as exceções e buscas complementares.** CI5 exige aplicação financeira e CE3 exclui aplicações não financeiras, mas a referência de Deng et al. (2022) trata de degradação de células a combustível. A tabela também inclui Millea (2014), identificado nas referências como dissertação, embora o portfólio seja descrito como composto por artigos. É necessário verificar quais fontes entraram pela busca formal e quais entraram como apoio técnico.

3. **Rever a abrangência da busca.** A string obriga a presença de `Survey`, `Review` ou `State of the art`. Isso pode excluir estudos experimentais relevantes que não utilizem esses termos nos campos pesquisados. A revisão pode preservar uma busca específica para revisões e acrescentar uma busca identificada separadamente para estudos primários. Essa é uma proposta metodológica; não foi executada uma nova busca nesta análise.

4. **Registrar o caminho dos registros até a amostra final.** Os 41 + 59 resultados são registros antes da deduplicação, não necessariamente 100 estudos únicos. O trecho metodológico não apresenta a contagem por etapa de exclusão. Para obter um fluxo auditável, registrar duplicatas, exclusões por título/resumo, leitura integral, motivos e número final. O fluxo deve refletir os registros reais.

5. **Conferir identificação e ano das fontes.** A tabela utiliza Duttilo et al. (2023a/2023b), enquanto a lista de referências apresenta uma tese de Duttilo de 2023 e um trabalho de Duttilo e Gattone de 2022. A Tabela 1 menciona Chen e Cortesi com ano 2024 em P3, enquanto a Tabela 2 e as referências os apresentam em 2025. Esses vínculos precisam ser reconciliados por título/DOI antes da importação. A referência de Soltani também precisa de conferência dos metadados disponíveis, pois está menos completa que várias outras entradas.

Esses achados são inconsistências internas do documento. Esta análise não realizou uma auditoria externa de todas as referências nem confirmou cada afirmação dos artigos citados.

## Como acrescentar as ferramentas ao trabalho

O Methodi Ordinatio já utilizado pode continuar como procedimento de seleção/priorização. O JabRef pode organizar as fontes selecionadas, e o bibliometrix/Biblioshiny pode produzir a caracterização bibliométrica complementar. Descrever separadamente a função de cada componente evita confundir seleção de artigos, organização das referências e análise dos registros.

O fluxo proposto é:

1. Conferir uma lista identificada por título e DOI, com uma coluna indicando portfólio formal, busca complementar ou referência de apoio.
2. Recuperar os arquivos originais exportados pelas bases, preservando autores, ano, fonte, DOI, resumo, palavras-chave e referências citadas quando disponíveis. Registrar a data da exportação.
3. Manter os arquivos brutos preservados. Criar uma biblioteca de trabalho no JabRef para conferir e organizar as fontes.
4. Importar os registros bibliográficos no bibliometrix ou Biblioshiny, indicando a origem e o formato efetivos. Não assumir que qualquer arquivo `.bib` possui os metadados necessários para todas as análises.
5. Gerar os resultados e relacioná-los às perguntas da revisão. Preservar configurações, filtros, arquivos de entrada e saídas.
6. Inserir o procedimento na seção 3.8.3 e os resultados descritivos na seção 2.8, com interpretações delimitadas ao conjunto analisado.

O Scopus possui formatos de exportação documentados pelo bibliometrix. Os registros de Springer Nature Link exigem verificação de compatibilidade e cobertura dos campos; não se deve atribuir a eles origem Scopus ou Web of Science. Resumo e referências citadas podem estar ausentes em arquivos simplificados de gerenciadores. [Documentação de importação](https://www.bibliometrix.org/vignettes/Data-Importing-and-Converting.html).

## Análises úteis para esta monografia

Começar por publicações por ano, periódicos/fontes mais presentes e palavras-chave recorrentes. Uma rede de coocorrência de palavras-chave pode ajudar a visualizar relações entre ESN, reservoir computing, otimização e previsão financeira, desde que a cobertura dos metadados permita isso. Para um conjunto pequeno e selecionado, interpretar redes e mapas como descrição daquele conjunto; não como representação completa do campo.

Os 34 estudos selecionados e um conjunto amplo de registros de busca respondem a perguntas diferentes. A bibliometria dos selecionados descreve o portfólio; uma análise da literatura do campo exige um corpus definido com esse objetivo. Caso os dois sejam analisados, apresentar resultados e critérios separadamente.

As perguntas P1–P5 continuam exigindo leitura e extração do conteúdo dos artigos. Uma rede de termos não demonstra, sozinha, que um estudo documentou a distribuição de Win/W ou aplicou Fator de Ajuste. Preservar a matriz de extração como evidência dessas classificações.

## Uso com Word e com o software

Como a monografia está em Word, o JabRef pode exportar fontes em XML para importação no gerenciador de fontes do Word. Essa importação não converte automaticamente todas as citações digitadas em campos nem garante adequação ao padrão exigido pela universidade. [Documentação oficial para Word](https://docs.jabref.org/cite/export-to-microsoft-word).

Uma primeira etapa suficiente é usar essas ferramentas no fluxo da pesquisa e inserir os resultados na monografia. Caso seja desejada integração ao ESNAUTO, uma evolução possível é um módulo independente de literatura com biblioteca `.bib`, importação de metadados e consulta às análises. A existência de duas interfaces feitas com Shiny não implica integração automática entre elas. Nenhuma alteração no ESNAUTO ou instalação de pacotes foi realizada nesta análise.

## Materiais necessários para executar a proposta

As exportações bibliográficas originais e as planilhas `methodi_ordinatio.xlsx` e `extracao_completa.xlsx`, mencionadas pela monografia, permitem reconstruir seleção e extração. Esses materiais não foram localizados no projeto pela busca de nomes realizada nesta análise. O DOCX permite uma avaliação inicial, mas não contém todos os metadados necessários para reconstruir citações, redes e triagens com segurança.

Para abrir Biblioshiny em um ambiente R preparado:

```r
install.packages("bibliometrix") # instalação inicial
bibliometrix::biblioshiny()
```

A instalação não foi executada. [Instruções oficiais de instalação](https://www.bibliometrix.org/download/).

A monografia fornecida ainda delimita a validação experimental à PETR4. A inclusão funcional de VALE3 no software pode ser registrada como evolução do artefato; conclusões sobre o desempenho em VALE3 dependem das baterias experimentais correspondentes.
