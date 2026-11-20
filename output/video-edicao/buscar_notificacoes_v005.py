"""Busca refinada da notificação confirmada pelo autor em 6:14."""
import json
from pathlib import Path
import numpy as np
from scipy import signal

QA=Path(__file__).resolve().parent/'analise_v005'
RATE=8000
sos=signal.butter(4,[70,3400],btype='bandpass',fs=RATE,output='sos')
raw=np.fromfile(QA/'audio_8k_stereo.f32',np.float32).reshape(-1,2).mean(1)
x=signal.sosfiltfilt(sos,raw)
r=signal.sosfiltfilt(sos,np.fromfile(QA/'Windows_Background_8k.f32',np.float32))
q=np.searchsorted(np.cumsum(r*r),np.dot(r,r)*np.array([0,.25,.5,.75,.999]))
prefix_ref=r[:q[3]]
dot=signal.oaconvolve(x,prefix_ref[::-1],mode='valid')
e=np.r_[0,np.cumsum(x*x)]
window=e[len(prefix_ref):]-e[:-len(prefix_ref)]
ncc=dot/np.sqrt(np.maximum(window*np.dot(prefix_ref,prefix_ref),1e-18))
ncc[window<len(prefix_ref)*1e-6]=0
peaks,_=signal.find_peaks(ncc,height=.30,distance=RATE//2)
accepted=[]
all_results=[]
for p in peaks:
    if p+len(r)>len(x): continue
    parts=[]
    for a,b in zip(q[:-1],q[1:]):
        v=x[p+a:p+b]
        ref=r[a:b]
        parts.append(float(np.dot(v,ref)/(np.linalg.norm(v)*np.linalg.norm(ref)+1e-15)))
    confirmed=(ncc[p]>.72 and min(parts[:3])>.60) or min(parts[:3])>.77
    item={'som':'Windows Background.wav','inicio_s':p/RATE,'fim_s':(p+len(r))/RATE,
          'inicio_8k':int(p),'correlacao_prefixo':float(ncc[p]),'subcorrelacoes':parts,
          'confirmado':confirmed}
    all_results.append(item)
    if confirmed: accepted.append(item)
(QA/'notificacoes_confirmadas.json').write_text(json.dumps(accepted,ensure_ascii=False,indent=2),encoding='utf-8')
(QA/'notificacoes_candidatas.json').write_text(json.dumps(all_results,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(accepted,ensure_ascii=False,indent=2))
print('Candidatos:',len(peaks),'confirmados:',len(accepted))
