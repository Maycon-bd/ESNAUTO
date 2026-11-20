import json,re
from pathlib import Path
from docx import Document
from docx.shared import Inches,Pt,RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

BUILD=Path(__file__).resolve().parent
OUT=BUILD.parent/'entrega'
slides=json.loads((BUILD/'conteudo.json').read_text(encoding='utf-8'))
doc=Document()
sec=doc.sections[0]
sec.page_width=Inches(8.27);sec.page_height=Inches(11.69)
sec.top_margin=Inches(.7);sec.bottom_margin=Inches(.65)
sec.left_margin=sec.right_margin=Inches(.8)
sec.header_distance=sec.footer_distance=Inches(.3)
for name in ['Normal','Title','Subtitle','Heading 1','Heading 2']:
 st=doc.styles[name];st.font.name='Arial';st.font.color.rgb=RGBColor(0,0,0)
 st.paragraph_format.space_after=Pt(7)
for st in doc.styles:
 for border in st.element.xpath('.//w:pBdr'):
  border.getparent().remove(border)
doc.styles['Normal'].font.size=Pt(12)
doc.styles['Normal'].paragraph_format.line_spacing=1.15
doc.styles['Title'].font.size=Pt(23)
doc.styles['Heading 1'].font.size=Pt(15)
doc.styles['Heading 2'].font.size=Pt(12)
header=sec.header.paragraphs[0];header.text='ESNAUTO   Roteiro de gravação';header.style='Normal'
header.runs[0].font.size=Pt(9)
footer=sec.footer.paragraphs[0];footer.alignment=2
r=footer.add_run();r.font.size=Pt(9)
fld=OxmlElement('w:fldSimple');fld.set(qn('w:instr'),'PAGE');r._r.addnext(fld)
doc.add_paragraph('Roteiro de apresentação da monografia',style='Title')
doc.add_paragraph('Maycon Garcia Silva',style='Subtitle')
doc.add_paragraph('Gravação prévia para a banca examinadora com duração planejada de 25 minutos. Este roteiro acompanha os 23 slides baseados na versão editorial v008 da monografia.')
doc.add_heading('Como usar o roteiro',level=1)
for text in [
 'As falas estão em primeira pessoa. Leia apenas os parágrafos sob “Fala”. As indicações de tempo, troca de slide e fontes servem para preparação e consulta.',
 'O texto tem aproximadamente 2.950 palavras. As janelas somam 25 minutos e incluem a troca dos slides e pausas curtas. A duração real depende da sua velocidade de fala e deve ser ajustada em um ensaio cronometrado.',
 'Use os horários como pontos de controle. Faça uma breve pausa ao concluir cada ideia. Na apresentação, explique o significado dos números e permita que a banca veja os valores completos na tela.',
 'Grave a tela em 16:9, com áudio claro e notificações desativadas. Teste o microfone e confira a primeira transição antes de gravar a versão completa. As falas também estão nas notas do PowerPoint.'
]:doc.add_paragraph(text)
doc.add_heading('Pontos de controle',level=1)
for text in ['05:10   Início da explicação da ESN','09:50   Apresentação do ESNAUTO','11:45   Início dos resultados históricos','15:00   Rodada controlada complementar','19:45   Avaliação das hipóteses','24:15   Início da conclusão','25:00   Encerramento']:
 p=doc.add_paragraph(text);p.paragraph_format.space_after=Pt(3)
doc.add_heading('Base utilizada',level=1)
p=doc.add_paragraph('Monografia v008. Os três blocos de evidência permanecem separados: 45 execuções históricas, rodada controlada DM e lote ilustrativo de 200 gerações. As propostas de continuidade são possibilidades para estudos posteriores.');p.runs[0].font.size=Pt(10)
doc.add_page_break()
for i,s in enumerate(slides):
 doc.add_heading(f'{s["number"]:02d}  {s["title"]}',level=1)
 p=doc.add_paragraph(f'{s["window"]}   Duração planejada {s["seconds"]} s');p.runs[0].bold=True;p.runs[0].font.size=Pt(10)
 p=doc.add_paragraph('Fala');p.runs[0].bold=True;p.paragraph_format.space_after=Pt(3)
 # Blocos breves para facilitar a leitura durante a gravação.
 sentences=re.split(r'(?<=[.!?])\s+',s['speech'])
 for k in range(0,len(sentences),3):doc.add_paragraph(' '.join(sentences[k:k+3]))
 p=doc.add_paragraph('Troca de slide ao concluir a fala.' if s['number']<23 else 'Encerre a gravação após uma pausa breve.');p.runs[0].italic=True;p.runs[0].font.size=Pt(9)
 p=doc.add_paragraph('Apoio para consulta: '+s['source']);p.runs[0].font.size=Pt(8);p.paragraph_format.space_after=Pt(10)
 if (i%2==1 or i==len(slides)-1) and i<len(slides)-1:doc.add_page_break()
doc.save(OUT/'Roteiro_video_ESNAUTO_25min_v008.docx')

lines=['# Roteiro de apresentação da monografia','','Maycon Garcia Silva · Base editorial v008','','Duração planejada: **25 minutos**, em 23 slides. Aproximadamente 2.950 palavras. A duração real depende do ritmo de fala: faça um ensaio cronometrado. As janelas incluem pausas curtas e troca de slides. As fontes e orientações não fazem parte da fala.','','## Cronograma','','| Slide | Intervalo | Tema |','|---|---|---|']
for s in slides:lines.append(f'| {s["number"]:02d} | {s["window"]} | {s["title"]} |')
for s in slides:
 lines.extend(['',f'## {s["number"]:02d} {s["title"]}','',f'**{s["window"]} · {s["seconds"]} segundos**','','### Fala','',s['speech'],'','*Apoio para consulta: '+s['source']+'*'])
(OUT/'Roteiro_video_ESNAUTO_25min_v008.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('Roteiro Word e texto gravados')
