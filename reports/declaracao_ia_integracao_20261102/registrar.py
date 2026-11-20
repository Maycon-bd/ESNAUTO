import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'reports/declaracao_ia_integracao_20261102'
cli = [sys.executable, str(ROOT / 'Scripts/versao_monografia.py')]

def run(args):
    return subprocess.run(cli + args, cwd=ROOT, check=True, capture_output=True,
                          encoding='utf-8', env={**__import__('os').environ, 'PYTHONIOENCODING': 'utf-8'}).stdout

current = json.loads(run(['atual', '--json']))
assert current['id'] == 'v010', 'A base avançou: conciliar antes de registrar.'
proof = json.loads((OUT / 'conferencia_final.json').read_text(encoding='utf-8'))
candidate = ROOT / 'reports/monografia/trabalho/declaracao_ia_20261102.docx'
assert hashlib.sha256(candidate.read_bytes()).hexdigest() == proof['trabalho_sha256']
visual = {
    'base': current['id'], 'base_sha256': current['sha256'],
    'candidato_sha256': proof['trabalho_sha256'],
    'paginas_renderizadas': 81,
    'paginas_inspecionadas': proof['paginas_a_inspecionar'],
    'corpos_identicos_excluida_faixa_superior': len(proof['corpos_identicos']),
    'declaracao_separada': 'Uma página renderizada e inspecionada; sem cortes ou sobreposições.',
    'resultado': 'Páginas afetadas inspecionadas; tabelas curtas inteiras, declaração e listas legíveis.'
}
(OUT / 'inspecao_visual.json').write_text(json.dumps(visual, ensure_ascii=False, indent=2), encoding='utf-8')
args = [
    'registrar', '--arquivo', str(candidate), '--base', 'v010',
    '--responsavel', 'Codex para Maycon Garcia Silva',
    '--resumo', 'Incorpora declaração de responsabilidade coletiva de IAG conforme relato do autor, com somente Codex nos testes; inclui indicação em 3.1, Anexo A e entrada no sumário. Atualiza paginação e mantém quatro tabelas curtas da metodologia inteiras, preservando os dados e resultados.',
    '--estado', 'em_revisao',
    '--validacao', '81 páginas renderizadas; 20 páginas afetadas inspecionadas e 61 corpos idênticos à base. 61 entradas de listas/sumário conciliadas, 34 atualizadas. 554 parágrafos anteriores e dados das 14 tabelas preservados. Apenas document.xml alterado. Declaração separada de uma página renderizada e inspecionada. Sem novos experimentos, aprovação acadêmica ou assinatura dos declarantes.'
]
for name in ['relatorio.md', 'conferencia_final.json', 'inspecao_visual.json', 'alteracoes.json', 'complemento_testes.json']:
    args += ['--evidencia', str(OUT / name)]
pending = current['pendencias'] + [
    'Declaração de uso de IAG preenchida conforme relato do autor; versões de Claude e Codex não informadas. Data e assinaturas do autor e orientador permanecem em branco para preenchimento pelos declarantes.'
]
for item in pending:
    args += ['--pendencia', item]
result = run(args)
(OUT / 'registro_saida.txt').write_text(result, encoding='utf-8')
final = json.loads(run(['atual', '--json']))
assert final['anterior'] == 'v010'
assert final['sha256'] == proof['trabalho_sha256']
assert hashlib.sha256(Path(final['caminho_absoluto']).read_bytes()).hexdigest() == final['sha256']
(OUT / 'versao_entregue.json').write_text(json.dumps(final, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({k: final[k] for k in ['id', 'arquivo', 'sha256']}, ensure_ascii=False, indent=2))
