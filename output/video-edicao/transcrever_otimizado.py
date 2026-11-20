"""Transcrição local incremental para orientar a edição, sem alterar a mídia."""
import argparse
import dataclasses
import json
import wave
import numpy as np
from pathlib import Path
from faster_whisper import WhisperModel, BatchedInferencePipeline

parser = argparse.ArgumentParser()
parser.add_argument('audio', type=Path)
parser.add_argument('saida', type=Path)
parser.add_argument('--modelo', default='base')
parser.add_argument('--beam-size', type=int, default=1)
parser.add_argument('--batch-size', type=int, default=0)
args = parser.parse_args()
args.saida.mkdir(parents=True, exist_ok=True)
model_dir = Path(__file__).parent / 'modelos' / 'faster-whisper'
print(f'Carregando modelo {args.modelo} INT8 na CPU...', flush=True)
model = WhisperModel(args.modelo, device='cpu', compute_type='int8', cpu_threads=4,
                     num_workers=1, download_root=str(model_dir))
with wave.open(str(args.audio), 'rb') as wav:
    if (wav.getnchannels(), wav.getframerate(), wav.getsampwidth()) != (1, 16000, 2):
        raise ValueError('Esperado WAV PCM16 mono a 16 kHz.')
    samples = np.frombuffer(wav.readframes(wav.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
engine = BatchedInferencePipeline(model=model) if args.batch_size else model
batch_options = {'batch_size': args.batch_size} if args.batch_size else {}
segments, info = engine.transcribe(samples, language='pt', beam_size=args.beam_size,
    word_timestamps=True, vad_filter=True,
    vad_parameters={'min_silence_duration_ms': 500},
    initial_prompt='Maycon Garcia Silva, Fabian Corrêa Cardoso, ESNAUTO, PETR4, ESN, GRU, LSTM, Win, Wout, Jaeger, BovDB, Diebold-Mariano.',
    **batch_options)
print(f'Áudio: {info.duration:.1f}s; idioma: {info.language}', flush=True)
results = []
with (args.saida / 'transcricao_segmentos.jsonl').open('w', encoding='utf-8') as jf, \
     (args.saida / 'transcricao_tempos.txt').open('w', encoding='utf-8') as tf:
    for segment in segments:
        item = dataclasses.asdict(segment)
        results.append(item)
        jf.write(json.dumps(item, ensure_ascii=False) + '\n')
        jf.flush()
        tf.write(f'[{segment.start:8.2f} - {segment.end:8.2f}] {segment.text.strip()}\n')
        tf.flush()
        print(f'{segment.end:7.1f}/{info.duration:.1f}s | {segment.text.strip()}', flush=True)
(args.saida / 'transcricao_automatica.json').write_text(json.dumps({
    'modelo': args.modelo, 'motor': 'faster-whisper', 'precisao': 'int8',
    'language': info.language, 'duration': info.duration,
    'nota': 'Transcrição automática para orientar edição; não validada como legenda.',
    'segments': results}, ensure_ascii=False, indent=2), encoding='utf-8')
print('Concluído.', flush=True)
