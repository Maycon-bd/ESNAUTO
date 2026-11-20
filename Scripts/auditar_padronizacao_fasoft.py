"""Verificação estrutural e de preservação; a inspeção visual é registrada à parte."""
from pathlib import Path
from collections import Counter
import re,json,hashlib,unicodedata,zipfile
from docx import Document
from docx.oxml.ns import qn
from pypdf import PdfReader
import pdfplumber
ROOT=Path(__file__).resolve().parents[1];QA=ROOT/'reports/padronizacao_fasoft_20261027'
SRC=ROOT/'reports/monografia/MayconGarciaSilva_monografia_observacoes_atendidas.docx'
OUT=ROOT/'reports/monografia/MayconGarciaSilva_monografia_padronizada_FASOFT.docx'
a=Document(SRC);b=Document(OUT);checks=[]
def check(name,ok,detail=None):checks.append({'requisito':name,'ok':bool(ok),'detalhe':detail})
def key(s):return ''.join(c for c in unicodedata.normalize('NFD',s.casefold()) if c.isalnum() and not unicodedata.combining(c))
def media(p):
    with zipfile.ZipFile(p) as z:return Counter(hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist() if n.startswith('word/media/'))
check('Imagens preservadas',media(SRC)==media(OUT),len(b.inline_shapes))
check('Todos os valores e textos das 13 tabelas preservados',[[c.text for r in t.rows for c in r.cells] for t in a.tables]==[[c.text for r in t.rows for c in r.cells] for t in b.tables],len(b.tables))
check('Texto das 49 referências preservado',Counter(p.text for p in a.paragraphs if p.style.name=='Referencias')==Counter(p.text for p in b.paragraphs if p.style.name=='Referencias'))
for i,s in enumerate(b.sections):
    values=[s.page_width.cm,s.page_height.cm,s.top_margin.cm,s.left_margin.cm,s.right_margin.cm,s.bottom_margin.cm]
    check(f'A4 e margens da seção {i+1}',all(abs(x-y)<.01 for x,y in zip(values,[21,29.7,3,3,2,2])))
for ti,t in enumerate(b.tables[1:],1):
    runs=[r for row in t.rows for c in row.cells for p in c.paragraphs for r in p.runs if r.text.strip()]
    check(f'Tabela {ti}: fonte 11',all(r.font.size and r.font.size.pt==11 for r in runs))
    check(f'Tabela {ti}: cabeçalho negrito',all(r.bold for c in t.rows[0].cells for p in c.paragraphs for r in p.runs if r.text.strip()))
caps=[p for p in b.paragraphs if p.style.name=='Caption' or re.match(r'^(Tabela|QUADRO|Figura)\s+\d+\s*[–—-]',p.text) and '\t' not in p.text]
check('Títulos das ilustrações em fonte 10',all(r.font.size and r.font.size.pt==10 for p in caps for r in p.runs if r.text.strip()),len(caps))
check('Títulos sem ponto final',all(not p.text.endswith('.') for p in caps))
sources=[p for p in b.paragraphs if p.text.startswith('Fonte:')]
check('Fontes em tamanho 10',all(r.font.size and r.font.size.pt==10 for p in sources for r in p.runs if r.text.strip()),len(sources))
refs=[p.text for p in b.paragraphs if p.style.name=='Referencias']
check('Referências em ordem alfabética pelo autor de entrada',[key(x.split(',')[0]) for x in refs]==sorted(key(x.split(',')[0]) for x in refs))
ps=b.paragraphs;ia=next(i for i,p in enumerate(ps) if p.text=='INTRODUÇÃO');ib=next(i for i,p in enumerate(ps) if p.text=='REVISÃO DA LITERATURA')
intro=ps[ia+1:ib]
check('Introdução sem citações autor–ano',not any(re.search(r'\(\d{4}[a-z]?\)',p.text) for p in intro))
check('Introdução contínua sem subseções',all(p.style.name=='Normal' for p in intro))
check('Hipóteses originais preservadas',all(any(q.text==p.text for q in b.paragraphs) for p in a.paragraphs if re.match(r'^H[1-5] - ',p.text)))
for title in ['RESUMO','ABSTRACT']:
    idx=next(i for i,p in enumerate(ps) if p.text==title)
    p=next(p for p in ps[idx+1:] if p.text.strip())
    check(title+': 150–500 palavras',150<=len(p.text.split())<=500,len(p.text.split()))
    check(title+': sem recuo e espaço simples',p.paragraph_format.first_line_indent==0 and p.paragraph_format.line_spacing==1)
pdf=PdfReader(QA/'monografia.pdf');texts=[p.extract_text() for p in pdf.pages]
body=[(i+1,t) for i,t in enumerate(texts) if re.match(r'^\s*\d+\s*\n',t)]
check('Paginação textual contínua excluindo capa',all(int(re.match(r'^\s*(\d+)',t)[1])==physical-1 for physical,t in body),len(body))
intro_pages=[physical for physical,t in body if physical>=ia and False]
start=next(i for i,t in enumerate(texts) if i>14 and '1 INTRODUÇÃO' in t[:100])
end=next(i for i,t in enumerate(texts) if i>start and '2 REVISÃO DA LITERATURA' in t[:100])
check('Introdução com 2–3 páginas',2<=end-start<=3,end-start)
check('Nenhuma página vazia',all(t.strip() for t in texts),len(texts))
mapa=json.loads((QA/'mapa_paginas.json').read_text(encoding='utf-8-sig'))
entries=[]
for p in ps:
    if '\t' not in p.text or not re.search(r'\t\d+\s*$',p.text):continue
    parts=p.text.split('\t');title=parts[-2] if len(parts)>=3 else parts[0];page=int(parts[-1])
    found=[x for x in mapa if key(x['texto'])==key(title)]
    if len(found)>1 and len(parts)>=3:found=[x for x in found if x['numero']==parts[0]]
    entries.append({'titulo':title,'pagina_lista':page,'pagina_corpo':found[0]['pagina'] if len(found)==1 else None})
check('Todas as listas e o sumário conferidos no mapa do Word',all(x['pagina_lista']==x['pagina_corpo'] for x in entries),entries)
outside=[]
with pdfplumber.open(QA/'monografia.pdf') as pl:
    for i,p in enumerate(pl.pages):
        bad=[c for c in p.chars if c['text'].strip() and (c['x0']<83 or c['x1']>541 or c['bottom']>789)]
        if bad:outside.append({'pagina':i+1,'texto':''.join(c['text'] for c in bad)})
check('Texto dentro das margens laterais e inferior',not outside,outside)
pending=[{'requisito':'Ficha catalográfica emitida pela biblioteca','situacao':'pendente','evidencia':'Tabela OOXML 0 permanece vazia; solicitada ao usuário.'},
{'requisito':'Folha de aprovação assinada e datada após aprovação','situacao':'dependente_da_etapa_academica','evidencia':'Campos de data e assinatura preservados, sem inventar aprovação.'}]
report={'arquivo':str(OUT),'sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),'paginas':len(pdf.pages),'checks':checks,'pendencias':pending,'conformidade_integral_atestada':False}
(QA/'auditoria_estrutural.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
for c in checks:
    if not c['ok']:print('FALHOU',c['requisito'],c['detalhe'])
print(sum(x['ok'] for x in checks),'/',len(checks),'verificações estruturais aprovadas; pendências documentais registradas.')
