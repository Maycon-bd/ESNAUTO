"""Transcrição comparativa de amostras para verificar palavras nos locais tratados."""
import json
from pathlib import Path
import numpy as np
from scipy import signal
from faster_whisper import WhisperModel

ROOT=Path(__file__).resolve().parent
QA=ROOT/'analise_v005'
old=np.memmap(QA/'audio_48k_stereo.f32',np.float32,mode='r').reshape(-1,2)
new=np.memmap(QA/'audio_sem_notificacoes.f32',np.float32,mode='r').reshape(-1,2)
events=json.loads((QA/'correcoes_audio.json').read_text(encoding='utf-8'))
model=WhisperModel('small',device='cpu',compute_type='int8',cpu_threads=4,
    download_root=str(ROOT/'modelos'/'faster-whisper'),local_files_only=True)
result=[]
for event in events:
    t=event['inicio_refinado_s']
    begin=max(0,t-2)
    end=event['fim_refinado_s']+2.5
    item={'alerta_s':t,'inicio_amostra_s':begin,'fim_amostra_s':end}
    for name,pcm in [('antes',old),('depois',new)]:
        audio=signal.resample_poly(pcm[round(begin*48000):round(end*48000)].mean(1),1,3).astype(np.float32)
        segments,_=model.transcribe(audio,language='pt',beam_size=1,
            initial_prompt='Maycon Garcia Silva, ESN, algoritmo genético, cromossomos, Ridge, MAE, RMSE, GRU, LSTM.')
        item[name]=' '.join(s.text.strip() for s in segments)
    result.append(item)
    print(json.dumps(item,ensure_ascii=False),flush=True)
(QA/'conferencia_fala.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
