"""Três ajustes locais; preserva todas as partes OOXML não afetadas."""
from pathlib import Path
from lxml import etree as E
import zipfile,json,hashlib,re
from copy import deepcopy
from docx import Document
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
SRC=ROOT/'reports/monografia/versoes/v007/MayconGarciaSilva_monografia_v007.docx'
DEST=ROOT/'reports/monografia/trabalho/revalidacao_cinco_skills_v007.docx'
assert hashlib.sha256(SRC.read_bytes()).hexdigest()=='983c46424ad039472bb12071540d392d73eb29cb08a07e0bc784e0ede008ff1c'
assert SRC.read_bytes()==DEST.read_bytes()
origin=json.loads(Path(str(DEST)+'.origem.json').read_text(encoding='utf-8-sig'))
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
W='{'+ns['w']+'}';XML='{http://www.w3.org/XML/1998/namespace}'
with zipfile.ZipFile(SRC) as z:
    root=E.fromstring(z.read('word/document.xml'))
changes=[]
targets=[('Busca GA por cenário ESN','Busca por AG por cenário ESN','siglas-checker-docx: uniformizar sigla genérica; não alterar nome do pacote GA'),('O ajuste analítico de aproximadamente 0,05 segundo','A Tabela 5 apresenta a decomposição do custo computacional. O ajuste analítico de aproximadamente 0,05 segundo','quadro-tabela-validator-docx e tcc-writer-docx: chamada local sem resultado novo'),('Nos quatro testes, a hipótese nula de igualdade de acurácia preditiva foi rejeitada ao nível de 5%.','Nos quatro testes apresentados na Tabela 6, a hipótese nula de igualdade de acurácia preditiva foi rejeitada ao nível de 5%.','quadro-tabela-validator-docx e tcc-writer-docx: chamada local sem alterar inferência')]
for before,after,why in targets:
    found=[]
    for p in root.findall('.//'+W+'p'):
        text=''.join(t.text or '' for t in p.findall('.//'+W+'t'))
        if before in text:found.append((p,text))
    assert len(found)==1,(before,len(found))
    p,txt=found[0];start=txt.index(before);end=start+len(before)
    nodes=p.findall('.//'+W+'t');offset=0;placed=False
    for t in nodes:
        s=t.text or '';a,b=offset,offset+len(s);offset=b
        if a<end and b>start:
            new=s[:max(0,start-a)]+(after if not placed else '')+s[max(0,end-a):]
            t.text=new;t.set(XML+'space','preserve');placed=True
    final=''.join(t.text or '' for t in p.findall('.//'+W+'t'))
    assert final==txt.replace(before,after)
    changes.append({'antes':txt,'depois':final,'motivo':why,'caracteres_depois':len(final),'estado':'incorporado'})
    assert len(final)<700
with zipfile.ZipFile(SRC) as z,zipfile.ZipFile(DEST,'w',zipfile.ZIP_DEFLATED) as writer:
    for item in z.infolist():writer.writestr(item,E.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True) if item.filename=='word/document.xml' else z.read(item.filename))
with zipfile.ZipFile(SRC) as a,zipfile.ZipFile(DEST) as b:
    assert a.namelist()==b.namelist()
    different=[n for n in a.namelist() if a.read(n)!=b.read(n)]
    assert different==['word/document.xml']
old=Document(SRC);new=Document(DEST)
assert len(old.paragraphs)==len(new.paragraphs)
diffs=[]
for i,(a,b) in enumerate(zip(old.paragraphs,new.paragraphs)):
    if a.text!=b.text:diffs.append({'local':f'P{i:04}','antes':a.text,'depois':b.text})
for ti,(t,u) in enumerate(zip(old.tables,new.tables)):
    for ri,(r,s) in enumerate(zip(t.rows,u.rows)):
        for ci,(a,b) in enumerate(zip(r.cells,s.cells)):
            if a.text!=b.text:diffs.append({'local':f'T{ti:02} L{ri+1} C{ci+1}','antes':a.text,'depois':b.text})
assert len(diffs)==3
expected={x['antes']:x['depois'] for x in changes}
assert all(expected[x['antes']]==x['depois'] for x in diffs)
# Os únicos números adicionados são os localizadores Tabela 5/Tabela 6.
assert [x.text for x in old.paragraphs if x.style.name=='Referencias']==[x.text for x in new.paragraphs if x.style.name=='Referencias']
record={'base':'v007','sha256_base':hashlib.sha256(SRC.read_bytes()).hexdigest(),'candidata':str(DEST.relative_to(ROOT)),'sha256_candidata':hashlib.sha256(DEST.read_bytes()).hexdigest(),'alteracoes':changes,'diferencas_localizadas':diffs,'partes_modificadas':different,'outras_partes_identicas':True,'referencias_preservadas':50,'limite':'Ajustes de navegação e sigla; sem mudança de informação científica, valores ou fontes. Preservada origem de trabalho.'}
(OUT/'alteracoes_aplicadas.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
print('Três ajustes incorporados; somente document.xml alterado; demais partes preservadas.')
