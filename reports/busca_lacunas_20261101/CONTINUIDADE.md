# Pesquisa ativa das 41 lacunas — base v009

Objetivo integral do autor: buscar nos artigos todas as informações que faltam para preencher os sinais de interrogação. Não encerrar a tarefa como concluída após uma amostra ou renomear códigos para aparentar fechamento. Não substituir lacunas por respostas presumidas.

## Estado material

- v009 e seu SHA256 confirmados. Nenhuma alteração Word promovida nesta pesquisa.
- `inventario_41.json`: lista exata das células com `?` na v009, com linha Word, ID histórico, fonte, hash e decisão anterior.
- `manifesto_fontes.json`: 22 PDFs pertinentes extraídos novamente após conferir os hashes. Extração feita com pypdf; alguns PDFs emitem avisos estruturais, sem impedir extração. Texto extraído deve ser confrontado com renderização quando ambíguo.
- `fontes_extraidas/`: extrações novas e vinculadas ao manifesto; não reutilizar extrações históricas como se fossem atuais.
- `evidencias_rodada1.json`: 12 células com registro individual desta rodada. Duas têm nova evidência localizada; dez ainda não se fecham nas passagens examinadas. As outras29permanecem em pesquisa; isso não significa que não tenham sido auditadas historicamente.
- Dois registros Liu têm IDs fora da ordem alfabética Word: linha17LiuB2022→D18; linha18LiuHLinRojas2025→D17. O script de inventário faz essa associação explicitamente. Não confundir a comparação nanofotônica com o trabalho de sentimento.

## Novas evidências importantes

Jaeger: suplemento `https://www.ai.rug.nl/minds/uploads/freqGen.zip`, vinculado explicitamente na página1do artigo. Baixado e arquivado; hash em `suplementos/Jaeger_freqGen_procedencia.json`. Somente lido, nunca executado. README relaciona o script diretamente ao exemplo Scholarpedia. Win=2*rand-1; W=sprand deslocada por-0.5 e reescalada; script fixa raio final0.25. Construção de canal de viés/entrada e transformações afins de entrada/alvo documentadas. Propostas D15/P1→D e D15/P3→D, com inclusão explícita do suplemento no escopo metodológico e distinção entre código atual disponibilizado (contém revisão2014e nota2015) e texto de2007.

Kumar: repositório oficial vinculado no PDF19. Conector GitHub leu `simulation.ipynb`, blob98e0051d3d4414255f8aae4b99a146c5faca808a. Células source preservadas em `suplementos/Kumar_simulation_fontes.json`, sem executar notebook. Célula11cria matrizes uniformes e esparsas, mas NÃO as passa ao objeto Reservoir. Não classificar como distribuição efetiva dos pesos. Versão de ReservoirPy não fixada; investigar histórico/dependências antes de inferir inicializador.

Wang/Bu/Huang: repositório oficial https://github.com/TingBu-forever/Supplymentary possui README, CITATION.cff e PNG de correlações. README trata features e correlações, sem lei dos pesos ou procedimento de otimização óptica. Artigo PDF3diz que alpha/beta serão otimizados, mas grid search do PDF5está ligado aos comparadores ML. Não transferir o procedimento ao RC por proximidade textual.

Sun: HTML oficial https://www.techscience.com/csse/v36n3/41260/html confirma o PDF. Seção3.2fornece500neurônios/raio0.999/esparsidade0.02, sem procedimento de escolha. Coleta e limpeza são rótulos do fluxo, mas operação específica não é descrita nas passagens3.1–3.3. Aleatoriedade dos pesos não individualiza lei.

## Leituras adicionais desta rodada ainda por registrar em decisões

- D29/P4: PDF7–10lido; comparação experimental se restringe a GS-ARIMA, PSO-ESN, HAR-PSO-ESN, HAR e GS-MLP; seção4.5lista explicitamente os comparadores. Buscar suplemento/alternativa segura antes de concluir a busca.
- D13/P4: PDF8–11lido; tabelas4–5contêm Conventional ESN, AEESN, DeepESN, BrESN e três topologias CESN, sem LSTM/GRU/Transformer. Não confundir DeepESN com essas arquiteturas.
- D22/P1,P4: PDF2–5e8consultados. Win/Waparecem sem lei; tabela3compara variantes ESN e Lorenz. Menção a RNNLSTM na revisão não é comparação numérica. Operações de geração Lorenz não são previsão de preços observados.
- D23/P1,P4: extração local PDF6contém trecho oculto de outra obra (Viehweg2023); já documentado historicamente e NÃO serve para preencher a célula. HTML oficial https://arxiv.org/html/2508.05416v1 confirma método: tabela de distribuição refere-se à amostragem de hiperparâmetros, ruídoGaussiano não define pesos. Resultados próprios com XGBoost e LastValue; menção qualitativa a comparação LSTM de Alessandretti não oferece números no artigo. Buscar código/versão oficial vinculada, sem trocar silenciosamente de obra.
- D34/P1,P2,P4: PDF2–12consultado. Gaussian measurement matrix é matriz de compressed sensing, não Win/W. OMP escolhe átomos/nós, não automaticamente procedimento de seleção de hiperparâmetros. Experimentos comparam ESN e CS-ESN; não LSTM. Sem código oficial localizado nesta rodada ainda.
- D01/P3: PDF8–10,12–14consultado; estimação AGED e aplicações incluem363semanas de ciberataques, colesterol e fibras. NÃO marcar não aplicável sem considerar a série semanal. Não foi identificada transformação temporal concreta nas passagens lidas.
- D19/P3,P4,P5: PDF30,47–48,63–68,79–83e87consultados. Tabela6.1sintetiza MSO, MackeyGlass, Sunspots e Laser. P4: tabela3.1importa números de Evolino de Koryakin et al.(2012), referência62. Investigar a cadeia original para identificar inequivocamente a arquitetura daqueles números; não presumir que toda variante Evolino seja LSTM. Página30apenas diz que também pode treinar LSTM.
- D03: busca textual nova localiza LSTM na referência187, não na síntese principal; não declarar leitura integral nova com base nisso. D30: páginas2e17com números72%/90% precisam checagem de comparabilidade comum e fonte antes de S.

## Próximas ações concretas

1. Continuar leitura dos artigos/células restantes, começando pelas cadeias Evolino/Millea, suplementos de Sharma, código de Kumar e método de Araújo. Ler integralmente textos quando necessário e declarar precisamente escopo, evitando megasaídas truncadas.
2. Registrar decisão e evidência por cada uma das41células, sem transformar ausência de passagem em resposta afirmativa ou negativa sobre o mundo.
3. Incorporar somente correções sustentadas em cópia preparada oficialmente da versão vigente. Atualizar em conjunto Quadro1, Tabela1, Figura1e prosa/legendas dependentes. Renderizar páginas afetadas e registrar revisão conforme controle de versões. Preservar resultados45históricos, rodadaDM e loteilustrativo; nenhum treino/GA/DM autorizado.
4. A conclusão ainda não está demonstrada. Meta permanece ativa; nenhuma condição repetida de bloqueio foi estabelecida. Entregar alcance real e eventuais lacunas científicas irrecuperáveis apenas após esgotar alternativas pertinentes, sem certificar preenchimento que não ocorreu.


## Estado posterior — v010 registrada

Os registros anteriores descrevem estágios preservados. A revisão v010 foi registrada, SHA256 `1da5ea82344c177d75af723362017e3e558bbb127bd9995f7ec0cbd6964f81ed`, com as três alterações Jaeger P1/P3 e Millea P4. Caminho: `reports/monografia/versoes/v010/MayconGarciaSilva_monografia_v010.docx`. Relatório final desta incorporação: `relatorio_incorporacao.md`; identidade e validação visual: `entrega_v010.json` e `inspecao_visual.json`. As 38 insuficiências restantes não foram resolvidas. Continuar alternativas documentais pertinentes sem presumir detalhes ausentes dos artigos. Partir da vigente obtida pelo CLI, nunca reaplicar o rascunho v009 nem executar novamente registrar_revisao.py. Nenhum treinamento/GA/DM autorizado.


## Rodada 2 — pesquisa adicional sem edição Word

Relatório `rodada2/relatorio.md` e evidências `rodada2/evidencias.json`, ligados à v010 por hash. Foram ampliadas 21 células em 13 fontes; nova leitura textual integral de Jaeger (9 páginas), Ping (2), Seddik (11) e Sun (12). As 38 células permanecem ?. Arquivadas fontes oficiais de ReservoirPy em 19 etiquetas anteriores à publicação de Kumar: padrões W normal e Win Bernoulli simétrica, mas ambiente do artigo não fixado. Isso é evidência condicional, não versão histórica certificada; o protocolo não autoriza inferir configuração por padrão presumido. Fonte de apoio Pagliaro baixada/arquivada: 72% vem de Google/cinco dias; não foi localizado 90% pela busca textual; não comprova confronto comum com CNN. Correção de localizador D30/P4: tabelas 3 e 4 na página 17, não Tabela 17. Relatórios registrados anteriormente preservados. Nenhuma edição Word, treino, GA ou DM nesta rodada. Próximas leituras completas: resultados de Araújo, Timbó e Zhang, depois demais fontes parciais, conferindo figuras quando o texto omite conteúdo. Meta ativa; avanço documental real nesta rodada, sem condição de bloqueio repetida.


## Rodada 3 — origem Cyber recuperada e históricos conciliados

Vigente continua v010, hash `1da5ea82344c177d75af723362017e3e558bbb127bd9995f7ec0cbd6964f81ed`, sem edição Word. Relatório/evidências em `rodada3/`. Ampliadas 11 células em seis fontes (Abebe, Araújo, Timbó, Zhang, Vishwas, Millea); 38 insuficiências permanecem. Os registros históricos das 22 fontes foram ligados por hash: não repetir leituras completas apenas por um relatório posterior ter escopo dirigido. Araújo/Timbó/Zhang já tinham leitura integral histórica; houve reexame. Vishwas: texto das 26 páginas agora coberto entre as rodadas2/3; nenhum percentual qualificador novo confirmado. O resumo indexado oficial de Gandhudi não sustenta transportar o ganho de18% da revisão; acesso direto403, sem leitura integral da fonte de apoio. Millea: bibliografia84–90 lida, complementando corpo1–83 registrado no lote21.

Avanço novo importante: RPubs de Gjika recuperado por HTTP (o navegador de pesquisa falhou). Página incorpora HTML público do S3; código lido, sem execução. O link OSF aj7vr é um PDF de figura, não projeto; API de arquivos revelou projeto rq82a. CSV original e dois Rmd recuperados com hashes. CSV366semanas,3zeros; exclusão desses zeros e divisão por100 produz363valores com mesmos quartis da Tabela5 deAbebe, porém média5.381322 versus5.3810 e momentos padronizados diferentes. É hipótese atual, não protocolo recuperado: P3 continua ?. A regra explícita deGjika substitui zeros por0.01, não se demonstrou queAbebe a adotou. Chamadas44/45 deCyber/heartfailure trocadas na própria publicação. Evidências, aritmética descritiva reproduzível e rascunho de perguntas estão em `rodada3/`; nada enviado a autores e nenhum modelo/treino/GA/DM executado.

Próximas alternativas concretas: verificar histórico oficial de versões de arXiv2508.05416 (Sharma), sem substituir silenciosamente a versão citada; conferir canais editoriais de suplementos/código de Deng e Hariharan. Para Abebe/Kumar, usar as perguntas específicas já redigidas se houver autorização futura para contato; não reapresentar conjecturas como documentação histórica nem transformar ausência de comparação LSTM em exigência de novo experimento. Meta ativa: esta rodada foi progresso documental e não estabeleceu três turnos de impasse.

## Rodada 4 — fonte arXiv e nova versão publicada localizada

V010/hash conferidos, sem edição Word. `rodada4/relatorio.md`, `evidencias.json`, `decisoes.json` e `manifesto_entrega.json` registram quatro células em três fontes. Pacotes editoriais arXiv2508.05416v1 (Sharma) e2512.08963v1 (Hariharan) recuperados e inventariados; passagens pertinentes lidas, sem compilar/executar. Sharma: distribuições da tabela são hiperparâmetros, não pesos; comentário sobre inicializadores padrão não faz parte do texto publicado e não individualiza Win/W. Comparadores próprios Last Value/XGBoost; menções LSTM qualitativas. Hariharan: tabelas de ações e vento solar apenas variantes ESN. Nenhum código experimental identificado no inventário desses dois pacotes, sem prova de ausência externa. Deng: ficha DTU e entrada exata no conteúdo público do site do autor ligam DOI, sem código naquela entrada. ArquivoJS apenas lido; nenhum auxiliar sensível ou código executado.

Nova rota específica: capítulo publicado de Sharma DOI10.1007/978-981-95-4109-6_25, pp365–380, online17/11/2025, identificado pela DFKI e editora. Prévia tem resumo com diferença de redação. Corpo não acessível: PDF oficial também não abriu pela web; busca local não achou segunda cópia integral. DFKI remete à mesma preprint. Não presumir versão final igual nem alterar corpus silenciosamente. Restam38células, conciliadas uma a uma com Word e hashes dos PDFs em `rodada4/pendencias38_conferidas.json`. Busca integral não concluída. Esta rodada mudou a próxima ação por identificar versão publicada antes não individualizada; não configura três turnos consecutivos de impasse. Para nova rodada, verificar disponibilidade legítima dessa versão ou outro material primário realmente novo; evitar simplesmente repetir as mesmas leituras ou reapresentar padrões de bibliotecas como configuração histórica certificada.

## Rodada5 — disponibilidade pública conferida

V010/hash preservados,38células. Buscas de versão publicadaSharma porDOI/título e domíniosStirling/NII não recuperaram segunda cópia identificada;DFKI continua ligando a preprint. FonteGandhudi: lista do autor consultada, semPDF vinculado; resumo/prévia oficial não confirma18%ou contraste qualificador. ConsultaOpenAlex porHTTPpúblico, após falhaDNS no ambiente restrito, retornou ambosDOIs como closed, semPDFaberto/repositório integral registrado. JSONs brutos, hashes e locais em `rodada5/resultado_acesso.json`; isso não é prova universal de ausência nem leitura de conteúdo científico.

`rodada5/requisitos_documentais38.md`/JSONindividualizam a informação a comprovar em todas38células, com hashes reconciliados. Não são novas respostas de autores. Corrigido na consolidação o localizador históricoD30“tabela17”: tabelas3/4pPDF17, tabela5p18. Relatório e manifesto no mesmo diretório. SemWord/treino/GA/DM/contatoexterno. Meta não concluída. A pesquisa de acesso adicional não obteve o corpo publicado; não repetir as mesmas consultas como avanço. Nenhuma espera de processo vivo existe. Persistem alternativas condicionadas a material específico novo; não houve demonstração de esgotamento universal de todas as fontes/canais, portanto não marcar bloqueio global apenas por estes dois acessos fechados.
