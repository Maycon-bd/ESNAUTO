import json,hashlib,zipfile,re
from pathlib import Path
from lxml import etree as E
from PIL import Image,ImageChops,ImageDraw
BUILD=Path(__file__).resolve().parent; ROOT=BUILD.parents[2]
old=ROOT/'reports/apresentacao_banca_v008_visual'
final=BUILD.parent/'entrega/Apresentacao_ESNAUTO_banca_visual_v010.pptx'
with zipfile.ZipFile(old/'entrega/Apresentacao_ESNAUTO_banca_visual.pptx') as a,zipfile.ZipFile(final) as b:
    differences=[n for n in a.namelist() if a.read(n)!=b.read(n)]
    allowed=json.loads((BUILD/'rastreabilidade.json').read_text(encoding='utf-8'))['partes_pptx_alteradas']
    assert set(differences)==set(allowed)
    ns={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
    for i in range(1,24):
        x=E.fromstring(a.read(f'ppt/slides/slide{i}.xml'));y=E.fromstring(b.read(f'ppt/slides/slide{i}.xml'))
        for tag in ['p:transition','a:hlinkClick']:
            assert [E.tostring(v) for v in x.findall('.//'+tag,ns)]==[E.tostring(v) for v in y.findall('.//'+tag,ns)]
rows=[]
for i in range(1,24):
    a=Image.open(old/f'build/powerpoint_render/Slide{i}.PNG').convert('RGB')
    b=Image.open(BUILD/f'powerpoint_render/Slide{i}.PNG').convert('RGB')
    box=ImageChops.difference(a,b).getbbox()
    rows.append({'slide':i,'bbox_alteracao':box,'conteudo_acima_rodape_identico':ImageChops.difference(a.crop((0,0,1280,675)),b.crop((0,0,1280,675))).getbbox() is None})
for offset in range(0,23,6):
    sheet=Image.new('RGB',(1280,3*390),'#dddddd');draw=ImageDraw.Draw(sheet)
    for j,i in enumerate(range(offset+1,min(offset+7,24))):
        im=Image.open(BUILD/f'powerpoint_render/Slide{i}.PNG').convert('RGB');im.thumbnail((640,360))
        x=(j%2)*640;y=(j//2)*390
        sheet.paste(im,(x,y+25));draw.text((x+8,y+5),f'Slide {i}',fill='black')
    sheet.save(BUILD/f'contato-{offset//6+1}.png')
native=json.loads((BUILD/'verificacao_nativa.json').read_text(encoding='utf-8-sig'))
assert native['slideCount']==23 and len(native['links'])==82
assert all(t['onClick']==-1 and t['onTime']==0 for t in native['effects'])
out={'partes_alteradas':differences,'comparacao_visual':rows,'links_nativos':82,'transicoes':23,
     'sha256_final':hashlib.sha256(final.read_bytes()).hexdigest()}
(BUILD/'conferencia_final.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(rows))
