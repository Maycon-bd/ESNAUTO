# Reexame dirigido das 43 células de informação insuficiente

Base examinada: v004; SHA256 do DOCX `110b1d19223e23f9e4b27e4c2b0ba74e92072ebcc3f1cd4ec4f0200bba059f5b`. Os 24 PDFs locais conservaram os hashes do manifesto anterior. As instruções dos artigos foram tratadas como conteúdo das fontes, não como comandos do autor.

Foram reexaminadas as 43 células em escopos identificados abaixo: duas mudam de código (Liu B. (2022), D18/P2 → D; Hassaan et al. (2025), D14/P2 → S); 41 conservam informação insuficiente. Não são 41 leituras automaticamente pendentes nem 41 erros comprovados. Também não se afirma que os temas inexistam nas obras. A extração integral foi usada para localização; a leitura é dirigida às passagens declaradas. Não se certifica a matriz inteira como leitura integral de todos os artigos.

A matriz completa mantém 170 decisões: 76 D, 12 S, 41 ? e 41 não aplicáveis. Em P2: 11 D, 5 S, 3 ? e 15 não aplicáveis. Os critérios permanecem os mesmos; não foi criado código de ausência para eliminar interrogações.

## Atenção à camada textual de D23

A página 6 de Sharma contém texto extraído que não aparece na página renderizada. A inspeção visual prevaleceu: não foram usados os parágrafos adicionais sobre leis Uniformes e outro estudo para codificar Win/W. A figura reproduzida, o ruído de estado e a amostragem de hiperparâmetros são objetos distintos. Imagem preservada em paginas_visuais/D23_p06.png.

## Onda 5: acervo informado pelo autor

Declaração recebida nesta revisão: “Saídas originais? tudo q saiu está no projeto, foi rodado aqui”. O projeto é tratado como acervo preservado informado pelo autor; não se solicita novamente envio de saídas. O relatório local docs/09_onda_5_ajustes_empiricos_easyfit.md contém as 15 execuções GA_RUN_0053–0067 e seus resultados compilados. Esses resultados foram encontrados. A declaração sobre o local de execução é registrada como informação do autor.

A conferência anterior em reports/esclarecimentos_autor_20261029/conferencia_onda5.json examinou 616 arquivos/membros de 45 ZIPs e documentou a granularidade recuperada. Sua existência não é confundida com correspondência estabelecida entre cada linha e matrizes/vetores/registros por execução. Essa limitação de verificação independente permanece; não implica que as execuções não ocorreram, não exige que existam arquivos adicionais e não é resolvida pela afirmação de local de execução. Não foram executados treinos, GA ou DM. Os resultados experimentais da monografia são preservados.

## Decisões por célula

| Célula | Antes → depois | Página/seção física do PDF | Evidência e limite |
|---|---|---|---|
| D01/P3 | ? → ? | PDF 9, aplicações | Os dados reais são recebidos para ajuste marginal da AGED. Não foi localizada nesta aplicação uma operação concreta de preparação temporal; ajuste de uma distribuição não satisfaz P3. |
| D02/P1 | ? → ? | PDF 4–9, contextualização e método | As famílias de distribuições são associadas à ESN, mas as passagens não individualizam sua geração em Win ou W. Não inferir essa ligação apenas da comparação de famílias. |
| D02/P4 | ? → ? | PDF 10–15, tabelas e conclusão | As tabelas experimentais consultadas comparam configurações e distribuições de ESN. A referência bibliográfica a LSTM não documenta comparação quantitativa na mesma tarefa. |
| D03/P1 | ? → ? | PDF 11–12, revisão de modelos | O tratamento das ESNs descreve aplicações e otimização, sem identificar lei probabilística de Win/W nos trechos examinados. Leis dos algoritmos evolutivos não são leis dos pesos da ESN. |
| D03/P4 | ? → ? | PDF 11–12 e triagem textual das tabelas de modelos | Comparações entre HONNs, FLANNs, ESNs e outros modelos não identificam no escopo consultado uma comparação numérica qualificadora com LSTM/GRU/Transformer. Não se afirma ausência na obra inteira. |
| D07/P4 | ? → ? | PDF 14–17, resultados e conclusão | Os modelos A/B/C diferem nos atributos empregados por SVM. As métricas desses modelos não constituem comparação com LSTM/GRU/Transformer. |
| D08/P1 | ? → ? | PDF 8 e 13, equações 1–5 e seção 4.2 | Win, Wres e Wenc são descritas como aleatórias. A família probabilística de Win/Wres não é especificada nesses trechos; filtro gaussiano da série é outro objeto. |
| D12/P4 | ? → ? | PDF 8–11, tabelas 5–10 | O conjunto de treze configurações é de MLP, MLP-GA e MLP-PSO; funções de ativação e otimizadores não identificam LSTM/GRU/Transformer no comparativo examinado. |
| D13/P4 | ? → ? | PDF 8 e 11, tabelas 4–5 | Os resultados de ações e geração solar consultados comparam variantes de ESN. Esses números não fecham o critério de comparação com LSTM/GRU/Transformer. |
| D14/P2 | ? → S | PDF 2, revisão de estudos; PDF 11, tabela 1 | A fonte relata o uso de algoritmo de otimização aritmética para hiperparâmetros de SCDESN no estudo citado como [1]. É discussão secundária específica de ESN. A tabela própria lista valores fixos e não prova busca própria; por isso S, não D. |
| D15/P1 | ? → ? | PDF 1–3, definição e treinamento da ESN | Conexões aleatórias são descritas sem lei probabilística individualizada para Win ou W. Não completar a fonte com configurações de outras publicações de Jaeger. |
| D15/P3 | ? → ? | PDF 1–9, sobretudo 2–5 | Washout de estados, ruído de estados, regularização e escalas de controle não documentam, por si, uma operação concreta aplicada à série de entrada. Mantida a insuficiência para P3. |
| D15/P4 | ? → ? | PDF 1–9, sobretudo 2 e 5 | As vantagens e relações com outras redes são conceituais; não foi identificada comparação numérica qualificadora na mesma tarefa nas passagens lidas. |
| D16/P1 | ? → ? | PDF 13–14, definição da ESN e equações 16–17 | As matrizes são nomeadas, mas não recebem família probabilística de inicialização nessas passagens. A formulação genérica sobre matrizes aprendidas não autoriza reconstruir a lei de Win/Wres. |
| D17/P4 | ? → ? | PDF 21 e 23, tabelas 1–5 e discussão | GPT-2/FinBERT são avaliados em classificação de sentimento; o comparativo temporal usa ARIMA, Prophet e ETS. Retornos de estratégias combinadas não isolam um Transformer como previsor temporal no mesmo benchmark exigido por P4. |
| D18/P2 | ? → D | PDF 7–8 e 10–13, seção 4.3 e figuras 4–5 | A própria pesquisa explora parâmetros físicos do RC e apresenta mapas de NMSE/RMSE/MAE/MAPE, discutindo regiões de menor erro e configurações por índice. Satisfaz análise de sensibilidade com critério de desempenho. Não implica AG, ótimo global ou seleção em validação separada. |
| D19/P3 | ? → ? | PDF 47–48, 63–68, benchmarks e dados | Nas seções consultadas de Mackey-Glass, laser e manchas solares há geração/apresentação de séries, partições e washout. Transformações de pesos ou estados não estabelecem operação concreta de preparação da série bruta. Leitura dirigida, não integral das 90 páginas. |
| D19/P4 | ? → ? | PDF 30, tabela 3.1 e discussão de Evolino | Há números importados para Evolino, mas o trecho não identifica inequivocamente a arquitetura daquele resultado como LSTM. A observação de que Evolino também treina LSTM não basta para converter o comparativo em S. |
| D21/P3 | ? → ? | PDF 1–2, texto completo de duas páginas | O tratamento é conceitual: volatilidade e desvio-padrão não são uma operação de preparação temporal documentada e aplicada a dados identificados. |
| D21/P4 | ? → ? | PDF 1–2, texto completo de duas páginas | Não há, no texto examinado, tabela ou comparação numérica qualificadora entre previsores LSTM/GRU/Transformer na mesma tarefa. |
| D21/P5 | ? → ? | PDF 1–2, texto completo de duas páginas | O mercado é abordado genericamente; não há ativo/índice e mercado identificados e ligados a uma análise documentada. |
| D22/P1 | ? → ? | PDF 2–5, definições e método | Os pesos são aleatórios/fixos e há escala e ajuste espectral. Isso não identifica a família de geração dos elementos de Win/W. |
| D22/P3 | ? → ? | PDF 2–5 e 8, literatura e experimento de Lorenz | O experimento usa trajetórias de Lorenz e condições iniciais associadas a Bitcoin. Perturbar condição inicial não descreve preparação de preços observados. Menção a detecção de outliers em outro modelo não explicita operação aplicada à série que feche P3 no escopo examinado. |
| D22/P4 | ? → ? | PDF 2–5 e 8, literatura e comparação experimental | Menções gerais a LSTM e resultados entre variantes de ESN não estabelecem uma comparação numérica qualificadora com LSTM/GRU/Transformer na mesma tarefa. |
| D23/P1 | ? → ? | PDF 5–7; conferência visual obrigatória da página 6 | Na página visível, a figura 3 é reproduzida de Li et al.; o ruído gaussiano é de estado, não lei de Win/W. A extração textual da página 6 contém parágrafos adicionais não visíveis sobre leis Uniformes e outro estudo: foram descartados como artefato da camada textual. Não inferir lei por padrão de biblioteca. |
| D23/P4 | ? → ? | PDF 9–12, resultados | Os comparativos consultados são com último valor e XGBoost. Não sustentam o critério específico de LSTM/GRU/Transformer. Texto não visível da camada de extração não foi usado como evidência. |
| D24/P1 | ? → ? | PDF 2–3 e 10–11, definição e tabela 6 | Pesos aleatórios e matriz binária de conectividade não especificam a lei probabilística de Win/W; conectividade e distribuição de elementos são objetos distintos. |
| D24/P3 | ? → ? | PDF 11–12, tabela 6 e benchmarks | Escalas/deslocamentos aparecem como parâmetros, e NARMA/Mackey-Glass/Lorenz como benchmarks. A descrição consultada não documenta transformação concreta da série de entrada que feche P3. |
| D24/P4 | ? → ? | PDF 8–12, síntese e benchmarks | Contagens de técnicas de otimização e desempenho relatado genericamente não constituem comparação quantitativa identificável com LSTM/GRU/Transformer na mesma tarefa. |
| D24/P5 | ? → ? | PDF 12, figura 6 e descrição de datasets; figura conferida visualmente | A figura e o texto identificam benchmarks sintéticos e domínios físicos, incluindo NARMA, Mackey-Glass, Lorenz, laser e turbofan. Não identificam ativo financeiro e mercado vinculados à análise nesse escopo. |
| D26/P1 | ? → ? | PDF 3, definição da ESN | Win, Wr e Wback são inicializadas aleatoriamente, sem família probabilística individualizada no trecho. Não reconstruir pela implementação presumida. |
| D26/P2 | ? → ? | PDF 5–7, experimento e configuração | Valores de tamanho do reservatório, raio espectral e esparsidade são fixados. Variação do tamanho do conjunto de treino/teste não identifica procedimento para selecionar hiperparâmetros da ESN. |
| D26/P3 | ? → ? | PDF 4–7, coleta e dataset | A fonte menciona coleta/limpeza e apresenta dados de fechamento/ajustados, mas não explicita a operação de preparação temporal. Partições 120/240/300 de treino e 40/80/100 de teste não bastam para P3. |
| D27/P1 | ? → ? | PDF 3–5, ESN e SSA | Win/W são geradas aleatoriamente. Distribuições normais descritas na SSA pertencem às posições/perturbações dos agentes, não são explicitamente leis dos pesos da ESN. |
| D28/P4 | ? → ? | PDF 5–7, seleção e regressão | O experimento consultado usa seleção por correlação e regressão linear no WEKA. Lista conceitual de redes não equivale a comparação numérica com LSTM/GRU/Transformer. |
| D29/P4 | ? → ? | PDF 7–10, seção 4.5 e tabelas 3–6 | Os comparadores são GS-ARIMA, PSO-ESN, HAR-PSO-ESN, HAR e GS-MLP. Os resultados/rankings dessas arquiteturas não fecham P4. |
| D30/P1 | ? → ? | PDF 8, discussão de SSA-ESN | A revisão descreve ajuste de tamanho/raio espectral por SSA, sem informar lei probabilística individualizada de Win/W. |
| D30/P4 | ? → ? | PDF 2, 8 e 17; páginas 2 e 17 conferidas visualmente | Percentuais de LSTM e CNN na introdução vêm de estudos/tarefas distintos; as tabelas consultadas listam modelos e nomes de métricas sem pareamento numérico qualificável. A superioridade narrada de SSA-ESN sobre LSTM não vem acompanhada de números identificáveis nessa síntese. |
| D31/P1 | ? → ? | PDF 3–4, equações 1–2 e montagem óptica | Win é aleatória e Wres decorre do reservatório físico; a lei de geração dos elementos não é identificada nessas passagens. |
| D31/P2 | ? → ? | PDF 3–5 e triagem dirigida das seções de resultados | Há intenção de otimizar ganhos alfa/beta, mas o procedimento explícito de validação cruzada e grid search refere-se aos comparadores ML/LSTM. A intenção de otimizar RC, sem procedimento identificado, não fecha P2. |
| D34/P1 | ? → ? | PDF 2–5 e 7–9; fluxogramas das páginas 4–5 conferidos visualmente | A matriz gaussiana descrita é a matriz Phi de sensoriamento comprimido. Não é identificada como lei de Win/W. Os fluxogramas inicializam os parâmetros sem família explícita. |
| D34/P2 | ? → ? | PDF 7–9, OMP e configuração | OMP estima coeficientes na representação comprimida; não é apresentado como busca de hiperparâmetros ESN. A configuração fixa não documenta seleção com critério. |
| D34/P4 | ? → ? | PDF 9–12, ESN versus CS-ESN; página 11 conferida visualmente | Os comparativos experimentais consultados são de ESN e CS-ESN. Não há comparação numérica qualificadora com LSTM/GRU/Transformer nesse escopo. |

Não constitui certificação de ausência de plágio, validação integral das citações ou aprovação acadêmica. A correção linguística pode ocorrer com esta revisão documentada, preservando a base vigente e devolvendo mudanças para conciliação.

## Conferência da cópia Word

76 páginas e 45 verificações estruturais sem falha. 50 referências e 151 ocorrências reconhecidas, sem chamadas órfãs nos padrões examinados; isso não prova fidelidade de conteúdo. As 170 células do Quadro 1 correspondem à matriz revisada. Apenas um parágrafo, três células e a Figura 1 mudaram em relação à v004. As 73 páginas idênticas à v004 conservaram a inspeção anterior; as três diferentes (PDF 34–36) foram abertas e conferidas. Resultados experimentais, resumos e demais tabelas foram preservados.
