from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from copy import deepcopy
from lxml import etree as E
import json,re,hashlib,shutil

ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
BASE=ROOT/'reports/monografia/versoes/v008/MayconGarciaSilva_monografia_v008.docx'
RECEBIDO=Path('C:/Users/User/Downloads/MayconGarciaSilva_monografia_correcao final antes da banca.docx')
DEST=ROOT/'reports/monografia/trabalho/devolutiva_orientador_20261101.docx'
W='http://schemas.openxmlformats.org/wordprocessingml/2006/main';ns={'w':W}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def txt(p):return ''.join(p.xpath('.//w:t/text()',namespaces=ns))
assert sha(BASE)=='0daacd3ea1753bca97619df025923b92a44a047b5c1252a4677f802dfe870dad'
assert sha(RECEBIDO)=='5c80490f4f698b27011037779c84622fc0aed3fd4d0ff54fee71385ffd7d2376'
shutil.copy2(RECEBIDO,OUT/'recebido_original.docx')
with ZipFile(BASE) as z:parts={i.filename:z.read(i.filename) for i in z.infolist()}
with ZipFile(RECEBIDO) as z:source=E.fromstring(z.read('word/document.xml'))
doc=E.fromstring(parts['word/document.xml']);body=doc.find('w:body',ns);ib=source.find('w:body',ns)
def interval(b):
 nodes=list(b);a=next(i for i,p in enumerate(nodes) if p.tag==f'{{{W}}}p' and txt(p)=='INTRODUÇÃO');e=next(i for i,p in enumerate(nodes[a+1:],a+1) if p.tag==f'{{{W}}}p' and txt(p)=='REVISÃO DA LITERATURA');return nodes[a+1:e]
old=interval(body);incoming=interval(ib)
assert len(old)==14 and len(incoming)==15
lookup={txt(p):p for p in old}
new=[];changes=[]
for p in incoming:
 t=txt(p)
 if t in lookup:q=deepcopy(lookup[t])
 else:
  q=deepcopy(p)
  for pr in q.findall('w:pPr',ns):q.remove(pr)
  template=old[3] if t.startswith('O problema de pesquisa') else old[0]
  pr=template.find('w:pPr',ns)
  if pr is not None:q.insert(0,deepcopy(pr))
  for color in q.xpath('.//w:color',namespaces=ns):
   if color.get(f'{{{W}}}val','').upper()=='FF0000':color.set(f'{{{W}}}val','000000')
 new.append(q)

def replace_span(paragraph,old_text,replacement):
 """Substituir texto preservando os runs externos, incluindo subscritos e itálico."""
 nodes=paragraph.xpath('.//w:t',namespaces=ns);full=''.join(n.text or '' for n in nodes)
 assert full.count(old_text)==1,(old_text,full)
 start=full.index(old_text);end=start+len(old_text);pos=0;affected=[]
 for node in nodes:
  text=node.text or '';lo=pos;hi=pos+len(text)
  if hi>start and lo<end:affected.append((node,text,max(0,start-lo),min(len(text),end-lo)))
  pos=hi
 first,first_text,left,_=affected[0];last,last_text,_,right=affected[-1]
 first_run=first.getparent();assert first_run.tag==f'{{{W}}}r'
 rp=first_run.find('w:rPr',ns)
 for node,text,a,b in affected:
  node.text=text[:a]+text[b:];node.set('{http://www.w3.org/XML/1998/namespace}space','preserve')
 suffix=''
 if first is last:
  suffix=first_text[right:];first.text=first_text[:left]
 insert_at=paragraph.index(first_run)+1
 for text,italic in replacement:
  run=E.Element(f'{{{W}}}r');pr=deepcopy(rp) if rp is not None else E.Element(f'{{{W}}}rPr')
  for it in pr.findall('w:i',ns)+pr.findall('w:iCs',ns):pr.remove(it)
  if italic:E.SubElement(pr,f'{{{W}}}i')
  run.append(pr);n=E.SubElement(run,f'{{{W}}}t');n.text=text;n.set('{http://www.w3.org/XML/1998/namespace}space','preserve');paragraph.insert(insert_at,run);insert_at+=1
 if suffix:
  run=deepcopy(first_run)
  for n in run.xpath('.//w:t',namespaces=ns):n.text=''
  run.find('w:t',ns).text=suffix;run.find('w:t',ns).set('{http://www.w3.org/XML/1998/namespace}space','preserve');paragraph.insert(insert_at,run)

problem=next(p for p in new if txt(p).startswith('O problema de pesquisa'))
replace_span(problem,'uma ESN',[('uma Rede Neural de Estados de Eco (',False),('Echo State Network',True),(' – ESN)',False)])
fundamental=next(p for p in new if txt(p).startswith('A abordagem central emprega'))
replace_span(fundamental,'Redes Neurais de Estados de Eco (Echo State Networks – ESNs)',[('ESNs',False)])
at=body.index(old[0])
for p in old:body.remove(p)
for offset,p in enumerate(new):body.insert(at+offset,p)
parts['word/document.xml']=E.tostring(doc,encoding='UTF-8',xml_declaration=True,standalone=True)
with ZipFile(DEST,'w',ZIP_DEFLATED) as z:
 for name,value in parts.items():z.writestr(name,value)
entry={'base':'v008','sha256_base':sha(BASE),'sha256_recebido':sha(RECEBIDO),'sha256_candidata':sha(DEST),'paragrafos_introducao_antes':len(old),'paragrafos_introducao_depois':len(new),'introducao_antes':[txt(p) for p in old],'introducao_depois':[txt(p) for p in new],'escopo':'Redação e ordem da introdução conforme devolutiva, com expansão de ESN na primeira ocorrência e retirada da redefinição posterior. Introdução contínua, sem subtítulos. Fora dela, conteúdo da v008 preservado. Interrogações mantidas com significado documentado. Nenhum resultado ou imagem alterado.'}
(OUT/'conciliacao_introducao.json').write_text(json.dumps(entry,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'artifact.md').write_text('# Referência editorial\n\nBase v008 SHA256 '+sha(BASE)+'\n\nPreservar integralmente o pacote da v008, exceto os 14 parágrafos da introdução substituídos pelos 15 parágrafos conciliados. Manter estilos, seções, listas, tabelas, imagens e cabeçalhos. O recebido é fonte das mudanças de texto, não modelo para reimportar a formatação regravada pelo LibreOffice. A4, corpo Times New Roman 12 e estilos institucionais existentes. Numeração automática dos títulos preservada. Sumário e listas são texto tabulado estático e precisam ser conciliados com a paginação exportada. Nenhuma subdivisão na introdução, segundo PDF25 do Guia FASOFT.\n',encoding='utf-8')
print('Introdução conciliada em cópia baseada na v008; resultados e imagens preservados.')
