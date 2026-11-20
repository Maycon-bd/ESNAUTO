"""Renderiza a base sem salvar o Word; PDF nativo exportado em leitura."""
from pathlib import Path
import importlib.util,os,shutil,tempfile,json,re,hashlib
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
DOC=ROOT/'reports/monografia/versoes/v001/MayconGarciaSilva_monografia_v001.docx'
PDF=OUT/'v001_leitura.pdf'
tempfile.tempdir=str(OUT/'temp_render');Path(tempfile.tempdir).mkdir(exist_ok=True)
os.environ['PATH']=r'C:\Users\User\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin'+os.pathsep+os.environ['PATH']
skill=Path(r'C:\Users\User\.codex\plugins\cache\openai-primary-runtime\documents\26.1025.11240\skills\documents\render_docx.py')
spec=importlib.util.spec_from_file_location('render_oficial',skill)
r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
def convert(doc_path,user_profile,convert_tmp_dir,stem,verbose=False):
    assert Path(doc_path).resolve()==DOC.resolve()
    dest=Path(convert_tmp_dir)/(stem+'.pdf');shutil.copy2(PDF,dest)
    return str(dest),'Microsoft Word em leitura, sem salvar o DOCX; rasterizador oficial.'
r.convert_to_pdf=convert
pages=r.rasterize(str(DOC),str(OUT/'png'),dpi=110,verbose=False,emit_pdf=False)
reader=PdfReader(PDF)
assert len(pages)==len(reader.pages)
texts=[p.extract_text() for p in reader.pages]
(OUT/'texto_pdf.txt').write_text('\n'.join(f'\nPAGINA FISICA {i+1}\n'+t for i,t in enumerate(texts)),encoding='utf-8')
locations={}
for i,t in enumerate(texts):
    # exclude front lists with dotted leaders by beginning after introductory pages
    if i<17:continue
    for kind,n in re.findall(r'\b(Tabela|Quadro)\s+(\d+)\s*[–—-]',t):locations.setdefault(kind+' '+n,[]).append(i+1)
(OUT/'mapa_visual.json').write_text(json.dumps({'paginas':len(pages),'pdf_sha256':hashlib.sha256(PDF.read_bytes()).hexdigest(),'elementos':locations},indent=2),encoding='utf-8')
print(len(pages),'paginas renderizadas;',locations)
