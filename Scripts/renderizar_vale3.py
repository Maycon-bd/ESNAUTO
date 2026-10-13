"""Rasteriza pelo render_docx.py o PDF exportado pelo Word, conforme fallback local."""
from pathlib import Path
root=Path(__file__).resolve().parents[1]
out=root/'reports/vale3_comparacao'
(out/'final').mkdir(exist_ok=True)
import shutil
shutil.copy2(out/'monografia_resultados_VALE3.pdf',out/'final/monografia.pdf')
src=(root/'Scripts/renderizar_monografia_word.py').read_text(encoding='utf-8')
src=src.replace("ROOT/'reports/qa_monografia_bibliometria'", "ROOT/'reports/vale3_comparacao'")
src=src.replace('MayconGarciaSilva_monografia_bibliometria_VALE3.docx','MayconGarciaSilva_monografia_resultados_VALE3.docx')
exec(compile(src,str(root/'Scripts/renderizar_monografia_word.py'),'exec'))
