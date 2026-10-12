# Reconstrução bibliográfica a partir dos PDFs citados

É possível iniciar a análise sem recuperar a exportação original do Scopus. A pasta `Artigos citados` contém 34 PDFs. Foi realizada uma inspeção automatizada das primeiras quatro páginas de cada arquivo, preservando nome, hash, trechos e candidatos a identificadores no arquivo `inventario_pdfs.json`.

Atualização: a reconstrução foi executada. A coleção de 34 registros foi importada no bibliometrix 5.5.0, o arquivo processado foi validado com o carregador do Biblioshiny e foram gerados gráficos a partir de 24 documentos com palavras-chave localizadas. Consultar [Resultados e texto para a monografia](Resultados_e_texto_para_monografia.md) para os arquivos finais, a cobertura e as diferenças de versão.

## Resultado da inspeção inicial

| Verificação | Quantidade |
|---|---:|
| PDFs encontrados | 34 |
| PDFs com mais de 200 caracteres extraídos nas páginas iniciais | 33 |
| PDFs com ao menos um candidato a DOI | 26 |
| PDFs com marcador de palavras-chave ou Index Terms | 24 |
| Erros que impediram abertura dos PDFs | 0 |

Um marcador não garante uma lista de palavras-chave completa. Um DOI encontrado pode corresponder a uma fonte citada, e não ao próprio documento. Os títulos e autores embutidos nas propriedades dos PDFs também não são considerados metadados confirmados.

O PDF de Nelson não forneceu texto útil nessa amostra inicial. Será necessário recuperar seus metadados por identificador/título ou usar OCR para extrair conteúdo. Não se concluiu, a partir dessa amostra, que todas as páginas do arquivo são imagens.

## Referências fundamentais e recorte temporal

As obras fundamentais anteriores ao recorte devem continuar citadas quando sustentam os conceitos utilizados. O recorte da seleção sistemática e o conjunto de referências da fundamentação possuem funções diferentes. Não é necessário remover as obras fundamentais para respeitar o recorte; é necessário explicitar como elas foram incorporadas.

Texto proposto para revisão pelo autor e orientador, ajustando-o ao procedimento efetivamente realizado:

> O recorte temporal de 2021 a 2026 foi aplicado à seleção de estudos recentes. A fundamentação teórica incorporou adicionalmente obras anteriores a esse intervalo, selecionadas por sua relevância para a origem e a definição dos conceitos utilizados. Essas referências complementares foram identificadas separadamente, sem serem tratadas como resultados da busca submetida ao recorte temporal.

Não atribuir essa justificativa automaticamente a todo estudo antigo. Identificar quais são obras fundadoras e quais entraram por comparação histórica ou apoio metodológico. As cinco entradas anteriores a 2021 na tabela atual são Nelson (1991), Jaeger (2007), Millea (2014), Timbó (2016) e Ecer (2020). A classificação deve refletir o uso efetivo de cada fonte.

Se os gráficos descreverem todos os 34 estudos citados na tabela, utilizar a denominação “conjunto de estudos analisados” e informar que ele inclui referências complementares. Se descreverem apenas o portfólio formal do recorte, filtrar os registros confirmados e recalcular os denominadores. Não excluir retrospectivamente fontes sem documentar a decisão.

## Procedimento proposto

1. Confirmar título, autores, ano, tipo documental e versão de cada PDF. Usar as referências do DOCX como apoio, confrontando-as com o documento efetivamente disponível.
2. Recuperar metadados faltantes por DOI ou título em fontes oficiais de publicação e índices abertos. Manter fonte e data de recuperação por registro.
3. Extrair as palavras-chave efetivamente declaradas pelos autores. Quando não houver palavras-chave, manter o campo ausente. Termos extraídos de títulos/resumos devem formar uma análise separada e ser identificados como tais.
4. Normalizar variantes de termos com um dicionário preservado, por exemplo “echo state network” e “echo state networks”. Não juntar termos distintos apenas para tornar a rede mais conectada.
5. Gerar um arquivo bibliográfico genérico ou uma coleção de dados reconhecida pelo bibliometrix. Verificar a importação e a cobertura dos campos antes de gerar os mapas.
6. Produzir a rede de coocorrência com as regras registradas: unidade de análise por documento, termos utilizados, frequência mínima, tratamento de sinônimos e número de documentos com metadados disponíveis. A rede não deve usar 34 como denominador quando somente uma parte do conjunto possuir palavras-chave.

O código oficial de `convert2df` contempla BibTeX genérico (`dbsource = "generic"`). Isso confirma uma alternativa no bibliometrix; não confirma, por si só, que um arquivo reconstruído ainda não produzido será aceito por qualquer versão da interface Biblioshiny. A importação precisa ser testada na versão utilizada. [Código oficial](https://github.com/massimoaria/bibliometrix/blob/master/R/convert2df.R).

O Biblioshiny também documenta importação de registros e recuperação por OpenAlex. Seu código de desenvolvimento contém funções de análise de conteúdo de PDFs, distintas da importação tradicional de uma coleção bibliográfica. A disponibilidade efetiva dessas funções depende da versão e de suas dependências. [Página oficial do Biblioshiny](https://www.bibliometrix.org/biblioshiny/).

## Conferências já identificadas

O PDF de Soltani disponível na pasta apresenta o DOI `10.21203/rs.3.rs-1909702/v1` e data de postagem de 4 de agosto de 2022. A referência da monografia informa Neural Processing Letters, 2023. É necessário localizar a versão publicada ou identificar claramente a versão usada, sem combinar silenciosamente ano e metadados de versões diferentes.

O PDF de Millea se identifica como dissertação de mestrado de junho de 2014. Um dos PDFs de Duttilo se identifica como tese de doutorado com anos acadêmicos 2020/23. Assim, o conjunto não deve ser descrito indiscriminadamente como composto exclusivamente por artigos.

## Análises e seus limites

As frequências por ano e as dimensões P1–P5 podem ser calculadas com metadados e extrações locais confirmados. As redes de palavras-chave podem ser calculadas quando houver cobertura suficiente, com o número de documentos participantes informado.

Contagens de citações recebidas não estão contidas integralmente nos PDFs. Caso sejam utilizadas, recuperá-las de uma fonte identificada e registrar a data. Contagens atuais de OpenAlex não devem ser apresentadas como contagens históricas do Scopus na busca de março de 2026. Referências citadas ao final dos PDFs são dados distintos das citações que esses documentos receberam.

A descrição metodológica correta é “base reconstruída a partir dos documentos e enriquecida por metadados externos”, caso essa seja a estratégia efetivamente executada. Não denominar essa coleção “exportação Scopus recuperada” nem recriar retroativamente o histórico de resultados, duplicatas e exclusões da busca original.

A inspeção inicial documentada acima foi seguida pela criação de `artigos_reconstruidos.bib` e `colecao_biblioshiny.RData`, instalação isolada do bibliometrix e execução da rede de palavras-chave. A matriz de coocorrência foi validada por uma contagem independente por documento. A ausência de campos de citações e afiliações permanece explicitamente registrada.
