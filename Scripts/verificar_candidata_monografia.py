"""Conferência estrutural e de preservação da candidata nativa; não certificação."""
import argparse,hashlib,json,re
from pathlib import Path
from zipfile import ZipFile
from docx import Document
from pypdf import PdfReader
import pdfplumber

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description=__doc__)
for arg in ['origem','candidata','pdf','mapa','saida']:parser.add_argument('--'+arg,required=True)
args=parser.parse_args()
paths={k:(ROOT/v).resolve() for k,v in vars(args).items()}
assert all(p.is_relative_to(ROOT) for p in paths.values())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
a,b=Document(paths['origem']),Document(paths['candidata'])
checks=[]
def check(name,ok,detail=None):checks.append({'item':name,'ok':bool(ok),'detalhe':detail})
assert len(a.paragraphs)==len(b.paragraphs)
changes=[]
for i,(p,q) in enumerate(zip(a.paragraphs,b.paragraphs)):
    if p.text!=q.text:
        assert '\t' in p.text and re.sub(r'\d+\s*$','',p.text)==re.sub(r'\d+\s*$','',q.text),(i,p.text,q.text)
        changes.append({'paragrafo_atual':i,'antes':p.text,'depois':q.text})
check('Texto do corpo preservado; apenas páginas das listas mudam',True,len(changes))
check('Texto das tabelas preservado',[[c.text for r in t.rows for c in r.cells] for t in a.tables]==[[c.text for r in t.rows for c in r.cells] for t in b.tables])
def media(path):
    with ZipFile(path) as z:return {n:hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist() if n.startswith('word/media/')}
check('Mídias preservadas',media(paths['origem'])==media(paths['candidata']))
for i,s in enumerate(b.sections):
    values=[s.page_width.cm,s.page_height.cm,s.top_margin.cm,s.left_margin.cm,s.right_margin.cm,s.bottom_margin.cm]
    check(f'A4/margens seção{i+1}',all(abs(x-y)<0.015 for x,y in zip(values,[21,29.7,3,3,2,2])),values)
for title in ['RESUMO','ABSTRACT']:
    i=next(i for i,p in enumerate(b.paragraphs) if p.text==title)
    p=next(p for p in b.paragraphs[i+1:] if p.text.strip())
    check(title+'150–500palavras',150<=len(p.text.split())<=500,len(p.text.split()))
for ti,t in enumerate(b.tables[1:],1):
    runs=[r for row in t.rows for c in row.cells for p in c.paragraphs for r in p.runs if r.text.strip()]
    check(f'TabelaXML{ti}:11pt',all(r.font.size and r.font.size.pt==11 for r in runs),len(runs))
    check(f'TabelaXML{ti}:cabeçalho negrito',all(r.bold for c in t.rows[0].cells for p in c.paragraphs for r in p.runs if r.text.strip()))
caps=[p for p in b.paragraphs if re.match(r'^(Tabela|Quadro|Figura)\s+\d+\s*[–—-]',p.text) and '\t' not in p.text]
sources=[p for p in b.paragraphs if p.text.startswith('Fonte:')]
check('Legendas10pt',all(r.font.size and r.font.size.pt==10 for p in caps for r in p.runs if r.text.strip()),len(caps))
check('Fontes10pt',all(r.font.size and r.font.size.pt==10 for p in sources for r in p.runs if r.text.strip()),len(sources))
check('Legendas sem ponto final',all(not p.text.rstrip().endswith('.') for p in caps))
check('Títulos quadros/tabelas sem siglas',all(not re.search(r'\b[A-Z]{2,}\b',p.text) for p in caps if p.text.startswith(('Quadro','Tabela'))))
mapping=json.loads(paths['mapa'].read_text(encoding='utf-8-sig'))
def key(t):return re.sub(r'\s+',' ',t).strip()
entries=[]
for i,p in enumerate(b.paragraphs):
    if '\t' not in p.text or not re.search(r'\t\d+\s*$',p.text):continue
    parts=p.text.split('\t');title=parts[-2] if len(parts)>=3 else parts[0]
    found=[x for x in mapping if key(x['texto'])==key(title)]
    if len(found)>1 and len(parts)>=3:found=[x for x in found if x['numero']==parts[0].strip()]
    entries.append({'paragrafo':i,'titulo':title,'pagina_lista':int(parts[-1]),'pagina_corpo':found[0]['pagina'] if len(found)==1 else None})
check('60 entradas de listas/sumário correspondem ao mapa Word',len(entries)==60 and all(x['pagina_lista']==x['pagina_corpo'] for x in entries),entries)
reader=PdfReader(paths['pdf']);texts=[p.extract_text() or '' for p in reader.pages]
check('Nenhuma página vazia',all(t.strip() for t in texts),len(texts))
number_errors=[]
for i,t in enumerate(texts[17:],18):
    m=re.match(r'^\s*(\d+)\s*\n',t)
    if not m or int(m[1])!=i-1:number_errors.append({'pagina_fisica':i,'inicio':t[:70]})
check('Paginação textual contínua',not number_errors,number_errors)
outside=[]
with pdfplumber.open(paths['pdf']) as pdf:
    for i,p in enumerate(pdf.pages,1):
        bad=[c for c in p.chars if c['text'].strip() and (c['x0']<82.5 or c['x1']>541.5 or c['bottom']>789.5)]
        if bad:outside.append({'pagina_fisica':i,'texto':''.join(c['text'] for c in bad),'limites':[min(c['x0'] for c in bad),max(c['x1'] for c in bad),max(c['bottom'] for c in bad)]})
check('Texto dentro dos limites laterais/inferiores',not outside,outside)
report={'arquivos':{k:{'caminho':str(p),'sha256':sha(p)} for k,p in paths.items() if k!='saida'},'checks':checks,'alteracoes_textuais_nativas':changes,'paginas_pdf':len(texts),'limites':'Verificações estruturais não comprovam fidelidade científica nem substituem inspeção visual de texto e imagens; coordenadas admitem tolerância de renderização. Ficha catalográfica e aprovação não foram fabricadas. Sem certificação integral.'}
paths['saida'].write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('Verificações:',len(checks),'falhas:',sum(not c['ok'] for c in checks),'páginas:',len(texts))
for c in checks:
    if not c['ok']:print(c['item'],str(c['detalhe'])[:1200])
