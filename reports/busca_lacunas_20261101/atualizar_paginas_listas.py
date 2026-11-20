from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from lxml import etree as E
import json,re,hashlib
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
DOC=ROOT/'reports/monografia/trabalho/busca_lacunas_20261101.docx'
info=json.loads((OUT/'paginacao_candidata.json').read_text(encoding='utf-8-sig'))
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
def text(p):return ''.join((n.text or '') if n.tag.endswith('}t') else '\t' if n.tag.endswith('}tab') else '\n' for n in p.xpath('.//w:t|.//w:r/w:tab|.//w:r/w:br',namespaces=ns))
def norm(s):return re.sub(r'\s+',' ',s).strip()
titles={(t['number'],norm(t['title'])):t for t in info['titles']}
captions={norm(t['title']):t for t in info['captions']}
assert len(titles)==41 and len(captions)==19
assert [t['number'] for t in info['titles'] if t['style']=='TITULO TCC']==['1','2','3','4','5','6','']
assert [t['number'] for t in info['titles'] if t['style']=='SUBÇÃO 2']==['3.8.1','3.8.2','3.8.3','3.8.4']
with ZipFile(DOC) as z:parts={n:z.read(n) for n in z.namelist()}
root=E.fromstring(parts['word/document.xml']);changes=[];seen=[]
for p in root.xpath('//w:body/w:p',namespaces=ns):
 t=text(p)
 if t=='INTRODUÇÃO':break
 if '\t' not in t:continue
 prefix,page=t.rsplit('\t',1)
 if not page.isdigit():continue
 fields=prefix.split('\t')
 key=(fields[0],norm(fields[-1])) if len(fields)>1 else ('',norm(prefix))
 target=titles.get(key)
 kind='sumario'
 if target is None:target=captions.get(norm(prefix));kind='lista'
 if target is None:continue
 wanted=str(target['page']);nodes=p.xpath('.//w:t',namespaces=ns)
 assert nodes[-1].text==page,(t,[n.text for n in nodes])
 if page!=wanted:nodes[-1].text=wanted;changes.append({'tipo':kind,'titulo':prefix,'antes':page,'depois':wanted})
 seen.append({'tipo':kind,'titulo':prefix,'pagina':wanted})
assert sum(s['tipo']=='sumario' for s in seen)==41
assert sum(s['tipo']=='lista' for s in seen)==19
parts['word/document.xml']=E.tostring(root,encoding='UTF-8',xml_declaration=True,standalone=True)
with ZipFile(DOC,'w',ZIP_DEFLATED) as z:
 for n,data in parts.items():z.writestr(n,data)
(OUT/'paginas_listas_atualizadas.json').write_text(json.dumps({'conferidas':seen,'alteradas':changes,'sha256_candidata':hashlib.sha256(DOC.read_bytes()).hexdigest()},ensure_ascii=False,indent=2),encoding='utf-8')
print('60 entradas conciliadas,',len(changes),'páginas atualizadas; títulos e ordem preservados.')
