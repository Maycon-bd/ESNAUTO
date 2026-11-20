from pathlib import Path
import copy, hashlib, json, re, zipfile
from lxml import etree as E

B = Path(__file__).resolve().parent
R = B.parents[1]
O = B / 'entrega'
O.mkdir(parents=True, exist_ok=True)
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
def qn(t): return '{' + NS['w'] + '}' + t
def text(p): return ''.join(p.itertext()) if False else ''.join(p.xpath('.//w:t/text()', namespaces=NS))

intro = [
    'Declaramos que as ferramentas de inteligência artificial generativa relacionadas a seguir foram utilizadas como apoio ao desenvolvimento deste TFC. O registro de suas finalidades e da conferência humana realizada atende aos princípios de integridade científica mencionados na Portaria CNPq nº 2.664/2026.',
    'A autoria intelectual permanece humana. Os signatários assumem integralmente a responsabilidade pelo conteúdo apresentado, pela consistência das afirmações científicas e pela correção técnica do software, assim como pelo cumprimento das normas de integridade, de propriedade industrial e de direitos autorais.'
]
rows = [
    ['Extração bibliográfica', 'Script próprio em Python; Gemini 2.5 Flash; temperatura 0',
     'Registro preliminar das respostas ao formulário de extração a partir dos PDFs, com trecho de apoio, localização e justificativa.',
     'O autor conferiu pessoalmente os artigos consultados.'],
    ['Revisão e leitura do texto', 'Claude Opus 5.5 e Codex Sol 5.6',
     'Leitura assistida e sugestões de ajustes na linguagem e na organização de trechos da monografia.',
     'O autor confrontou o conteúdo com os artigos. O orientador apresentou correções no texto.'],
    ['Testes do projeto', 'Codex Sol 5.6',
     'Assistência na preparação e execução de testes e na interpretação das saídas obtidas.',
     'O autor executou testes diretamente e também com apoio do Codex.'],
    ['Formatação e material de defesa', 'Codex Sol 5.6',
     'Ajustes na apresentação do documento, verificações por scripts e elaboração de slides e roteiro.',
     'O autor avaliou as propostas e solicitou alterações; o orientador devolveu a monografia com correções.']
]
method = ('Na extração bibliográfica, empregou-se Gemini 2.5 Flash (temperatura 0), por script próprio em Python. '
          'Claude Opus 5.5 e Codex Sol 5.6 auxiliaram na revisão e leitura; apenas o Codex apoiou os testes. '
          'O autor conferiu os artigos pessoalmente e executou testes. O Anexo A detalha o uso de inteligência '
          'artificial generativa (IAG) e a conferência humana realizada.')

def set_paragraph(p, newtext, italic_script=False):
    # Preserve paragraph properties and the first run's typography.
    first_run = p.find('w:r', NS)
    rp = first_run.find('w:rPr', NS) if first_run is not None else None
    rp = copy.deepcopy(rp) if rp is not None else None
    for c in list(p):
        if c.tag != qn('pPr'): p.remove(c)
    for part in re.split(r'(\bscript\b)', newtext) if italic_script else [newtext]:
        if not part: continue
        r = E.SubElement(p, qn('r'))
        if rp is not None: r.append(copy.deepcopy(rp))
        if italic_script and part == 'script':
            rpr = r.find('w:rPr', NS)
            if rpr is None: rpr = E.SubElement(r, qn('rPr'))
            E.SubElement(rpr, qn('i'))
        t = E.SubElement(r, qn('t')); t.text = part
        t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')

def edit(source, target, monograph):
    changes = []
    with zipfile.ZipFile(source) as z:
        root = E.fromstring(z.read('word/document.xml'))
        body = root.find('w:body', NS)
        for p in body.findall('w:p', NS):
            old = text(p)
            if old.startswith('Em observância aos princípios de integridade científica'):
                set_paragraph(p, intro[0]); changes.append({'antes': old, 'depois': intro[0]})
            elif old.startswith('Fica certificado que não houve delegação'):
                set_paragraph(p, intro[1]); changes.append({'antes': old, 'depois': intro[1]})
            elif monograph and old.startswith('Na extração bibliográfica, utilizou-se'):
                set_paragraph(p, method, True); changes.append({'antes': old, 'depois': method})
        assert len(changes) == (3 if monograph else 2)
        tables = body.findall('w:tbl', NS)
        table = tables[-1]
        trs = table.findall('w:tr', NS)
        assert len(trs) == 5
        for tr, row in zip(trs[1:], rows):
            cells = tr.findall('w:tc', NS); assert len(cells) == 4
            for cell, newtext in zip(cells, row):
                ps = cell.findall('w:p', NS); assert len(ps) == 1
                changes.append({'antes': text(ps[0]), 'depois': newtext})
                set_paragraph(ps[0], newtext)
        with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as out:
            for info in z.infolist():
                out.writestr(info, E.tostring(root, encoding='UTF-8', xml_declaration=True, standalone=True)
                             if info.filename == 'word/document.xml' else z.read(info.filename))
    return changes

base = R / 'reports/monografia/versoes/v011/MayconGarciaSilva_monografia_v011.docx'
assert hashlib.sha256(base.read_bytes()).hexdigest() == '6ce846aec1d02f0ab1c6e575f822f082920331f8d7b6c444914bb45d0563ce4a'
work = R / 'reports/monografia/trabalho/declaracao_ia_reescrita_20261102.docx'
declbase = R / 'reports/declaracao_ia_integracao_20261102/entrega/Declaracao_responsabilidade_coletiva_Maycon.docx'
decl = O / 'Declaracao_responsabilidade_coletiva_Maycon_reescrita.docx'
changes = edit(base, work, True)
edit(declbase, decl, False)
(B / 'alteracoes.json').write_text(json.dumps({
    'base': 'v011', 'base_sha256': hashlib.sha256(base.read_bytes()).hexdigest(),
    'trabalho_sha256': hashlib.sha256(work.read_bytes()).hexdigest(),
    'declaracao_sha256': hashlib.sha256(decl.read_bytes()).hexdigest(),
    'confirmacao_autor': 'Modelos usados sempre foram do Claude Opus 5.5 e do Codex foi o Sol 5.6',
    'origem_modelos': 'Nomes informados pelo autor; não constituem identificação técnica independente por logs.',
    'alteracoes': changes}, ensure_ascii=False, indent=2), encoding='utf-8')

# Reuse the proven native Word QA pipeline without altering its historical files.
src = (R / 'reports/declaracao_ia_integracao_20261102/word_qa.ps1').read_text(encoding='utf-8-sig')
src = src.replace('declaracao_ia_integracao_20261102', B.name)
src = src.replace('trabalho\\declaracao_ia_20261102.docx', 'trabalho\\declaracao_ia_reescrita_20261102.docx')
src = src.replace('versoes\\v010\\MayconGarciaSilva_monografia_v010.docx', 'versoes\\v011\\MayconGarciaSilva_monografia_v011.docx')
src = src.replace('Declaracao_responsabilidade_coletiva_Maycon.docx', decl.name)
(B / 'word_qa.ps1').write_text(src, encoding='utf-8-sig')
src = (R / 'reports/declaracao_ia_integracao_20261102/renderizar.py').read_text(encoding='utf-8')
src = src.replace('trabalho/declaracao_ia_20261102.docx', 'trabalho/declaracao_ia_reescrita_20261102.docx')
src = src.replace('Declaracao_responsabilidade_coletiva_Maycon.docx', decl.name)
(B / 'renderizar.py').write_text(src, encoding='utf-8')
print('Cópias reescritas; modelos registrados como informados pelo autor.')
