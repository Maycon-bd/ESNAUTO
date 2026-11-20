"""Conferência documental de duas fontes e incorporação de três precisões."""
from copy import deepcopy
from zipfile import ZipFile
from lxml import etree
from registrar_fechamento_lote6_araujo import ROOT, OUT, read, save, sha, helper

def main():
    target = OUT / 'leituras_sharma_duttilo_lote7.json'
    assert not target.exists()
    state = read(OUT / 'estado_meta.json')
    catalog = read(ROOT / 'docs/assistencia_monografia/versao_vigente.json')
    base = next(v for v in catalog['versoes'] if v['id'] == catalog['vigente'])
    assert base['id'] == state['base'] == 'v005'
    assert sha(ROOT / base['arquivo']) == state['sha256_base']
    dest = ROOT / state['copia_trabalho']
    previous = sha(dest)
    assert previous == state['sha256_copia_trabalho_atual'] == '05333a74f190adc9cf7cc18387b502e9ff2073021147a71195863a1555be2ddc'
    manifest = read(OUT / 'manifesto_fontes.json')
    inv = read(OUT / 'inventario_unidades.json')
    units = {u['id']: u for u in inv['unidades']}
    matrix = read(OUT / 'matriz_lote4/matriz_recodificada.json')
    sources, cells = [], []
    for sid, pages, visuals, method, start, codes in [
        ('D23',15,list(range(1,16)),'Todas as 15 páginas abertas e lidas visualmente; texto extraído das páginas 1–5 e 7–15 lido como apoio. A camada textual adicional da página 6 não foi usada como evidência.',425,['?','D','D','?','D']),
        ('D10',6,[3,4,5,6],'Texto completo das seis páginas lido; páginas 3–6 abertas visualmente para fórmulas, aplicação, tabelas e figura.',353,['-','-','D','-','D']),
    ]:
        source = next(x for x in manifest if x['id'] == sid)
        assert source['paginas'] == pages and sha(ROOT / source['arquivo']) == source['sha256']
        cs = deepcopy([c for c in matrix['decisoes'] if c['id'] == sid])
        assert [c['codigo'] for c in cs] == codes
        for i,c in enumerate(cs):
            assert units[f'U{start+i:04}']['texto'].replace('—','-') == c['codigo']
            c['escopo_leitura'] = method
            c['unidade'] = f'U{start+i:04}'
        entry = {**deepcopy(source), 'estado_leitura':'leitura_integral_com_evidencias_visuais', 'log_leitura':[{'registro':target.name,'metodo':method,'paginas_visuais_abertas':visuals}]}
        sources.append(entry)
        cells.extend(cs)
    book = read(OUT / 'fontes_suplementares/SIS2022_Pearson_final_origem.json')
    assert sha(ROOT / book['extrato']) == book['sha256_extrato']
    title = 'SIS 2022: 51st Scientific Meeting of the Italian Statistical Society: Book of the Short Papers'
    changes = {
        'U0212':'Sharma (2025) avaliou ESNs para preços de Bitcoin, com XGBoost e previsão pelo último valor como comparadores. O estudo relacionou o erro ao caos estimado por expoentes de Lyapunov. O teste de Mann–Whitney comparou, entre grupos de menor e maior caos, a razão dos RMSEs da ESN e do XGBoost. Foi relatada diferença para janelas de treino de 30 e 60 dias, mas não de 15. Isso não demonstra superioridade estatística geral da ESN sobre ARIMA ou em todos os períodos.',
        'U1014':'SHARMA, M.; SARTOR, E.; CAVAZZA, M.; PRENDINGER, H. Echo State Networks for Bitcoin Time Series Prediction. arXiv, 2025. Preprint arXiv:2508.05416v1. DOI: 10.48550/arXiv.2508.05416.',
        'U0993':f'DUTTILO, P.; GATTONE, S. A. Modelling Financial Returns with Finite Mixtures of GED. In: BALZANELLA, A.; BINI, M.; CAVICCHIA, C.; VERDE, R. (ed.). {title}. [S. l.]: Pearson, 2022. p. 1364-1369. ISBN 9788891932310.',
    }
    with ZipFile(dest) as z:
        infos=z.infolist();parts={i.filename:z.read(i.filename) for i in infos}
    before=dict(parts);root=etree.fromstring(parts['word/document.xml']);pars=root.xpath('//w:p',namespaces=helper.NS)
    for uid,new in changes.items():
        assert helper.visible(pars[units[uid]['indice_paragrafo_xml']]) == units[uid]['texto']
        assert len(new) <= 700
    helper.ITALIC_PHRASES=(*helper.ITALIC_PHRASES,title,'Preprint')
    edits=[]
    for uid,new in changes.items():
        u=units[uid];p=pars[u['indice_paragrafo_xml']];old=helper.visible(p)
        helper.replace_text(p,new);helper.format_revised_prose(p,u['indice_paragrafo_xml'])
        edits.append({'unidade':uid,'antes':old,'depois':new})
    parts['word/document.xml']=etree.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
    assert [k for k in parts if before[k]!=parts[k]] == ['word/document.xml']
    temp=dest.with_suffix('.tmp.docx')
    with ZipFile(temp,'w') as z:
        for i in infos:z.writestr(i,parts[i.filename])
    temp.replace(dest)
    claims=[
        {'unidade':'U0233','diagnostico':'condizente','evidencia':'Araújo D02 PDF7–11, conferido no lote6; Sharma D23 PDF6visível,7Tabela1e8TPE. Famílias da ESN, amostragem de hiperparâmetros e ruído de estado não são intercambiáveis.'},
        {'unidade':'U0252','diagnostico':'condizente','evidencia':'D23 PDF7Tabela1e8: TPE/Hyperopt, janelas de treino15/30/60,teste10,stride1 e tarefa de um passo. Não são horizontes de previsão15/30/60.'},
        {'unidade':'U0226','diagnostico':'condizente_com_escopo_documental','evidencia':'D10 PDF1–6: misturas de duas GED sobre retornos do DJIA2016–2022 e comparação por LR/AIC/BIC/HQIC. O parágrafo não transcreve os valores dos critérios nem os confunde com testes de normalidade.'},
    ]
    record={
        'base':state['base'],'sha256_base':state['sha256_base'],'sha256_rascunho_examinado':previous,
        'fontes_lidas_integralmente':sources,'celulas_reexaminadas':cells,'n_celulas_reexaminadas':10,'n_codigos_alterados':0,
        'unidades_conferidas_sem_edicao':claims,
        'unidades_com_conferencia_parcial':[{'unidade':'U0257','conferido':'Somente otimização Bayesiana de Sharma; Deng,Tian e Soltani mantêm conferências próprias.'}],
        'alteracoes_word':edits,
        'metadados':[{'referencia':'R40','fonte':'https://arxiv.org/abs/2508.05416','diagnostico':'Título,quatro autores,data7agosto2025,v1 e DOI conferidos no arXiv oficial. Referência normalizada para a versão efetivamente consultada, sem presumir edição final de anais ICONIP.'},{'referencia':'R19','fonte':book,'diagnostico':'Capa,créditos e sumário final abertos: quatro editores,obra,evento emCaserta22–24junho2022,Pearson,ISBN9788891932310e início1364. Fim1369no artigo local. Universidade dos autores não foi mantida como editora. Local de publicação não consta das páginas de identificação; indicado[S.l.],sem confundir com a cidade do evento.'}],
        'ressalvas_fontes':[
            'Sharma: Uniforme/LogUniforme da Tabela1são amostragem de hiperparâmetros; ruído Gaussiano da página6visível não individualiza Win/W.',
            'Sharma: Mann–Whitney compara razões de RMSE entre grupos de caos; os p-valores0,258/0,022/0,038referem-se a treinos15/30/60. Não é teste geral contra ARIMA ou arquiteturas profundas.',
            'Sharma: texto diz que atributos multivariados melhoram ESN, mas Tabela3tem RMSEmultivariado maior que univariado nas três janelas. Isso não é transportado ao TCC.',
            'Sharma: interpolação e atributos técnicos estão documentados; texto sobre ausência de transformações e análise de diferenciação fracionária devem ser lidos em seus contextos,sem inferir que toda entrada de previsão foi diferenciada.',
            'Duttilo: a frase da página3inverte os casos Normal/Laplace para nu1/2; fórmula e casos da página4indicam Normalnu2eLaplacenu1. O TCC não copia a inversão.',
            'Duttilo: AIC na Tabela1aparenta usar penalização k em vez de2k para contagens usuais5/5/7,considerando os LL publicados. Não transcrever os valores como cálculo validado. A descrição documental do uso de critérios continua condizente; não endossa toda a análise original.',
            'Duttilo: ajuste incondicional de distribuições e aplicação VaR não são inicialização de ESN ou teste causal de efeito de caudas sobre previsão de preços.',
            'O arquivo preliminar Sis-2022-A.pdf do editor tinha ISBNDraft e paginação1375no sumário. Foi descartado para paginação/edição final, substituído pelo arquivo finalSis-2022-4c-low.pdf; os extratos e origens distinguem ambos.',
        ],
        'sha256_copia_apos_edicao':sha(dest),'estado':'incorporado_pendente_exportacao_nativa',
    }
    save(target,record)
    for entry in sources:
        source=next(x for x in manifest if x['id']==entry['id']);source.update(estado_leitura=entry['estado_leitura'],log_leitura=entry['log_leitura'])
    save(OUT/'manifesto_fontes.json',manifest)
    for claim in claims:units[claim['unidade']].update(status_conteudo='conferida_no_texto_base',afirmacoes=[claim],evidencia_integral=target.name)
    for c in cells:units[c['unidade']].update(status_conteudo='decisao_de_celula_conferida_no_escopo_integral_da_fonte',afirmacoes=[c])
    for edit in edits:units[edit['unidade']].update(status_conteudo='reexaminada_correcao_incorporada_em_rascunho',afirmacoes=[edit],evidencia_integral=target.name)
    units['U0257'].update(status_conteudo='conferencia_parcial_com_escopo_explicito',evidencias_parciais_lote7=record['unidades_com_conferencia_parcial'])
    save(OUT/'inventario_unidades.json',inv)
    refs=read(OUT/'inventario_referencias.json')
    for rid,sid in [('R40','D23'),('R19','D10')]:
        ref=next(r for r in refs['referencias'] if r['id']==rid);ref.update(status_conferencia_integral='fonte_lida_decisoes_por_afirmacao_registradas',fontes_primarias=[s for s in sources if s['id']==sid],diagnosticos_por_afirmacao=[target.name],limites_restantes='Passes globais de similaridade e Guia permanecem próprios; não reprodução dos estudos.')
    save(OUT/'inventario_referencias.json',refs)
    for sid in ['D23','D10']:
        assert sid not in state['fontes_com_texto_integral_lido_nesta_meta'];state['fontes_com_texto_integral_lido_nesta_meta'].append(sid)
    state.update(sha256_copia_trabalho_atual=sha(dest),correcoes_word_incorporadas_nesta_meta=22,revalidacao_de_celulas_registrada=55,ultimo_registro_de_leitura=str(target.relative_to(ROOT)),checkpoint_mais_recente=str(target.relative_to(ROOT)),conferencia_visual_checkpoint='Lote7aguarda exportação; um parágrafo e duas referências alterados. Tabelas,mídias e resultados preservados.',unidades_com_conferencia_iniciada=sum(u['status_conteudo']!='nao_examinada_nesta_meta' for u in inv['unidades']))
    save(OUT/'estado_meta.json',state)
    print('D23 e D10 registrados; dez células confirmadas; um parágrafo e duas referências precisados. Exportação pendente.')

if __name__=='__main__':
    main()
