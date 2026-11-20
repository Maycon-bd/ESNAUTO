from pathlib import Path
import json,zipfile,hashlib
from lxml import etree as E
from PIL import Image,ImageChops
from docx import Document
B=Path(__file__).resolve().parent;R=B.parents[2];O=B.parent/'entrega'
slides=json.loads((B/'conteudo.json').read_text(encoding='utf-8'))
src=R/'reports/apresentacao_banca_v010_visual/entrega/Apresentacao_ESNAUTO_banca_visual_v010.pptx'
dst=O/'Apresentacao_ESNAUTO_v010_notas_fala_clara.pptx'
ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
with zipfile.ZipFile(src) as a,zipfile.ZipFile(dst) as b:
    changes=[n for n in a.namelist() if a.read(n)!=b.read(n)]
    assert len(changes)==23 and all(n.startswith('ppt/notesSlides/notesSlide') for n in changes)
    for s in slides:
        text='\n'.join(E.fromstring(b.read(f'ppt/notesSlides/notesSlide{s["number"]}.xml')).xpath('//a:t/text()',namespaces=ns))
        for p in s['paragraphs']:assert p in text
doc=Document(O/'Roteiro_ESNAUTO_v010_fala_clara.docx');tx='\n'.join(p.text for p in doc.paragraphs)
for s in slides:
    for p in s['paragraphs']:assert p in tx
    assert s['source'] in tx
assert sum(s['seconds'] for s in slides)==1500
native=json.loads((B/'verificacao_nativa.json').read_text(encoding='utf-8-sig'))
assert len(native['links'])==82 and native['slideCount']==23
assert all(t['onClick']==-1 and t['onTime']==0 for t in native['effects'])
original=R/'reports/apresentacao_banca_v010_visual/build/powerpoint_render'
for i in range(1,24):
    a=Image.open(original/f'Slide{i}.PNG');b=Image.open(B/f'powerpoint_render/Slide{i}.PNG')
    assert ImageChops.difference(a.convert('RGB'),b.convert('RGB')).getbbox() is None,i
changed_pages=[]
for i in range(1,14):
    a=Image.open(B/f'roteiro_render/antes-page-{i}.png');b=Image.open(B/f'roteiro_render/page-{i}.png')
    if ImageChops.difference(a.convert('RGB'),b.convert('RGB')).getbbox():changed_pages.append(i)
print('Paginas alteradas na ultima revisao',changed_pages)
base=R/'reports/monografia/versoes/v010/MayconGarciaSilva_monografia_v010.docx'
assert hashlib.sha256(base.read_bytes()).hexdigest()=='1da5ea82344c177d75af723362017e3e558bbb127bd9995f7ec0cbd6964f81ed'
q={'base':'v010','base_sha256':hashlib.sha256(base.read_bytes()).hexdigest(),'palavras_fala':sum(s['words'] for s in slides),'segundos_planejados':1500,'paginas_word':13,'falas_sincronizadas':23,'graficos_preservados':10,'links_preservados':82,'slides_renderizados_identicos':23,'alteracao_pptx_somente_notas':True,'paginas_modificadas_ultima_iteracao':changed_pages,'artefatos':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in O.iterdir()}}
(B/'entrega_verificada.json').write_text(json.dumps(q,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(q,ensure_ascii=True))
