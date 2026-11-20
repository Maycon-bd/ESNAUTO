import json
from pathlib import Path
import subprocess
import wave
import numpy as np

root = Path(__file__).resolve().parent
ffmpeg = next((root.parent / 'bin' / 'ffmpeg-dist').glob('*/bin/ffmpeg.exe'))
output = root.parent / 'exportados' / 'ESNAUTO_apresentacao_25min_v002_audio_corrigido.mp4'
with wave.open(str(root / 'diagnostico.wav')) as wav:
    original = np.frombuffer(wav.readframes(wav.getnframes()), np.int16).astype(float)
results = []
for second in [660, 700, 760]:
    a = original[(second-626)*16000:(second-626+5)*16000]
    b = np.frombuffer(subprocess.check_output([str(ffmpeg), '-v', 'error', '-ss', str(second),
        '-i', str(output), '-t', '5', '-ac', '1', '-ar', '16000', '-f', 'f32le', 'pipe:1']), np.float32)
    a, b = a - a.mean(), b - b.mean()
    n = 1 << ((len(a)+len(b)-1).bit_length())
    corr = np.fft.irfft(np.fft.rfft(b,n) * np.conj(np.fft.rfft(a,n)),n)
    lags = np.arange(-1600,1601)
    lag = int(lags[np.argmax(corr[lags%n])])
    assert abs(lag) < 16, 'Deslocamento superior a 1 ms exige reexame.'
    results.append({'inicio_s': second, 'atraso_ms': lag/16})
(root/'alinhamento_final.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print(json.dumps(results,indent=2))
