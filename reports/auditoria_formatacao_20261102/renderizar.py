from pathlib import Path
import importlib.util, shutil,hashlib,json
import pypdfium2 as pdfium
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
DOC=(ROOT/'reports/monografia/versoes/v010/MayconGarciaSilva_monografia_v010.docx').resolve()
skill=Path('C:/Users/User/.codex/plugins/cache/openai-primary-runtime/documents/26.1026.10807/skills/documents/render_docx.py')
pdf=OUT/'v010_word.pdf'
if not pdf.exists():
 old=ROOT/'reports/busca_lacunas_20261101/candidata.pdf'
 evidence=json.loads((ROOT/'reports/busca_lacunas_20261101/inspecao_visual.json').read_text(encoding='utf-8'))
 assert hashlib.sha256(DOC.read_bytes()).hexdigest()==evidence['sha256_docx']
 assert hashlib.sha256(old.read_bytes()).hexdigest()==evidence['pdf_sha256']
 pdf=old
 (OUT/'origem_render.json').write_text(json.dumps({'modo':'Nova rasterização de exportação Word anterior ligada por hashes à mesma v010; nova exportação não obtida nesta auditoria','docx_sha256':evidence['sha256_docx'],'pdf_sha256':evidence['pdf_sha256'],'pdf':str(pdf)},ensure_ascii=False,indent=2),encoding='utf-8')
spec=importlib.util.spec_from_file_location('render_oficial',skill);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
def native(doc_path,user_profile,convert_tmp_dir,stem,verbose=False):
 assert Path(doc_path).resolve()==DOC
 target=Path(convert_tmp_dir)/(stem+'.pdf');shutil.copy2(pdf,target)
 return str(target),'PDFWord com procedência registrada; conversorLibreOffice indisponível'
module.convert_to_pdf=native
module.rasterize(str(DOC),str(OUT/'paginas'),dpi=96,verbose=False,emit_pdf=False)
guide=pdfium.PdfDocument(ROOT/'output/skills-docx/GUIA-FASOFT-UniRV.pdf')
for p in [37,38,39,40,43,44,45,48,49,50,53,54,55,60]:
 guide[p-1].render(scale=1.5).to_pil().save(OUT/f'guia-{p}.png')
print('Renderização concluída')
