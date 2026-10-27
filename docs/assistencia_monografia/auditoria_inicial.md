# Auditoria inicial de coerência da monografia ESNAUTO

Em 23 de outubro de 2026, a revisão PETR4 já apresenta coerência substancial entre
objetivos, método, resultados e conclusão. Há correções de redação e lacunas de
comprovação documental que devem ser resolvidas antes da entrega. Esta auditoria
não altera os arquivos Word, não repete os experimentos e não atesta conformidade
visual, aprovação institucional ou leitura integral de todos os PDFs citados.

## Base e modo de localização

- Documento: `reports/monografia/MayconGarciaSilva_monografia_PETR4_revisao_orientador.docx`.
- SHA-256 observado: `b182bfe623d934644b7b2c462ed3adcbb6bae98e114819bb649bb40ece41f3dc`.
- Extração: `reports/assistencia_monografia/monografia_base_texto.txt`.
- Registro de identidade: `reports/assistencia_monografia/snapshot_fontes.json`.
- Método: leitura do conteúdo OOXML, incluindo tabelas, confronto com relatórios,
  resultados CSV, manifestos e trechos dos executores. Não foi renderizado um novo
  Word. Validações visuais anteriores são registros existentes, não verificações
  refeitas nesta auditoria.

`P0296`, por exemplo, significa o parágrafo 296 da extração XML, contando células
e parágrafos vazios. Não corresponde à página impressa. Localize também a seção e
a expressão citada. Os números deixam de ser estáveis quando o Word muda.

Prioridade alta indica risco de interpretação científica ou afirmação documental
sem suporte localizado. Prioridade média indica harmonização necessária. Os
diagnósticos abaixo distinguem divergência confirmada de questão pendente.

## Coerência dos objetivos

| Objetivo específico | Evidência no trabalho | Situação inicial |
|---|---|---|
| a — Consolidar literatura | Capítulo 2 e seção 3.8.3 | Texto e coleção presentes; harmonizar anos e recuperar rastreabilidade da seleção |
| b — Empregar série ajustada | Seção 3.2 e arquivos PETR4 | Série disponível; explicitar se o ajuste foi aplicado nesta pesquisa ou recebido pronto |
| c — Desenvolver ESNAUTO | Código em app e Scripts; seção 4.10 | Artefato presente; sem alegação de auditoria funcional integral nesta revisão |
| d — Investigar distribuições | Cinco ondas e tabelas 4 e 5 | Relatórios documentam 45 execuções; interpretação descritiva |
| e — Otimizar cinco hiperparâmetros | Quadro 2 e ga_engine.R | Codificação de 55 bits encontrada; corrigir resíduos de redação genérica |
| f — Comparar MAE, RMSE e R² | Capítulo 4 | Populações e blocos precisam permanecer identificados |
| g — Comparar modelos e custos; DM | Tabelas 4, 6 e 7 | Separação entre histórico, ajuste e rodada controlada está explícita |
| h — Analisar estabilidade e falha | Seção 4.4 | Caso extremo foi mantido; não generalizar estabilidade de poucas execuções |
| i — Documentar contribuições e limites | Capítulos 5 e 6 | Limites presentes; acervo histórico incompleto e documentos ausentes permanecem abertos |

## Achados e propostas

### A01 H1 usa não significância como critério de comparabilidade

**Prioridade alta. Divergência conceitual confirmada na redação.** Introdução,
P0296: a hipótese considera desempenho comparável a “ausência de diferença
estatisticamente significativa pelo teste de Diebold-Mariano”. O teste empregado
tem hipótese nula de igualdade de acurácia; uma não rejeição, sozinha, não é
demonstração de equivalência ou de não inferioridade. Isso não desfaz os quatro
resultados significativos documentados na rodada controlada.

**Redação proposta para revisão:**

> H1 — desempenho: no protocolo adotado, a ESN otimizada apresentará menor perda
> preditiva que os baselines LSTM e GRU. A comparação histórica será descritiva.
> Na execução controlada complementar, o apoio inferencial será avaliado pela
> diferença de acurácia no teste bilateral de Diebold–Mariano, em conjunto com a
> direção do diferencial médio de perda. A não rejeição da hipótese nula será
> interpretada como ausência de evidência suficiente de diferença, sem demonstrar
> equivalência entre os modelos.

Essa redação é uma proposta editorial, não comprova que o critério tenha sido
pré-registrado. Se o autor quiser manter uma hipótese de equivalência, será
necessário definir margem e procedimento próprios antes de uma nova análise.
Não criar uma nova análise retroativamente nesta revisão.

**Aceitação:** harmonizar H1 na introdução, seção 4.9, Tabela 8 e conclusão, sem
alterar resultados nem apresentar revisão de redação como pré-especificação.

Referência de interpretação: [documentação dos autores do forecast para dm.test](https://pkg.robjhyndman.com/forecast/reference/dm.test.html).

### A02 Identificação das versões bibliográficas permanece divergente

**Prioridade alta. Divergências documentais confirmadas.** A base reconstruída e
seu relatório já registram diferenças que não foram totalmente incorporadas:

| Fonte | Word vigente | Reconstrução local |
|---|---|---|
| Chen | Tabela 2, P0415: 2025; referência P1043: arXiv v2 e ano 2025 | Versão v2 identificada como 2026 |
| Cortesi | Tabela 2, P0421, e referência P1045: 2025 | Versão local identificada como 2026 |
| Duttilo e Gattone | Tabela 2, P0451: 2023b | Referência P1051 e base: encontro de 2022 |
| Soltani | Tabela 2, P0529, e referência P1072: publicação de 2023 | PDF local identificado como preprint de 2022 |

Fontes: `reports/bibliometria_reconstrucao/Resultados_e_texto_para_monografia.md`,
`base_reconstruida.json` e `artigos_reconstruidos.bib`.

**Correção proposta:** decidir e registrar a versão efetivamente consultada de cada
obra; conferir o PDF; ajustar as citações, rótulos da Tabela 2, referências e figuras
afetadas em conjunto. Se for escolhida uma publicação posterior em vez do preprint
local, obter e ler essa versão. Não substituir anos indiscriminadamente.

**Aceitação:** cada obra tem uma versão e um ano identificados consistentemente;
eventuais versões distintas ficam explicitadas, incluindo a data da consulta.

### A03 O texto afirma preservação de planilhas não localizadas

**Prioridade alta. Lacuna do acervo confirmado; existência histórica desconhecida.**
Seção 3.8.3, P0771: “foram mantidas no acervo da pesquisa as planilhas
methodi_ordinatio.xlsx e extracao_completa.xlsx”. A busca por arquivos XLS/XLSX no
projeto não localizou essas planilhas.

**Correção proposta:** localizar os arquivos originais e registrar sua procedência.
Enquanto isso, substituir a afirmação de disponibilidade por uma descrição fiel:

> A documentação do trabalho menciona planilhas de seleção e extração bibliográfica.
> Esses arquivos não foram localizados no acervo examinado nesta consolidação, o
> que limita a auditoria retrospectiva dessas etapas. A coleção reconstruída a
> partir dos PDFs não substitui os registros originais de busca e seleção.

**Aceitação:** os arquivos são recuperados com origem identificada ou a limitação
fica explícita. Não criar planilhas retrospectivas como se fossem registros de
23 de março de 2026.

### A04 A descrição de ausência de vazamento é mais ampla que o motor legado

**Prioridade alta. Diferença de implementação confirmada; impacto numérico não
recalculado.** Seção 3.2, P0629, afirma divisão rigorosa para evitar vazamento.
Em `app/utils/esn_core.R`, a construção de Yt em validação inclui alvo de índice
`treino + 1`. Em `app/utils/ga_engine.R`, a função de fitness contém a mesma
fronteira. Em `app/utils/data_prep.R`, `treina_testa` concatena treino e teste,
retirando o bloco de validação da propagação de estado. O executor controlado
`Scripts/diebold_mariano/02_esn_controlled.R` usa fronteira estrita e preserva a
continuidade cronológica. O próprio Word reconhece essa correção em P0956.

Esses trechos demonstram que os motores diferem; não identificam, sozinhos, a
versão exata que produziu cada uma das 45 execuções históricas. Não atribuir
automaticamente esse comportamento a todas elas nem afirmar magnitude de viés.

**Correção proposta:** restringir a garantia forte à execução controlada em que há
verificação explícita; descrever separadamente a divisão dos blocos e a fronteira
dos alvos no ajuste de Wout. Vincular os resultados históricos ao código arquivado
disponível e declarar a incerteza restante. Não corrigir o motor e reapresentar
novos resultados como antigos.

**Aceitação:** protocolo e código da rodada controlada ficam identificados;
declarações sobre ausência de vazamento nos históricos refletem apenas o que
pode ser demonstrado pelos registros preservados.

### A05 Título e descrição do Fator de Ajuste precisam de alinhamento

**Prioridade média. Questão de enquadramento e procedência, não erro de resultado
demonstrado.** O título nas páginas iniciais enfatiza “aplicação de fator de
correção”, mas o objetivo em P0276 enfatiza distribuições Win/W e otimização, e a
conclusão P1026 informa que não foi isolado efeito causal do fator. Em P0628, o
texto diz que a série foi submetida ao ajuste; os executores consultados recebem
arquivos já identificados como “com factor”.

**Correção proposta:** esclarecer quem produziu os arquivos ajustados e onde está
o procedimento que transforma os dados de origem. Se foram recebidos ajustados,
usar “utilizou-se a série previamente ajustada”, com atribuição da origem. Se o
ajuste foi aplicado pelo autor, apontar o script e os registros correspondentes.

Título alternativo para decisão editorial, sem alterar agora capa e folha de rosto:

> Redes neurais de estados de eco com inicialização probabilística e otimização
> genética para previsão do preço ajustado da PETR4

**Aceitação:** título e resumo representam o escopo efetivo e a procedência do
ajuste está clara. A escolha final do título fica com autor e orientador.

### A06 Persistem generalizações que o próprio trabalho restringe depois

**Prioridade média. Redação excessivamente ampla confirmada; apoio integral das
fontes ainda não auditado.** P0272 fala em maior velocidade e estabilidade “sem
perda relevante de capacidade representacional”; P0291 afirma que “séries
financeiras são reconhecidamente leptocúrticas”. A Tabela 3 apresenta curtose
de Fisher de −0,82 para preços ajustados. Preços, retornos e pesos do reservatório
são objetos diferentes, como o próprio P0292 já reconhece ao discutir Power
Function.

**Correção proposta:** delimitar a discussão de caudas ao tipo de variável e aos
estudos citados; não aplicar uma propriedade geral dos retornos à série de preços
utilizada sem cálculo correspondente. Apresentar eficiência e capacidade da ESN
como dependentes da tarefa, configuração e protocolo. Conferir as afirmações
atribuídas a Wang, Ribeiro, Millea e Soltani nos PDFs antes de reescrever o apoio.

**Aceitação:** cada afirmação técnica tem objeto definido e evidência localizada;
motivação experimental não se torna prova de adequação da distribuição dos pesos.

### A07 H4 menciona manutenção de diversidade sem medida correspondente

**Prioridade média. Falta de alinhamento entre hipótese e evidência.** P0299
propõe que LHS e cataclismo manterão diversidade; a Tabela 8, P0972–P0973, registra
integração sem ablação, e a conclusão preserva a limitação causal. A presença do
operador não mede, por si só, diversidade populacional.

**Correção proposta:** separar o objetivo de implementação da hipótese de efeito.
Se não houver séries de medidas de diversidade preservadas, registrar que H4 não
foi diretamente testada quanto a esse desfecho, além da ausência de atribuição
causal. Não gerar retrospectivamente métricas ausentes para as buscas históricas.

**Aceitação:** hipótese, Tabela 8 e conclusão distinguem implementação observada,
diversidade não medida e ganho causal não avaliado.

### A08 O método de ranqueamento bibliográfico necessita comprovação

**Prioridade média. Verificação pendente.** P0770 apresenta uma fórmula InOrdinatio
com divisão de citações por 100 e descreve FI como “fator de impacto (SJR)”. Sem
as planilhas e sem confronto completo com o método original, não é possível
atestar qual fórmula, indicador e valores foram efetivamente usados.

**Correção proposta:** confrontar o texto com Pagani et al. (2015), localizar a
planilha original, registrar o indicador bibliométrico empregado e sua data de
coleta. Se houve adaptação da fórmula ou do indicador, descrevê-la explicitamente
e explicar seu uso. Esta auditoria não declara uma fórmula substituta como a
efetivamente executada.

**Aceitação:** fórmula escrita, valores utilizados e ranqueamento são rastreáveis,
ou a limitação é declarada sem alegação de reprodução integral do método.

## Distinções corretas que devem ser preservadas

- P0753 e P0815–P0826 identificam o lote ilustrativo de 200 gerações e sua seleção
  por fitness, sem agregá-lo às 45 execuções.
- P0755–P0757 e P0927–P0956 separam o DM complementar dos resultados históricos.
- O registro `dm/dm_execution.json` contém `dm_executed: true`, enquanto o manifesto
  anterior contém `false`. São registros de etapas diferentes; não alterar o
  manifesto imutável para eliminar essa aparente divergência.
- P0897–P0916 e a conclusão separam o ajuste de aproximadamente 0,05 s das 37,9 h
  de busca. Não anunciar a razão de tempos como economia total do processo.
- P0773–P0777 distinguem revisão recente, fontes complementares, 34 documentos e
  24 listas de palavras-chave, preservando a origem reconstruída.
- P1024 mantém VALE3 como continuidade. O relatório da extensão registra que
  nenhuma das 12 ESNs superou a persistência em MAE; não omitir esse resultado
  em eventual retomada do segundo ativo.

## Próxima sequência editorial

Primeiro, corrigir H1 e delimitar as garantias de protocolo. Depois harmonizar
as versões bibliográficas e a disponibilidade das planilhas. Revisar introdução,
métodos, tabelas e conclusão com o roteiro em `plano_revisao.md`. Só depois
conferir a apresentação final contra o manual institucional e renderizar o Word.

Esta primeira auditoria não exige nova coleta nem treinamento. Questões que
dependem de arquivos ausentes devem permanecer identificadas até sua recuperação
ou até uma redação explícita da limitação.
