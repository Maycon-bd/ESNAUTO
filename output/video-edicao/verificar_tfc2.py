"""Conferência do arquivo exportado, sincronização, decodificação e quadros."""
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent
ANALISE = ROOT / 'analise_tfc2'
BIN = next((ROOT / 'bin' / 'ffmpeg-dist').glob('*/bin'))
plan = json.loads((ANALISE / 'plano_edicao.json').read_text(encoding='utf-8'))
output = Path(plan['saida'])
probe = json.loads(subprocess.check_output([str(BIN / 'ffprobe.exe'), '-v', 'error',
    '-show_streams', '-show_format', '-of', 'json', str(output)], text=True))
video = next(s for s in probe['streams'] if s['codec_type'] == 'video')
audio = next(s for s in probe['streams'] if s['codec_type'] == 'audio')
assert video['width'] == 1920 and video['height'] == 1080
assert video['r_frame_rate'] == '30/1'
assert int(video['nb_frames']) == plan['quadros_saida_esperados']
assert float(probe['format']['duration']) <= 1500
assert abs(float(video['duration']) - float(audio['duration'])) < .05
print('Metadados e limite de duração conferidos.', flush=True)
with (ANALISE / 'qa_decodificacao_audio.log').open('w', encoding='utf-8') as log:
    subprocess.run([str(BIN / 'ffmpeg.exe'), '-hide_banner', '-nostats', '-nostdin',
        '-threads', '4', '-filter_threads', '2', '-i', str(output),
        '-map', '0:v:0', '-map', '0:a:0', '-af', 'ebur128=peak=true:framelog=verbose',
        '-f', 'null', 'NUL'], stdout=log, stderr=subprocess.STDOUT, check=True)
print('Decodificação integral concluída.', flush=True)
samples = [0, 10940, 12766, 14385, 14484, 22500, 25165, 39428, 41580, 44940, 46000, 46760]
comparisons = []
for i, original_frame in enumerate(samples):
    removed = sum(c['fim_frame_exclusivo'] - c['inicio_frame'] for c in plan['cortes']
                  if c['fim_frame_exclusivo'] <= original_frame)
    edited_frame = original_frame - removed
    for tag, path, frame in [('original', plan['original'], original_frame), ('editado', str(output), edited_frame)]:
        folder = ANALISE / 'qa_quadros' / tag
        folder.mkdir(parents=True, exist_ok=True)
        subprocess.run([str(BIN / 'ffmpeg.exe'), '-v', 'error', '-nostdin', '-n',
            '-threads', '2', '-ss', f'{frame / 30:.9f}', '-i', path,
            '-vf', 'scale=960:-1', '-frames:v', '1', '-threads', '1', str(folder / f'{i:02d}.jpg')], check=True)
    comparisons.append({'original_frame': original_frame, 'editado_frame': edited_frame,
                        'original_s': original_frame / 30, 'editado_s': edited_frame / 30})
for tag in ['original', 'editado']:
    folder = ANALISE / 'qa_quadros' / tag
    subprocess.run([str(BIN / 'ffmpeg.exe'), '-v', 'error', '-nostdin', '-n',
        '-framerate', '1', '-i', str(folder / '%02d.jpg'), '-vf', 'scale=384:-1,tile=4x3',
        '-frames:v', '1', '-threads', '1', str(ANALISE / f'qa_contato_{tag}.jpg')], check=True)
with output.open('rb') as file:
    output_hash = hashlib.file_digest(file, 'sha256').hexdigest()
with Path(plan['original']).open('rb') as file:
    source_hash = hashlib.file_digest(file, 'sha256').hexdigest()
assert source_hash == plan['sha256_original'], 'Original alterado durante a edição.'
result = {'arquivo': str(output), 'sha256': output_hash, 'original_preservado_sha256': source_hash,
          'duracao_s': float(probe['format']['duration']), 'quadros': int(video['nb_frames']),
          'resolucao': [video['width'], video['height']], 'fps': video['r_frame_rate'],
          'audio_video_diferenca_s': abs(float(video['duration']) - float(audio['duration'])),
          'decodificacao_integral': 'sucesso', 'quadros_para_inspecao_visual': comparisons,
          'probe': probe}
(ANALISE / 'verificacao_final.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({key: result[key] for key in ['arquivo', 'duracao_s', 'quadros', 'audio_video_diferenca_s', 'sha256']}, ensure_ascii=False, indent=2), flush=True)
