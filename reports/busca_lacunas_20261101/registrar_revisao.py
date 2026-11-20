import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[2]
os.environ['PYTHONIOENCODING'] = 'utf-8'
cli = root / 'Scripts/versao_monografia.py'
task = root / 'reports/busca_lacunas_20261101'
base = json.loads(subprocess.check_output([sys.executable, str(cli), 'atual', '--json'], cwd=root))
assert base['id'] == 'v009', 'Base avançou: conciliar antes de registrar.'
draft = root / 'reports/monografia/trabalho/busca_lacunas_20261101.docx'
sha = hashlib.sha256(draft.read_bytes()).hexdigest()
qa = json.loads((task / 'verificacao_estrutural.json').read_text(encoding='utf-8'))
visual = json.loads((task / 'inspecao_visual.json').read_text(encoding='utf-8'))
assert sha == qa['sha256_candidata'] == visual['sha256_docx']
pending = list(base['pendencias'])
pending[2] = 'Limitação bibliográfica preservada: buscas complementares e registros de seleção parciais. Três células resolvidas com evidência; restam 38 marcações de informação insuficiente, com pesquisa em andamento. Sem alegação de revisão sistemática integral.'
args = [sys.executable, str(cli), 'registrar', '--arquivo', str(draft), '--base', 'v009',
        '--responsavel', 'Codex, revisão documental para Maycon Garcia Silva',
        '--resumo', 'Incorpora três respostas documentadas: Jaeger P1/P3 e Millea P4. Atualiza Quadro 1, Tabela 1, Figura 1 e prosa dependente; inclui fonte original de Evolino e suplemento de Jaeger com limites de versão explícitos. Reduz 41 insuficiências para 38. Pesquisa restante em andamento; resultados experimentais preservados.',
        '--estado', 'em_revisao',
        '--validacao', '78 páginas renderizadas; 45 páginas alteradas inspecionadas e 33 com corpo pixel a pixel idêntico à base. Matriz de 170 células conciliada; 41 títulos, 19 legendas e 60 entradas de listas/sumário conferidos (48 páginas atualizadas). 50 referências anteriores preservadas, 51 no total. Apenas document.xml e imagem da Figura 1 alterados. Introdução e capítulos 3–6 preservados em XML. Sem novos experimentos ou validação científica integral; 38 lacunas permanecem.']
for name in ['relatorio_incorporacao.md', 'verificacao_estrutural.json', 'inspecao_visual.json', 'decisoes_41_em_consolidacao.json', 'conciliacao_proposta.json']:
    args.extend(['--evidencia', str(task / name)])
for item in pending:
    args.extend(['--pendencia', item])
subprocess.run(args, cwd=root, check=True)
current = json.loads(subprocess.check_output([sys.executable, str(cli), 'atual', '--json'], cwd=root))
assert current['anterior'] == 'v009' and current['sha256'] == sha
(task / 'entrega_v010.json').write_text(json.dumps(current, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'id': current['id'], 'arquivo': current['arquivo'], 'sha256': sha}, ensure_ascii=False))
