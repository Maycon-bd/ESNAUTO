import collections, hashlib, json, pathlib

out=pathlib.Path(__file__).resolve().parent
inv=json.loads((out/'inventario_41.json').read_text(encoding='utf-8'))
first=json.loads((out/'evidencias_rodada1.json').read_text(encoding='utf-8'))
by={(d['id'],d['dimensao']):d for d in first['decisoes']}
# Sínteses de leitura dirigida desta pesquisa. Não são afirmações de leitura
# integral nova nem prova de que o tema inexiste em toda a obra.
notes={
('D01','P3'):('PDF8–10,12–14','O artigo ajusta distribuições aos dados recebidos, incluindo médias semanais de ciberataques; não explicita operação de preparação temporal aplicada nessa análise. A agregação semanal caracteriza o dado recebido, sem procedimento de transformação atribuído aos autores.'),
('D02','P1'):('PDF4–9; página oficial Springer e nota de dados','Normal, Uniforme, Student-t, GED e Student-t assimétrica são associadas à ESN, mas sem ligação individualizada suficiente a Win ou W. Fórmulas das famílias não demonstram em qual matriz foram aplicadas. A nota oficial vincula BovDB como dados, sem código da ESN.'),
('D02','P4'):('PDF10–15; síntese experimental da prova local','A comparação apresentada varia famílias e fitness MAE/RMSE da ESN com AG. Menção bibliográfica a LSTM não é um contraste quantitativo com essa arquitetura.'),
('D03','P1'):('PDF11–12, subseção sobre ESN e redes correlatas','A revisão descreve aplicações e otimização de ESNs, sem individualizar lei de geração de Win/W nos trechos examinados. Leis dos otimizadores não são distribuições dos pesos.'),
('D03','P4'):('PDF11–12 e localização textual de LSTM no PDF48','A ocorrência localizada de LSTM consta da referência187. A passagem examinada não fornece comparação numérica qualificadora na mesma tarefa; é necessário distinguir a referência de resultados reproduzidos na revisão.'),
('D07','P4'):('PDF14–17, resultados e discussão','Os modelos A, B e C aplicam SVM com atributos fundamentalistas, técnicos e combinados. Acurácias56.46%,55.72%e70.7% são desses modelos, sem contraste com LSTM/GRU/Transformer nas passagens examinadas.'),
('D08','P1'):('PDF7–8,12–13, método e seção4.2','Win/Wres/Wenc são descritas como aleatórias e fixas; IS e SR escalam as matrizes. O filtro gaussiano da tensão é pré-processamento, não a lei dos pesos. Nenhuma família individualizada localizada nesses trechos.'),
('D12','P4'):('PDF8–11, tabelas5–10','Os treze modelos são configurações de MLP, MLP-GA e MLP-PSO; comparação quantitativa dessas configurações não satisfaz o critério específico de LSTM/GRU/Transformer.'),
('D13','P4'):('PDF8–11, tabelas4–5','Os comparadores são ESN convencional, AEESN, DeepESN, BrESN e CESNs com três topologias; DeepESN não é LSTM/GRU/Transformer. Nenhum contraste qualificável localizado nessas tabelas.'),
('D15','P4'):('PDF1–5; distinção em relação ao suplemento oficial','O artigo apresenta exemplo de geração de frequência e discussão de vantagens de treinamento, sem comparação numérica identificada com LSTM/GRU/Transformer. O suplemento do exemplo não implementa esses comparadores.'),
('D17','P4'):('PDF21–23, seções4.1–4.4; tabelas1–5','GPT-2/FinBERT classificam sentimento, ARIMA/Prophet/ETS fazem previsão temporal e estratégias combinadas geram retornos. Comparar classificadores de sentimento ou retornos combinados não isola uma comparação quantitativa de previsão temporal com Transformer.'),
('D19','P3'):('PDF48,64–68, métodos dos benchmarks','Geração Mackey-Glass, partições, washout, ruído de estado e reescala da matriz são descritos; não foi localizada operação concreta de preparação da série de entrada nessas passagens. Não confundir normalização do erro com normalização dos dados.'),
('D19','P5'):('PDF3,64–68,81–83; tabela6.1','Os experimentos sintetizados são MSO, Mackey-Glass, Sunspots e Laser. A menção introdutória a previsão de ações não identifica ativo/mercado submetido a análise. Não foi localizada evidência qualificadora de P5 no escopo examinado.'),
('D22','P1'):('PDF2–5, método de ESN-Lorenz','A fonte representa Win/W e descreve ajuste/esparsidade sem especificar família probabilística de inicialização. Evolução do Lorenz e inicialização dos dados não individualizam a lei de pesos.'),
('D22','P4'):('PDF2–5,8, revisão e tabela3','A revisão menciona RNNLSTM, mas a comparação numérica consultada é entre Lorenz e variantes de ESN. Não transportar números de outros artigos como se estivessem nesta tabela.'),
('D23','P1'):('PDF5–7 e HTML oficial arXiv2508.05416v1, seção4.1','A tabela1define distribuições para amostragem de hiperparâmetros e ruídoGaussiano, sem família de Win/W. Trecho extraído não visível do PDF6pertence a outra obra; foi rejeitado como evidência. Nenhum repositório do experimento foi identificado no HTML consultado.'),
('D23','P4'):('PDF9–12 e HTML oficial, resultados','Experimentos próprios comparam ESN, XGBoost e LastValue. Discussão qualitativa de LSTM em trabalhos anteriores não fornece números de uma comparação qualificadora no escopo lido.'),
('D24','P1'):('PDF2–3,10–11, definição e tabela6','As conexões aleatórias e a representação binária de topologia não individualizam a distribuição de valores de Win/W. Não converter matriz de conectividade em lei de pesos.'),
('D24','P3'):('PDF11–12, tabela6e seção4.4','Escalas de entrada/saída aparecem como hiperparâmetros. A apresentação dos benchmarks NARMA/Mackey-Glass/Lorenz não fornece tratamento temporal concreto aplicado que feche P3 nessas passagens.'),
('D24','P4'):('PDF8–12, síntese de métodos, métricas e benchmarks','A síntese consultada não apresenta comparação quantitativa identificada entre LSTM/GRU/Transformer na mesma tarefa; enumeração de métodos de otimização de ESN não é essa comparação.'),
('D24','P5'):('PDF12, figura6e descrição dos benchmarks','São nomeados benchmarks sintéticos e físicos, inclusive NARMA, Mackey-Glass, Lorenz, laser e turbofan. Não foi localizado ativo/mercado financeiro ligado à análise nessa síntese; não se inventa um mercado a partir da motivação de previsão.'),
('D27','P1'):('PDF3–5, equações1–8e algoritmo passo3','Win/W são geradas aleatoriamente e mantidas fixas. Variáveis normalmente distribuídas Q/beta e valores±1pertencem à movimentação dos pardais/SSA, não à geração dos elementos de Win/W.'),
('D28','P4'):('PDF5–7, seleção e regressão, nova leitura dirigida','O desenho examinado utiliza regressão linear múltipla por mínimos quadrados para PETR4. As tabelas2–3apresentam indicadores selecionados e valores previstos/reais; não foi localizada comparação quantitativa qualificadora com LSTM/GRU/Transformer nessas passagens.'),
('D29','P4'):('PDF7–10, tabelas3–6e seção4.5','Comparadores listados: GS-ARIMA, PSO-ESN, HAR-PSO-ESN, HAR e GS-MLP. Os números e testes desses modelos não são comparação com LSTM/GRU/Transformer.'),
('D30','P1'):('PDF8, discussão de SSA-ESN','A revisão relata otimização de ESN por SSA, sem lei individualizada de geração dos pesos. A fonte primária Tian/Pei também separa aleatoriedade de pesos das variáveis do otimizador.'),
('D30','P4'):('PDF2,8e17, números gerais e tabelas de síntese','A revisão apresenta72%paraLSTM e90%paraCNN em tarefas descritas de forma geral, além de discussões de superioridade. Não há na passagem vínculo inequívoco desses valores ao mesmo benchmark/protocolo. A tabela17lista métricas e vantagens, sem os resultados numéricos que estabeleçam o contraste exigido.'),
('D34','P1'):('PDF2–9, matrizes ESN e compressed sensing','A matriz gaussiana é a matriz de observação do compressed sensing. Win/W são inicializadas sem família especificada. A normalização espectral não determina sua lei de geração.'),
('D34','P2'):('PDF7–9, algoritmoOMP e configuração','OMP seleciona átomos/nós do reservatório e ajusta a representação; não descreve por si a escolha de hiperparâmetros da ESN. Valores fixos e compressão50% não provam busca/sensibilidade com critério de escolha.'),
('D34','P4'):('PDF9–12, experimentos caóticos e de ações','Os contrastes examinados são ESN versus CS-ESN. Sem comparação quantitativa com LSTM/GRU/Transformer localizada nessas páginas.')
}
for key,(loc,text) in notes.items():
    by[key]={'id':key[0],'dimensao':key[1],'antes':'?','proposta':'?','estado':'insuficiencia_mantida_no_escopo_lido','localizador':loc,'sintese':text,'leitura_integral_nova':False}
by['D19','P4']={
 'id':'D19','dimensao':'P4','antes':'?','proposta':'S','estado':'evidencia_nova_localizada_requer_conciliacao_editorial',
 'localizador':'Millea PDF30, tabela3.1e explicação de Evolino; Schmidhuber et al.(2007), PDF3e16, tabela2e seção3.4',
 'sintese':'Os quatro NRMSE de Evolino em Millea (0.00415,0.00804,0.110,0.166 para MSO2–5) correspondem exatamente à tabela2do trabalho original, que identifica PI-Evolino baseado em LSTM. Portanto a tabela de Millea inclui comparação numérica secundária com LSTM, sem novo experimento LSTM executado por Millea.',
 'url':'https://people.idsia.ch/~tino/papers/schmidhuber.neco07.pdf',
 'sha256_suplemento':'4cc201772dcfdc37586bf6b5f6fb794b71825180ac388497be1093328b29c0e9',
 'limite':'A identificação usa a cadeia original e igualdade dos quatro valores e tarefas, não o pressuposto de que qualquer Evolino seja LSTM. Não representa protocolos de otimização equivalentes; não prova superioridade financeira. Leitura dirigida, não integral das duas obras.'}
assert len(by)==41
rows=[]
for d in inv['celulas']:
    row=dict(d);row.update(by[d['id'],d['dimensao']]);rows.append(row)
counts=collections.Counter(d['proposta'] for d in rows)
data={'base':inv['base'],'sha256_base':inv['sha256_base'],'total_celulas':41,'propostas_com_nova_evidencia':counts['D']+counts['S'],'insuficientes_no_escopo_lido':counts['?'],'busca_integral_concluida':False,'word_alterado':False,'decisoes':rows}
(out/'decisoes_41_em_consolidacao.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
report=['# Busca das informações da matriz — em andamento','',f"Base v009, SHA256 `{inv['sha256_base']}`.",'','Três células possuem nova evidência documental;38mantêm informação insuficiente no escopo lido. O conjunto ainda não é declarado busca exaustiva concluída. Nenhuma revisão Word promovida.','', '| Fonte / célula | Proposta | Evidência e alcance |','|---|---|---|']
for d in rows:
    report.append(f"| {d['autor']} / {d['dimensao']} | {d['proposta']} | {d.get('localizador','')} — {d['sintese'].replace('|','/')} |")
(out/'relatorio_em_andamento.md').write_text('\n'.join(report)+'\n',encoding='utf-8')
print(dict(counts))
