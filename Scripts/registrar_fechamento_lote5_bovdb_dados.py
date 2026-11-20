"""Registra BovDB/RBras, confere dados preservados e precisa um parágrafo."""
import hashlib,json
from pathlib import Path
from zipfile import ZipFile
from lxml import etree
import incorporar_fechamento_integral_lote1 as helper

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reports/fechamento_integral_20261029'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,a):p.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
    state=read(OUT/'estado_meta.json');dest=ROOT/state['copia_trabalho'];previous=sha(dest)
    assert previous==state['sha256_copia_trabalho_atual']==read(OUT/'checkpoint_lote4.json')['sha256_atual_apos_exportacao_nativa']
    target=OUT/'leituras_bovdb_rbras_dados_lote5.json';assert not target.exists()
    manifest=read(OUT/'manifesto_fontes.json');sources=[]
    for sid,visuals,method in [('D04',[1,5,7,8,9,11,16],'Texto completo das18páginas lido em ordem nos blocos1–9e10–18; sete páginas de evidência abertas.'),('SUP_CARDOSO_RBRAS',list(range(1,11)),'PDF sem camada textual: todas as10páginas197–206abertas e lidas visualmente, em blocos1–5e6–10.')]:
        s=next(s for s in manifest if s['id']==sid);assert sha(ROOT/s['arquivo'])==s['sha256']
        entry={**s,'leitura':method,'paginas_visuais_abertas':visuals,'limites':'Conferência de fidelidade documental; os estudos e o ajuste corporativo não foram reproduzidos.'};sources.append(entry)
        s.update(estado_leitura='leitura_integral_com_evidencias_visuais',log_leitura=[{'registro':target.name,'metodo':method,'paginas_visuais_abertas':visuals}])
    inv=read(OUT/'inventario_unidades.json');units={u['id']:u for u in inv['unidades']}
    claims=[
      {'unidade':'U0235','diagnostico':'condizente','localizador':'BovDB PDF4–8,Fig1eEq1–2','afirmacao':'Base de cotações/eventos, fator por evento e acumulado por preço; não prova processamento do arquivo local.'},
      {'unidade':'U0236','diagnostico':'condizente','localizador':'BovDB PDF5,7–8','afirmacao':'Razão fechamento anterior/abertura do evento, acumulação regressiva e campo applied. O texto não promete reconstrução de cada exceção local.'},
      {'unidade':'U0242','diagnostico':'condizente','localizador':'BovDB PDF1,3–8,15–17','afirmacao':'Proposição do conjunto BovDB e tratamento retroativo de eventos. Introduzem o fator no contexto do artigo; não é atribuição de invenção universal de ajustes de ações.'},
      {'unidade':'U0896','diagnostico':'condizente','localizador':'RBras PDF6–9,p202–205','afirmacao':'5197observações,75%/25%,hiperparâmetros fixos,RMSE11,1785sem fator e0,4987com fator. Não são apresentados como novo teste de superioridade do ESNAUTO.'}
    ]
    partial=[
      {'unidade':'U0525','conferido':'Procedência declarada pelo autor e método BovDB; arquivos recebidos já ajustados, conforme esclarecimento do autor. Não constitui reconstrução do ajuste.'},
      {'unidade':'U0549','conferido':'Atribuição do método e valores da Tabela2compatíveis com os arquivos; desenho gráfico/forma têm passagens próprias.'},
      {'unidade':'U0580','conferido':'Apenas valores fixos de1,25;0,2;10^-8e localizadorp203da RBras. Os intervalos e55bits do ESNAUTO ainda dependem da conferência do código/cromossomo.'},
      {'unidade':'U0612','conferido':'Apenas pertinência de Cardoso2022aeJaeger2007; Araújo2025e a implementação própria ainda têm conferências independentes.'}
    ]
    matrix=read(OUT/'matriz_lote4/matriz_recodificada.json');cells=[dict(x) for x in matrix['decisoes'] if x['id']=='D04'];assert [x['codigo'] for x in cells]==['-','-','D','-','D']
    for c in cells:c['escopo_leitura']='BovDB PDF1–18lido integralmente; Fig1,Eq1–2,exemplo VALE3eFig6PETR4inspecionados visualmente.'
    for c in cells:
        if c['dimensao']=='P3':c.update(localizador='PDF5,7–11,15',evidencia_e_limite='Fator corporativo por evento e acumulado, padronização/identificação de tickers e exemplos de séries com/sem ajuste. Evidência documental direta, sem reconstruir a aplicação aos arquivos recebidos.')
        if c['dimensao']=='P4':c['evidencia_e_limite']='Objeto próprio é construção/apresentação de base. Referências a C-LSTMem classificação textual não constituem comparação quantitativa de previsão temporal qualificadora.'
    with ZipFile(dest) as z:infos=z.infolist();parts={x.filename:z.read(x.filename) for x in infos}
    before=dict(parts);root=etree.fromstring(parts['word/document.xml']);pars=root.xpath('//w:p',namespaces=helper.NS)
    u=units['U0214'];p=pars[u['indice_paragrafo_xml']];old=helper.visible(p);assert old==u['texto']
    new='O comportamento do reservatório depende da configuração de seus hiperparâmetros. O raio espectral é utilizado no reescalonamento da matriz recorrente; a esparsidade regula a conectividade, e a taxa de vazamento pondera a contribuição do estado anterior na atualização. A seleção desses parâmetros deve considerar a tarefa e o protocolo de avaliação.'
    assert len(new)<=700;helper.replace_text(p,new);helper.format_revised_prose(p,u['indice_paragrafo_xml'])
    parts['word/document.xml']=etree.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
    assert [k for k in parts if parts[k]!=before[k]]==['word/document.xml']
    tmp=dest.with_suffix('.tmp.docx')
    with ZipFile(tmp,'w') as z:
        for info in infos:z.writestr(info,parts[info.filename])
    tmp.replace(dest)
    numeric=read(OUT/'conferencia_numerica_entradas_e_rodada_controlada.json');assert numeric['sha256_rascunho']==previous
    record={'base':state['base'],'sha256_base':state['sha256_base'],'sha256_rascunho_examinado':previous,'fontes_lidas_integralmente':sources,'unidades_conferidas_sem_edicao':claims,'unidades_com_conferencia_parcial':partial,'celulas_reexaminadas':cells,'n_celulas_reexaminadas':5,'n_codigos_alterados':0,
      'metadados_referencias':[{'referencia':'R06','diagnostico':'condizente_com_fontes','fontes':'Original10páginas com título/autores/evento/local/ano/p197–206; capa do livro no acervo UFRGS; tese do próprio Cardoso PDF118(p115),entrada da referência, aberta e lida.','nota':'A capa denomina Livro de Resumos; o próprio autor cita como Anais da66ªReunião, com RBras como entidade de publicação. A forma abreviada Anais[...]da monografia é compatível. As letras2022a/b/c são desambiguação local; não copiar as letras distintas da tese.'},{'referencia':'R07','diagnostico':'condizente_com_fontes','fontes':'PDF1e cabeçalhos/rodapés: sete autores, título,JournalofInformationandDataManagement13(1):77–94,August2022.','nota':'O exemplo de citação sugerido no interior do artigo usa2021, mas o veículo/cabeçalhos/publicação identificam2022. Mantido2022b.'}],
      'capa_metadados_RBras':{'arquivo':'reports/fechamento_integral_20261029/fontes_suplementares/RBras_2022_capa_acervo_UFRGS.pdf','sha256':'4451064d8dd40bbb0e44a1f8ea9bb4adaebcb9f527a867a96805618944e4c4a5','url':'https://lume.ufrgs.br/bitstream/10183/252914/1/001157560.pdf','escopo':'Apenas capa,página1,usada para metadados do evento. A página2é resumo de outro trabalho e não entra no corpus nem nos resultados. O HTML do item retornou Verificação de segurança e não foi usado como prova de metadados.'},
      'tese_consultada_parcialmente':{'arquivo':'reports/tese_Fabian_Correa_Cardoso.pdf','sha256':'0713862798eb01327e7534ff86e694d76bb8bf9bc2113ba6407bef04f14b2e26','escopo':'Somente PDF118(p115),bibliografia,para a autodescrição do trabalho RBras. Não declarar leitura integral da tese a partir desta consulta.'},
      'ressalvas_fontes':['BovDB PDF7menciona divisão de preços pelo fator isolado; o esquema e exemplos também descrevem um fator acumulado. A monografia não reconstrói a rotina de correção dos arquivos locais nem seleciona uma interpretação para atribuí-la ao autor.','BovDB TabelaIIlista1,99547e acumulados3,72/1,86,que não coincidem exatamente por essa multiplicação. Não converter o exemplo em validação aritmética da série recebida.','RBras introdução menciona VALE3em um parágrafo, mas título, metodologia, resultados e figuras tratam PETR4. A monografia se apoia nas seções metodológica e de resultados.','RBras descreve pesos aleatórios entre-1e1,sem nomear explicitamente a lei. Não usar essa outra obra para preencher células de Jaeger2007ouAraújo2025.','Valores RBras e dos arquivos atuais não são forçados a coincidir:5197versus5198observações,além de protocolos diferentes.'],
      'alteracao_word':{'unidade':'U0214','antes':old,'depois':new,'motivo':'Precisar o papel do raio espectral, retirando associação vaga a caoticidade e a hierarquia não quantificada de pontos mais sensíveis. Não altera hipótese ou protocolo.','evidencias':'Jaeger2001/2010PDF8,13,27,33–34; Jaeger2007; RBrasp200–203; app/utils/esn_core.Rlinhas21–23e29–31; Scripts/acoes_petr4_esn.Rlinhas265–266.','sha256_esn_core_atual':sha(ROOT/'app/utils/esn_core.R'),'limite':'Código atual lido,não presumido idêntico a todas as execuções históricas.'},
      'dados_e_metricas':'conferencia_numerica_entradas_e_rodada_controlada.json','sha256_copia_apos_edicao':sha(dest),'estado':'leitura_e_correcao_incorporada_pendente_exportacao_nativa'}
    save(target,record);save(OUT/'manifesto_fontes.json',manifest)
    for item in claims:units[item['unidade']].update(status_conteudo='conferida_no_texto_base',afirmacoes=[item],evidencia_integral=target.name)
    for item in partial:units[item['unidade']].update(status_conteudo='conferencia_parcial_com_escopo_explicito',evidencias_parciais_lote5=[item])
    for i,c in enumerate(cells):units[f'U{311+i:04}'].update(status_conteudo='decisao_de_celula_conferida_no_escopo_integral_da_fonte',afirmacoes=[c])
    u.update(status_conteudo='reexaminada_correcao_incorporada_em_rascunho',afirmacoes=[record['alteracao_word']])
    for uid in ['U0526','U0533']+[f'U{i:04}' for i in range(537,549)]:units[uid].update(status_conteudo='conferida_com_arquivos_de_entrada',evidencia_numerica='conferencia_numerica_entradas_e_rodada_controlada.json')
    for uid in ['U0531','U0532','U0842','U0945']:
        units[uid].update(status_conteudo='conferencia_numerica_parcial',evidencia_numerica='conferencia_numerica_entradas_e_rodada_controlada.json',limite_pendente='Somente datas/partições ou métricas da rodada controlada aqui; demais afirmações de aptidão,treinamento,histórico/inferência exigem conferências próprias.')
    save(OUT/'inventario_unidades.json',inv)
    refs=read(OUT/'inventario_referencias.json')
    for rid,sid in [('R06','SUP_CARDOSO_RBRAS'),('R07','D04')]:
        ref=next(x for x in refs['referencias'] if x['id']==rid);ref.update(status_conferencia_integral='fonte_lida_decisoes_por_afirmacao_registradas',fontes_primarias=[s for s in sources if s['id']==sid],diagnosticos_por_afirmacao=[target.name],limites_restantes='Passes globais de forma e similaridade ainda próprios; protocolos publicados não foram repetidos.')
    save(OUT/'inventario_referencias.json',refs)
    for sid in ['D04','SUP_CARDOSO_RBRAS']:
        assert sid not in state['fontes_com_texto_integral_lido_nesta_meta'];state['fontes_com_texto_integral_lido_nesta_meta'].append(sid)
    state.update(sha256_copia_trabalho_atual=sha(dest),correcoes_word_incorporadas_nesta_meta=16,revalidacao_de_celulas_registrada=40,ultimo_registro_de_leitura=str(target.relative_to(ROOT)),checkpoint_mais_recente=str(target.relative_to(ROOT)),conferencia_visual_checkpoint='Lote5aguarda exportação; uma unidade textual alterada,todas as tabelas e mídias preservadas.',unidades_com_conferencia_iniciada=sum(x['status_conteudo']!='nao_examinada_nesta_meta' for x in inv['unidades']));save(OUT/'estado_meta.json',state)
    print('BovDB/RBras registrados; entrada e métricas controladas conferidas; um parágrafo precisado. Exportação pendente.')

if __name__=='__main__':main()
