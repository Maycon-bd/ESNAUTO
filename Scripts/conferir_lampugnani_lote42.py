"""Confronto do antecedente correlato e da comparação dos 24 resultados."""
import hashlib,json
from pathlib import Path
from decimal import Decimal
from docx import Document
root=Path(__file__).resolve().parents[1];out=root/'reports/fechamento_integral_20261029';doc=root/'reports/monografia/trabalho/fechamento_integral_20261029.docx';src=root/'MatheusTeixeiraLampugnani_monografia (1).docx';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(doc)=='4cf48044445c0760210b1206c185487b8406af3eaecb541de6db381cdbf735b0' and sha(src)=='21bcfd9deefb4535540978b3b8007dbe1bdcd8351676ab97116c7f3745f7e94f'
D=Document(doc);S=Document(src);records=[]
for i in range(9,13):
 t=S.tables[i];assert [c.text for c in t.rows[0].cells]==['Distribuição de probabilidade (Win)','Distribuição de probabilidade W','RMSE (Teste)','MAE (Teste)']
 for j,r in enumerate(t.rows[1:],1):
  c=[v.text for v in r.cells];records.append({'tabela_docx':i,'linha':j,'Win':c[0],'W':c[1],'RMSE':c[2],'MAE':c[3]})
assert len(records)==24;mae=min(records,key=lambda r:Decimal(r['MAE']));rmse=min(records,key=lambda r:Decimal(r['RMSE']));assert (mae['MAE'],mae['Win'],mae['W'])==('0.378706','Cauchy','Normal');assert (rmse['RMSE'],rmse['Win'],rmse['W'])==('0.568178','Cauchy','Uniforme')
t=D.tables[12];assert all(s in t.cell(1,j).text for j,s in [(1,'0,378706'),(2,'0,568178')]);assert '0,327224' in t.cell(2,1).text and '0,495386' in t.cell(2,2).text
assert 'não fazer tratamento' in S.paragraphs[408].text and 'Algoritmo Genético' in S.paragraphs[435].text
items=[
 (226,'P 397, 402, 435; tabelas DOCX 9–12','Fonte estuda distribuições para Win/W e GA em PETR4; comparação genérica não afirma identidade de protocolo.'),
 (242,'P 397, 402; matriz de 34 obras','Fonte é monografia correlata e não integra a matriz reconstruída; é decisão de organização do portfólio, não atributo extraído do título.'),
 (246,'P 397, 402, 435 e tabelas DOCX 9–12','Tema, GA, distribuições e aplicação à PETR4 são confirmados; utilização separada é decisão metodológica do trabalho.'),
 (260,'P 397, 435 e 459–460','Distribuições e AG aparecem na monografia anterior; demais atribuições a Araújo e Cardoso requerem suas próprias evidências.'),
 (264,'Matriz de 34 obras; fonte DOCX','A referência é excluída do corpus da matriz por decisão documentada; definição dos critérios da matriz é própria do estudo atual.'),
 (450,'P 397, 402, 435; tabelas DOCX 9–12','ESN, AG, PETR4 e erros de teste estão documentados; confronto é entre estudos sem execução conjunta.'),
 (452,'Tabela DOCX 12 do trabalho atual','Título identifica uma comparação descritiva e é acompanhado pela fonte e resultados.'),
 (453,'Tabelas DOCX 9–12 da fonte e tabela 12 do trabalho atual','Fonte da tabela identifica o outro trabalho; mínimos de MAE e RMSE são efetivamente de combinações distintas.'),
 (454,'Tabelas DOCX 9–12; relatório das quatro ondas do projeto','Mínimos da fonte são 0,378706 e 0,568178, versus 0,327224 e 0,495386 nos registros consolidados. A diferença não identifica um efeito causal.'),
 (455,'P 408 da fonte','A fonte declara ausência de tratamento adicional; isso não determina se houve ajuste anterior ao recebimento.'),
 (470,'Tabelas DOCX 9–12 da fonte','A menção à comparação é descritiva; melhores próprios e baselines dependem de evidências do projeto examinadas separadamente.'),
 (489,'Tabelas DOCX 9–12 da fonte','O vínculo a Lampugnani indica comparação descritiva; o teste DM é dependente de evidências separadas da rodada controlada.'),
 (498,'P 397, 435 e 459–460; Quadro 6','A contribuição de ESN, AG e distribuições é antecedida pelo trabalho correlato; demais atribuições do quadro dependem de fontes próprias.')]
rows=[]
for p,loc,e in items:
 text=D.paragraphs[p].text;assert 'Lampugnani (2026)' in text,(p,text);rows.append({'ancora':f'P_atual{p:04}','texto_atual':text,'referencia':'R30','fonte':str(src.relative_to(root)),'sha256_fonte':sha(src),'localizador':loc,'evidencia':e,'diagnostico':'condizente no ponto delimitado'})
rows.append({'ancora':'T_atual12/L1','referencia':'R30','texto_atual':[c.text for c in t.rows[1].cells],'fonte':str(src.relative_to(root)),'sha256_fonte':sha(src),'localizador':'Tabelas 9–12 do DOCX da fonte','evidencia':'24 linhas conferidas diretamente; mínimos e combinações indicados nesta linha conferem; tratamento declarado não prova estado inicial dos dados.','diagnostico':'condizente no ponto delimitado'})
f=out/'afirmacoes_lampugnani_lote42.json';assert not f.exists();f.write_text(json.dumps({'base':'v005','sha256_base':'2af31abca4e3ba9fd5caf7cd161e55472dc94edc136cdf89732c0d0401118d6b','sha256_rascunho':sha(doc),'n_registros_fonte':24,'min_mae':mae,'min_rmse':rmse,'registros':rows,'limite':'Não certifica equivalência dos protocolos nem sustenta automaticamente as demais fontes ou números no mesmo parágrafo.'},ensure_ascii=False,indent=2)+'\n',encoding='utf8');s=out/'estado_meta.json';state=json.loads(s.read_text(encoding='utf8'));state['ultimo_registro_de_leitura']=str(f.relative_to(root));state['proxima_passagem']='Continuar confronto das outras fontes e requisitos qualitativos do Guia.';s.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print('24 resultados da fonte e 14 contextos atuais conferidos.')
