"""Consolida julgamentos editoriais explícitos, sem alterar a monografia."""
from pathlib import Path
from docx import Document
import json,csv,re,hashlib,sys
sys.stdout.reconfigure(encoding='utf8')
R=Path(__file__).resolve().parents[1];O=R/'reports/auditoria_citacoes_integridade_20261028'
d=Document(R/'reports/monografia/MayconGarciaSilva_monografia_FASOFT_conferida.docx')
refs=[p.text for p in d.paragraphs if p.style.name=='Referencias']
# A = apoio localizado ao núcleo da atribuição, não certificação integral da obra.
# P = parcial; D = divergência específica; N = consulta primária não fechada; U = sem chamada.
data='''0|A/P|Abebe PDF 1 e 10–12|AGED, assimetria e comparação de ajustes apoiados; iniciais da referência erradas (F20). Aplicações não são evidência financeira direta.
1|A/P|Araújo PDF 4–9|GA, ESN e cinco distribuições apoiados. Prova de autor; paginação final não conferida. Contradiz lista de apenas cinco fontes (F05).
2|A limitado|Página editorial bibliometrix; resumo|Apoia descrição do pacote/workflow; artigo integral não foi consultado nesta auditoria. Não comprova execução local.
3|A limitado|Comunicação primária do coautor; DOI 101837|Interface Biblioshiny e SAAS apoiados; publicação integral não consultada. Execução local exige registros próprios.
4|P|Behera PDF 1, 12, 28, 39, 41|Revisão HONN/otimização apoiada; não garante estabilidade ou superioridade universal de GA/PSO. Conferir iniciais.
5|N|RBras 2022a não localizado no acervo de PDFs|RMSE 0,4987, período e protocolo dependem do texto primário. Tese de 2025 não o substitui (F19).
6|A/P|BovDB PDF 1 e 7–8, categorias na p. 12|BovDB e razão/acumulação do fator apoiados; exceções detalhadas e aplicação efetiva no ESNAUTO não são automaticamente demonstradas (F17/R03).
7|A|ENMC_texto; figuras PDF 6–8|Referência de formatos de frequência/visualização pertinente; não é fonte dos números da coleção atual.
8|A|KBS_texto; figuras PDF 6–7|Referência de formatos gráficos pertinente; possível adaptação de protocolo de busca exige identificação própria.
9|U|Tese Cardoso local, 176 páginas|Não foi localizada chamada Cardoso 2025 no corpo. Fonte comparada na triagem de atribuição; não substituir Cardoso 2022a.
10|A/P|Chen PDF 1, 4–5, 13–14|QTCNN/JPX e Sharpe apoiados; limitar a 22 dias OOS e ao benchmark do preprint v2 de 2026.
11|A|Texto primário ACL, seção 2.3, PDF 2–3|Unidade com portas e encoder–decoder apoiados. Não constitui evidência de desempenho financeiro.
12|A|Cortesi PDF 1–2 e 16–18|Multiplicidade de funções com perdas semelhantes e dados CRSP/ajustes apoiados.
13|D/P|Costa/Lunkes PDF 12, 15, 17, 19|Preço ajustado apoiado; F1 agregado não é F1 específico PETR4; recomendação é de redes neurais em geral (F01/F07).
14|A/P|Deng PDF 2, 10, 13, 20|ESN empilhada com GA e aplicação PEMFC apoiadas; comparadores de trabalhos anteriores e limites do domínio precisam ser preservados.
15|A/P|Dewick PDF 1–6|Distribuições e regressão apoiadas; não há comparação experimental com LSTM/GRU/Transformer que justifique P4 do quadro (F15).
16|A limitado|Identidade do artigo 1995; acesso textual primário limitado|Núcleo da hipótese de igualdade de acurácia é compatível; não se certificam detalhes de forecast::dm.test apenas com esta referência.
17|P|Duttilo tese PDF 14–19, capítulos 3–4|MGND e retornos/normalidade apoiados; DJIA e HQIC de 2022 não devem ser concentrados na chamada de 2023 (F23).
18|A|Duttilo/Gattone PDF 1 e 4–6|DJIA, mistura GED, AIC/BIC/HQIC apoiados; ano 2022 é consistente com o encontro citado.
19|A/P|Ecer PDF 1, métodos e resultados|MLP–GA/PSO, BIST100 e métricas apoiados; não é otimização de ESN nem garantia geral de estabilidade.
20|N|Identificação do capítulo/DOI; acesso integral não obtido|A atribuição de inspiração CHC está prudentemente limitada, mas conteúdo do capítulo original não foi fechado nesta auditoria.
21|A|Artigo assinado Washington Post, primeiro parágrafo|Frase e autoria da epígrafe conferidas; data do cabeçalho 17/10/1987.
22|A/P|Hariharan PDF 4, 7–10|Clusters, entrada uniforme e NIFTYBEES apoiados; separar Win de W e revisar definição P4 (DeepESN versus LSTM/GRU/Transformer).
23|A/P|Hassaan PDF 1, 3–4, 7–8, 12–13|Sequências caóticas, Xavier/He e seis datasets apoiados; não inferir superioridade uniforme em toda métrica/dataset.
24|A limitado|Publicação original disponibilizada pelos autores; resumo|Introdução de LSTM e problema do gradiente apoiados no resumo; não houve leitura integral das 46 páginas.
25|P|Página MIT Press da reedição 1992|Origem evolutiva e tema de AG compatíveis; primeira edição 1975 não foi consultada integralmente.
26|U|Catálogo de publicações do autor, GMD Report 148|Obra identificada, mas sem chamada Jaeger 2001 localizada no alvo. Texto integral específico não auditado.
27|A/P|Jaeger PDF 1–5|Reservatório fixo/readout e Ridge apoiados; não garante estabilidade ou vantagem universal de tempo (F13).
28|A|Kumar PDF 1–5 e comparação experimental|RC, petróleo, ARIMA/LSTM/GRU e métricas apoiados. Online 2024 e fascículo 2025 são versões distintas.
29|A/P|Lampugnani L0402–L0415 e tabelas do Word|PETR4, GA, opção de não tratar adicionalmente e comparação documental apoiados; conferir escala e datas antes de equiparar protocolos.
30|D/P|Liu B. PDF 6–8, 10, 14|Sistema e mercados apoiados; flutuações violentas aumentam erros e não sustentam imunidade a regimes nem comparação geral com software (F10).
31|D/P|Liu H. PDF 1, 21, 28|Integração sentimento/indicadores apoiada; 75,56% é classificação de sentimento Benzinga, não direção S&P500 (F02).
32|A|McKay et al., seção 2 da reprodução do artigo|Estratificação LHS apoiada; reprodução em retrospectiva de 2000 de trabalho original 1979. Não prova ganho de LHS nesta pesquisa.
33|P|Millea seção 3.3, PDF 24–26|Resultados de ortonormalidade em tarefas específicas apoiados; definição AG e generalizações da área não tiveram apoio localizado (F11).
34|A/P|Nelson PDF 7–8, pp. impressas 352–353, leitura visual|GED, parametrização e uso em EGARCH apoiados. Não determina distribuição ótima de pesos nem comprova prioridade histórica absoluta (F22).
35|N/P|Página primária de Pagani 2015 e publicação posterior dos autores|Proposta do método apoiada no resumo; fórmula integral de 2015 e ranking executado não fechados (F18).
36|A|Ping PDF 1–2|Relevância de prever volatilidade para risco/investimento apoiada. Não confundir volatilidade com preço.
37|A/P|Ribeiro PDF 1, 3–6, resultados|HAR–PSO–ESN e volatilidade Nasdaq apoiados; comparadores ARIMA/HAR/MLP/ESN não validam a marca P4 da definição atual.
38|D/P|Seddik PDF 4–7|Lorenz e ESN apoiados; são trajetórias simuladas com condições associadas a Bitcoin, não teste direto de preços observados (F09).
39|D/P|Sharma PDF 7–12|ESN/Bitcoin/TPE apoiados; distinguir treino 15/30/60 e teste dez, bem como hiperparâmetros e pesos (F03/F04).
40|N/P|Soltani PDF 1–2, 6, 8, 11–13, preprint v1 2022|74 itens e métodos apoiados nesta versão; edição final 2023 não lida; lacuna financeira/distribuições e ranking de eficácia não demonstrados (F12).
41|A|Sudiatmika/Putra PDF 3–6|Arquiteturas recorrentes e discussão de eficiência da GRU apoiadas com caráter contextual; não equivalem a garantia geral de desempenho.
42|D/P|Sun PDF 1, 5–6, 8–9|Comparação ESN/LSTM simplificada apoiada; fechamento ajustado não inequivocamente comprovado; RMSE não deve ser convertido em tempo (F08).
43|A/P|Tian PDF 3–5, 12|SSA–ESN e vinte ativos apoiados; não garante eliminação de mínimos locais e superioridade universal.
44|D/P|Timbó PDF 5, 7–8, 10|Regressão/correlação apoiadas; taxa de acerto por tolerância não é acerto direcional (F06).
45|A/P|Vishwas PDF 1, 15, 20–21|Revisão e desafios computacionais apoiados; não demonstra inviabilidade universal de backpropagation nem estabilidade garantida da ESN.
46|A/P|Wang F. PDF 5–8 e métricas|RC óptica, ponderação correlacional, sete índices e avaliações apoiados; evitar extrapolar causalidade ou superioridade uniforme.
47|A/P|Wang W. PDF 2 e 7, resultados|Sete índices, topologias, entrada uniforme e comparadores apoiados; não qualificar topologia como causa isolada preponderante sem controle correspondente.
48|A/P|Xiao PDF 2 e 4–6|Tesla/LSTM/GRU/Transformer apoiados; não demonstra por ablação a afirmação de P0204 sobre ausência de feedback do mercado.
49|A/P|Zhang PDF 2–3 e 8|Compressão de estados/nós da ESN apoiada; não transpor automaticamente discussão de amostragem de sinais para resultado de preços.'''
rows=[]
for line in data.splitlines():
    i,status,loc,note=line.split('|',3);i=int(i)
    rows.append({'id':f'R{i+1:02d}','paragrafo_referencia':f'P{505+i:04d}','referencia':refs[i],'avaliacao':status,'evidencia':loc,'parecer':note})
assert len(rows)==len(refs)==50
def csvout(name,items):
    with (O/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(items[0]));w.writeheader();w.writerows(items)
csvout('matriz_50_referencias.csv',rows)
md=['# Conferência das 50 referências','', 'A: apoio localizado ao núcleo específico; P: parcial; D: divergência em atribuição; N: consulta primária não fechada; U: chamada não localizada. Combinações preservam essas distinções. Nenhum A certifica toda a obra ou todos os usos.','', '| ID | Obra | Avaliação | Evidência | Decisão |','|---|---|---|---|---|']
for r in rows:md.append('| '+' | '.join([r['id'],r['referencia'],r['avaliacao'],r['evidencia'],r['parecer']])+' |')
(O/'matriz_50_referencias.md').write_text('\n'.join(md)+'\n',encoding='utf8')
with (O/'inventario_ocorrencias.csv').open(encoding='utf-8-sig',newline='') as f:occ=list(csv.DictReader(f))
byref={r['referencia']:r for r in rows}
overrides={194:'Divergência F06: taxa por tolerância não é direcional; reconhecimento de limitações não localizado.',195:'Divergências F01/F07: F1 da amostra e recomendação genérica, não PETR4/RNN específica.',196:'Divergência F02: sentimento Benzinga não é acerto direcional S&P500.',203:'Parcial F13: custo elevado não demonstra inviabilidade geral.',204:'Parcial: Cortesi apoia multiplicidade; Xiao não isola causalmente feedback do mercado.',208:'Parcial F14: revisão não garante elevação substancial em toda tarefa.',212:'Parcial/divergência F08: LSTM simplificada e fechamento declarado; uso ajustado não fechado.',213:'Parcial F14: comparações apoiadas; causa preponderante não isolada.',214:'Apoio ao modelo e comparadores; retirar extensão causal/caos não demonstrada.',215:'Apoio ao sistema/métricas; ressalva de abrangência F14.',216:'Divergência F10: flutuações aumentam erro; tempo real não comparado genericamente.',217:'Parcial: compressão de estados não equivale automaticamente a efeito de subamostragem de preços.',218:'Parcial: NRMSE menor em condições examinadas; não presumir teste estatístico causal.',219:'Parcial/divergência F09: conferir separadamente Hassaan e simulação Lorenz em Seddik.',220:'Parcial F03: significância por janela e comparador deve ser preservada.',223:'Parcial F11: ortonormalidade apoiada; definição de AG não localizada em Millea.',224:'Parcial F14: vinte ativos/SSA apoiados; evitar mínimos locais não é garantia.',225:'Apoio ao experimento PEMFC; restringir comparação e interpretação ao protocolo.',226:'Parcial F14: MLP-GA/PSO não garante estabilidade nem otimiza ESN.',227:'Parcial/versão não fechada F12: 74 no preprint, sem ranking causal de eficácia.',228:'Apoio ao núcleo GA/ESN/distribuições; contribuição própria exige procedência.',230:'Parcial: generalização da área não demonstrada por uma dissertação.',232:'Apoio GED/EGARCH; prioridade histórica absoluta não demonstrada (F22).',233:'Apoio à parametrização GED e relato correlato; separar os dois objetos.',234:'Parcial F23: separar tese 2023 de estudo DJIA/HQIC 2022.',235:'Apoio à AGED e aos ajustes nas aplicações da fonte; não é resultado financeiro.',236:'Parcial: Dewick apoia distribuição; lacuna atribuída a Soltani não localizada.',240:'Divergência F04/F05: pesos, escalonamento e distribuição de hiperparâmetros confundidos.',243:'Parcial F17: fator apoiado; condições detalhadas por evento não todas explicitadas na fonte.',245:'Separar fontes: Sun não demonstra inequivocamente ajustado; CRSP em Cortesi apoiado.',246:'Parcial: preço ajustado em Costa apoiado; necessidade para qualquer modelo extrapola.',248:'Método identificado, execução histórica e original integral não fechados (F18).',252:'Núcleo Araújo apoiado; preservação dos melhores resultados exige harmonizar R05.',254:'Núcleo HAR-PSO-ESN apoiado; comparar à definição P4 (F15).',255:'Apoio aos sete índices, topologias e entrada uniforme; equação foi lida com glifos incompletos.',256:'Apoio descritivo restrito a vários cenários; sem superioridade geral.',257:'Apoio ao SSA-ESN/ativos; revisar abrangência de consistentemente (F14).',260:'Divergência F03/F04: tamanhos de treino e amostragem de hiperparâmetros.',264:'Parcial F13: evitar BPTT não garante ausência de instabilidade numérica.',265:'Parcial F12: frequência de métodos não é eficácia causal; versão final não lida.',266:'Parcial F12/F16: lacuna do portfólio exige extração corrigida, não imputação aos autores.',267:'Parcial F16: conclusão do portfólio depende da recodificação e da procedência.',278:'Apoio à escolha de formatos e descrição de ferramentas; não valida números locais.',309:'Apoio ao BovDB; amplo estudo nacional não demonstrado por uma única referência.',310:'Parcial F19: Cardoso 2022a sem original; Lampugnani tem datas descritas com diferenças.',311:'Parcial F17/R03: regra BovDB apoiada; aplicação/categorias requerem registros.',312:'Parcial: razão fator e opção declarada de Lampugnani apoiadas; execução local exige procedência.',328:'Base conceitual apoiada em parte; faixas 55 bits são decisões locais; Cardoso2022a não fechado.',329:'Apoio aos conceitos de reservatório/readout/Ridge; não é validação do código executado.',332:'LHS apoiado em McKay; Holland primeira edição não consultada integralmente.',333:'N: original Eshelman não consultado integralmente; caracterização limitada é prudente.',351:'Apoio conceitual à igualdade de acurácia; implementação forecast requer referência própria.',365:'N/P F18: método identificado, busca/contagens históricas não comprovadas pelas planilhas ausentes.',367:'N F18: fórmula original integral e ranking aplicado não fechados.',372:'Apoio à descrição das ferramentas; versão/execução dependem dos registros locais.',373:'Apoio como modelos de visualização; não é autoria dos dados locais.',450:'Fonte conceitual compatível; números remetem à execução controlada, não ao artigo.',457:'Separar Cardoso2022a N de Lampugnani apoiado documentalmente.',460:'Comparação parcialmente fechada: original Cardoso2022a pendente; conferir tabelas Lampugnani.',461:'Comparação com Cardoso2022a permanece não fechada (F19).',462:'Cardoso2022a sem primário; Lampugnani apoia declaração de não tratar adicionalmente.',477:'Comparação com fontes parcialmente fechada; não validar Cardoso2022a por repetição.',493:'Parcial: afirmação de objetivos atendidos requer revisão da literatura/procedência.',494:'Apoio à opção declarada de Lampugnani; aplicação própria exige R03.',496:'Comparação descritiva prudente, mas número Cardoso2022a não fechado.',562:'D F04/F05: somente cinco e Sharma não sustentam distribuição Win.',565:'D F15: Ecer é MLP, não otimização de ESN.',568:'Parcial F15/F17: objeto de pré-processamento precisa ser uniforme.',571:'Parcial F15: exemplos específicos apoiados; total P4 não fechado.',574:'Parcial F16: mercados apoiados em parte; raridade não é inferível da seleção sem limites.',1013:'N F19: identificação de fonte na tabela não comprova RMSE nem protocolo.'}
for r in occ:
    pi=int(r['paragrafo'][1:]);rr=[byref[x] for x in r['referencias'].split(' || ') if x in byref]
    r['avaliacao_fonte']='; '.join(x['id']+': '+x['avaliacao'] for x in rr)
    if pi in overrides:r['avaliacao_ocorrencia']=overrides[pi]
    elif 581<=pi<=784:r['avaliacao_ocorrencia']='Rótulo autor–ano identificado; conteúdo das cinco células da linha exige a matriz P1–P5. Não é validação científica só do nome.'
    else:r['avaliacao_ocorrencia']=' | '.join(x['parecer'] for x in rr)
    r['evidencia_localizada']=' | '.join(x['evidencia'] for x in rr)
csvout('matriz_ocorrencias_avaliadas.csv',occ)
# Quadro 1: a tabela é localizada por cabeçalho e conteúdo, sem pressupor número fixo.
t=next(t for t in d.tables if any('P₁' in c.text for c in t.rows[0].cells))
axes=[]
contested={('Ribeiro',4):'F15: comparadores ARIMA/HAR/MLP/ESN; não sustenta comparação própria com LSTM/GRU/Transformer.',('Dewick',4):'F15: métodos estatísticos; comparação experimental P4 não localizada.',('Jaeger',4):'F15: exposição conceitual; comparação experimental P4 não localizada.',('Hariharan',4):'F15: há DeepESN; definição atual especifica LSTM/GRU/Transformer. Requer regra explícita.',('Sharma',1):'F04: distribuição de busca de hiperparâmetros não identifica geração de Win.',('Abebe',3):'F15: ajuste de distribuições em dados não financeiros não é automaticamente pré-processamento temporal financeiro.',('Seddik',5):'F09: distinguir condições associadas a Bitcoin de trajetórias observadas de preços.'}
for row in t.rows[1:]:
    name=row.cells[0].text
    for a in range(1,6):
        note=next((v for (key,ax),v in contested.items() if key.casefold() in name.casefold() and ax==a),None)
        axes.append({'estudo':name,'dimensao':f'P{a}','marca_original':row.cells[a].text,'estado':'contestada' if note else 'recodificacao_uniforme_nao_fechada','justificativa':note or 'Marca inventariada. Não há julgamento individual fechado desta célula nesta auditoria; exigir passagem e regra uniforme antes de novo total.'})
assert len(axes)==170,len(axes)
csvout('matriz_34_estudos.csv',axes)
(O/'estado_auditoria.json').write_text(json.dumps({'data':'2026-10-28','word_sha256':hashlib.sha256((R/'reports/monografia/MayconGarciaSilva_monografia_FASOFT_conferida.docx').read_bytes()).hexdigest(),'referencias_inventariadas':50,'ocorrencias_reconhecidas_avaliadas':len(occ),'celulas_p1_p5_inventariadas':len(axes),'celulas_diretamente_contestadas':sum(a['estado']=='contestada' for a in axes),'conclusao':'Não há validação integral de todas as atribuições; há divergências comprovadas, apoio parcial e consultas primárias não fechadas. A recodificação das 170 células não está concluída. Não foi demonstrado plágio, nem certificada ausência.','word_alterado':False,'experimentos_executados':False},ensure_ascii=False,indent=2),encoding='utf8')
print('50 referências,',len(occ),'ocorrências e',len(axes),'células inventariadas;',sum(a['estado']=='contestada' for a in axes),'células diretamente contestadas.')
