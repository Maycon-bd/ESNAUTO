"""Registra leituras integrais e corrige a identificação dos ativos de Ribeiro."""
from pathlib import Path
from zipfile import ZipFile
from shutil import copy2
from lxml import etree
import hashlib
import json
from incorporar_fechamento_integral_lote1 import visible, replace_text, NS

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'reports/fechamento_integral_20261029'


def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    record = OUT / 'incorporacao_lote13.json'
    assert not record.exists(), 'Não reaplicar.'
    state = json.loads((OUT / 'estado_meta.json').read_text(encoding='utf-8'))
    draft = ROOT / state['copia_trabalho']
    digest = hashlib.sha256(draft.read_bytes()).hexdigest()
    assert digest == state['sha256_copia_trabalho_atual'] == 'f7377019848a9ffc69278210a02051003fd7f7d347e0187a8e98b3f2d27b0235'
    reg = json.loads((ROOT / 'docs/assistencia_monografia/versao_vigente.json').read_text(encoding='utf-8'))
    assert reg['vigente'] == state['base'] == 'v005'
    base = next(x for x in reg['versoes'] if x['id'] == reg['vigente'])
    assert hashlib.sha256((ROOT / base['arquivo']).read_bytes()).hexdigest() == state['sha256_base']
    manifest = json.loads((OUT / 'manifesto_fontes.json').read_text(encoding='utf-8'))
    readings = []
    for sid, count, pages in [('D29', 13, [1,2,4,6,8,9,10]), ('D32', 14, [1,4,6,7,10,11,12]), ('D34', 15, [1,5,7,9,12,13,14])]:
        source = next(x for x in manifest if x['id'] == sid)
        assert hashlib.sha256(Path(source['arquivo']).read_bytes()).hexdigest() == source['sha256']
        readings.append({'id': sid, 'arquivo': source['arquivo'], 'sha256': source['sha256'],
                         'paginas_textuais_lidas': list(range(1, count+1)), 'paginas_visuais_inspecionadas': pages})
    with ZipFile(draft) as z:
        infos = z.infolist()
        parts = {i.filename: z.read(i.filename) for i in infos}
    tree = etree.fromstring(parts['word/document.xml'])
    ip = OUT / 'inventario_unidades.json'
    inv = json.loads(ip.read_text(encoding='utf-8'))
    units = {x['id']: x for x in inv['unidades']}
    p = tree.xpath(units['U0246']['xpath'], namespaces=NS)[0]
    before = visible(p)
    assert before.count('três ações da Nasdaq') == 1
    after = before.replace('três ações da Nasdaq', 'CAT, EBAY e MSFT')
    assert len(after) <= 700
    assert not p.xpath('.//w:fldChar | .//w:instrText | .//w:hyperlink', namespaces=NS)
    replace_text(p, after)
    assert visible(p) == after
    change = {'unidade': 'U0246', 'antes': before, 'depois': after,
              'motivo': 'A CAT era listada na NYSE; o próprio artigo usa classificação Nasdaq inadequada. Manter os ativos sem reproduzir essa classificação.'}
    units['U0246'].setdefault('revisoes_lote13', []).append(change)
    for uid in ['U0205','U0206','U0209','U0231','U0246','U0247','U0248']:
        units[uid]['status_conteudo'] = 'conferida_correcao_incorporada_em_rascunho' if uid == 'U0246' else 'conferida_sem_alteracao_lote13'
    parts['word/document.xml'] = etree.tostring(tree, xml_declaration=True, encoding='UTF-8', standalone=True)
    backup = OUT / 'antes_lote13.docx'
    assert not backup.exists()
    copy2(draft, backup)
    temp = draft.with_suffix('.tmp.docx')
    with ZipFile(temp, 'w') as z:
        for info in infos:
            z.writestr(info, parts[info.filename])
    temp.replace(draft)
    h = hashlib.sha256(draft.read_bytes()).hexdigest()
    cells = json.loads((OUT / 'matriz_lote4/matriz_recodificada.json').read_text(encoding='utf-8'))['decisoes']
    reviewed = [dict(x, estado_lote13='confirmado_apos_leitura_integral') for x in cells if x['id'] in ['D29','D32','D34'] and (x['id'], x['dimensao']) != ('D29','P4')]
    assert len(reviewed) == 14
    evidence = {'base': state['base'], 'sha256_base': state['sha256_base'], 'sha256_rascunho_examinado': digest,
        'fontes_lidas_integralmente': readings, 'celulas_reexaminadas': reviewed, 'n_celulas_reexaminadas': 14,
        'n_codigos_alterados': 0, 'afirmacoes_conferidas': ['U0205','U0206','U0209','U0231','U0247','U0248'],
        'alteracoes_propostas': [change],
        'pendencia_de_conciliacao': {'id': 'D29', 'dimensao': 'P4', 'codigo_atual': '?',
            'localizador': 'PDF 2, introdução e Tabela 1',
            'evidencia': 'Identifica LSTM-GARCH de Kim e Won (2018) e apresenta MSE 0.00149 para KOSPI200 na tabela retrospectiva. A justificativa anterior cobria apenas comparadores próprios e omitia esse quadro.',
            'decisao_pendente': 'Conciliar se catálogo quantitativo heterogêneo constitui comparação secundária S nos critérios atuais; não concluir ausência de LSTM nem promover a matriz sem decidir.'},
        'conferencia_externa_CAT': {'titulo': 'Caterpillar Celebrates 90 Years on the New York Stock Exchange', 'data': '2019-12-17',
            'url': 'https://www.caterpillar.com/en/news/corporate-press-releases/h/caterpillar-celebrates-90-years-on-the-nyse.html',
            'fato_confirmado': 'Comunicado oficial identifica CAT como NYSE e informa listagem iniciada em 2/12/1929.',
            'uso': 'Justifica retirar classificação Nasdaq; não foi acrescentada nova referência à monografia.'},
        'ressalvas_fontes': [
            'D29: Uniforme é explícita para Win, recorrentes e realimentação; não individualiza intervalo. Normalização descrita com extremos de treino e partição por ativos, não supor divisão temporal interna por ativo.',
            'D29: equação 10 imprime 1/(1-exp(-x)); equações 17–22 imprimem mínimo menos mínimo no denominador. Confirmado visualmente em PDF 4/8. Não copiar essas expressões como fórmulas corretas; não são reproduzidas nos trechos conferidos.',
            'D32: Uniforme de Win não é lei do reservatório, que usa adjacência. Wout é ajustado por RMSProp, não Ridge. Tabela 5 compara RNN/LSTM próprios; tabelas 6/7 usam números de outros estudos em comparação separada.',
            'D32: tabela 5 mostra melhores RMSE em quatro índices e MAE em três, mas conclusão menciona seis e dois. A monografia não reproduz essas contagens. Datas/amostras também divergem entre narrativa e tabelas; não importá-las sem ressalva.',
            'D34: Gaussiana refere-se à matriz de medição Phi, não a Win/W. Valores fixos e OMP não comprovam seleção de hiperparâmetros ESN. P3 documenta operações; P5 identifica conjunto de 200 ações/SSE, sem lista de tickers.',
            'D34: z-score não garante normalidade; números de Remark 2 divergem da tabela 3. Melhorias ESN/CS-ESN não provam preservação geral de picos/caos ou comparação com LSTM. Essas extrapolações não são adotadas.'
        ], 'estado': 'leituras_concluidas_conciliacao_P4_Ribeiro_pendente_rascunho_aguarda_QA', 'sha256_rascunho_apos_correcao': h}
    dump(OUT / 'leituras_ribeiro_wang_zhang_lote13.json', evidence)
    dump(record, {'base': state['base'], 'sha256_base': state['sha256_base'], 'sha256_antes': digest,
                  'sha256_apos_edicao': h, 'alteracoes': [change], 'estado': 'incorporado_pendente_exportacao_e_inspecao'})
    for sid in ['D29','D32','D34']:
        assert sid not in state['fontes_com_texto_integral_lido_nesta_meta']
        state['fontes_com_texto_integral_lido_nesta_meta'].append(sid)
    state.update(sha256_copia_trabalho_atual=h, estado_copia='rascunho_pendente_validacao_visual_lote13',
                 fontes_corpus34_lidas_integralmente=25, revalidacao_de_celulas_registrada=119,
                 correcoes_word_incorporadas_nesta_meta=54,
                 ultimo_registro_de_leitura=str(OUT.relative_to(ROOT) / 'leituras_ribeiro_wang_zhang_lote13.json'),
                 proxima_passagem='Conciliar P4 de Ribeiro à luz da Tabela 1 e atualizar matriz/agregados se necessário. Continuar nove obras do corpus ainda sem leitura integral nesta meta e referências suplementares; fechar unidades restantes, similaridade/atribuição, Guia e registro final. U0231 fechada quanto às três fontes.')
    dump(ip, inv)
    dump(OUT / 'estado_meta.json', state)
    print('Uma unidade corrigida; três leituras integrais registradas; P4 de Ribeiro permanece para conciliação explícita.')


if __name__ == '__main__':
    main()
