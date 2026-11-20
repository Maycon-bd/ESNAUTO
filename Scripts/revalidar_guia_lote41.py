"""Executa conferência estrutural anterior sobre o rascunho atual, em pasta separada."""
from pathlib import Path
import hashlib
root=Path(__file__).resolve().parents[1];doc=root/'reports/monografia/trabalho/fechamento_integral_20261029.docx'
assert hashlib.sha256(doc.read_bytes()).hexdigest()=='4cf48044445c0760210b1206c185487b8406af3eaecb541de6db381cdbf735b0'
script=(root/'Scripts/auditar_integral_fasoft.py').read_text(encoding='utf8')
replacements={
 "QA=ROOT/'reports/auditoria_integral_fasoft_20261028'":"QA=ROOT/'reports/fechamento_integral_20261029/guia_lote41'",
 "SRC=ROOT/'reports/monografia/MayconGarciaSilva_monografia_padronizada_FASOFT.docx'":"SRC=ROOT/'reports/monografia/versoes/v005/MayconGarciaSilva_monografia_v005.docx'",
 "OUT=ROOT/'reports/monografia/MayconGarciaSilva_monografia_FASOFT_conferida.docx'":"OUT=ROOT/'reports/monografia/trabalho/fechamento_integral_20261029.docx'"}
for a,b in replacements.items():assert script.count(a)==1;script=script.replace(a,b)
exec(compile(script,str(root/'Scripts/auditar_integral_fasoft.py'),'exec'),{'__file__':str(root/'Scripts/auditar_integral_fasoft.py'),'__name__':'__main__'})
