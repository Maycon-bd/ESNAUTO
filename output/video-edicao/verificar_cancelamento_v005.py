import json
from pathlib import Path
import numpy as np
from scipy import signal
import sys

QA=Path(__file__).resolve().parent/'analise_v005'
RATE=8000
sos=signal.butter(4,[70,3400],btype='bandpass',fs=RATE,output='sos')
r=signal.sosfiltfilt(sos,np.fromfile(QA/'Windows_Background_8k.f32',np.float32))
q=np.searchsorted(np.cumsum(r*r),np.dot(r,r)*np.array([0,.25,.5,.75,.999]))
ref=r[:q[3]]
final='--final' in sys.argv
x=np.fromfile(QA/('audio_final_8k_stereo.f32' if final else 'audio_corrigido_8k_stereo.f32'),np.float32).reshape(-1,2).mean(1)
x=signal.sosfiltfilt(sos,x)
dot=signal.oaconvolve(x,ref[::-1],mode='valid')
prefix=np.r_[0,np.cumsum(x*x)]
energy=prefix[len(ref):]-prefix[:-len(ref)]
ncc=dot/np.sqrt(np.maximum(energy*np.dot(ref,ref),1e-18))
ncc[energy<len(ref)*1e-6]=0
peaks,_=signal.find_peaks(ncc,height=.30,distance=RATE//2)
remaining=[]
for p in peaks:
    if p+q[-1]>=len(x): continue
    parts=[]
    for a,b in zip(q[:-1],q[1:]):
        v=x[p+a:p+b]
        t=r[a:b]
        parts.append(float(np.dot(v,t)/(np.linalg.norm(v)*np.linalg.norm(t)+1e-15)))
    if (ncc[p]>.72 and min(parts[:3])>.60) or min(parts[:3])>.77:
        remaining.append({'tempo_s':p/RATE,'correlacao':float(ncc[p]),'partes':parts})
events=json.loads((QA/'notificacoes_confirmadas.json').read_text(encoding='utf-8'))
known=[]
for c in events:
    p=c['inicio_8k']
    a,b=max(0,p-10),min(len(ncc),p+11)
    known.append({'tempo_s':c['inicio_s'],'correlacao_antes':c['correlacao_prefixo'],
        'correlacao_maxima_depois':float(np.max(np.abs(ncc[a:b]))),
        'rms_banda_depois_dbfs':float(20*np.log10(np.sqrt(energy[p]/len(ref))+1e-15))})
result={'ocorrencias_confirmadas_antes':len(events),'ocorrencias_confirmadas_depois':remaining,
        'conferencia_dos_locais':known}
(QA/('verificacao_cancelamento_final.json' if final else 'verificacao_cancelamento.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
assert not remaining, 'Ainda há notificação reconhecível pela busca.'
