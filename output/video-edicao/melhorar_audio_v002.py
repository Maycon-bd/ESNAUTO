"""Correção localizada no áudio de 10:31–13:06, preservando vídeo e duração."""
import hashlib
import json
from pathlib import Path
import subprocess
import wave
import numpy as np

ROOT = Path(__file__).resolve().parent
QA = ROOT / 'analise_audio_v002'
BIN = next((ROOT / 'bin' / 'ffmpeg-dist').glob('*/bin'))
SOURCE = ROOT / 'exportados' / 'ESNAUTO_apresentacao_25min_v001.mp4'
OUTPUT = ROOT / 'exportados' / 'ESNAUTO_apresentacao_25min_v002_audio_corrigido.mp4'
START, END, RATE = 631, 786, 48000
DSP = ('highpass=f=75,afftdn=nr=6:nf=-48:tn=1,'
       'equalizer=f=280:t=q:w=0.8:g=-1.5,equalizer=f=2600:t=q:w=0.8:g=2.5,'
       'acompressor=threshold=0.05:ratio=3:attack=3:release=160:knee=4,'
       'dynaudnorm=f=300:g=21:p=0.9:m=16:r=0.13:t=0.002:b=1,'
       'loudnorm=I=-16:TP=-1.5:LRA=7:print_format=json,aresample=48000')

def ffmpeg(args, log):
    with (QA / log).open('w', encoding='utf-8') as f:
        subprocess.run([str(BIN / 'ffmpeg.exe'), '-hide_banner', '-nostdin',
                        '-nostats', '-n', *args], stdout=f, stderr=subprocess.STDOUT, check=True)

probe = json.loads(subprocess.check_output([str(BIN / 'ffprobe.exe'), '-v', 'error',
    '-show_streams', '-show_format', '-of', 'json', str(SOURCE)], text=True))
audio = next(s for s in probe['streams'] if s['codec_type'] == 'audio')
sample_count = round(float(audio['duration']) * RATE)
if not (QA / 'trecho_tratado_contexto.wav').exists():
    ffmpeg(['-threads', '2', '-ss', '626', '-i', str(SOURCE), '-t', '165', '-vn',
            '-af', DSP, '-c:a', 'pcm_f32le', str(QA / 'trecho_tratado_contexto.wav')], 'tratamento.log')
ffmpeg(['-threads', '2', '-i', str(SOURCE), '-vn', '-af', f'atrim=end_sample={sample_count}',
        '-ar', str(RATE), '-ac', '2', '-c:a', 'pcm_s16le', str(QA / 'audio_v001.wav')], 'decodificar_audio.log')
# O denoiser introduz 25 ms, medidos por correlação em quatro janelas. Remover
# esse atraso antes da mistura para preservar a sincronia e evitar eco na transição.
ffmpeg(['-ss', '5.025', '-i', str(QA / 'trecho_tratado_contexto.wav'), '-t', str(END-START),
        '-ar', str(RATE), '-ac', '2', '-c:a', 'pcm_s16le', str(QA / 'trecho_alinhado.wav')], 'alinhar_trecho.log')
with wave.open(str(QA / 'audio_v001.wav')) as original, \
     wave.open(str(QA / 'trecho_alinhado.wav')) as treated, \
     wave.open(str(QA / 'audio_v002.wav'), 'wb') as dest:
    dest.setparams(original.getparams())
    remaining = START * RATE
    while remaining:
        count = min(remaining, RATE * 30)
        dest.writeframesraw(original.readframes(count))
        remaining -= count
    count = (END-START) * RATE
    dry = np.frombuffer(original.readframes(count), np.int16).reshape(-1, 2).astype(np.float32)
    wet = np.frombuffer(treated.readframes(count), np.int16).reshape(-1, 2).astype(np.float32)
    assert dry.shape == wet.shape == (count, 2)
    mix = np.ones(count, dtype=np.float32)
    fade = round(.6 * RATE)
    mix[:fade] = np.linspace(0, 1, fade, dtype=np.float32)
    mix[-fade:] = np.linspace(1, 0, fade, dtype=np.float32)
    mixed = np.rint(dry * (1-mix[:, None]) + wet * mix[:, None]).clip(-32768, 32767).astype(np.int16)
    dest.writeframesraw(mixed.tobytes())
    while block := original.readframes(RATE * 30):
        dest.writeframesraw(block)
print('Trecho tratado e alinhado; transições de 600 ms aplicadas.', flush=True)
ffmpeg(['-i', str(SOURCE), '-i', str(QA / 'audio_v002.wav'), '-map', '0:v:0', '-map', '1:a:0',
        '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-ar', str(RATE),
        '-movflags', '+faststart', '-map_metadata', '0', '-metadata',
        'title=ESNAUTO - Apresentação do TFC - áudio corrigido v002', str(OUTPUT)], 'exportar_v002.log')
new_probe = json.loads(subprocess.check_output([str(BIN / 'ffprobe.exe'), '-v', 'error',
    '-show_streams', '-show_format', '-of', 'json', str(OUTPUT)], text=True))
assert float(new_probe['format']['duration']) <= 1500
assert abs(float(new_probe['format']['duration']) - float(probe['format']['duration'])) < .025
video_hashes = []
for path in [SOURCE, OUTPUT]:
    video_hashes.append(subprocess.check_output([str(BIN / 'ffmpeg.exe'), '-v', 'error', '-i', str(path),
        '-map', '0:v:0', '-c', 'copy', '-f', 'hash', '-hash', 'sha256', '-'], text=True).strip())
assert video_hashes[0] == video_hashes[1], 'A trilha de vídeo deve permanecer idêntica.'
outside = []
with wave.open(str(QA / 'audio_v001.wav')) as a, wave.open(str(QA / 'audio_v002.wav')) as b:
    assert a.getnframes() == b.getnframes()
    for start, end in [(0, START*RATE), (END*RATE, a.getnframes())]:
        a.setpos(start)
        b.setpos(start)
        ha, hb = hashlib.sha256(), hashlib.sha256()
        remaining = end-start
        while remaining:
            count = min(remaining, RATE*30)
            ha.update(a.readframes(count))
            hb.update(b.readframes(count))
            remaining -= count
        assert ha.hexdigest() == hb.hexdigest()
        outside.append({'inicio_amostra': start, 'fim_amostra': end, 'sha256_pcm': ha.hexdigest()})
with OUTPUT.open('rb') as f:
    output_hash = hashlib.file_digest(f, 'sha256').hexdigest()
with SOURCE.open('rb') as f:
    source_hash = hashlib.file_digest(f, 'sha256').hexdigest()
result = {'base': str(SOURCE), 'sha256_base': source_hash, 'saida': str(OUTPUT),
    'sha256_saida': output_hash, 'inicio_tratamento_s': START, 'fim_tratamento_s': END,
    'compensacao_atraso_dsp_ms': 25, 'transicoes_s': .6, 'filtros': DSP,
    'video_identico_sha256': video_hashes[0], 'pcm_fora_do_trecho_inalterado': outside,
    'duracao_s': float(new_probe['format']['duration']), 'probe': new_probe}
(QA / 'verificacao_v002.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({k: result[k] for k in ['saida', 'duracao_s', 'sha256_saida', 'video_identico_sha256']}, ensure_ascii=False, indent=2), flush=True)
