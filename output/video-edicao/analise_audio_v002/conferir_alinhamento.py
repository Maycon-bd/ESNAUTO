import json
from pathlib import Path
import subprocess
import wave
import numpy as np

root = Path(__file__).resolve().parent
ffmpeg = next((root.parent / 'bin' / 'ffmpeg-dist').glob('*/bin/ffmpeg.exe'))
with wave.open(str(root / 'diagnostico.wav')) as wav:
    original = np.frombuffer(wav.readframes(wav.getnframes()), np.int16).astype(float)
processed = np.frombuffer(subprocess.check_output([str(ffmpeg), '-v', 'error', '-i',
    str(root / 'trecho_tratado_contexto.wav'), '-ac', '1', '-ar', '16000', '-f', 'f32le', 'pipe:1']), np.float32)
results = []
for second in [20, 60, 100, 145]:
    a = original[second*16000:(second+5)*16000]
    b = processed[second*16000:(second+5)*16000]
    a = a - a.mean()
    b = b - b.mean()
    n = 1 << ((len(a) + len(b) - 1).bit_length())
    corr = np.fft.irfft(np.fft.rfft(b, n) * np.conj(np.fft.rfft(a, n)), n)
    lags = np.arange(-1600, 1601)
    lag = int(lags[np.argmax(corr[lags % n])])
    result = {'contexto_s': second, 'atraso_amostras_16k': lag, 'atraso_ms': lag/16}
    results.append(result)
print(json.dumps(results, indent=2))
(root / 'alinhamento.json').write_text(json.dumps(results, indent=2), encoding='utf-8')
