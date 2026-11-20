import json
from pathlib import Path
import numpy as np
from scipy import signal

ROOT=Path(__file__).resolve().parent
QA=ROOT/'analise_v005'
d=json.loads((QA/'deteccao.json').read_text(encoding='utf-8'))
sos=signal.butter(4,[320,3400],btype='bandpass',fs=8000,output='sos')
x=np.fromfile(QA/'audio_8k_stereo.f32',np.float32).reshape(-1,2).mean(1)
x=signal.sosfiltfilt(sos,x)
accepted=[]
checks=[]
for c in d['candidatos']:
    if c['correlacao']<.22: continue
    ref=signal.sosfiltfilt(sos,np.load(c['referencia_npy']))
    cumulative=np.cumsum(ref*ref)
    indices=np.searchsorted(cumulative,cumulative[-1]*np.array([.001,.25,.5,.75,.999]))
    span=(indices[3]-indices[1])/8000
    correlations=[]
    gains=[]
    for a,b in zip(indices[:-1],indices[1:]):
        v=x[c['amostra_inicio']+a:c['amostra_inicio']+b]
        r=ref[a:b]
        correlations.append(float(np.dot(v,r)/(np.linalg.norm(v)*np.linalg.norm(r)+1e-15)))
        gains.append(float(np.dot(v,r)/(np.dot(r,r)+1e-15)))
    ok=(span>=.08 and sum(v>.82 for v in correlations)>=3 and min(correlations)>-.1)
    if span<.08: ok=c['correlacao']>.96 and min(correlations)>.85
    checks.append({**c,'subcorrelacoes':correlations,'ganhos_subjanelas':gains,'aceito':ok})
    if ok: accepted.append(checks[-1])
accepted.sort(key=lambda c:c['inicio_s'])
# Uma mesma notificação pode compartilhar trechos com mais de um arquivo do SO.
unique=[]
for c in sorted(accepted,key=lambda c:c['correlacao'],reverse=True):
    if any(abs(c['inicio_s']-a['inicio_s'])<.3 for a in unique): continue
    unique.append(c)
unique.sort(key=lambda c:c['inicio_s'])
(QA/'alertas_confirmados.json').write_text(json.dumps(unique,ensure_ascii=False,indent=2),encoding='utf-8')
(QA/'validacao_candidatos.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(unique,ensure_ascii=False,indent=2))
