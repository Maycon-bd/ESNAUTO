"""Render do skill, usando exportação nativa do Word feita previamente."""
from pathlib import Path
import importlib.util, os, shutil, tempfile, sys
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[1]
QA=ROOT/'reports/padronizacao_fasoft_20261027'
DOC=ROOT/'reports/monografia/MayconGarciaSilva_monografia_padronizada_FASOFT.docx'
PDF=QA/'monografia.pdf'
tempfile.tempdir=str(QA/'temp');Path(tempfile.tempdir).mkdir(exist_ok=True)
os.environ['TEMP']=tempfile.tempdir;os.environ['TMP']=tempfile.tempdir
os.environ['PATH']='C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin'+os.pathsep+os.environ['PATH']
skill=Path('C:/Users/User/.codex/plugins/cache/openai-primary-runtime/documents/26.1025.11240/skills/documents/render_docx.py')
spec=importlib.util.spec_from_file_location('renderer',skill)
r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
def convert(doc_path,user_profile,convert_tmp_dir,stem,verbose=False):
    assert Path(doc_path).resolve()==DOC.resolve()
    dest=Path(convert_tmp_dir)/(stem+'.pdf');shutil.copy2(PDF,dest)
    return str(dest),'Exportação Microsoft Word; rasterização pelo renderer do skill.'
r.convert_to_pdf=convert
out=QA/(sys.argv[1] if len(sys.argv)>1 else 'png')
pages=r.rasterize(str(DOC),str(out),dpi=110,verbose=False,emit_pdf=False)
assert len(pages)==len(PdfReader(PDF).pages)
print(len(pages),'páginas rasterizadas')
