from pathlib import Path
import copy,hashlib,json,re,zipfile
from lxml import etree as E
B=Path(__file__).resolve().parent;R=B.parents[1];B.mkdir(exist_ok=True)
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
q=lambda t:'{'+NS['w']+'}'+t
base=R/'reports/monografia/versoes/v013/MayconGarciaSilva_monografia_v013.docx'
work=R/'reports/monografia/trabalho/sumario_links_20261102.docx'
assert hashlib.sha256(base.read_bytes()).hexdigest()=='ff4f2978111152c4b1d2dea38b066f0b549b5fc34d13d49a674f559d0c59a47b'
def text(p):return ''.join(('\t' if e.tag==q('tab') else e.text or '') for e in p.iter() if e.tag in (q('tab'),q('t')))
def style(p):
 s=p.find('w:pPr/w:pStyle',NS);return s.get(q('val')) if s is not None else ''
with zipfile.ZipFile(base) as z:
 original_xml=z.read('word/document.xml')
 root=E.fromstring(original_xml);body=root.find('w:body',NS)
 entries=[p for p in body if style(p).startswith('Sumrio')]
 targets=[p for p in body if style(p) in ('TITULOTCC','SEOTCC','SUBO2') and list(body).index(p)>list(body).index(entries[-1]) or text(p)=='ANEXO']
 assert len(entries)==len(targets)==42,(len(entries),len(targets))
 ids=[int(x.get(q('id'))) for x in root.findall('.//w:bookmarkStart',NS)]
 nextid=max(ids)+1;names={x.get(q('name')) for x in root.findall('.//w:bookmarkStart',NS)}
 manifest=[]
 for i,(entry,target) in enumerate(zip(entries,targets),1):
  parts=text(entry).split('\t');title=parts[-2];page=int(parts[-1])
  expected='ANEXO' if title=='ANEXOS' else title
  assert text(target)==expected,(title,text(target))
  name=f'ESNAUTO_Sumario_{i:03d}';assert name not in names
  start=E.Element(q('bookmarkStart'));start.set(q('id'),str(nextid));start.set(q('name'),name)
  end=E.Element(q('bookmarkEnd'));end.set(q('id'),str(nextid));nextid+=1
  target.insert(1 if target.find('w:pPr',NS) is not None else 0,start);target.append(end)
  link=E.Element(q('hyperlink'));link.set(q('anchor'),name);link.set(q('history'),'1')
  link.set(q('tooltip'),'Ir para '+title)
  for child in list(entry):
   if child.tag!=q('pPr'):entry.remove(child);link.append(child)
  entry.append(link)
  manifest.append({'entrada':text(entry),'titulo':title,'destino':expected,'bookmark':name,'pagina':page})
 with zipfile.ZipFile(work,'w',zipfile.ZIP_DEFLATED) as out:
  for info in z.infolist():out.writestr(info,E.tostring(root,encoding='UTF-8',xml_declaration=True,standalone=True) if info.filename=='word/document.xml' else z.read(info.filename))
 # Remove only the newly introduced navigation and recover the original XML exactly.
 check=copy.deepcopy(root)
 for link in list(check.findall('.//w:hyperlink',NS)):
  parent=link.getparent();at=parent.index(link)
  for child in list(link):link.remove(child);parent.insert(at,child);at+=1
  parent.remove(link)
 for mark in list(check.findall('.//w:bookmarkStart',NS)):
  if mark.get(q('name'),'').startswith('ESNAUTO_Sumario_'):
   ident=mark.get(q('id'));mark.getparent().remove(mark)
   ends=check.xpath('.//w:bookmarkEnd[@w:id="'+ident+'"]',namespaces=NS);assert len(ends)==1
   ends[0].getparent().remove(ends[0])
 assert E.tostring(check)==E.tostring(E.fromstring(original_xml))
(B/'links.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
(B/'estrutura.json').write_text(json.dumps({'base':'v013','base_sha256':hashlib.sha256(base.read_bytes()).hexdigest(),'trabalho_sha256':hashlib.sha256(work.read_bytes()).hexdigest(),'links':42,'conteudo_e_formatacao_originais_recuperados_exatamente_apos_remover_navegacao':True},ensure_ascii=False,indent=2),encoding='utf-8')
previous=R/'reports/declaracao_ia_assinaturas_20261102'
src=(previous/'word_qa.ps1').read_text(encoding='utf-8-sig').replace('declaracao_ia_assinaturas_20261102',B.name).replace('versoes\\v012\\MayconGarciaSilva_monografia_v012.docx','versoes\\v013\\MayconGarciaSilva_monografia_v013.docx')
test='''
 $taskExpected=Get-Content (Join-Path $taskRoot 'links.json') -Raw -Encoding utf8|ConvertFrom-Json
 $taskTest=@()
 foreach($taskH in $taskDoc.Hyperlinks) {
  $taskAnchor=$taskH.SubAddress
  $taskMatch=@($taskExpected|Where-Object {$_.bookmark -eq $taskAnchor})
  if($taskMatch.Count -ne 1){throw "Destino inesperado: $taskAnchor"}
  $taskBookmark=$taskDoc.Bookmarks.Item($taskAnchor).Range
  $taskPage=$taskBookmark.Information(1)
  $taskH.Follow()
  $taskPosition=$taskWord.Selection.Range.Start
  $taskOK=($taskPosition -eq $taskBookmark.Start -and $taskPage -eq $taskMatch[0].pagina)
  if(-not $taskOK){throw "Navegação incorreta: $taskAnchor"}
  $taskTest+=@{anchor=$taskAnchor;page=$taskPage;start=$taskBookmark.Start;followed=$taskOK}
 }
 if($taskTest.Count -ne 42){throw 'Quantidade de links incorreta'}
 $taskTest|ConvertTo-Json -Depth 4|Set-Content (Join-Path $taskRoot 'teste_links_word.json') -Encoding utf8
 Write-Output ('Links seguidos e conferidos: '+$taskTest.Count)
'''
src=src.replace(" Write-Output ('Paginas '+$taskCount+'; etapa '+$Stage)"," Write-Output ('Paginas '+$taskCount+'; etapa '+$Stage)\n"+test)
(B/'word_qa.ps1').write_text(src,encoding='utf-8-sig')
src=(previous/'renderizar.py').read_text(encoding='utf-8').replace('declaracao_ia_assinaturas_20261102',B.name)
(B/'renderizar.py').write_text(src,encoding='utf-8')
print('42 entradas do sumário vinculadas aos títulos correspondentes.')
