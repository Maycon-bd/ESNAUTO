# Figuras para a fundamentação da monografia

Este conjunto reúne quatro figuras calculadas com os documentos da pesquisa. O novo gráfico de expressões dos títulos complementa a cobertura P1–P5, a frequência de palavras-chave e a rede de coocorrência. A proposta é inserir as figuras na seção 2.8, com interpretação dos dados e identificação das diferentes unidades de análise. As fontes anteriores ao recorte temporal foram mantidas.

Os arquivos PNG estão a 300 dpi e os SVGs permitem redimensionamento sem perda de definição. O Word original não foi modificado. As indicações Figura A–D abaixo são provisórias; a numeração definitiva depende da ordem das figuras na monografia.

## Ordem de apresentação

| Ordem | Arquivo PNG e SVG | Base | Função no argumento |
|---|---|---|---|
| A | `01_cobertura_p1_p5` | 34 estudos da matriz da monografia | Relacionar o portfólio às dimensões investigadas |
| B | `02_frequencia_palavras_chave` | 24 documentos com palavras-chave localizadas | Caracterizar os temas declarados pelos autores |
| C | `03_rede_palavras_chave` | Os mesmos 24 documentos | Mostrar quais termos são declarados conjuntamente |
| D | `04_expressoes_titulos` | 34 títulos | Complementar a caracterização textual com cobertura integral dos títulos |

A distribuição por ano produzida anteriormente pode permanecer como caracterização complementar, mas não integra este conjunto de quatro figuras. Ela exige harmonizar as referências da monografia com os anos das versões locais documentados no relatório de reconstrução.

## Método complementar para a seção 3.8.3

Texto proposto, a integrar à metodologia já existente:

> A caracterização bibliográfica foi complementada por uma análise descritiva dos documentos utilizados na fundamentação. A coleção de 34 registros foi reconstruída a partir dos PDFs disponíveis, das referências da monografia e de conferência de metadados por DOI ou título. As referências anteriores ao recorte temporal foram preservadas como fontes complementares, distinguindo-se a seleção de estudos recentes da utilização de obras fundamentais e de contextualização. As frequências da matriz P1–P5 foram calculadas a partir das classificações já apresentadas na Tabela 2.

> A análise de palavras-chave utilizou os 24 documentos em que foram localizadas listas declaradas pelos autores. Após a normalização registrada das variantes de termos, foram calculadas frequências binárias por documento e uma matriz de coocorrência no bibliometrix 5.5.0. A rede incluiu os termos presentes em pelo menos dois documentos, com 14 nós e 33 ligações. O posicionamento visual utilizou Fruchterman–Reingold e a identificação das comunidades utilizou Walktrap, com a semente 20261012 registrada no código.

> Para a análise dos títulos, foram extraídos pares de palavras adjacentes, denominados bigrams, dos 34 registros. Os títulos foram convertidos para minúsculas e tokenizados em palavras; pontuação, algarismos e hífens não foram conservados como parte dos tokens. Os pares foram formados antes da exclusão de palavras de ligação, de modo que a remoção dessas palavras não criasse pares entre termos originalmente distantes. Não foram aplicados stemming, expansão de siglas nem agrupamento entre singular e plural. Cada expressão contou uma única vez por documento, e o gráfico incluiu pares presentes em pelo menos dois títulos. Para Costa e Lunkes, foi utilizada a versão inglesa do título explicitamente apresentada na página 2 do PDF. Os textos bibliográficos originais foram preservados em campos separados.

> A matriz de expressões dos títulos foi processada com biblioNetwork, campo titles, no bibliometrix e conferida por contagem independente dos pares por documento. As análises de títulos e palavras-chave foram mantidas separadas. Seus resultados descrevem a coleção utilizada no trabalho e não constituem uma estimativa da produção de toda a área ou uma demonstração isolada de lacuna científica.

A seleção dos formatos tomou como referência as figuras de frequência dos artigos de Cardoso et al. do ENMC de 2022 e da Knowledge-Based Systems de 2024. O gráfico de títulos se inspira no objeto de análise da Figura 7 do ENMC, apresentado aqui em barras, permitindo comparação direta dos valores. Os gráficos da monografia utilizam seus próprios registros e contagens.

## Figura A e interpretação

**Figura A — Cobertura das dimensões analíticas nos estudos da matriz bibliográfica.**

**Fonte:** Elaborado pelo autor a partir da Tabela 2 da monografia (2026).

**Nota:** P1 — distribuição de inicialização dos pesos; P2 — otimização de hiperparâmetros; P3 — pré-processamento; P4 — comparação com modelos de Deep Learning; P5 — mercado e ativo. Um estudo pode cobrir várias dimensões. Os percentuais têm denominador 34 e não somam 100%.

Texto proposto:

> A Figura A sintetiza a cobertura das dimensões analisadas nos 34 estudos da matriz bibliográfica. O pré-processamento apresenta a maior frequência, com 31 estudos (91,2%), seguido da identificação do mercado e ativo, presente em 30 (88,2%). A comparação com Deep Learning aparece em 21 estudos (61,8%), enquanto inicialização dos pesos e otimização dos hiperparâmetros são abordadas em 16 estudos cada (47,1%). As frequências permitem comparar a cobertura relativa das perguntas de extração no conjunto selecionado. A identificação das distribuições efetivamente utilizadas e de sua fundamentação exige a consulta aos estudos e à matriz de extração, além da contagem agregada.

## Figura B e interpretação

**Figura B — Frequência documental das palavras-chave recorrentes declaradas pelos autores.**

**Fonte:** Elaborado pelo autor a partir dos PDFs citados, com processamento no bibliometrix 5.5.0 (2026).

**Nota:** Foram analisados 24 documentos com palavras-chave localizadas, correspondentes a 70,6% dos 34 documentos da coleção. O gráfico apresenta termos declarados em pelo menos dois documentos. A repetição de uma palavra-chave no mesmo documento não aumenta sua frequência.

Texto proposto:

> A Figura B apresenta a frequência das palavras-chave recorrentes no subconjunto com metadados disponíveis. Echo state network foi identificado em nove documentos (37,5%), enquanto reservoir computing apareceu em cinco (20,8%). Deep learning, stock price forecasting e time series foram registrados em três documentos cada (12,5%). As frequências caracterizam os temas declarados pelos autores dos documentos incluídos nessa análise. A ausência de determinado termo entre as palavras-chave não significa ausência de discussão do conceito no corpo do artigo.

## Figura C e interpretação

**Figura C — Rede de coocorrência de palavras-chave declaradas nos documentos analisados.**

**Fonte:** Elaborado pelo autor com bibliometrix 5.5.0 a partir da base reconstruída (2026).

**Nota:** Matriz obtida dos mesmos 24 documentos da Figura B. A frequência mínima de dois documentos resulta em 14 termos e 33 ligações. A área dos nós representa frequência documental, a espessura das ligações representa documentos compartilhados e as cores correspondem às comunidades calculadas por Walktrap. A figura representa relações entre termos, e não coautoria ou citações entre documentos.

Texto proposto:

> A Figura C permite observar relações entre echo state network, reservoir computing, deep learning e termos associados à previsão financeira. LSTM e GRU também integram a rede, juntamente com expressões como optimization e machine learning. As ligações indicam que os termos foram declarados conjuntamente como palavras-chave nos documentos analisados. Esse resultado oferece uma caracterização temática complementar, enquanto as afirmações específicas sobre inicialização de Win/W, otimização e pré-processamento permanecem fundamentadas na leitura dos estudos e na extração P1–P5.

## Figura D e interpretação

**Figura D — Frequência documental de expressões de duas palavras nos títulos dos estudos.**

**Fonte:** Elaborado pelo autor a partir dos 34 títulos da base reconstruída (2026). A escolha do objeto de análise tomou como referência a Figura 7 da revisão bibliométrica apresentada por Cardoso et al. no ENMC de 2022.

**Nota:** Cada par de palavras adjacentes é contado uma vez por documento. São exibidas 19 expressões presentes em pelo menos dois títulos. Singular, plural e siglas foram conservados separadamente. O título inglês de Costa e Lunkes foi transcrito do próprio PDF. Os pares podem compartilhar palavras e ocorrer no mesmo documento; suas frequências não devem ser somadas como categorias independentes.

Texto proposto:

> A análise dos títulos identificou 19 expressões presentes em pelo menos dois documentos, conforme a Figura D. Echo state apareceu em 11 títulos (32,4%), state network em sete (20,6%) e time series em seis (17,6%). Reservoir computing, stock market e stock price foram identificadas em quatro títulos cada (11,8%), enquanto genetic algorithm ocorreu em dois (5,9%). Esses resultados caracterizam a presença textual de arquiteturas e tarefas nos títulos do conjunto analisado. Expressões como echo state e state network constituem partes da denominação Echo State Network e não devem ser interpretadas como conceitos independentes nem somadas para estimar a quantidade de estudos sobre ESN.

> A análise dos títulos utiliza 34 documentos, ao passo que a análise de palavras-chave utiliza 24. Assim, as diferenças entre suas frequências também refletem a cobertura dos campos, a redação dos títulos e as regras de normalização aplicadas. A comparação entre as figuras serve à caracterização do conjunto e não substitui a análise do conteúdo dos trabalhos.

## Referências dos modelos de apresentação

Os artigos fornecidos pelo autor devem ser citados caso a monografia descreva sua influência na escolha das visualizações:

- CARDOSO, F. C.; BERRI, R. A.; BORGES, E. N.; LUCCA, G.; MATTOS, V. L. D. Associação de redes de estado de eco com métodos estatísticos clássicos de previsão: uma revisão bibliométrica. In: XXV ENCONTRO NACIONAL DE MODELAGEM COMPUTACIONAL, 2022. Anais [...]. 2022.
- CARDOSO, F. C.; BERRI, R. A.; BORGES, E. N.; DALMAZO, B. L.; LUCCA, G.; MATTOS, V. L. D. Echo state network and classical statistical techniques for time series forecasting: A review. Knowledge-Based Systems, v. 293, art. 111639, 2024.

Conferir o padrão institucional e completar os dados bibliográficos exigidos antes da inclusão definitiva. A monografia já utiliza sufixos 2022a/2022b para outras referências de Cardoso; a entrada do ENMC exige harmonizar esses identificadores. Não atribuir um sufixo novo sem verificar a ordenação de toda a bibliografia. Para o pacote, utilizar a referência retornada por `citation("bibliometrix")` no ambiente registrado.

## Arquivos de rastreabilidade

Os registros usados no novo gráfico estão em `../expressoes_titulos.json`, incluindo título original, título analisado, tokens, pares e identificadores dos documentos que contêm cada expressão. A lista de palavras de ligação foi preservada no mesmo arquivo. As validações estão em `validacao_conjunto.json`.

A coleção `../colecao_biblioshiny.RData` mantém os títulos bibliográficos em TI e acrescenta TI_TM para os pares extraídos. Foi preservada a identificação da origem reconstruída e a ausência de contagens de citações. Os dados de título e a análise P1–P5 não foram convertidos em palavras-chave declaradas.

Para regenerar o conjunto a partir da raiz do projeto:

```powershell
& "C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe" Scripts/extrair_expressoes_titulos.py
& "C:/Program Files/R/R-4.6.0/bin/Rscript.exe" Scripts/gerar_conjunto_figuras_monografia.R
```

Se a base bibliográfica for reconstruída novamente com os scripts anteriores, executar essas duas etapas ao final para repor a análise dos títulos na coleção processada.
