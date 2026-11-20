"""Consolida verificações e evidências, sem editar a base editorial."""
from pathlib import Path
import json,re,hashlib,unicodedata,collections
from docx import Document
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1]
meta=json.loads((OUT/'identidade_e_cobertura.json').read_text(encoding='utf-8'))
d=Document(ROOT/meta['base']['arquivo'])
assert hashlib.sha256((ROOT/meta['base']['arquivo']).read_bytes()).hexdigest()==meta['base']['sha256']
ps=d.paragraphs
tables=json.loads((OUT/'quadros_tabelas.json').read_text(encoding='utf-8'))
sig=json.loads((OUT/'siglas.json').read_text(encoding='utf-8'))
italics=json.loads((OUT/'italicos.json').read_text(encoding='utf-8'))
def visible(edge):return edge.get('val') not in [None,'nil','none','0']
tablechecks=[]
for t in tables:
    rows=t['celulas'];kind=t['tipo'];cap=t['titulo'];source=t['fonte_dados']
    check={'elemento':kind+' '+str(t['numero']),'local':cap['local'],'titulo':cap['texto'],
           'titulo_10':all(r['pt']==10 for r in cap['runs'] if r['texto'].strip()),
           'titulo_justificado_simples':cap['alinhamento']==3 and cap['entrelinhas']==1,
           'titulo_sem_ponto':not cap['texto'].endswith('.'),
           'corpo_11':all(r['pt']==11 for row in rows for c in row for r in c['runs'] if r['texto'].strip()),
           'cabecalho_negrito':all(r['negrito'] for c in rows[0] for r in c['runs'] if r['texto'].strip()),
           'entrelinhas_simples':all(x==1 for row in rows for c in row for x in c['entrelinhas']),
           'fonte_10_simples':source['texto'].startswith('Fonte:') and all(r['pt']==10 for r in source['runs'] if r['texto'].strip()) and source['entrelinhas']==1,
           'fonte_com_ano_ponto':bool(re.search(r'\b20\d{2}\b',source['texto'])) and source['texto'].endswith('.'),
           'minimo_linhas_colunas':t['linhas']>=3 and t['colunas']>=2,
           'largura_quadro_16':abs(t['largura_cm']-16)<.015 if kind=='Quadro' else None,
           'corpo_sem_divisorias':all(not visible(c['bordas'].get('right',{})) and not visible(row[ci+1]['bordas'].get('left',{})) for row in rows[1:] for ci,c in enumerate(row[:-1])) and all(not visible(c['bordas'].get('bottom',{})) for row in rows[1:-1] for c in row),
           'laterais':all(visible(row[0]['bordas'].get('left',{}))==bool(kind=='Quadro') and visible(row[-1]['bordas'].get('right',{}))==bool(kind=='Quadro') for row in rows),
           'cabecalho_divisorias_verticais':any(visible(c['bordas'].get('right',{})) or visible(rows[0][ci+1]['bordas'].get('left',{})) for ci,c in enumerate(rows[0][:-1])),
           'chamada_nominal':bool(t['chamadas']),'chamadas':t['chamadas']}
    tablechecks.append(check)
(OUT/'checks_quadros_tabelas.json').write_text(json.dumps(tablechecks,ensure_ascii=False,indent=2),encoding='utf-8')

# Cruzamento formal das citações: este passo não comprova sustentação conceitual.
refs=[p.text for p in ps if p.style.name=='Referencias']
def norm(s):return ''.join(c for c in unicodedata.normalize('NFD',s.casefold()) if not unicodedata.combining(c))
names=sorted({x.split(',')[0] for x in refs},key=len,reverse=True)
name='(?:'+'|'.join(map(re.escape,names))+')';year=r'(?:19|20)\d{2}[a-z]?'
co=r'(?:\s*(?:;|,|e\b|&)\s*[A-ZÀ-Ü][A-Za-zÀ-ü-]+)*'
lead=r'\b(?P<autor>'+name+r')(?:\s+[A-Z]\.)?(?:\s+et al\.)?'+co
patterns=[re.compile(lead+r'\s*\((?P<anos>'+year+r'(?:\s*,\s*'+year+r')*)\)',re.I),re.compile(lead+r'\s*,\s*(?P<anos>'+year+r')',re.I)]
records=[]
for item in json.loads((OUT/'paragrafos_e_formatacao.json').read_text(encoding='utf-8')):
    if item['estilo']=='Referencias':continue
    for pattern in patterns:
        for m in pattern.finditer(item['texto']):
            for y in re.findall(year,m['anos']):
                found=[r for r in refs if norm(r.split(',')[0])==norm(m['autor']) and re.search(r'(?<!\d)'+y+r'(?![a-z\d])',r,re.I)]
                records.append({'local':item['local'],'citacao':m[0],'ano':y,'referencias':found})
(OUT/'cruzamento_citacoes.json').write_text(json.dumps({'referencias':len(refs),'ocorrencias_reconhecidas':len(records),'sem_correspondencia':[r for r in records if not r['referencias']],'limite':'Reconhecimento por padrões; não é censo de todas as atribuições nem validação de fidelidade.','registros':records},ensure_ascii=False,indent=2),encoding='utf-8')

# Proposta da writer: apenas no relatório; nenhum Word foi editado.
rewrite='Timbó et al. (2016) aplicaram regressão linear múltipla à previsão do fechamento da PETR4, selecionando variáveis com apoio da correlação de Pearson. O estudo avaliou o acerto por uma tolerância absoluta de 0,50 entre o valor previsto e o observado, e não pelo sinal da variação do preço. Esse critério deve ser distinguido de uma taxa de acerto direcional.'
assert len(rewrite)<=700
primary=next((ROOT/'Artigos citados').glob('Timbo*'))
source={'arquivo':str(primary.relative_to(ROOT)),'sha256':hashlib.sha256(primary.read_bytes()).hexdigest(),'titulo':'Approach Based on Linear Regression for Stock Exchange Prediction – Case Study of Petr4 Petrobrás, Brazil','autores':'Nadson S. Timbó; Sofiane Labidi; Thiago P. do Nascimento; Milson L. Lima; Gilberto Nunes Neto; Rodrigo C. Matos','ano':2016,'doi':'10.5121/ijaia.2016.7103','paginas_pdf_lidas':list(range(1,12)),'leitura':'Conteúdo textual das 11 páginas; título e critério de acerto conferidos também em imagem. Extração do título na primeira página tem codificação defeituosa, resolvida por inspeção visual.','localizadores':[{'secao':'3 Methodology','pdf':5,'impressa':25,'apoio':'Seleção de variáveis com correlação de Pearson e coeficiente de determinação.'},{'secao':'3 Methodology','pdf':6,'impressa':26,'apoio':'Regressão linear múltipla e mínimos quadrados.'},{'secao':'4 Results','pdf':8,'impressa':28,'trecho_literal':'considered as success a maximum deviation of 0.50 cents','apoio':'Acerto definido por tolerância absoluta, não direção.'}]}
(OUT/'teste_writer.json').write_text(json.dumps({'estado':'proposto_nao_incorporado','versao_base':'v001','sha256_base':meta['base']['sha256'],'local':'Seção 2.1, P0194, início Ainda assim, abordagens estatísticas simples','antes':ps[194].text,'depois':rewrite,'caracteres_com_espacos':len(rewrite),'fonte':source,'coerencia_verificada':['Introdução P0173–P0186: objeto e horizonte próprios preservados','Seção 2.1 P0189–P0197: remove primazia não demonstrada e reconhecimento de limitações sem passagem localizada','Seção 3.2 P0309: contexto de escolha de PETR4 continua requerendo apoio para alta liquidez; não foi corrigido por inferência','Discussão e conclusão P0473–P0503: não foram transferidas métricas do estudo de Timbó para ESNAUTO'],'efeitos_preservados':['Sem mudar resultados, hipóteses, tabelas ou bibliografia','Sem introduzir citação de outra obra','Sem certificado de originalidade']},ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'fonte_timbo.json').write_text(json.dumps(source,ensure_ascii=False,indent=2),encoding='utf-8')

checks=[]
for s in ['quadro-tabela-validator-docx','ingles-italico-checker-docx','siglas-checker-docx','tcc-writer-docx','tcc-citation-checker-docx']:
    p=Path(r'C:\Users\User\.codex\skills')/s/'SKILL.md'
    checks.append({'skill':s,'sha256_skill':hashlib.sha256(p.read_bytes()).hexdigest(),'estado':'executada','edicao_word':False})
state={'base':meta['base'],'skills':checks,'modo':'Auditoria e propostas de redação; sem edição do Word e sem nova versão editorial.','cruzamento':{'referencias':len(refs),'ocorrencias':len(records),'sem_correspondencia':len([x for x in records if not x['referencias']])},'writer_caracteres':len(rewrite),'renderizacao':json.loads((OUT/'mapa_visual.json').read_text(encoding='utf-8')),'inspecao_visual_paginas_fisicas':[12,13,33,34,35,36,37,38,42,43,44,47,54,57,59,61,62,63],'limitacoes':['Fidelidade científica testada em amostra de afirmações sobre uma obra lida integralmente, não nas 50 referências','Sem ensaio de salvamento/reabertura de Word modificado ou de Google Docs','Varredura de estrangeirismos orientada a candidatos; não garante ausência de todo termo estrangeiro','Checagem de snapshot antiga falhou por caminho absoluto do guia; registro vigente e SHA256 conferidos diretamente']}
(OUT/'estado_testes.json').write_text(json.dumps(state,ensure_ascii=False,indent=2),encoding='utf-8')
print('Cruzamento',len(records),'ocorrencias, ausentes',state['cruzamento']['sem_correspondencia'],'Writer',len(rewrite),'caracteres')
print('Falhas chamadas',[x['elemento'] for x in tablechecks if not x['chamada_nominal']])
print('Falhas cabecalhos',[x['elemento'] for x in tablechecks if x['elemento'].startswith('Tabela') and not x['cabecalho_divisorias_verticais']])
for key in ['titulo_10','titulo_justificado_simples','titulo_sem_ponto','corpo_11','cabecalho_negrito','entrelinhas_simples','fonte_10_simples','fonte_com_ano_ponto','minimo_linhas_colunas','corpo_sem_divisorias','laterais']:
 print(key,[x['elemento'] for x in tablechecks if not x[key]])
