from pathlib import Path
from PIL import Image
import hashlib,json
p=Path(__file__).resolve().parent;old=p.parent/'devolutiva_orientador_20261101/png_final'
def key(file):
    im=Image.open(file).convert('RGB')
    return hashlib.sha256(im.crop((0,90,im.width,im.height)).tobytes()).hexdigest()
index={key(f):int(f.stem.split('-')[1]) for f in old.glob('page-*.png')}
files=sorted((p/'png_final').glob('page-*.png'),key=lambda f:int(f.stem.split('-')[1]))
checks=[{'pagina':int(f.stem.split('-')[1]),'pagina_base_com_corpo_pixel_identico':index.get(key(f))} for f in files]
changed=[c['pagina'] for c in checks if c['pagina_base_com_corpo_pixel_identico'] is None]
(p/'comparacao_visual.json').write_text(json.dumps({'paginas_total':len(files),'comparacao':'Pixels a96dpi, excluindo faixa superior90px com numeração','paginas_novas_ou_alteradas':changed,'paginas':checks},ensure_ascii=False,indent=2),encoding='utf-8')
(p/'pares').mkdir(exist_ok=True)
for i in range(0,len(files),2):
    a=Image.open(files[i]).convert('RGB');b=Image.open(files[i+1]).convert('RGB') if i+1<len(files) else None
    c=Image.new('RGB',(a.width*2,a.height),'#ddd');c.paste(a,(0,0))
    if b:c.paste(b,(a.width,0))
    c.save(p/'pares'/f'par-{i+1:02}.png')
print('Paginas a inspecionar:',changed)
