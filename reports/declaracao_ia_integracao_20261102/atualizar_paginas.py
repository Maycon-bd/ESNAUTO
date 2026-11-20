from pathlib import Path
import json,re,zipfile
from docx import Document
from lxml import etree as E
B=Path(__file__).resolve().parent;R=B.parents[1];p=R/'reports/monografia/trabalho/declaracao_ia_20261102.docx'
m=json.loads((B/'mapa_map.json').read_text(encoding='utf-8-sig'))
items=[x for x in m['items'] if '\t' not in x['title']]
norm=lambda s:' '.join(s.replace('–','-').replace('—','-').split()).casefold()
d=Document(p);changes=[];entries=[]
for para in d.paragraphs:
    text=para.text
    if '\t' not in text or not re.search(r'\t\d+\s*$',text):continue
    parts=text.split('\t');title=parts[-2]
    target='ANEXO' if title=='ANEXOS' else title
    found=[x for x in items if norm(x['title'])==norm(target)]
    if len(found)>1 and len(parts)>=3:found=[x for x in found if x['number']==parts[0].strip()]
    assert len(found)==1,(text,found)
    page=str(found[0]['page']);entry={'texto':text,'pagina':int(page),'titulo':target};entries.append(entry)
    if parts[-1].strip()==page:continue
    for t in reversed(para._p.xpath('.//w:t')):
        if re.fullmatch(r'\d+\s*',t.text or ''):
            old=t.text;t.text=page;changes.append({'titulo':title,'antes':old,'depois':page});break
    else:raise ValueError(text)
buf=E.tostring(d._element,xml_declaration=True,encoding='UTF-8',standalone=True)
with zipfile.ZipFile(p) as z:contents=[(i,z.read(i.filename)) for i in z.infolist()]
with zipfile.ZipFile(p,'w',zipfile.ZIP_DEFLATED) as z:
    for info,data in contents:z.writestr(info,buf if info.filename=='word/document.xml' else data)
(B/'paginas_atualizadas.json').write_text(json.dumps({'entradas_conferidas':len(entries),'mudancas':changes,'entradas':entries},ensure_ascii=False,indent=2),encoding='utf-8')
print('Entradas conferidas',len(entries),'paginas atualizadas',len(changes))
