"""Auditoria documental local. Não treina modelos nem modifica os documentos fonte."""
from pathlib import Path
from docx import Document
from pypdf import PdfReader
from collections import defaultdict
import re,json,hashlib,unicodedata,sys,csv
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reports/auditoria_citacoes_integridade_20261028'
DOC=Path('C:/Users/User/Downloads/MayconGarciaSilva_monografia_FASOFT_conferida.docx')
GUIDE=Path('C:/Users/User/Downloads/GUIA_Padronizacao_Monografia_FASOFT_UniRV (1).pdf')
def norm(s):
    s=''.join(c for c in unicodedata.normalize('NFD',s.casefold()) if not unicodedata.combining(c))
    return re.findall(r'\w+',s)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def paras(d):return d.paragraphs+[p for t in d.tables for row in t.rows for c in row.cells for p in c.paragraphs]
d=Document(DOC);ps=paras(d)
sources=[]
for f in sorted((ROOT/'Artigos citados').glob('*.pdf')):
    t=OUT/(f.stem+'.txt')
    sources.append((str(f),t.read_text(encoding='utf8'),sha(f)))
lamp=ROOT/'MatheusTeixeiraLampugnani_monografia (1).docx';ld=Document(lamp)
sources.append((str(lamp),'\n'.join(f'[L{i:04d}] '+p.text for i,p in enumerate(paras(ld))),sha(lamp)))
sources.append((str(GUIDE),(OUT/'guia.txt').read_text(encoding='utf8'),sha(GUIDE)))
sources.append((str(ROOT/'reports/tese_Fabian_Correa_Cardoso.pdf'),(OUT/'Cardoso_tese.txt').read_text(encoding='utf8'),sha(ROOT/'reports/tese_Fabian_Correa_Cardoso.pdf')))
for f in (ROOT/'reports/bibliometria_reconstrucao/referencias_graficas').glob('*_texto.txt'):
    sources.append((str(f),f.read_text(encoding='utf8'),sha(f)))
manifest=[{'path':path,'sha256':h,'tokens_extraidos':len(norm(s))} for path,s,h in sources]
manifest.insert(0,{'path':str(DOC),'sha256':sha(DOC),'tipo':'alvo'})
(OUT/'manifesto.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
# Índice de oito palavras consecutivas. Não mede similaridade semântica/tradução.
n=8;idx=defaultdict(set)
for si,(path,s,h) in enumerate(sources):
    for seg in re.split(r'(?=\[PÁGINA PDF \d+\]|\[L\d+\])',s):
        m=re.search(r'\[(PÁGINA PDF \d+|L\d+)\]',seg);loc=m[1] if m else 'texto sem paginação'
        w=norm(seg)
        for k in range(len(w)-n+1):idx[tuple(w[k:k+n])].add((si,loc))
matches=[]
for pi,p in enumerate(ps):
    if pi<172 or p.style.name=='Referencias':continue
    w=norm(p.text)
    for k in range(len(w)-n+1):
        hit=idx.get(tuple(w[k:k+n]))
        if hit:matches.append({'paragrafo':pi,'trecho_normalizado':' '.join(w[k:k+n]),'fontes':[{'path':sources[si][0],'localizador':loc} for si,loc in sorted(hit)]})
(OUT/'triagem_similaridade.json').write_text(json.dumps({'n':n,'limites':'Somente texto extraível e normalização de caixa, acentos e pontuação. Não é percentual de plágio. Sem OCR integral, corpus externo ou detecção de tradução.','coincidencias':matches},ensure_ascii=False,indent=2),encoding='utf8')
pdf=ROOT/'reports/auditoria_integral_fasoft_20261028/monografia.pdf';pages=[' '.join(norm(p.extract_text() or '')) for p in PdfReader(pdf).pages]
locs={}
for i,p in enumerate(ps):
    w=norm(p.text)
    if len(w)<5:continue
    key=' '.join(w[:min(12,len(w))]);found=[j+1 for j,s in enumerate(pages) if key in s]
    if found:locs[str(i)]=found
(OUT/'localizadores_paginas.json').write_text(json.dumps(locs,ensure_ascii=False,indent=2),encoding='utf8')
old=json.loads((ROOT/'reports/auditoria_integral_fasoft_20261028/cruzamento_citacoes.json').read_text(encoding='utf8'))
rows=[]
for i,r in enumerate(old['registros'],1):
    p=ps[r['paragrafo']]
    rows.append({'id':f'C{i:03d}','paragrafo':f'P{r["paragrafo"]:04d}','pagina_pdf':','.join(map(str,locs.get(str(r['paragrafo']),[]))),'citacao':r['citacao'],'ano':r['ano'],'texto_integral':p.text,'referencias':' || '.join(r['referencias'])})
with (OUT/'inventario_ocorrencias.csv').open('w',encoding='utf-8-sig',newline='') as f:
    wr=csv.DictWriter(f,fieldnames=list(rows[0]));wr.writeheader();wr.writerows(rows)
print('Fontes indexadas:',len(sources),'ocorrências autor–ano:',len(rows),'janelas de 8 palavras:',len(matches))
for m in matches[:25]:print('P'+str(m['paragrafo']),m['trecho_normalizado'],Path(m['fontes'][0]['path']).name,m['fontes'][0]['localizador'])
