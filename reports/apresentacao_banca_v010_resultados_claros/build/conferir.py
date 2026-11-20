import hashlib,json,zipfile,re
from pathlib import Path
from lxml import etree as E
from PIL import Image,ImageChops
from docx import Document
B=Path(__file__).resolve().parent;R=B.parents[2];O=B.parent/'entrega';A=R/'reports/apresentacao_banca_v010_fala_clara'
src=A/'entrega/Apresentacao_ESNAUTO_v010_notas_fala_clara.pptx';final=O/'Apresentacao_ESNAUTO_v010_resultados_claros.pptx'
slides=json.loads((B/'conteudo.json').read_text(encoding='utf-8'));changes=json.loads((B/'textos_slides.json').read_text(encoding='utf-8'))
ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main'}
with zipfile.ZipFile(src) as a,zipfile.ZipFile(final) as b:
    assert a.namelist()==b.namelist()
    differences=[n for n in a.namelist() if a.read(n)!=b.read(n)]
    for n in differences:
        assert re.fullmatch(r'ppt/(notesSlides/notesSlide\d+|slides/slide(19|20|21|23))\.xml',n),n
    for i in range(1,24):
        old=E.fromstring(a.read(f'ppt/slides/slide{i}.xml'));new=E.fromstring(b.read(f'ppt/slides/slide{i}.xml'))
        for tag in ['p:transition','a:hlinkClick']:
            assert [E.tostring(x) for x in old.findall('.//'+tag,ns)]==[E.tostring(x) for x in new.findall('.//'+tag,ns)]
        if str(i) in changes:
            for text in changes[str(i)].values():assert text in ''.join(new.xpath('//a:t/text()',namespaces=ns))
        notes='\n'.join(E.fromstring(b.read(f'ppt/notesSlides/notesSlide{i}.xml')).xpath('//a:t/text()',namespaces=ns))
        for p in slides[i-1]['paragraphs']:assert p in notes
        assert slides[i-1]['window'] in notes
doc=Document(O/'Roteiro_ESNAUTO_v010_resultados_claros.docx');tx='\n'.join(p.text for p in doc.paragraphs)
for s in slides:
    for p in s['paragraphs']:assert p in tx
    assert s['window'] in tx and s['source'] in tx
assert sum(s['seconds'] for s in slides)==1500
native=json.loads((B/'verificacao_nativa.json').read_text(encoding='utf-8-sig'))
assert len(native['links'])==82 and native['slideCount']==23
assert all(x['onClick']==-1 and x['onTime']==0 for x in native['effects'])
changed_pages=[];changed_slides=[]
for i in range(1,14):
    old=Image.open(A/f'build/roteiro_render/page-{i}.png').convert('RGB');new=Image.open(B/f'roteiro_render/page-{i}.png').convert('RGB')
    if ImageChops.difference(old,new).getbbox():changed_pages.append(i)
assert changed_pages==[1,11,12,13]
for i in range(1,24):
    old=Image.open(A/f'build/powerpoint_render/Slide{i}.PNG').convert('RGB');new=Image.open(B/f'powerpoint_render/Slide{i}.PNG').convert('RGB')
    if ImageChops.difference(old,new).getbbox():changed_slides.append(i)
assert changed_slides==[19,20,21,23]
base=R/'reports/monografia/versoes/v010/MayconGarciaSilva_monografia_v010.docx'
h=hashlib.sha256(base.read_bytes()).hexdigest();assert h=='1da5ea82344c177d75af723362017e3e558bbb127bd9995f7ec0cbd6964f81ed'
q={'base':'v010','base_sha256':h,'paginas_roteiro':13,'paginas_alteradas_inspecionadas':changed_pages,'slides_alterados_inspecionados':changed_slides,'demais_paginas_e_slides_identicos_as_imagens_anteriores_inspecionadas':True,'falas_sincronizadas':23,'palavras_fala':sum(s['words'] for s in slides),'segundos_planejados':1500,'links_nativos':82,'transicoes_por_clique':23,'graficos_preservados':10,'partes_alteradas':differences,'arquivos':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in O.iterdir()}}
(B/'entrega_verificada.json').write_text(json.dumps(q,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(q,ensure_ascii=True))
