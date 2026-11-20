"""Cruzamento autor–ano; não substitui avaliação de sustentação científica."""
from pathlib import Path
import json,re,unicodedata
from docx import Document
ROOT=Path(__file__).resolve().parents[1];QA=ROOT/'reports/auditoria_integral_fasoft_20261028'
d=Document(ROOT/'reports/monografia/MayconGarciaSilva_monografia_FASOFT_conferida.docx')
refs=[p.text for p in d.paragraphs if p.style.name=='Referencias']
def norm(s):return ''.join(c for c in unicodedata.normalize('NFD',s.casefold()) if not unicodedata.combining(c))
names=sorted({x.split(',')[0] for x in refs},key=len,reverse=True)
name='(?:'+'|'.join(map(re.escape,names))+')'
year=r'(?:19|20)\d{2}[a-z]?'
co=r'(?:\s*(?:;|,|e\b|&)\s*[A-ZÀ-Ü][A-Za-zÀ-ü-]+)*'
lead=r'\b(?P<autor>'+name+r')(?:\s+[A-Z]\.)?(?:\s+et al\.)?'+co
patterns=[re.compile(lead+r'\s*\((?P<anos>'+year+r'(?:\s*,\s*'+year+r')*)\)',re.I),re.compile(lead+r'\s*,\s*(?P<anos>'+year+r')',re.I)]
ps=d.paragraphs+[p for t in d.tables for row in t.rows for c in row.cells for p in c.paragraphs]
records=[]
for pi,p in enumerate(ps):
 if p.style.name=='Referencias':continue
 for pattern in patterns:
  for m in pattern.finditer(p.text):
   for y in re.findall(year,m['anos']):
    found=[r for r in refs if norm(r.split(',')[0])==norm(m['autor']) and re.search(r'(?<!\d)'+y+r'(?![a-z\d])',r,re.I)]
    records.append({'paragrafo':pi,'citacao':m[0],'ano':y,'referencias':found})
missing=[r for r in records if not r['referencias']]
report={'metodo':'Padrões autor–ano narrativos e parentéticos, com conferência dos grupos compostos na leitura. Não avalia se cada afirmação é sustentada pela obra.','referencias':len(refs),'ocorrencias_reconhecidas':len(records),'sem_correspondencia':missing,'epigrafe':'Alternativa de Gleick verificada no primeiro parágrafo do artigo assinado pelo autor, com referência eletrônica e localizador, sem página de livro inventada.','registros':records}
(QA/'cruzamento_citacoes.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('Reconhecidas:',len(records),'sem correspondência:',len(missing))
for r in missing:print(r['citacao'])
