"""Registra leituras primárias e incorpora precisão de LSTM/GRU no rascunho."""
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile
from lxml import etree
import incorporar_fechamento_integral_lote1 as helper

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reports/fechamento_integral_20261029'
DEST=ROOT/'reports/monografia/trabalho/fechamento_integral_20261029.docx'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,data):(OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
    checkpoint=json.loads((OUT/'checkpoint_lotes12.json').read_text(encoding='utf-8'))
    assert sha(DEST)==checkpoint['sha256_atual_apos_exportacao_nativa']
    inv=json.loads((OUT/'inventario_unidades.json').read_text(encoding='utf-8'));lookup={x['id']:x for x in inv['unidades']}
    originals=[
      {'id':'SUP_JAEGER2001','arquivo':'reports/fechamento_integral_20261029/fontes_suplementares/Jaeger_2001_errata_2010.pdf','url':'https://www.ai.rug.nl/minds/uploads/EchoStatesTechRep.pdf','sha256':'0a0296f586f86a0e49e651e4581ce2aef3a926ca9cb3d57653c8963b7b83e625','paginas':47,'leitura':'Texto completo, inclusive apêndices e errata, lido sequencialmente em blocos1–10,11–20,21–30,31–40,41–47.','visuais_abertos':[1,5,8,12,13,27,34,42,43,47],'limites':'Não foi feita inspeção visual de todas as páginas nem verificação independente de cada prova ou reprodução dos experimentos. A página2 não tem texto extraído. O DOI redirecionou ao registro Fraunhofer, mas a página bloqueou leitura automatizada; a identidade do título/autor/versão é conferida no PDF do repositório do autor.'},
      {'id':'SUP_HOCH1997','arquivo':'reports/fechamento_integral_20261029/fontes_suplementares/Hochreiter_Schmidhuber_1997_copia_autor.pdf','url':'https://people.idsia.ch/~juergen/lstm1997-2024head.pdf','sha256':'51e319ebc53b96964bc167faa3a45d02eca61964eb7ed6bbc1cb2e70517064f2','paginas':32,'leitura':'Todas as32páginas renderizadas abertas e lidas visualmente em blocos de4, inclusive tabelas, discussão, apêndice e referências.','visuais_abertos':list(range(1,33)),'limites':'Cópia distribuída pelo coautor, com cabeçalho bibliográfico e modificação de metadados em2024; não é comparação byte a byte com a diagramação da edição publicada. O corpo tem paginação1–32 e identifica a publicação Neural Computation9(8):1735–1780,1997. A extração textual é ilegível e foi descartada como evidência de conteúdo. Não se reproduziram os experimentos.'}
    ]
    for s in originals:assert sha(ROOT/s['arquivo'])==s['sha256']
    code=[]
    for name in ['app/modules/mod_lstm.R','app/modules/mod_gru.R']:
        p=ROOT/name;code.append({'arquivo':name,'sha256':sha(p),'escopo_lido':'Arquitetura, compile e fit, aproximadamente linhas75–120; procura de épocas/otimizador no arquivo.','evidencia':'Camadas LSTM/GRU e Dense, compile com MSE e otimizador configurável; fit com épocas/lotes e medição elapsed.','limite':'Estado atual lido; não prova identidade com cada execução histórica. Não foi executado, restaurado ou alterado.'})
    proposals=[
      {'unidade':'U0192','diagnostico':'condizente_com_precisao_de_escopo','motivo':'Retirar ranking de uso não medido pelas fontes, corrigir a expansão de LSTM e distinguir a motivação original de LSTM da unidade simplificada de Cho. Não atribuir resultados financeiros aos estudos de tarefas artificiais/tradução.','evidencias':[{'referencia':'R25','localizador':'Hochreiter/Schmidhuber PDF1–8 e22–30: fluxo de erro, células, portas e limites do algoritmo original.'},{'referencia':'R12','localizador':'Cho PDF1–3 e10: proposta de codificador–decodificador e unidade de duas portas; não é benchmark financeiro.'}],'proposta':'As redes Long Short-Term Memory (LSTM) foram introduzidas por Hochreiter e Schmidhuber (1997) para facilitar a aprendizagem de dependências longas, usando células de memória e controle do fluxo de erro. Cho et al. (2014) propuseram uma unidade com portas de atualização e reinicialização, hoje conhecida como Gated Recurrent Unit (GRU), no contexto de uma arquitetura de rede neural recorrente (Recurrent Neural Network – RNN) do tipo codificador–decodificador. A simplificação estrutural dessa unidade não constitui, por si, uma garantia de menor erro em séries financeiras.'},
      {'unidade':'U0194','diagnostico':'generalizacao_nao_sustentada_no_alcance_enunciado','motivo':'A redação anterior estendia instabilidades residuais a ambas as arquiteturas em séries muito longas. Hochreiter descreve solução e limites específicos do algoritmo original; Cho descreve outra unidade em tradução, sem demonstrar essa generalização financeira. Delimitar o contraste ao treinamento implementado e à avaliação de custos.','evidencias':[{'referencia':'R25','localizador':'PDF8–10,22–30: algoritmo original com truncamento, complexidade e limites específicos, não teorema de instabilidade residual das duas arquiteturas.'},{'referencia':'R12','localizador':'PDF3 e5–6: unidade simplificada treinada por gradiente na tarefa de tradução.'},{'artefatos':code}],'proposta':'Na implementação do ESNAUTO, LSTM e GRU são treinadas iterativamente por retropropagação através do tempo (Backpropagation Through Time – BPTT), ajustando pesos internos e de saída. O custo desse processo depende da configuração da rede e do orçamento de treinamento. A comparação com a ESN deve distinguir esse treinamento do ajuste da camada de saída e da busca de hiperparâmetros, sem pressupor inviabilidade ou superioridade geral.'}
    ]
    with ZipFile(DEST) as z:infos=z.infolist();parts={x.filename:z.read(x.filename) for x in infos}
    before=dict(parts);root=etree.fromstring(parts['word/document.xml']);pars=root.xpath('//w:p',namespaces=helper.NS)
    helper.ITALIC_PHRASES+=('Long Short-Term Memory','Gated Recurrent Unit','Recurrent Neural Network','Backpropagation Through Time')
    for x in proposals:
        u=lookup[x['unidade']];p=pars[u['indice_paragrafo_xml']];assert helper.visible(p)==u['texto'];assert len(x['proposta'])<=700
        x.update(texto_anterior=u['texto'],sha256_texto_base=u['sha256_texto'],estado='incorporado_em_copia_pendente_conferencia_nativa')
        helper.replace_text(p,x['proposta']);helper.format_revised_prose(p,u['indice_paragrafo_xml'])
        u.update(status_conteudo='reexaminada_correcao_incorporada_em_rascunho',afirmacoes=x['evidencias'])
    parts['word/document.xml']=etree.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
    assert [k for k in parts if parts[k]!=before[k]]==['word/document.xml']
    tmp=DEST.with_suffix('.tmp.docx')
    with ZipFile(tmp,'w') as z:
        for info in infos:z.writestr(info,parts[info.filename])
    tmp.replace(DEST)
    # A unidade conjunta de fundamentos da ESN agora tem as duas fontes lidas.
    u=lookup['U0202'];u.update(status_conteudo='conferida_no_texto_base',afirmacoes=[{'afirmacao':'A ESN usual usa estados de uma rede recorrente e treina pesos de saída por regressão, mantendo pesos internos fixos.','diagnostico':'condizente','localizador':'Jaeger2001/2010 PDF3–5 e11–15; Jaeger2007 PDF1–3.','limite':'Configuração usual; não exclusividade de todas as variantes RC nem garantia de estabilidade numérica.'}])
    record={'base':'v005','sha256_base':inv['sha256_base'],'sha256_copia_antes_lote':checkpoint['sha256_atual_apos_exportacao_nativa'],'sha256_copia_apos_lote':sha(DEST),'fontes':originals,'codigo_atual_lido':code,'alteracoes':proposals,'unidades_conferidas_sem_mudanca':['U0202'],'notas_fonte_Jaeger':['A condição suficiente da proposição3 usa maior valor singular, e o raio espectral não é identificado como garantia universal da ESP.','A definição corrigida na errata42–45 requer contração uniforme; não repetir a definição falha da página7.','A fonte2001descreve leis discretas explícitas em Win/W nas páginas13/17/29. Não transportá-las à célula de Jaeger2007(D15), que é outra obra e mantém P1?.','A equação21 da página27 é o modelo geral com parâmetros de passo, escala e decaimento; não igualar nomes de parâmetros a taxas da implementação sem conferir as convenções.'],'notas_fonte_LSTM':['A arquitetura original tem portas de entrada e saída; não atribuir a porta moderna de esquecimento ao artigo1997sem fonte adicional. A descrição moderna da monografia se apoia em Sudiatmika2024.','Os benchmarks são artificiais, não de ações; custo em apresentações de sequências ou complexidade assintótica não é tempo medido para PETR4.','O artigo original analisa uma versão eficiente truncada, com discussão de gradientes completos; não descrever todos os detalhes dessa versão como idênticos a treinamento moderno de bibliotecas.'],'limites_pendentes':'Verificação nativa dos dois novos parágrafos, passe global de similaridade, números próprios e Guia ainda não encerrados.'}
    save('leituras_fundamentos_lote3.json',record);save('inventario_unidades.json',inv)
    refs=json.loads((OUT/'inventario_referencias.json').read_text(encoding='utf-8'))
    for rid,src in [('R27',originals[0]),('R25',originals[1])]:
        r=next(x for x in refs['referencias'] if x['id']==rid);r.update(fontes_primarias=[src],status_conferencia_integral='fonte_lida_e_decisoes_de_conteudo_registradas',diagnosticos_por_afirmacao=['leituras_fundamentos_lote3.json'],limites_restantes='Todas as retomadas, atribuição de código, similaridade global e conferência final do Word têm verificações próprias ainda em andamento.')
    save('inventario_referencias.json',refs)
    state=json.loads((OUT/'estado_meta.json').read_text(encoding='utf-8'))
    for sid in ['SUP_JAEGER2001','SUP_HOCH1997']:
        if sid not in state['fontes_com_texto_integral_lido_nesta_meta']:state['fontes_com_texto_integral_lido_nesta_meta'].append(sid)
    state.update(correcoes_word_incorporadas_nesta_meta=9,sha256_copia_trabalho_atual=sha(DEST),checkpoint_mais_recente='reports/fechamento_integral_20261029/leituras_fundamentos_lote3.json',conferencia_visual_checkpoint='Lotes1/2conferidos; lote3aguarda exportação nativa.');save('estado_meta.json',state)
    print('Dois parágrafos incorporados; fontes primárias e unidade ESN conferidas. Cópia continua em auditoria.')

if __name__=='__main__':main()
