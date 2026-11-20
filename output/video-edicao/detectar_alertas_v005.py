"""Busca local de alertas por comparação com os arquivos de som do Windows."""
import hashlib
import json
from pathlib import Path
import subprocess
import numpy as np
from scipy import signal

ROOT=Path(__file__).resolve().parent
QA=ROOT/'analise_v005'
BIN=next((ROOT/'bin'/'ffmpeg-dist').glob('*/bin'))
RATE=8000
x=np.memmap(QA/'audio_8k_stereo.f32',dtype=np.float32,mode='r').reshape(-1,2).mean(axis=1)
sos=signal.butter(4,[320,3400],btype='bandpass',fs=RATE,output='sos')
x=signal.sosfiltfilt(sos,x).astype(np.float32)
prefix=np.r_[0,np.cumsum(x.astype(np.float64)**2)]
cache=QA/'referencias'
cache.mkdir(exist_ok=True)
templates=[]
all_candidates=[]
seen={}
for path in sorted(Path('C:/Windows/Media').glob('*.wav')):
    digest=hashlib.sha256(path.read_bytes()).hexdigest()
    if digest in seen:
        continue
    seen[digest]=path.name
    pcm=subprocess.check_output([str(BIN/'ffmpeg.exe'),'-v','error','-i',str(path),
        '-ac','1','-ar',str(RATE),'-f','f32le','pipe:1'])
    raw=np.frombuffer(pcm,np.float32).copy()
    ref=signal.sosfiltfilt(sos,raw).astype(np.float32)
    active=np.flatnonzero(np.abs(ref)>np.max(np.abs(ref))*.002)
    if not len(active): continue
    start=max(0,int(active[0])-80)
    end=min(len(ref),int(active[-1])+81)
    ref=ref[start:end]
    raw=raw[start:end]
    np.save(cache/(path.stem+'.npy'),raw)
    energy=float(np.dot(ref,ref))
    cross=signal.oaconvolve(x,ref[::-1],mode='valid')
    window=prefix[len(ref):]-prefix[:-len(ref)]
    ncc=cross/np.sqrt(np.maximum(window*energy,1e-18))
    # Silêncio digital amplifica o erro numérico do FFT na normalização.
    # Excluir janelas abaixo de -60 dBFS e resultados não físicos.
    ncc[(window<len(ref)*1e-6) | (np.abs(ncc)>1.0001)]=0
    peaks,properties=signal.find_peaks(np.abs(ncc),height=.22,
        distance=max(int(RATE*.18),int(len(ref)*.7)))
    best=np.argsort(properties['peak_heights'])[::-1][:80]
    candidates=[]
    for j in best:
        pos=int(peaks[j])
        candidates.append({'som':path.name,'inicio_s':pos/RATE,'fim_s':(pos+len(ref))/RATE,
            'correlacao':float(ncc[pos]),'amostra_inicio':pos,'amostras_ref':len(ref),
            'referencia_npy':str(cache/(path.stem+'.npy'))})
    templates.append({'som':path.name,'duracao_ref_s':len(ref)/RATE,
        'correlacao_maxima':float(np.max(np.abs(ncc))), 'candidatos':len(candidates)})
    all_candidates.extend(candidates)
    print(f'{path.name}: pico {np.max(np.abs(ncc)):.3f}; {len(candidates)} candidatos',flush=True)
    (QA/'deteccao_parcial.json').write_text(json.dumps({'referencias':templates,'candidatos':all_candidates},
        ensure_ascii=False,indent=2),encoding='utf-8')
all_candidates.sort(key=lambda item:abs(item['correlacao']),reverse=True)
result={'taxa_amostragem':RATE,'banda_busca_hz':[320,3400],
    'referencias':sorted(templates,key=lambda d:d['correlacao_maxima'],reverse=True),
    'candidatos':all_candidates}
(QA/'deteccao.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print('Busca concluída.',flush=True)
