from pathlib import Path
import hashlib, json, zipfile
from lxml import etree as E
B=Path(__file__).resolve().parent; R=B.parents[1]
O=B/'entrega'; O.mkdir(exist_ok=True,parents=True)
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
q=lambda t:'{'+NS['w']+'}'+t
base=R/'reports/monografia/versoes/v012/MayconGarciaSilva_monografia_v012.docx'
work=R/'reports/monografia/trabalho/declaracao_ia_assinaturas_20261102.docx'
decl=O/'Declaracao_responsabilidade_coletiva_Maycon_assinaturas.docx'
assert hashlib.sha256(base.read_bytes()).hexdigest()=='37feaaa77a3257c9e0b2dbc414dfbbaef55db0a14f24e50d8532aa44d0a3a398'
def edit(src,dst):
 with zipfile.ZipFile(src) as z:
  root=E.fromstring(z.read('word/document.xml')); body=root.find('w:body',NS)
  # Restrict changes to the declaration's last page, after its table.
  nodes=list(body); ti=max(i for i,x in enumerate(nodes) if x.tag==q('tbl'))
  table=nodes[ti]
  for p in table.findall('.//w:p',NS):
   txt=''.join(p.xpath('.//w:t/text()',namespaces=NS))
   replacement={'Formatação e material de defesa':'Formatação da monografia',
                'Ajustes na apresentação do documento, verificações por scripts e elaboração de slides e roteiro.':'Ajustes de formatação da monografia e apoio a verificações documentais por scripts.'}.get(txt)
   if replacement:
    ts=p.xpath('.//w:t',namespaces=NS);ts[0].text=replacement
    for t in ts[1:]:t.text=''
  counts=[0,0]
  for p in nodes[ti+1:]:
   if p.tag!=q('p'):continue
   txt=''.join(p.xpath('.//w:t/text()',namespaces=NS))
   if txt.startswith('Rio Verde/GO,'):
    ts=p.xpath('.//w:t',namespaces=NS); assert ts
    ts[0].text='Rio Verde/GO, 2 de novembro de 2026.'
    for t in ts[1:]:t.text=''
    counts[0]+=1
   if txt=='_____________________________________________':
    pr=p.find('w:pPr',NS)
    if pr is None:pr=E.Element(q('pPr'));p.insert(0,pr)
    sp=pr.find('w:spacing',NS)
    if sp is None:sp=E.SubElement(pr,q('spacing'))
    sp.set(q('before'),'960') # 48 pt above each signature line (previously 14 pt).
    counts[1]+=1
  assert counts==[1,2],counts
  with zipfile.ZipFile(dst,'w',zipfile.ZIP_DEFLATED) as out:
   for info in z.infolist():out.writestr(info,E.tostring(root,encoding='UTF-8',xml_declaration=True,standalone=True) if info.filename=='word/document.xml' else z.read(info.filename))
edit(base,work)
edit(R/'reports/declaracao_ia_reescrita_20261102/entrega/Declaracao_responsabilidade_coletiva_Maycon_reescrita.docx',decl)
previous=R/'reports/declaracao_ia_reescrita_20261102'
src=(previous/'word_qa.ps1').read_text(encoding='utf-8-sig').replace('declaracao_ia_reescrita_20261102',B.name).replace('versoes\\v011\\MayconGarciaSilva_monografia_v011.docx','versoes\\v012\\MayconGarciaSilva_monografia_v012.docx').replace('Declaracao_responsabilidade_coletiva_Maycon_reescrita.docx',decl.name)
(B/'word_qa.ps1').write_text(src,encoding='utf-8-sig')
src=(previous/'renderizar.py').read_text(encoding='utf-8').replace('declaracao_ia_reescrita_20261102',B.name).replace('Declaracao_responsabilidade_coletiva_Maycon_reescrita.docx',decl.name)
(B/'renderizar.py').write_text(src,encoding='utf-8')
(B/'alteracoes.json').write_text(json.dumps({'base':'v012','base_sha256':hashlib.sha256(base.read_bytes()).hexdigest(),'data':'2 de novembro de 2026','espaco_antes_das_linhas_pt':48,'espaco_anterior_pt':14,'comentarios_atendidos':['Ampliar espaço para assinaturas gov.br','Preencher data de hoje','Retirar elaboração de slides e roteiro da declaração'],'assinaturas':'Campos vazios; nenhuma assinatura aplicada.'},ensure_ascii=False,indent=2),encoding='utf-8')
print('Data preenchida; espaço antes de cada assinatura ampliado de 14 para 48 pontos.')
