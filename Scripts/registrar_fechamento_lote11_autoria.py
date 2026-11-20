"""Harmoniza chamadas de oito obras com autoria conferida nas fontes originais."""
from pathlib import Path
from zipfile import ZipFile
from shutil import copy2
import hashlib
import json
import re
from lxml import etree
from incorporar_fechamento_integral_lote1 import visible, replace_text, format_revised_prose, NS

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'reports/fechamento_integral_20261029'
DEST = ROOT / 'reports/monografia/trabalho/fechamento_integral_20261029.docx'

# Somente autores já conferidos em leituras integrais. Demais obras continuam
# sujeitas à conferência de identidade, conteúdo e chamada nos lotes seguintes.
FORMS = [
    ('Vishwas', '2025', 'Vishwas, Usha e Sangeetha', 'Vishwas; Usha; Sangeetha', 'D30'),
    ('Hassaan', '2025', 'Hassaan, Yacoub e Said', 'Hassaan; Yacoub; Said', 'D14'),
    ('Soltani', '2022', 'Soltani, Benmohamed e Ltifi', 'Soltani; Benmohamed; Ltifi', 'D24'),
    ('Tian', '2024', 'Tian e Pei', 'Tian; Pei', 'D27'),
    ('Sun', '2021', 'Sun et al.', 'Sun et al.', 'D26'),
    ('Sharma', '2025', 'Sharma et al.', 'Sharma et al.', 'D23'),
    ('Ecer', '2020', 'Ecer et al.', 'Ecer et al.', 'D12'),
    ('Cardoso', '2022a', 'Cardoso, Berri e Mattos', 'Cardoso; Berri; Mattos', 'SUP_CARDOSO_RBRAS'),
]


def main():
    logpath = OUT / 'incorporacao_autoria_lote11.json'
    assert not logpath.exists(), 'Lote já registrado; não reaplicar.'
    state = json.loads((OUT / 'estado_meta.json').read_text(encoding='utf-8'))
    digest = hashlib.sha256(DEST.read_bytes()).hexdigest()
    assert digest == state['sha256_copia_trabalho_atual'] == '4d8ad77d6266568f21d1593e1026c4f6a567c439749daafe44b4e6a6ed49efad'
    registry = json.loads((ROOT / 'docs/assistencia_monografia/versao_vigente.json').read_text(encoding='utf-8'))
    assert registry['vigente'] == state['base'] == 'v005'
    base = next(x for x in registry['versoes'] if x['id'] == registry['vigente'])
    assert hashlib.sha256((ROOT / base['arquivo']).read_bytes()).hexdigest() == state['sha256_base']
    with ZipFile(DEST) as z:
        infos = z.infolist()
        parts = {i.filename: z.read(i.filename) for i in infos}
    before = dict(parts)
    tree = etree.fromstring(parts['word/document.xml'])
    invpath = OUT / 'inventario_unidades.json'
    inv = json.loads(invpath.read_text(encoding='utf-8'))
    changes = []
    for u in inv['unidades']:
        if u['parte'] != 'word/document.xml' or int(u['id'][1:]) > 970:
            continue  # referências não são chamadas autor-data
        nodes = tree.xpath(u['xpath'], namespaces=NS)
        assert len(nodes) == 1
        p = nodes[0]
        old = visible(p)
        new = old
        sources = []
        for author, year, narrative, parenthetical, sid in FORMS:
            pattern = re.escape(author) + r'(?:\s+et al\.)?'
            newer = re.sub(r'\b' + pattern + r'\s*\(' + year + r'(?=[,)])', narrative + ' (' + year, new)
            newer = re.sub(r'\b' + pattern + r',\s*' + year + r'(?=[,)])', parenthetical + ', ' + year, newer)
            if newer != new:
                sources.append(sid)
                new = newer
        # A inclusão de coautores muda o sujeito, preservando o conteúdo afirmado.
        for a, b in [
            ('Sun et al. (2021) comparou', 'Sun et al. (2021) compararam'),
            ('e reportou menores erros', 'e reportaram menores erros'),
            ('Sharma et al. (2025) avaliou', 'Sharma et al. (2025) avaliaram'),
            ('Sharma et al. (2025), por outro lado, apresenta', 'Sharma et al. (2025), por outro lado, apresentam'),
            ('Sharma et al. (2025) empregou', 'Sharma et al. (2025) empregaram'),
            ('Tian e Pei (2024) empregou', 'Tian e Pei (2024) empregaram'),
            ('Ecer et al. (2020) comparou', 'Ecer et al. (2020) compararam'),
        ]:
            if sources:
                new = new.replace(a, b)
        if new == old:
            continue
        assert len(new) <= 700, (u['id'], len(new))
        assert not p.xpath('.//w:fldChar | .//w:instrText | .//w:hyperlink | .//m:oMath', namespaces={**NS, 'm': 'http://schemas.openxmlformats.org/officeDocument/2006/math'})
        replace_text(p, new)
        format_revised_prose(p, u['indice_paragrafo_xml'])
        changes.append({'unidade': u['id'], 'antes': old, 'depois': new, 'fontes': sources, 'motivo': 'Autoria completa para duas/três pessoas, et al. para quatro ou mais; concordância do sujeito plural. Manual UniRV2025,p195–196; Guia FASOFT,p71.'})
        u.setdefault('revisoes_formais', []).append({'registro': logpath.name, 'texto_atual': new})
    assert len(changes) == 27, [(x['unidade'], x['depois']) for x in changes]
    parts['word/document.xml'] = etree.tostring(tree, xml_declaration=True, encoding='UTF-8', standalone=True)
    assert [k for k in parts if parts[k] != before[k]] == ['word/document.xml']
    backup = OUT / 'antes_autoria_lote11.docx'
    assert not backup.exists()
    copy2(DEST, backup)
    temp = DEST.with_suffix('.tmp.docx')
    with ZipFile(temp, 'w') as z:
        for info in infos:
            z.writestr(info, parts[info.filename])
    temp.replace(DEST)
    record = {'base': state['base'], 'sha256_base': state['sha256_base'], 'sha256_antes': digest,
              'sha256_apos_edicao': hashlib.sha256(DEST.read_bytes()).hexdigest(), 'alteracoes': changes,
              'regra_primaria': 'fontes_suplementares/UniRV_2025_citacoes_p195_197.pdf',
              'escopo': 'Oito obras identificadas; não é aprovação global das chamadas ou dos metadados de cinquenta referências.',
              'resultados_experimentais_preservados': True, 'estado': 'incorporado_pendente_exportacao_e_inspecao'}
    logpath.write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    invpath.write_text(json.dumps(inv, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    state.update(sha256_copia_trabalho_atual=record['sha256_apos_edicao'], estado_copia='rascunho_pendente_validacao_visual_lote11')
    (OUT / 'estado_meta.json').write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'{len(changes)} unidades de autoria corrigidas, pendentes de validação visual.')


if __name__ == '__main__':
    main()
