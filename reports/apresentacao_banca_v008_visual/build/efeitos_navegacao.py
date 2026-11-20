import json,re,posixpath
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from lxml import etree as E
B=Path(__file__).resolve().parent
P='http://schemas.openxmlformats.org/presentationml/2006/main'
A='http://schemas.openxmlformats.org/drawingml/2006/main'
R='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
PKG='http://schemas.openxmlformats.org/package/2006/relationships'
ns={'p':P,'a':A,'r':R}
links=[]
with ZipFile(B/'visual_sem_efeitos.pptx') as src:
 parts={i.filename:src.read(i.filename) for i in src.infolist()}
 for n in range(1,24):
  member=f'ppt/slides/slide{n}.xml';rels=f'ppt/slides/_rels/slide{n}.xml.rels'
  root=E.fromstring(parts[member]);rr=E.fromstring(parts[rels]) if rels in parts else E.Element(f'{{{PKG}}}Relationships',nsmap={None:PKG})
  for item in root.xpath('//p:cNvPr[starts-with(@name,"nav-")]',namespaces=ns):
   target=int(item.get('name').split('-')[1]);assert 1<=target<=23
   existing={e.get('Id') for e in rr};j=1
   while f'rIdNav{j}' in existing:j+=1
   rid=f'rIdNav{j}'
   E.SubElement(rr,f'{{{PKG}}}Relationship',Id=rid,Type=R+'/slide',Target=f'slide{target}.xml')
   h=E.Element(f'{{{A}}}hlinkClick');h.set(f'{{{R}}}id',rid);h.set('action','ppaction://hlinksldjump');h.set('tooltip',f'Ir para o slide {target}');item.insert(0,h)
   links.append({'origem':n,'destino':target,'shape':item.get('name'),'id':rid})
  for old in root.findall(f'{{{P}}}transition'):root.remove(old)
  transition=E.Element(f'{{{P}}}transition',spd='fast',advClick='1');E.SubElement(transition,f'{{{P}}}fade')
  following=root.find(f'{{{P}}}timing')
  if following is None:following=root.find(f'{{{P}}}extLst')
  if following is None:root.append(transition)
  else:root.insert(root.index(following),transition)
  parts[member]=E.tostring(root,encoding='UTF-8',xml_declaration=True,standalone=True)
  parts[rels]=E.tostring(rr,encoding='UTF-8',xml_declaration=True,standalone=True)
 # O primeiro gráfico é a série mensal. Mostrar os anos a cada 24 meses.
 C='http://schemas.openxmlformats.org/drawingml/2006/chart'
 for name in sorted(parts):
  if re.fullmatch(r'ppt/(?:slides/)?charts/chart\d+\.xml',name):
   cr=E.fromstring(parts[name])
   if cr.find(f'.//{{{C}}}lineChart') is not None:
    for ax in cr.findall(f'.//{{{C}}}catAx'):
     for tag in ['tickLblSkip','tickMarkSkip']:
      if ax.find(f'{{{C}}}{tag}') is None:
       node=E.Element(f'{{{C}}}{tag}',val='24');ext=ax.find(f'{{{C}}}extLst')
       if ext is None:ax.append(node)
       else:ax.insert(ax.index(ext),node)
    parts[name]=E.tostring(cr,encoding='UTF-8',xml_declaration=True,standalone=True)
 # Rótulos arredondados a quatro casas para caber nos dois gráficos do slide 16.
 rr16=E.fromstring(parts['ppt/slides/_rels/slide16.xml.rels'])
 for rel in rr16:
  if rel.get('Type','').endswith('/chart'):
   target=rel.get('Target');name=target.lstrip('/') if target.startswith('/') else posixpath.normpath(posixpath.join('ppt/slides',target))
   cr=E.fromstring(parts[name])
   for labels in cr.findall(f'.//{{{C}}}dLbls'):
    num=labels.find(f'{{{C}}}numFmt')
    if num is not None:num.set('formatCode','0.0000')
   parts[name]=E.tostring(cr,encoding='UTF-8',xml_declaration=True,standalone=True)
 with ZipFile(B/'candidate.pptx','w',ZIP_DEFLATED) as dst:
  for name,value in parts.items():dst.writestr(name,value)
(B/'navegacao.json').write_text(json.dumps({'transicoes':23,'tipo':'Fade por clique, sem avanço automático','links':links},ensure_ascii=False,indent=2),encoding='utf-8')
print(f'23 transições Fade e {len(links)} atalhos internos')
