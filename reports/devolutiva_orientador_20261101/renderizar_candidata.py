from pathlib import Path
import importlib.util,shutil
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
DOC=(ROOT/'reports/monografia/trabalho/devolutiva_orientador_20261101.docx').resolve()
skill=Path('C:/Users/User/.codex/plugins/cache/openai-primary-runtime/documents/26.1026.10807/skills/documents/render_docx.py')
spec=importlib.util.spec_from_file_location('render_oficial',skill);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
def native(doc_path,user_profile,convert_tmp_dir,stem,verbose=False):
 assert Path(doc_path).resolve()==DOC
 target=Path(convert_tmp_dir)/(stem+'.pdf');shutil.copy2(OUT/'candidata.pdf',target)
 return str(target),'Exportação Word somente leitura; sem salvar o DOCX'
module.convert_to_pdf=native
module.rasterize(str(DOC),str(OUT/'png_final'),dpi=96,verbose=False,emit_pdf=False)
print('77 páginas renderizadas com o rasterizador oficial')
