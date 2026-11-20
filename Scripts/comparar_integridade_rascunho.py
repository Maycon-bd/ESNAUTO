"""Triagem textual local do Word corrente, sem alterar fontes nem auditorias antigas."""
from __future__ import annotations
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import re
import unicodedata
from difflib import SequenceMatcher
from docx import Document
from docx.table import Table

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / 'reports/auditoria_citacoes_integridade_20261028'
OUTPUT_ROOT = ROOT / 'reports/correcao_parecer_integridade'
W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def words(text):
    plain = ''.join(c for c in unicodedata.normalize('NFD', text.casefold())
                    if not unicodedata.combining(c))
    return re.findall(r'\w+', plain)


def all_paragraphs(doc):
    return doc.paragraphs + [p for t in doc.tables for r in t.rows
                             for c in r.cells for p in c.paragraphs]


def targets(doc, include_tables=True):
    """Percorre corpo e tabelas em ordem; índices são da cópia atual, não v001."""
    para_map = {p._p: (i, p) for i, p in enumerate(doc.paragraphs)}
    table_map = {t._tbl: i for i, t in enumerate(doc.tables)}
    active = False
    saw_references = False
    section = ''
    items = []
    for child in doc.element.body:
        if child.tag == W + 'p':
            index, p = para_map[child]
            if words(p.text) in (['introducao'], ['1', 'introducao']):
                active = True
            if words(p.text) == ['referencias']:
                saw_references = True
                active = False
            if not active:
                continue
            if p.style.name in ('TITULO TCC', 'SEÇÃO TCC', 'SUBÇÃO 2'):
                section = p.text
            items.append({'id': f'P_atual{index:04d}', 'secao': section,
                          'texto': p.text, 'tokens': words(p.text)})
        elif child.tag == W + 'tbl' and active and include_tables:
            table = Table(child, doc)
            assert not table._tbl.findall('.//' + W + 'tbl'), 'Tabela aninhada exige inspeção adicional.'
            seen = set()
            for ri, row in enumerate(table.rows):
                for ci, cell in enumerate(row.cells):
                    if cell._tc in seen:
                        continue
                    seen.add(cell._tc)
                    for pi, p in enumerate(cell.paragraphs):
                        items.append({'id': f'T_atual{table_map[child]:02d}/L{ri}/C{ci}/P{pi}',
                                      'secao': section, 'texto': p.text,
                                      'tokens': words(p.text)})
    assert saw_references and items, 'Limites da parte textual não identificados.'
    return items


def load_sources():
    baseline = json.loads((AUDIT / 'manifesto.json').read_text(encoding='utf8'))
    assert len(baseline[1:]) == 39, 'O corpus histórico esperado mudou.'
    sources = []
    for entry in baseline[1:]:
        path = Path(entry['path']).resolve()
        assert sha(path) == entry['sha256'], f'Fonte mudou desde a auditoria: {path}'
        if path.suffix.lower() == '.docx':
            text = '\n'.join(f'[L{i:04d}] {p.text}'
                             for i, p in enumerate(all_paragraphs(Document(path))))
            extraction = 'Extração em memória, mesma ordem do comparador original.'
        elif path.parent.name == 'Artigos citados':
            source_text = AUDIT / (path.stem + '.txt')
            text = source_text.read_text(encoding='utf8')
            extraction = str(source_text)
        elif path.suffix.lower() == '.pdf':
            name = 'Cardoso_tese.txt' if path.name == 'tese_Fabian_Correa_Cardoso.pdf' else 'guia.txt'
            source_text = AUDIT / name
            text = source_text.read_text(encoding='utf8')
            extraction = str(source_text)
        else:
            text = path.read_text(encoding='utf8')
            extraction = str(path)
        assert len(words(text)) == entry['tokens_extraidos'], f'Extração diverge da auditoria: {path}'
        segments = []
        for segment in re.split(r'(?=\[PÁGINA PDF \d+\]|\[L\d+\])', text):
            marker = re.search(r'\[(PÁGINA PDF \d+|L\d+)\]', segment)
            clean = re.sub(r'\[(?:PÁGINA PDF \d+|L\d+)\]', '', segment)
            segments.append((marker[1] if marker else 'sem paginação', words(clean)))
        sources.append({'arquivo': str(path), 'sha256': sha(path),
                        'extracao': extraction,
                        'sha256_texto_extraido': hashlib.sha256(text.encode('utf8')).hexdigest(),
                        'tokens_sem_marcadores': sum(len(w) for _, w in segments),
                        'segmentos': segments})
    return sources


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--docx', required=True)
    parser.add_argument('--saida', required=True)
    parser.add_argument('--pares-lampugnani', action='store_true')
    args = parser.parse_args()
    docx = (ROOT / args.docx).resolve()
    out = (ROOT / args.saida).resolve()
    assert out.is_relative_to(OUTPUT_ROOT.resolve()) and out != OUTPUT_ROOT.resolve()
    assert not out.exists(), 'Preservar relatório anterior; escolher outra pasta de saída.'
    assert docx.suffix.lower() == '.docx'
    input_hash = sha(docx)
    items = targets(Document(docx))
    sources = load_sources()
    index = defaultdict(set)
    n = 8
    for si, source in enumerate(sources):
        for location, tokens in source['segmentos']:
            for start in range(len(tokens) - n + 1):
                index[tuple(tokens[start:start + n])].add((si, location))
    windows = []
    groups = defaultdict(list)
    by_id = {p['id']: p for p in items}
    for target in items:
        for start in range(len(target['tokens']) - n + 1):
            hits = index.get(tuple(target['tokens'][start:start + n]))
            if hits:
                windows.append({'alvo': target['id'], 'inicio_token': start,
                                'trecho_normalizado': ' '.join(target['tokens'][start:start+n]),
                                'fontes': [{'fonte': si, 'localizador': loc} for si, loc in sorted(hits)]})
                for si, loc in hits:
                    groups[(target['id'], si, loc)].append(start)
    blocks = []
    for (target_id, si, loc), starts in sorted(groups.items()):
        runs = []
        for start in sorted(set(starts)):
            if runs and start <= runs[-1][1]:
                runs[-1][1] = max(runs[-1][1], start + n)
            else:
                runs.append([start, start + n])
        p = by_id[target_id]
        for start, end in runs:
            blocks.append({'id': f'B{len(blocks)+1:03d}', 'alvo': target_id,
                           'secao': p['secao'], 'texto_alvo': p['texto'],
                           'fonte': sources[si]['arquivo'], 'localizador_fonte': loc,
                           'inicio_token': start, 'fim_token_exclusivo': end,
                           'trecho_normalizado': ' '.join(p['tokens'][start:end]),
                           'estado': 'requer_interpretacao_humana'})
    pair_result = None
    if args.pares_lampugnani:
        lamp = ROOT / 'MatheusTeixeiraLampugnani_monografia (1).docx'
        a = [p for p in items if p['id'].startswith('P_atual') and len(p['tokens']) >= 15]
        b = [p for p in targets(Document(lamp), include_tables=False) if p['id'].startswith('P_atual') and len(p['tokens']) >= 15]
        pairs = []
        for p in a:
            for q in b:
                matcher = SequenceMatcher(None, p['tokens'], q['tokens'], autojunk=False)
                if matcher.real_quick_ratio() < 0.4 or matcher.quick_ratio() < 0.4:
                    continue
                ratio = matcher.ratio()
                if ratio >= 0.4:
                    pairs.append({'alvo': p['id'], 'fonte': q['id'], 'razao_tokens': ratio,
                                  'texto_alvo': p['texto'], 'texto_fonte': q['texto']})
        pair_result = {'alvo_sha256': input_hash, 'fonte': str(lamp), 'fonte_sha256': sha(lamp),
                       'n_paragrafos_alvo': len(a), 'n_paragrafos_fonte': len(b),
                       'n_pares_examinados': len(a) * len(b), 'limiar': 0.4,
                       'metodo': 'SequenceMatcher em tokens normalizados, autojunk=False; '
                                 'corpo entre Introdução e Referências, parágrafos15+ palavras. '
                                 'Os filtros quick_ratio são limites superiores.',
                       'limite': 'Heurística de triagem, não escore de originalidade ou detector semântico.',
                       'pares': pairs}
    assert sha(docx) == input_hash, 'O Word mudou durante a análise.'
    result = {'alvo': str(docx), 'sha256_alvo': input_hash, 'sha256_script': sha(Path(__file__)),
              'manifesto_original': str(AUDIT / 'manifesto.json'),
              'sha256_manifesto_original': sha(AUDIT / 'manifesto.json'),
              'n_fontes': len(sources), 'n_paragrafos_examinados': len(items),
              'janela_palavras': n, 'janelas_coincidentes': len(windows),
              'n_blocos_fonte_localizador': len(blocks),
              'limites': 'Corpo entre Introdução e Referências e tabelas nesse intervalo. '
                        'Coincidência lexical normalizada, não percentual de plágio. '
                        'Sem detecção semântica, tradução, OCR integral, internet ou fontes privadas. '
                        'Não inclui o conteúdo de fontes eletrônicas adicionais ausentes no corpus39. '
                        'A interpretação exige conferir contexto e atribuição. Índices são da cópia atual.',
              'fontes_sem_texto_indexavel': [s['arquivo'] for s in sources if not s['tokens_sem_marcadores']],
              'fontes': [{k: v for k, v in s.items() if k != 'segmentos'} for s in sources],
              'blocos': blocks, 'janelas': windows}
    lines = ['# Triagem textual do rascunho atual', '', f'Alvo: `{docx}`.',
             f'SHA256: `{input_hash}`.', '',
             f'{len(sources)} fontes; {len(windows)} janelas de oito palavras; '
             f'{len(blocks)} blocos por fonte/localizador após agrupar sobreposições.', '', result['limites'], '']
    for block in blocks:
        lines += [f"## {block['id']} — {block['alvo']}", '',
                  f"Seção: {block['secao']}.", f"Fonte: `{Path(block['fonte']).name}`, {block['localizador_fonte']}.",
                  '', f"Trecho coincidente normalizado: {block['trecho_normalizado']}", '',
                  'Contexto do alvo: ' + block['texto_alvo'], '',
                  'Interpretação: pendente; não classificar automaticamente como plágio.', '']
    out.mkdir(parents=True, exist_ok=False)
    (out / 'triagem.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf8')
    (out / 'triagem.md').write_text('\n'.join(lines)+'\n', encoding='utf8')
    if pair_result is not None:
        (out / 'pares_lampugnani.json').write_text(json.dumps(pair_result, ensure_ascii=False, indent=2)+'\n', encoding='utf8')
        print(f"Pares Lampugnani: {pair_result['n_pares_examinados']} examinados; {len(pair_result['pares'])} acima do limiar.")
    print(f'{len(sources)} fontes; {len(windows)} janelas; {len(blocks)} blocos. Saída: {out}')


if __name__ == '__main__':
    main()
