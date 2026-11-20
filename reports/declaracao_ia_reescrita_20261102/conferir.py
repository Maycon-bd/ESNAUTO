from pathlib import Path
import hashlib, json, zipfile
from lxml import etree as E
from PIL import Image, ImageChops

B = Path(__file__).resolve().parent
R = B.parents[1]
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
base = R / 'reports/monografia/versoes/v011/MayconGarciaSilva_monografia_v011.docx'
work = R / 'reports/monografia/trabalho/declaracao_ia_reescrita_20261102.docx'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
with zipfile.ZipFile(base) as a, zipfile.ZipFile(work) as z:
    changed = [k for k in a.namelist() if a.read(k) != z.read(k)]
    assert changed == ['word/document.xml'], changed
    old = E.fromstring(a.read('word/document.xml')).find('w:body', NS)
    new = E.fromstring(z.read('word/document.xml')).find('w:body', NS)
    assert len(old) == len(new)
    altered = []
    for i, (x, y) in enumerate(zip(old, new)):
        if E.tostring(x) != E.tostring(y):
            txt = ''.join(x.xpath('.//w:t/text()', namespaces=NS))
            assert txt.startswith(('Na extração bibliográfica, utilizou-se', 'Em observância aos princípios', 'Fica certificado que não houve', 'Fase do TFC / Processo')), txt
            altered.append(i)
    assert len(altered) == 4, altered
    tables_old = old.findall('w:tbl', NS)
    tables_new = new.findall('w:tbl', NS)
    assert len(tables_old) == len(tables_new) == 15
    assert all(E.tostring(x) == E.tostring(y) for x, y in zip(tables_old[:-1], tables_new[:-1]))
    alltext = ''.join(new.xpath('.//w:t/text()', namespaces=NS))
    assert 'versões não informadas' not in alltext
    assert 'versão não informada' not in alltext
    assert alltext.count('Claude Opus 5.5') == 2
    assert alltext.count('Codex Sol 5.6') == 4

oldmap = json.loads((R / 'reports/declaracao_ia_integracao_20261102/mapa_final.json').read_text(encoding='utf-8-sig'))
newmap = json.loads((B / 'mapa_final.json').read_text(encoding='utf-8-sig'))
assert newmap['pages'] == oldmap['pages'] == 81
assert oldmap['items'] == newmap['items'], 'Mudou a paginação dos localizadores.'
images = B / 'word_final'
original = R / 'reports/declaracao_ia_integracao_20261102/word_final'
different = []
identical = []
for page in range(1, 82):
    with Image.open(images / f'page-{page}.png') as a, Image.open(original / f'page-{page}.png') as o:
        (different if ImageChops.difference(a.convert('RGB'), o.convert('RGB')).getbbox() else identical).append(page)
proof = {
    'base': 'v011', 'base_sha256': sha(base), 'trabalho_sha256': sha(work),
    'partes_alteradas': changed, 'elementos_de_corpo_alterados': altered,
    'tabelas_cientificas_preservadas_xml': 14, 'paginas': 81,
    'localizadores_preservados': len(newmap['items']),
    'paginas_identicas': identical, 'paginas_a_inspecionar': different,
    'declaracao_sha256': sha(B / 'entrega/Declaracao_responsabilidade_coletiva_Maycon_reescrita.docx')
}
(B / 'conferencia_final.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({k: proof[k] for k in ['paginas', 'localizadores_preservados', 'paginas_a_inspecionar']}, ensure_ascii=False))
