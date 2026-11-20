"""Acrescenta ressalva da variância DM na cópia de trabalho; não executa testes."""
import hashlib
import json
import shutil
from pathlib import Path
from docx import Document

root = Path(__file__).resolve().parents[1]
folder = root / 'reports/fechamento_integral_20261029'
draft = root / 'reports/monografia/trabalho/fechamento_integral_20261029.docx'
expected = '7bcd83fdf866295be877135b8c33c413f21f2e492f7002b5a9278b43e25c7344'
digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
assert digest(draft) == expected
backup = folder / 'antes_lote25.docx'
assert not backup.exists()
shutil.copy2(draft, backup)
doc = Document(draft)
targets = [p for p in doc.paragraphs if p.text.startswith('A variância de longo prazo foi estimada pelo método')]
assert len(targets) == 1
p = targets[0]
before = p.text
addition = (' Com horizonte de um passo, esse cálculo considera apenas a autocovariância '
            'de defasagem zero; eventual dependência serial do diferencial de perda em outras '
            'defasagens não é incorporada à estimativa, o que limita a interpretação dos valores de p.')
p.add_run(addition)
doc.save(draft)
report = {
 'base_registrada': 'v005', 'sha256_base': '2af31abca4e3ba9fd5caf7cd161e55472dc94edc136cdf89732c0d0401118d6b',
 'sha256_rascunho_antes': expected, 'sha256_rascunho_apos_edicao': digest(draft),
 'paragrafo_antes': before, 'acrescimo': addition.strip(),
 'evidencias': ['Scripts/diebold_mariano/06_diebold_mariano.R',
 'Scripts/results/diebold_mariano/ambiente/R-library/forecast/DESCRIPTION',
 'Scripts/results/diebold_mariano/ambiente/R-library/forecast/R/forecast.rdb',
 'https://raw.githubusercontent.com/robjhyndman/forecast/master/R/DM2.R'],
 'verificacao': 'Corpo de forecast::dm.test 9.0.2 extraído da biblioteca local por lazyLoad, sem executar o teste: lag.max=h-1, portanto zero para h=1.',
 'limites': 'A ressalva não demonstra que exista dependência serial nem invalida por si só os resultados; nenhuma execução ou teste foi repetido.',
 'estado': 'editado_pendente_exportacao_validacao_e_inspecao'
}
(folder / 'conferencia_dm_lote25.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print('Ressalva incorporada; rascunho requer exportação e inspeção.')
