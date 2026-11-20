"""Verificação estrutural e de preservação; a inspeção visual é registrada à parte."""
from pathlib import Path
from collections import Counter
import re,json,hashlib,unicodedata,zipfile
from docx import Document
from docx.oxml.ns import qn
from regularizar_epigrafe_fasoft import NEW_QUOTE, NEW_CITATION, REFERENCE, OLD_QUOTE
from pypdf import PdfReader
import pdfplumber
ROOT=Path(__file__).resolve().parents[1];QA=ROOT/'reports/auditoria_integral_fasoft_20261028'
SRC=ROOT/'reports/monografia/MayconGarciaSilva_monografia_padronizada_FASOFT.docx'
OUT=ROOT/'reports/monografia/MayconGarciaSilva_monografia_FASOFT_conferida.docx'
a=Document(SRC);b=Document(OUT);checks=[]
def check(name,ok,detail=None):checks.append({'requisito':name,'ok':bool(ok),'detalhe':detail})
def key(s):return ''.join(c for c in unicodedata.normalize('NFD',s.casefold()) if c.isalnum() and not unicodedata.combining(c))
def media(p):
    with zipfile.ZipFile(p) as z:return Counter(hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist() if n.startswith('word/media/'))
check('Imagens preservadas',media(SRC)==media(OUT),len(b.inline_shapes))
check('Valores e textos das tabelas experimentais preservados',[[c.text for r in t.rows for c in r.cells] for t in a.tables[3:]]==[[c.text for r in t.rows for c in r.cells] for t in b.tables[3:]],len(b.tables)-3)
check('Identidade das 49 referências preservada; apenas referência de Gleick acrescentada',Counter(key(p.text)[:65] for p in a.paragraphs if p.style.name=='Referencias')+Counter([key(REFERENCE)[:65]])==Counter(key(p.text)[:65] for p in b.paragraphs if p.style.name=='Referencias'))
check('Epígrafe corresponde à passagem primária verificada e tem referência e localizador',sum(p.text==NEW_QUOTE for p in b.paragraphs)==1 and sum(p.text==NEW_CITATION for p in b.paragraphs)==1 and sum(p.text==REFERENCE for p in b.paragraphs)==1 and not any(p.text==OLD_QUOTE for p in b.paragraphs))
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
def prop(p,name):
    v=getattr(p.paragraph_format,name)
    st=p.style
    while v is None and st is not None:
        v=getattr(st.paragraph_format,name);st=st.base_style
    return v
def rf(r,p,name):
    v=getattr(r.font,name);st=p.style
    while v is None and st is not None:
        v=getattr(st.font,name);st=st.base_style
    if v is None and name=='name':
        defaults=b.styles.element.xpath('./w:docDefaults/w:rPrDefault/w:rPr/w:rFonts')
        if defaults:v=defaults[0].get(qn('w:ascii'))
    return v
def cm(v):return 0 if v is None else v.cm
ic=next(i for i,p in enumerate(ps) if p.text=='REFERÊNCIAS')
body=ps[ia:ic]
ordinary=[p for p in body if p.style.name=='Normal' and p.text.strip() and not p.text.startswith(('Fonte:','Nota:'))]
check('Corpo justificado',all(prop(p,'alignment')==3 for p in ordinary))
check('Corpo em entrelinhas 1,5',all(prop(p,'line_spacing')==1.5 for p in ordinary))
plain=[p for p in ordinary if not re.match(r'^[a-z]\) ',p.text)]
check('Corpo com primeira linha de 1,25 cm',all(abs(cm(prop(p,'first_line_indent'))-1.25)<.01 for p in plain))
check('Corpo sem recuo lateral adicional',all(abs(cm(prop(p,'left_indent')))<.01 and abs(cm(prop(p,'right_indent')))<.01 for p in plain))
check('Corpo em Times New Roman 12',all(rf(r,p,'name')=='Times New Roman' and rf(r,p,'size') and rf(r,p,'size').pt==12 for p in ordinary for r in p.runs if r.text.strip()))
allp=ps+[p for t in b.tables for row in t.rows for c in row.cells for p in c.paragraphs]
check('Texto em preto ou automático',all(r.font.color.rgb is None or str(r.font.color.rgb)=='000000' for p in allp for r in p.runs if r.text.strip()))
for name,bold,upper in [('TITULO TCC',True,True),('SEÇÃO TCC',False,True),('SUBÇÃO 2',True,False)]:
    hs=[p for p in body if p.style.name==name]
    check('Hierarquia: '+name,all(prop(p,'alignment')==3 and all(rf(r,p,'size').pt==12 and bool(rf(r,p,'bold'))==bold for r in p.runs if r.text.strip()) and (not upper or p.text==p.text.upper()) for p in hs),len(hs))
check('Títulos acompanhados do texto seguinte',all(prop(p,'keep_with_next') for p in body if p.style.name in ['TITULO TCC','SEÇÃO TCC','SUBÇÃO 2']))
check('Controle de linhas órfãs e viúvas no corpo',all(prop(p,'widow_control') is not False for p in ordinary))
ft=['RESUMO','ABSTRACT','LISTA DE FIGURAS','LISTA DE QUADROS','LISTA DE TABELAS','LISTA DE ABREVIATURAS E SIGLAS','LISTA DE SÍMBOLOS','SUMÁRIO']
idx=[next(i for i,p in enumerate(ps) if p.text==title) for title in ft]
check('Ordem dos elementos pré-textuais',idx==sorted(idx))
check('Títulos pré-textuais centralizados e em negrito 12',all(prop(ps[i],'alignment')==1 and all(rf(r,ps[i],'size').pt==12 and rf(r,ps[i],'bold') for r in ps[i].runs if r.text.strip()) for i in idx))
ficha=b.tables[0]
check('Ficha: caixa de 12,5 × 7,5 cm',abs(ficha.cell(0,0).width.cm-12.5)<.01 and abs(ficha.rows[0].height.cm-7.5)<.01)
check('Ficha vazia preservada por instrução do autor',not any(c.text.strip() for row in ficha.rows for c in row.cells))
for title in ['RESUMO','ABSTRACT']:
    i=next(i for i,p in enumerate(ps) if p.text==title);p=ps[i+1];kw=ps[i+2]
    terms=kw.text.split(':',1)[-1].strip().rstrip('.').split(';')
    check(title+': de 3 a 5 palavras-chave',3<=len(terms)<=5,terms)
    check(title+': palavras-chave separadas por ponto e vírgula e encerradas por ponto',kw.text.endswith('.') and ';' in kw.text)
sig=[p for p in ps[idx[5]+1:idx[6]] if p.text.strip()]
keys=[p.text.split(' – ')[0] for p in sig]
check('Lista de siglas alfabética',keys==sorted(keys,key=str.casefold),len(keys))
check('Lista de siglas justificada em fonte 12 e espaço 1,5',all(prop(p,'alignment')==3 and prop(p,'line_spacing')==1.5 and all(rf(r,p,'size').pt==12 for r in p.runs if r.text.strip()) for p in sig))
for kind in ['Figura','Quadro','Tabela']:
    numbers=[int(re.match(r'^'+kind+r'\s+(\d+)',p.text,re.I)[1]) for p in caps if re.match(r'^'+kind+r'\s+\d+',p.text,re.I)]
    check(kind+': numeração consecutiva',numbers==list(range(1,len(numbers)+1)),numbers)
    noncaps=' '.join(p.text for p in body if p not in caps)
    check(kind+': chamada de todos os elementos no texto',all(re.search(r'\b'+kind+r'\s+'+str(n)+r'\b',noncaps,re.I) for n in numbers))
check('Fontes abaixo dos elementos: indicação e ano',len(sources)==len(caps) and all(re.search(r'\b(?:19|20)\d{2}\b',p.text) and p.text.endswith('.') for p in sources))
check('Referências em fonte 12 e espaço simples',all(prop(p,'line_spacing')==1 and all(rf(r,p,'size').pt==12 for r in p.runs if r.text.strip()) for p in ps if p.style.name=='Referencias'))
check('Imagens sem alteração de proporção ou tamanho',[(x.width,x.height) for x in a.inline_shapes]==[(x.width,x.height) for x in b.inline_shapes])
check('Sem notas de rodapé a formatar',not b._element.xpath('.//w:footnoteReference'))
check('Sem comentários ou revisões pendentes',not b._element.xpath('.//w:commentReference | .//w:ins | .//w:del'))
check('Tabelas e quadros com largura efetiva de 16 cm',all(abs(sum(c.width.cm for c in t.columns)-16)<.015 for t in b.tables[1:]),[round(sum(c.width.cm for c in t.columns),3) for t in b.tables[1:]])
def italic_span(p,m):
    pos=0
    for r in p.runs:
        lo,hi=pos,pos+len(r.text);pos=hi
        if lo<m.end() and hi>m.start() and not rf(r,p,'italic'):return False
    return True
latin=[(p,m) for p in allp for m in re.finditer(r'\bet al\.',p.text)]
check('Todas as ocorrências de et al. em itálico',all(italic_span(p,m) for p,m in latin),len(latin))
symbols=[(p,m) for p in allp for m in re.finditer(r'\bW(?:in|out)\b',p.text)]
check('Símbolos Win e Wout em itálico',all(italic_span(p,m) for p,m in symbols),len(symbols))
pdf=PdfReader(QA/'monografia.pdf');texts=[p.extract_text() for p in pdf.pages]
primary=[p for p in body if p.style.name=='TITULO TCC']
check('Seções primárias em nova página no PDF do Word',all(any(re.match(r'^\s*\d+\s*\n'+str(n)+r'\s+'+re.escape(p.text),t) for t in texts) for n,p in enumerate(primary,1)))
body=[(i+1,t) for i,t in enumerate(texts) if re.match(r'^\s*\d+\s*\n',t)]
check('Paginação textual contínua excluindo capa',all(int(re.match(r'^\s*(\d+)',t)[1])==physical-1 for physical,t in body),len(body))
intro_pages=[physical for physical,t in body if physical>=ia and False]
start=next(i for i,t in enumerate(texts) if re.match(r'^\s*\d+\s*\n1\s+INTRODUÇÃO\b',t))
end=next(i for i,t in enumerate(texts) if i>start and re.match(r'^\s*\d+\s*\n2\s+REVISÃO DA LITERATURA\b',t))
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
institutional=[{'requisito':'Ficha catalográfica emitida pela biblioteca','situacao':'etapa_institucional_posterior_autorizada','evidencia':'Espaço reservado preservado por decisão expressa do autor, sem bloquear a formatação.'},
{'requisito':'Folha de aprovação assinada e datada após aprovação','situacao':'dependente_da_etapa_academica','evidencia':'Campos de data e assinatura preservados, sem inventar aprovação.'}]
pending=[]
report={'arquivo':str(OUT),'sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),'paginas':len(pdf.pages),'checks':checks,'pendencias':pending,'etapas_institucionais_posteriores':institutional,'auditoria_estrutural_sozinha_atesta_conformidade_integral':False}
(QA/'auditoria_estrutural.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
for c in checks:
    if not c['ok']:print('FALHOU',c['requisito'],c['detalhe'])
print(sum(x['ok'] for x in checks),'/',len(checks),'verificações estruturais aprovadas; pendências documentais registradas.')
