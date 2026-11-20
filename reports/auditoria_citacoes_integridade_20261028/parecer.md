# Auditoria de citações e integridade acadêmica da monografia ESNAUTO

Data da auditoria: 28 de outubro de 2026. Autor da monografia: Maycon Garcia Silva.

A versão examinada **não está integralmente coerente com as fontes citadas**. Foram encontrados erros de atribuição de métricas, população, horizonte e objeto experimental, além de extrapolações e lacunas documentais. A correspondência autor–ano está organizada, mas não assegura fidelidade científica. Recomenda-se corrigir os achados de prioridade alta antes de encaminhar esta versão para avaliação.

Na comparação textual local não foi demonstrado plágio. Isso não é certificado de ausência de plágio: o exame não alcança todo o conteúdo publicado, documentos privados, traduções não literais ou a procedência integral do código. Os problemas comprovados de citação devem ser corrigidos independentemente de uma eventual classificação disciplinar.

## Identidade e alcance

- Alvo: `C:/Users/User/Downloads/MayconGarciaSilva_monografia_FASOFT_conferida.docx`.
- SHA256: `2b233d00b880f0f8727baf587828419b591f45428b409be5ec680932d09805aa`. É idêntico à cópia do projeto. O relatório não audita uma versão Word diferente.
- Guia: `GUIA_Padronizacao_Monografia_FASOFT_UniRV (1).pdf`, 76 páginas, primeira edição, versão 1.0.2. Suas orientações foram tratadas como critérios de análise, não como autorização para contactar pessoas ou realizar ações externas.
- Foram inventariadas 50 referências e as 184 ocorrências reconhecidas pelo cruzamento autor–ano existente, novamente vinculadas ao texto da cópia idêntica. Esse número é de ocorrências reconhecidas, não de afirmações independentes nem garantia de detecção universal de todos os formatos de citação.
- Foram extraídos os 34 PDFs de `Artigos citados`; consultados os trechos pertinentes às atribuições, incluindo métodos e resultados. Também foram examinados Lampugnani, a tese de Cardoso e as extrações dos dois trabalhos de Cardoso usados como modelos gráficos. Não se declara leitura integral de todas as páginas de todas as obras.
- Algumas obras da lista de referências não estão em `Artigos citados`. Foram procuradas no projeto e consultadas fontes primárias eletrônicas quando acessíveis. O registro das 50 obras distingue apoio localizado, divergência, verificação limitada e ausência de consulta integral.
- O PDF nativo de 75 páginas já preservado foi usado para localizar passagens; os localizadores automáticos podem ser ambíguos e não substituem a frase e o identificador P. Não foi refeita a auditoria visual de todas as páginas nesta análise de conteúdo.
- Não houve alteração do Word, de resultados, de código experimental ou das bases históricas. Não foram executados treinamento, GA ou DM.

Os identificadores P são índices de parágrafos da extração desta auditoria, começando em zero: primeiro os parágrafos do corpo, depois os das tabelas. Não são números de página. A extração preserva o texto integral para localizar cada achado. A matriz de ocorrências aponta também a página física do PDF quando reconhecida; a numeração impressa é uma unidade menor.

O comando histórico `auditar_base_monografia.py --check` falhou porque seu validador rejeita o caminho absoluto do guia em Downloads. O snapshot não foi alterado. A identidade desta auditoria foi estabelecida por hashes diretos, sem reutilizar localizações da monografia PETR4 antiga como se fossem desta versão.

## Achados sobre fidelidade às fontes

Prioridade **alta** significa risco de comprometer a sustentação de uma afirmação, resultado bibliográfico ou procedimento. **Média** significa delimitação, metadados ou redação que exigem correção. Nenhuma prioridade constitui previsão de nota ou decisão da banca.

### F01 F1 de uma amostra de ações atribuído especificamente à PETR4

**Alta; divergência comprovada.** Seção 2.1, P0195: o F1 de 72,7% é descrito como resultado para a PETR4. Costa e Lunkes, PDF p. 15, apresentam F1 de 72,74% para o modelo de classificação na amostra de 40.562 observações; a comparação dos modelos A/B/C está na p. 17. O artigo não apresenta esse número como F1 individual da PETR4.

**Proposta:** “Costa e Lunkes (2025) obtiveram F1 de aproximadamente 72,7% com o modelo híbrido de classificação na amostra de ações brasileiras analisada.” Identificar a população do artigo; não atribuir o número a um ativo sem resultado desagregado.

### F02 Sentimento de notícias confundido com direção do índice

**Alta; divergência comprovada.** P0196 atribui a Liu H. uma acurácia preditiva de 75% para a direção do S&P 500. Nas pp. 21 e 28 do PDF, o valor de 75,56% é a classificação de sentimento do FinBERT nas notícias da Benzinga. A Tabela 2 da p. 28 trata separadamente a classificação temporal; a Tabela 1 é de sentimento.

**Proposta:** mencionar a integração de sentimento, indicadores e modelos temporais sem usar 75% como acerto da direção do índice. Se mantido o número, escrever sua tarefa, modelo e fonte de notícias exatos. Não converter resultados de NLP em desempenho de previsão financeira.

### F03 Janelas de treinamento apresentadas como horizonte de previsão

**Alta; divergência comprovada.** P0260 diz “janelas de previsão de 15, 30 e 60 dias”. Sharma, seção 5, PDF p. 8, define treino de 15, 30 ou 60 pontos, teste de dez pontos e avanço de um ponto. A seção 6 retoma esses tamanhos de treino.

**Proposta:** “Sharma et al. (2025) utilizaram janelas de treino de 15, 30 e 60 observações, com teste de dez pontos.” Rever também P0220: os testes estatísticos descritos na p. 12 são contra XGBoost e o comportamento não é uniforme para os três tamanhos de janela. A comparação exploratória com ARIMA não é o mesmo contraste estatístico.

### F04 Distribuição da busca de hiperparâmetros confundida com distribuição dos pesos

**Alta; divergência comprovada.** P0240, P0260 e P0562 usam a Uniforme do input scaling e a Log Uniforme do raio espectral de Sharma como evidência sobre a lei de geração dos elementos de Win. A Tabela 1, PDF p. 7, apresenta **distribuições de amostragem dos hiperparâmetros**. Isso não identifica, por si, a distribuição dos pesos da matriz. Também não confundir distribuição de Win e de W: em Hariharan, p. 4, a passagem explícita `uniform(−1, 1)` refere-se às conexões de entrada para os clusters.

**Proposta:** separar três campos na extração: distribuição dos elementos de Win, distribuição/estrutura de W e distribuição usada para amostrar hiperparâmetros. Reescrever a síntese somente após essa separação.

### F05 A lista dos cinco trabalhos omite uma fonte explicitamente pertinente

**Alta; inconsistência comprovada da síntese.** P0239–P0241 e P0562 sustentam que só cinco trabalhos especificam a distribuição. Araújo descreve cinco famílias probabilísticas na própria pesquisa (PDF pp. 5, 7–9), mas não integra a lista dos cinco. Hassaan ainda explicita os controles Xavier e He nas pp. 7–8, além das sequências caóticas. A lista mistura variáveis diferentes, conforme F04.

**Proposta:** retirar provisoriamente a afirmação “apenas cinco” e a generalização sobre “os demais”. Refazer a codificação documental com localizador para cada marcação. Não substituir por um novo total sem revisar as 34 obras sob a mesma definição.

### F06 Taxa de acerto por tolerância confundida com acerto direcional

**Alta; divergência comprovada.** P0194 descreve Timbó como uso de “taxa de acerto direcional”. No PDF pp. 7–8, o acerto depende de um desvio absoluto máximo de 0,50 em relação ao fechamento, não do sinal da variação. A discussão apresenta 60,87% sob essa tolerância. A correlação de Pearson está documentada na p. 5.

**Proposta:** “O estudo selecionou indicadores por correlação e avaliou previsões por uma tolerância absoluta em relação ao fechamento.” A afirmação de que os autores reconhecem ausência de adaptação e de memória longa também não teve apoio localizado nas conclusões; retirar a atribuição ou localizar a passagem exata. Não apresentar a primazia histórica brasileira como demonstrada por um único artigo.

### F07 Recomendação de redes recorrentes atribuída além do que a fonte diz

**Média; apoio parcial.** P0195 afirma que Costa e Lunkes recomendam especificamente redes recorrentes. Na conclusão, PDF p. 19, a recomendação é de outros algoritmos, como redes neurais e ensembles. A qualificação “recorrentes” é uma escolha da monografia. A superioridade sobre abordagens “puramente estatísticas” também não resulta de um confronto comum com Timbó.

**Proposta:** manter a recomendação geral e apresentar a opção por redes recorrentes como decisão do presente trabalho. Não comparar F1 e erro/tolerância entre estudos como se medissem a mesma tarefa.

### F08 Uso de fechamento ajustado em Sun não está demonstrado

**Alta; apoio insuficiente da atribuição.** P0212 e P0245 afirmam uso de adjusted close. Sun, PDF p. 5, lista fechamento e fechamento ajustado como colunas distintas e declara testar o fechamento; p. 6 volta a dizer que os experimentos leem closing prices. Há inconsistências nos valores e descrições da própria fonte. A presença da coluna ajustada não comprova qual coluna entrou efetivamente no modelo.

**Proposta:** relatar previsão do fechamento conforme os métodos e não usar Sun como prova inequívoca de adoção de ajuste corporativo. Sua comparação principal é com LSTM **simplificada**, não com toda configuração LSTM. O artigo ainda chama RMSE de indicador de convergência/tempo; essa terminologia não deve virar medida de tempo computacional na monografia.

### F09 Seddik exige distinção entre série simulada e preços observados

**Alta; omissão de condição experimental.** P0219 apresenta aplicação a Bitcoin e RMSE inferior a 1 como evidência financeira direta. O artigo menciona Bitcoin, inclusive nas pp. 4–6, mas descreve séries **geradas pelo sistema de Lorenz** a partir de condições iniciais associadas a valores de preço, máxima e mínima. Não equivale a previsão fora da amostra de uma série observada de preços do Bitcoin. A Tabela 2, p. 7, apresenta vários RMSE iguais ou superiores a 1; o resumo destaca um mínimo.

**Proposta:** “Seddik et al. (2023) examinaram uma ESN em trajetórias simuladas de Lorenz, inicializadas com valores associados a Bitcoin.” Distinguir mínimo de erro e conjunto de resultados. Não transformar sensibilidade das condições iniciais do sistema gerador em teste isolado dos pesos iniciais da ESN. A fonte contém imprecisões internas; elas precisam ser contextualizadas.

### F10 Resultados conservadores em Liu não demonstram imunidade a mudanças de regime

**Alta; extrapolação.** P0216 atribui ao sistema nanofotônico reação ajustada mesmo em grandes flutuações e afirma incapacidade de sistemas de software lentos em tempo real. Liu B., PDF p. 8, explica que as curvas ajustam pior nas flutuações violentas e apresenta o comportamento conservador como efeito de ancoragem. As pp. 10 e 14 discutem limitações e resultados direcionais próximos de 0,5.

**Proposta:** relatar os quatro índices, o sistema nanofotônico e as limitações em flutuações intensas; retirar a comparação genérica com software em tempo real sem benchmark correspondente.

### F11 Definição de AG atribuída a Millea sem apoio localizado

**Média; apoio parcial.** P0223 junta os resultados sobre matrizes ortonormais à afirmação de que “o mesmo trabalho” descreve os AGs. A seção 3.3 e a Tabela 3.3, PDF pp. 24–26, apoiam a investigação de ortonormalidade em tarefas específicas. Não foi localizada ali uma exposição de algoritmos genéticos que sustente a última frase; a busca pelo termo também não a recuperou.

**Proposta:** separar a síntese de Millea e a definição de AG. Apoiar esta última em uma fonte efetivamente consultada sobre AG. Não usar estabilidade em benchmarks sintéticos como demonstração geral sobre preços de ações.

### F12 Versão de Soltani e conclusões de lacuna precisam ser distinguidas

**Alta; diferença documental confirmada, parte interpretativa não demonstrada.** O arquivo local é o preprint v1 de 4/8/2022, DOI `10.21203/rs.3.rs-1909702/v1`; a referência P0545 indica Neural Processing Letters, 2023. A contagem de 74 estudos é apoiada pelo preprint, pp. 2 e 6. A Tabela 5, p. 8, apresenta 16 usos de PSO e dez de GA; frequência de uso não é ranking causal de eficácia.

Não foi localizada afirmação específica dos autores que confirme a escassez de finanças ou o papel negligenciado das distribuições com a amplitude atribuída em P0227, P0236, P0265–P0266. O foco é otimização de parâmetros e os datasets são discutidos nas pp. 11–13.

**Proposta:** citar a versão efetivamente lida ou obter a publicação final e confrontá-la. Apresentar a lacuna sobre distribuições financeiras como conclusão delimitada da presente revisão, com extração verificável, quando sustentada. Não trocar apenas o ano e manter automaticamente a atribuição.

### F13 Eficiência e estabilidade apresentadas como garantias gerais

**Alta; extrapolação.** P0211 diz que o ajuste é matematicamente estável e ordens de grandeza mais rápido que BPTT; P0264 afirma que evitar BPTT evita instabilidades numéricas. A redução do conjunto de pesos treináveis é apoiada por Jaeger, mas não garante condicionamento numérico, estabilidade dinâmica ou uma razão universal de tempos. Jaeger, PDF pp. 3–5, discute ESP, regularização, escolhas de parâmetros e perigos de instabilidade.

**Proposta:** “O treinamento apenas do readout reduz a otimização necessária em relação ao ajuste de todos os pesos; o custo e a estabilidade dependem da configuração e da tarefa.” Reservar a razão de tempos aos próprios registros, distinguindo 0,05 s de ajuste e 37,9 h de busca. Não confundir esta ressalva com invalidação dos tempos registrados.

### F14 Comparações e linguagem causal mais fortes que a evidência localizada

**Média; revisão de escopo.** P0213 chama a topologia de fator preponderante; P0218 fala em superioridade significativa por impedir mistura caótica; P0224 e P0226 atribuem evitar mínimos locais e garantir estabilidade. Os estudos apoiam comparação de configurações e resultados sob seus protocolos, não garantias universais ou mecanismos causais automaticamente isolados.

Wang W., PDF pp. 2 e 7, documenta sete mercados, topologias e comparação com LSTM/RNN. Hariharan, pp. 4 e 7–10, documenta clusters e NRMSE. Tian, pp. 3 e 12, documenta SSA–ESN em vinte ativos. Ecer, p. 1 e resultados, documenta MLP–GA/PSO em BIST100. Deng, pp. 10 e 20, documenta otimização de ESN empilhada para PEMFCs, com comparação a resultados de modelos anteriores.

**Proposta:** usar “os autores reportaram menor erro nas condições examinadas”; reservar “estatisticamente significativo” a testes efetivamente identificados e “causal” a controles que isolem o mecanismo. Separar finanças, engenharia de combustível e séries sintéticas.

### F15 A matriz P1–P5 tem marcas incompatíveis com suas definições

**Alta; inconsistências comprovadas e recodificação necessária.** P0271 define P4 como comparação experimental com LSTM, GRU ou Transformer. O Quadro 1 marca P4 presente para Ribeiro, Dewick e Jaeger. Ribeiro lista ARIMA, HAR, MLP e ESN (PDF pp. 1 e 3), não uma experiência própria com aqueles três baselines. Dewick trata métodos estatísticos de distribuições e regressão; Jaeger é exposição conceitual. Citar literatura sobre redes não é realizar comparação experimental com elas. Hariharan inclui DeepESN e outras variantes ESN; decidir explicitamente se isso satisfaz uma definição mais ampla de P4.

Também há mistura entre otimização de ESN e de outros modelos: P0565 usa Ecer para ilustrar predominância de GA na dimensão P2, embora seu modelo seja MLP e a própria linha de Ecer marque P2 ausente. O tratamento de séries simuladas em Seddik exige qualificação de P5, conforme F09. Abebe descreve ajuste de distribuições em aplicações não financeiras; isso não equivale automaticamente a pré-processamento de séries financeiras em P3.

**Proposta:** registrar, para cada um dos 170 cruzamentos estudo × pergunta, a regra operacional e a passagem de evidência. Não validar as porcentagens 47%, 47%, 91%, 62% e 88% somente porque a soma das marcas coincide com o gráfico. Ver `matriz_34_estudos.csv`, que sinaliza as células diretamente contestadas e as demais como pendentes de recodificação uniforme; não oferece totais substitutos fictícios.

### F16 Lacunas científicas e palavras de abrangência não estão sustentadas pelas contagens atuais

**Alta; conclusão bibliográfica precisa de revisão.** P0230, P0239–P0241, P0263–P0267 e P0274–P0277 usam “maioria”, “consenso”, “garantindo” e quantificações cuja base contém os problemas F04, F05 e F15. A distinção da coleção reconstruída de 34 estudos e das 24 listas de palavras-chave está corretamente explicitada em P0270 e P0370–P0374; isso não valida semanticamente as classificações P1–P5.

**Proposta:** manter o portfólio como coleção descritiva e suspender as conclusões quantitativas de lacuna até corrigir a extração. A ausência de um termo de palavra-chave não prova ausência de abordagem no artigo, ressalva já corretamente presente em P0288.

### F17 Ajuste corporativo tem apoio, mas a lista detalhada contém interpretação adicional

**Média; apoio parcial.** Cardoso BovDB, PDF pp. 7–8, sustenta razão entre fechamento anterior e abertura do evento, acumulação regressiva e correção dos preços. A enumeração detalhada de exceções e condições para Ex-Split Up, Full Rights, Units e BDR em P0243–P0244 e P0311–P0312 não deve ser apresentada como transcrição literal de um procedimento validado para cada categoria. O artigo lista categorias no panorama da p. 12; listagem não é uma ablação de necessidade de ajuste por categoria.

**Proposta:** distinguir a regra documentada da interpretação econômica do autor e apontar a implementação usada na pesquisa. Substituir em P0246 a generalização de que ajuste é necessário para “qualquer modelo” por sua relevância para séries afetadas por eventos e pela variável/horizonte estudados.

### F18 Fórmula e execução de Methodi Ordinatio não podem ser certificadas

**Alta; verificação incompleta.** P0365–P0368 afirma execução e preservação das planilhas de busca e ranking. Os arquivos originais `methodi_ordinatio.xlsx` e `extracao_completa.xlsx` não foram localizados na árvore do projeto. Foram encontrados scripts e metadados reconstruídos, que não substituem esses registros. Isso não prova inexistência histórica das planilhas.

O original de Pagani et al. (2015) não está no acervo identificado; sua página primária permite ler o resumo, não a equação integral. O termo `Citações/100` em P0367 exige conferência no texto integral e na planilha aplicada. Foi consultada também uma publicação posterior dos mesmos autores, em Ciência da Informação, que descreve o procedimento e ressalva o uso de JCR/SJR; ela não foi tratada como se fosse o texto integral de 2015 nem como prova do cálculo executado em ESNAUTO.

**Proposta:** recuperar os registros; ou declarar a limitação retrospectiva e caracterizar honestamente a revisão realizada. Se a fórmula/indicador foi adaptado, explicitar a adaptação. Não criar uma planilha nova e apresentá-la como registro original de 23/3/2026. Não há, nesta auditoria, novo ranking ou recálculo.

### F19 Comparação com Cardoso 2022a depende do original

**Alta; apoio primário não fechado.** P0310, P0457–P0462, P1013–P1016 e retomadas usam período, ausência de GA e RMSE de 0,4987 do trabalho RBras. Não foi localizado seu texto primário completo entre os PDFs do projeto. A tese de Cardoso (2025) é outra obra e outro protocolo; não pode ocupar esse lugar automaticamente.

**Proposta:** conferir os anais, a página do resultado, a definição da métrica, a escala e o período da amostra antes de manter o número e a comparação. A indisponibilidade é uma pendência de validação; não demonstra que 0,4987 esteja errado. A comparação com Lampugnani foi examinada separadamente e não resolve essa pendência.

### F20 Metadados não estão integralmente reconciliados

**Média; erro confirmado e revisão adicional.** P0505 abrevia Abebe como “E.” e Goshu como “A.”, mas a primeira página do PDF identifica **Tayu Nigusie Abebe** e **Ayele Taye Goshu**. Corrigir para nomes completos ou iniciais correspondentes, mantendo consistência. A referência de Behera também deve ser conferida contra os nomes completos da primeira página, evitando iniciais redundantes ou invertidas.

O PDF de Araújo é uma prova de autor, com paginação editorial provisória e informação de copyright 2024/2025 em partes diferentes. Sua substância metodológica foi lida; a identidade da prova não equivale à conferência das páginas 314–325 da edição final. Deng é accepted manuscript de 2021 com referência ao fascículo de 2022; Kumar tem publicação on-line de 2024 e fascículo de 2025. Essas diferenças não significam automaticamente erro de ano. Registrar a versão lida e os metadados da edição citada, especialmente em Soltani.

### F21 Duas referências não têm chamada autor–ano localizada

**Média; reconciliação inversa.** Cardoso (2025), P0514, e Jaeger (2001), P0531, não aparecem nas 184 ocorrências reconhecidas; a busca adicional no corpo não localizou chamadas aos dois anos. Estar na lista não prova apropriação indevida ou proibição expressa do guia. Mas é necessário decidir se foram efetivamente usados e se falta atribuição onde contribuíram.

**Proposta:** citar onde sustentam o texto, se efetivamente consultados e pertinentes, ou retirar da seção de referências conforme orientação institucional. Não adicionar chamadas decorativas para satisfazer contagem. A tese de Cardoso deve constar na análise de procedência se houver aproveitamento de código ou metodologia.

### F22 Resultados de Nelson apoiam a parametrização, não uma necessidade de pesos GED

**Média; núcleo apoiado e limite de inferência.** Nelson é um PDF escaneado sem texto extraível; as páginas físicas 4–9 foram abertas visualmente. As pp. impressas 352–353 (PDF 7–8) confirmam ν = 2 Normal, ν = 1 dupla exponencial/Laplace e caudas mais espessas para ν < 2. O uso financeiro de GED/EGARCH está sustentado.

**Proposta:** preservar esse conteúdo de P0232–P0233. Não concluir que distribuições dos retornos determinam a lei ideal dos pesos da ESN. A monografia já reconhece parte dessa distinção em P0237–P0238, mas P0231 ainda fala em fidelidade estatística do reservatório como se fosse consequência demonstrada. “Justificativa mais antiga” requer pesquisa histórica adicional; preferir “referência clássica”.

### F23 Duttilo 2023 reúne afirmações de fontes distintas

**Média; apoio parcial e atribuição composta.** A tese de Duttilo documenta GND/MGND, mercados, índices e rejeição da normalidade, inclusive Euro Stoxx e S&P500. O estudo Duttilo–Gattone de 2022, pp. 1, 4–5, trata especificamente de DJIA e apresenta AIC, BIC e HQIC. P0234 concentra esses elementos na chamada única de Duttilo (2023). Não foi localizado HQIC no texto extraído da tese, que apresenta extensivamente AIC e BIC; parte dos glifos de números precisou de normalização documentada.

**Proposta:** separar o estudo DJIA de 2022 e a tese, citando os dois quando necessário. Não transferir critérios ou resultados de uma versão à outra. Não concluir que um critério de informação, isoladamente, é teste de normalidade.

### F24 H1 ainda define comparabilidade por não significância

**Alta; problema conceitual confirmado na versão atual.** P0181 mantém a definição de desempenho comparável como ausência de diferença estatisticamente significativa no DM. Não rejeitar igualdade de acurácia não demonstra equivalência ou não inferioridade; pode refletir informação insuficiente. A documentação primária de `forecast::dm.test` define a hipótese nula como igualdade de acurácia e a alternativa bilateral como diferença, não um teste de equivalência.

**Proposta:** “H1 — desempenho: a ESN otimizada apresentará menor perda preditiva que os baselines definidos, sob o protocolo adotado. A evidência histórica será descritiva; a rodada controlada complementar avaliará diferença de acurácia e direção do diferencial médio de perda. A não rejeição da hipótese nula será interpretada como evidência insuficiente de diferença, sem demonstrar equivalência.” Registrar a reformulação como esclarecimento editorial, não como hipótese pré-registrada. Os quatro contrastes observados rejeitaram a nula; o erro conceitual da definição continua exigindo correção mesmo assim.

A função documenta a modificação de Harvey, Leybourne e Newbold (1997). É recomendável identificar essa implementação e acrescentar sua referência pertinente em métodos, sem afirmar que os números precisam ser refeitos ou que foram invalidados.

### F25 A introdução teórica exclui modelos estatísticos de forma indevida

**Média; generalização incompatível com a própria revisão.** P0193 afirma que a não linearidade e a estocasticidade “inviabilizam” a aplicação direta de ARIMA e regressão linear. Os estudos de Timbó, Ribeiro e Kumar discutidos no próprio capítulo empregam tais modelos ou os usam como comparadores. Não normalidade dos retornos, não linearidade e não estacionariedade são propriedades distintas; não é correto reuni-las como proibição automática de uso.

**Proposta:** “Modelos lineares podem apresentar limitações na representação de dependências não lineares e mudanças de regime, razão pela qual seu desempenho precisa ser confrontado com alternativas sob protocolos comparáveis.” Explicitar que ARIMA inclui diferenciação e que a adequação depende da série e da tarefa, conforme a descrição dos próprios artigos.

## Riscos metodológicos que uma banca pode questionar

Estes pontos são inferências de avaliação acadêmica, **não cláusulas de reprovação automática do guia**.

| ID | Questão possível | Evidência atual | Tratamento recomendado |
|---|---|---|---|
| R01 | “Como a revisão foi sistemática se não há trilha de seleção/ranking?” | P0365–P0368; F18 | Recuperar busca e planilhas ou limitar a alegação. O número de PDFs não reconstitui o fluxo dos 100 registros retornados. |
| R02 | “Por que as contagens de cobertura contêm estudos mal classificados?” | F04, F05, F15, F16 | Recodificar P1–P5 e atualizar as conclusões dependentes. Gráficos corretos aritmeticamente podem representar dados codificados incorretamente. |
| R03 | “Quem aplicou o Fator de Ajuste e onde está a transformação?” | P0311 e resumo afirmam aplicação; contexto e executores recebem série com fator | Localizar cadeia de processamento e autoria. Usar “série previamente ajustada” caso isso corresponda ao procedimento real. Não declarar reaplicação sem registro. |
| R04 | “A ordem cronológica garante sozinha ausência de vazamento?” | P0314–P0316 versus fronteira estrita e continuidade corrigida em P0354 e P0451 | Delimitar a garantia à execução auditável. Ordem dos blocos e fronteira dos alvos são propriedades distintas. Não atribuir automaticamente o comportamento do motor atual a todas as execuções antigas. |
| R05 | “Foram preservadas as matrizes campeãs?” | P0252/P0337–P0338 soam abrangentes; P0352/P0468 reconhecem ausência de GA_RUN_0030 e de outras saídas | Harmonizar capacidade do software, política aplicada e artefatos realmente disponíveis. |
| R06 | “O teste foi usado para escolher o campeão?” | P0315 afirma isolamento; tabelas destacam recordes de teste | Manter clara a seleção por fitness treino/validação e caracterizar rankings de teste como descrição posterior. Confirmar nos registros antes de afirmar garantia universal. |
| R07 | “Qual o efeito específico de LHS/cataclismo?” | P0184 e H4; P1004–P1005 e conclusão reconhecem ausência de ablação | Distinguir implementação, diversidade não mensurada e ganho causal não testado. Não tratar “não testada causalmente” como confirmação do efeito. |
| R08 | “Baixa variação entre configurações é estabilidade entre repetições?” | Onda 5 com 15 execuções, sem distribuição de repetidas sementes por configuração | Distinguir dispersão descritiva entre configurações de repetibilidade/robustez estocástica. H5 não sustenta superioridade universal. |
| R09 | “A comparação favorece a ESN pelo orçamento de otimização?” | P0340 e P0484 reconhecem extensa busca ESN e um baseline por arquitetura | Preservar essa limitação. DM não elimina a diferença de orçamento. |
| R10 | “DM comprova equivalência, generalização ou todas as sementes?” | Rodada controlada com uma semente e quatro contrastes | Conservar o escopo controlado. Não misturar os vetores novos às 45 execuções ou ao lote ilustrativo de 200 gerações. |
| R11 | “R² alto demonstra utilidade financeira ou valor além da persistência?” | P0476/P0485 restringem o uso; não há demonstração econômica | Manter a restrição e registrar que o baseline de persistência é uma questão relevante para preços em nível. Não exigir novo experimento como consequência automática desta auditoria editorial. |
| R12 | “O título atribui ao fator uma contribuição que não foi isolada?” | Título enfatiza correção; P0313 e conclusão negam ablação | Discutir alinhamento com orientador; explicar contribuição experimental e de software sem reivindicação causal do fator. |
| R13 | “Qual a contribuição própria frente a Araújo, Lampugnani e Cardoso?” | Fontes reconhecidas; combinações e motor próximos | Apresentar quadro explícito de elementos herdados, adaptados e desenvolvidos. Identificar origem do código quando houver. Semelhança metodológica e agradecimento não substituem atribuição de trechos/código adaptados. |

As quatro linhas do arquivo primário `Scripts/results/diebold_mariano/controlled_runs/seed_20260926/dm/resultados_dm.csv` e a separação de protocolos continuam sendo a evidência dos testes; esta auditoria não os recalculou. Os riscos acima não demonstram invalidação automática dos quatro contrastes.

## Exame de plágio e atribuição

### Procedimento efetivamente executado

O script `Scripts/auditar_integridade_textual_fasoft.py` compara o corpo textual e as tabelas do alvo com 39 fontes locais indexadas: 34 PDFs de artigos, a monografia Lampugnani, o guia, a tese de Cardoso e duas extrações de revisões de Cardoso. As 39 entradas não representam 39 artigos citados distintos. A normalização ignora caixa, acentos e pontuação. O índice procura sequências de oito palavras; foram encontradas dez janelas, algumas sobrepostas. A busca anterior com 12 palavras não encontrou ocorrências no corpus menor que então estava extraído; ela não deve ser apresentada como resultado do corpus ampliado final.

O alvo exclui pré-textuais e a lista de referências desta triagem para não inflar o resultado com nomes institucionais e títulos de obras. As fontes podem conter bibliografias, textos de figuras e camadas invisíveis; por isso, coincidências são candidatos para leitura, não veredictos. O PDF de Nelson é imagem e não entra efetivamente na comparação por texto; seu conteúdo relevante foi lido visualmente, sem OCR integral. O manifesto registra a cobertura extraível.

Uma comparação adicional de parágrafos do corpo com o corpo de Lampugnani, por SequenceMatcher de tokens, não encontrou pares com razão ≥ 0,40. Esse limiar é heurístico e não possui valor de classificação acadêmica. Não é escore de originalidade.

### Leitura dos candidatos

| Local | Coincidência | Avaliação |
|---|---|---|
| P0200 × Lampugnani L0268 | Trecho sobre Hochreiter, Schmidhuber e GRU, com quatro janelas sobrepostas | Sequência de nomenclatura e referência histórica, com atribuições às fontes originais no alvo. Insuficiente para acusação de cópia extensa. A redação deve continuar independente. |
| P0200 × Cardoso ENMC p. 2 | Expansão de rede neural recorrente/RNN | Terminologia técnica padronizada; não demonstra plágio. |
| P0234 × tese de Cardoso PDF p. 38 | Nome do critério de informação de Akaike | Denominação técnica convencional. |
| P0254 × tese de Cardoso PDF p. 59 | Início da síntese de Ribeiro et al. | Há fonte atribuída, mas é útil reler o artigo primário e manter a síntese autoral. A janela curta não prova cópia substancial. |
| P0268 × Lampugnani L0543 | Distribuições probabilísticas aplicadas às matrizes Win/W | Expressão técnica curta comum ao método; não suficiente para acusação. |
| P0365 × Cardoso KBS PDF p. 4 | Parte comum da string de busca | Fragmento convencional de consulta bibliográfica. A origem/adaptação de um protocolo específico merece crédito, mas esse fragmento não prova cópia nem execução da busca declarada. |

Não foi encontrado, nesses candidatos, um bloco extenso de prosa reproduzida que permita afirmar plágio textual. A epígrafe é citação direta atribuída e sua frase foi novamente conferida no primeiro parágrafo do artigo assinado por Gleick. A existência dessa citação literal é regular, não indício de plágio.

Também foram comparados os hashes dos arquivos de mídia incorporados nos dois Word: seis no alvo e cinco em Lampugnani, sem identidade byte a byte. Isso não detecta redesenho, recorte ou recompressão e não substitui perícia visual de imagens derivadas. Resultado em `comparacao_midias.json`.

### Riscos que a comparação lexical não resolve

1. **Plágio por tradução ou paráfrase dependente:** as fontes são majoritariamente em inglês; sequências em português podem não ter correspondência literal. O confronto semântico revelou F01–F25, mas não mede automaticamente dependência estilística ou tradução disfarçada de todo o corpus.
2. **Apropriação de ideia, método ou código:** ESN, GA, fitness 40/60, distribuições, BovDB e elementos de implementação precisam de atribuição proporcional. A monografia cita Araújo e Lampugnani, o que é positivo; isso não certifica licenças, histórico de autoria ou independência integral do código. Esta auditoria não realizou perícia completa de proveniência do repositório.
3. **Citação de fonte não consultada:** usar uma revisão ou tese para atribuir detalhes ao artigo original sem o ler pode gerar citação secundária não declarada. A matriz das 50 obras deixa explícito onde não houve acesso integral.
4. **Figuras, tabelas e dados:** as Figuras 1–4 são análises próprias de uma coleção reconstruída, mas suas classificações precisam das correções descritas. As Figuras 5–6 têm procedência documentada no lote ilustrativo. Fonte “Elaborado pelo autor” não transforma dados de terceiros em dados próprios; deve-se preservar a indicação de origem.
5. **Erro de citação não é automaticamente fraude:** os achados comprovam problemas no texto, não intenção de enganar. A classificação disciplinar exige procedimento institucional e evidência adequada.

O exame não usou Turnitin, iThenticate ou base institucional de trabalhos submetidos. Não há percentual confiável de plágio a fornecer a partir desta auditoria. Detector de IA tampouco foi usado como prova de autoria ou irregularidade.

## Guia FASOFT e possibilidade de reprovação

### O que está expresso no guia

| Página física | Exigência ou orientação efetiva | Relação com este caso |
|---|---|---|
| 2 | Respeito aos direitos autorais e crédito adequado | Fundamenta atenção à atribuição; não estabelece percentual de similaridade nem penalidade automática. |
| 14 | Paráfrases/citações e posicionamento apoiado em dados e provas; referência citada na lista | Autor–ano é necessário, mas os erros F01–F25 impedem afirmar fidelidade integral. |
| 19 | Revisão, estado da arte, metodologia, critérios, resultados e retomada de objetivos/hipóteses | A estrutura existe; sua presença não substitui qualidade da evidência. |
| 20 | Título claro, preciso e identificador do conteúdo | Risco de alinhamento do título ao papel efetivamente demonstrado do Fator de Ajuste. |
| 21 | Epígrafe com autoria; formalidades de aprovação | Epígrafe atual atribuída; campos de aprovação são posteriores e não foram inventados. |
| 29–31 | Fundamentação, ordenação e exposição rigorosa dos procedimentos | F15–F19 e R01–R06 exigem atenção. |
| 32–33 | Resultados dos procedimentos propostos; fontes obrigatórias; “adaptado de” se aplicável | As fontes formais existem, mas conteúdo e procedência precisam ser corretos. |
| 33–35 | Discussão dos resultados, hipóteses e conclusões coerentes com objetivo/método | Riscos de causalidade, estabilidade e extrapolação precisam ficar delimitados. |
| 35 | Referências padronizadas de fontes consultadas, identificáveis | F12, F19–F21 mostram que o fechamento bibliográfico não é integral. |
| 69–71 | Linguagem formal, clara, objetiva; revisão; leitura atenta das referências | Exageros como “garantem”, “inviabiliza”, “qualquer modelo” e resultados trocados reduzem o rigor. |
| 71–72 | Estrangeirismos, expressões latinas e siglas | Há auditoria formal anterior da mesma versão; não foi substituída por uma nova certificação visual nesta etapa. |

Nas 76 páginas fornecidas não foi localizada uma cláusula que determine reprovação automática por X% de plágio, por uso de IA, por número específico de citações, por ausência de significância estatística ou por qualquer um dos achados individuais acima. Também não há, nesse arquivo, uma tabela completa de pesos e nota mínima da banca. Não se pode inventar essas regras.

“Formas implícitas de reprovar” foram interpretadas aqui como **pontos defensáveis de questionamento acadêmico derivados dos critérios de rigor do guia**, não sanções ocultas. Um erro bibliográfico isolado e uma inconsistência central do método não têm necessariamente o mesmo efeito. A decisão depende do regulamento aplicável, avaliação e correções exigidas pela instituição; este parecer não estima probabilidade ou nota.

### Formatação já documentada e limites de reaproveitamento

A matriz anterior possui 81 requisitos e a auditoria estrutural registra 86 verificações para o mesmo hash Word. São evidências reaproveitáveis de apresentação, não provas novas de sustentação científica. As conclusões “metadados reconciliados” e “garantindo que cada afirmação fosse ancorada” precisam ser limitadas pelos achados desta auditoria. Não converter 86 verificações ou 184 correspondências em “100% correto”.

Ficha catalográfica vazia e data/assinaturas de aprovação permanecem etapas posteriores, conforme decisão anterior do autor. Não foram tratadas como defeitos já comprovados da etapa atual. Recomendações como parágrafos de quatro a sete linhas e equilíbrio dos capítulos não foram convertidas em critérios automáticos de reprovação. As partes de DERS/GDD não são obrigações de uma monografia experimental só porque o trabalho também possui um software.

## Ordem de correção sugerida

1. Corrigir F01–F10 e as atribuições dos resultados: métrica, população, variável, série simulada e horizonte.
2. Refazer P1–P5 com evidência por célula; depois atualizar Tabela 1, Quadro 1, Figura 1 e conclusões de lacuna dependentes. Não gerar novos resultados experimentais para essa correção.
3. Fechar originais e versões, especialmente Cardoso 2022a, Pagani 2015, Eshelman 1991 e Soltani final se mantida sua referência de 2023. Corrigir autoria de Abebe/Goshu.
4. Resolver a declaração de preservação das planilhas e a origem da série ajustada, sem reconstruir registros como se fossem originais.
5. Harmonizar as garantias de fronteira temporal, preservação, causalidade e estabilidade; conservar os três protocolos separados.
6. Revisar resumo, conclusão e afirmação de atendimento dos objetivos após o corpo; conferir novamente referências e apresentação na cópia corrigida.

Todas as propostas deste parecer estão no estado **proposto**, não incorporado. A versão auditada permanece preservada.

## Arquivos que permitem conferir o parecer

- `matriz_50_referencias.md` e `.csv`: decisão e localizadores por obra, incluindo consulta limitada e referências sem chamada.
- `matriz_ocorrencias_avaliadas.csv`: as 184 ocorrências reconhecidas, texto, referência, página encontrada e avaliação de apoio. “Parcial” ou “não fechado” não é aprovação.
- `matriz_34_estudos.csv`: as 170 células originais P1–P5 com sinalização das contestações e dos limites da recodificação.
- `triagem_similaridade.json`: dez janelas curtas de oito palavras e seus candidatos de origem.
- `manifesto.json`: arquivos locais e hashes; Nelson consta com cobertura textual nula.
- `monografia_paragrafos.txt` e extrações por PDF: textos para localizar cada passagem; a extração não substitui o PDF.

## Fontes primárias eletrônicas complementares

Estas consultas são distinguíveis das fontes locais e de uma leitura integral da edição citada:

- [Cho et al., texto integral, especialmente seção 2.3 e Figura 2](https://aclanthology.org/D14-1179.pdf): sustenta a unidade com portas no encoder–decoder; não valida implementações ESNAUTO.
- [Hochreiter e Schmidhuber, publicação original disponibilizada pelos autores](https://www.bioinf.jku.at/publications/older/2604.pdf): identificação e resumo de LSTM consultados; não se declara leitura integral das 46 páginas nesta auditoria.
- [McKay, Beckman e Conover, reprodução do artigo, seção 2](https://www.asc.ohio-state.edu/statistics/comp_exp/jour.club/McKayConoverBeckman.pdf): sustenta estratificação por LHS; a reprodução está em edição retrospectiva de 2000, preservando autoria original de 1979.
- [Aria e Cuccurullo, página editorial do artigo bibliometrix](https://www.sciencedirect.com/science/article/pii/S1751157717300500): descrição do pacote e workflow; não comprova a execução local das análises.
- [Aria et al., comunicação de coautor sobre Biblioshiny/SAAS](https://lucadaniello.github.io/blog/biblioshiny-saas/): apoio à descrição da interface e identificação da obra; não foi tratada como artigo integral.
- [Pagani et al. 2015, página primária editorial e resumo](https://link.springer.com/article/10.1007/s11192-015-1744-x): não dá acesso integral à fórmula no conteúdo consultado.
- [Pagani et al., publicação posterior dos autores em Ciência da Informação](https://revista.ibict.br/ciinf/article/download/1886/3708/12368): etapas e limites de métricas; não substitui a edição de 2015 citada no alvo.
- [Gleick, artigo assinado, primeiro parágrafo](https://www.washingtonpost.com/archive/opinions/1987/10/18/making-sense-of-natures-mess/09f82e1d-5e92-4abf-81ee-9a60f6de1f89/): confirma a epígrafe atual. O cabeçalho informa 17/10/1987, embora o URL contenha o dia 18.
- [Holland, página da editora da reedição de 1992](https://mitpress.mit.edu/9780262581110/adaptation-in-natural-and-artificial-systems/): apoio temático à origem evolutiva dos AGs; não é consulta integral à primeira edição de 1975.
- [Diebold e Mariano, reprodução do artigo](https://users.ssc.wisc.edu/~behansen/718/DieboldMariano1995.pdf): identidade do artigo conferida; acesso textual limitado. O núcleo conceitual de igualdade de acurácia é compatível com a atribuição, mas isto não certifica as opções da implementação `forecast::dm.test`, que merecem sua própria referência.
- [Documentação primária de dm.test, argumentos e detalhes](https://pkg.robjhyndman.com/forecast/reference/dm.test.html): hipótese nula, perdas e modificação de Harvey–Leybourne–Newbold; apoia F24 e a identificação da implementação, sem repetir os testes locais.
