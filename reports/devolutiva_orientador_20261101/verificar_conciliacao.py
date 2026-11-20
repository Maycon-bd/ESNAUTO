from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
from collections import Counter
from PIL import Image,ImageChops
import pypdfium2 as pdf
import json,re,hashlib
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
BASE=ROOT/'reports/monografia/versoes/v008/MayconGarciaSilva_monografia_v008.docx'
DOC=ROOT/'reports/monografia/trabalho/devolutiva_orientador_20261101.docx'
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
def txt(p):return ''.join(p.xpath('.//w:t/text()',namespaces=ns))
def interval(r):
 ps=r.xpath('//w:body/w:p',namespaces=ns);start=next(i for i,p in enumerate(ps) if txt(p)=='INTRODUÇÃO');end=next(i for i,p in enumerate(ps) if txt(p)=='REVISÃO DA LITERATURA');return ps,start,end
with ZipFile(BASE) as a,ZipFile(DOC) as z:
 assert z.testzip() is None
 assert set(a.namelist())==set(z.namelist())
 changed=[n for n in a.namelist() if a.read(n)!=z.read(n)];assert changed==['word/document.xml']
 ra=E.fromstring(a.read('word/document.xml'));r=E.fromstring(z.read('word/document.xml'))
 pa,sa,ea=interval(ra);p,s,e=interval(r)
 assert [E.tostring(x) for x in pa[ea:]]==[E.tostring(x) for x in p[e:]]
 assert len(p[s+1:e])==15
 assert all(x.find('w:pPr/w:pStyle',ns) is None or x.find('w:pPr/w:pStyle',ns).get('{'+ns['w']+'}val') not in ['TITULOTCC','SEOTCC','SUBO2'] for x in p[s+1:e])
 assert len(r.xpath('//w:color[@w:val="FF0000"]',namespaces=ns))==0
 tables=r.xpath('//w:tbl',namespaces=ns);assert len(tables)==14
 assert [E.tostring(t) for t in tables]==[E.tostring(t) for t in ra.xpath('//w:tbl',namespaces=ns)]
 q=''.join(r.xpath('//w:t/text()',namespaces=ns)).count('?');assert q==52
 assert ''.join(r.xpath('//w:t/text()',namespaces=ns)).count('\ufffd')==0
 first=next(i for i,x in enumerate(p[s+1:e]) if 'ESN' in txt(x));assert 'Echo State Network – ESN)' in txt(p[s+1+first])
 for old in ['Busca por AG por cenário ESN','A Tabela 5 apresenta a decomposição do custo computacional.','Nos quatro testes apresentados na Tabela 6']:
  assert old in ''.join(r.xpath('//w:t/text()',namespaces=ns))
 figures=[{'part':n,'sha256':hashlib.sha256(z.read(n)).hexdigest()} for n in z.namelist() if n.startswith('word/media/')];assert len(figures)==6
 references=[txt(x) for x in p if (x.find('w:pPr/w:pStyle',ns) is not None and x.find('w:pPr/w:pStyle',ns).get('{'+ns['w']+'}val')=='Referencias')];assert len(references)==50
j=json.loads((OUT/'paginacao_candidata.json').read_text(encoding='utf-8-sig'));t=j['titles']
assert len(t)==41
for chapter,count in [(2,9),(3,8),(4,10),(5,3)]:
 assert [x['number'] for x in t if re.fullmatch(f'{chapter}\\.\\d+',x['number'])]==[f'{chapter}.{i}' for i in range(1,count+1)]
assert [x['number'] for x in t if x['style']=='TITULO TCC']==['1','2','3','4','5','6','']
assert [x['number'] for x in t if x['style']=='SUBÇÃO 2']==['3.8.1','3.8.2','3.8.3','3.8.4']
u=json.loads((OUT/'paginas_listas_atualizadas.json').read_text(encoding='utf-8'));assert len(u['conferidas'])==60 and len(u['alteradas'])==59
# Conferência do texto das páginas do desenvolvimento após a nova introdução.
a=pdf.PdfDocument(OUT/'base_v008.pdf');b=pdf.PdfDocument(OUT/'candidata.pdf');assert len(a)==76 and len(b)==77
def bodytext(page):
 lines=page.get_textpage().get_text_range().splitlines()
 if lines and lines[0].strip().isdigit():lines=lines[1:]
 return '\n'.join(lines)
pagechecks=[]
for new_i in range(20,77):
 old_i=new_i-1
 ta,tb=bodytext(a[old_i]),bodytext(b[new_i]);same=ta==tb
 assert same,(new_i+1,'texto divergente fora da introdução')
 ia=a[old_i].render(scale=1.2).to_pil().convert('RGB');ib=b[new_i].render(scale=1.2).to_pil().convert('RGB')
 # A única diferença esperada nessas páginas é o número no cabeçalho.
 crop=(0,110,ia.width,ia.height)
 pixel_same=ImageChops.difference(ia.crop(crop),ib.crop(crop)).getbbox() is None
 pagechecks.append({'pagina_nova':new_i+1,'pagina_base':old_i+1,'texto_corpo_identico':same,'pixels_corpo_identicos':pixel_same})
qa={'base':'v008','sha256_base':hashlib.sha256(BASE.read_bytes()).hexdigest(),'sha256_candidata':hashlib.sha256(DOC.read_bytes()).hexdigest(),'partes_alteradas':changed,'paginas':77,'introducao_paginas_fisicas':[18,19,20],'titulos':41,'sumario_e_listas_conferidos':60,'paginas_corrigidas':59,'tabelas_preservadas':14,'referencias_preservadas':50,'figuras_preservadas':figures,'interrogacoes_com_significado':52,'comparacao_paginas_desenvolvimento':pagechecks}
(OUT/'verificacao_final.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf-8')
pngs=sorted((OUT/'png_final').glob('page-*.png'),key=lambda x:int(x.stem.split('-')[-1]));assert len(pngs)==77
pairs=OUT/'pares';pairs.mkdir(exist_ok=True)
for i in range(0,len(pngs),2):
 im1=Image.open(pngs[i]).convert('RGB');im2=Image.open(pngs[i+1]).convert('RGB') if i+1<len(pngs) else None
 canvas=Image.new('RGB',(im1.width*2,im1.height),'#dddddd');canvas.paste(im1,(0,0))
 if im2:canvas.paste(im2,(im1.width,0))
 canvas.save(pairs/f'par-{i+1:02d}.png')
print('Conferências estruturais concluídas. Corpo do desenvolvimento preservado nas 57 páginas seguintes à introdução.')
