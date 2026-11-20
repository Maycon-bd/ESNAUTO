import importlib.util,shutil,sys
from pathlib import Path
build=Path(__file__).resolve().parent
skill=Path('C:/Users/User/.codex/plugins/cache/openai-primary-runtime/documents/26.1026.10807/skills/documents/render_docx.py')
spec=importlib.util.spec_from_file_location('docx_renderer',skill)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
def native_pdf(doc_path,user_profile,convert_tmp_dir,stem,verbose=False):
    out=Path(convert_tmp_dir)/(stem+'.pdf')
    shutil.copy2(build/'roteiro_word.pdf',out)
    return str(out),'PDF exportado do Word em leitura; DOCX preservado'
mod.convert_to_pdf=native_pdf
sys.argv=[str(skill),str(build.parent/'entrega/Roteiro_video_ESNAUTO_25min_v008.docx'),'--output_dir',str(build/'roteiro_render'),'--emit_pdf']
mod.main()
