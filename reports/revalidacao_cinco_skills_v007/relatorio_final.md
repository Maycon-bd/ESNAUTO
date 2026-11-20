# Revalidação das cinco skills na monografia

A conferência das cinco skills foi concluída, partindo da versão vigente v007. Os achados antigos da v001 foram confrontados com o texto atual, sem serem automaticamente reapresentados como defeitos. Foram incorporados três ajustes finais de consistência e navegação. Não restou correção conhecida por aplicar no escopo desta passagem; permanecem os limites científicos e documentais explicitados no manuscrito.

Esta conclusão se refere às verificações e evidências descritas abaixo. Não significa garantia absoluta de ausência de erro, leitura integral nova das 50 obras, certificado de originalidade ou aprovação institucional.

## Identidade e método

- Base resolvida por `python Scripts/versao_monografia.py atual --json`: v007, `reports/monografia/versoes/v007/MayconGarciaSilva_monografia_v007.docx`.
- SHA256 da base: `983c46424ad039472bb12071540d392d73eb29cb08a07e0bc784e0ede008ff1c`.
- Cópia preparada pelo controle de versões: `reports/monografia/trabalho/revalidacao_cinco_skills_v007.docx`, com `.origem.json` preservado.
- SHA256 da cópia conferida: `0daacd3ea1753bca97619df025923b92a44a047b5c1252a4677f802dfe870dad`.
- Foram lidos os arquivos de instrução das cinco skills e as referências aplicáveis, a skill monografia-esnauto, contexto e registro de fontes do projeto.
- Inventário atual: 551 parágrafos principais, 484 parágrafos de células, 13 elementos tabulares acadêmicos, 50 entradas de siglas e 50 referências. A ficha catalográfica é a tabela de índice zero e não foi confundida com quadro de conteúdo.

Os localizadores P são índices zero-based dos parágrafos principais da v007. T09 L5 C1, por exemplo, identifica tabela de índice 9, linha 5, coluna 1. Não são números de página. Os parágrafos não foram inseridos ou excluídos nesta revisão.

## Resultado das cinco skills

| Skill | Conferência realizada | Resultado |
|---|---|---|
| quadro-tabela-validator-docx | 7 tabelas e 6 quadros; classificação, tipografia efetiva, dimensões, bordas de cabeçalho/corpo, títulos, fontes, chamadas, sequência e listas; confronto visual com PDF 53–54 do guia | Controles tabulares aprovados antes e depois dos ajustes. Chamadas locais para Tabelas 5 e 6 acrescentadas para aproximar a remissão da discussão correspondente |
| ingles-italico-checker-docx | Varredura atual de 138 ocorrências candidatas, com runs/estilos, expansões e contexto; confronto com exceções institucionais e lista oficial da Secom | Não identificada omissão nova nos candidatos. As cinco omissões antigas foram corrigidas nas revisões intermediárias. As 56 ocorrências de et al. localizadas na parte textual e células estão em itálico |
| siglas-checker-docx | 50 entradas, ordenação, usos e primeiras menções na parte textual, exceções para nomes de modelos/tickers/pacotes, relação com títulos | Lista alfabética e sem entrada sem uso no escopo. Expansões incompletas antigas corrigidas. Padronizada a sigla genérica AG em uma célula da Tabela 5, preservando o nome do pacote GA |
| tcc-writer-docx | Conciliação dos 328 parágrafos do corpo com decisões prévias, reavaliação dos sete parágrafos linguísticos modificados, leitura visual do documento, redação/aplicação das duas chamadas locais | 321 parágrafos idênticos após normalização de espaços e sete ajustes linguísticos equivalentes. Chamadas novas têm menos de 700 caracteres com seus parágrafos, sem afirmação científica nova |
| tcc-citation-checker-docx | Conciliação das 163 chamadas inventariadas, das 50 referências, da matriz de 170 células e das evidências primárias/dirigidas existentes; preservação após os três ajustes | 161 contextos idênticos à validação anterior e dois com ajustes linguísticos equivalentes reavaliados. As 170 células correspondem à conciliação atual; os 34 PDFs da matriz conservam seus hashes |

## Quadros, tabelas e apresentação

Os 13 elementos mantêm títulos em 10 pt, justificados, simples e sem ponto-final; cabeçalhos em 11 pt e negrito; corpo em 11 pt e simples; fontes em 10 pt, com ano e pontuação. Os seis quadros têm 16 cm e fechamento lateral; as sete tabelas têm laterais abertas. O corpo de ambos permanece sem grade interna. As divisórias de cabeçalho, ausentes na v001, estão presentes na v007 e na cópia revisada.

Todos têm chamada narrativa e numeração própria. As listas distinguem Quadros e Tabelas; os títulos dos elementos não contêm as siglas listadas. A correspondência das páginas de abertura das 19 legendas — incluindo seis figuras — foi conferida no PDF e permaneceu igual após os ajustes.

A anotação de cabeçalho do quadro no guia tem tensão com o desenho que não exibe claramente as divisórias verticais. Foi preservada a decisão já aplicada, coerente com a anotação, sem impor grade ao corpo. A chamada posterior de um elemento não foi declarada infração automática: o guia exige referência e proximidade, sem ordem textual absoluta na passagem normativa examinada.

O corpo da Tabela 7 tem duas linhas de dados mais o cabeçalho. O guia indica mínimo de três linhas e duas colunas sem esclarecer se exclui o cabeçalho; não se inventou uma terceira linha de resultados para satisfazer uma interpretação não explicitada.

## Siglas e estrangeirismos

Os 50 extensos e suas primeiras ocorrências foram novamente localizados na sequência do texto, incluindo tabelas na posição documental. Modelos compostos, tickers e nomes de software não foram automaticamente adicionados à lista como siglas órfãs. Por exemplo, MLP em TConv-MLP pertence ao nome de um comparador; a explicação do conceito está no contexto de Ecer. BIST e DJIA estão na lista e possuem extensos no texto; JPX identifica o título oficial de um conjunto de dados.

CS-ESN está expandida como Compressed Sensing Echo State Network, e HQNN não reaparece como expansão incompleta na lista. Reapresentações de termos em seções conceituais não foram substituídas mecanicamente. Siglas consagradas e nomes em títulos originais foram preservados.

Nas ocorrências candidatas sem itálico restaram Ridge, software e script/scripts. Ridge é mantido como denominação técnica do método na convenção editorial já registrada, e não como nome de pessoa. Software e script pertencem às exceções da [lista oficial da Secom/Senado](https://www12.senado.leg.br/manualdecomunicacao/verbetes-acessorio/estrangeirismos-grafados-sem-italico-ou-aspas), novamente acessada em 31/10/2026. A variação de Ridge dentro da expressão inglesa completa Ridge Regression tem função distinta. Abstract, nomes bibliográficos e símbolos matemáticos não foram classificados como prosa portuguesa a ser corrigida globalmente.

Uma varredura lexical não prova detecção universal de toda palavra estrangeira. Ela foi conciliada com as decisões de expansões, termos residuais e leitura contextual anteriores, e com a inspeção atual do texto renderizado.

## Fidelidade e rastreabilidade

A conciliação não se limitou a contar nomes e anos. Foram comparados os contextos das 163 chamadas ao texto vigente: 161 permanecem iguais, e os outros dois contêm apenas a correção de bio-inspiradas para bioinspiradas e a explicitação da comparação entre erros dos modelos. Essas mudanças não alteram a atribuição às fontes. Os 61 arquivos de evidência diretamente vinculados foram localizados e receberam hashes na conciliação; os dez hashes de evidências declarados na consolidação de conteúdo anterior foram conferidos.

As 50 referências foram reconciliadas com o inventário. A única diferença textual em relação ao índice anterior é a pontuação da inicial de Zhang, já corrigida na v007. A parte de citações desta revisão não acrescentou ou retirou referências. As seis chamadas com localizadores que ficam fora de certos padrões automáticos não foram descartadas: continuam incluídas nas 163 chamadas conciliadas.

O erro de Timbó da v001 foi corrigido: o texto atual distingue acerto por tolerância absoluta de preço de acerto direcional. As versões bibliográficas, tarefas, métricas, população e limites dos demais contextos permanecem vinculados às decisões dirigidas anteriores. Isso permite reutilizar a evidência sem fingir nova leitura integral de todas as fontes nesta passagem.

Para a matriz, foi usada a conciliação atual das 170 células, não apenas a cópia histórica do primeiro reexame. A ordem dos dois estudos de Liu difere dos identificadores D17/D18; o cruzamento usa a linha Word documentada e a identidade da fonte. Duas decisões posteriores sobre Millea e Seddik também foram preservadas. Uma primeira tentativa do verificador contra o arquivo antigo detectou a divergência; o verificador foi corrigido para usar a conciliação posterior, sem restaurar códigos antigos ou alterar a matriz para fazê-lo passar.

Os 41 sinais de informação insuficiente permanecem com localizadores e limites. São classificações explícitas do alcance da leitura, não 41 erros que devam ser convertidos artificialmente em aprovação. As contagens da Tabela 1 e da Figura 1 correspondem à codificação vigente, que distingue evidência direta, secundária, informação insuficiente e não aplicabilidade.

## Três alterações incorporadas

| Local da base v007 | Antes | Depois | Motivo |
|---|---|---|---|
| T09 L5 C1, Tabela 5 | Busca GA por cenário ESN | Busca por AG por cenário ESN | Uniformiza a sigla genérica adotada no texto; não renomeia o pacote GA |
| P0422, seção 4.6 | Inicia diretamente em “O ajuste analítico…” | Acrescenta “A Tabela 5 apresenta a decomposição do custo computacional.” | Aproxima a remissão da discussão de custos |
| P0442, seção 4.8 | “Nos quatro testes, a hipótese…” | “Nos quatro testes apresentados na Tabela 6, a hipótese…” | Aproxima a remissão dos resultados inferenciais |

As duas chamadas já existiam em passagens anteriores. A alteração é um aperfeiçoamento de navegação e não foi apresentada como descoberta de ausência absoluta. Todos os valores, fórmulas, referências e ressalvas científicas foram preservados.

## Verificação final

- Edição por OOXML: somente `word/document.xml` mudou; todas as outras partes do ZIP/DOCX permanecem byte a byte iguais. Os três trechos modificados correspondem exatamente ao log.
- Reabertura: 551 parágrafos principais, 14 tabelas incluindo ficha e mesmas mídias/referências. Os 170 códigos da matriz permaneceram iguais.
- Reauditoria da cópia: 13 elementos tabulares sem falha nos controles aplicados; 50 siglas ordenadas e com uso; 56 ocorrências textuais de et al. com itálico; nenhuma das cinco omissões antigas reapareceu.
- Preservação de conteúdo: a adição dos números 5 e 6 é exclusivamente a dos rótulos das chamadas; não representa alteração de resultados numéricos.
- Visual: as 76 páginas do PDF vinculado à v007 foram abertas em 38 pares nesta passagem. Após os três ajustes, o Word local exportou a cópia em modo somente leitura e o rasterizador da skill documentos produziu os PNGs. As 74 páginas idênticas foram confirmadas por igualdade de pixels; páginas físicas 59 e 61 foram abertas e inspecionadas novamente, sem recorte ou sobreposição. As páginas seguintes e as páginas das legendas permaneceram iguais.
- Paginação: 76 páginas antes e depois, sem mudança das páginas dos títulos/legendas e, portanto, sem necessidade de recalcular listas para estas alterações.
- Controle de versões: antes de registrar e de entregar, conferir a vigente; uma promoção concorrente exigiria conciliação. O documento numerado final é informado em `entrega.json` após o registro.

Falhas intermediárias de scripts auxiliares — uma chave opcional ausente, o mapeamento histórico da matriz e um caminho duplicado no verificador pós-ajustes — foram corrigidas nos próprios verificadores e executadas novamente. Não foram suprimidas alterando o manuscrito para acomodar o teste.

## Alcance da conclusão

O levantamento atual das cinco skills está fechado, sem correção conhecida por aplicar nesta revisão. A matriz, o corpo, as chamadas, o perfil de quadros/tabelas e a apresentação final têm evidências rastreáveis. A revisão não cria aprovação acadêmica e não elimina limitações intrínsecas da pesquisa: preservação histórica incompleta, cadeia original do ajuste não reconstruída, buscas complementares, uma semente no DM, orçamentos distintos e ausência de ablações ou de demonstração de utilidade econômica. Essas limitações continuam no texto e delimitam suas conclusões.

Ficha catalográfica, data e assinaturas de aprovação permanecem nas etapas institucionais conforme decisões já registradas. Nenhum treinamento, busca genética ou teste DM foi reexecutado. Nenhum material foi enviado externamente.

Evidências desta passagem: `conciliacao_integral_v007.json`, `alteracoes_aplicadas.json`, `pos_ajustes/checks_quadros_tabelas.json`, `pos_ajustes/siglas.json`, `pos_ajustes/italicos.json`, `verificacao_visual.json` e `estado_final.json`. Os relatórios anteriores foram preservados.
