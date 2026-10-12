# Comparação dos gráficos bibliométricos e aplicação à monografia

Foram examinados o texto e as páginas com figuras dos dois PDFs fornecidos: a revisão apresentada no XXV ENMC em 2022 e o artigo de Cardoso et al. publicado em Knowledge-Based Systems em 2024. Os artigos oferecem modelos adequados para algumas figuras da monografia. A prioridade é frequência de palavras-chave, distribuição temporal e uma análise de expressões dos títulos. A rede de palavras-chave já produzida acrescenta a visualização de relações entre temas.

Os estudos de referência trabalham com 23 artigos selecionados, com recorte 2018–2022. Nossa coleção reconstruída contém 34 documentos, incluindo artigos, trabalhos de evento, preprints, dissertação, tese e referências anteriores ao recorte temporal. O tipo de gráfico pode ser aproveitado, mas as legendas, unidades e conclusões precisam descrever nosso conjunto real. A publicação de 2024 discute essencialmente a mesma linha de revisão do texto de 2022; os dois não devem ser tratados como duas amostras bibliográficas independentes que confirmam os resultados da nossa coleção.

## Inventário e compatibilidade

As páginas indicadas abaixo são as posições no PDF, contando a capa/primeira página como 1.

| Visualização | ENMC 2022 | KBS 2024 | Compatibilidade com nossos dados | Prioridade |
|---|---|---|---|---|
| Frequência de palavras-chave dos autores | Figura 2, p. 6; pontos e segmentos horizontais | Figura 1, p. 6; barras horizontais | Já produzida com 24 documentos com palavras-chave localizadas. A figura deve informar essa cobertura. | Alta |
| Documentos por ano | Figura 3, p. 7; linha e área | Figura 5, p. 7; colunas com efeito tridimensional | Já produzida com os 34 documentos e identificação das referências anteriores ao recorte. Manter barras em duas dimensões e o ano da versão adotada. | Alta |
| Frequência de expressões de duas palavras dos resumos | Figura 6, p. 8; treemap | Figura 2, p. 7; barras horizontais | Viável após completar e conferir os resumos. A base atual tem somente 10 resumos externos com mais de 100 caracteres; eles não representam os 34 documentos. | Alta após completar os dados |
| Expressões de duas palavras dos títulos | Figura 7, p. 8; nuvem de palavras | Sem figura equivalente | Viável com os 34 títulos disponíveis. Preferir barras para comparação de frequência; a nuvem pode ser uma apresentação complementar. | Alta para uma próxima figura |
| Dendrograma de expressões dos resumos | Figura 1, p. 6 | Sem figura equivalente | Exige resumos completos, extração de termos e decisões de agrupamento registradas. Não é prioritário com a cobertura atual. | Condicional |
| Documentos por revista ou evento | Figura 5, p. 7; pontos e segmentos | Fontes apresentadas nas tabelas e discutidas no texto | Viável. Separar os 24 artigos em periódicos dos demais tipos documentais. Na base atual apenas Expert Systems with Applications aparece mais de uma vez entre os periódicos, com dois documentos; as demais fontes têm um. | Média/baixa |
| Colaboração entre autores | Sem figura equivalente; o texto comenta grupos a partir do impacto de citações | Figura 3, p. 7; rede de coautoria | Viável após reconciliar nomes completos e iniciais. Não depende de contagens de citações, mas exige conferir homônimos e variantes de nomes. Acrescenta contexto social, com relação indireta à hipótese da monografia. | Média/baixa |
| Países dos autores correspondentes | Sem figura equivalente | Figura 4, p. 7; mapa | As afiliações e os autores correspondentes ainda não foram estruturados. Exige extração desses campos dos PDFs. Não usar o país do mercado estudado como substituto do país da afiliação. | Baixa neste trabalho |
| Impacto de citações dos autores | Figura 4, p. 7; pontos e segmentos, medida TC | O texto destaca trabalhos citados, com consulta ao Google Scholar em julho de 2023 | Não disponível na nossa base atual. Exige fonte de contagem, data de consulta e definição da métrica. Não substituir ausência por zero nem chamar quantidade de artigos de impacto de citação. | Baixa |
| Assuntos por ano | Figura 8, p. 8; tópicos temporais com segmentos e pontos | Sem figura equivalente | Pode ser calculada com termos e anos, mas a pequena amostra e a mistura de referências antigas com estudos recentes exigem recortes explícitos. Não sustenta uma afirmação de tendência de toda a área. | Baixa |

## O que cada artigo acrescenta como referência

O ENMC apresenta oito figuras e um repertório visual mais amplo. Sua Figura 7 demonstra uma opção que ainda não foi explorada na nossa coleção: expressões dos títulos. A Figura 1 documenta uma configuração do Biblioshiny para agrupamento de expressões dos resumos: Topic Dendrogram, Multidimensional Scaling, Abstracts, Bigrams, 34 termos e quatro grupos. O número 34 nessa configuração corresponde a termos selecionados, não à quantidade de documentos. Não há motivo para reutilizar automaticamente o mesmo número de termos ou grupos na nossa amostra.

O artigo de Knowledge-Based Systems apresenta cinco figuras. Para a nossa monografia, as mais diretamente úteis são as Figuras 1 e 2, com comparações de frequência em barras. A Figura 3 é uma rede de coautoria, diferente da rede de coocorrência de palavras-chave que já produzimos. São duas relações distintas: quem publicou com quem e quais termos foram declarados conjuntamente. A Figura 4 exige o país dos autores correspondentes; esse campo não pode ser deduzido apenas pelo nome dos autores.

As barras horizontais da KBS facilitam a leitura dos termos. O uso de colunas tridimensionais na Figura 5 não é necessário para nossa representação temporal; a versão em duas dimensões já produzida mantém os valores mais fáceis de comparar. O treemap e a nuvem do ENMC são possíveis formas de apresentação, mas a figura de barras oferece uma comparação quantitativa mais direta quando o objetivo é fundamentar a discussão.

## Conjunto de figuras recomendado

Para manter a seção 2.8 concentrada no problema da pesquisa:

1. **Cobertura das dimensões P1–P5**, derivada da extração de conteúdo já presente na monografia. É a figura mais diretamente ligada à discussão de inicialização, otimização e pré-processamento.
2. **Frequência de palavras-chave declaradas**, tomando como referência ENMC Figura 2 e KBS Figura 1. Já disponível na coleção reconstruída.
3. **Rede de coocorrência das palavras-chave**, já calculada com bibliometrix. Deve complementar a frequência, mostrando relações entre termos, sem ser apresentada como reprodução da rede de coautoria da KBS.
4. **Frequência de expressões dos títulos**, tomando como referência ENMC Figura 7. É a próxima adição mais viável porque os 34 títulos estão disponíveis. Uma apresentação em barras reúne a ideia do ENMC e a leitura quantitativa das figuras de frequência da KBS.

A distribuição temporal pode permanecer como caracterização inicial do conjunto ou ser deslocada para uma apresentação complementar, conforme o espaço da seção. Ela não deve ser interpretada como crescimento da produção de toda a área, pois o conjunto foi selecionado e contém fontes fundamentais anteriores ao recorte.

Se houver limitação de espaço, usar P1–P5, frequência de palavras-chave e a rede; incorporar a figura dos títulos somente se ela revelar informação complementar, sem repetir a mesma conclusão.

## Regras para a figura de títulos

Para que a nova análise seja compatível com a referência do ENMC e auditável:

- Usar o campo de título dos 34 registros reconstruídos e preservar o texto original.
- Identificar o idioma e tratar a referência de Costa e Lunkes, cujo título na base está em português; não misturar traduções livres silenciosamente com títulos em inglês. O PDF fornece também título em inglês, que pode ser transcrito e identificado como essa versão.
- Definir o que é uma expressão de duas palavras: pares adjacentes no título, tratamento de pontuação, palavras de ligação e repetição por documento.
- Para nossa proposta, contar presença por documento e indicar isso no eixo. Uma expressão repetida no mesmo título conta uma vez. Caso sejam contadas ocorrências, nomear o eixo como ocorrências e não como número de documentos.
- Informar o número de documentos incluídos e as normalizações. Não confundir palavras extraídas dos títulos com palavras-chave declaradas pelos autores.
- Evitar transformar pares incompletos, como “echo state” ou “state network”, em conceitos independentes na interpretação. A expressão completa Echo State Network pode ser comentada com base nos títulos originais.

Nos artigos de referência, as figuras de expressões dos resumos usam contagens de ocorrências; por exemplo, “time series” aparece 34 vezes no conjunto de 23 estudos. Essa quantidade não é diretamente comparável à nossa frequência binária por documento. A diferença entre as unidades deve ser mantida explícita.

## Resumos, dendrograma e tendências

O campo de resumo atual contém dez registros externos com texto substancial. É possível ampliar a cobertura pela extração e conferência dos PDFs, mas ainda não foi feita uma transcrição validada de todos os resumos. Não usar introduções inteiras como substitutos nem atribuir palavras-chave a partir de uma leitura do resumo sem identificar que se trata de uma análise textual diferente.

Após completar os resumos, barras de expressões recorrentes são uma primeira opção mais simples que dendrogramas. Caso se opte por agrupamento, registrar termos, distância, método, número de grupos e sensibilidade às escolhas. A ausência de ligação ou o afastamento visual de um termo não demonstra, isoladamente, ausência de trabalhos sobre uma temática. As lacunas específicas sobre distribuições Win/W continuam dependendo da leitura e da matriz P1–P5.

Um gráfico temporal de temas pode descrever sua coleção, mas sua interpretação deve reconhecer anos com poucos documentos e o papel das obras fundamentais. Não é adequado afirmar que um método “surgiu” no ano em que aparece nessa pequena amostra.

## Como referenciar as figuras adaptadas

Para figuras calculadas com nossa base, a fonte deve identificar a autoria do gráfico e a origem dos dados. Exemplo:

> Fonte: Elaborado pelo autor a partir da base bibliográfica reconstruída dos documentos citados (2026). A escolha da visualização tomou como referência Cardoso et al. (2022, Figura 2) e Cardoso et al. (2024, Figura 1).

Utilizar “adaptado de” quando houver adaptação concreta de uma representação ou estrutura do artigo e explicá-la. As imagens, valores, autores, países e resultados dos artigos de referência não devem ser apresentados como resultados da nossa pesquisa. A referência metodológica ao bibliometrix deve permanecer separada da referência aos artigos que inspiraram a apresentação.

Antes da inserção, conferir a identificação das novas referências na bibliografia. A monografia já usa Cardoso et al. (2022a/2022b) para outros trabalhos; o artigo ENMC é uma fonte adicional e a ordenação dos sufixos daquele ano precisará ser harmonizada com as regras utilizadas na monografia. O artigo da KBS corresponde a uma referência publicada em 2024, distinta do artigo de Araújo et al. (2024).

## Documentos examinados

- Cardoso, F. C.; Berri, R. A.; Borges, E. N.; Lucca, G.; Mattos, V. L. D. **Associação de redes de estado de eco com métodos estatísticos clássicos de previsão: uma revisão bibliométrica.** XXV ENMC, 2022. Figuras 1–2 na p. 6; Figuras 3–5 na p. 7; Figuras 6–8 na p. 8 do PDF fornecido.
- Cardoso, F. C.; Berri, R. A.; Borges, E. N.; Dalmazo, B. L.; Lucca, G.; Mattos, V. L. D. **Echo state network and classical statistical techniques for time series forecasting: A review.** Knowledge-Based Systems, v. 293, art. 111639, 2024. Figura 1 na p. 6 e Figuras 2–5 na p. 7 do PDF fornecido.

Os arquivos foram examinados localmente. As páginas renderizadas em `previas/` servem para conferência interna das figuras de referência. Esta etapa é uma análise de compatibilidade; não incluiu os dois artigos na coleção de 34 documentos nem criou novos gráficos de resumos ou títulos.
