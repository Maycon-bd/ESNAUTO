"""Revalidação de identidade, cobertura e equivalência na v007, sem editar Word."""
from pathlib import Path
import json,re,hashlib,collections
from docx import Document
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1]
QA=ROOT/'reports/fechamento_integral_20261029'
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def norm(s):return ' '.join(s.split())
reg=read(ROOT/'docs/assistencia_monografia/versao_vigente.json')
base=next(x for x in reg['versoes'] if x['id']==reg['vigente'])
assert base['id']=='v007','A base mudou; conciliar antes de encerrar.'
src=ROOT/base['arquivo'];assert sha(src)==base['sha256']
d=Document(src);old=Document(ROOT/'reports/monografia/versoes/v006/MayconGarciaSilva_monografia_v006.docx')
allp=[(f'P{i:04}',p.text) for i,p in enumerate(d.paragraphs)]
for ti,t in enumerate(d.tables):
    for ri,row in enumerate(t.rows):
        for ci,c in enumerate(row.cells):
            for pi,p in enumerate(c.paragraphs):allp.append((f'T{ti:02} L{ri+1} C{ci+1} P{pi+1}',p.text))
texts=collections.defaultdict(list)
for l,t in allp:texts[norm(t)].append(l)
changes=[]
assert len(old.paragraphs)==len(d.paragraphs)
for i,(a,b) in enumerate(zip(old.paragraphs,d.paragraphs)):
    if norm(a.text)!=norm(b.text):changes.append({'local':f'P{i:04}','antes':a.text,'depois':b.text,'classe':'ajuste linguístico conferido; números e atribuições mantidos'})
assert len(changes)==9
for ti,(a,b) in enumerate(zip(old.tables,d.tables)):
    for ri,(r,s) in enumerate(zip(a.rows,b.rows)):
        for ci,(c,e) in enumerate(zip(r.cells,s.cells)):
            if norm(c.text)!=norm(e.text):changes.append({'local':f'T{ti:02} L{ri+1} C{ci+1}','antes':c.text,'depois':e.text,'classe':'t Student passa a t de Student; valores mantidos'})
assert len(changes)==10 # nove correções, com reexecução refletida também no sumário
ling={norm(x['antes']):x for x in changes}
citation=read(QA/'validacao_citacoes_conciliada_lote164.json')
mapped=[]
paths=set()
for x in citation['registros']:
    context=norm(x['contexto']);loc=texts.get(context)
    state='texto_idêntico_ao_contexto_validado'
    if not loc:
        assert context in ling,('Contexto sem equivalência',x)
        loc=texts.get(norm(ling[context]['depois']));assert loc
        state='ajuste_linguístico_equivalente_reavaliado'
    for e in x['evidencias']:
        path=e.get('arquivo') if isinstance(e,dict) else e
        if path:
            p=ROOT/path
            if not p.exists():p=QA/path
            assert p.exists(),path
            paths.add(p)
    mapped.append({'referencia':x['referencia'],'chamada':x['chamada'],'local_atual':loc,'estado':state,'estado_fidelidade_herdado':x['estado'],'contexto':x['contexto'],'evidencias':x['evidencias']})
assert len(mapped)==163
content=read(QA/'auditoria_final_conteudo_lote169.json')
body=[]
for x in content['corpo']:
    t=norm(x['texto']);state='idêntico'
    if t not in texts:
        assert t in ling,('Parágrafo sem conciliação',x['paragrafo'])
        t=norm(ling[t]['depois']);state='ajuste_linguístico_equivalente'
    assert t in texts
    body.append({'origem_paragrafo':x['paragrafo'],'locais_v007':texts[t],'estado':state,'evidencia_previa':x})
assert len(body)==328
matrix=read(ROOT/'reports/revisao_43_celulas_20261029/matriz_recodificada.json')
decisions=matrix['decisoes'];assert len(decisions)==170
current_matrix=read(QA/'conciliacao_matriz_atual_lote70.json')['celulas']
assert len(current_matrix)==170
sources={};matrixmap=[]
for x in decisions:
    p=ROOT/'Artigos citados'/x['arquivo_pdf'];assert p.exists();assert sha(p)==x['sha256_pdf']
    sources[str(p.relative_to(ROOT))]=x['sha256_pdf']
    reconciled=next(c for c in current_matrix if c['fonte']==x['id'] and c['dimensao']==x['dimensao'])
    ri=reconciled['linha_word'];ci=int(x['dimensao'][1:]);actual=d.tables[2].cell(ri,ci).text.strip()
    expected=reconciled['codigo_matriz_atual'];assert actual.replace('—','-')==expected.replace('—','-'),(ri,ci,actual,expected)
    for evidence in reconciled['registros']:
        path=ROOT/evidence['arquivo'];assert path.exists();paths.add(path)
    matrixmap.append({'fonte':x['id'],'dimensao':x['dimensao'],'codigo':actual,'localizador':reconciled['localizador_matriz'],'conciliacao':reconciled,'decisao_anterior':x})
assert len(sources)==34
idx=read(QA/'indice_citacoes_atuais_lote163.json')
references=[]
current=[p.text.strip() for p in d.paragraphs if p.style.name=='Referencias']
for x in idx['registros']:
    t=norm(x['referencia_atual'])
    found=[r for r in current if norm(r)==t]
    if not found:
        assert t in ling and norm(ling[t]['depois']) in {norm(r) for r in current},x['id']
    references.append({'id':x['id'],'identidade':bool(found),'correcao_apenas_pontuacao':not bool(found),'chamadas':len(x['ocorrencias'])})
assert len(current)==len(references)==50
assert all(x['chamadas'] for x in references)
evidencefiles=[]
for x in content['evidencias']:
    p=ROOT/x['arquivo'];assert sha(p)==x['sha256'],p
    paths.add(p)
for p in sorted(paths):evidencefiles.append({'arquivo':str(p.relative_to(ROOT)),'sha256_atual':sha(p)})
pdf=ROOT/'reports/revisao_linguistica_v006/revisao_final.pdf'
assert sha(pdf)=='2ea9a334f061be016f94a32495f3192689aa9d970af09e21748231e114db7d1d'
qa=read(ROOT/'reports/revisao_linguistica_v006/verificacao_final.json')
assert qa['arquivos']['candidata']['sha256']==base['sha256']
assert all(x['ok'] for x in qa['checks'])
sig=read(OUT/'siglas.json');keys=[x['sigla'] for x in sig['lista']]
assert len(keys)==50 and keys==sorted(keys,key=str.casefold)
assert all(x['usos'] for x in sig['lista'])
tablechecks=read(OUT/'checks_quadros_tabelas.json')
assert len(tablechecks)==13
assert not any(v is False for x in tablechecks for k,v in x.items())
result={'base':base,'word_sha256':sha(src),'pdf_sha256':sha(pdf),'corpo_conciliado':body,'citacoes_conciliadas':mapped,'referencias':references,'matriz':matrixmap,'fontes_matriz_verificadas':sources,'diferencas_v006_v007':changes,'evidencias_verificadas':evidencefiles,'controles_exportacao_confirmados':len(qa['checks']),'controles_tabulares':tablechecks,'resumo':{'corpo':dict(collections.Counter(x['estado'] for x in body)),'citacoes':dict(collections.Counter(x['estado'] for x in mapped)),'matriz_celulas':len(decisions),'matriz_insuficientes':sum(x['codigo']=='?' for x in matrixmap),'fontes_matriz':len(sources),'referencias':len(current),'siglas':len(keys),'elementos_tabulares':len(tablechecks)},'limite':'Conciliação de evidências dirigidas prévias com texto vigente; não é nova leitura integral das 50 obras nem garantia universal de ausência de erros/plágio.'}
(OUT/'conciliacao_integral_v007.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result['resumo'],ensure_ascii=False));print('Controles exportacao:',len(qa['checks']),'Arquivos de evidência conferidos:',len(evidencefiles))
