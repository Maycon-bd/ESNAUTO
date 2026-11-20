import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parent
QA=ROOT/'analise_v003'
SOURCE=ROOT/'exportados'/'ESNAUTO_apresentacao_25min_v002_audio_corrigido.mp4'
OUT=ROOT/'exportados'/'ESNAUTO_apresentacao_v003.mp4'
BIN=next((ROOT/'bin'/'ffmpeg-dist').glob('*/bin'))
cuts=json.loads((QA/'cortes_v002.json').read_text(encoding='utf-8'))
prep=json.loads((QA/'preparacao.json').read_text(encoding='utf-8'))
assert not prep['legendas_rapidas_para_exame']
assert not prep['palavras_em_cortes']
select='not('+'+'.join(f"gte(n,{c['inicio_frame']})*lt(n,{c['fim_frame_exclusivo']})" for c in cuts)+')'
vf=f"select='{select}',setpts=N/(30*TB),ass=analise_v003/orientacoes_final.ass"
af=f"aresample=48000,asetnsamples=n=1600:p=0,aselect='{select}',asetpts=N/SR/TB"
cmd=[str(BIN/'ffmpeg.exe'),'-hide_banner','-nostdin','-nostats','-n','-threads','4',
     '-i',str(SOURCE),'-i',str(ROOT/'exportados'/'ESNAUTO_apresentacao_v003.srt'),
     '-map','0:v:0','-map','0:a:0','-map','1:s:0','-vf',vf,'-af',af,
     '-c:v','h264_nvenc','-preset','p5','-tune','hq','-rc','vbr','-cq','18','-b:v','0',
     '-profile:v','high','-pix_fmt','yuv420p','-c:a','aac','-b:a','256k',
     '-c:s','mov_text','-metadata:s:s:0','language=por',
     '-metadata:s:s:0','title=Português - legendas revisadas','-disposition:s:0','0',
     '-map_metadata','-1','-metadata','title=ESNAUTO - Apresentação v003',
     '-movflags','+faststart','-progress',str(QA/'render_progresso.log'),str(OUT)]
with SOURCE.open('rb') as f:
    source_hash=hashlib.file_digest(f,'sha256').hexdigest()
assert source_hash=='6f24f9a4a1264375803f5aa97ace2b32afad4e6994fe4d913512bb79777fdcdc'
(QA/'render_comando.json').write_text(json.dumps({'comando':cmd,'sha256_base':source_hash,
    'audio':'A trilha aprovada da v002 é usada diretamente; somente cortes e nova codificação AAC.',
    'saida':str(OUT)},ensure_ascii=False,indent=2),encoding='utf-8')
if '--somente-verificar' not in sys.argv:
    with (QA/'render.log').open('w',encoding='utf-8') as log:
        subprocess.run(cmd,cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,check=True)
probe=json.loads(subprocess.check_output([str(BIN/'ffprobe.exe'),'-v','error',
    '-show_streams','-show_format','-of','json',str(OUT)],text=True))
video=next(s for s in probe['streams'] if s['codec_type']=='video')
audio=next(s for s in probe['streams'] if s['codec_type']=='audio')
sub=next(s for s in probe['streams'] if s['codec_type']=='subtitle')
assert int(video['nb_frames'])==prep['quadros_previstos']
assert float(probe['format']['duration'])<=1500
assert abs(float(probe['format']['duration'])-prep['duracao_prevista_s'])<.03
assert abs(float(video['duration'])-float(audio['duration']))<.05
assert sub['codec_name']=='mov_text' and sub['tags']['language']=='por'
assert sub['disposition']['forced']==0
with OUT.open('rb') as f:
    output_hash=hashlib.file_digest(f,'sha256').hexdigest()
with SOURCE.open('rb') as f:
    assert hashlib.file_digest(f,'sha256').hexdigest()==source_hash
result={'arquivo':str(OUT),'sha256':output_hash,'sha256_base_preservada':source_hash,
    'duracao_s':float(probe['format']['duration']),'quadros':int(video['nb_frames']),
    'diferenca_audio_video_s':abs(float(video['duration'])-float(audio['duration'])),
    'legenda_opcional_nao_forcada':True,
    'nota_legenda':'Faixa separada; ativação conforme o player. O muxer MP4 habilita a primeira faixa de cada tipo.',
    'probe':probe}
(QA/'verificacao_exportacao.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:result[k] for k in ['arquivo','duracao_s','quadros','diferenca_audio_video_s','sha256']},ensure_ascii=False,indent=2),flush=True)
