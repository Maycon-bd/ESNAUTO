"""Auditoria somente leitura da versão resolvida pelo registro editorial."""
from pathlib import Path
import json, re, hashlib, zipfile, collections
from lxml import etree as E
from docx import Document
from docx.text.paragraph import Paragraph
from docx.text.run import Run
from docx.oxml.ns import qn

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
reg=json.loads((ROOT/'docs/assistencia_monografia/versao_vigente.json').read_text(encoding='utf-8-sig'))
base=next(x for x in reg['versoes'] if x['id']==reg['vigente'])
src=ROOT/base['arquivo']
assert hashlib.sha256(src.read_bytes()).hexdigest()==base['sha256']
d=Document(src)
ps=d.paragraphs
body_start=next(i for i,p in enumerate(ps) if p.text=='INTRODUÇÃO')
ref_start=next(i for i,p in enumerate(ps) if p.text=='REFERÊNCIAS')
def scalar(v):
    if hasattr(v,'pt'):return v.pt
    return v
def prop(p,n):
    v=getattr(p.paragraph_format,n);s=p.style
    while v is None and s is not None:
        v=getattr(s.paragraph_format,n);s=s.base_style
    return scalar(v)
def rf(r,p,n):
    v=getattr(r.font,n)
    # Direct run > character style > paragraph style chain > defaults.
    if v is not None:return scalar(v)
    for s in [r.style,p.style]:
        while s is not None:
            v=getattr(s.font,n)
            if v is not None:return scalar(v)
            s=s.base_style
    tag={'italic':'i','bold':'b','size':'sz','name':'rFonts'}.get(n)
    nodes=d.styles.element.xpath('./w:docDefaults/w:rPrDefault/w:rPr/w:'+tag) if tag else []
    if nodes:
        if n in ['italic','bold']:return nodes[0].get(qn('w:val'),'1') not in ['0','false','off']
        if n=='size':return int(nodes[0].get(qn('w:val')))/2
        if n=='name':return nodes[0].get(qn('w:ascii'))
    return False if n in ['italic','bold'] else None
def runs(p):return [Run(x,p) for x in p._p.xpath('.//w:r')]
def pinfo(p,loc):
    return {'local':loc,'texto':p.text,'estilo':p.style.name,
            'alinhamento':prop(p,'alignment'),'entrelinhas':prop(p,'line_spacing'),
            'runs':[{'texto':r.text,'italico':rf(r,p,'italic'),'negrito':rf(r,p,'bold'),'pt':rf(r,p,'size'),'fonte':rf(r,p,'name')} for r in runs(p) if r.text]}
allp=[]
for i,p in enumerate(ps):allp.append((p,f'P{i:04}',i))
for ti,t in enumerate(d.tables):
    seen=set()
    for ri,row in enumerate(t.rows):
        for ci,c in enumerate(row.cells):
            if c._tc in seen:continue
            seen.add(c._tc)
            for pi,p in enumerate(c.paragraphs):allp.append((p,f'T{ti:02} L{ri+1} C{ci+1} P{pi+1}',None))
# Primeira ocorrência depende da ordem de leitura, incluindo tabelas intercaladas.
xml_order={el:i for i,el in enumerate(d.element.xpath('.//w:body//w:p'))}
allp.sort(key=lambda item:xml_order[item[0]._p])
dump=[pinfo(p,l) for p,l,i in allp]
(OUT/'paragrafos_e_formatacao.json').write_text(json.dumps(dump,ensure_ascii=False,indent=2),encoding='utf-8')
pi_by_el={p._p:i for i,p in enumerate(ps)}
caps=[]
for i,p in enumerate(ps):
    if p.style.name=='Caption' and re.match(r'^(Tabela|Quadro)\s+\d+',p.text,re.I):caps.append((i,p))
tables=[]
def borders(el):
    if el is None:return {}
    return {E.QName(x).localname:{E.QName(k).localname:v for k,v in x.attrib.items()} for x in el}
for ti,t in enumerate(d.tables):
    if ti==0:continue
    prev=t._tbl.getprevious();cap=None
    while prev is not None:
        idx=pi_by_el.get(prev)
        if idx is not None and any(idx==ci for ci,cp in caps):cap=(idx,ps[idx]);break
        prev=prev.getprevious()
    assert cap is not None,ti
    ci,cp=cap;kind=re.match(r'^(Tabela|Quadro)\s+(\d+)',cp.text,re.I)
    following=t._tbl.getnext();source=None
    while following is not None:
        idx=pi_by_el.get(following)
        if idx is not None and ps[idx].text.strip():source=(idx,ps[idx]);break
        following=following.getnext()
    cells=[]
    for ri,row in enumerate(t.rows):
        rowcells=[]
        for c in row.cells:
            b=c._tc.xpath('./w:tcPr/w:tcBorders')
            rowcells.append({'texto':c.text,'bordas':borders(b[0] if b else None),
                             'runs':[x for p in c.paragraphs for x in pinfo(p,'')['runs']],
                             'entrelinhas':[prop(p,'line_spacing') for p in c.paragraphs]})
        cells.append(rowcells)
    bn=t._tbl.xpath('./w:tblPr/w:tblBorders')
    refs=[f'P{j:04}' for j,p in enumerate(ps[body_start:ref_start],body_start) if p.style.name!='Caption' and re.search(r'\b'+kind[1]+r'\s+'+kind[2]+r'\b',p.text,re.I)]
    tables.append({'indice':ti,'tipo':kind[1],'numero':int(kind[2]),'titulo':pinfo(cp,f'P{ci:04}'),
                   'fonte_dados':pinfo(source[1],f'P{source[0]:04}') if source else None,
                   'linhas':len(t.rows),'colunas':len(t.columns),'largura_cm':sum(c.width.cm for c in t.columns),
                   'estilo_tabela':t.style.name if t.style else None,'bordas_tabela':borders(bn[0] if bn else None),
                   'chamadas':refs,'celulas':cells})
(OUT/'quadros_tabelas.json').write_text(json.dumps(tables,ensure_ascii=False,indent=2),encoding='utf-8')
si=next(i for i,p in enumerate(ps) if p.text=='LISTA DE ABREVIATURAS E SIGLAS')
se=next(i for i,p in enumerate(ps[si+1:],si+1) if p.text=='LISTA DE SÍMBOLOS')
sig=[]
for i in range(si+1,se):
    if ' – ' in ps[i].text:
        key,ext=ps[i].text.split(' – ',1)
        occurrences=[{'local':l,'texto':p.text,'em_tabela':idx is None} for p,l,idx in allp if (idx is None or body_start<=idx<ref_start) and re.search(r'(?<!\w)'+re.escape(key)+r'(?:s)?(?!\w)',p.text)]
        sig.append({'sigla':key,'extenso':ext,'local_lista':f'P{i:04}','usos':occurrences})
known={x['sigla'] for x in sig}
tokens=collections.defaultdict(list)
for p,l,i in allp:
    if i is not None and not body_start<=i<ref_start:continue
    for m in re.finditer(r'(?<!\w)[A-Z][A-Z0-9-]{1,}(?:s)?(?!\w)',p.text):
        tok=m[0]
        if tok not in known and tok.removesuffix('s') not in known:tokens[tok].append(l)
(OUT/'siglas.json').write_text(json.dumps({'lista':sig,'nao_listadas_candidatas':tokens},ensure_ascii=False,indent=2),encoding='utf-8')
terms=r'et al\.|apud|ibid\.|ibidem|opus citatum|backpropagation|feedback|download|marketing|on-line|bullying|campus|software|hardware|dataset|datasets|dropout|washout|input scaling|readout|ridge|baseline|baselines|benchmark|benchmarks|pipeline|pipelines|rollback|checkpoint|fitness|framework|frameworks|grid search|random search|data leakage|look-ahead|leakage|boosting|ensemble|ensembles|out-of-sample|in-sample|skewness|kurtosis|Scale-Free|Scale Free|Power Function|Small-World|small world|script|scripts|sparse|sparsity|leaking rate'
italics=[]
for p,l,i in allp:
    if i is not None and i>=ref_start:region='referencias'
    elif i is not None and i<body_start:region='pretextual'
    else:region='textual'
    rr=runs(p)
    for m in re.finditer(r'(?<!\w)(?:'+terms+r')(?!\w)',p.text,re.I):
        offset=0;states=[]
        for r in rr:
            start,end=offset,offset+len(r.text);offset=end
            if start<m.end() and end>m.start():states.append(rf(r,p,'italic'))
        italics.append({'local':l,'regiao':region,'termo':m[0],'italico_integral':bool(states) and all(states),'contexto':p.text[max(0,m.start()-65):m.end()+65]})
(OUT/'italicos.json').write_text(json.dumps(italics,ensure_ascii=False,indent=2),encoding='utf-8')
refs=[p.text for p in ps if p.style.name=='Referencias']
meta={'base':base,'sha256_conferido':hashlib.sha256(src.read_bytes()).hexdigest(),'paragrafos_corpo':len(ps),'paragrafos_com_celulas':len(allp),'quadros_tabelas':len(tables),'referencias':len(refs),'siglas_listadas':len(sig),'candidatos_italico':len(italics),'partes_zip':None}
with zipfile.ZipFile(src) as z:
    meta['partes_zip']=z.namelist()
    meta['notas_rodape']=len(d.element.xpath('.//w:footnoteReference'))
    meta['notas_fim']=len(d.element.xpath('.//w:endnoteReference'))
    meta['caixas_texto']=len(d.element.xpath('.//w:txbxContent'))
    meta['revisoes']=len(d.element.xpath('.//w:ins | .//w:del'))
(OUT/'identidade_e_cobertura.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in meta.items() if k not in ['base','partes_zip']},ensure_ascii=False))
for t in tables:
    print(t['indice'],t['titulo']['texto'],'width',round(t['largura_cm'],3),'size',sorted({x['pt'] for row in t['celulas'] for c in row for x in c['runs'] if x['texto'].strip()}), 'borders',t['bordas_tabela'])
print('ITALICOS sem destaque no corpo:',dict(collections.Counter(x['termo'] for x in italics if x['regiao']=='textual' and not x['italico_integral'])))
print('SIGLAS lista',len(sig),'candidatas ausentes:',dict(tokens))
