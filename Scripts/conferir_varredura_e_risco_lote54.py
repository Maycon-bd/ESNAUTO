"""Procura anos fora do índice e confere estatísticas descritivas de subperíodos."""
import csv,datetime,hashlib,json,re,statistics
from pathlib import Path
from docx import Document
root=Path(__file__).resolve().parents[1];out=root/'reports/fechamento_integral_20261029';doc=root/'reports/monografia/trabalho/fechamento_integral_20261029.docx';data=root/'Scripts/data/PETR4_close com factor_2000-2020_com data.csv';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert sha(doc)=='61fac8da8ab082633bbaa113ed697fd32ccfd7d72c2142f003b18b5b10083e2a'
idx=json.loads((out/'indice_citacoes_atuais_lote50.json').read_text(encoding='utf8'));locations={o['local'] for r in idx['registros'] for o in r['ocorrencias']};d=Document(doc);pattern=re.compile(r'\b(?:18|19|20)\d{2}[a-z]?\b');other=[]
for i,p in enumerate(d.paragraphs[:499]):
 loc=f'P_atual{i:04}'
 if pattern.search(p.text) and loc not in locations:other.append({'local':loc,'texto':p.text,'classificacao':'data, período, ano da autoria própria ou elemento da lista; sem chamada externa autor–ano identificada na leitura'})
seen=set();other_cells=[]
for ti,t in enumerate(d.tables):
 for ri,row in enumerate(t.rows):
  for ci,c in enumerate(row.cells):
   if c._tc in seen:continue
   seen.add(c._tc)
   for pi,p in enumerate(c.paragraphs):
    loc=f'T_atual{ti}/L{ri}/C{ci}/P{pi}'
    if pattern.search(p.text) and loc not in locations:other_cells.append({'local':loc,'texto':p.text})
assert not other_cells
with data.open(encoding='utf-8-sig',newline='') as f:values=[(datetime.date.fromisoformat(r[0]),float(r[1])) for r in csv.reader(f,delimiter=';')]
periods=[('2015-09-29','2016-12-29',311,3.99,-52.27),('2017-01-02','2019-12-30',739,2.56,-46.55),('2020-01-02','2020-12-30',249,4.32,-63.36)];results=[]
for a,b,n,vol,draw in periods:
 v=[x for date,x in values if datetime.date.fromisoformat(a)<=date<=datetime.date.fromisoformat(b)];returns=[y/x-1 for x,y in zip(v,v[1:])];peak=v[0];dd=0.0
 for price in v:peak=max(peak,price);dd=min(dd,price/peak-1)
 sd=statistics.stdev(returns)*100;dd*=100;assert len(v)==n and abs(sd-vol)<0.0051 and abs(dd-draw)<0.0051;results.append({'inicio':a,'fim':b,'observacoes':len(v),'volatilidade_amostral_retornos_simples_pct':sd,'drawdown_por_maximo_acumulado_no_subperiodo_pct':dd})
assert '3,99%' in d.paragraphs[416].text and '-63,36%' in d.paragraphs[416].text
f=out/'varredura_citacoes_e_risco_lote54.json';assert not f.exists();f.write_text(json.dumps({'base':'v005','sha256_base':'2af31abca4e3ba9fd5caf7cd161e55472dc94edc136cdf89732c0d0401118d6b','sha256_rascunho':sha(doc),'fonte_serie':str(data.relative_to(root)),'sha256_serie':sha(data),'anos_sem_chamada_indexada':other,'celulas_com_ano_fora_indice':other_cells,'subperiodos':results,'metodo':'Desvio padrão amostral dos retornos simples internos ao subperíodo e menor razão preço/máximo acumulado menos um; comparação com arredondamentos do texto.','limites':'Busca por anos não detecta atribuições sem ano, citações em imagens ou erros de fonte; figuras e referências exigem revisão própria. Retornos entre períodos são excluídos nesta conferência; não se executou treinamento nem teste DM.','acao':'Nenhuma edição Word.'},ensure_ascii=False,indent=2)+'\n',encoding='utf8');s=out/'estado_meta.json';state=json.loads(s.read_text(encoding='utf8'));state['ultimo_registro_de_leitura']=str(f.relative_to(root));state['proxima_passagem']='Revisar atribuições sem ano, triagem de similaridade e requisitos qualitativos do Guia.';s.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print(len(other),'parágrafos com anos fora do índice; três subperíodos conferidos.')
