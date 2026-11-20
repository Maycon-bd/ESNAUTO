from pathlib import Path
import json,re,zipfile,hashlib,copy
from PIL import Image
from docx import Document
from lxml import etree as E
B=Path(__file__).resolve().parent;R=B.parents[1]
base=R/'reports/monografia/versoes/v010/MayconGarciaSilva_monografia_v010.docx';work=R/'reports/monografia/trabalho/declaracao_ia_20261102.docx'
with zipfile.ZipFile(base) as a,zipfile.ZipFile(work) as b:
    assert a.namelist()==b.namelist()
    altered=[n for n in a.namelist() if a.read(n)!=b.read(n)]
    assert altered==['word/document.xml']
old=Document(base);new=Document(work)
norm=lambda s:s.rsplit('\t',1)[0] if '\t' in s and s.rsplit('\t',1)[-1].isdigit() else s
it=iter(new.paragraphs)
for p in old.paragraphs:assert any(norm(q.text)==norm(p.text) for q in it),p.text
assert len(new.tables)==len(old.tables)+1
for i,(a,b) in enumerate(zip(old.tables,new.tables)):
    assert len(a.rows)==len(b.rows) and len(a.columns)==len(b.columns)
    assert [[c.text for c in row.cells] for row in a.rows]==[[c.text for c in row.cells] for row in b.rows]
    if i not in [3,4,5,6]:assert E.tostring(a._tbl)==E.tostring(b._tbl)
data=json.loads((B/'alteracoes.json').read_text(encoding='utf-8'))
assert data['paragrafos_metodologia'][0] in [p.text for p in new.paragraphs]
assert new.paragraphs[-1].text=='Assinatura do(a) Professor(a) Orientador(a)\nProf. Dr. Fabian Corrêa Cardoso'
assert 'OpenAI Codex; versão não informada'==data['rows'][2][1]
assert len(new.tables[-1].columns)==4
locator=json.loads((B/'mapa_final.json').read_text(encoding='utf-8-sig'))
items=[x for x in locator['items'] if '\t' not in x['title']]
normalize=lambda s:' '.join(s.replace('–','-').replace('—','-').split()).casefold()
entries=[]
for p in new.paragraphs:
    if '\t' not in p.text or not re.search(r'\t\d+\s*$',p.text):continue
    parts=p.text.split('\t');title=parts[-2];target='ANEXO' if title=='ANEXOS' else title
    found=[x for x in items if normalize(x['title'])==normalize(target)]
    if len(found)>1 and len(parts)>=3:found=[x for x in found if x['number']==parts[0].strip()]
    assert len(found)==1,(p.text,found)
    assert int(parts[-1])==found[0]['page'],(p.text,found)
    entries.append({'entrada':p.text,'pagina':found[0]['page']})
assert len(entries)==61
def signature(p):
    im=Image.open(p).convert('RGB');return hashlib.sha256(im.crop((0,145,im.width,im.height)).tobytes()).hexdigest()
source={}
for p in (B/'word_base').glob('page-*.png'):source.setdefault(signature(p),[]).append(int(p.stem.split('-')[-1]))
changed=[];same=[]
for i in range(1,locator['pages']+1):
    found=source.get(signature(B/f'word_final/page-{i}.png'),[])
    if found:same.append({'pagina':i,'base':found})
    else:changed.append(i)
q={'base':'v010','base_sha256':hashlib.sha256(base.read_bytes()).hexdigest(),'trabalho_sha256':hashlib.sha256(work.read_bytes()).hexdigest(),'paginas':locator['pages'],'partes_alteradas':altered,'paragrafos_anteriores_preservados':len(old.paragraphs),'tabelas_anteriores_com_dados_preservados':len(old.tables),'tabelas_curta_metodologia_mantidas_juntas':[3,4,5,6],'entradas_conferidas':entries,'paginas_a_inspecionar':changed,'corpos_identicos':same,'declaracao_sha256':hashlib.sha256((B/'entrega/Declaracao_responsabilidade_coletiva_Maycon.docx').read_bytes()).hexdigest()}
(B/'conferencia_final.json').write_text(json.dumps(q,ensure_ascii=False,indent=2),encoding='utf-8')
print('Paginas',locator['pages'],'corpos identicos',len(same),'a inspecionar',changed)
