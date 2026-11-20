from pathlib import Path
import hashlib,json
from docx import Document
from docx.shared import Cm,Pt,RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT,WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
B=Path(__file__).resolve().parent;O=B/'entrega';O.mkdir(exist_ok=True)
d=Document();s=d.sections[0]
s.page_width=Cm(21);s.page_height=Cm(29.7)
s.top_margin=s.left_margin=Cm(3);s.right_margin=s.bottom_margin=Cm(2)
s.header_distance=s.footer_distance=Cm(1.2)
for name in ['Normal','Title','Subtitle']:
 st=d.styles[name];st.font.name='Times New Roman';st.font.size=Pt(12);st.font.color.rgb=RGBColor(0,0,0)
 st.paragraph_format.line_spacing=1.5;st.paragraph_format.space_before=Pt(0);st.paragraph_format.space_after=Pt(0)
d.styles['Title'].font.bold=True
for st in d.styles:
 for border in st.element.xpath('.//w:pBdr'):
  border.getparent().remove(border)
h=s.header.paragraphs[0];h.alignment=WD_ALIGN_PARAGRAPH.CENTER
r=h.add_run('MINUTA PARA CONFERÊNCIA DOS DECLARANTES');r.bold=True;r.font.size=Pt(9)
p=d.add_paragraph('DECLARAÇÃO DE RESPONSABILIDADE COLETIVA',style='Title');p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.paragraph_format.space_after=Pt(14)
paragraphs=[
'Em observância aos princípios de integridade científica regulamentados pela Portaria CNPq nº 2.664/2026, declaramos que todas as ferramentas de IAG abaixo identificadas foram empregadas estritamente em caráter de auxílio instrumental ao desenvolvimento do TFC.',
'Fica certificado que não houve delegação da autoria intelectual, e que os autores respondem direta e integralmente pela fidedignidade teórica da redação científica, pela correção técnica das arquiteturas de software/jogos geradas, bem como pelo respeito incondicional às normas de integridade, propriedade industrial e direito autoral vigente.'
]
for text in paragraphs:
 p=d.add_paragraph(text);p.alignment=WD_ALIGN_PARAGRAPH.JUSTIFY;p.paragraph_format.first_line_indent=Cm(1.25)
d.add_paragraph().paragraph_format.space_after=Pt(0)
table=d.add_table(rows=1,cols=4);table.alignment=WD_TABLE_ALIGNMENT.CENTER;table.autofit=False
widths=[3.0,3.0,5.2,4.8]
headers=['Fase do TFC / Processo','Ferramenta Utilizada','Finalidade Específica e Escopo','Método de Validação Humana Realizado']
rows=[
 ['Revisão do texto e padronização','OpenAI Codex\nModelo/versão a confirmar','Apoio à revisão e reformulação de trechos, clareza da redação, formatação, siglas, estrangeirismos, quadros e tabelas.','Devolutiva textual do orientador recebida pelo autor. Detalhar as demais conferências humanas efetivamente realizadas.'],
 ['Conferência documental e fontes','OpenAI Codex\nModelo/versão a confirmar','Apoio à busca e ao confronto de citações com fontes disponíveis; registro de evidências e de informações insuficientes.','[Informar quais fontes e afirmações foram conferidas pessoalmente pelo autor e/ou orientador.]'],
 ['Automação documental e apresentação','OpenAI Codex\nModelo/versão a confirmar','Scripts de apoio à edição e conferência de documentos; preparação de slides, gráficos e roteiro de apresentação.','[Descrever a leitura, conferência dos resultados e revisão de scripts realizadas pessoalmente.]']
]
for c,t in zip(table.rows[0].cells,headers):c.text=t
for row in rows:
 cells=table.add_row().cells
 for c,t in zip(cells,row):c.text=t
for row in table.rows:
 trpr=row._tr.get_or_add_trPr();trpr.append(OxmlElement('w:cantSplit'))
 for i,c in enumerate(row.cells):
  c.width=Cm(widths[i]);c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.TOP
  tcpr=c._tc.get_or_add_tcPr()
  borders=OxmlElement('w:tcBorders')
  for edge in ['top','left','bottom','right']:
   x=OxmlElement('w:'+edge);x.set(qn('w:val'),'single');x.set(qn('w:sz'),'4');x.set(qn('w:color'),'000000');borders.append(x)
  tcpr.append(borders)
  for p in c.paragraphs:
   p.alignment=WD_ALIGN_PARAGRAPH.LEFT;p.paragraph_format.line_spacing=1;p.paragraph_format.space_after=Pt(3);p.paragraph_format.space_before=Pt(3)
   for r in p.runs:r.font.size=Pt(10)
for c in table.rows[0].cells:
 for r in c.paragraphs[0].runs:r.bold=True
p=d.add_paragraph('Rio Verde/GO, ______ de ________________________ de 20____.');p.paragraph_format.space_before=Pt(14)
for name,label in [('Maycon Garcia Silva','Assinatura do(a) Acadêmico(a) Autor(a)'),('Prof. Dr. Fabian Corrêa Cardoso','Assinatura do(a) Professor(a) Orientador(a)')]:
 p=d.add_paragraph('_____________________________________________');p.paragraph_format.space_before=Pt(14)
 p=d.add_paragraph(label+'\n'+name);p.paragraph_format.line_spacing=1
 for r in p.runs:r.font.size=Pt(11)
f=s.footer.paragraphs[0];f.alignment=WD_ALIGN_PARAGRAPH.CENTER
r=f.add_run('Campos entre colchetes e versões devem ser conferidos antes da assinatura.');r.font.size=Pt(8)
path=O/'Declaracao_responsabilidade_coletiva_Maycon_MINUTA.docx';d.save(path)
meta={'estado':'minuta com dados a confirmar, sem assinatura','base_editorial':'v010','base_sha256':'1da5ea82344c177d75af723362017e3e558bbb127bd9995f7ec0cbd6964f81ed','monografia_alterada':False,'arquivo':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'origem_texto_institucional':'Anexo 14 - Declaração de Uso de IA.pdf, p. 4','dados_pendentes':['Inventário completo de ferramentas e versões','Validação humana efetivamente realizada','Data e assinaturas dos declarantes']}
(B/'estado.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
print(path)
