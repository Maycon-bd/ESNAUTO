"""Usa o rasterizador do skill com o PDF exportado pelo Word local.

O conversor LibreOffice não está disponível neste ambiente. A exportação nativa
é efetuada previamente e somente essa etapa é substituída no renderer do skill.
"""
import importlib.util
import os
from pathlib import Path
import shutil
import tempfile
from PIL import Image, ImageDraw
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
QA=ROOT/'reports/qa_monografia_bibliometria'
DOC=ROOT/'reports/monografia/MayconGarciaSilva_monografia_bibliometria_VALE3.docx'
PDF=QA/'final/monografia.pdf'
SKILL=Path('C:/Users/User/.codex/plugins/cache/openai-primary-runtime/documents/26.1011.11113/skills/documents/render_docx.py')
TEMP=QA/'temp'
TEMP.mkdir(exist_ok=True)
tempfile.tempdir=str(TEMP)
os.environ['TEMP']=str(TEMP);os.environ['TMP']=str(TEMP)
os.environ['PATH']='C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin'+os.pathsep+os.environ['PATH']
spec=importlib.util.spec_from_file_location('skill_render_docx',SKILL)
renderer=importlib.util.module_from_spec(spec);spec.loader.exec_module(renderer)
def word_pdf(doc_path,user_profile,convert_tmp_dir,stem,verbose=False):
    assert Path(doc_path).resolve()==DOC.resolve()
    target=Path(convert_tmp_dir)/(stem+'.pdf')
    shutil.copy2(PDF,target)
    return str(target),'PDF exportado pelo Microsoft Word; LibreOffice indisponível.'
renderer.convert_to_pdf=word_pdf
pages=renderer.rasterize(str(DOC),str(QA/'final/png'),dpi=110,verbose=False,emit_pdf=False)
assert len(pages)==len(PdfReader(PDF).pages)
# Pares em resolução nativa para inspeção integral, sem redução das páginas.
contact=QA/'final/pares';contact.mkdir(exist_ok=True)
for i in range(0,len(pages),2):
    ims=[Image.open(p).convert('RGB') for p in pages[i:i+2]]
    width=sum(im.width for im in ims);height=max(im.height for im in ims)+28
    sheet=Image.new('RGB',(width,height),'#d9dde0');draw=ImageDraw.Draw(sheet)
    x=0
    for j,im in enumerate(ims):
        draw.text((x+10,5),f'Página física {i+j+1}',fill='black');sheet.paste(im,(x,28));x+=im.width
    sheet.save(contact/f'par-{i+1:02}.png')
print(f'{len(pages)} páginas rasterizadas pelo render_docx.py; pares em resolução nativa.')
text='\n\n'.join(f'PÁGINA {i+1}\n{p.extract_text()}' for i,p in enumerate(PdfReader(PDF).pages))
(QA/'final/texto_pdf.txt').write_text(text,encoding='utf-8')
