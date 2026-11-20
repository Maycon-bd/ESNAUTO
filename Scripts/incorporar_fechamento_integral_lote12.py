"""Incorpora nove precisões/autorias com evidências do lote 12."""
from pathlib import Path
from zipfile import ZipFile
from shutil import copy2
from lxml import etree
import json
import hashlib
from incorporar_fechamento_integral_lote1 import visible, replace_text, format_revised_prose, NS

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'reports/fechamento_integral_20261029'


def main():
    record = OUT / 'incorporacao_lote12.json'
    assert not record.exists(), 'Não reaplicar lote já incorporado.'
    state = json.loads((OUT / 'estado_meta.json').read_text(encoding='utf-8'))
    draft = ROOT / state['copia_trabalho']
    evidence = json.loads((OUT / 'leituras_liu_hariharan_xiao_lote12.json').read_text(encoding='utf-8'))
    digest = hashlib.sha256(draft.read_bytes()).hexdigest()
    assert digest == state['sha256_copia_trabalho_atual'] == evidence['sha256_rascunho_examinado']
    registry = json.loads((ROOT / 'docs/assistencia_monografia/versao_vigente.json').read_text(encoding='utf-8'))
    assert registry['vigente'] == state['base'] == 'v005'
    base = next(x for x in registry['versoes'] if x['id'] == registry['vigente'])
    assert hashlib.sha256((ROOT / base['arquivo']).read_bytes()).hexdigest() == state['sha256_base']
    with ZipFile(draft) as z:
        infos = z.infolist()
        parts = {i.filename: z.read(i.filename) for i in infos}
    before = dict(parts)
    tree = etree.fromstring(parts['word/document.xml'])
    invpath = OUT / 'inventario_unidades.json'
    inv = json.loads(invpath.read_text(encoding='utf-8'))
    lookup = {x['id']: x for x in inv['unidades']}
    assert len(evidence['alteracoes_propostas']) == 9
    for change in evidence['alteracoes_propostas']:
        u = lookup[change['unidade']]
        p = tree.xpath(u['xpath'], namespaces=NS)[0]
        assert visible(p) == change['antes']
        assert len(change['depois']) <= 700
        assert not p.xpath('.//w:fldChar | .//w:instrText | .//w:hyperlink', namespaces=NS)
        replace_text(p, change['depois'])
        format_revised_prose(p, u['indice_paragrafo_xml'])
        assert visible(p) == change['depois']
        u.setdefault('revisoes_lote12', []).append(change)
        if u['id'] in ['U0189', 'U0208', 'U0210', 'U0279']:
            u['status_conteudo'] = 'conferida_correcao_incorporada_em_rascunho'
    parts['word/document.xml'] = etree.tostring(tree, xml_declaration=True, encoding='UTF-8', standalone=True)
    assert [k for k in parts if parts[k] != before[k]] == ['word/document.xml']
    backup = OUT / 'antes_lote12.docx'
    assert not backup.exists()
    copy2(draft, backup)
    temp = draft.with_suffix('.tmp.docx')
    with ZipFile(temp, 'w') as z:
        for info in infos:
            z.writestr(info, parts[info.filename])
    temp.replace(draft)
    h = hashlib.sha256(draft.read_bytes()).hexdigest()
    result = {'base': state['base'], 'sha256_base': state['sha256_base'], 'sha256_antes': digest,
              'sha256_apos_edicao': h, 'alteracoes': evidence['alteracoes_propostas'],
              'evidencia': 'leituras_liu_hariharan_xiao_lote12.json',
              'estado': 'incorporado_pendente_exportacao_e_inspecao'}
    record.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    invpath.write_text(json.dumps(inv, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    state.update(sha256_copia_trabalho_atual=h, estado_copia='rascunho_pendente_validacao_visual_lote12')
    (OUT / 'estado_meta.json').write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Nove unidades incorporadas, pendentes de exportação e inspeção.')


if __name__ == '__main__':
    main()
