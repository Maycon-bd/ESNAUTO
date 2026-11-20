# Andamento da correção do parecer

Objetivo ativo: resolver os 25 achados F01–F25 e os riscos R01–R13 do parecer de
28/10/2026, aplicando correções à monografia e verificando as fontes e a apresentação.
O objetivo não está concluído. Não reduzir o escopo aos pontos já editados.

## Estado mais recente: matriz incorporada

A etapa mais recente é a recodificação dos 34 documentos/170 células, incorporada
à cópia de trabalho. O construtor contém 62 parágrafos do corpo, 187 células/
parágrafos de tabelas e uma imagem alterados. Estado/hash em estado_matriz170.json.
A vigente registrada continua v001; nenhuma promoção foi feita. As etapas e PDFs
anteriores abaixo são históricos. O objetivo completo ainda não foi concluído.

## Base e cópia de trabalho

- Base do parecer e do controle: v001, SHA256
  `2b233d00b880f0f8727baf587828419b591f45428b409be5ec680932d09805aa`.
- Cópia: `reports/monografia/trabalho/revisao_parecer_integridade.docx`.
- Origem: arquivo adjacente `.docx.origem.json`, preparado pelo controle.
- Script cumulativo desta etapa: `Scripts/revisar_parecer_integridade_lote1.py`.
  Recria a cópia a partir de v001 e aplica as alterações de seu dicionário. Antes de
  acrescentar outro script ou editar manualmente a cópia, considerar que executá-lo
  novamente apaga alterações não incorporadas ao script. Não executar sobre outra base.
- Registro antes/depois/evidência/hash: `lote1_alteracoes.json`, 22 parágrafos.
- Nenhuma promoção foi feita. A vigente permanece v001 enquanto o rascunho passa
  pela revisão completa. Conferir o registro de versão a cada retomada; se outra
  revisão tiver sido promovida, comparar antes de continuar.

## O que foi feito

Primeira aplicação: 13 parágrafos de revisão de literatura corrigidos, cobrindo
atribuições Costa/Lunkes, Liu H., Sharma, Seddik, Sun, Liu B., Millea, estabilidade
da ESN e exclusão indevida de modelos lineares. O contexto pertinente das extrações
primárias foi relido. Foi corrigido o localizador de Millea: seção 3.3 nas páginas
físicas 28–31, não 24–26 como constava no parecer inicial. Não se declarou leitura
integral das obras nesta etapa.

Segunda aplicação cumulativa: 22 parágrafos. Acrescentou esclarecimento editorial
da H1, limites de vazamento/preservação de matrizes, atribuição do fitness 40/60 a
Araújo e declaração da indisponibilidade das duas planilhas. A H1 revisada não deve
ser apresentada como pré-registro retrospectivo. A implementação controlada foi
consultada em `Scripts/diebold_mariano/02_esn_controlled.R`, sem execução científica.

Os snapshots, tabelas, referências, imagens e demais partes ZIP foram preservados
byte a byte nesta etapa; apenas os parágrafos listados de document.xml mudaram.
Parágrafos novos têm até 700 caracteres. O algoritmo conserva segmentos iguais e
suas propriedades, mas a formatação de termos introduzidos precisa de revisão.
Não foi usado `paragraph.text` para apagar runs, campos ou vínculos.

## Renderização e verificações

A primeira exportação pelo Word foi bloqueada pelo sandbox (COM 80070005).
A execução escalada foi autorizada automaticamente e exportou `lote1.pdf`, 75
páginas. Esse PDF corresponde à primeira aplicação de 13 parágrafos e **não é a
cópia final nem a aplicação atual de 22 parágrafos**.

Foram abertas as imagens físicas 20–23 da primeira aplicação. Sem recortes ou
sobreposição nessas páginas, mas termos estrangeiros novos como Support Vector
Machine e Large Language Models ainda requerem itálico. Foram rasterizadas 20–32;
essas imagens não equivalem a inspeção integral. A lista de páginas com texto
alterado está em `lote1_paginas_alteradas.json`; inclui deslocamentos até 35 e
diferença na p. 70, a investigar (exportador ajusta recuos em memória).

Foi concluída nova exportação da aplicação cumulativa de 22 parágrafos para
`trabalho_atual.pdf`, com 76 páginas. A verificação visual desta exportação ainda
está pendente. `exportacao_atual.json` registra os hashes do PDF e Word relacionados;
conferi-los novamente após qualquer edição. A paginação cresceu e listas/sumário
precisam ser atualizados na etapa final.
O script de exportação existente é `Scripts/exportar_padronizacao_fasoft.ps1`.
Não passar `-AtualizarListas` antes de decidir e verificar suas alterações, pois
essa opção salva o Word; sem ela, a exportação é sem gravação do DOCX.

## Trabalho que permanece

1. Continuar a revisão de todas as atribuições, inclusive F04/F05/F12/F14/F16/F17,
   e verificar os 34 PDFs com critérios uniformes. Não usar o fato de uma fonte ter
   sido corrigida em um parágrafo como prova de todos os seus outros usos.
2. Fechar 170 células P1–P5 com fonte/localizador/regra. Atualizar Tabela 1, Quadro 1,
   Figura 1 e conclusões dependentes. A matriz original não é confiável. Não criar
   novos totais de cobertura sem conferência.
3. Resolver versões e metadados (Abebe/Goshu, Soltani preprint 2022 versus final
   2023, prova Araújo), referências sem chamadas e fontes externas pendentes. Tentar
   localizar Cardoso RBras 2022a, Pagani e Eshelman; se impossível, limitar/remover
   alegações sem comprovação e registrar o material que o autor pode fornecer.
4. Harmonizar F18 por inteiro: P0368 já declara ausência das planilhas, mas
   P0365–P0367 ainda afirmam busca executada e fórmula não verificada. Resolver a
   contradição com descrição fiel do que é documentado, sem fingir execução nem
   reconstruir um registro original. Fonte de busca pode ser histórica declarada.
5. R03: investigar cadeia da série ajustada; não atribuir aplicação ao autor sem
   comprovação. Resumo/abstract/conclusão e P0311–P0312 continuam dependentes disso.
6. R07/R08: H4 e H5, sua avaliação e conclusão ainda precisam distinguir diversidade
   não medida, ausência de ablação e dispersão entre configurações versus sementes.
7. Rever comparação Cardoso2022a, delimitação da contribuição própria e título.
   Preservar os três protocolos e números sem repetir GA/treinos/DM.
8. Revisar itálicos/siglas dos parágrafos alterados e conformidade com o guia,
   atualizar listas/campos conforme necessário, renderizar e inspecionar a versão
   final, conferir todas as tabelas/referências e os invariantes experimentais.
9. Fechar matriz de resolução dos 25 achados e 13 riscos com estados verificáveis.
   Registrar a revisão pelo controle (`registrar --base` conferida) somente após
   verificação; entregar Word, evidências e pendências específicas ao autor.

Recursos: Python e Node empacotados em
`C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/`.
Poppler disponível em `native/poppler/Library/bin/pdftoppm.exe`.
Usar as skills monografia-esnauto, tcc-citation-checker-docx, tcc-writer-docx e
documents. As referências dessas skills já foram lidas nesta retomada. Não há
autorização/instrução de subagentes e nenhum foi criado.


## Retomada: 46 trechos e conferência seletiva

O construtor cumulativo contém agora 45 parágrafos do corpo e uma célula de tabela
alterados (46 registros). O SHA e os antes/depois estão em lote1_alteracoes.json.
Nenhuma versão foi promovida: v001 continua sendo a base registrada. Há rascunho
mais adiantado, que deve ser retomado por este construtor com origem v001.

Foram corrigidos Wang W., Hariharan, Tian, Deng e Ecer/Behera: comparações dependem
do índice/métrica/tarefa; ligações entre grupos continuam presentes; os números
LSTM da Tabela 6 de Deng vêm da referência [36]. Nelson não é apresentado como
prioridade histórica absoluta, nem a cauda dos retornos valida pesos GED. Duttilo
P0234 passou a distinguir a conferência 2022 da tese 2023 e critérios de informação
de testes de normalidade. A tese continua referenciada e usada no quadro, a conferir.

Soltani foi reconciliado com o preprint v1 de 04/08/2022, DOI
10.21203/rs.3.rs-1909702/v1: chamadas do corpo, referência P0545 e linha do quadro
corrigidas. Não há mais Soltani 2023 no texto visível do DOCX. Conferir gráficos
por ano e demais derivados; as marcas P1–P5 ainda não foram recodificadas.

F18 foi harmonizado em P0248, título P0364 e sumário P0152 e P0365–P0369. A coleção
é descrita como material recuperado; os números 41/59 são relato histórico não
verificado, não execução comprovada. A fórmula InOrdinatio não verificada foi
retirada; não se fabricaram pontuações. Referência Pagani permanece como método
indicado na documentação anterior, sem alegar ordenação recuperada.

Metadados Abebe/Goshu e Behera/Nayak/Kumar corrigidos pelas primeiras páginas.
A prova de Araújo ainda requer decisão bibliográfica verificada.

A substituição textual deixou itálicos e até um índice subscrito em fragmentos
portugueses novos. Foram corrigidos apenas os parágrafos reescritos com base no
Guia PDF 71: et al. e expressões inglesas em itálico; siglas/nomes próprios em romano;
Win/Wout e λmax mantêm os índices matemáticos semanticamente corretos. Registro
em formatacao_trechos_reescritos.json. Não foi refeita a formatação do documento
inteiro. O construtor passou a recusar execução se a vigente mudar ou se o rascunho
for modificado fora dele, para evitar perder intervenções de outra etapa.

Exportação atual: revisao_46_trechos.pdf, 76 páginas, hashes em
exportacao_46_trechos.json. Foram abertas as páginas físicas 22,25,26,27,28,51,75:
sem recortes/sobreposição; tipografia dos trechos examinados adequada. Isso não
substitui inspeção final integral. TOC/listas ainda precisam da atualização final.
Os PDFs trabalho_atual.pdf e revisao_41_trechos.pdf são intermediários antigos.

resolucao_achados.csv contém os 25 achados e 13 riscos, com próximos passos; nenhum
foi encerrado por mera existência de uma edição. Prioridade agora: recodificar as
170 células e atualizar derivados, R03, H4/H5 e atribuição de contribuição própria.

Investigação R03: Scripts/diebold_mariano/01_prepare_data.R importa os arquivos
PETR4_close com factor e verifica datas/valores; não implementa o ajuste corporativo.
Não se executou o script. A busca em fontes/código não localizou cadeia suficiente
para atribuir a transformação original ao autor. Harmonizar como série recebida já
ajustada, salvo obtenção da cadeia, e registrar limite de procedência.

Busca complementar Cardoso: surgiu o livro de resumos RBras em
https://lume.ufrgs.br/bitstream/10183/252914/1/001157560.pdf, mas a ferramenta web
não recuperou o conteúdo (timeout) e urllib falhou por DNS. Não foi lido e não
prova o valor RMSE. Também surgiu artigo primário Exacta 2025,
https://periodicos.uninove.br/exacta/article/download/28045/11892/143805,
DOI 10.5585/2025.28045, sobre ESN+AG+correção de eventos em VALE3. Há texto web,
mas não foi incorporado ao corpus34 nem usado para transferir números à PETR4.
Ler para contextualizar contribuição/novidade antes de decidir eventual inclusão
complementar. Não tratar como original RBras 2022a.


## Etapa da matriz: 34 fontes, 170 células e derivados coerentes

Foram conferidos os hashes dos 34 PDFs em Artigos citados. Scripts/
recodificar_matriz_literatura.py contém decisões de leitura humana, não inferências
por palavra-chave: cada célula tem código, localizador físico, síntese, limite e
escopo consultado. Não se declarou leitura integral das 34 obras. A tese longa
foi examinada nos capítulos/aplicações pertinentes. Nelson digitalizado foi lido
visualmente, inclusive físicas 11/13–15 (impressas 356/358–360), para dados/retornos.

Critérios em criterios_matriz_p1_p5.md. D=direta; S=secundária/contextual;
?=informação insuficiente; —=não aplicável. Preserva-se o tema de cada dimensão,
explicitando pesos/matriz, seleção ESN/RC, operação de preparação, comparação
quantitativa LSTM/GRU/Transformer e mercado/ativo. Não tratar Transformer como
arquitetura recorrente; não confundir priors da busca com leis dos pesos.

D por P1–P5: 5,10,25,10,25. S: 0,4,2,2,3. ?:13,5,7,16,2.
Não aplicável:16,15,0,6,4. Total:75 D,11 S,43 ?,41 não aplicável.
Cada dimensão soma34. As 43 células ? estão também em arquivo separado, com motivo;
não são marca de inexistência na fonte ou na literatura. Araújo é pertinente às
cinco famílias mas a descrição lida não individualiza Win/W; sua P1 é ?, não é
excluído da discussão. Hassaan tem divergência entre fórmula e prosa de Xavier;
Millea informa Uniforme antes da transformação ortonormal e também W Gaussiana.

Scripts/revisar_parecer_integridade_lote1.py monta Tabela1/Quadro1/Figura1 a partir
da recodificação. A ordem do quadro é diferente dos IDs em Duttilo e Liu: há mapa
explícito que trata as inversões. Verificação independente com python-docx conferiu
170/170 células e os cinco totais. Mantêm-se34 linhas, sem incluir Lampugnani,
Cardoso RBras2022a ou artigo novo Exacta2025 no corpus.

O texto P0214, P0239–P0241 e P0263/P0267–P0268 foi revisado: volatilidade de Ribeiro
é diária derivada de retornos de cinco minutos; retiradas listas fechadas/lacunas
não comprovadas e alegações universais de custo. P0268 passa a usar série
'disponibilizada como ajustada', sem atribuir aplicação original do fator ao autor.
Isso é avanço parcial R03; resumo/abstract, método e conclusão ainda precisam ser
harmonizados. R13 exige quadro de atribuição/origem do código; não está encerrado.

O script R novo plotar_cobertura_recodificada.R apenas plota a matriz, sem treinar
modelos. R local em C:/Program Files/R/R-4.6.0/bin/Rscript.exe; avisos de locale no
início exigiram strings Unicode escapadas no script. O PNG/SVG finais têm acentos
corretos. Foram ajustados tamanho e aspecto para manter letras legíveis no Word;
o parágrafo de imagem P0280 muda só suas dimensões, conforme log de mídias.
Quadro1 teve500dxa redistribuídos para a primeira coluna e100 retirados de cada
coluna de códigos; largura total preservada. Tabela1 foi condensada para caber
inteira na página, mantendo11pt. A fonte/legenda dos códigos acompanha a tabela.

Durante a primeira montagem de tabelas o teste raw XML falhou porque w:t vazio
serializado é equivalente a elemento autocontido. A tentativa foi preservada em
arquivo próprio e a recuperação está documentada. Agora a comparação usa C14N e
o construtor valida o ZIP integralmente em memória antes de gravar o rascunho.
Não houve alteração do registro v001 nem atualização de seu hash para contornar teste.

PDF mais recente: revisao_matriz170_sintese.pdf,76páginas. Foram abertas as físicas
34,35,36,37: Tabela1 inteira, Quadro1 sem sobreposição de nomes/códigos, cabeçalho
repetido, fonte/nota presente e Figura1 legível/sem recorte. Hashes e alcance em
estado_matriz170.json. revisao_matriz170.pdf, _atual.pdf e _legivel.pdf são
intermediários antigos. As Figuras2–4 efetivas do Word são palavras-chave/rede/
títulos; não há gráfico por ano a corrigir no Word. O antigo script de gráficos
por ano não representa as imagens atuais e não deve ser usado indiscriminadamente.
A chamada de Soltani no quadro permanece2022, coerente com preprint e referência.

Prioridade seguinte: R03 (procedência do ajuste em todos os trechos), H4/H5,
atribuição/contribuição própria, F17eventos, F19comparador sem fonte original,
F20metadados Araújo e F21referências sem chamadas. Revalidar todas as alegações
restantes F14 e citações correlatas. Depois atualizar listas/campos e fazer inspeção
final integral, fechar os38itens por evidência, registrar versão e entregar.
Não marcar o objetivo completo porque a etapa da matriz avançou.
