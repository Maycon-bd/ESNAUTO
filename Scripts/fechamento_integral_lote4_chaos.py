"""Leitura integral de Hassaan/Seddik e recodificação documental, sem experimentos."""
import csv,hashlib,json,sys
from pathlib import Path
from collections import Counter
from zipfile import ZipFile
from lxml import etree
import incorporar_fechamento_integral_lote1 as helper

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reports/fechamento_integral_20261029'
MATRIX=OUT/'matriz_lote4'
DEST=ROOT/'reports/monografia/trabalho/fechamento_integral_20261029.docx'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,a):p.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def prepare():
    MATRIX.mkdir(exist_ok=True)
    assert not (MATRIX/'matriz_recodificada.json').exists(),'Não sobrescrever decisões já registradas.'
    a=read(ROOT/'reports/revisao_43_celulas_20261029/matriz_recodificada.json')
    a.update(base_examinada='v005',sha256_base='2af31abca4e3ba9fd5caf7cd161e55472dc94edc136cdf89732c0d0401118d6b',validacao_integral_das_fontes=False,derivada_de='reports/revisao_43_celulas_20261029/matriz_recodificada.json')
    selected=[]
    for d in a['decisoes']:
        if d['id'] not in ['D14','D22']:continue
        d['escopo_leitura']='Texto integral lido nesta meta e páginas de evidência inspecionadas visualmente; ver leituras_chaos_lote4.json.'
        d['codigo_anterior_neste_lote']=d['codigo']
        if d['id']=='D22' and d['dimensao']=='P3':
            assert d['codigo']=='?';d.update(codigo='D',localizador='PDF7, coluna esquerda, parágrafo sobre a série U2; conferido no PNG.',evidencia_e_limite='Os autores chamam U2 de série decimada (decimated time series), nomeando uma operação de preparação aplicada à série simulada. P3 admite séries não financeiras. A menção é direta, mas não especifica fator de decimação, filtro ou procedimento reprodutível; não prova preparo de preços observados. D registra documentação localizada, não reprodução nem completude de parâmetros.')
        if d['id']=='D22' and d['dimensao']=='P1':d['evidencia_e_limite']+=' A leitura integral não localizou lei probabilística dos elementos; a palavra aleatório e os valores de raio/esparsidade não a identificam.'
        selected.append(d)
    counts=[]
    for dim in ['P1','P2','P3','P4','P5']:
        c=Counter(d['codigo'] for d in a['decisoes'] if d['dimensao']==dim);assert sum(c.values())==34
        counts.append(dict(dimensao=dim,direta=c['D'],secundaria=c['S'],insuficiente=c['?'],nao_aplicavel=c['-']))
    assert counts[2]==dict(dimensao='P3',direta=26,secundaria=2,insuficiente=6,nao_aplicavel=0)
    save(MATRIX/'matriz_recodificada.json',a)
    with (MATRIX/'contagens_recodificadas.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=counts[0].keys());w.writeheader();w.writerows(counts)
    r=(ROOT/'Scripts/plotar_cobertura_recodificada.R').read_text(encoding='utf-8').replace('root <- "reports/correcao_parecer_integridade"','root <- "reports/fechamento_integral_20261029/matriz_lote4"')
    (MATRIX/'plotar_apenas_cobertura.R').write_text(r,encoding='utf-8')
    sources=read(OUT/'manifesto_fontes.json')
    logs=[]
    for sid,visuals in [('D14',[7,8,11,12,13,19,20]),('D22',[1,5,6,7,8,9])]:
        source=next(s for s in sources if s['id']==sid);assert sha(ROOT/source['arquivo'])==source['sha256']
        logs.append({**source,'leitura_integral':'Texto completo, inclusive referências e declarações finais, lido sequencialmente. D14 em blocos1–11 e12–22; D22em blocos1–6 e7–11.','paginas_visuais_abertas':visuals,'limites':'Leitura e conferência de coerência documental, sem replicação de experimentos ou comprovação independente dos resultados.'})
    record={'base':'v005','sha256_base':a['sha256_base'],'fontes':logs,'celulas_reexaminadas':selected,'n_celulas_reexaminadas':10,'n_codigos_alterados':1,'decisao_P3':'Decimação é uma operação temporal nomeada, mesmo sem parâmetros de implementação. Esse limiar documental também é usado para normalização/validação cruzada declaradas sem detalhes completos; não se exige reprodução para marcar D. A natureza simulada é preservada e P5 continua S.','unidades_conferidas_sem_edicao':['U0232','U0250','U0251'],'unidades_conferidas_parcialmente':[{'unidade':'U0255','escopo':'Apenas as afirmações sobre Hassaan e Sun; Kumar ainda exige leitura nesta meta.'}],'achados_internos_fontes':{'D14':['PDF7equação9b usa rand uniforme; PDF8prosa/figura4f descrevem distribuição semelhante à Gaussiana. A ressalva existente na monografia é mantida.','PDF13Tabela2: para GRU/S&P500caótico, MAE0,043727ao quadrado excede MSE0,000183; seriam incompatíveis se calculados sobre os mesmos erros. Nenhum desses números foi transferido à monografia.','PDF5apresenta TSCO.L/Tesco e simultaneamente chama o conjunto de FTSE100. Não acrescentar ao texto uma identificação mais precisa do que a fonte permite.','PDF19relata496ciclos,4,96microssegundos e83,5MHz;496/83,5MHz resulta cerca de5,94microssegundos. Não transportar a latência declarada como custo de treino do ESNAUTO. Aceleração tratada na seção6é de predição após treinamento em software.'],'D22':['PDF5diz perturbação10^-3, mas os valores39,102501e39,102501001diferem por10^-9. A monografia não transporta esse número.','PDF3–4e6divergem no significado de esparsidade0,95; descrevem regressão linear, Ridge e Levenberg–Marquardt sem conciliação operacional. Não usar essas passagens como garantia de implementação ou estabilidade.','PDF8prosa diz RMSE idênticos em todos os horizontes, mas Tabela3varia. PDF9Tabela5traz pares RMSE/MSE/MAE incoerentes em algumas linhas. A monografia não reproduz esses valores nem apresenta superioridade universal.','Não localizar família de geração dos pesos não permite aproveitar a distribuição de outro artigo para preencher P1.']} ,'estado':'leituras_concluidas_ajustes_editoriais_pendentes'}
    save(OUT/'leituras_chaos_lote4.json',record)
    print('Leituras registradas,10células reexaminadas,1mudança; gráfico e incorporação pendentes.')

def apply():
    checkpoint=read(OUT/'checkpoint_lote3.json');assert sha(DEST)==checkpoint['sha256_atual_apos_exportacao_nativa']
    record=read(OUT/'leituras_chaos_lote4.json');assert record['estado']=='leituras_concluidas_ajustes_editoriais_pendentes'
    inventory=read(OUT/'inventario_unidades.json');units=inventory['unidades'];lookup={u['id']:u for u in units}
    with ZipFile(DEST) as z:infos=z.infolist();parts={x.filename:z.read(x.filename) for x in infos}
    before=dict(parts);root=etree.fromstring(parts['word/document.xml']);ps=root.xpath('//w:p',namespaces=helper.NS);changes=[]
    def change(u,new,reason,prose=False):
        p=ps[u['indice_paragrafo_xml']];old=helper.visible(p);assert old==u['texto'];assert old!=new
        helper.replace_text(p,new)
        if prose:helper.format_revised_prose(p,u['indice_paragrafo_xml'])
        changes.append(dict(unidade=u['id'],antes=old,depois=new,motivo=reason));u.update(status_conteudo='reexaminada_correcao_incorporada_em_rascunho',evidencia_lote4='leituras_chaos_lote4.json')
    text='Hassaan et al. (2025) compararam ESN e GRU com inicializações caóticas e controles Xavier e He em seis conjuntos financeiros. Seddik, Routaib e Elhaddadi (2023) investigaram uma ESN em trajetórias simuladas de Lorenz, com condições iniciais associadas ao Bitcoin. O texto menciona uma série decimada, sem detalhar o procedimento. As métricas avaliam trajetórias geradas, não previsões de preços observados, e não isolam o efeito da distribuição dos pesos iniciais.'
    assert len(text)<=700
    change(lookup['U0211'],text,'Crédito aos três autores e delimitação da preparação relatada na série simulada.',True)
    change(lookup['U0418'],'Seddik, Routaib e Elhaddadi (2023)','Autoria da linha do Quadro1.')
    assert lookup['U0421']['texto']=='?';change(lookup['U0421'],'D','P3: relato de série decimada, PDF7, com limites expressos no registro.')
    u=next(u for u in units if u['texto']=='25 D; 2 S; 7 ?; 0 —');change(u,'26 D; 2 S; 6 ?; 0 —','Contagem P3derivada da única recodificação.')
    u=next(u for u in units if 'evidência direta de preparação de séries em 25 documentos' in u['texto'])
    change(u,u['texto'].replace('preparação de séries em 25 documentos','preparação de séries em 26 documentos'),'Conciliar descrição da Figura1com contagens.',True)
    u=next(u for u in units if u['texto'].startswith('SEDDIK, S;'));p=ps[u['indice_paragrafo_xml']];old=helper.visible(p)
    matched=False
    for t in p.xpath('.//w:t',namespaces=helper.NS):
        if 'SEDDIK, S;' in (t.text or ''):t.text=t.text.replace('SEDDIK, S;','SEDDIK, S.;',1);matched=True;break
    assert matched and helper.visible(p)==old.replace('SEDDIK, S;','SEDDIK, S.;',1)
    changes.append(dict(unidade=u['id'],antes=old,depois=helper.visible(p),motivo='Pontuação da inicial bibliográfica, preservando os três autores e título.'));u.update(status_conteudo='referencia_conferida_pontuacao_corrigida')
    # Descobrir a mídia pela figura, sem supor seu número no pacote OOXML.
    body=root.find(helper.W+'body');bodyps=body.findall(helper.W+'p')
    anchor=next(p for p in bodyps if p.xpath('.//*[local-name()="blip"]') and bodyps.index(p)>250 and bodyps.index(p)<280)
    rid=anchor.xpath('.//*[local-name()="blip"]/@*[local-name()="embed"]')[0]
    rels=etree.fromstring(parts['word/_rels/document.xml.rels']);media='word/'+next(r.get('Target') for r in rels if r.get('Id')==rid)
    assert hashlib.sha256(parts[media]).hexdigest()==sha(ROOT/'reports/revisao_43_celulas_20261029/figura1_recodificada.png')
    parts[media]=(MATRIX/'figura1_recodificada.png').read_bytes()
    parts['word/document.xml']=etree.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
    assert {k for k in parts if parts[k]!=before[k]}=={'word/document.xml',media}
    temp=DEST.with_suffix('.tmp.docx')
    with ZipFile(temp,'w') as z:
        for info in infos:z.writestr(info,parts[info.filename])
    temp.replace(DEST)
    record.update(estado='incorporado_pendente_exportacao_nativa',sha256_copia_antes=checkpoint['sha256_atual_apos_exportacao_nativa'],sha256_copia_apos=sha(DEST),alteracoes_textuais=changes,figura_alterada=media,contagens_globais={'D':77,'S':12,'?':40,'-':41})
    for uid in ['U0232','U0250','U0251']:lookup[uid].update(status_conteudo='conferida_no_texto_base',afirmacoes=[{'diagnostico':'condizente_com_limites_explicitos','evidencia':'D14PDF3–13; ver leituras_chaos_lote4.json.'}])
    save(OUT/'inventario_unidades.json',inventory);save(OUT/'leituras_chaos_lote4.json',record)
    sources=read(OUT/'manifesto_fontes.json')
    for source in record['fontes']:
        row=next(s for s in sources if s['id']==source['id']);row.update(estado_leitura='texto_integral_lido_e_evidencias_visuais_inspecionadas',log_leitura=[{'registro':'leituras_chaos_lote4.json','paginas_lidas':list(range(1,source['paginas']+1)),'paginas_visuais_abertas':source['paginas_visuais_abertas']}])
    save(OUT/'manifesto_fontes.json',sources)
    refs=read(OUT/'inventario_referencias.json')
    for rid,sid in [('R24','D14'),('R39','D22')]:
        r=next(r for r in refs['referencias'] if r['id']==rid);r.update(fontes_primarias=[s for s in record['fontes'] if s['id']==sid],status_conferencia_integral='fonte_lida_decisoes_por_afirmacao_registradas',diagnosticos_por_afirmacao=['leituras_chaos_lote4.json'],limites_restantes='Passes globais de similaridade e forma, exportação atual e retomadas compostas têm conferências próprias. D não certifica qualidade metodológica ou reprodução do estudo.')
    save(OUT/'inventario_referencias.json',refs)
    state=read(OUT/'estado_meta.json')
    for sid in ['D14','D22']:
        if sid not in state['fontes_com_texto_integral_lido_nesta_meta']:state['fontes_com_texto_integral_lido_nesta_meta'].append(sid)
    state.update(sha256_copia_trabalho_atual=sha(DEST),correcoes_word_incorporadas_nesta_meta=15,revalidacao_de_celulas_registrada=30,checkpoint_mais_recente='reports/fechamento_integral_20261029/leituras_chaos_lote4.json',conferencia_visual_checkpoint='Lote4pendente exportação nativa; Figura1recalculada apenas a partir de códigos editoriais.');save(OUT/'estado_meta.json',state)
    print('Seis unidades textuais e uma figura alteradas. Nenhum resultado experimental modificado.')

if __name__=='__main__':
    {'preparar':prepare,'incorporar':apply}[sys.argv[1]]()
