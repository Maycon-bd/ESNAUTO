from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
import collections,hashlib,json
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1]
base=ROOT/'reports/monografia/versoes/v009/MayconGarciaSilva_monografia_v009.docx'
doc=ROOT/'reports/monografia/trabalho/busca_lacunas_20261101.docx'
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
def parts(p):
    with ZipFile(p) as z:return {n:z.read(n) for n in z.namelist()}
def txt(p):return ''.join(p.xpath('.//w:t/text()',namespaces=ns))
a,b=parts(base),parts(doc)
assert a.keys()==b.keys()
changed=[n for n in a if a[n]!=b[n]]
assert set(changed)=={'word/document.xml','word/media/image1.png'}
ar,br=E.fromstring(a['word/document.xml']),E.fromstring(b['word/document.xml'])
at,bt=ar.xpath('.//w:tbl',namespaces=ns),br.xpath('.//w:tbl',namespaces=ns)
assert len(at)==len(bt)==14
changed_tables=[i for i in range(14) if E.tostring(at[i])!=E.tostring(bt[i])]
assert len(changed_tables)==2
mt=next(t for t in bt if len(t.findall('w:tr',ns))==35)
matrix=[[txt(c) for c in tr.findall('w:tc',ns)] for tr in mt.findall('w:tr',ns)]
plan=json.loads((OUT/'conciliacao_proposta.json').read_text(encoding='utf-8'))
assert matrix==plan['matriz_proposta']
assert sum(c=='?' for row in matrix[1:] for c in row[1:])==38
def interval(r,start,end):
    body=r.find('w:body',ns);n=list(body);lo=next(i for i,p in enumerate(n) if txt(p)==start);hi=next(i for i,p in enumerate(n[lo+1:],lo+1) if txt(p)==end)
    return [E.tostring(p) for p in n[lo:hi]]
assert interval(ar,'INTRODUÇÃO','REVISÃO DA LITERATURA')==interval(br,'INTRODUÇÃO','REVISÃO DA LITERATURA')
assert interval(ar,'MATERIAL E MÉTODOS','REFERÊNCIAS')==interval(br,'MATERIAL E MÉTODOS','REFERÊNCIAS')
def refs(r):
    pars=r.xpath('./w:body/w:p',namespaces=ns);i=next(i for i,p in enumerate(pars) if txt(p)=='REFERÊNCIAS');return [txt(p) for p in pars[i+1:] if txt(p).strip()]
old,new=refs(ar),refs(br)
assert len(old)==50 and len(new)==51
for s in old:
    assert s in new or (s.startswith('JAEGER, Herbert. Echo state network.') and any(n.startswith(s) for n in new))
alltext=''.join(br.xpath('//w:t/text()',namespaces=ns))
assert '\ufffd' not in alltext
assert alltext.count('?')==49
assert 'Schmidhuber et al. (2007, p. 772)' in alltext
assert 'em 27 documentos' in alltext and 'tem seis registros diretos' in alltext
v={'base':'v009','sha256_base':hashlib.sha256(base.read_bytes()).hexdigest(),'sha256_candidata':hashlib.sha256(doc.read_bytes()).hexdigest(),'partes_alteradas':changed,'tabelas_total':14,'tabelas_alteradas_indices':changed_tables,'celulas_alteradas':plan['alteracoes'],'matriz_170_celulas_conferida':True,'insuficientes_restantes':38,'interrogacoes_textuais':49,'referencias_anteriores_preservadas':50,'referencias_total':51,'introducao_identica':True,'metodo_resultados_discussao_conclusao_identicos_xml':True,'imagens_preservadas':5,'figura1_atualizada':True,'validacao_visual':'pendente'}
(OUT/'verificacao_estrutural.json').write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
print('Verificacao estrutural concluida;38insuficiencias permanecem explicitas.')
