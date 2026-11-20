"""Reescuta automática das duas junções de fala para apoio à revisão."""
import json
from pathlib import Path
import subprocess
import numpy as np
from faster_whisper import WhisperModel

root = Path(__file__).resolve().parent
analysis = root / 'analise_tfc2'
plan = json.loads((analysis / 'plano_edicao.json').read_text(encoding='utf-8'))
ffmpeg = next((root / 'bin' / 'ffmpeg-dist').glob('*/bin/ffmpeg.exe'))
model = WhisperModel('base', device='cpu', compute_type='int8', cpu_threads=4,
                     download_root=str(root / 'modelos' / 'faster-whisper'), local_files_only=True)
results = []
for cut in plan['cortes']:
    if 'analogia' not in cut['motivo']:
        continue
    removed_before = sum(c['fim_frame_exclusivo'] - c['inicio_frame'] for c in plan['cortes']
                         if c['fim_frame_exclusivo'] <= cut['inicio_frame'])
    seam = (cut['inicio_frame'] - removed_before) / 30
    pcm = subprocess.check_output([str(ffmpeg), '-v', 'error', '-threads', '2',
        '-ss', str(seam - 3), '-i', plan['saida'], '-t', '18', '-vn',
        '-ac', '1', '-ar', '16000', '-f', 's16le', 'pipe:1'])
    signal = np.frombuffer(pcm, dtype=np.int16).astype(np.float32) / 32768
    segments, _ = model.transcribe(signal, language='pt', beam_size=1,
        initial_prompt='ESN, algoritmo genético, cromossomos, cataclismo, hipercubo latino.')
    text = ' '.join(segment.text.strip() for segment in segments)
    results.append({'juncao_saida_s': seam, 'transcricao_automatica': text})
    print(json.dumps(results[-1], ensure_ascii=False), flush=True)
(analysis / 'conferencia_juncoes.json').write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')
