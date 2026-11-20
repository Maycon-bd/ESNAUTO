"""Decisão editorial de 28/10/2026; não altera dados experimentais."""
from pathlib import Path
from copy import deepcopy
from collections import Counter
import hashlib, json, shutil
from docx import Document
from docx.shared import Pt, RGBColor

ROOT = Path(__file__).resolve().parents[1]
QA = ROOT / 'reports/auditoria_integral_fasoft_20261028'
DOC = ROOT / 'reports/monografia/MayconGarciaSilva_monografia_FASOFT_conferida.docx'
OLD_QUOTE = '“O caos não é desordem. O caos é o desmascaramento da ordem oculta que existe.”'
NEW_QUOTE = '“Where chaos begins, classical science stops.”'
NEW_CITATION = '(Gleick, 1987, par. 1)'
URL = 'https://www.washingtonpost.com/archive/opinions/1987/10/18/making-sense-of-natures-mess/09f82e1d-5e92-4abf-81ee-9a60f6de1f89/'
REFERENCE = 'GLEICK, James. Making sense of nature’s mess. The Washington Post, 17 out. 1987. Disponível em: ' + URL + '. Acesso em: 28 out. 2026.'

def apply_decision(d):
    """Idempotente; preserva os formatos dos dois parágrafos pessoais."""
    old = [p for p in d.paragraphs if p.text == OLD_QUOTE]
    new = [p for p in d.paragraphs if p.text == NEW_QUOTE]
    assert len(old) + len(new) == 1
    if old:
        p = old[0]
        p.clear()
        r = p.add_run(NEW_QUOTE)
        r.italic = True
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        r.font.color.rgb = RGBColor(0, 0, 0)
        author = next(p for p in d.paragraphs if p.text == '(James Gleick)')
        author.clear()
        r = author.add_run(NEW_CITATION)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(11)
        r.italic = False
        r.font.color.rgb = RGBColor(0, 0, 0)
    refs = [p for p in d.paragraphs if p.style.name == 'Referencias']
    if not any(p.text == REFERENCE for p in refs):
        following = next(p for p in refs if p.text.casefold() > REFERENCE.casefold())
        p = following.insert_paragraph_before(style=following.style)
        p._p.insert(0, deepcopy(following._p.pPr))
        for text, italic in [('GLEICK, James. Making sense of nature’s mess. ', False),
                             ('The Washington Post', True),
                             (', 17 out. 1987. Disponível em: ' + URL + '. Acesso em: 28 out. 2026.', False)]:
            r = p.add_run(text)
            r.italic = italic
            r.font.name = 'Times New Roman'
            r.font.size = Pt(12)
            r.font.color.rgb = RGBColor(0, 0, 0)
    assert sum(p.text == REFERENCE for p in d.paragraphs) == 1

if __name__ == '__main__':
    backup = QA / 'antes_epigrafe'
    backup.mkdir(exist_ok=True)
    for src in [DOC, QA / 'monografia.pdf', *QA.glob('*.json'), QA / 'conferencia_guia.md']:
        dst = backup / src.name
        if not dst.exists(): shutil.copy2(src, dst)
    before = Document(DOC)
    d = Document(DOC)
    apply_decision(d)
    nonref_before = [p.text for p in before.paragraphs if p.style.name != 'Referencias']
    expected = [NEW_QUOTE if x == OLD_QUOTE else NEW_CITATION if x == '(James Gleick)' else x for x in nonref_before]
    assert expected == [p.text for p in d.paragraphs if p.style.name != 'Referencias']
    assert [[c.text for r in t.rows for c in r.cells] for t in before.tables] == [[c.text for r in t.rows for c in r.cells] for t in d.tables]
    oldrefs = Counter(p.text for p in before.paragraphs if p.style.name == 'Referencias')
    newrefs = Counter(p.text for p in d.paragraphs if p.style.name == 'Referencias')
    assert newrefs == oldrefs + Counter([REFERENCE])
    d.save(DOC)
    record = json.loads((QA / 'decisao_epigrafe.json').read_text(encoding='utf-8'))
    record.update(estado='alternativa_adotada', decisao_do_autor='Sim à proposta de alternativa verificada; anotação 1, mensagem de 28/10/2026; interpretação comunicada ao autor.', word_alterado=True, antiga_atribuicao_validada=False, texto_adotado=NEW_QUOTE, citacao=NEW_CITATION, referencia=REFERENCE, sha256_apos_edicao=hashlib.sha256(DOC.read_bytes()).hexdigest())
    record.pop('condicao_pendente', None)
    record['auditoria_bloqueio_historica'] = record.pop('auditoria_bloqueio', {})
    record['turnos_consecutivos_com_condicao'] = 0
    (QA / 'decisao_epigrafe.json').write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding='utf-8')
    print('Epígrafe e referência regularizadas; 49 referências anteriores e todo o corpo preservados.')
