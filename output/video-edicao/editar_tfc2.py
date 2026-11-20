"""Edição discreta: encurta silêncios longos e normaliza áudio em duas passagens."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parent
ANALISE = ROOT / 'analise_tfc2'
ORIGINAL = ROOT / 'entrada' / 'Video final tfc2.mp4'
SAIDA = ROOT / 'exportados' / 'ESNAUTO_apresentacao_25min_v001.mp4'
BIN = next((ROOT / 'bin' / 'ffmpeg-dist').glob('*/bin'))
FPS = 30

parser = argparse.ArgumentParser()
parser.add_argument('--render', action='store_true')
args = parser.parse_args()
log = (ANALISE / 'audio_analise.log').read_text(encoding='utf-8-sig')
metrics = json.loads(re.findall(r'\{[^{}]*"input_i"[^{}]*\}', log)[-1])
silences = json.loads((ANALISE / 'pausas.json').read_text())
transcript_path = ANALISE / 'transcricao_automatica.json'
if not transcript_path.exists():
    raise RuntimeError('Concluir a transcrição antes de fechar o plano de cortes.')
transcript = json.loads(transcript_path.read_text(encoding='utf-8'))
protected = [(word['start'] - 0.2, word['end'] + 0.2)
             for segment in transcript['segments'] for word in segment.get('words', [])]
cuts = []
for item in silences:
    # Silêncios menores preservam o ritmo natural da fala. Não cortar palavras.
    if item['duracao'] < 1.5:
        continue
    start = math.ceil((item['inicio'] + 0.38) * FPS)
    end = math.floor((item['fim'] - 0.38) * FPS)
    # O reconhecimento automático pode posicionar uma palavra nas margens do
    # silêncio detectado. Preservar também 200 ms ao redor dessas palavras.
    for word_start, word_end in protected:
        if word_end <= start / FPS or word_start >= end / FPS:
            continue
        if word_start <= start / FPS:
            start = max(start, math.ceil(word_end * FPS))
        elif word_end >= end / FPS:
            end = min(end, math.floor(word_start * FPS))
        else:
            # Uma palavra no centro torna esse corte incerto: preservar o trecho.
            end = start
            break
    if end > start:
        cuts.append({'inicio_frame': start, 'fim_frame_exclusivo': end,
                     'inicio_s': start / FPS, 'fim_s': end / FPS,
                     'motivo': 'Encurtamento do centro de silêncio longo; margens preservadas.'})

# Retirar a analogia longa com uma folha de papel. A definição da busca e os
# cinco hiperparâmetros permanecem; o cataclismo é explicado novamente adiante.
# Retirar também a referência verbal à analogia retirada, preservando a frase
# "e o mecanismo de cataclismo ... para renovar as soluções".
for start, end, reason in [
    (10952, 12754, 'Retirada da analogia longa com papel/hiperplano; explicação operacional mantida.'),
    (14397, 14472, 'Retirada da referência à analogia anterior; mantém objetivo do cataclismo.')]:
    cuts.append({'inicio_frame': start, 'fim_frame_exclusivo': end,
                 'inicio_s': start / FPS, 'fim_s': end / FPS, 'motivo': reason})
cuts.sort(key=lambda item: item['inicio_frame'])
for previous, following in zip(cuts, cuts[1:]):
    assert previous['fim_frame_exclusivo'] <= following['inicio_frame']
kept = 46770 - sum(c['fim_frame_exclusivo'] - c['inicio_frame'] for c in cuts)
assert kept / FPS <= 1500, 'A entrega deve ter no máximo 25 minutos.'
expr = 'not(' + '+'.join(f"gte(n,{c['inicio_frame']})*lt(n,{c['fim_frame_exclusivo']})" for c in cuts) + ')'
norm = ('loudnorm=I=-16:TP=-1.5:LRA=11:linear=true:'
        f"measured_I={metrics['input_i']}:measured_TP={metrics['input_tp']}:"
        f"measured_LRA={metrics['input_lra']}:measured_thresh={metrics['input_thresh']}:"
        'offset=0:print_format=json')
# Quadros de áudio de 1600 amostras = 1/30 s a 48 kHz. A mesma seleção por
# número de quadro mantém áudio e vídeo sincronizados em todos os cortes.
vf = f"select='{expr}',setpts=N/(30*TB)"
af = f"{norm},aresample=48000,asetnsamples=n=1600:p=0,aselect='{expr}',asetpts=N/SR/TB"
cmd = [str(BIN / 'ffmpeg.exe'), '-hide_banner', '-nostdin', '-n',
       '-threads', '4', '-i', str(ORIGINAL), '-map', '0:v:0', '-map', '0:a:0',
       '-vf', vf, '-af', af, '-c:v', 'h264_nvenc', '-preset', 'p5', '-tune', 'hq',
       '-rc', 'vbr', '-cq', '18', '-b:v', '0', '-profile:v', 'high',
       '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000',
       '-movflags', '+faststart', '-map_metadata', '-1',
       '-metadata', 'title=ESNAUTO - Apresentação do TFC - edição v001',
       '-progress', str(ANALISE / 'render_progresso.log'), '-nostats', str(SAIDA)]
with ORIGINAL.open('rb') as file:
    source_hash = hashlib.file_digest(file, 'sha256').hexdigest()
plan = {'original': str(ORIGINAL), 'sha256_original': source_hash,
        'duracao_original_s': 1559, 'fps': FPS, 'cortes': cuts,
        'quadros_saida_esperados': kept, 'duracao_saida_esperada_s': kept / FPS,
        'segundos_retirados': (46770 - kept) / FPS,
        'audio_medido_original': metrics,
        'audio_alvo': {'LUFS': -16, 'true_peak_dBTP': -1.5, 'LRA': 11},
        'conteudo': 'Edição discreta com redução da analogia repetida, ajuste de referência verbal e pausas. Slides, câmera, demonstração e resultados mantidos; sem aceleração.',
        'limite_autor_s': 1500,
        'comando': cmd, 'saida': str(SAIDA)}
(ANALISE / 'plano_edicao.json').write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({key: plan[key] for key in ['segundos_retirados', 'duracao_saida_esperada_s', 'cortes']}, ensure_ascii=False, indent=2), flush=True)
if args.render:
    with (ANALISE / 'render.log').open('w', encoding='utf-8') as render_log:
        subprocess.run(cmd, stdout=render_log, stderr=subprocess.STDOUT, check=True)
    print(f'Exportado: {SAIDA}', flush=True)
