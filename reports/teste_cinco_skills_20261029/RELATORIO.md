# Teste das cinco skills na monografia ESNAUTO

As cinco skills foram executadas sobre a versão editorial **v001**, resolvida pelo registro oficial e conferida por SHA256. O teste identificou diferenças de apresentação e de fidelidade de citações; não representa aprovação integral da monografia nem ausência de plágio.

Esta execução fez auditorias e produziu propostas concretas. Não editou o Word, não criou nova versão editorial, não refez experimentos e não modificou os resultados existentes. O teste de escrita foi entregue como trecho pronto com rastreabilidade. A geração de uma cópia Word de auditoria sem edição foi dispensada conforme a regra atual de controle de versões; o PDF de leitura e as extrações são evidências auxiliares.

## Identidade examinada

- Versão: v001.
- Documento: `reports/monografia/versoes/v001/MayconGarciaSilva_monografia_v001.docx`.
- SHA256: `2b233d00b880f0f8727baf587828419b591f45428b409be5ec680932d09805aa`.
- Critério de seleção: `Scripts/versao_monografia.py atual --json`, seguido de hash direto. Nenhuma escolha por data, nome de arquivo ou indicação histórica da skill.
- Data da execução: 29/10/2026, horário de Brasília.
- Guia: FASOFT UniRV, primeira edição, v.1.0.2, PDF de 76 páginas. Páginas de guia citadas abaixo são posições físicas no PDF.
- Foram examinados 555 parágrafos principais e 470 parágrafos de células, totalizando 1.025 registros, 12 elementos tabulares acadêmicos, 57 entradas da lista de siglas e 50 referências.
- `P0194` identifica o parágrafo de índice zero-based na extração desta v001; não é página. `T01 L3 C3 P1` é tabela de índice 1, terceira linha, terceira coluna e primeiro parágrafo da célula. T00 é a ficha catalográfica e foi excluída da auditoria tabular acadêmica.

## Execução por skill

| Skill | Trabalho efetivamente executado | Resultado e limite |
|---|---|---|
| quadro-tabela-validator-docx | Classificação e propriedades dos 7 elementos Tabela e 5 elementos Quadro; títulos, fontes, dimensões, bordas de células, chamadas e listas; inspeção visual dos 12 elementos | Tipografia e contornos principais conformes; faltam divisórias de cabeçalho nas 7 tabelas e chamadas nominais para 4 elementos |
| ingles-italico-checker-docx | Varredura assistida por candidatos em parágrafos/células, propriedades diretas/herdadas e consulta à lista oficial da Secom | Cinco omissões claras nos candidatos; Ridge requer uniformização editorial; termos incorporados e abstract foram diferenciados |
| siglas-checker-docx | Inventário das 57 entradas, usos na parte textual em ordem de leitura, primeiras menções, repetições, títulos e candidatos não listados | Lista ordenada e com usos localizados; há expansões incompletas/redundantes e candidatos que exigem decisão sem normalização indiscriminada |
| tcc-writer-docx | Revisão delimitada do P0194 da seção 2.1, com leitura da fonte, confronto com contexto e proposta de 357 caracteres | Trecho pronto, rastreável, não incorporado ao Word; sem expansão do escopo nem criação de resultados |
| tcc-citation-checker-docx | Novo cruzamento formal das referências e comparação de afirmações sobre Timbó com o PDF original de 11 páginas | 184 ocorrências autor–ano reconhecidas, sem referência correspondente ausente; a amostra conceitual revela confusão de métrica e atribuições sem apoio localizado |

“Executada” significa que o procedimento foi aplicado ao material real dentro do alcance declarado. Não significa que todas as correções tenham sido incorporadas, que o salvamento de um Word modificado tenha sido testado ou que as 50 obras tenham recebido leitura integral nesta execução.

## Quadros e tabelas

Os 12 elementos têm título acima em 10 pt, justificado e simples, sem ponto-final; cabeçalho em 11 pt e negrito; corpo em 11 pt e simples; fonte dos dados abaixo em 10 pt, simples, com ano e ponto-final; mínimo de três linhas e duas colunas. Os cinco quadros têm 16 cm, laterais fechadas e corpo sem grade interna. As sete tabelas têm laterais abertas e corpo sem grade interna. Esses resultados foram conferidos por propriedades de células, não apenas por `tblBorders`, que estão anuladas no nível da tabela.

| Elemento | Localização do título | Página física do Word exportado | Tipo e finalidade | Achado |
|---|---|---|---|---|
| Tabela 1 | P0272 | 33 | Quantificação de cobertura com síntese textual; tabela adequada | Sem divisórias verticais no cabeçalho |
| Quadro 1 | P0275 | 34–35 | Matriz descritiva de cobertura de dimensões por estudo; quadro adequado | Cabeçalho sem divisórias verticais; ambiguidade do modelo de quadro registrada |
| Tabela 2 | P0318 | 42 | Medidas estatísticas da série; tabela adequada | Sem divisórias verticais no cabeçalho |
| Quadro 2 | P0323 | 43 | Organização das ondas; contagens não alteram a finalidade descritiva | Ambiguidade de cabeçalho registrada |
| Quadro 3 | P0327 | 44 | Descrição da codificação e papel dos hiperparâmetros | Ambiguidade de cabeçalho registrada |
| Quadro 4 | P0344 | 47 | Desenho experimental com objetivos e blocos | Ambiguidade de cabeçalho registrada |
| Tabela 3 | P0392 | 54 | Comparação numérica de modelos | Sem divisórias verticais no cabeçalho; há chamada posterior, não ausência de chamada |
| Tabela 4 | P0411 | 57 | Configurações e métricas selecionadas | Sem divisórias de cabeçalho e sem chamada nominal no corpo |
| Tabela 5 | P0426 | 59 | Durações e interpretação do custo | Sem divisórias de cabeçalho e sem chamada nominal no corpo |
| Tabela 6 | P0449 | 61 | Estatísticas e p-valores da rodada controlada | Sem divisórias de cabeçalho e sem chamada nominal no corpo |
| Quadro 5 | P0453 | 62 | Síntese qualitativa da avaliação das hipóteses | Sem chamada nominal no corpo; ambiguidade de cabeçalho registrada |
| Tabela 7 | P0459 | 63 | Comparação numérica com estudos relacionados | Sem divisórias verticais no cabeçalho |

O modelo de tabela do guia, PDF 53, mostra separações verticais somente no cabeçalho. **Proposta:** acrescentá-las nas sete tabelas, preservando laterais externas abertas e corpo sem grade. No quadro, PDF 54, a anotação pede linhas internas no cabeçalho, mas o desenho não as mostra claramente: não transformar essa ambiguidade em ordem para criar grade completa. Não há razão para converter os quadros em tabelas contando células com números.

As chamadas foram buscadas no corpo, distinguindo título e entrada da lista pré-textual. As quatro ausências foram confirmadas na leitura do texto, incluindo variantes plurais de “tabelas/quadros”. Propostas de inserção, sem substituir os parágrafos já existentes:

- Seção 4.3, antes de Tabela 4: “A Tabela 4 reúne configurações selecionadas das cinco ondas experimentais.”
- Seção 4.6, antes de Tabela 5: “A Tabela 5 distingue os tempos de ajuste, treinamento e busca documentados.”
- Seção 4.8, antes de Tabela 6: “A Tabela 6 apresenta os quatro contrastes da execução controlada complementar.”
- Seção 4.9, antes de Quadro 5: “O Quadro 5 sintetiza a avaliação das cinco hipóteses.”

Essas frases remetem ao conteúdo já presente, sem novo dado ou nova inferência. A chamada anterior é recomendação de leitura; a exigência confirmada no PDF 32 é referência no texto e proximidade. A chamada posterior da Tabela 3 não foi tratada como erro automático.

Listas próprias de Quadros e Tabelas estão presentes, com 5 e 7 entradas e páginas que correspondem à exportação examinada. Não foram identificadas siglas nos 12 títulos. A recomendação de alinhamento dos números no modelo não foi convertida em obrigação de alterar todas as células; o guia não fixa largura individual de colunas nem espessura universal de traço.

Detalhes reproduzíveis: `quadros_tabelas.json` e `checks_quadros_tabelas.json`.

## Estrangeirismos e itálico

Foram registradas 192 ocorrências candidatas entre os termos procurados, com contexto e estado tipográfico em `italicos.json`. O inventário cobre também as células; a varredura não é garantia de detecção semântica de todo estrangeirismo possível. Não há notas de rodapé, notas de fim ou caixas de texto no documento que tenham ficado fora desse escopo por esses mecanismos.

| Local | Como está | Proposta | Base/decisão |
|---|---|---|---|
| P0213 | Scale-Free sem itálico | Aplicar itálico à expressão | Expressão estrangeira; seção 7.2 do guia |
| P0213 | Small-World sem itálico | Aplicar itálico à expressão | Mesmo critério; a lista pré-textual já usa itálico |
| P0237 | Power Function sem itálico | Aplicar itálico à expressão | Nome estrangeiro da distribuição; outros usos no documento já têm destaque |
| P0240 | input scaling sem itálico | Aplicar itálico à expressão completa | A exceção de “input” isolado não resolve a expressão técnica completa |
| T01 L3 C3 P1 | grid search sem itálico | Aplicar itálico à expressão completa | Expressão técnica estrangeira, fora da lista de exceções consultada |

As 83 ocorrências de `et al.` encontradas na parte textual e nas células estão em itálico. Esse número não inclui a lista de referências como se fosse prosa narrativa. O abstract em inglês não foi marcado integralmente como erro de estrangeirismo. Nomes de software, autores, comandos e identificadores não foram normalizados por origem linguística.

A consulta à [lista oficial da Secom](https://www12.senado.leg.br/manualdecomunicacao/verbetes-acessorio/estrangeirismos-grafados-sem-italico-ou-aspas), em 29/10/2026, confirmou exceções relevantes como feedback, hardware, software e script. Seus usos sem itálico não foram contados como omissões. Formas plurais foram avaliadas no contexto, sem inventar mudança de classe pela flexão. A regra institucional específica para expressões latinas prevalece quando diverge da lista geral do Senado.

Ridge apresenta variação de tratamento entre corpo, células e referências explicativas. A capitalização e a denominação do método exigem decisão editorial consistente; não foi aplicado itálico automaticamente a todos os usos como se houvesse omissão normativa indiscutível. A tabela de ocorrências permite localizar os usos para uniformização posterior.

## Siglas

Há 57 entradas, todas com pelo menos um uso localizado na parte textual/células e em ordem alfabética. O limiar específico do guia, PDF 24, é **mais de dez itens**, portanto a lista é exigida nesse caso. Não se aplicou o limiar inventado de dez itens da versão anterior da skill. A nota geral de listas opcionais não foi apagada: foi distinguida da regra específica para siglas.

Primeiras ocorrências foram examinadas a partir da Introdução, incluindo as tabelas em sua posição no documento. Resumo, abstract e lista pré-textual não substituíram a definição no texto. A matriz de todas as entradas e seus usos está em `siglas.json` e no relatório `siglas_detalhadas.md`.

| Local | Achado | Proposta/limite |
|---|---|---|
| P0191 | HQNN aparece após “redes quântico-híbridas”, com expansão abreviada em relação à própria lista | Empregar a expansão completa “redes neurais quântico-híbridas (HQNN)”, conferindo a denominação na obra citada antes de uma alteração bibliográfica |
| P0217 | CS-ESN é associado somente a “Compressed Sensing”, que expande CS, não o composto inteiro | Usar a forma completa já registrada na lista, mantendo o significado do modelo e conferindo com a fonte |
| P0197 | SVM é reapresentada com extenso depois de sua introdução no P0191 | Propor apenas SVM nesse segundo uso; conferir o fluxo do parágrafo |
| P0200 | LSTM e GRU reaparecem por extenso após P0176 | Tratar como reapresentação explicativa; propor redução quando não houver necessidade conceitual. Não executar substituição global |
| P0208 | AG reaparece como “Algoritmos Genéticos (AG)” depois de P0176 | Propor AG, preservando concordância e a atribuição da frase |
| P0210 | RC volta a ser definida após P0174 | Propor “Computação de Reservatório” ou RC conforme a função explicativa, sem tratar toda menção do conceito como erro |
| P0257 | SSA é reapresentada após P0224 | Propor uso da sigla sem repetir o extenso se não necessário |
| P0206 e passagens sobre mercados | JPX, NASDAQ, FTSE, SSE, NYSE, DJIA/DJI e ISEQ precisam de tratamento próprio | Identificar se nome oficial, índice, bolsa ou abreviação; propor explicação e entrada pertinente. Não inventar expansões por iniciais |
| P0367 | FI é definido como indicador de impacto no parágrafo, mas não está na lista | Propor entrada coerente com o indicador efetivamente usado; não confundir fator de impacto com SJR sem comprovação |
| T01 L6 C3 P1 | EUA aparece na tabela e não está na lista | Propor “Estados Unidos” na célula ou inclusão/definição de EUA conforme a convenção adotada |
| T09 L5 C1 P1 | “Busca GA por cenário ESN” usa GA no sentido genérico, enquanto o texto adota AG | Propor “Busca por AG em cada cenário ESN”; diferenciar do nome do pacote GA mencionado no ambiente computacional |

H1–H5, P1–P5, identificadores de critérios, nomes de pacotes GA/MASS, tickers PETR4/VALE3 e nomes do artefato ESNAUTO/JANUS não foram classificados automaticamente como siglas ausentes. LESN foi mantido para conferência da notação de perda na fórmula, sem inserção cega na lista. Os títulos dos 12 quadros/tabelas não contêm as siglas listadas.

O exame não alterou grafias consagradas nem impôs tradução dupla a todo termo estrangeiro. A função da repetição do extenso foi considerada antes de recomendar redução.

## Escrita e fidelidade de citações

A referência de Timbó está presente em P0549 com autores, ano, periódico, páginas 21–31 e DOI. O novo cruzamento formal reconheceu 184 ocorrências autor–ano, todas com referência correspondente nesses padrões. Isso **não comprova** que as respectivas afirmações são sustentadas pelas obras.

Para testar fidelidade conceitual, foi lido o conteúdo textual das 11 páginas do PDF original de Timbó e examinadas visualmente a página inicial e a página 8. As páginas 6–7 foram relidas para conferir método e avaliação. A codificação defeituosa do título extraído foi resolvida pela imagem, sem reconstrução por suposição.

| Afirmação de P0194 | Classificação | Confronto com a fonte |
|---|---|---|
| Aplicação de regressão linear à PETR4 | Condizente | Metodologia, PDF 6, impressa 26: regressão linear múltipla; resultados aplicados à PETR4 |
| Seleção com apoio de correlação de Pearson | Condizente | Metodologia, PDF 5, impressa 25: análise de correlação e coeficiente de determinação para seleção de variáveis |
| “taxa de acerto direcional” | Não sustentada/contraditória com a definição operacional examinada | Resultados, PDF 8, impressa 28: o acerto é definido por desvio absoluto máximo de 0,50 entre previsão e fechamento, não pelo sinal da variação |
| Uma das primeiras referências brasileiras | Não sustentada como primazia na obra examinada | A existência do artigo em 2016 não demonstra prioridade histórica frente ao restante da literatura |
| Os autores reconhecem que o método não é adaptativo e não captura dependências longas | Apoio não localizado na fonte lida | Não manter essa atribuição como conclusão dos autores sem passagem específica; isso não prova que a limitação técnica em si seja falsa |

O P0309 usa Timbó para contextualizar a escolha de PETR4 e sua alta liquidez. A fonte sustenta o uso do ativo e sua relação com estudos anteriores, mas não fornece, nas passagens examinadas, uma medição de liquidez que fundamente toda a afirmação. A alegação deve receber fonte apropriada ou ser delimitada. A leitura do artigo também revelou inconsistências internas de datas e contagens amostrais; o teste não tentou “corrigi-las” nem incorporou esses números à monografia.

**Proposta da tcc-writer-docx para substituir P0194, seção 2.1:**

> Timbó et al. (2016) aplicaram regressão linear múltipla à previsão do fechamento da PETR4, selecionando variáveis com apoio da correlação de Pearson. O estudo avaliou o acerto por uma tolerância absoluta de 0,50 entre o valor previsto e o observado, e não pelo sinal da variação do preço. Esse critério deve ser distinguido de uma taxa de acerto direcional.

O trecho tem **357 caracteres com espaços**, dentro da preferência de 700 caracteres herdada da skill; esse limite não foi apresentado como exigência do guia. A passagem preserva a citação existente e remove primazia e reconhecimento de limitações sem apoio localizado. A distinção final entre tolerância e direção é explicação metodológica desta revisão, não uma frase atribuída literalmente ao artigo.

Rastreabilidade: fonte, autores, ano, DOI, SHA256, seções, páginas e trecho literal curto estão em `fonte_timbo.json` e `teste_writer.json`. Conferiram-se a delimitação da Introdução, a seção 2.1, o uso de Timbó em 3.2 e a discussão/conclusão relacionadas à validade do trabalho. A proposta não transfere métricas de Timbó para ESNAUTO e não muda hipóteses nem interpreta os três blocos experimentais como um único protocolo.

Essa é uma amostra real de teste da skill de fidelidade, não uma segunda auditoria integral das 50 obras. Os 25 achados do parecer anterior continuam históricos e não foram automaticamente recontados como descobertas desta execução. O presente teste não os declara resolvidos.

## Verificação visual e preservação

O Word local abriu a v001 em **somente leitura**, exportou PDF e fechou sem salvar. A primeira tentativa de acesso COM no ambiente restrito recebeu acesso negado; a exportação autorizada fora dessa restrição funcionou. A rasterização usou `render_docx.py` da skill de documentos, com a conversão substituída apenas pelo PDF exportado pelo Word, pois o fluxo local disponível já usa essa alternativa.

Foram geradas 75 páginas. Nesta execução, foram inspecionadas visualmente as páginas físicas **12, 13, 33–38, 42–44, 47, 54, 57, 59, 61–63**. A inspeção cobriu os 12 elementos tabulares, incluindo a continuação do Quadro 1, e uma parte das listas. Não se declara nova inspeção visual integral das 75 páginas. Nos elementos examinados não foram observados cortes ou sobreposições que impeçam a leitura; as diferenças de modelo e chamadas permanecem registradas.

O PDF exportado tem SHA256 `97cb5c90d8080cc112635d39b968eaa5e1bb6705e31b18715e7d654eb5a4c6f0`. Não se exige que seja idêntico ao PDF histórico, pois exportações podem alterar metadados e composição. A identidade autoritativa da base é o SHA256 do DOCX.

O validador histórico `auditar_base_monografia.py --check` falhou por rejeitar o caminho absoluto do guia em Downloads. O snapshot não foi renovado nem modificado para contornar isso. A seleção e integridade da base foram verificadas pelo controle de versões vigente e por hash direto. Os scripts de auditoria novos só leem a monografia e escrevem evidências nesta pasta.

## Limites e encaminhamento

- As cinco skills foram exercitadas; não houve teste de salvamento de um DOCX modificado ou edição de Google Docs.
- Escrita e citações foram testadas com proposta delimitada e fonte integral; as demais obras não receberam nova leitura integral nesta execução.
- A varredura lexical auxilia a localizar estrangeirismos, mas não certifica que todas as palavras estrangeiras foram encontradas.
- A ausência de referências faltantes nos padrões reconhecidos não elimina erros de atribuição ou generalizações científicas.
- As ambiguidades do guia foram preservadas como ambiguidades; não se inventou regra para fechar a grade do corpo dos quadros.
- A v001 permanece a base editorial. Incorporar as propostas exige uma revisão registrada pelo fluxo `preparar` → edição/verificação → `registrar --base`, com reconciliação se outro chat avançar a base.

Os arquivos `estado_testes.json`, `identidade_e_cobertura.json` e `manifesto_evidencias.json` registram alcance, hashes e verificações. O agendamento único deve ser encerrado após esta entrega, pois as cinco execuções estão concluídas.
