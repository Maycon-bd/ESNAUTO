from pathlib import Path
import hashlib,json,zipfile
from lxml import etree as E
from PIL import Image,ImageChops
B=Path(__file__).resolve().parent;R=B.parents[1]
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
base=R/'reports/monografia/versoes/v012/MayconGarciaSilva_monografia_v012.docx'
work=R/'reports/monografia/trabalho/declaracao_ia_assinaturas_20261102.docx'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
with zipfile.ZipFile(base) as a,zipfile.ZipFile(work) as z:
 changed=[k for k in a.namelist() if a.read(k)!=z.read(k)];assert changed==['word/document.xml']
 old=E.fromstring(a.read('word/document.xml')).find('w:body',NS);new=E.fromstring(z.read('word/document.xml')).find('w:body',NS)
 assert len(old)==len(new)
 diffs=[]
 for i,(x,y) in enumerate(zip(old,new)):
  if E.tostring(x)!=E.tostring(y):
   tx=''.join(x.xpath('.//w:t/text()',namespaces=NS));ty=''.join(y.xpath('.//w:t/text()',namespaces=NS))
   assert tx.startswith(('Rio Verde/GO,','Fase do TFC / Processo')) or tx=='_____________________________________________'
   diffs.append({'indice':i,'antes':tx,'depois':ty})
 assert len(diffs)==4
 ot=old.findall('w:tbl',NS);nt=new.findall('w:tbl',NS)
 assert len(ot)==len(nt)==15
 assert all(E.tostring(x)==E.tostring(y) for x,y in zip(ot[:-1],nt[:-1]))
 cellchanges=[]
 for x,y in zip(ot[-1].findall('.//w:tc',NS),nt[-1].findall('.//w:tc',NS)):
  tx=''.join(x.xpath('.//w:t/text()',namespaces=NS));ty=''.join(y.xpath('.//w:t/text()',namespaces=NS))
  if tx!=ty:cellchanges.append((tx,ty))
 assert len(cellchanges)==2
 assert 'slides' not in ''.join(nt[-1].xpath('.//w:t/text()',namespaces=NS))
 assert 'roteiro' not in ''.join(nt[-1].xpath('.//w:t/text()',namespaces=NS))
oldmap=json.loads((R/'reports/declaracao_ia_reescrita_20261102/mapa_final.json').read_text(encoding='utf-8-sig'))
newmap=json.loads((B/'mapa_final.json').read_text(encoding='utf-8-sig'))
assert newmap['pages']==oldmap['pages']==81
assert oldmap['items']==newmap['items']
different=[]
for p in range(1,82):
 with Image.open(B/f'word_final/page-{p}.png') as a,Image.open(R/f'reports/declaracao_ia_reescrita_20261102/word_final/page-{p}.png') as o:
  if ImageChops.difference(a.convert('RGB'),o.convert('RGB')).getbbox():different.append(p)
assert different==[81],different
proof={'base':'v012','base_sha256':sha(base),'trabalho_sha256':sha(work),'paginas':81,'paginas_identicas':80,'paginas_alteradas':different,'partes_alteradas':changed,'elementos_alterados':diffs,'tabelas_identicas':14,'celulas_declaracao_alteradas':cellchanges,'localizadores_preservados':len(newmap['items']),'declaracao_sha256':sha(B/'entrega/Declaracao_responsabilidade_coletiva_Maycon_assinaturas.docx')}
(B/'conferencia_final.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(proof,ensure_ascii=False))
