"""Consolida verificações e evidências, sem editar a base editorial."""
from pathlib import Path
import json,re,hashlib,unicodedata,collections
from docx import Document
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1]
meta=json.loads((OUT/'identidade_e_cobertura.json').read_text(encoding='utf-8'))
d=Document(ROOT/meta['base']['arquivo'])
assert hashlib.sha256((ROOT/meta['base']['arquivo']).read_bytes()).hexdigest()==meta['base']['sha256']
ps=d.paragraphs
tables=json.loads((OUT/'quadros_tabelas.json').read_text(encoding='utf-8'))
sig=json.loads((OUT/'siglas.json').read_text(encoding='utf-8'))
italics=json.loads((OUT/'italicos.json').read_text(encoding='utf-8'))
def visible(edge):return edge.get('val') not in [None,'nil','none','0']
tablechecks=[]
for t in tables:
    rows=t['celulas'];kind=t['tipo'];cap=t['titulo'];source=t['fonte_dados']
    check={'elemento':kind+' '+str(t['numero']),'local':cap['local'],'titulo':cap['texto'],
           'titulo_10':all(r['pt']==10 for r in cap['runs'] if r['texto'].strip()),
           'titulo_justificado_simples':cap['alinhamento']==3 and cap['entrelinhas']==1,
           'titulo_sem_ponto':not cap['texto'].endswith('.'),
           'corpo_11':all(r['pt']==11 for row in rows for c in row for r in c['runs'] if r['texto'].strip()),
           'cabecalho_negrito':all(r['negrito'] for c in rows[0] for r in c['runs'] if r['texto'].strip()),
           'entrelinhas_simples':all(x==1 for row in rows for c in row for x in c['entrelinhas']),
           'fonte_10_simples':source['texto'].startswith('Fonte:') and all(r['pt']==10 for r in source['runs'] if r['texto'].strip()) and source['entrelinhas']==1,
           'fonte_com_ano_ponto':bool(re.search(r'\b20\d{2}\b',source['texto'])) and source['texto'].endswith('.'),
           'minimo_linhas_colunas':t['linhas']>=3 and t['colunas']>=2,
           'largura_quadro_16':abs(t['largura_cm']-16)<.015 if kind=='Quadro' else None,
           'corpo_sem_divisorias':all(not visible(c['bordas'].get('right',{})) and not visible(row[ci+1]['bordas'].get('left',{})) for row in rows[1:] for ci,c in enumerate(row[:-1])) and all(not visible(c['bordas'].get('bottom',{})) for row in rows[1:-1] for c in row),
           'laterais':all(visible(row[0]['bordas'].get('left',{}))==bool(kind=='Quadro') and visible(row[-1]['bordas'].get('right',{}))==bool(kind=='Quadro') for row in rows),
           'cabecalho_divisorias_verticais':any(visible(c['bordas'].get('right',{})) or visible(rows[0][ci+1]['bordas'].get('left',{})) for ci,c in enumerate(rows[0][:-1])),
           'chamada_nominal':bool(t['chamadas']),'chamadas':t['chamadas']}
    tablechecks.append(check)
(OUT/'checks_quadros_tabelas.json').write_text(json.dumps(tablechecks,ensure_ascii=False,indent=2),encoding='utf-8')

