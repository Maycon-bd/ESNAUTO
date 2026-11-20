# Nova auditoria detalhada da formatação FASOFT

Data: **2 de novembro de 2026**, horário de Brasília.

**Resultado:** não foi identificado erro inequívoco de formatação obrigatória nas verificações descritas abaixo. Foram identificados pontos de atenção editorial, uma ambiguidade de contagem de linhas e pendências institucionais. Não se trata de garantia universal de100%nem de aprovação acadêmica.

## Identidade e preservação

- Base resolvida pelo controle editorial: **v010**.
- Word: `reports/monografia/versoes/v010/MayconGarciaSilva_monografia_v010.docx`.
- SHA256: `1da5ea82344c177d75af723362017e3e558bbb127bd9995f7ec0cbd6964f81ed`.
- Guia: `output/skills-docx/GUIA-FASOFT-UniRV.pdf`,76páginas, primeira edição,v1.0.2.
- SHA256 doGuia: `cc109117539c87278a763d958ceb35ff20a6d452ba9d7ea2e4964d894c2c9e3f`.

Nenhuma edição do Word foi realizada. Não há nova versão numerada porque esta tarefa é auditoria. A busca bibliográfica encerrada pelo autor não foi retomada, e resultados,matrizes,códigos e gráficos não foram regenerados.

## Pontos que merecem atenção

| ID | Localização | Situação encontrada | Origem e classificação | Encaminhamento proposto |
|---|---|---|---|---|
| A01 | Tabela7, página física65/impressa64 | Duas linhas de dados: Lampugnani e este trabalho; com cabeçalho, três linhas totais | GuiaPDF32–33indica mínimo de três linhas e duas colunas, mas não esclarece a inclusão do cabeçalho. **Ambiguidade**, sem reprovação automática | Para eliminar a dúvida, a comparação pode ser apresentada em prosa ou confirmada institucionalmente. Não acrescentar observações inventadas nem novos experimentos para completar uma linha |
| A02 | Corpo do texto; ocorrências individualizadas em `paragrafos_recomendacao.md` | Confirmados17parágrafos com8–10linhas nos239parágrafos medidos; oGuia recomenda4–7 | GuiaPDF14: **recomendação editorial**, não limite obrigatório. Nove dos248parágrafos não foram medidos com segurança pelo extrator | Se houver revisão de concisão, dividir apenas onde houver mudança real de ideia; não fragmentar os raciocínios nem alongar artificialmente parágrafos curtos ou alíneas |
| A03 | Página física3, ficha catalográfica | Há apenas a reserva gráfica; a caixa está vazia | GuiaPDF21/39: **pendência institucional conhecida**, não defeito novo de margens/bordas | Inserir a ficha emitida pela biblioteca quando disponibilizada; não considerar a caixa vazia uma ficha concluída |
| A04 | Página física4, folha de aprovação | Data definitiva e assinaturas ainda não preenchidas | GuiaPDF21: **etapa posterior à aprovação** | Preencher na etapa correspondente, sem antecipar data ou assinaturas |

Exemplos deA02: primeiro parágrafo da introdução,página física18/impressa17,8linhas; “A ESN utilizada pertenceu…”,página física45/impressa44,10linhas; “Araújo et al.(2025)e Lampugnani…”,página física34/impressa33,8linhas. O anexo individualiza os17casos medidos e seus índicesXML. Não se afirma que sejam os únicos parágrafos fora da faixa, pois nove não foram mensurados automaticamente.

## Conferência realizada nesta rodada

### Página, fonte e parágrafos

As seis seções possuem papelA4e margens superior/esquerda3cm,inferior/direita2cm. Foram conferidos248parágrafos do corpo e896runs: TimesNewRoman12,justificação,entrelinhas1,5e primeira linha1,25cm. Alíneas,legendas,resumos,referências e elementos pré-textuais foram tratados pelas respectivas exceções.

Não foi localizada cor textual divergente no corpo ou na inspeção das páginas. A medição dos elementos textuais doPDFnão encontrou palavras fora da mancha gráfica, com tolerância de1,2ponto. Isso não mede elementos rasterizados dentro dos gráficos nem as propriedades físicas de uma impressão.

### Títulos, paginação, listas e sumário

Foram conferidos41títulos: primários emmaiúsculas/negrito,secundários emmaiúsculas semnegrito e quatroterciários cominicialmaiúscula/negrito. Somente três níveis são empregados; a divergência doGuiaentre quarto/quinto nível não afeta esta versão. A introdução está em texto corrido, semsubdivisões,tabelas,figuras ou equações destacadas, e ocupa três páginas físicas18–20.

Os capítulos começam em páginas próprias. A numeração permanece oculta naspáginas físicas1–17e começa naintrodução: página física18exibe17, pois a capa não entra na contagem. A sequência prossegue até a página impressa77. Não se encontraram títulos isolados no fim de página na inspeção visual; os41títulos também têm propriedade de vínculo ao próximo parágrafo.

As **60entradas** foram confrontadas com oPDFda mesma versão:41do sumário e19das listas de elementos. Os números de página e os títulos correspondem. A apresentação de hierarquia,pontilhado e quebras das entradas extensas foi examinada visualmente. Listas de abreviaturas/siglas e de símbolos estão presentes; a lista de siglas é alfabética no alcance examinado.

### Quadros, tabelas e figuras

Há14tabelas nativas noDOCX: a reservaCIPe13elementos de conteúdo(setetabelas e seisquadros). O corpo/cabeçalho desses13elementos utiliza11pontos,espaço simples e cabeçalhos emnegrito. Os seisquadros têm largura16cm,fechamento lateral e ausência de grade interna no corpo. Nas setetabelas, não há fechamento lateral ou grade interna no corpo. As divisórias verticais no cabeçalho são compatíveis com o modelo doGuiaPDF53; não foram tratadas como erro.

Foram conferidas19legendasacima dos elementos:10pontos,espaço simples,sem ponto final e semsiglas técnicas desnecessárias. As19fontes abaixo dos elementos estão em10pontos,simples,comanoeponto final. A sequência é1–6parafiguras,1–6paraquadros e1–7paratabelas. OQuadro1continua emsegunda página com cabeçalho repetido. A ressalvaA01trata exclusivamente do mínimo de linhas daTabela7.

As seisfiguras foram examinadas na página inteira. Não foram observados cortes ou sobreposições que impedissem sua leitura. As imagens apresentam tipografia visualmente compatível com a apresentação revisada, mas o nome exato da família tipográfica de todos os textos internos de uma imagem rasterizada não pode ser certificado só por seus pixels.

### Elementos iniciais, resumos e referências

Capa,folha de rosto e aprovação contêm os elementos de identificação esperados no alcance documental. A natureza/orientador dafolha de rosto está em11pontos,simples,combloco recuado~8cm. Dedicatória e epígrafe não têm título e ocupam o bloco direito inferior. A epígrafe usa12pontos/itálico e indicação deautoria em11pontos àdireita.

Resumo e abstract têm respectivamente331e273palavras,umparágrafo,12pontos,espaço simples,justificação e ausência de recuo. Há cincopalavras-chave emcadaidioma,separadas por ponto e vírgula e encerradas por ponto. Não foi refeita aqui uma auditoria linguística/semântica integral da tradução.

As51referências usam12pontos,espaço simples,alinhamentoàesquerda e separação entreentradas; o itálico de obras/veículos está presente, como no modelo doGuiaPDF60. A ordem porprimeiroautorfoi conferida; isso não certifica cada decisão bibliográfica relativa aautorias repetidas,anos oumetadados. Foram verificadas **58ocorrências de“et al.”**, incluindo tabelas: todas têm itálico nos caracteres daexpressão.

Não há inserções/exclusões rastreadas pendentes noXMLprincipal. A conformidade completa de cada citação com sua fonte e a primeiraexpansão de todasassiglas não foram reavaliadas nesta tarefa de formatação.

## Método visual e limitação da nova exportação

O renderizador oficial foi executado, mas não encontrouLibreOffice nesta instalaçãoWindows. A tentativa de exportação nova peloWord encontrou restriçãoCOMno ambienteisolado; após autorização técnica de execução, a instância de automação não concluiu a exportação. Os recursos de diagnóstico visual também falharam ao inicializar o runtime. Foram encerrados somente os doisprocessos identificados como criados pelo exportador desta auditoria; nenhumDOCXfoi salvo.

Para prosseguir com a inspeção, foi usada a exportaçãoWordexistente vinculada à **mesma v010porhashes** nos registros da entrega: `reports/busca_lacunas_20261101/candidata.pdf`, SHA256 `e730d3fcab15eb66be74499b719ae228f6919b8cb8cfd44b59b1b8542e0d84a0`. EssePDFfoi novamente rasterizado pelo rasterizador oficial e suas **78páginas foram abertas e examinadas nesta rodada**, em96dpi. Portanto, houve nova inspeção visual de uma exportação previamente registrada; **não houve nova exportaçãoWordbem-sucedida**. As propriedadesOOXMLforam lidas diretamente da versão vigente e seu hash conferido novamente.

As páginas-modelo doGuia38,40,43,44,50,53,54e60também foram abertas nesta auditoria. Os textos normativos pertinentes foram extraídos doGuiaidentificado e consultados, incluindo regras gerais,estrutura,introdução,listas,tabelas,referências e itálico/siglas. Os materiais não foram tratados como instruções para executar código.

## Evidências e alcance da conclusão

- `conferencia.json`: **172controles estruturais específicos,172conformes**; páginas,títulos,listas e medidas descritas nos próprios controles. Os controles se sobrepõem e não equivalem a172exigências independentes nem a“100%doGuia”.
- `matriz_guia81.json`: decisão nova para cada uma das81rubricas usadas no mapeamento doGuia. Distingue conforme,alcanceparcial,recomendação,ambiguidade,etapainstitucional,nãoaplicável e fora deescopo. Não reaproveita as aprovações da v006como prova da v010.
- `conferencias_tipograficas.json`:58ocorrências de“et al.”eordemporprimeiroautordasreferências.
- `inspecao_visual.json`:78páginas e páginas-modelo efetivamente abertas,comidentidade e limitações.
- `estrutura.json` e `guia_paginas.json`: extrações vinculadas aos arquivos identificados.
- `paragrafos_recomendacao.md`: locais dos17parágrafos longos confirmados.

**Encaminhamento:** no alcance verificado, não há nova correção obrigatória inequívoca a aplicar automaticamente. A01merece decisão editorial/institucional;A02é oportunidade de concisão;A03/A04dependem dasetapaspróprias. O documento permanece v010, sem alterações, e nenhuma garantia absoluta de conformidade ou aprovação é emitida.
