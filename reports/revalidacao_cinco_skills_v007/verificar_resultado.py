from pathlib import Path
import json,hashlib,re,importlib.util,os,shutil,tempfile
from docx import Document
from pypdf import PdfReader
import pypdfium2 as pdfium
from PIL import Image,ImageDraw,ImageChops
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
DOC=ROOT/'reports/monografia/trabalho/revalidacao_cinco_skills_v007.docx'
PDF=OUT/'revisao_final.pdf';PREV=ROOT/'reports/revisao_linguistica_v006/revisao_final.pdf'
delta=json.loads((OUT/'alteracoes_aplicadas.json').read_text(encoding='utf-8'))
assert hashlib.sha256(DOC.read_bytes()).hexdigest()==delta['sha256_candidata']
tempfile.tempdir=str(OUT/'temp_render');Path(tempfile.tempdir).mkdir(exist_ok=True)
os.environ['PATH']=r'C:\Users\User\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin'+os.pathsep+os.environ['PATH']
skill=Path(r'C:\Users\User\.codex\plugins\cache\openai-primary-runtime\documents\26.1026.10807\skills\documents\render_docx.py')
spec=importlib.util.spec_from_file_location('render_oficial',skill)
r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
def convert(doc_path,user_profile,convert_tmp_dir,stem,verbose=False):
    assert Path(doc_path).resolve()==DOC.resolve()
    dest=Path(convert_tmp_dir)/(stem+'.pdf');shutil.copy2(PDF,dest)
    return str(dest),'Microsoft Word somente leitura, sem salvar DOCX; rasterizador oficial.'
r.convert_to_pdf=convert
pages=r.rasterize(str(DOC),str(OUT/'png_final'),dpi=110,verbose=False,emit_pdf=False)
old=pdfium.PdfDocument(PREV);new=pdfium.PdfDocument(PDF)
assert len(pages)==len(old)==len(new)==76
diffs=[];same=[];visual=[]
for i in range(len(new)):
    a=old[i].render(scale=1.3).to_pil().convert('RGB');b=new[i].render(scale=1.3).to_pil().convert('RGB')
    if ImageChops.difference(a,b).getbbox() is None:same.append(i+1)
    else:
        diffs.append(i+1);b.save(OUT/f'alterada-{i+1}.png')
    visual.append({'pagina':i+1,'pixels_iguais':i+1 in same,'sha256_pixels_antes':hashlib.sha256(a.tobytes()).hexdigest(),'sha256_pixels_depois':hashlib.sha256(b.tobytes()).hexdigest()})
texts=[p.extract_text() for p in PdfReader(PDF).pages]
beforetexts=[p.extract_text() for p in PdfReader(PREV).pages]
assert all(t.strip() for t in texts)
# Páginas de abertura dos títulos e legendas mantidas; números de lista não precisam mudar.
d=Document(DOC);elements=[p.text for p in d.paragraphs if p.style.name=='Caption']
def normalize(s):return ' '.join(s.split())
positions=[]
for cap in elements:
    a=[i+1 for i,t in enumerate(beforetexts) if normalize(cap) in normalize(t)]
    b=[i+1 for i,t in enumerate(texts) if normalize(cap) in normalize(t)]
    assert a==b,(cap,a,b)
    positions.append({'titulo':cap,'paginas_antes':a,'paginas_depois':b})
state={'base':'v007','candidata_sha256':hashlib.sha256(DOC.read_bytes()).hexdigest(),'pdf_sha256':hashlib.sha256(PDF.read_bytes()).hexdigest(),'paginas':len(new),'paginas_identicas':same,'paginas_alteradas':diffs,'comparacao_visual':visual,'legendas_paginas_preservadas':positions,'origem_pdf':'Exportação nativa Word em leitura; rasterização com render_docx.py 26.1026.10807; comparação de pixels com pypdfium2.','inspecao_paginas_alteradas':'pendente'}
(OUT/'verificacao_visual.json').write_text(json.dumps(state,ensure_ascii=False,indent=2),encoding='utf-8')
print('76 páginas; diferentes:',diffs,'idênticas:',len(same),'páginas de legendas preservadas:',len(positions))
