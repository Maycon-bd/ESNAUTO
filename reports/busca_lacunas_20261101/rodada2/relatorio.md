# Continuação da pesquisa das lacunas — rodada 2

Versão examinada: **v010**, SHA256 `1da5ea82344c177d75af723362017e3e558bbb127bd9995f7ec0cbd6964f81ed`.

A rodada anterior foi progresso: três respostas foram incorporadas na v010. Nesta rodada, foram ampliadas as evidências de 21 células em 13 fontes. Nenhuma recebeu nova classificação suficiente para editar o Word. As 38 células permanecem; a meta integral está ativa.

Houve nova leitura do texto integral de Jaeger (9 páginas), Ping (2 páginas), Seddik (11 páginas) e Sun (12 páginas); as demais leituras têm alcance delimitado abaixo. Não se apresenta busca lexical como leitura integral, nem detalhes de biblioteca como configuração histórica certificada.

## D15 / P4

**Alcance:** Nova leitura do texto das nove páginas da versão local Scholarpedia, revisão 196567, inclusive referências e identificação da revisão.

**Evidência:** O exemplo é um gerador de frequência, e as afirmações de desempenho são qualitativas. Não apresenta tabela nem números de contraste com LSTM/GRU/Transformer. A referência Evolino (2007) é listada, mas seus números não são reproduzidos aqui. Não transferir para Jaeger a comparação localizada em Millea.

**Decisão:** Mantido ?. Nenhuma evidência numérica qualificadora no texto integral consultado. O suplemento do gerador já foi lido na rodada anterior.

## D22 / P1, P4

**Alcance:** Nova leitura do texto das 11 páginas, inclusive método, tabelas 1–5, conclusões e referências.

**Evidência:** P1: pesos descritos como aleatórios/fixos; matriz de conectividade, tanh e ajuste de escala não individualizam lei dos elementos de Win/W. P4: LSTM aparece na revisão e nas referências 8/32, mas tabelas 2–5 comparam Lorenz e variantes ESN, sem arquitetura qualificadora. As tabelas 4 e 5 das páginas posteriores também foram verificadas no texto.

**Decisão:** Dois ? mantidos. Não apresentar resultados de obras citadas como se fossem números comparativos deste artigo.

## D16 / P1

**Alcance:** PDF 11–14; célula 11 do código público já arquivada; fontes oficiais de ReservoirPy em 19 etiquetas de lançamento/pré-lançamento até novembro de 2024.

**Evidência:** O notebook importa Reservoir de reservoirpy.nodes e não passa W/Win locais ao construtor. As 19 assinaturas conferidas usam W normal e Win Bernoulli simétrica (nomes antigos generate_internal_weights/generate_input_weights na série 0.3.0). Os respectivos geradores foram arquivados por etiqueta. Isso recupera o comportamento das versões públicas consultadas, mas não fixa o ambiente efetivamente usado por Kumar.

**Decisão:** Mantido ?. A inferência sobre os padrões públicos da biblioteca deve ficar identificada como condicional. Não atribuir distribuição uniforme ao modelo nem certificar a versão da execução. Próxima análise: distinguir documentação do exemplo público de prova da configuração histórica, conforme o protocolo já adotado.

## D26 / P1, P2, P3

**Alcance:** Nova leitura do texto das 12 páginas, incluindo referências. Fluxograma da Figura 2 (PDF 4, impressa 512) e configuração da página 6 (impressa 514) conferidos visualmente.

**Evidência:** P1: pesos descritos como aleatórios, sem família. P2: fixados 500 neurônios, raio 0.999 e esparsidade 0.02, sem procedimento de seleção. P3: coleta/limpeza aparece no fluxo, mas não há operação especificada; seleção do fechamento e partições não demonstram limpeza ou transformação. O fluxograma visível não contém operação adicional oculta na extração.

**Decisão:** Três ? mantidos após ampliar a conferência para todo o texto local. Não inventar operação a partir de diferenças numéricas entre tabelas.

## D21 / P3, P4, P5

**Alcance:** Nova leitura integral do texto das duas páginas, inclusive dez referências.

**Evidência:** Comunicação conceitual, sem dados identificados, preparação aplicada ou comparação numérica qualificadora. Os estudos listados nas referências são obras distintas; seus resultados não são resultados apresentados nesta comunicação.

**Decisão:** Três ? mantidos. Não há uma experiência incompleta do TCC a realizar para preencher estas células; faltam informações na obra examinada.

## D30 / P4

**Alcance:** PDF local 1, 2, 17 e 25; tabelas 3/4 da página 17 conferidas visualmente; HTML da editora. Fonte de apoio Pagliaro (2025): seção 6.1.4, PDF/impressa 13, e referências da página 46; busca textual nas 48 páginas para 72/90 seguidos de percentual.

**Evidência:** As tabelas 3 e 4 listam métricas e vantagens, sem resultados numéricos comparáveis. A referência 10 de Vishwas é Pagliaro; a menção a Hong como [10] no corpo é inconsistente com sua própria lista. Pagliaro atribui 72% a Google/horizonte de cinco dias e discute CNN em outra obra; não foi localizado 90% pela busca textual. Essa leitura não comprova contraste comum 72% versus 90%. Não é leitura integral nova de Pagliaro.

**Decisão:** Mantido ?. Retificar o localizador anterior: não existe uma Tabela 17 nesse ponto; são tabelas 3 e 4 na página 17. Preservar o relatório histórico e registrar esta retificação no novo relatório.

## D19 / P3, P5

**Alcance:** Páginas 1–6, 48–49 e passagens de 64–80; busca dirigida por normalização, reescala, Forex, moedas e negociação no texto. PDF oficial de Groningen consultado, com 90 páginas, correspondente à estrutura local.

**Evidência:** As alterações de feedback/matriz e o ruído de estado não são preparação da série. O resumo menciona Forex, mas o texto examinado e o sumário não identificam par de moedas/ativo de uma análise financeira. Um artigo posterior do mesmo autor, sobre Forex, é outra obra e não preenche automaticamente o campo da dissertação.

**Decisão:** Dois ? mantidos no escopo lido. Não declarar leitura integral das 90 páginas; persistem alternativas documentais a conferir.

## D02 / P1, P4

**Alcance:** Páginas 1–9 da prova local; busca externa por título/código.

**Evidência:** A descrição das cinco famílias e dos hiperparâmetros não individualiza sua geração em Win/W. A busca não forneceu um código do estudo com procedência demonstrada. Os scripts locais do TCC recebidos do orientador não têm ligação documental estabelecida com as execuções do artigo de Araújo.

**Decisão:** Dois ? mantidos. Não transportar a distribuição dos scripts do TCC para o artigo.

## D08 / P1

**Alcance:** Texto das páginas 7–8 e 12–14.

**Evidência:** Win/Wres/Wenc aleatórias e fixas; IS/SR escalonam as matrizes. Filtro gaussiano é aplicado à tensão, não define geração dos pesos.

**Decisão:** Mantido ?.

## D27 / P1

**Alcance:** Texto das páginas 1–5, incluindo método e passos SSA–ESN.

**Evidência:** Famílias normais e sinais ±1 pertencem a Q/beta/A da SSA. Passo 3 apenas manda gerar Win/W aleatoriamente; não vincula essas famílias aos pesos.

**Decisão:** Mantido ?.

## D34 / P1, P2

**Alcance:** Texto das páginas 6–9, algoritmo OMP e configuração.

**Evidência:** A matriz gaussiana é Phi de medição. OMP seleciona átomos e atualiza resíduos; a configuração fixa compressão de 50% e demais parâmetros. Não foi identificado procedimento de escolha dos hiperparâmetros da ESN nessas páginas.

**Decisão:** Dois ? mantidos.

## D24 / P3

**Alcance:** Busca em todo o texto por normalização, pré-processamento, escala, janelas e padronização; leitura das passagens recuperadas.

**Evidência:** Escalas de entradas/saídas são listadas como parâmetros; normalização sináptica descreve conexões da rede. Nenhuma dessas passagens individualiza uma operação aplicada de preparação temporal.

**Decisão:** Mantido ?. Busca lexical não é leitura integral nova.

## D03 / P4

**Alcance:** Busca por LSTM/GRU/Transformer em todo o PDF e por referência 187 no corpo; passagens das páginas 21 e 48.

**Evidência:** LSTM aparece no título da referência 187. A chamada no corpo integra uma enumeração de variantes IPSO, sem números de contraste com a arquitetura.

**Decisão:** Mantido ?. Não atribuir a esta revisão uma tabela numérica da obra referenciada.

## Fontes complementares preservadas

- Código oficial de ReservoirPy em 19 etiquetas até novembro de 2024, com geradores e hashes: `suplementos/historico_reservoirpy/`. Não é uma cópia do ambiente original de Kumar.
- Pagliaro (2025), DOI 10.3390/electronics14091721, PDF da editora e hash em `suplementos/Pagliaro_procedencia.json`. Apoio ao rastreio da referência 10 de Vishwas; não é um novo item do portfólio.
- Imagens de conferência: `visuais/Sun_p4.png`, `visuais/Sun_p6.png`, `visuais/Vishwas_p17.png` e `visuais/Pagliaro_p13.png`.

## O que ainda impede preencher cada campo

P1 exige lei ligada a Win/W, não apenas a palavra aleatório. P2 exige como os valores foram selecionados. P3 exige operação de preparação aplicada. P4 exige comparação quantitativa identificável com as arquiteturas previstas pelo critério; a mera existência de LSTM na bibliografia não atende. P5 exige mercado e ativo ligados à análise.

Se a publicação não especifica a informação, preencher com um resultado de outra obra ou inventar um experimento alteraria a pesquisa. A indisponibilidade deve permanecer documentada. A leitura integral nova de Sun e Ping restringe a lacuna à informação não fornecida no texto, sem provar inexistência universal de material complementar.

| Fonte | Campos ainda insuficientes |
|---|---|
| Abebe e Goshu (2024) | P3 |
| Araújo et al. (2025) | P1, P4 |
| Behera, Nayak e Kumar (2023) | P1, P4 |
| Costa e Lunkes (2025) | P4 |
| Deng et al. (2022) | P1 |
| Ecer et al. (2020) | P4 |
| Hariharan, Suresh e Chandrasekar (2025) | P4 |
| Jaeger (2007) | P4 |
| Kumar (2025) | P1 |
| Liu, Lin e Rojas (2025) | P4 |
| Millea (2014) | P3, P5 |
| Ping (2023) | P3, P4, P5 |
| Seddik, Routaib e Elhaddadi (2023) | P1, P4 |
| Sharma et al. (2025) | P1, P4 |
| Soltani, Benmohamed e Ltifi (2022) | P1, P3, P4, P5 |
| Sun et al. (2021) | P1, P2, P3 |
| Tian e Pei (2024) | P1 |
| Timbó et al. (2016) | P4 |
| Ribeiro et al. (2021) | P4 |
| Vishwas, Usha e Sangeetha (2025) | P1, P4 |
| Wang, Bu e Huang (2025) | P1, P2 |
| Zhang et al. (2021) | P1, P2, P4 |

## Continuidade

Priorizar conferência integral dos textos ainda lidos parcialmente e respectivas figuras/suplementos; começar pelos resultados completos de Araújo, Timbó e Zhang. Jaeger, Seddik, Ping e Sun tiveram texto integral lido nesta rodada; as células neles ainda não se fecham. Em Kumar, a lei nos padrões públicos consultados foi recuperada, mas o ambiente efetivamente usado não foi identificado: manter essa distinção na decisão. Não alterar os critérios para eliminar sinais. Não repetir experimentos. Consultar a vigente antes de qualquer incorporação.

A auditoria não depende de confirmação intermediária do autor. Não há processo de download/exportação ainda em execução. Não foi estabelecido bloqueio repetido da meta integral.
