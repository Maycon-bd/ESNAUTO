"""Decisões de leitura rastreáveis; não é classificador automático de artigos."""
from pathlib import Path
import json, csv, hashlib

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reports/correcao_parecer_integridade'
manifest=json.loads((ROOT/'reports/bibliometria_reconstrucao/base_reconstruida.json').read_text(encoding='utf8'))
sources={r['id']:r for r in manifest['records']}
decisions={}

def add(id,kind,scope,codes,*cells):
    assert id in sources and id not in decisions
    assert len(codes)==5 and len(cells)==5
    assert set(codes)<=set('DS?-')
    decisions[id]={'tipo':kind,'escopo_leitura':scope,'celulas':[
        {'dimensao':f'P{i+1}','codigo':code,'localizador':cell[0],'evidencia_e_limite':cell[1]}
        for i,(code,cell) in enumerate(zip(codes,cells))]}

add('D02','aplicacao_ESN','Prova local: PDF 4, 6–11 e 14; foco em método, dados, distribuições e comparações. Não declara leitura integral.','?DD?D',
 ('PDF 7 e 10–11, seções 3–4','Identifica Normal, Uniforme, t, GED e t assimétrica em ESNs; os trechos não individualizam a geração dos elementos de Win e W. Não excluir a fonte da discussão de distribuições, nem inventar uma lei de Win.'),
 ('PDF 7–9, seção 3','AG binário, 55 bits, seleção por fitness 40% treino/60% validação; seleção de cinco hiperparâmetros ESN.'),
 ('PDF 8, seções 3.1–3.2','Calcula retornos e variâncias a partir de preços diários/intradiários. O texto chama log-retornos, mas também mostra fórmula de retorno simples: evitar atribuir fórmula inequívoca sem ressalva.'),
 ('PDF 10–11 e 14, resultados e conclusão','Comparações localizadas são entre fitness e distribuições ESN; não foi localizada comparação quantitativa com LSTM/GRU/Transformer neste escopo.'),
 ('PDF 10, seção 4','ITSA4, B3, preços de janeiro/2001 a julho/2023. Não atribuir esses dados à PETR4.'))

add('D04','conjunto_de_dados','PDF 5–7, esquema, descrição da base e seção 4.1; não declara leitura integral.','--D-D',
 ('PDF 5–7, seções 3–4','Objeto é o conjunto de dados BovDB e seu esquema relacional; não estuda inicialização ESN.'),
 ('PDF 5–7, seções 3–4','Não há modelo ESN a otimizar no objeto destas seções.'),
 ('PDF 7, seção 4.1, equações 1–2','Descreve fator isolado close(d)/open(d+1), acumulação regressiva e transformação das colunas. Isso documenta a proposta BovDB, não comprova autoria da transformação dos arquivos ESNAUTO.'),
 ('PDF 6–7, seção 4','Avaliação/descrição de base e eventos, não comparação de previsão entre arquiteturas LSTM/GRU/Transformer.'),
 ('PDF 6–7, seção 4','B3, 1995–2020; exemplo VALE3 em torno de evento. Não confundir com Cardoso RBras 2022a.'))

add('D10','modelagem_distribuicoes','PDF 3–5, formulação, aplicação e tabelas; não declara leitura integral.','--D-D',
 ('PDF 3–4, seção 2','Misturas de distribuições de retornos; não inicialização de redes ESN.'),
 ('PDF 3–4, seção 2','Estimativa de misturas por ECM não é seleção de hiperparâmetros ESN.'),
 ('PDF 4, seção 3','Converte fechamentos em retornos logarítmicos multiplicados por 100 e separa subperíodos.'),
 ('PDF 4–5, seção 3 e Tabela 1','Comparadores são misturas Gaussianas/Gaussiana-Laplace/GED e estimativas VaR; não arquiteturas elegíveis de previsão.'),
 ('PDF 4, seção 3','DJIA, fechamentos de 04/01/2016 a 31/01/2022; S&P500 aparece como resultado de outro trabalho, não esta aplicação.'))

add('D13','aplicacao_ESN','PDF 4, 6–9 e 11–12: construção, sensibilidade, normalização e comparações.','DDD?D',
 ('PDF 4, definição de Win','Entradas não nulas de Win geradas por Uniforme(-1,1), escalonadas e mascaradas segundo o grupo. Não chamar essa lei de distribuição de W recorrente.'),
 ('PDF 6–8, seção 3.1 e Figura 5','Varia probabilidades de conectividade e grau médio; compara NRMSE em 50 realizações e identifica escolhas de conectividade. É análise de sensibilidade, não AG.'),
 ('PDF 7, equação 15','Normalização min–max [0,1] e preparação das séries multivariadas.'),
 ('PDF 8, Tabela 4; PDF 11, Tabela 5','Comparadores localizados são variantes ESN: convencional, AEESN, DeepESN, BrESN e agrupadas. Não são LSTM, GRU ou Transformer.'),
 ('PDF 8, Figura 6 e Tabela 4','NIFTYBEES, NSE/Índia; também experimentos não financeiros, que não devem ser confundidos com o conjunto financeiro.'))

add('D14','aplicacao_ESN_GRU','PDF 6–13: inicialização, arquiteturas, preparação, pseudocódigo e Tabela 2.','D?DDD',
 ('PDF 7, equações 9a–9b; PDF 12, Algoritmo 1','Win He usa randn e Xavier usa rand uniforme reescalado; inicializações caóticas seguem sequências normalizadas. A prosa PDF 8 descreve Xavier diferentemente da fórmula: manter a ressalva e não reclassificar sequência caótica como lei probabilística nomeada.'),
 ('PDF 11, Tabela 1; PDF 12, Algoritmo 1','Hiperparâmetros fixos são listados e Wout é estimado por Ridge. Comparar seis inicializações não descreve, por si, busca de hiperparâmetros; procedimento de seleção não fechado.'),
 ('PDF 11, seção 5.1, equação 16','Interpolação linear de ausentes e normalização min–max.'),
 ('PDF 13, Tabela 2','Resultados numéricos próprios ESN e GRU; outros comparadores são importados e não equivalem a novas execuções.'),
 ('PDF 13, Tabela 2','S&P500, ISEQ, XAU/USD, USD/JPY, Pci-Suntek e FTSE100.'))

add('D21','comunicacao_conceitual','PDF 1–2 integralmente disponíveis como texto: descrição, conclusão e referências.','--???',
 ('PDF 1–2','Comunicação conceitual sobre volatilidade; não apresenta ESN nem pesos de reservatório.'),
 ('PDF 1–2','Comunicação conceitual; não apresenta seleção de hiperparâmetros ESN.'),
 ('PDF 1, metodologias e desafios','Discute qualidade e lacunas de dados genericamente; não localiza operação concreta de preparação que satisfaça P3.'),
 ('PDF 1–2','Não há tabela de avaliação ou comparação quantitativa LSTM/GRU/Transformer. Citar artigos em referências não constitui comparação própria.'),
 ('PDF 1–2','Refere mercados e opções em geral, sem vincular ativo/índice identificado a uma análise específica.'))

add('D23','aplicacao_ESN','PDF 6–8, arquitetura, Tabela 1, atributos e avaliação; resultados delimitados pelo parecer e leitura anterior.','?DD?D',
 ('PDF 6–7, seção 4.1 e Tabela 1','Uniforme/Log Uniforme da Tabela 1 são priors de busca de hiperparâmetros. Ruído Gaussiano não é lei dos pesos. Figura reproduzida contém texto de outra fonte e não comprova inicialização executada por Sharma.'),
 ('PDF 8, seção 5, Hyperparameter Selection','TPE/Hyperopt para selecionar hiperparâmetros ESN e XGBoost.'),
 ('PDF 7–8, seção 4.3','Constrói médias móveis, desvios, RSI, MACD e razões de preços; janelas móveis com treino 15/30/60 e teste 10.'),
 ('PDF 8, seção 5.1; resultados PDF 9–12 consultados no parecer','Comparadores identificados são último valor e XGBoost. Menções LSTM/GRU na fundamentação não satisfazem o critério experimental.'),
 ('PDF 7–8, características e avaliação','Preços de Bitcoin; RMSE expresso em dólares.'))

add('D25','aplicacao_LSTM_GRU','PDF 3–7, teoria, método e quadro de resultados.','--DDD',
 ('PDF 5–6, seção 3.1.6','Estuda arquiteturas LSTM/GRU, não inicialização de ESN.'),
 ('PDF 6–7, seção 3.1.7','Grid search existe, mas para LSTM/GRU. Não conta como otimização de hiperparâmetros ESN.'),
 ('PDF 5, seções 3.1.4–3.1.5','MinMaxScaler [0,1] e sequências/janelas de preços de 60 dias.'),
 ('PDF 7, seção 4','Tabela apresenta MSE, MAE e R² para LSTM e GRU próprios; satisfaz P4 mesmo sem ESN.'),
 ('PDF 4, seção 3.1.1','Preço de fechamento do ouro, Yahoo Finance, dezembro/2017 a março/2024.'))

add('D26','aplicacao_ESN','PDF 3–8, descrição da arquitetura, dados, configuração e resultados.','???DD',
 ('PDF 3, seção 2','Win, Wr e Wback são descritos como aleatoriamente inicializados; não há lei probabilística identificada nos trechos lidos.'),
 ('PDF 5–6, seção 3.2','Fixa 500 unidades, raio 0,999 e esparsidade 0,02; não localiza regra de busca/seleção. Discutir importância dos parâmetros não basta.'),
 ('PDF 4–6, seções 3–3.2','O fluxo menciona coleta e limpeza, mas não especifica operação concreta de transformação/limpeza nos trechos consultados. Fechamento e fechamento ajustado aparecem separadamente; uso efetivo do ajustado não é inequívoco.'),
 ('PDF 6 e 8, seção 3.3, Tabelas 2–3','ESN versus LSTM simplificada em três grupos de dados; a simplificação é condição relevante.'),
 ('PDF 5, seção 3.1','Kweichow Moutai, mercado chinês, 360 pregões de novembro/2009 a abril/2011.'))

add('D27','aplicacao_ESN','PDF 3–7, construção, procedimento SSA, preparação e comparadores.','?DDDD',
 ('PDF 3–4, seções 2.1 e 2.3','Matrizes Win e W geradas aleatoriamente sem lei nomeada nesses trechos. A Normal no SSA governa posições dos agentes, não os pesos da ESN.'),
 ('PDF 4, seção 2.3; PDF 6, Tabela 3','SSA seleciona taxa de aprendizado e regularização; não atribuir otimização de todos os parâmetros ou das matrizes.'),
 ('PDF 4–5, seções 2.3 e 3.2','Normaliza dados em [0,1]; fonte informa que não realizou limpeza dos dados.'),
 ('PDF 5–6, seções 3.3 e 5','Compara BP, Elman, LSTM, ESN e SSA-ESN; tabelas de métricas especificadas nos resultados.'),
 ('PDF 5, Tabelas 1–2','Dez ações americanas e dez chinesas, incluindo INTC, QCOM e Vanke.'))

add('D29','aplicacao_ESN','PDF 4–8, descrição ESN, dados, preparação, modelos e resultados.','DDD?D',
 ('PDF 4, seção 3.2.4','Win, W recorrente e W feedback são inicializadas com distribuição Uniforme. Intervalo não individualizado nesse trecho.'),
 ('PDF 8, seção 4.4','HAR-PSO-ESN utiliza PSO para selecionar hiperparâmetros ESN.'),
 ('PDF 6–8, seções 4.1–4.3','Calcula volatilidade realizada com retornos intradiários, gera janelas e normaliza usando mínimo/máximo de treino.'),
 ('PDF 7, Tabelas 3–5','Comparadores localizados são GS-ARIMA, HAR, GS-MLP, PSO-ESN e HAR-PSO-ESN; não LSTM/GRU/Transformer.'),
 ('PDF 6, seção 4.1','CAT, EBAY e MSFT, volatilidades realizadas diárias derivadas de retornos de cinco minutos.'))

add('D32','aplicacao_RC','PDF 6–7 e 11–12 relidos; construção e discussão também consultadas na etapa anterior.','DDDDD',
 ('PDF 7, seção 4.1','Win tem distribuição Uniforme com escala dependente da dimensão de entrada; Wres é a adjacência da rede gerada. Não confundir lei de Win com topologia de Wres.'),
 ('PDF 7 e 11, configurações e Tabela 8','Explora topologias, tamanho, janela e taxa de aprendizado, selecionando configurações por índice. Não é evidência de causa única da topologia.'),
 ('PDF 6, Figura 4; PDF 7, seção 4.1','Constrói janelas móveis dos fechamentos como entradas de previsão de um passo. P3 admite construção de janelas, sem presumir normalização não documentada.'),
 ('PDF 7, seção 4.3','Executa RNN/LSTM nos mesmos períodos de teste e compara métricas; a segunda comparação usa modelos de outros estudos, separadamente.'),
 ('PDF 11, conclusão e Tabela 8','S&P500, NYSE, DJI, Nasdaq, FTSE100, Nikkei225 e SSE.'))

add('D01','modelagem_distribuicoes','PDF 1, 8–9 e 12–13: simulações, conjuntos reais e adequação; não declara leitura integral.','--?--',
 ('PDF 8–9, seção 8','Simulação e estimação da distribuição AGED; não gera pesos de ESN.'),
 ('PDF 8–9, seção 8','Otimização de máxima verossimilhança dos parâmetros AGED, não hiperparâmetros ESN.'),
 ('PDF 9, seção 8.2.1','Ajusta distribuições marginais a ataques cibernéticos semanais, colesterol e resistência de fibra de vidro. Não localiza uma operação de preparação temporal que satisfaça P3; uma amostra ordenável no tempo não basta.'),
 ('PDF 9 e 12, seção 8.2 e Tabela 8','Compara Normal, Laplace, GED e AGED; não arquiteturas de previsão.'),
 ('PDF 9, seção 8.2.1','As três aplicações são cibersegurança, saúde e materiais, sem ativo financeiro. Referência bibliográfica a finanças não constitui aplicação própria.'))

add('D05','aplicacao_quantica','PDF 3–5, 12–13: dataset, preparação, configurações, análise fora da amostra.','--DDD',
 ('PDF 12, Tabela 4, arquiteturas','Modelos QTCNN, QCNN, QLSTM e baselines clássicos; não inicialização de pesos ESN.'),
 ('PDF 12, Tabela 4','Configurações/otimizadores de modelos quânticos e LSTM/Transformer não são seleção de hiperparâmetros ESN.'),
 ('PDF 4–5, seção II','Ajuste de features por eventos, engenharia de atributos, winsorização, z-score transversal e sequências. A fonte informa que o Target oficial não é reajustado: não extrapolar o ajuste dos atributos para o alvo.'),
 ('PDF 12–13, configurações e seção IV-B','Compara LSTM e Transformer com modelos quânticos por Sharpe fora da amostra; teste de 22 dias limita a generalização.'),
 ('PDF 3–4, seção II','Conjunto JPX Tokyo Stock Exchange/Kaggle, ações japonesas e universo filtrado.'))

add('D06','aplicacao_redes_profundas','PDF 2–3: desenho, dados, arquiteturas e comparação; apêndices de dados 16–18 consultados anteriormente.','--DDD',
 ('PDF 3, seção 2.2','Arquiteturas MLP, CNN, LSTM e Transformer; não inicialização ESN.'),
 ('PDF 3, seção 2.2','Busca de taxa e decaimento para pares arquitetura/otimizador; não ESN.'),
 ('PDF 2, seção 2.1','Calcula proxy Garman–Klass e log-variância a partir de OHLC; usa janelas de volatilidades. Dados CRSP e ajustes corporativos discutidos nos apêndices.'),
 ('PDF 2–3, contribuições e seção 2.2','Avalia 12 pares arquitetura/otimizador com LSTM e Transformer e 13 sementes; compara NMSE. Não transportar equivalência do estudo para PETR4.'),
 ('PDF 2, seção 2.1','Constituintes históricos do S&P500/CRSP, 2000–2024.'))

add('D07','aplicacao_SVM','PDF 2–3, 10–12 e 15–19 consultados no parecer e na retomada; variáveis e resultados.','--D?D',
 ('PDF 2–3, objeto do artigo','Modelo SVM para classificação do comportamento de ações; não inicialização ESN.'),
 ('PDF 2–3 e seção de métodos','Seleção/treinamento de SVM, não hiperparâmetros de ESN. Não contar recomendação futura de redes como método executado.'),
 ('PDF 11–12, Tabelas 2–3 e variável dependente','Constrói indicadores fundamentalistas e técnicos com preços ajustados a splits/dividendos e classes de comportamento.'),
 ('PDF 15–19, resultados e conclusões','Resultados localizados são de modelos SVM com conjuntos de variáveis; redes neurais aparecem como trabalhos futuros. Não localizada comparação experimental LSTM/GRU/Transformer no escopo lido.'),
 ('PDF 10, Tabela 1; PDF 11–12','Amostra de empresas brasileiras da B3. F1 agregado não é resultado específico da PETR4.'))

add('D08','aplicacao_ESN_nao_financeira','PDF 6–7, 10, 12–13 e 20: modelo, otimização, dados e comparação.','?DDS-',
 ('PDF 7 e 13, seções 3.1 e 4.2','Pesos Win/Wres/Wenc aleatórios e fixos, sem lei probabilística nomeada nos trechos consultados. Não inferir distribuição dos pesos do nome do filtro de dados.'),
 ('PDF 10 e 13, seções 3.2 e 4.2','AG seleciona input scaling, spectral radius e leak rate de cada reservatório.'),
 ('PDF 12, seção 4','Suaviza as tensões FC1/FC2 com filtro de média móvel ponderada Gaussiana. Não atribuir wavelet de trabalhos relacionados ao procedimento deste artigo.'),
 ('PDF 20, Tabela 6','LSTM RNN, ARIMA e Fusion têm valores provenientes de [36]; são comparação quantitativa secundária, não novas execuções correspondentes.'),
 ('PDF 6 e 12, problema e dados','Degradação de células PEMFC, testes IEEE PHM 2014; não mercado financeiro.'))

add('D09','modelagem_series_estatistica','PDF 5–6 e 8–10: famílias e aplicação própria em futuros de carbono.','--D-D',
 ('PDF 9–10, seção 4','Distribuições dos dados e modelos Box–Jenkins/GBM/Tsallis; não pesos ESN.'),
 ('PDF 9–10, seção 4','Modelagem/seleção estatística de séries, não hiperparâmetros ESN.'),
 ('PDF 9, seção 4.1','Log-diferenciação para estabilizar o conjunto de preços; modela a distribuição resultante.'),
 ('PDF 10, Tabela 1','Compara Log-diff., ARIMA, variantes GARCH, GBM e Tsallis, não arquiteturas LSTM/GRU/Transformer.'),
 ('PDF 9, seção 4','Preços de contratos futuros de emissões de carbono entre 01/05/2012 e 01/05/2022.'))

add('D12','aplicacao_MLP','PDF 5–8: dados, indicadores, arquitetura e treinamento por AG/PSO; resultados examinados no parecer.','--D?D',
 ('PDF 6, seção 3.2.1','MLP feedforward, não ESN; aleatoriedade dos pesos MLP não satisfaz P1.'),
 ('PDF 7–8, seções 3.2.2–3.2.3','AG e PSO estimam pesos/vieses da MLP. Não é seleção de hiperparâmetros de ESN.'),
 ('PDF 5, seção 3.1 e Tabela 4','Constrói nove indicadores técnicos, incluindo médias, momentum e RSI, com fórmulas e critério de seleção por estudos/especialistas.'),
 ('PDF 6–8, modelos; discussão no parecer','Comparações próprias localizadas são MLP-GA e MLP-PSO e suas configurações. Não localiza LSTM/GRU/Transformer como baseline experimental.'),
 ('PDF 5–6, seção 3.1','Borsa Istanbul BIST100, março/1996 a fevereiro/2020, 5.968 pregões.'))

add('D17','sentimento_e_estrategias','PDF 8–9 e 21/28 relidos; demais métodos/resultados pertinentes consultados no parecer.','--D?D',
 ('PDF 21/28, tipos de modelos e tabelas','FinBERT/GPT-2 para sentimentos e modelos estatísticos/indicadores; não inicialização ESN.'),
 ('PDF 21/28','Sem modelo ESN em otimização no objeto dessas comparações.'),
 ('PDF 8–9, seções 2.2–2.4','Alinha notícias a dias de negociação/defasagens, limpa texto, integra por data e categoriza retornos. Não confundir classificação de notícias com direção do índice.'),
 ('PDF 21/28, Tabelas 1–2','Tabela 1 compara Transformer-LLMs na tarefa de sentimento de notícias; a previsão temporal da Tabela 2 usa ARIMA/Prophet/ETS. Não comprova comparação entre arquiteturas elegíveis na mesma tarefa de previsão de série.'),
 ('Título; PDF 8–9 e 21','S&P500, retornos/estratégias e notícias de fontes financeiras identificadas.'))

add('D28','aplicacao_regressao_linear','PDF 4–7: preparação, indicadores, regressão e resultados.','--D?D',
 ('PDF 6, método de mineração','Regressão linear múltipla, não reservatório ESN.'),
 ('PDF 6, método de mineração','Mínimos quadrados para regressão, não seleção de hiperparâmetros ESN.'),
 ('PDF 4–5, processo KDD e Tabela 2','Verifica inconsistências, constrói indicadores e seleciona variáveis por correlação/Pearson e determinação. Valores iguais em dias distintos não foram excluídos como duplicatas.'),
 ('PDF 6–7, método e resultados','O estudo avalia a regressão linear; não localiza comparação quantitativa LSTM/GRU/Transformer no escopo examinado.'),
 ('PDF 4 e 6–7','PETR4/Bovespa, Yahoo Finance; as datas finais diferem entre trechos da fonte, portanto o código não confirma um período único.'))

add('D33','aplicacao_LSTM_GRU_Transformer','PDF 4–6: metodologia, dados e comparação; não declara leitura integral.','--DDD',
 ('PDF 5, seção 3.2','Arquiteturas LSTM/GRU/Transformer, não ESN.'),
 ('PDF 5, seção 3.2','Treinamento/tuning dessas arquiteturas não satisfaz seleção de hiperparâmetros ESN.'),
 ('PDF 4, seção 3.1 e Tabela 2','Descreve limpeza e diferenciação/ADF; há inconsistência entre descrição de dados do site Tesla e tabela OHLC. A codificação de presença não endossa qualidade/procedência.'),
 ('PDF 5, Tabela 3; PDF 6, resultados','Compara métricas LSTM/GRU/Transformer. Há inconsistências internas entre RMSE e MSE e entre interpretação e tabela; não transportar os números como benchmark confiável.'),
 ('PDF 4, seção 3.1','Tesla, observações OHLC 2015–2024; a fonte descreve o período contraditoriamente como nove/quase cinco anos. Apenas a identificação do ativo é contada.'))

add('D03','revisao','PDF 1, 10–11, 17, 19 e 28: escopo, aplicações, bases e técnicas; não declara leitura integral.','?SS?S',
 ('PDF 28, aplicações ESN-PSO/DRESN/GWO-ESN','Há discussão de ESNs, mas não uma lei de geração de Win/W individualizada nos trechos lidos.'),
 ('PDF 28','Descreve estudos ESN-PSO, DRESN-GA e GWO-ESN. Evidência secundária de otimização ESN; não contar toda otimização HONN como ESN.'),
 ('PDF 10–11 e 28','Revisa expansões funcionais, dados virtuais e enriquecimento de treinamento em modelos para séries; evidência secundária, não nova preparação experimental própria.'),
 ('PDF 10–11 e 28','Contrastes qualitativos com MLP/FLANN/HONN não comprovam comparação quantitativa específica com LSTM/GRU/Transformer no escopo examinado.'),
 ('PDF 17 e 19, agrupamento de datasets','Identifica BSE, DJIA, Nasdaq, TAIEX, FTSE, câmbio, Bitcoin e outros mercados como aplicações revisadas, não nova amostra própria.'))

add('D11','tese_modelagem_distribuicoes','Seções 4.5.3–4.5.4, PDF 85/88; texto auxiliar normalizado dos códigos numéricos. Não declara leitura integral da tese.','--D-D',
 ('PDF 85/88, seções 4.5.3–4.5.4','Objeto são misturas GND/CMGND de retornos, não pesos ESN.'),
 ('PDF 85/88','Estimação e seleção de misturas estatísticas por LRTS/BIC, não hiperparâmetros ESN.'),
 ('PDF 85, seção 4.5.3; PDF 88, Data','Converte fechamentos em retornos por diferença de log natural; a fonte distingue estatística JB de critérios AIC/BIC.'),
 ('PDF 85/88, modelos e medidas','Compara famílias de distribuições e modelos de mistura, não arquiteturas de previsão elegíveis.'),
 ('PDF 85 e 88','S&P500 e STOXX50E, 2007–2023; também 52 ações que compuseram STOXX50E, 2010–2023. Não substituir a conferência DJIA 2022 por esta aplicação.'))

add('D15','artigo_teorico_com_demonstracao','PDF 1–5: definição, gerador de frequência, formalismo e recomendações.','?S??-',
 ('PDF 1 e 3','Conexões aleatórias e matrizes são definidas, sem família probabilística explicitada nos trechos lidos.'),
 ('PDF 4–5, Practical issues','Explicita otimização conjunta, validação, regularização e prática de experimentação manual. É recomendação metodológica, não busca financeira própria.'),
 ('PDF 3–5','Washout, regularização e escalonamento interno são discutidos; não foi localizada preparação concreta de uma série que se possa somar automaticamente a P3.'),
 ('PDF 5, Significance','Discute treinamento recorrente e benchmarks sem comparação quantitativa LSTM/GRU/Transformer no escopo lido.'),
 ('PDF 1–2, demonstração','Aplicação ilustrativa é gerador de frequência ajustável, não ativo financeiro.'))

add('D16','aplicacao_RC','PDF 7–8 e 16–17: dados, preparação, tuning e Tabela 3.','?DDDD',
 ('PDF 16, seção 4.1.4','Lista conectividade e escala de entrada, sem lei probabilística dos elementos de Win/W identificada nesses trechos.'),
 ('PDF 16, seção 4.1.4','Hyperopt/TPE para unidades, leak rate, conectividades e regularização, minimizando métrica em validação.'),
 ('PDF 8, seção 3.2','Tratamento de ausentes, remoção de outliers e normalização [0,1] descritos; a codificação não prova ausência de vazamento no estudo.'),
 ('PDF 16–17, seção 4.2 e Tabela 3','Compara ARIMA, LSTM, GRU e RC. A alegação textual de superioridade em todas as métricas não coincide com a Tabela 3, especialmente NRMSE; não reproduzir a generalização.'),
 ('PDF 7–8 e 16–17','Preços diários de petróleo bruto; benchmark específico não é individualizado nestes trechos. Não inventar WTI/Brent.'))

add('D18','RC_nanofotonico','PDF 3, 6–8 e 14: preparação, parâmetros por índice e comparações secundárias.','-?DSD',
 ('PDF 3, sistema e máscara','Entrada modulada por máscara caótica e reservatório optomecânico; não se apresenta geração probabilística de uma matriz de pesos neuronais Win/W como objeto experimental.'),
 ('PDF 7–8, seção 4.1 e Tabela 3','Configura kfb/kinj por índice visando melhor desempenho, mas o procedimento de seleção não está suficientemente individualizado no trecho consultado.'),
 ('PDF 6, equação 7','Normalização e denoising DWT com db3/três níveis; descarta primeiras cem observações no treinamento.'),
 ('PDF 14, discussão e Table 6 indicada','Compara DS com resultados LSTM/RNN/híbridos provenientes de [4] e outras referências; não são novas execuções próprias desses comparadores.'),
 ('PDF 6, seção 3.1 e Tabela 2','SHSECI, SZSECI, Nasdaq Composite e FTSE100.'))

add('D19','tese_ESN_nao_financeira','PDF 28–31, seção 3.3 e Tabelas 3.1–3.3; trechos anteriores consultados no parecer.','DD??-',
 ('PDF 28 e 31, seção 3.3','Gera W inicial Uniforme(0,1) e transforma por orth; também compara W Gaussiana média zero/desvio 0,2. Win é vetor de uns no exemplo. Lei pré-transformação não é distribuição final de W.'),
 ('PDF 30–31, Tabela 3.2 e experimentos','Varia tamanhos e conectividade em repetições e compara probabilidades de atingir limiares de NRMSE: exploração/sensibilidade explícita, não AG empregado pelo autor.'),
 ('PDF 28–31','A transformação ortonormal é sobre pesos, não pré-processamento da série. Não foi localizada outra operação concreta de preparação neste escopo.'),
 ('PDF 30, Tabela 3.1 e texto Evolino','Tabela importa resultados de outros métodos. A frase de que Evolino também treina LSTM não identifica inequivocamente a arquitetura do valor importado; não contar como comparação LSTM própria.'),
 ('PDF 28–31','Problema MSO de osciladores sobrepostos, não aplicação a preços financeiros.'))

add('D20','modelagem_volatilidade','Leitura visual do PDF digitalizado: físicas 7–8 e 10–11/13–15, impressas 352–353 e 355–356/358–360.','--D-D',
 ('PDF 7–8 e 11','GED para inovações de modelo de heterocedasticidade; não pesos ESN.'),
 ('PDF 11, impressa 356','Critério Schwarz para ordem ARMA e máxima verossimilhança, não hiperparâmetros ESN.'),
 ('PDF 11, impressa 356 e nota 12','Usa retornos logarítmicos, extrai Treasury bills mensais e aproxima taxa diária sem risco para calcular excessos de retorno.'),
 ('PDF 11 e 13–15','Modelagem ARCH/ARMA e análise de estimativas; não arquiteturas neurais LSTM/GRU/Transformer.'),
 ('PDF 11, impressa 356; PDF 15, Figura 3','Índice de mercado CRSP ponderado por valor, retornos diários julho/1962 a dezembro/1987.'))

add('D22','ESN_sobre_trajetoria_simulada','PDF 4–6: construção, seleção de tamanho e resultados; condições iniciais consultadas no parecer.','?D??S',
 ('PDF 4, matrizes e treino','Win/Wr fixas e escalonamento Win, mas sem família probabilística identificada no escopo lido.'),
 ('PDF 6, Number of Neurons','Declara validação cruzada entre tamanhos para escolher 300 neurônios. Demais detalhes/contradições do treinamento não são resolvidos por esta marca.'),
 ('PDF 4–6','Trajetórias geradas por Lorenz e escolhas de treino são descritas; não localiza operação de preparação temporal distinta da geração/partição que satisfaça P3.'),
 ('PDF 6, avaliação e Tabela 2 indicada','Compara ESN e trajetórias/modelo Lorenz; não localiza baseline LSTM/GRU/Transformer.'),
 ('PDF 4 e 6; condições iniciais no parecer','Associa valores de Bitcoin às condições iniciais; resultados são de trajetórias simuladas, não previsão de uma série financeira observada. S indica vínculo contextual apenas.'))

add('D24','revisao_ESN','Preprint v1 2022: PDF 1, 6, 8, 11–13, objeto, técnicas e benchmarks.','?S???',
 ('PDF 11, Tabela 6','Descreve escalonamento/topologia e pesos binários de conectividade, não uma lei probabilística de Win/W localizada neste escopo.'),
 ('PDF 8 e 11–13','Revisa PSO, AG e outras técnicas e parâmetros; evidência secundária, frequência não é ranking de eficácia.'),
 ('PDF 12, datasets','Descreve NARMA/Mackey-Glass/Lorenz e geração matemática; isso não especifica preparação de séries observadas conforme P3.'),
 ('PDF 11–13','Lista objetivos de erro e métodos, sem comparação quantitativa LSTM/GRU/Transformer localizada no escopo.'),
 ('PDF 12–13, benchmarks','Datasets de referência caóticos, vento e outros; não foi identificado ativo financeiro específico no escopo consultado.'))

add('D30','revisao_IA_financeira','PDF 8, 10, 12–16: exemplos de métodos, datasets e preparação; não declara leitura integral.','?SS?S',
 ('PDF 10, seção 5.2','SSA-ESN é descrita secundariamente, mas não uma lei probabilística de Win/W.'),
 ('PDF 10 e 12','Apresenta SSA para hiperparâmetros de ESN [18]; classificação S, não nova execução própria.'),
 ('PDF 8 e 15–16','Revisa normalização, testes de estacionariedade e tratamento de outliers em dados financeiros; procedimentos são dos estudos revisados.'),
 ('PDF 10 e 13–16','Discute LSTM/GRU/Transformer e suas aplicações, mas os trechos não fecham comparação quantitativa na mesma tarefa que satisfaça P4.'),
 ('PDF 14, Tabela 1','Identifica S&P500, Nasdaq e Dow Jones como datasets das aplicações revisadas.'))

add('D31','RC_optico','PDF 3–8: sistema, métodos, dados, atributos e identificação dos baselines.','??DDD',
 ('PDF 3–4, Optical RC','Win é aleatória e Wres representa o efeito do sistema óptico; não localiza família probabilística de Win. Wcor é ponderação de atributos por correlação, não distribuição aleatória dos pesos.'),
 ('PDF 3 e 5','O texto diz otimizar ganhos RC; a busca em grade detalhada se refere aos baselines ML. Não atribuir automaticamente essa busca à seleção dos parâmetros ópticos.'),
 ('PDF 6–7, seção 3','Constrói indicadores, atributos macroeconômicos/defasagens e pesos de correlação; normaliza entradas por z-score.'),
 ('PDF 5 e 8','Executa LSTM entre os baselines; LSTM é identificada como Best ML para quatro/dez passos. As comparações Best ML de um passo usam Lasso, não sempre LSTM.'),
 ('PDF 5, Tabela 1','Sete séries identificadas por ^HSI, ^IXIC, ^N225, ^NYA, MME=F, UKX.L e VTHR. A classificação genérica da fonte não transforma todos os símbolos em índices de ações.'))

add('D34','aplicacao_CS_ESN','PDF 2–3 e 9–11: arquitetura, compressão, experimentos e dados.','??D?D',
 ('PDF 2–3, seção 2.1','Matrizes inicializadas e reescalonadas, sem lei de seus elementos identificada nos trechos consultados. Uniformidade de vazamento espectral não é lei dos pesos.'),
 ('PDF 2 e 9–11','Propõe compressão de estados/nós e usa parâmetros fixos; otimização estrutural não documenta, por si, busca de hiperparâmetros com critério de seleção.'),
 ('PDF 9 e 11, seções 4.1–4.2','Escala sequência Logistic e padroniza dados de 200 ações. Compressão de estados é registrada separadamente da preparação das séries.'),
 ('PDF 10–11, Tabela 2 e seção 4.2','Contrastes localizados são ESN e CS-ESN, sem arquitetura LSTM/GRU/Transformer identificada.'),
 ('PDF 11, seção 4.2','200 ações obtidas da Shanghai Stock Exchange, dados de 17 anos. Mercado e conjunto identificados, sem inventar tickers ausentes do trecho.'))

def main():
    rows=[]
    for id,s in sources.items():
        source_path=ROOT/'Artigos citados'/s['arquivo_pdf']
        assert hashlib.sha256(source_path.read_bytes()).hexdigest()==s['sha256_pdf'],source_path
        decision=decisions.get(id)
        for i in range(5):
            cell=decision['celulas'][i] if decision else {'dimensao':f'P{i+1}','codigo':'PENDENTE','localizador':'','evidencia_e_limite':''}
            rows.append({'id':id,'arquivo_pdf':s['arquivo_pdf'],'sha256_pdf':s['sha256_pdf'],
                         'tipo':decision['tipo'] if decision else '',
                         **cell,'escopo_leitura':decision['escopo_leitura'] if decision else ''})
    assert len(rows)==170
    payload={'criterios':'criterios_matriz_p1_p5.md','n_fontes':34,'n_celulas':170,
             'n_recodificadas':sum(c['codigo']!='PENDENTE' for c in rows),
             'recodificacao_registrada_para_todas_as_celulas':len(decisions)==34,
             'validacao_integral_das_fontes':False,'decisoes':rows}
    (OUT/'matriz_recodificada.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    with (OUT/'matriz_recodificada.csv').open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    if len(decisions)==34:
        from collections import Counter
        summary=[]
        for dim in range(1,6):
            counts=Counter(r['codigo'] for r in rows if r['dimensao']==f'P{dim}')
            assert sum(counts.values())==34
            summary.append({'dimensao':f'P{dim}','direta':counts['D'],'secundaria':counts['S'],'insuficiente':counts['?'],'nao_aplicavel':counts['-']})
        with (OUT/'contagens_recodificadas.csv').open('w',encoding='utf8',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=list(summary[0]));writer.writeheader();writer.writerows(summary)
    print(f"{len(decisions)}/34 fontes; {payload['n_recodificadas']}/170 células recodificadas. "
          'Contagens finais e derivados Word ainda não atualizados.')

if __name__=='__main__':main()
