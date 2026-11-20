"""Registra leitura da prova de Araújo e precisões editoriais, sem executar R."""
import hashlib
import json
from copy import deepcopy
from pathlib import Path
from zipfile import ZipFile
from lxml import etree
import incorporar_fechamento_integral_lote1 as helper

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'reports/fechamento_integral_20261029'

def read(p):
    return json.loads(p.read_text(encoding='utf-8'))

def save(p, value):
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    target = OUT / 'leitura_D02_araujo_lote6.json'
    assert not target.exists(), 'Registro já existe: não repetir a incorporação.'
    state = read(OUT / 'estado_meta.json')
    catalog = read(ROOT / 'docs/assistencia_monografia/versao_vigente.json')
    registry = next(v for v in catalog['versoes'] if v['id'] == catalog['vigente'])
    assert registry['id'] == state['base'] == 'v005'
    assert sha(ROOT / registry['arquivo']) == state['sha256_base']
    dest = ROOT / state['copia_trabalho']
    previous = sha(dest)
    assert previous == state['sha256_copia_trabalho_atual'] == 'da445d5b67022ad03c9ba66825e861264e828502834d1dbe28605304160fc5f2'
    manifest = read(OUT / 'manifesto_fontes.json')
    source = next(s for s in manifest if s['id'] == 'D02')
    assert sha(ROOT / source['arquivo']) == source['sha256'] == 'cbf3101a4e98dc4b09f9a43f4f555910a9aeffccc53faa4200335db20f2e24b2'
    inv = read(OUT / 'inventario_unidades.json')
    units = {u['id']: u for u in inv['unidades']}
    changes = {
        'U0244': 'Araújo et al. (2025) compararam MAE e RMSE como aptidão de um AG para ESNs com cinco distribuições. A prova consultada descreve retornos de fechamento da ITSA4 e variâncias diárias, com partição declarada de 60%/20%/20%. Esse protocolo difere da previsão do preço ajustado da PETR4 no ESNAUTO. A presente pesquisa adapta essa linha de trabalho, integra LHS e um operador antiestagnação inspirado no CHC. A preservação histórica parcial dos artefatos está descrita na Seção 3.8. Foi consultada a prova de autor; os metadados da edição final foram conferidos no editor.',
        'U0580': 'O Quadro 3 apresenta a codificação de 55 bits utilizada no ESNAUTO, com alocação e faixas conferidas no código. Araújo et al. (2025) também empregaram cromossomos de 55 bits para cinco hiperparâmetros, sem detalhar na prova consultada a repartição de bits. Cardoso et al. (2022a, p. 203) utilizaram valores fixos de 1,25 para o raio espectral, 0,2 para a taxa de vazamento e 10⁻⁸ para a regularização. Esses antecedentes fundamentam o método e devem ser distinguidos das configurações utilizadas nesta pesquisa.',
        'U0601': 'Descarta os estados iniciais na estimação de Wout.',
    }
    reasons = {
        'U0244': 'Individualizar tarefa, ativo e partição do antecedente; não equiparar retornos/variâncias da ITSA4 à previsão de preços ajustados da PETR4. Preserva o limite de acervo e a identificação da prova de autor.',
        'U0580': 'Reconhecer expressamente o antecedente dos 55 bits. As tabelas de valores encontrados no artigo não são limites de busca nem partição dos bits; estes foram conferidos nos códigos locais.',
        'U0601': 'Descrever o descarte efetivamente implementado, sem prometer que qualquer quantidade otimizada elimine todos os transientes dinâmicos.',
    }
    with ZipFile(dest) as z:
        infos = z.infolist()
        parts = {i.filename: z.read(i.filename) for i in infos}
    before = dict(parts)
    root = etree.fromstring(parts['word/document.xml'])
    pars = root.xpath('//w:p', namespaces=helper.NS)
    edits = []
    for uid, new in changes.items():
        u = units[uid]
        p = pars[u['indice_paragrafo_xml']]
        old = helper.visible(p)
        assert old == u['texto'], uid
        assert len(new) <= 700
        helper.replace_text(p, new)
        helper.format_revised_prose(p, u['indice_paragrafo_xml'])
        edits.append({'unidade': uid, 'antes': old, 'depois': new, 'motivo': reasons[uid]})
    parts['word/document.xml'] = etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)
    assert [k for k in parts if before[k] != parts[k]] == ['word/document.xml']
    tmp = dest.with_suffix('.tmp.docx')
    with ZipFile(tmp, 'w') as z:
        for i in infos:
            z.writestr(i, parts[i.filename])
    tmp.replace(dest)
    cells = deepcopy([c for c in read(OUT / 'matriz_lote4/matriz_recodificada.json')['decisoes'] if c['id'] == 'D02'])
    assert [c['codigo'] for c in cells] == ['?', 'D', 'D', '?', 'D']
    for c in cells:
        c['escopo_leitura'] = 'Prova local completa, PDF1–17, lida sequencialmente em blocos1–9e10–17; páginas1,4,7,8,10–14abertas visualmente. Inclui metadados e consultas de autor, tratados como conteúdo documental.'
    cells[0]['evidencia_e_limite'] = 'Cinco famílias associadas à ESN, sem individualização suficiente de sua geração em Win ou W na prova integral consultada. Não preencher por analogia com código próprio ou outros artigos.'
    cells[3]['evidencia_e_limite'] = 'Tabelas3–4comparam variantes ESN e métricas de aptidão. Referências a outros modelos não fornecem comparação quantitativa qualificadora com LSTM,GRUouTransformer nesta prova.'
    scopes = [
        {'unidade': 'U0220', 'conferido': 'Apenas antecedente AG+ESN+distribuições em séries da B3. Integrações próprias e cinco ondas exigem seus registros específicos.'},
        {'unidade': 'U0233', 'conferido': 'Cinco famílias e falta de individualização Win/W na prova Araújo. A atribuição a Sharma permanece com conferência própria.'},
        {'unidade': 'U0259', 'conferido': 'Somente oração sobre Araújo. Não conclui a leitura de Lampugnani ou da tese Cardoso.'},
        {'unidade': 'U0621', 'conferido': 'Ponderação40%/60%confirmada na provaPDF7–8; sinal e MAEs no código atual ga_engine.R227–315. Registro de parâmetros/erros em history_tracker.R88–184e matrizes de recordes em168–171. Não comprova identidade do código em cada execução histórica nem validade independente dos erros.'},
    ]
    record = {
        'base': state['base'], 'sha256_base': state['sha256_base'], 'sha256_rascunho_examinado': previous,
        'fonte_lida_integralmente': {**source, 'estado_leitura': 'leitura_integral_com_evidencias_visuais', 'leitura': 'PDF1–17lido integralmente em ordem, incluindo três páginas de metadados, treze do manuscrito e uma de consultas de autor.', 'paginas_visuais_abertas': [1,4,7,8,10,11,12,13,14]},
        'celulas_reexaminadas': cells, 'n_celulas_reexaminadas': 5, 'n_codigos_alterados': 0,
        'unidades_conferidas_sem_edicao': [{'unidade': 'U0258', 'diagnostico': 'condizente_com_limites_explicitos', 'evidencia': 'AraújoPDF4,7–11documenta antecedente financeiro com distribuições alternativas. O parágrafo formula questão/objetivo e não reivindica ineditismo ou isolamento causal.'}],
        'unidades_com_conferencia_parcial': scopes,
        'quadro3_conferencia': {
            'unidades': [f'U{i:04}' for i in range(581,613)],
            'alocacao_bits': [17,17,7,5,9], 'soma_bits': 55,
            'limites_numericos': {'a_sr': 'k/131071; k=0recebe7.62939453125e-6; positivos e<=1; grade discreta.', 'initLen': 'k+2,kentre0e127,resulta2a129.', 'reservatorio': 'k+2,kentre0e31,resulta2a33.', 'regularizacao': '(k/511+1e-4)*(1e-4-1e-6),kentre0e511:9.9e-9a9.90099e-5. Limites aproximados do Quadro3conferem.'},
            'fontes_codigo': [{'arquivo': p, 'sha256': sha(ROOT / p)} for p in ['app/utils/ga_engine.R', 'Scripts/acoes_petr4_esn.R', 'app/utils/history_tracker.R']],
            'trechos_lidos': 'Decodificador atual227–238e legado212–237; atual248–265para descarte e Ridge; atual288–315para aptidão; atual480–543para chamada de persistência; history_tracker.R1–200. Não foi executado ou declarado lido o restante do software.',
            'fontes_conceituais': 'Jaeger2001/2007eRBras2022já conferidos; AraújoPDF7–11neste lote. A citação conjunta não atribui os intervalos a tabelas de resultados do artigo.',
            'limite': 'Compatibilidade estática dos códigos examinados; não prova que toda execução histórica usou esses bytes. Não houve treinamento, busca ou novo teste DM.',
        },
        'metadados_R02': {
            'url_editor': 'https://link.springer.com/chapter/10.1007/978-3-031-77738-7_26',
            'verificacao': 'Página oficial aberta e lida: título, sete autores, livro IDEAL2024,editorJulian,volume15347,p315–327,SpringerCham,DOI conferem. Cite this paper e copyright indicam2025; First Online/Published indica14November2024. A monografia usa o ano da edição2025, mantido.',
            'limite': 'Manuscrito integral conferido na prova local; não se declara acesso ao texto integral final, disponível por assinatura. A página pública permite metadados/resumo, não comprova identidade byte a byte entre versões.'
        },
        'ressalvas_fontes': [
            'PDF8chama log-retornos, mas a fórmula mostrada é retorno simples. A monografia usa a designação genérica retornos nesta comparação.',
            'PDF8declara60/20/20e contagens3335/1118/1118. A soma5571confere; os percentuais são nominais/aproximados. Não transferir contagens ou partições para PETR4.',
            'O período declarado ITSA4estende-se a2023, embora o BovDB citado anuncie1995–2020. A monografia não usa essa atribuição para provar origem/atualização da sua série.',
            'Abstract, prosa, Figura2e conclusão divergem sobre famílias destacadas. Não transportar ranking, causalidade ou significância sem teste para a monografia.',
            'Tabelas1–2apresentam valores encontrados em execuções, não intervalos completos de busca ou a alocação dos55bits.',
            'A proporção40/60é documentada; não constitui prova de que toda a metodologia ou código dos estudos seja idêntico.',
        ],
        'alteracoes_word': edits, 'sha256_copia_apos_edicao': sha(dest),
        'estado': 'leitura_e_correcao_incorporada_pendente_exportacao_nativa',
    }
    save(target, record)
    source.update(estado_leitura='leitura_integral_com_evidencias_visuais', log_leitura=[{'registro': target.name, 'metodo': record['fonte_lida_integralmente']['leitura'], 'paginas_visuais_abertas': [1,4,7,8,10,11,12,13,14]}])
    save(OUT / 'manifesto_fontes.json', manifest)
    units['U0258'].update(status_conteudo='conferida_no_texto_base', afirmacoes=record['unidades_conferidas_sem_edicao'], evidencia_integral=target.name)
    for item in scopes:
        units[item['unidade']].update(status_conteudo='conferencia_parcial_com_escopo_explicito', evidencias_parciais_lote6=[item])
    for n,c in enumerate(cells):
        u=units[f'U{299+n:04}'];assert u['texto'] == c['codigo']
        u.update(status_conteudo='decisao_de_celula_conferida_no_escopo_integral_da_fonte', afirmacoes=[c])
    for n in range(581,613):
        units[f'U{n:04}'].update(status_conteudo='conferida_com_codigo_e_fontes_conceituais', evidencia_integral=target.name, limite='Conteúdo técnico/atribuição; forma e preservação visual conferidas no checkpoint do lote.')
    for edit in edits:
        units[edit['unidade']].update(status_conteudo='reexaminada_correcao_incorporada_em_rascunho', afirmacoes=[edit], evidencia_integral=target.name)
    save(OUT / 'inventario_unidades.json', inv)
    refs=read(OUT / 'inventario_referencias.json')
    ref=next(r for r in refs['referencias'] if r['id']=='R02')
    ref.update(status_conferencia_integral='fonte_lida_decisoes_por_afirmacao_registradas', fontes_primarias=[record['fonte_lida_integralmente']], diagnosticos_por_afirmacao=[target.name], limites_restantes='Somente prova de autor integral, metadados finais oficiais; afirmações próprias/mistas e similaridade mantêm conferências específicas.')
    save(OUT / 'inventario_referencias.json', refs)
    assert 'D02' not in state['fontes_com_texto_integral_lido_nesta_meta']
    state['fontes_com_texto_integral_lido_nesta_meta'].append('D02')
    state.update(sha256_copia_trabalho_atual=sha(dest), correcoes_word_incorporadas_nesta_meta=19, revalidacao_de_celulas_registrada=45, ultimo_registro_de_leitura=str(target.relative_to(ROOT)), checkpoint_mais_recente=str(target.relative_to(ROOT)), conferencia_visual_checkpoint='Lote6aguarda exportação; dois parágrafos e uma célula do Quadro3alterados. Nenhum resultado experimental alterado.', unidades_com_conferencia_iniciada=sum(u['status_conteudo']!='nao_examinada_nesta_meta' for u in inv['unidades']))
    save(OUT / 'estado_meta.json', state)
    print('Araújo integral registrado; cinco células confirmadas; dois parágrafos e uma célula precisados. Exportação pendente.')

if __name__ == '__main__':
    main()
