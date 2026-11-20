import hashlib,json,pathlib
from pypdf import PdfReader
out=pathlib.Path(__file__).resolve().parent
root=out.parents[1]
inv=json.loads((out/'inventario_41.json').read_text(encoding='utf-8'))
dest=out/'fontes_extraidas';dest.mkdir(exist_ok=True)
manifest=[]
for ident in sorted({d['id'] for d in inv['celulas']}):
    d=next(d for d in inv['celulas'] if d['id']==ident)
    p=root/d['pdf']; sha=hashlib.sha256(p.read_bytes()).hexdigest()
    assert sha==d['sha256_pdf']
    pdf=PdfReader(p)
    pages=[{'pagina_pdf':i+1,'texto':page.extract_text()} for i,page in enumerate(pdf.pages)]
    target=dest/f'{ident}_paginas.json'
    target.write_text(json.dumps(pages,ensure_ascii=False,indent=2),encoding='utf-8')
    manifest.append({'id':ident,'pdf':d['pdf'],'sha256_pdf':sha,'paginas':len(pdf.pages),'sha256_extracao':hashlib.sha256(target.read_bytes()).hexdigest()})
(out/'manifesto_fontes.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(len(manifest),'PDFs extraidos com identidade conferida')
