from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from copy import deepcopy
from lxml import etree as E
import hashlib,json,re,csv

OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1]
BASE=ROOT/'reports/monografia/versoes/v009/MayconGarciaSilva_monografia_v009.docx'
DEST=ROOT/'reports/monografia/trabalho/busca_lacunas_20261101.docx'
assert hashlib.sha256(BASE.read_bytes()).hexdigest()=='793910fae2daaa2d5dbdcfa0cd76177c6c6a38c353d98d94ecaaaecf118c7b03'
W='http://schemas.openxmlformats.org/wordprocessingml/2006/main';ns={'w':W}
with ZipFile(BASE) as z: parts={n:z.read(n) for n in z.namelist()}
r=E.fromstring(parts['word/document.xml']);body=r.find('w:body',ns)
def text(p):return ''.join(p.xpath('.//w:t/text()',namespaces=ns))
def settext(p,s):
    nodes=p.xpath('.//w:t',namespaces=ns);assert nodes
    nodes[0].text=s;nodes[0].set('{http://www.w3.org/XML/1998/namespace}space','preserve')
    for n in nodes[1:]:n.text=''
def para_like(p,s,italic_spans=()):
    q=deepcopy(p)
    for child in list(q):
        if child.tag!=f'{{{W}}}pPr':q.remove(child)
    # Preserve inherited paragraph style; construct runs for text and italics.
    pos=0
    def run(t,italic=False):
        if not t:return
        rr=E.SubElement(q,f'{{{W}}}r')
        if italic:
            pr=E.SubElement(rr,f'{{{W}}}rPr');E.SubElement(pr,f'{{{W}}}i')
        tt=E.SubElement(rr,f'{{{W}}}t');tt.text=t;tt.set('{http://www.w3.org/XML/1998/namespace}space','preserve')
    spans=[]
    for term in italic_spans:
        for m in re.finditer(re.escape(term),s):spans.append((m.start(),m.end()))
    for lo,hi in sorted(spans):run(s[pos:lo]);run(s[lo:hi],True);pos=hi
    run(s[pos:]);return q
plan=json.loads((OUT/'conciliacao_proposta.json').read_text(encoding='utf-8'))
tables=r.xpath('.//w:tbl',namespaces=ns)
matrix=next(t for t in tables if len(t.findall('w:tr',ns))==35)
for d in plan['alteracoes']:
    row=matrix.findall('w:tr',ns)[d['linha_word']]
    assert text(row.findall('w:tc',ns)[0])==d['autor']
    c=row.findall('w:tc',ns)[int(d['dimensao'][1:])]
    assert text(c)=='?';settext(c,d['depois'])
tab=next(t for t in tables if any(text(tr).startswith('P1 Distribuição') for tr in t.findall('w:tr',ns)))
counts=plan['contagens_depois']
for tr in tab.findall('w:tr',ns):
    cells=tr.findall('w:tc',ns)
    if not cells:continue
    k=text(cells[0])[:2]
    if k in counts:
        c=counts[k];settext(cells[1],f"{c.get('D',0)} D; {c.get('S',0)} S; {c.get('?',0)} ?; {c.get('—',0)} —")
p=next(p for p in body.findall('w:p',ns) if text(p).startswith('A Figura 1 registra evidência direta'))
for node in p.xpath('.//w:t',namespaces=ns):
    node.text=(node.text or '').replace('em 26 documentos','em 27 documentos').replace('tem cinco registros diretos','tem seis registros diretos')
anchor=next(p for p in body.findall('w:p',ns) if text(p).startswith('O Quadro 1 apresenta a codificação'))
s='Na conferência documental da matriz, o exemplo de Jaeger (2007) foi examinado também pelo código suplementar vinculado ao artigo, na versão disponibilizada com revisões posteriores. Esse material explicita a geração dos pesos e a construção das entradas. Em Millea (2014), a identificação da comparação secundária com LSTM foi conferida pelos valores de Evolino e pela fonte original de Schmidhuber et al. (2007, p. 772). Esses materiais complementam a verificação, sem ampliar o portfólio de 34 documentos.'
assert len(s)<=700
body.insert(list(body).index(anchor)+1,para_like(anchor,s,('et al.',)))
jaeger=next(p for p in body.findall('w:p',ns) if text(p).startswith('JAEGER, Herbert. Echo state network.'))
# Keep existing styled title and append a plain supplemental locator.
rr=E.SubElement(jaeger,f'{{{W}}}r');tt=E.SubElement(rr,f'{{{W}}}t');tt.set('{http://www.w3.org/XML/1998/namespace}space','preserve')
tt.text=' Material suplementar do exemplo: https://www.ai.rug.nl/minds/uploads/freqGen.zip. Acesso em: 1 nov. 2026.'
ref=next(p for p in body.findall('w:p',ns) if text(p).startswith('SED DIK'.replace(' ','')))
reference='SCHMIDHUBER, J.; WIERSTRA, D.; GAGLIOLO, M.; GOMEZ, F. Training Recurrent Networks by Evolino. Neural Computation, v. 19, n. 3, p. 757-779, 2007. DOI: 10.1162/neco.2007.19.3.757.'
body.insert(list(body).index(ref),para_like(ref,reference,('Neural Computation',)))
parts['word/document.xml']=E.tostring(r,encoding='UTF-8',xml_declaration=True,standalone=True)
assert (OUT/'figura1_atualizada.png').is_file()
parts['word/media/image1.png']=(OUT/'figura1_atualizada.png').read_bytes()
with ZipFile(DEST,'w',ZIP_DEFLATED) as z:
    for n,data in parts.items():z.writestr(n,data)
(OUT/'alteracoes_word.json').write_text(json.dumps({'base':'v009','alteracoes_celulas':plan['alteracoes'],'novo_paragrafo':s,'referencia_adicionada':reference,'partes_alteradas':['word/document.xml','word/media/image1.png'],'sha256_copia':hashlib.sha256(DEST.read_bytes()).hexdigest(),'estado':'rascunho_a_renderizar'},ensure_ascii=False,indent=2),encoding='utf-8')
print('Tres celulas, contagens, figura e rastreabilidade incorporadas na copia de trabalho.')
