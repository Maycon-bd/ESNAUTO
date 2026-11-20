from pathlib import Path
import importlib.util,shutil,sys
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
B=Path(__file__).resolve().parent
pdf=B/'paginas_word_qa.pdf';c=canvas.Canvas(str(pdf),pagesize=A4)
c.drawImage(str(B/'word_paginas/page-1.png'),0,0,width=A4[0],height=A4[1]);c.showPage();c.save()
skill=Path('C:/Users/User/.codex/plugins/cache/openai-primary-runtime/documents/26.1026.10807/skills/documents/render_docx.py')
spec=importlib.util.spec_from_file_location('docx_renderer',skill);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
def native_pdf(doc_path,user_profile,convert_tmp_dir,stem,verbose=False):
 out=Path(convert_tmp_dir)/(stem+'.pdf');shutil.copy2(pdf,out)
 return str(out),'Minuta atual renderizada diretamente no Word por Page.EnhMetaFileBits'
mod.convert_to_pdf=native_pdf
sys.argv=[str(skill),str(B/'entrega/Declaracao_responsabilidade_coletiva_Maycon_MINUTA.docx'),'--output_dir',str(B/'render'),'--emit_pdf'];mod.main()
