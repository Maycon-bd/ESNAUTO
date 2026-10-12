# Análise bibliométrica reconstruída dos documentos citados

A base foi reconstruída dos 34 PDFs disponíveis na pasta `Artigos citados`, com apoio das referências da monografia e de consultas Crossref. Os documentos antigos foram preservados como parte do conjunto de fontes utilizadas. A importação foi executada no bibliometrix 5.5.0 e o arquivo `colecao_biblioshiny.RData` foi validado com o carregador usado pelo Biblioshiny.

Não foi alterado o documento Word original. Os textos abaixo são propostas para inserir a análise complementar, descrevendo o procedimento realmente executado.

## Arquivos para uso

- `graficos/figura_rede_palavras_chave.png`: mapa de coocorrência; versão vetorial `.svg` com o mesmo nome.
- `graficos/figura_frequencia_palavras_chave.png`: frequência documental dos termos recorrentes; versão `.svg` disponível.
- `graficos/figura_anos_reconstruidos.png`: distribuição temporal com os anos das versões adotadas; versão `.svg` disponível.
- `colecao_biblioshiny.RData`: coleção processada, contendo o objeto `M` de classe `bibliometrixDB`, para carregar no Biblioshiny.
- `artigos_reconstruidos.bib`: arquivo de intercâmbio bibliográfico. Para análises na interface, preferir a coleção `.RData`, pois já corrige o rótulo de origem e representa contagens de citações indisponíveis como ausentes.
- `base_reconstruida.json`: metadados, palavras-chave originais e normalizadas, referências originais, notas por documento, fontes e hashes.
- `validacao_bibliometrix.json`: resultados da importação e da conferência independente da matriz.

Os PNGs foram gerados a 300 dpi. SVGs preservam a qualidade ao redimensionar.

## Cobertura e validação

| Verificação | Resultado |
|---|---:|
| Documentos na base | 34 |
| Documentos com palavras-chave localizadas e transcritas | 24 |
| Cobertura das palavras-chave | 70,6% |
| Documentos sem palavras-chave localizadas nas páginas iniciais | 10 |
| Termos distintos depois da normalização registrada | 92 |
| Termos presentes em pelo menos dois documentos | 14 |
| Ligações entre esses termos | 33 |

Título e primeiro autor foram reconciliados com resultados Crossref em 27 registros. Isso inclui dois registros relacionados a versões distintas de preprints; seus DOIs externos não foram atribuídos aos PDFs locais. Os demais sete conservaram os metadados apoiados na referência e na conferência local, com esse status registrado. A reconciliação bibliográfica não representa validação do conteúdo científico dos estudos.

As palavras-chave foram transcritas dos trechos explícitos de Keywords/Index Terms dos PDFs, sem substituir esse campo por assuntos de Crossref, termos inferidos do resumo ou palavras da própria monografia. A ausência de palavras-chave nas páginas iniciais inspecionadas não prova sua ausência em toda versão possível do documento.

O dicionário de normalização conserva as formas originais e unifica variantes registradas, como ESN/echo state networks/echo state network. As frequências são binárias por documento: repetir o mesmo termo no documento não aumenta sua contagem. Os termos individuais são preservados em inglês conforme os artigos; a introdução da figura pode explicar sua tradução.

## Método sugerido para a seção 3.8.3

> Como análise complementar do conjunto de fontes utilizadas, foi reconstruída uma base bibliográfica a partir de 34 documentos disponíveis no acervo local. Foram utilizadas as referências da monografia e as páginas iniciais dos PDFs para identificar título, autores, ano, tipo documental e versão. Quando disponíveis, os registros foram confrontados com metadados de Crossref, preservando-se as diferenças entre versões. As fontes anteriores ao recorte temporal da busca foram mantidas e identificadas como referências complementares, utilizadas na fundamentação dos conceitos ou na contextualização do trabalho. A coleção reconstruída não foi tratada como reprodução da exportação original de Scopus.

> Foram localizadas palavras-chave declaradas pelos autores em 24 documentos, correspondentes a 70,6% do conjunto. As listas foram transcritas e normalizadas por um dicionário de variantes, mantendo-se uma contagem binária de presença por documento. A base foi importada no bibliometrix, versão 5.5.0, e a matriz de coocorrência foi obtida com a função biblioNetwork para Author Keywords. Na representação da rede foram mantidos termos presentes em pelo menos dois documentos. A matriz foi conferida por contagem independente das palavras-chave por documento. Para a disposição visual foram usados o algoritmo Fruchterman–Reingold e a semente 20261012; as comunidades foram identificadas pelo algoritmo Walktrap. A análise é descritiva do conjunto reconstruído e não representa toda a literatura da área.

Os parágrafos devem ser integrados ao texto existente sem dizer que a reconstrução foi realizada na data da busca original. A exceção das referências fundamentais precisa ser descrita conforme a trajetória real da pesquisa; a bibliometria não corrige retroativamente os critérios de seleção nem transforma todas as referências em estudos elegíveis da busca formal.

## Figura da frequência de palavras-chave

Legenda proposta: **Figura X — Frequência documental das palavras-chave recorrentes no conjunto reconstruído.**

Fonte: Elaborado pelo autor a partir dos PDFs citados, com processamento no bibliometrix (2026).

Nota: Análise de 24 documentos com palavras-chave localizadas. São exibidos os termos presentes em pelo menos dois documentos. Cada documento pode declarar diversos termos; as frequências não somam o total de documentos.

Texto proposto:

> Entre os documentos com palavras-chave disponíveis, echo state network foi o termo mais frequente, identificado em nove estudos (37,5%), seguido de reservoir computing, presente em cinco (20,8%). Deep learning, stock price forecasting e time series apareceram em três estudos cada (12,5%). Essa distribuição caracteriza a ênfase temática das palavras-chave declaradas no subconjunto analisado. A frequência de um termo não equivale ao número total de estudos que discutem o conceito no corpo do texto.

## Figura da rede de coocorrência

Legenda proposta: **Figura Y — Rede de coocorrência de palavras-chave declaradas pelos autores.**

Fonte: Elaborado pelo autor com bibliometrix 5.5.0 a partir da base reconstruída (2026).

Nota: A matriz utiliza 24 documentos. O limiar de frequência de dois documentos resulta em 14 nós e 33 ligações. A área dos nós representa frequência documental e a espessura das ligações representa o número de documentos que declaram ambos os termos. As cores correspondem às comunidades calculadas por Walktrap, e não a categorias previamente atribuídas pelo autor.

Texto proposto:

> A rede mostra conexões entre echo state network, reservoir computing, deep learning e termos associados à previsão de preços e às séries temporais. LSTM e GRU aparecem conectados no conjunto de palavras-chave recorrentes, enquanto optimization, artificial intelligence e machine learning também integram o mapa. A representação ajuda a visualizar a articulação temática entre arquiteturas e tarefas nos documentos analisados, mas não demonstra, por si só, uma lacuna de pesquisa. As afirmações sobre distribuição de inicialização, pré-processamento e otimização permanecem apoiadas na extração de conteúdo organizada pelas perguntas P1–P5.

Posição sugerida: seção 2.8, após a síntese P1–P5. A figura de frequência facilita a leitura da rede; se o espaço for limitado, priorizar a rede acompanhada de uma descrição das frequências principais.

## Figura temporal e diferenças de versão

Legenda proposta: **Figura Z — Distribuição temporal dos documentos segundo as versões bibliográficas adotadas na reconstrução.**

Fonte: Elaborado pelo autor a partir das referências e versões locais dos PDFs (2026).

As cinco fontes anteriores a 2021 foram mantidas e indicadas em cinza. A representação utiliza categorias de ano; intervalos sem documentos não aparecem como barras. As contagens diferem da figura anteriormente extraída da Tabela 2, por causa das seguintes conferências:

| Documento | Informação anterior | Versão disponível e decisão na base |
|---|---|---|
| Chen | Referência de 2025 | PDF arXiv:2512.06630v2 com rodapé de 13 de fevereiro de 2026; adotado 2026. O DOI de exemplo do template IEEE foi rejeitado. |
| Cortesi | Referência de 2025 | PDF arXiv:2603.02620v1 com rodapé de 3 de março de 2026; adotado 2026. |
| Soltani | Referência de publicação de 2023 | PDF Research Square v1, DOI 10.21203/rs.3.rs-1909702/v1, publicado como preprint em 4 de agosto de 2022; adotado 2022 para essa versão. |
| Duttilo e Gattone | Rótulo 2023b na Tabela 2 | Documento associado à edição SIS 2022 e referência de 2022; adotado 2022. |
| Kumar | Referência de 2025; Crossref registra 2024 | O PDF informa publicação online em 2024 e volume 66 de 2025; preservado 2025 como ano da edição citada. |

Essas decisões não alteraram o Word original. Antes de incorporar a figura temporal definitiva, harmonizar as citações e referências da monografia com a versão que será efetivamente utilizada. Se a decisão for usar a versão publicada de Soltani, substituir os metadados e verificar o documento correspondente antes de recalcular a figura.

## Abrir a base no Biblioshiny

A partir da pasta do projeto, no PowerShell:

```powershell
& "C:/Program Files/R/R-4.6.0/bin/Rscript.exe" Scripts/abrir_biblioshiny_reconstruido.R
```

Na interface, utilizar **Data → Import or Load → Load bibliometrix file(s)** e selecionar `reports/bibliometria_reconstrucao/colecao_biblioshiny.RData`. O objeto foi validado com `smart_load`, o carregador do Biblioshiny. Não foi feita uma sessão interativa completa da interface.

Para a rede, escolher **Author Keywords** e frequência mínima de dois documentos. Keywords Plus não foi reconstruído. Contagens de citações recebidas, listas completas de referências citadas e afiliações permanecem ausentes; gráficos de citações, cocitação ou colaboração por país/instituição não devem ser interpretados a partir dessa coleção.

O código de importação genérica do pacote rotula a origem como Scopus internamente. A coleção `.RData` corrige explicitamente esse rótulo para `RECONSTRUIDA_PDFS_CROSSREF`. A documentação e os textos preservam essa identificação.

## Fontes das ferramentas

[bibliometrix](https://www.bibliometrix.org/software/) e [Biblioshiny](https://www.bibliometrix.org/biblioshiny/). Para citar o pacote na monografia, usar a referência bibliográfica retornada por `citation("bibliometrix")` no ambiente registrado. A data de recuperação de cada consulta Crossref está preservada nos arquivos de resposta em `crossref_bruto/`.
