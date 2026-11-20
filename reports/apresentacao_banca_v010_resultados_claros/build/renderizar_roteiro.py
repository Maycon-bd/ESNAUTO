import importlib.util,shutil,sys
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
BUILD=Path(__file__).resolve().parent
# New renders from the updated DOCX, obtained via Word Page.EnhMetaFileBits.
# Direct PDF export hangs on this installation; no prior-version PDF is reused.
pdf=BUILD/'roteiro_paginas_word.pdf'
c=canvas.Canvas(str(pdf),pagesize=A4)
for i in range(1,14):
    im=BUILD/f'word_paginas/page-{i}.png'
    assert im.exists()
    c.drawImage(str(im),0,0,width=A4[0],height=A4[1]);c.showPage()
c.save()
skill=Path('C:/Users/User/.codex/plugins/cache/openai-primary-runtime/documents/26.1026.10807/skills/documents/render_docx.py')
spec=importlib.util.spec_from_file_location('docx_renderer',skill)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
def native_pdf(doc_path,user_profile,convert_tmp_dir,stem,verbose=False):
    out=Path(convert_tmp_dir)/(stem+'.pdf');shutil.copy2(pdf,out)
    return str(out),'Páginas atuais renderizadas pelo Word em EMF, rasterizadas e reunidas em PDF para QA'
mod.convert_to_pdf=native_pdf
sys.argv=[str(skill),str(BUILD.parent/'entrega/Roteiro_ESNAUTO_v010_resultados_claros.docx'),'--output_dir',str(BUILD/'roteiro_render'),'--emit_pdf']
mod.main()
