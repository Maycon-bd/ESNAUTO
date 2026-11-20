import hashlib
import json
from pathlib import Path
import shutil
import subprocess

ROOT=Path(__file__).resolve().parent
QA=ROOT/'analise_v005'
BIN=next((ROOT/'bin'/'ffmpeg-dist').glob('*/bin'))
SOURCE=ROOT/'exportados'/'ESNAUTO_apresentacao_v004.mp4'
OUTPUT=ROOT/'exportados'/'ESNAUTO_apresentacao_v005.mp4'
validation=json.loads((QA/'verificacao_cancelamento.json').read_text(encoding='utf-8'))
assert not validation['ocorrencias_confirmadas_depois']
with SOURCE.open('rb') as f:
    source_hash=hashlib.file_digest(f,'sha256').hexdigest()
assert source_hash=='0ca62f952fdde7d3c8fb76e9aebcd576110b54d348825cb7ef002c7950bbcce5'
cmd=[str(BIN/'ffmpeg.exe'),'-hide_banner','-nostdin','-nostats','-n','-i',str(SOURCE),
     '-f','f32le','-ar','48000','-ac','2','-i',str(QA/'audio_sem_notificacoes.f32'),
     '-map','0:v:0','-map','1:a:0','-map','0:s:0','-c:v','copy','-c:a','aac','-b:a','256k',
     '-c:s','copy','-map_metadata','0','-metadata','title=ESNAUTO - Apresentação v005',
     '-movflags','+faststart','-progress',str(QA/'exportacao_progresso.log'),str(OUTPUT)]
with (QA/'exportacao.log').open('w',encoding='utf-8') as log:
    subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,check=True)
probe=json.loads(subprocess.check_output([str(BIN/'ffprobe.exe'),'-v','error','-show_streams','-show_format','-of','json',str(OUTPUT)],text=True))
v=next(s for s in probe['streams'] if s['codec_type']=='video')
a=next(s for s in probe['streams'] if s['codec_type']=='audio')
assert int(v['nb_frames'])==44280
assert abs(float(probe['format']['duration'])-1476)<.03
assert abs(float(v['duration'])-float(a['duration']))<.05
track_hashes={}
for kind in ['v','s']:
    h=[]
    for path in [SOURCE,OUTPUT]:
        h.append(subprocess.check_output([str(BIN/'ffmpeg.exe'),'-v','error','-i',str(path),
            '-map',f'0:{kind}:0','-c','copy','-f','hash','-hash','sha256','-'],text=True).strip())
    assert h[0]==h[1]
    track_hashes[kind]=h[0]
corrections=json.loads((QA/'correcoes_audio.json').read_text(encoding='utf-8'))
intervals=[(c['inicio_amostra_48k']*8,(c['inicio_amostra_48k']+c['amostras_corrigidas'])*8) for c in corrections]
total=(QA/'audio_48k_stereo.f32').stat().st_size
outside=[]
position=0
for start,end in intervals+[(total,total)]:
    hashes=[]
    for path in [QA/'audio_48k_stereo.f32',QA/'audio_sem_notificacoes.f32']:
        h=hashlib.sha256()
        with path.open('rb') as f:
            f.seek(position)
            remaining=start-position
            while remaining:
                block=f.read(min(remaining,8*48000*30))
                assert block
                h.update(block)
                remaining-=len(block)
        hashes.append(h.hexdigest())
    assert hashes[0]==hashes[1]
    outside.append({'inicio_byte':position,'fim_byte':start,'sha256_pcm':hashes[0]})
    position=end
shutil.copyfile(ROOT/'exportados'/'ESNAUTO_apresentacao_v004.srt',ROOT/'exportados'/'ESNAUTO_apresentacao_v005.srt')
with SOURCE.open('rb') as f:
    assert hashlib.file_digest(f,'sha256').hexdigest()==source_hash
with OUTPUT.open('rb') as f:
    output_hash=hashlib.file_digest(f,'sha256').hexdigest()
result={'saida':str(OUTPUT),'sha256_saida':output_hash,'base_preservada_sha256':source_hash,
    'duracao_s':float(probe['format']['duration']),'quadros':int(v['nb_frames']),
    'diferenca_audio_video_s':abs(float(v['duration'])-float(a['duration'])),
    'video_e_legendas_identicos_por_hash':track_hashes,
    'pcm_inalterado_fora_das_correcoes':outside,
    'ocorrencias_tratadas':len(corrections),'probe':probe,'comando':cmd}
(QA/'verificacao_exportacao.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:result[k] for k in ['saida','duracao_s','ocorrencias_tratadas','sha256_saida']},ensure_ascii=False,indent=2),flush=True)
