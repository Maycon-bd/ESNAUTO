import collections,hashlib,json,pathlib,zipfile
from xml.etree import ElementTree as E
out=pathlib.Path(__file__).resolve().parent
root=out.parents[1]
doc=root/'reports/monografia/versoes/v009/MayconGarciaSilva_monografia_v009.docx'
sha=hashlib.sha256(doc.read_bytes()).hexdigest()
assert sha=='793910fae2daaa2d5dbdcfa0cd76177c6c6a38c353d98d94ecaaaecf118c7b03'
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
r=E.fromstring(zipfile.ZipFile(doc).read('word/document.xml'))
tables=r.findall('.//w:tbl',ns)
matrix=None
for t in tables:
    rows=[[''.join(x.text or '' for x in c.findall('.//w:t',ns)) for c in tr.findall('w:tc',ns)] for tr in t.findall('w:tr',ns)]
    if len(rows)==35 and len(rows[0])==6: matrix=rows
assert matrix
dec=json.loads((out/'decisoes_41_em_consolidacao.json').read_text(encoding='utf-8'))
new=[list(row) for row in matrix]
changes=[]
for d in dec['decisoes']:
    i=d['linha_word'];j=int(d['dimensao'][1:])
    assert matrix[i][0]==d['autor'] and matrix[i][j]=='?'
    if d['proposta']!='?':
        new[i][j]=d['proposta']
        changes.append({'linha_word':i,'autor':d['autor'],'dimensao':d['dimensao'],'antes':'?','depois':d['proposta']})
def counts(m):
    return {f'P{j}':dict(collections.Counter(row[j] for row in m[1:])) for j in range(1,6)}
before=counts(matrix);after=counts(new)
assert all(sum(c.values())==34 for c in after.values())
assert len(changes)==3
data={'base':'v009','sha256_base':sha,'status':'proposta_concreta_ainda_nao_incorporada_ao_word','alteracoes':changes,'contagens_antes':before,'contagens_depois':after,'matriz_proposta':new,'leitura_integral_de_todas_as_fontes':False,'avisos':['Contagens derivadas da v009, não das tabelas históricas; os valores de D/S/NA mudaram em revisões anteriores.','Apenas três decisões têm evidência nova suficiente;38insuficiências não foram preenchidas por inferência.']}
(out/'conciliacao_proposta.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'alteracoes':changes,'antes':before,'depois':after},ensure_ascii=True))
