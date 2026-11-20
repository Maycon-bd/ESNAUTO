import collections, hashlib, json, pathlib, zipfile
import xml.etree.ElementTree as E

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = pathlib.Path(__file__).resolve().parent
base = json.loads((ROOT/'docs/assistencia_monografia/versao_vigente.json').read_text(encoding='utf-8'))
doc = ROOT/'reports/monografia/versoes/v009/MayconGarciaSilva_monografia_v009.docx'
assert hashlib.sha256(doc.read_bytes()).hexdigest() == '793910fae2daaa2d5dbdcfa0cd76177c6c6a38c353d98d94ecaaaecf118c7b03'
ns = {'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
r = E.fromstring(zipfile.ZipFile(doc).read('word/document.xml'))
tables = r.findall('.//w:tbl', ns)
matrix = None
for t in tables:
    rows = [[''.join(n.text or '' for n in c.findall('.//w:t',ns)) for c in tr.findall('w:tc',ns)] for tr in t.findall('w:tr',ns)]
    if len(rows) == 35 and len(rows[0]) == 6:
        matrix = rows
assert matrix is not None
catalog = json.loads((ROOT/'reports/fechamento_integral_20261029/matriz_lote21/matriz_recodificada.json').read_text(encoding='utf-8'))
dec = catalog['decisoes']
entries = []
for i,row in enumerate(matrix[1:],1):
    # The Word alphabetic order puts Liu B. (nanophotonics) before Liu H.
    # (sentiment). Historical source IDs put these two in the opposite order.
    source_number = {17:18,18:17}.get(i,i)
    ident = f'D{source_number:02}'
    source = next(d for d in dec if d['id']==ident)
    pdf = ROOT/'Artigos citados'/source['arquivo_pdf']
    assert hashlib.sha256(pdf.read_bytes()).hexdigest() == source['sha256_pdf']
    for j,code in enumerate(row[1:],1):
        if code == '?':
            old = next(d for d in dec if d['id']==ident and d['dimensao']==f'P{j}')
            entries.append({'id':ident,'linha_word':i,'autor':row[0],'dimensao':f'P{j}','pdf':str(pdf.relative_to(ROOT)),'sha256_pdf':source['sha256_pdf'],'evidencia_anterior':old,'estado':'a_reexaminar'})
assert len(entries)==41
data = {'base':'v009','sha256_base':hashlib.sha256(doc.read_bytes()).hexdigest(),'total':len(entries),'contagens':dict(collections.Counter(d['dimensao'] for d in entries)),'celulas':entries}
(OUT/'inventario_41.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
for d in entries:
    print(d['id'],d['dimensao'],d['autor'],':',d['evidencia_anterior']['localizador'])
