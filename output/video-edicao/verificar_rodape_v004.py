import json
from pathlib import Path
import subprocess
import numpy as np

ROOT=Path(__file__).resolve().parent
QA=ROOT/'analise_v004'
BIN=next((ROOT/'bin'/'ffmpeg-dist').glob('*/bin'))
VIDEO=ROOT/'exportados'/'ESNAUTO_apresentacao_v004.mp4'
with (QA/'decodificacao.log').open('w',encoding='utf-8') as log:
    subprocess.run([str(BIN/'ffmpeg.exe'),'-hide_banner','-nostdin','-nostats','-n',
        '-threads','4','-i',str(VIDEO),'-an','-sn',
        '-vf','fps=1,crop=1100:40:100:1028,scale=110:4,format=rgb24',
        '-f','rawvideo',str(QA/'rodapes_amostrados.rgb')],stdout=log,stderr=subprocess.STDOUT,check=True)
raw=np.frombuffer((QA/'rodapes_amostrados.rgb').read_bytes(),np.uint8).reshape(-1,440,3)
deviation=raw.std(axis=1).max(axis=1)
slide_indices=[i for i in range(len(raw)) if i<619 or i>708]
demo_indices=list(range(623,704))
assert len(raw)==1476
assert max(deviation[slide_indices])<1.5
assert min(deviation[demo_indices])>5
for t in [110,630,680,1000,1450]:
    subprocess.run([str(BIN/'ffmpeg.exe'),'-v','error','-nostdin','-n','-threads','2',
        '-ss',str(t),'-i',str(VIDEO),'-frames:v','1','-threads','1',str(QA/f'depois_{t}.png')],check=True)
result={'decodificacao_video_integral':'sucesso','amostras_rodape':len(raw),
    'quadros_amostrados_com_pintura':len(slide_indices),
    'maximo_desvio_pixel_por_canal_nos_slides':float(max(deviation[slide_indices])),
    'minimo_desvio_pixel_por_canal_na_demonstracao':float(min(deviation[demo_indices])),
    'quadros_para_conferencia_visual':[110,630,680,1000,1450]}
(QA/'conferencia_pintura.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2),flush=True)
