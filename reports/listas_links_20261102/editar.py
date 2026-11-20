from pathlib import Path
import copy,hashlib,json,re,zipfile
from lxml import etree as E
B=Path(__file__).resolve().parent;R=B.parents[1]
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'};q=lambda t:'{'+NS['w']+'}'+t
base=R/'reports/monografia/versoes/v014/MayconGarciaSilva_monografia_v014.docx'
work=R/'reports/monografia/trabalho/listas_links_20261102.docx'
assert hashlib.sha256(base.read_bytes()).hexdigest()=='b93979a24f68abb962e0ae36871990b791d7916bcf8229b001f6d20e09e0f539'
def text(p):return ''.join(('\t' if e.tag==q('tab') else e.text or '') for child in p if child.tag!=q('pPr') for e in child.iter() if e.tag in (q('tab'),q('t')))
def style(p):
 s=p.find('w:pPr/w:pStyle',NS);return s.get(q('val')) if s is not None else ''
with zipfile.ZipFile(base) as z:
 original=z.read('word/document.xml');root=E.fromstring(original);body=root.find('w:body',NS)
 pattern=r'^(Figura|Quadro|Tabela)\s+\d+\s*[–-]'
 entries=[p for p in body if re.match(pattern,text(p)) and re.search(r'\t\d+$',text(p))]
 targets={text(p):p for p in body if style(p)=='Legenda' and re.match(pattern,text(p))}
 assert len(entries)==len(targets)==19,(len(entries),len(targets))
 nextid=max(int(x.get(q('id'))) for x in root.findall('.//w:bookmarkStart',NS))+1
 manifest=[]
 for i,entry in enumerate(entries,1):
  title,page=text(entry).rsplit('\t',1);target=targets[title];name=f'ESNAUTO_Lista_{i:03d}'
  assert not root.xpath('.//w:bookmarkStart[@w:name="'+name+'"]',namespaces=NS)
  start=E.Element(q('bookmarkStart'));start.set(q('id'),str(nextid));start.set(q('name'),name)
  end=E.Element(q('bookmarkEnd'));end.set(q('id'),str(nextid));nextid+=1
  target.insert(1 if target.find('w:pPr',NS) is not None else 0,start);target.append(end)
  link=E.Element(q('hyperlink'));link.set(q('anchor'),name);link.set(q('history'),'1');link.set(q('tooltip'),'Ir para '+title)
  for child in list(entry):
   if child.tag!=q('pPr'):entry.remove(child);link.append(child)
  entry.append(link)
  manifest.append({'entrada':text(entry),'titulo':title,'destino':title,'bookmark':name,'pagina':int(page)})
 check=copy.deepcopy(root)
 for link in list(check.findall('.//w:hyperlink',NS)):
  if not link.get(q('anchor'),'').startswith('ESNAUTO_Lista_'):continue
  parent=link.getparent();at=parent.index(link)
  for child in list(link):link.remove(child);parent.insert(at,child);at+=1
  parent.remove(link)
 for mark in list(check.findall('.//w:bookmarkStart',NS)):
  if mark.get(q('name'),'').startswith('ESNAUTO_Lista_'):
   ident=mark.get(q('id'));mark.getparent().remove(mark)
   ends=check.xpath('.//w:bookmarkEnd[@w:id="'+ident+'"]',namespaces=NS);assert len(ends)==1
   ends[0].getparent().remove(ends[0])
 assert E.tostring(check)==E.tostring(E.fromstring(original))
 with zipfile.ZipFile(work,'w',zipfile.ZIP_DEFLATED) as out:
  for info in z.infolist():out.writestr(info,E.tostring(root,encoding='UTF-8',xml_declaration=True,standalone=True) if info.filename=='word/document.xml' else z.read(info.filename))
previous=R/'reports/sumario_links_20261102'
oldlinks=json.loads((previous/'links.json').read_text(encoding='utf-8'))
(B/'links.json').write_text(json.dumps(oldlinks+manifest,ensure_ascii=False,indent=2),encoding='utf-8')
(B/'estrutura.json').write_text(json.dumps({'base':'v014','base_sha256':hashlib.sha256(base.read_bytes()).hexdigest(),'trabalho_sha256':hashlib.sha256(work.read_bytes()).hexdigest(),'links_adicionados':19,'figuras':6,'quadros':6,'tabelas':7,'links_totais':61,'xml_original_recuperado_exatamente_apos_remover_apenas_nova_navegacao':True},ensure_ascii=False,indent=2),encoding='utf-8')
src=(previous/'word_qa.ps1').read_text(encoding='utf-8-sig').replace('sumario_links_20261102',B.name).replace('versoes\\v013\\MayconGarciaSilva_monografia_v013.docx','versoes\\v014\\MayconGarciaSilva_monografia_v014.docx').replace('$taskTest.Count -ne 42','$taskTest.Count -ne 61')
(B/'word_qa.ps1').write_text(src,encoding='utf-8-sig')
src=(previous/'renderizar.py').read_text(encoding='utf-8').replace('sumario_links_20261102',B.name)
(B/'renderizar.py').write_text(src,encoding='utf-8')
src=(previous/'conferir.py').read_text(encoding='utf-8').replace('v013','v014').replace('sumario_links_20261102.docx','listas_links_20261102.docx').replace('declaracao_ia_assinaturas_20261102','sumario_links_20261102').replace('==42','==61').replace("'links_testados_por_follow_no_word':42","'links_testados_por_follow_no_word':61")
(B/'conferir.py').write_text(src,encoding='utf-8')
print('19 links adicionados às listas: 6 figuras, 6 quadros e 7 tabelas; 42 links do sumário preservados.')
