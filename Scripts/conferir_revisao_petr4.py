"""Confere listas ou rasteriza a revisão usando o renderer da habilidade documents."""
from pathlib import Path
import sys,shutil
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reports/revisao_orientador_petr4'
if '--listas' in sys.argv:
    text=(ROOT/'Scripts/ajustar_listas_vale3.py').read_text(encoding='utf-8')
    text=text.replace('MayconGarciaSilva_monografia_resultados_VALE3.docx','MayconGarciaSilva_monografia_PETR4_revisao_orientador.docx')
    text=text.replace('reports/vale3_comparacao/monografia_resultados_VALE3.pdf','reports/revisao_orientador_petr4/monografia_PETR4_revisao_orientador.pdf')
    exec(compile(text,str(ROOT/'Scripts/ajustar_listas_vale3.py'),'exec'))
else:
    (OUT/'final').mkdir(exist_ok=True)
    shutil.copy2(OUT/'monografia_PETR4_revisao_orientador.pdf',OUT/'final/monografia.pdf')
    text=(ROOT/'Scripts/renderizar_monografia_word.py').read_text(encoding='utf-8')
    text=text.replace("ROOT/'reports/qa_monografia_bibliometria'","ROOT/'reports/revisao_orientador_petr4'")
    text=text.replace('MayconGarciaSilva_monografia_bibliometria_VALE3.docx','MayconGarciaSilva_monografia_PETR4_revisao_orientador.docx')
    text=text.replace('documents/26.1011.11113','documents/26.1022.11436')
    exec(compile(text,str(ROOT/'Scripts/renderizar_monografia_word.py'),'exec'))
