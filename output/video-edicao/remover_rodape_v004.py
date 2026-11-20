"""Cobre o rodapé de fonte com uma amostra do próprio fundo do slide."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

ROOT=Path(__file__).resolve().parent
QA=ROOT/'analise_v004'
BIN=next((ROOT/'bin'/'ffmpeg-dist').glob('*/bin'))
SOURCE=ROOT/'exportados'/'ESNAUTO_apresentacao_v003.mp4'
OUTPUT=ROOT/'exportados'/'ESNAUTO_apresentacao_v004.mp4'
# Chrome ocupa os quadros [18623,21202). As fronteiras abaixo ficam entre
# quadros para evitar ambiguidades de arredondamento na expressão temporal.
FILTER=("[0:v]split=2[base][amostra];"
        "[amostra]crop=2:2:80:1044,scale=1100:40:flags=neighbor,setsar=1[pintura];"
        "[base][pintura]overlay=x=100:y=1028:enable='lt(t,620.75)+gt(t,706.716666667)'[limpo]")
with SOURCE.open('rb') as f:
    source_hash=hashlib.file_digest(f,'sha256').hexdigest()
assert source_hash=='00edeefb946731f933b15616c4ef911477f38dedb4483617b5b3b47765dd63c2'
cmd=[str(BIN/'ffmpeg.exe'),'-hide_banner','-nostdin','-nostats','-n','-threads','4',
     '-i',str(SOURCE),'-filter_complex',FILTER,'-map','[limpo]','-map','0:a:0','-map','0:s:0',
     '-c:v','h264_nvenc','-preset','p5','-tune','hq','-rc','vbr','-cq','16','-b:v','0',
     '-profile:v','high','-pix_fmt','yuv420p','-c:a','copy','-c:s','copy','-map_metadata','0',
     '-metadata','title=ESNAUTO - Apresentação v004','-movflags','+faststart',
     '-progress',str(QA/'progresso.log'),str(OUTPUT)]
(QA/'plano.json').write_text(json.dumps({'base':str(SOURCE),'sha256_base':source_hash,
    'retangulo':[100,1028,1100,40],'amostra_do_fundo':[80,1044,2,2],
    'demonstracao_excluida_quadros':[18623,21202], 'filtro':FILTER,'comando':cmd},ensure_ascii=False,indent=2),encoding='utf-8')
with (QA/'render.log').open('w',encoding='utf-8') as log:
    subprocess.run(cmd,cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,check=True)
probe=json.loads(subprocess.check_output([str(BIN/'ffprobe.exe'),'-v','error','-show_streams','-show_format','-of','json',str(OUTPUT)],text=True))
video=next(s for s in probe['streams'] if s['codec_type']=='video')
assert int(video['nb_frames'])==44280
assert abs(float(probe['format']['duration'])-1476)<.03
hashes={}
for kind in ['a','s']:
    values=[]
    for path in [SOURCE,OUTPUT]:
        values.append(subprocess.check_output([str(BIN/'ffmpeg.exe'),'-v','error','-i',str(path),
            '-map',f'0:{kind}:0','-c','copy','-f','hash','-hash','sha256','-'],text=True).strip())
    assert values[0]==values[1], f'Trilha {kind} alterada.'
    hashes[kind]=values[0]
shutil.copyfile(ROOT/'exportados'/'ESNAUTO_apresentacao_v003.srt',ROOT/'exportados'/'ESNAUTO_apresentacao_v004.srt')
with SOURCE.open('rb') as f:
    assert hashlib.file_digest(f,'sha256').hexdigest()==source_hash
with OUTPUT.open('rb') as f:
    output_hash=hashlib.file_digest(f,'sha256').hexdigest()
result={'saida':str(OUTPUT),'sha256_saida':output_hash,'base_preservada_sha256':source_hash,
        'duracao_s':float(probe['format']['duration']),'quadros':int(video['nb_frames']),
        'trilhas_identicas_por_hash':hashes,'probe':probe}
(QA/'verificacao.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:result[k] for k in ['saida','duracao_s','quadros','sha256_saida','trilhas_identicas_por_hash']},ensure_ascii=False,indent=2),flush=True)
