"""Subtração localizada da notificação conhecida; preserva a linha de tempo."""
import json
from pathlib import Path
import shutil
import numpy as np
from scipy import signal, ndimage

ROOT=Path(__file__).resolve().parent
QA=ROOT/'analise_v005'
RATE=48000
source=np.memmap(QA/'audio_48k_stereo.f32',dtype=np.float32,mode='r').reshape(-1,2)
ref=np.fromfile(QA/'Windows_Background_48k.f32',np.float32).reshape(-1,2).astype(np.float64)
events=json.loads((QA/'notificacoes_confirmadas.json').read_text(encoding='utf-8'))
shutil.copyfile(QA/'audio_48k_stereo.f32',QA/'audio_sem_notificacoes.f32')
output=np.memmap(QA/'audio_sem_notificacoes.f32',dtype=np.float32,mode='r+').reshape(-1,2)
sos=signal.butter(4,[70,3400],btype='bandpass',fs=RATE,output='sos')
rb=signal.sosfiltfilt(sos,ref.mean(1))
fit_end=int(np.searchsorted(np.cumsum(rb*rb),np.dot(rb,rb)*.8))
results=[]
for event in events:
    coarse=round(event['inicio_s']*RATE)
    margin=64
    local=source[coarse-margin:coarse+len(ref)+margin].mean(1).astype(float)
    local=signal.sosfiltfilt(sos,local)
    scores=[]
    for lag in range(-24,25):
        v=local[margin+lag:margin+lag+fit_end]
        r=rb[:fit_end]
        scores.append(np.dot(v,r)/(np.linalg.norm(v)*np.linalg.norm(r)+1e-15))
    best=int(np.argmax(scores))
    lag=best-24
    fractional=0.
    if 0<best<len(scores)-1:
        left,center,right=scores[best-1:best+2]
        fractional=float(np.clip(.5*(left-right)/(left-2*center+right),-.5,.5))
    exact=coarse+lag+fractional
    start=int(np.floor(exact))
    r=ndimage.shift(ref,(exact-start,0),order=3,mode='constant',cval=0)
    actual=source[start:start+len(r)].astype(float)
    components=[]
    for low,high in [(60,220),(220,400),(400,800)]:
        sos_part=signal.butter(4,[low,high],btype='bandpass',fs=RATE,output='sos')
        components.append(signal.sosfiltfilt(sos_part,r,axis=0))
    components.append(r-sum(components))
    model=np.zeros_like(actual)
    coefficients=[]
    for channel in range(2):
        columns=[]
        for component in components:
            analytic=signal.hilbert(component[:,channel])
            columns.extend([analytic.real,analytic.imag])
        basis=np.column_stack(columns)
        a=basis[:fit_end]
        gram=a.T@a
        ridge=max(float(np.trace(gram))/len(gram)*1e-6,1e-12)
        coeff=np.linalg.solve(gram+np.eye(len(gram))*ridge,a.T@actual[:fit_end,channel])
        model[:,channel]=basis@coeff
        coefficients.append(coeff.tolist())
    # Ganho suave no tempo compensa a dinâmica aplicada anteriormente na voz
    # distante. O sinal subtraído continua limitado à forma de onda do alerta.
    xb=signal.sosfiltfilt(sos,actual.mean(1))
    mb=signal.sosfiltfilt(sos,model.mean(1))
    width=int(.10*RATE)
    hop=int(.025*RATE)
    centers=[]
    gains=[]
    energies=[]
    for a in range(0,len(r)-width+1,hop):
        b=a+width
        energy=float(np.dot(mb[a:b],mb[a:b]))
        gain=float(np.dot(xb[a:b],mb[a:b])/(energy+1e-15))
        centers.append(a+width/2)
        gains.append(gain)
        energies.append(energy)
    energies=np.array(energies)
    trusted=energies>energies.max()*.002
    valid_gains=np.clip(np.array(gains)[trusted],.65,1.65)
    envelope=np.interp(np.arange(len(r)),np.array(centers)[trusted],valid_gains)
    envelope=ndimage.gaussian_filter1d(envelope,sigma=RATE*.012)
    cancellation=model*envelope[:,None]
    fade=int(.005*RATE)
    cancellation[:fade]*=np.linspace(0,1,fade)[:,None]
    cancellation[-fade:]*=np.linspace(1,0,fade)[:,None]
    cleaned=actual-cancellation
    assert np.max(np.abs(cleaned))<1, 'Pico inesperado na correção.'
    output[start:start+len(r)]=cleaned.astype(np.float32)
    residual=signal.sosfiltfilt(sos,cleaned.mean(1))
    before_projection=float(np.dot(xb,mb)/(np.dot(mb,mb)+1e-15))
    after_projection=float(np.dot(residual,mb)/(np.dot(mb,mb)+1e-15))
    attenuation=20*np.log10(max(abs(after_projection),1e-12)/max(abs(before_projection),1e-12))
    item={**event,'inicio_refinado_s':start/RATE,'fim_refinado_s':(start+len(r))/RATE,
          'inicio_amostra_48k':start,'amostras_corrigidas':len(r),
          'defasagem_fracionaria_amostras':float(lag+fractional),
          'atenuacao_projecao_do_alerta_db':float(attenuation),
          'ganho_adaptativo_min':float(envelope.min()),'ganho_adaptativo_max':float(envelope.max()),
          'coeficientes_de_fase_e_amplitude':coefficients}
    results.append(item)
    print(f"Alerta {start/RATE:.3f}s: projeção reduzida {attenuation:.1f} dB",flush=True)
output.flush()
(QA/'correcoes_audio.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print('Correções locais concluídas.',flush=True)
