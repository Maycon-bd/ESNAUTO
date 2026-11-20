from pathlib import Path
from zipfile import ZipFile
from collections import Counter
import hashlib,json,sys
from lxml import etree as E
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
DOC=ROOT/'reports/monografia/versoes/v010/MayconGarciaSilva_monografia_v010.docx'
GUIDE=ROOT/'output/skills-docx/GUIA-FASOFT-UniRV.pdf'
assert hashlib.sha256(DOC.read_bytes()).hexdigest()=='1da5ea82344c177d75af723362017e3e558bbb127bd9995f7ec0cbd6964f81ed'
assert hashlib.sha256(GUIDE.read_bytes()).hexdigest()=='cc109117539c87278a763d958ceb35ff20a6d452ba9d7ea2e4964d894c2c9e3f'
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','wp':'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'}
W='{'+NS['w']+'}'
def txt(el):return ''.join(el.xpath('.//w:t/text()',namespaces=NS))
def props(el):
 if el is None:return {}
 d={}
 for x in el:
  v={E.QName(k).localname:v for k,v in x.attrib.items()}
  if len(x):v.update(props(x))
  d[E.QName(x).localname]=v or True
 return d
def merge(d,v):
 for k,x in v.items():
  if isinstance(x,dict) and isinstance(d.get(k),dict):d[k]={**d[k],**x}
  else:d[k]=x
with ZipFile(DOC) as z:
 doc=E.fromstring(z.read('word/document.xml'));styles=E.fromstring(z.read('word/styles.xml'))
 lookup={s.get(W+'styleId'):s for s in styles.findall('w:style',NS)}
 defaultp=props(styles.find('w:docDefaults/w:pPrDefault/w:pPr',NS));defaultr=props(styles.find('w:docDefaults/w:rPrDefault/w:rPr',NS))
 def chain(sid):
  seen=set();a=[]
  while sid in lookup and sid not in seen:
   seen.add(sid);s=lookup[sid];a.insert(0,s);v=s.find('w:basedOn',NS);sid=v.get(W+'val') if v is not None else None
  return a
 def pf(p):
  d=dict(defaultp);v=p.find('w:pPr/w:pStyle',NS);sid=v.get(W+'val') if v is not None else 'Normal'
  for s in chain(sid):merge(d,props(s.find('w:pPr',NS)))
  merge(d,props(p.find('w:pPr',NS)));return sid,d
 def rf(r,sid):
  d=dict(defaultr)
  for s in chain(sid):merge(d,props(s.find('w:rPr',NS)))
  v=r.find('w:rPr/w:rStyle',NS)
  if v is not None:
   for s in chain(v.get(W+'val')):merge(d,props(s.find('w:rPr',NS)))
  merge(d,props(r.find('w:rPr',NS)));return d
 pars=[]
 for i,p in enumerate(doc.xpath('/w:document/w:body/w:p',namespaces=NS)):
  sid,d=pf(p);runs=[{'texto':txt(r),'propriedades':rf(r,sid)} for r in p.xpath('.//w:r',namespaces=NS) if txt(r)]
  pars.append({'indice':i,'texto':txt(p),'estilo':sid,'paragrafo':d,'runs':runs,'imagens':len(p.xpath('.//w:drawing',namespaces=NS)),'equacoes':len(p.xpath('.//*[local-name()="oMath"]'))})
 tables=[]
 for i,t in enumerate(doc.xpath('/w:document/w:body/w:tbl',namespaces=NS)):
  rows=[]
  for row in t.findall('w:tr',NS):
   cells=[]
   for c in row.findall('w:tc',NS):
    ps=[]
    for p in c.findall('w:p',NS):
     sid,d=pf(p);ps.append({'texto':txt(p),'estilo':sid,'paragrafo':d,'runs':[{'texto':txt(r),'propriedades':rf(r,sid)} for r in p.xpath('.//w:r',namespaces=NS) if txt(r)]})
    cells.append({'texto':txt(c),'propriedades':props(c.find('w:tcPr',NS)),'paragrafos':ps})
   rows.append({'propriedades':props(row.find('w:trPr',NS)),'celulas':cells})
  tables.append({'indice':i,'propriedades':props(t.find('w:tblPr',NS)),'grid':[x.get(W+'w') for x in t.findall('w:tblGrid/w:gridCol',NS)],'linhas':rows})
 sections=[props(s) for s in doc.findall('.//w:sectPr',NS)]
 extras={n:z.read(n).decode('utf-8') for n in z.namelist() if n.startswith(('word/header','word/footer')) and n.endswith('.xml')}
 data={'base':'v010','sha256':hashlib.sha256(DOC.read_bytes()).hexdigest(),'secoes':sections,'paragrafos':pars,'tabelas':tables,'cabecalhos_rodapes':extras,'estilos':{k:E.tostring(v,encoding='unicode') for k,v in lookup.items()},'revisoes':{'insercoes':len(doc.findall('.//w:ins',NS)),'exclusoes':len(doc.findall('.//w:del',NS))}}
 (OUT/'estrutura.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
 guide=[{'pagina_pdf':i+1,'texto':p.extract_text() or ''} for i,p in enumerate(PdfReader(GUIDE).pages)]
 (OUT/'guia_paginas.json').write_text(json.dumps(guide,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'paragrafos':len(pars),'tabelas':len(tables),'secoes':len(sections),'paginas_guia':len(guide),'revisoes':data['revisoes']}))
