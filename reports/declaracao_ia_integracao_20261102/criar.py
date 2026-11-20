from pathlib import Path
import json,copy,zipfile,hashlib,re
from lxml import etree as E
from docx import Document
from docx.shared import Pt,Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
B=Path(__file__).resolve().parent;R=B.parents[1];O=B/'entrega';O.mkdir(exist_ok=True,parents=True)
WIP=R/'reports/monografia/trabalho/declaracao_ia_20261102.docx'
BASE=R/'reports/monografia/versoes/v010/MayconGarciaSilva_monografia_v010.docx'
assert hashlib.sha256(BASE.read_bytes()).hexdigest()=='1da5ea82344c177d75af723362017e3e558bbb127bd9995f7ec0cbd6964f81ed'
rows=[
 ['Extração dos dados','Script próprio em Python; Gemini 2.5 Flash; temperatura 0','Preenchimento inicial do formulário a partir do PDF de cada publicação, com trecho, localização e justificativa de cada resposta.','Conferência pessoal dos artigos pelo autor.'],
 ['Revisão e leitura do texto','Claude e OpenAI Codex; versões não informadas','Auxílio à revisão e reformulação de trechos, leitura assistida, correção linguística e conferência documental.','Leitura com auxílio de IA e conferência pessoal dos artigos pelo autor; devolutiva textual do orientador.'],
 ['Execução de testes','Scripts de teste e apoio de IAG; ferramenta específica não informada','Apoio à preparação, execução e análise de testes.','Execução de testes pelo autor, tanto pessoalmente quanto com auxílio de IA.'],
 ['Padronização e apresentação','OpenAI Codex; versão não informada','Apoio à formatação, a scripts de conferência documental e à preparação de slides e roteiro.','Análise e solicitação de ajustes pelo autor; correções textuais do orientador na monografia.']
]
if (B/'complemento_testes.json').exists():
    c=json.loads((B/'complemento_testes.json').read_text(encoding='utf-8'))
    rows[2][1]=c['ferramenta']
source=(R/'reports/declaracao_ia_20261102/criar_minuta.py').read_text(encoding='utf-8')
source=source[:source.index("meta={'estado'")]
source=source.replace("rows=[",'rows='+repr(rows)+'\nOLD_ROWS=[').replace('for row in rows:','for row in rows:')
source=source.replace("r=h.add_run('MINUTA PARA CONFERÊNCIA DOS DECLARANTES');r.bold=True;r.font.size=Pt(9)",'')
source=source.replace("r=f.add_run('Campos entre colchetes e versões devem ser conferidos antes da assinatura.');r.font.size=Pt(8)",'')
source=source.replace('Declaracao_responsabilidade_coletiva_Maycon_MINUTA.docx','Declaracao_responsabilidade_coletiva_Maycon.docx')
exec(compile(source,str(B/'modelo_preenchido.py'),'exec'),{'__file__':str(B/'modelo_preenchido.py')})
decl=Document(O/'Declaracao_responsabilidade_coletiva_Maycon.docx')
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
texts=[
'Na extração bibliográfica, utilizou-se Gemini 2.5 Flash, temperatura 0, por script próprio em Python. Claude e OpenAI Codex apoiaram a revisão e a leitura; Codex também apoiou os testes. O autor conferiu pessoalmente os artigos e executou testes. O escopo e a validação humana do uso de inteligência artificial generativa (IAG) constam da declaração no Anexo A.'
]
with zipfile.ZipFile(BASE) as z:xml=E.fromstring(z.read('word/document.xml'))
body=xml.find('w:body',ns);pars=body.findall('w:p',ns)
tables=body.findall('w:tbl',ns)
# Keep the four short methodological tables together after the added paragraph.
# Their cells, numbers and wording are preserved.
for ti in [3,4,5,6]:
    table=tables[ti]
    ps=table.findall('.//w:p',ns)
    for pi,pp in enumerate(ps):
        pr=pp.find('w:pPr',ns)
        if pr is None:pr=E.Element(qn('w:pPr'));pp.insert(0,pr)
        keep=pr.find('w:keepNext',ns)
        if keep is None:keep=E.SubElement(pr,qn('w:keepNext'))
        keep.set(qn('w:val'),'1' if pi<len(ps)-1 else '0')
def txt(p):return ''.join(p.xpath('.//w:t/text()',namespaces=ns))
anchor=next(p for p in pars if txt(p).startswith('A reexecução e a auditabilidade do protocolo'))
template=anchor
added=[]
for s in texts:
    p=copy.deepcopy(template)
    for child in list(p):
        if child.tag!=qn('w:pPr'):p.remove(child)
    for x in p.xpath('./w:pPr/w:sectPr',namespaces=ns):x.getparent().remove(x)
    for part in re.split(r'(\bscript\b)',s):
        if not part:continue
        run=E.SubElement(p,qn('w:r'))
        if part=='script':
            rp=E.SubElement(run,qn('w:rPr'));E.SubElement(rp,qn('w:i'))
        t=E.SubElement(run,qn('w:t'));t.text=part
        if part.startswith(' ') or part.endswith(' '):t.set('{http://www.w3.org/XML/1998/namespace}space','preserve')
    anchor.addnext(p);anchor=p;added.append(s)
# No original text paragraph is changed; only two methodological paragraphs and annex material are added.
def p_new(text,pagebreak=False,bold=False):
    p=OxmlElement('w:p');pr=OxmlElement('w:pPr');p.append(pr)
    if pagebreak:pr.append(OxmlElement('w:pageBreakBefore'))
    j=OxmlElement('w:jc');j.set(qn('w:val'),'center');pr.append(j)
    sp=OxmlElement('w:spacing');sp.set(qn('w:before'),'0');sp.set(qn('w:after'),'360');sp.set(qn('w:line'),'360');sp.set(qn('w:lineRule'),'auto');pr.append(sp)
    ind=OxmlElement('w:ind');ind.set(qn('w:firstLine'),'0');ind.set(qn('w:left'),'0');pr.append(ind)
    r=OxmlElement('w:r');rp=OxmlElement('w:rPr');r.append(rp)
    f=OxmlElement('w:rFonts');f.set(qn('w:ascii'),'Times New Roman');f.set(qn('w:hAnsi'),'Times New Roman');rp.append(f)
    sz=OxmlElement('w:sz');sz.set(qn('w:val'),'24');rp.append(sz)
    b=OxmlElement('w:b');b.set(qn('w:val'),'1' if bold else '0');rp.append(b)
    tt=OxmlElement('w:t');tt.text=text;r.append(tt);p.append(r);return p
sect=body.find('w:sectPr',ns)
openp=p_new('ANEXO',True,True);sect.addprevious(openp)
head=p_new('ANEXO A – Declaração de responsabilidade coletiva',True,False);sect.addprevious(head)
for i,child in enumerate(decl._element.body):
    if i==0 or child.tag==qn('w:sectPr'):continue
    c=copy.deepcopy(child)
    for pp in list(c.iter(qn('w:p'))) if c.tag!=qn('w:p') else [c]:
        pr=pp.find('w:pPr',ns)
        if pr is None:pr=E.Element(qn('w:pPr'));pp.insert(0,pr)
        ind=pr.find('w:ind',ns)
        if ind is None:ind=E.SubElement(pr,qn('w:ind'))
        if c.tag!=qn('w:p') or ind.get(qn('w:firstLine')) is None:ind.set(qn('w:firstLine'),'0')
        if c.tag!=qn('w:p'):
            ind.set(qn('w:left'),'0');ind.set(qn('w:right'),'0')
    if c.tag==qn('w:p'):
        # The institutional form uses direct font/spacing, independent of the monograph's styles.
        pr=c.find('w:pPr',ns)
        if pr is not None:
            for st in pr.findall('w:pStyle',ns):pr.remove(st)
        for run in c.findall('.//w:r',ns):
            rp=run.find('w:rPr',ns)
            if rp is None:rp=E.SubElement(run,qn('w:rPr'));run.remove(rp);run.insert(0,rp)
            for tag,val in [('w:rFonts',None),('w:sz','24')]:
                el=rp.find(tag,ns)
                if el is None:el=E.SubElement(rp,qn(tag))
                if val:el.set(qn('w:val'),val)
                else:el.set(qn('w:ascii'),'Times New Roman');el.set(qn('w:hAnsi'),'Times New Roman')
    sect.addprevious(c)
# Add an unnumbered TOC entry, following the existing references entry formatting.
toc=next(p for p in pars if txt(p).startswith('REFERÊNCIAS') and p.find('w:pPr/w:pStyle',ns) is not None and p.find('w:pPr/w:pStyle',ns).get(qn('w:val'))=='Sumrio1')
entry=copy.deepcopy(toc)
tt=entry.xpath('.//w:t',namespaces=ns)
assert len(tt)>=2
for t in tt:t.text=''
tt[0].text='ANEXOS';tt[-1].text='78'
toc.addnext(entry)
with zipfile.ZipFile(BASE) as a,zipfile.ZipFile(WIP,'w',zipfile.ZIP_DEFLATED) as z:
    for info in a.infolist():z.writestr(info,E.tostring(xml,xml_declaration=True,encoding='UTF-8',standalone=True) if info.filename=='word/document.xml' else a.read(info.filename))
(B/'alteracoes.json').write_text(json.dumps({'base':'v010','base_sha256':hashlib.sha256(BASE.read_bytes()).hexdigest(),'paragrafos_metodologia':texts,'rows':rows,'declaracao':str(O/'Declaracao_responsabilidade_coletiva_Maycon.docx'),'trabalho':str(WIP),'declaracao_autor':'Informações fornecidas pelo autor em resposta no chat; versões de Claude e Codex não informadas; data e assinaturas vazias.'},ensure_ascii=False,indent=2),encoding='utf-8')
print('Copia e declaracao preenchida preparadas.')
