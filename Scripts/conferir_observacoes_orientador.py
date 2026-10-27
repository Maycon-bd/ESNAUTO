from pathlib import Path
import sys,shutil
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reports/observacoes_orientador_20261026'
if '--listas' in sys.argv:
    text=(ROOT/'Scripts/ajustar_listas_vale3.py').read_text(encoding='utf-8')
    text=text.replace('MayconGarciaSilva_monografia_resultados_VALE3.docx','MayconGarciaSilva_monografia_observacoes_atendidas.docx')
    text=text.replace('reports/vale3_comparacao/monografia_resultados_VALE3.pdf','reports/observacoes_orientador_20261026/monografia_observacoes_atendidas.pdf')
    exec(compile(text,str(ROOT/'Scripts/ajustar_listas_vale3.py'),'exec'))
else:
    (OUT/'final').mkdir(exist_ok=True)
    shutil.copy2(OUT/'monografia_observacoes_atendidas.pdf',OUT/'final/monografia.pdf')
    text=(ROOT/'Scripts/renderizar_monografia_word.py').read_text(encoding='utf-8')
    text=text.replace("ROOT/'reports/qa_monografia_bibliometria'","ROOT/'reports/observacoes_orientador_20261026'")
    text=text.replace('MayconGarciaSilva_monografia_bibliometria_VALE3.docx','MayconGarciaSilva_monografia_observacoes_atendidas.docx')
    text=text.replace('documents/26.1011.11113','documents/26.1025.11240')
    exec(compile(text,str(ROOT/'Scripts/renderizar_monografia_word.py'),'exec'))
