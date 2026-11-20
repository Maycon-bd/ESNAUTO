"""Confronto dirigido de afirmações de previsão com as fontes originais."""
import hashlib,json
from pathlib import Path
from docx import Document

root=Path(__file__).resolve().parents[1]; out=root/'reports/fechamento_integral_20261029'; doc=root/'reports/monografia/trabalho/fechamento_integral_20261029.docx'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(doc)=='ee6e179ab0ba157fb9f1348a1ac75c38813be767c3a27367481727f59641af50'
D=Document(doc); idx=json.loads((out/'indice_citacoes_atuais_lote32.json').read_text(encoding='utf8')); refs={r['id']:r for r in idx['registros']}
items=[
 (189,'R32','Liu, Lin e Rojas (2025)','PDF 20–21 e 28, Tabela 1','A acurácia de 75,56% está na classificação de sentimento com notícias Benzinga, não como acurácia de previsão de preços. A distinção do texto é pertinente.'),
 (190,'R49','Xiao, Deng e Bi (2024)','PDF 2 e 4, Tabela 2','A comparação envolve Tesla, LSTM, GRU e Transformer. A Tabela 2 declara ausência de valores faltantes; o artigo também faz referência genérica a tratamento, sem avaliação de imputação identificada.'),
 (197,'R49','Xiao, Deng e Bi (2024)','PDF 5, Tabela 3','Para LSTM: MSE 260,8710984 e RMSE 26,0917386, cuja raiz quadrada não coincide; para Transformer também há divergência. O trecho delimita a inconsistência a alguns modelos.'),
 (197,'R13','Cortesi et al. (2026)','PDF 1–2 e Figuras 1–3','A fonte relaciona escolhas de otimizador a funções distintas apesar de desempenho agregado semelhante, no contexto de previsão financeira. Não atribui esse resultado a Xiao.'),
 (206,'R48','Wang et al. (2021)','PDF 1–2, 7–11 e Tabelas 5 e 8','Sete índices e topologias ER, SW e SF; desempenho muda com índice e métrica. Há comparação própria com RNN/LSTM e discussão de outros estudos, com limitações dos protocolos.'),
 (208,'R47','Wang, Bu e Huang (2025)','PDF 2, 5–6, 8 e 13, Tabela 1 e Figura 9','Sete séries, indicadores financeiros e macroeconômicos, previsões em 1, 4 e 10 passos e comparação com melhor método de ML. A descrição de atraso não é extrapolada a todos os regimes.'),
 (209,'R31','Liu et al. (2022)','PDF 6, 8–10 e 14–15','Estudo nanofotônico usa simulação numérica; índices de China, EUA e Reino Unido, discussão de previsão conservadora e efeito de ancoragem. Não confere superioridade geral em tempo real.'),
 (207,'R38','Ribeiro et al. (2021)','PDF 1, 3, 6 e 10–11','Três ações e volatilidade realizada com retornos intradiários de cinco minutos; horizontes 1, 5 e 21 dias e modelos comparadores. A referência a volatilidade não comprova caos.'),
 (232,'R38','Ribeiro et al. (2021)','PDF 4','Pesos de entrada, recorrentes e de realimentação são descritos como inicializados aleatoriamente por distribuição uniforme.'),
 (232,'R23','Hariharan, Suresh e Chandrasekar (2025)','PDF 4','As entradas não nulas de Win usam uniforme entre -1 e 1 com fator de escala; conexões ausentes recebem zero.'),
 (232,'R48','Wang et al. (2021)','PDF 7','Pesos de entrada uniformes; matriz recorrente é matriz de adjacência gerada pela rede. Escalonamento ou conectividade não identificam por si só lei de pesos.'),
 (247,'R38','Ribeiro et al. (2021)','PDF 1, 4 e 10–11','HAR-PSO-ESN, distribuições de inicialização e testes Friedman/Nemenyi são relatados; desempenho é descrito como melhor na maioria, não universal.'),
 (248,'R48','Wang et al. (2021)','PDF 7 e 10–11','Entrada inicializada uniformemente, reservatório por adjacência, saída treinada por RMSProp, e topologia mais eficaz varia entre índices.'),
 (249,'R48','Wang et al. (2021)','PDF 7 e 10–11, Tabelas 5 e 8','Dados permitem afirmar competitividade e variação da melhor topologia entre índices, sem afirmar uma distribuição ótima geral.'),
 (210,'R50','Zhang et al. (2021)','PDF 2, 9 e seções experimentais posteriores','Estudo apresenta compressão dos estados, sequência logística e dados acionários, com comparação de erros; não estabelece preservação geral de picos ou caos financeiro.')]
rows=[]
for p,r,anchor,where,evidence in items:
 text=D.paragraphs[p].text; assert anchor in text,(p,anchor)
 ref=refs[r]; path=root/ref['arquivo_fonte']; assert sha(path)==ref['sha256_fonte']
 rows.append({'ancora':f'P_atual{p:04}','texto_atual':text,'fonte_id':ref['fonte_id'],'arquivo_fonte':ref['arquivo_fonte'],'sha256_fonte':sha(path),'localizador':where,'evidencia':evidence,'diagnostico':'condizente no escopo da afirmação examinada'})
f=out/'afirmacoes_previsao_lote34.json'; assert not f.exists(); f.write_text(json.dumps({'base':'v005','sha256_base':'2af31abca4e3ba9fd5caf7cd161e55472dc94edc136cdf89732c0d0401118d6b','sha256_rascunho':sha(doc),'escopo':'15 relações entre trechos e nove fontes locais; outras afirmações nos mesmos parágrafos exigem avaliação própria. Usa registros anteriores de leitura integral e verifica os trechos identificados; não certifica ausência de plágio.', 'registros':rows,'acao':'Nenhuma alteração adicional no Word com base nos pontos examinados.'},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
s=out/'estado_meta.json'; state=json.loads(s.read_text(encoding='utf8')); state['ultimo_registro_de_leitura']=str(f.relative_to(root)); state['proxima_passagem']='Continuar conferência das demais afirmações do índice por fonte, sobretudo referências suplementares e lacunas de atribuição; revalidar Guia.'; s.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf8'); print('Conferidas 15 relações e registrados localizadores.')
