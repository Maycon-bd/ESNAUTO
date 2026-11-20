import json
from pathlib import Path
import numpy as np
from scipy import signal

QA=Path(__file__).resolve().parent/'analise_v005'
rate=8000
x=np.fromfile(QA/'audio_8k_stereo.f32',np.float32).reshape(-1,2).mean(1)
sos=signal.butter(4,[320,3400],btype='bandpass',fs=rate,output='sos')
part=signal.sosfiltfilt(sos,x[370*rate:379*rate])
results=[]
for path in (QA/'referencias').glob('*.npy'):
    r=signal.sosfiltfilt(sos,np.load(path))
    if len(r)>=len(part): continue
    dot=signal.correlate(part,r,mode='valid',method='fft')
    e=np.r_[0,np.cumsum(part*part)]
    ncc=dot/np.sqrt(np.maximum((e[len(r):]-e[:-len(r)])*np.dot(r,r),1e-15))
    index=int(np.argmax(np.abs(ncc)))
    results.append({'som':path.stem,'tempo':370+index/rate,'correlacao':float(ncc[index])})
results.sort(key=lambda r:abs(r['correlacao']),reverse=True)
(QA/'referencia_autor_comparacoes.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(results[:20],ensure_ascii=False,indent=2))
f,t,z=signal.stft(x[370*rate:379*rate],rate,nperseg=1024,noverlap=960,boundary=None)
db=20*np.log10(np.maximum(np.abs(z),1e-8))
np.savez(QA/'espectrograma_referencia_autor.npz',frequencias=f,tempos=t+370,db=db)
