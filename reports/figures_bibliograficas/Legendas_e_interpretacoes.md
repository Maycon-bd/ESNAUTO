# Gráficos da literatura para a monografia

Estas primeiras versões representam os 34 estudos listados na Tabela 2 do documento fornecido. Os dados foram extraídos sem excluir estudos nem alterar anos ou classificações. A composição do portfólio ainda precisa ser reconciliada com os critérios descritos na seção 3.8.3 antes da inserção definitiva. Os gráficos foram produzidos em R a partir da tabela, sem uso do bibliometrix ou Biblioshiny.

## Cobertura das dimensões analíticas

Arquivo: `figura_cobertura_p1_p5.png`. Versão vetorial: `figura_cobertura_p1_p5.svg`.

Legenda sugerida: **Figura X — Cobertura das dimensões analíticas nos estudos listados na Tabela 2.**

Fonte sugerida: Elaborado pelo autor a partir da matriz de extração bibliográfica (2026).

Nota sugerida: P1 corresponde à distribuição de inicialização dos pesos; P2, à otimização dos hiperparâmetros; P3, ao pré-processamento; P4, à comparação com modelos de Deep Learning; e P5, ao mercado e ativo investigado. Cada estudo pode cobrir mais de uma dimensão; os percentuais não somam 100%.

Texto descritivo sugerido:

> Na matriz de extração dos 34 estudos, o pré-processamento foi a dimensão com maior cobertura, presente em 31 trabalhos (91,2%), seguido da identificação do mercado e ativo, registrada em 30 (88,2%). A comparação com modelos de Deep Learning apareceu em 21 estudos (61,8%), enquanto inicialização dos pesos e otimização dos hiperparâmetros foram abordadas em 16 estudos cada (47,1%). Essa distribuição permite visualizar a cobertura relativa das dimensões investigadas no conjunto selecionado. A identificação das práticas específicas de inicialização depende da análise do conteúdo de cada estudo, e não apenas dessas frequências.

Posição sugerida: seção 2.8, após a apresentação da Tabela 2. Evitar repetir integralmente a mesma informação em tabela, gráfico e texto; usar a tabela para consulta por estudo e o gráfico para a comparação agregada.

## Distribuição dos estudos por ano

Arquivo: `figura_estudos_por_ano.png`. Versão vetorial: `figura_estudos_por_ano.svg`.

Legenda sugerida: **Figura Y — Distribuição dos estudos listados na Tabela 2 segundo o ano informado.**

Fonte sugerida: Elaborado pelo autor a partir dos anos apresentados na Tabela 2 (2026).

Texto descritivo sugerido:

> Dos 34 estudos listados, 29 (85,3%) possuem anos informados entre 2021 e 2025, enquanto cinco são anteriores a 2021. O ano de 2025 reúne dez estudos, a maior frequência no conjunto. Essa concentração caracteriza a composição da tabela e não representa, isoladamente, a evolução da produção científica de toda a área.

Nota de conferência: a tabela inclui Nelson (1991), Jaeger (2007), Millea (2014), Timbó (2016) e Ecer (2020), apesar do recorte formal 2021–2026. Os rótulos Duttilo (2023a/2023b) também precisam ser conciliados com os anos e tipos documentais das referências. O gráfico transcreve os anos da tabela atual. Caso a tabela seja corrigida ou referências complementares sejam separadas do portfólio, regenerar ambos os gráficos e seus denominadores.

## Etapa seguinte com Biblioshiny

Para produzir coocorrência de palavras-chave, obter os registros exportados de Scopus ou outra base suportada, incluindo palavras-chave, títulos, resumos e referências citadas quando disponíveis. Recuperar a exportação existente é suficiente para iniciar; não é necessário organizar a biblioteca no JabRef.

Para manter a análise ligada aos estudos citados, filtrar os registros pelos títulos/DOIs do conjunto que for confirmado. Não importar todos os resultados de uma busca e descrever o gráfico como sendo dos 34 estudos selecionados. O mapa deve representar os dados reais disponíveis; o DOCX sozinho não fornece palavras-chave originais completas para essa análise.

Se as exportações não estiverem disponíveis, os gráficos descritivos derivados da tabela podem ser utilizados após a conferência, sem declarar que foram produzidos com Biblioshiny. Uma nova recuperação de metadados deve registrar origem e data efetivas, sem atribuir retrospectivamente esses dados à busca original.
