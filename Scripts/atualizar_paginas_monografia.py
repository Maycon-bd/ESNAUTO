"""Atualiza números estáticos sem alterar marcadores de parágrafo ou seções."""
from pathlib import Path
import json,re
from docx import Document
ROOT=Path(__file__).resolve().parents[1]
out=ROOT/'reports/monografia/MayconGarciaSilva_monografia_bibliometria_VALE3.docx'
page_map=json.loads((ROOT/'reports/qa_monografia_bibliometria/final/mapa_paginas.json').read_text(encoding='utf-8-sig'))
d=Document(out)
count=0
def norm(x):return ' '.join(x.split()).casefold()
for p in d.paragraphs:
    if '\t' not in p.text or not re.search(r'\t\d+\s*$',p.text):continue
    parts=p.text.split('\t')
    title=parts[-2]
    found=[x for x in page_map if norm(x['texto'])==norm(title)]
    if len(found)>1 and len(parts)>=3:
        found=[x for x in found if x['numero']==parts[0].strip()]
    if len(found)!=1:raise ValueError(f'Entrada sem correspondência unívoca: {p.text}')
    target=str(found[0]['pagina'])
    if parts[-1].strip()==target:continue
    # No original e na lista nova, o número final está contido no último run.
    for run in reversed(p.runs):
        if re.search(r'\d+\s*$',run.text):
            run.text=re.sub(r'\d+\s*$',target,run.text);count+=1;break
    else:raise ValueError(p.text)
assert len(d.sections)==6
d.save(out)
print(f'{count} números atualizados; seis seções preservadas.')
