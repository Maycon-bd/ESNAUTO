"""Triagem aproximada em português, com localizadores; não certifica originalidade."""
from collections import defaultdict
from difflib import SequenceMatcher
from hashlib import sha256
import json,re,sys
from pathlib import Path
from docx import Document
from comparar_integridade_rascunho import targets,words

root=Path(__file__).resolve().parents[1]; audit=root/'reports/fechamento_integral_20261029'
doc=root/'reports/monografia/trabalho/fechamento_integral_20261029.docx'; digest=lambda p:sha256(p.read_bytes()).hexdigest()
assert digest(doc)=='3a6ac6ee012d5946cefcebaf5883818ff889b45b7de4ec7373a5446eabbbc5e6'
source=root/'reports/fechamento_integral_20261029/fontes_extraidas/SUP_CARDOSO_TESE_paginas.json'
pages=json.loads(source.read_text(encoding='utf8')); segments=[]
for page in pages:
 text=re.sub(r'(?<=\w)-\s*\n\s*(?=\w)','',page['texto'])
 text=re.sub(r'\s+',' ',text)
 sentences=re.split(r'(?<=[.!?])\s+(?=[A-ZÀ-Ú])',text)
 for i in range(len(sentences)):
  for width in (1,2):
   phrase=' '.join(sentences[i:i+width]); toks=words(phrase)
   if 12<=len(toks)<=140: segments.append({'pagina_pdf':page['pagina_pdf'],'texto':phrase,'tokens':toks})
index=defaultdict(set)
for j,s in enumerate(segments):
 t=s['tokens']
 for i in range(len(t)-3): index[tuple(t[i:i+4])].add(j)
items=[p for p in targets(Document(doc)) if p['id'].startswith('P_atual') and len(p['tokens'])>=15]
pairs=[]
for p in items:
 candidates=set(); t=p['tokens']
 for i in range(len(t)-3): candidates.update(index.get(tuple(t[i:i+4]),()))
 for j in candidates:
  s=segments[j]; match=SequenceMatcher(None,t,s['tokens'],autojunk=False); blocks=match.get_matching_blocks(); longest=max((b.size for b in blocks),default=0); ratio=match.ratio()
  if ratio>=.28 and longest>=4:
   pairs.append({'alvo':p['id'],'secao':p['secao'],'pagina_pdf':s['pagina_pdf'],'razao':round(ratio,4),'maior_sequencia_palavras':longest,'texto_alvo':p['texto'],'trecho_fonte':s['texto']})
pairs.sort(key=lambda x:(-x['razao'],-x['maior_sequencia_palavras']))
result={'sha256_base_v005':'2af31abca4e3ba9fd5caf7cd161e55472dc94edc136cdf89732c0d0401118d6b','sha256_rascunho':digest(doc),'sha256_tese':digest(root/'reports/tese_Fabian_Correa_Cardoso.pdf'),'sha256_extracao':digest(source),'paragrafos_alvo':len(items),'segmentos_fonte':len(segments),'metodo':'Trechos de uma ou duas frases da extração da tese; candidatos compartilham quatro palavras normalizadas consecutivas, razão de SequenceMatcher >= 0,28. Triagem contextual, não taxa de plágio.', 'limites':'Não identifica paráfrases que escapem ao filtro, traduções, imagens, ou materiais externos à tese. A extração de PDF pode perder texto. Inclui referências da própria tese; comparar contexto antes de qualquer conclusão.', 'pares':pairs}
f=audit/'semelhanca_cardoso_lote121.json'; assert not f.exists(); f.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8'); print('parágrafos',len(items),'segmentos',len(segments),'pares',len(pairs));
for x in pairs[:20]: print(x['alvo'],x['pagina_pdf'],x['razao'],x['maior_sequencia_palavras'],x['texto_alvo'][:100].encode('ascii','backslashreplace').decode())
