from pathlib import Path
import importlib.util,shutil,sys,json
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
B=Path(__file__).resolve().parent;R=B.parents[1]
stage=sys.argv[1] if len(sys.argv)>1 else 'final'
doc=R/'reports/monografia/trabalho/listas_links_20261102.docx' if stage=='final' else B/'entrega/Declaracao_responsabilidade_coletiva_Maycon_assinaturas.docx'
images=sorted((B/('word_'+stage)).glob('page-*.png'),key=lambda p:int(p.stem.split('-')[1]))
assert len(images)==(json.loads((B/'mapa_final.json').read_text(encoding='utf-8-sig'))['pages'] if stage=='final' else 1),len(images)
pdf=B/(stage+'_word_qa.pdf');c=canvas.Canvas(str(pdf),pagesize=A4)
for im in images:c.drawImage(str(im),0,0,width=A4[0],height=A4[1]);c.showPage()
c.save()
skill=Path('C:/Users/User/.codex/plugins/cache/openai-primary-runtime/documents/26.1026.10807/skills/documents/render_docx.py')
spec=importlib.util.spec_from_file_location('docx_renderer',skill);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
def native_pdf(doc_path,user_profile,convert_tmp_dir,stem,verbose=False):
 out=Path(convert_tmp_dir)/(stem+'.pdf');shutil.copy2(pdf,out)
 return str(out),'Páginas atuais obtidas do Word via Page.EnhMetaFileBits, sem reutilizar PDF anterior'
mod.convert_to_pdf=native_pdf
sys.argv=[str(skill),str(doc),'--output_dir',str(B/('render_'+stage)),'--emit_pdf'];mod.main()
