"""Executa conferência estrutural anterior sobre o rascunho atual, em pasta separada."""
from pathlib import Path
import hashlib
root=Path(__file__).resolve().parents[1];doc=root/'reports/monografia/trabalho/fechamento_integral_20261029.docx'
assert hashlib.sha256(doc.read_bytes()).hexdigest()=='31ec505d2f39784a17b6d076f5a0893cc8753f25cdab6bb1a4095eeef363268f'
script=(root/'Scripts/auditar_integral_fasoft.py').read_text(encoding='utf8')
replacements={
 "QA=ROOT/'reports/auditoria_integral_fasoft_20261028'":"QA=ROOT/'reports/fechamento_integral_20261029/guia_lote126'",
 "SRC=ROOT/'reports/monografia/MayconGarciaSilva_monografia_padronizada_FASOFT.docx'":"SRC=ROOT/'reports/monografia/versoes/v005/MayconGarciaSilva_monografia_v005.docx'",
 "OUT=ROOT/'reports/monografia/MayconGarciaSilva_monografia_FASOFT_conferida.docx'":"OUT=ROOT/'reports/monografia/trabalho/fechamento_integral_20261029.docx'"}
for a,b in replacements.items():assert script.count(a)==1;script=script.replace(a,b)
exec(compile(script,str(root/'Scripts/auditar_integral_fasoft.py'),'exec'),{'__file__':str(root/'Scripts/auditar_integral_fasoft.py'),'__name__':'__main__'})



