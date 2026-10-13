from pathlib import Path
import re
from docx import Document
from pypdf import PdfReader
root=Path(__file__).resolve().parents[1]
path=root/'reports/monografia/MayconGarciaSilva_monografia_resultados_VALE3.docx'
d=Document(path)
pdf=PdfReader(root/'reports/vale3_comparacao/monografia_resultados_VALE3.pdf')
norm=lambda s:''.join(c for c in s.casefold() if c.isalnum())
body=[]
rawbody=[]
for i,p in enumerate(pdf.pages):
    txt=p.extract_text()
    if i<14:continue
    m=re.match(r'^\s*(\d+)\s',txt)
    if m:
        body.append((int(m[1]),norm(txt)))
        rawbody.append((int(m[1]),txt))
for p in d.paragraphs:
    if p.text.startswith('A Tabela 8 apresenta'):
        for r in p.runs:r.text=r.text.replace('A Tabela 8 apresenta','A Tabela 10 apresenta')
    if '\t' not in p.text or not re.search(r'\t\d+\s*$',p.text):continue
    parts=p.text.split('\t');title=parts[-2]
    found=[page for page,txt in body if norm(title) in txt]
    if norm(title)=='referências':
        found=[page for page,txt in rawbody if any(norm(line)==norm(title) for line in txt.splitlines())]
    if not found:raise ValueError('Entrada ausente do PDF: '+title)
    # Títulos curtos de capítulos devem ocorrer como cabeçalhos numerados.
    if len(parts)>=3:
        pair=norm(parts[0]+title)
        exact=[page for page,txt in body if pair in txt]
        if exact:found=exact
    for r in reversed(p.runs):
        if re.search(r'\d+\s*$',r.text):
            r.text=re.sub(r'\d+\s*$',str(found[0]),r.text);break
d.save(path)
print('Listas conferidas pela numeração impressa do PDF.')
