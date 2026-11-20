from pathlib import Path
import hashlib,json,zipfile
from PIL import Image,ImageChops
from lxml import etree as E
B=Path(__file__).resolve().parent;R=B.parents[1]
base=R/'reports/monografia/versoes/v013/MayconGarciaSilva_monografia_v013.docx'
work=R/'reports/monografia/trabalho/sumario_links_20261102.docx'
with zipfile.ZipFile(base) as a,zipfile.ZipFile(work) as z:
 parts=[k for k in a.namelist() if a.read(k)!=z.read(k)];assert parts==['word/document.xml']
 n={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
 old=E.fromstring(a.read('word/document.xml'));new=E.fromstring(z.read('word/document.xml'))
 assert old.xpath('.//w:t/text()',namespaces=n)==new.xpath('.//w:t/text()',namespaces=n)
 assert [E.tostring(t) for t in old.findall('.//w:tbl',n)]==[E.tostring(t) for t in new.findall('.//w:tbl',n)]
 assert len(new.findall('.//w:hyperlink',n))==42
before=json.loads((R/'reports/declaracao_ia_assinaturas_20261102/mapa_final.json').read_text(encoding='utf-8-sig'))
after=json.loads((B/'mapa_final.json').read_text(encoding='utf-8-sig'))
assert before['pages']==after['pages']==81
assert before['items']==after['items']
different=[]
for p in range(1,82):
 with Image.open(R/f'reports/declaracao_ia_assinaturas_20261102/word_final/page-{p}.png') as a,Image.open(B/f'word_final/page-{p}.png') as z:
  if ImageChops.difference(a.convert('RGB'),z.convert('RGB')).getbbox():different.append(p)
tests=json.loads((B/'teste_links_word.json').read_text(encoding='utf-8-sig'))
assert len(tests)==42 and all(t['followed'] for t in tests)
proof={'base':'v013','base_sha256':hashlib.sha256(base.read_bytes()).hexdigest(),'trabalho_sha256':hashlib.sha256(work.read_bytes()).hexdigest(),'partes_alteradas':parts,'links_testados_por_follow_no_word':42,'paginas':81,'localizadores_preservados':81,'paginas_identicas':81-len(different),'paginas_diferentes':different,'texto_e_tabelas_preservados':True}
(B/'conferencia_final.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(proof,ensure_ascii=False))
