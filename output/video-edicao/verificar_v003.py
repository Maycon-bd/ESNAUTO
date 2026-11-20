import json
from pathlib import Path
import re
import subprocess
import numpy as np

ROOT=Path(__file__).resolve().parent
QA=ROOT/'analise_v003'
BIN=next((ROOT/'bin'/'ffmpeg-dist').glob('*/bin'))
OUT=ROOT/'exportados'/'ESNAUTO_apresentacao_v003.mp4'
SOURCE=ROOT/'exportados'/'ESNAUTO_apresentacao_25min_v002_audio_corrigido.mp4'
cuts=json.loads((QA/'cortes_v002.json').read_text(encoding='utf-8'))
captions=json.loads((QA/'legendas_alinhadas.json').read_text(encoding='utf-8'))
cues=json.loads((QA/'orientacoes_final.json').read_text(encoding='utf-8'))

def remap(t):
    return t-sum(max(0,min(t,c['fim_frame_exclusivo']/30)-c['inicio_frame']/30) for c in cuts)

def run(args,log=None):
    cmd=[str(BIN/'ffmpeg.exe'),'-hide_banner','-nostdin',*args]
    if log:
        with (QA/log).open('w',encoding='utf-8') as f:
            subprocess.run(cmd,cwd=ROOT,stdout=f,stderr=subprocess.STDOUT,check=True)
    else:
        return subprocess.check_output(cmd,cwd=ROOT,stderr=subprocess.DEVNULL)

run(['-nostats','-threads','4','-filter_threads','2','-i',str(OUT),'-map','0:v:0','-map','0:a:0',
     '-af','ebur128=peak=true:framelog=verbose','-f','null','NUL'],'decodificacao_audio_final.log')
print('Decodificação integral concluída.',flush=True)
run(['-v','error','-n','-i',str(OUT),'-map','0:s:0',str(QA/'legendas_extraidas.srt')])
def read_srt(path):
    blocks=re.split(r'\r?\n\s*\r?\n',path.read_text(encoding='utf-8-sig').strip())
    return [' '.join(block.splitlines()[2:]) for block in blocks]
assert read_srt(QA/'legendas_extraidas.srt')==read_srt(ROOT/'exportados'/'ESNAUTO_apresentacao_v003.srt')
for i,c in enumerate(captions):
    assert 0<=c['start']<c['end']<=1476
    assert len(c['text'].splitlines())<=2
    assert all(len(line)<=42 for line in c['text'].splitlines())
    assert len(c['text'].replace('\n',' '))/(c['end']-c['start'])<=25
    if i+1<len(captions): assert c['end']<captions[i+1]['start']

samples=[]
for t in [660,700,760]:
    def pcm(path,start):
        return np.frombuffer(run(['-v','error','-ss',str(start),'-i',str(path),'-t','4',
            '-vn','-ac','1','-ar','16000','-f','f32le','pipe:1']),np.float32)
    a,b=pcm(SOURCE,t),pcm(OUT,remap(t))
    count=min(len(a),len(b))
    a,b=a[:count],b[:count]
    a,b=a-a.mean(),b-b.mean()
    n=1<<((len(a)+len(b)-1).bit_length())
    corr=np.fft.irfft(np.fft.rfft(b,n)*np.conj(np.fft.rfft(a,n)),n)
    lags=np.arange(-16,17)
    lag=int(lags[np.argmax(corr[lags%n])])
    if lag>0: x,y=a[:-lag],b[lag:]
    elif lag<0: x,y=a[-lag:],b[:lag]
    else: x,y=a,b
    correlation=float(np.corrcoef(x,y)[0,1])
    assert abs(lag)<=16 and correlation>.98, (t,lag,correlation)
    samples.append({'tempo_base_s':t,'tempo_final_s':remap(t),'atraso_ms':lag/16,
                    'correlacao_com_audio_aprovado':correlation})

for i,cue in enumerate(cues):
    t=(cue['start_final']+cue['end_final'])/2
    run(['-v','error','-n','-threads','2','-ss',str(t),'-i',str(OUT),'-frames:v','1','-threads','1',str(QA/f'qa_orientacao_{i+1}.png')])

# Versão ASS apenas para visualizar a diagramação das legendas na conferência.
def ts(t):
    cs=round(t*100)
    return f'{cs//360000}:{cs//6000%60:02d}:{cs//100%60:02d}.{cs%100:02d}'
ass=['[Script Info]','ScriptType: v4.00+','PlayResX: 1920','PlayResY: 1080','',
     '[V4+ Styles]',
     'Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding',
     'Style: Default,Segoe UI,40,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,2,0,2,160,160,55,1','',
     '[Events]','Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text']
for c in captions:
    text=c['text'].replace('\n','\\N')
    ass.append(f"Dialogue: 0,{ts(c['start'])},{ts(c['end'])},Default,,0,0,0,,{text}")
(QA/'legendas_qa.ass').write_text('\n'.join(ass)+'\n',encoding='utf-8-sig')
for t in [20,968,1062,1400]:
    run(['-v','error','-n','-threads','2','-ss',str(t),'-i',str(OUT),
         '-vf',f'setpts=PTS+{t}/TB,ass=analise_v003/legendas_qa.ass',
         '-frames:v','1','-threads','1',str(QA/f'qa_legenda_{t}.png')])
result={'decodificacao_integral':'sucesso','legendas_embutidas_iguais_ao_srt':True,
    'legendas_conferidas':len(captions),'maximo_linhas':2,'maximo_caracteres_por_linha':42,
    'limite_cps':25,'sobreposicoes_de_tempo':0,'audio_aprovado_comparacoes':samples,
    'orientacoes_para_inspecao_visual':len(cues),'legendas_para_inspecao_visual':4}
(QA/'conferencia_final.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2),flush=True)
