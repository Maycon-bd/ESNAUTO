import hashlib
import json
import pathlib
import subprocess

r = json.loads(subprocess.check_output(
    ['python', 'Scripts/versao_monografia.py', 'atual', '--json'],
    text=True, encoding='utf-8'))
assert r['id'] == 'v009'
assert hashlib.sha256(pathlib.Path(r['arquivo']).read_bytes()).hexdigest() == r['sha256'] == '793910fae2daaa2d5dbdcfa0cd76177c6c6a38c353d98d94ecaaaecf118c7b03'
pathlib.Path('reports/devolutiva_orientador_20261101/entrega.json').write_text(
    json.dumps(r, ensure_ascii=False, indent=2), encoding='utf-8')
p = pathlib.Path('docs/assistencia_monografia/contexto.md')
t = p.read_text(encoding='utf-8')
marker = '## Conciliação da devolutiva — 1º de novembro de 2026'
if marker not in t:
    t += '''

## Conciliação da devolutiva — 1º de novembro de 2026

O autor determinou expressamente que o Guia FASOFT prevalece na formatação. A introdução deve permanecer em texto corrido, sem subseções, conforme a página física 25 do guia. A observação do orientador sobre seções/subseções motivou conferência da numeração existente: 41 títulos sequenciais, sem necessidade de subdividir a introdução.

Registrada v009 a partir da v008, SHA256 `793910fae2daaa2d5dbdcfa0cd76177c6c6a38c353d98d94ecaaaecf118c7b03`, conciliando a introdução da devolutiva recebida em Downloads e preservando as três correções locais da v008. Introdução contínua em três páginas; 59 referências de página atualizadas no sumário/listas; 77 páginas inspecionadas. Os 52 sinais textuais de interrogação são códigos explicados de informação insuficiente, preservados. Resultados, imagens, tabelas e referências mantidos. Relatório: `reports/devolutiva_orientador_20261101/relatorio.md`. Consultar sempre o registro oficial antes de novo trabalho; esta anotação é histórica.
'''
    p.write_text(t, encoding='utf-8')
print('Vigente v009 e SHA256 confirmados; entrega e contexto registrados.')
