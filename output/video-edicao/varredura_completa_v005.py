"""Confere famílias de sons do Windows usando a banda completa das notas."""
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
sos=signal.butter(4,[70,3400],btype='bandpass',fs=RATE,output='sos')
x=np.fromfile(QA/'audio_8k_stereo.f32',np.float32).reshape(-1,2).mean(1)
x=signal.sosfiltfilt(sos,x)
energy_prefix=np.r_[0,np.cumsum(x*x)]
seen=set()
results=[]
confirmed=[]
for path in sorted(Path('C:/Windows/Media').glob('*.wav')):
    digest=hashlib.sha256(path.read_bytes()).hexdigest()
    if digest in seen: continue
    seen.add(digest)
    pcm=subprocess.check_output([str(BIN/'ffmpeg.exe'),'-v','error','-i',str(path),
        '-ac','1','-ar',str(RATE),'-f','f32le','pipe:1'])
    r=signal.sosfiltfilt(sos,np.frombuffer(pcm,np.float32))
    q=np.searchsorted(np.cumsum(r*r),np.dot(r,r)*np.array([0,.25,.5,.75,.999]))
    prefix=r[:q[3]]
    if len(prefix)<32: continue
    dot=signal.oaconvolve(x,prefix[::-1],mode='valid')
    window=energy_prefix[len(prefix):]-energy_prefix[:-len(prefix)]
    ncc=dot/np.sqrt(np.maximum(window*np.dot(prefix,prefix),1e-18))
    ncc[window<len(prefix)*1e-6]=0
    span=(q[3]-q[1])/RATE
    threshold=.55 if span>=.08 else .97
    peaks,_=signal.find_peaks(ncc,height=threshold,distance=RATE//2)
    accepted=[]
    for p in peaks:
        if p+q[-1]>=len(x): continue
        parts=[]
        for a,b in zip(q[:-1],q[1:]):
            a,b=int(a),int(b)
            v=x[p+a:p+b]
            t=r[a:b]
            parts.append(float(np.dot(v,t)/(np.linalg.norm(v)*np.linalg.norm(t)+1e-15)))
        valid=(ncc[p]>.72 and min(parts[:3])>.60) or min(parts[:3])>.77
        if span<.08: valid=ncc[p]>.97 and min(parts[:3])>.93
        if valid:
            accepted.append({'som':path.name,'inicio_s':float(p/RATE),
                'correlacao_prefixo':float(ncc[p]),'subcorrelacoes':parts})
    results.append({'som':path.name,'pico_correlacao':float(np.max(ncc)),
                    'candidatos':len(peaks),'confirmados':accepted})
    confirmed.extend(accepted)
    (QA/'varredura_completa_parcial.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'{path.name}: {len(accepted)} correspondências',flush=True)
result={'referencias_unicas':len(results),'banda_hz':[70,3400],
    'correspondencias':confirmed,'por_referencia':results}
(QA/'varredura_completa.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'referencias':len(results),'correspondencias':confirmed},ensure_ascii=False,indent=2),flush=True)
