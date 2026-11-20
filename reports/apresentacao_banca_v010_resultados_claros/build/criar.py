import hashlib,json,re,zipfile,copy
from pathlib import Path
from lxml import etree as E
from docx import Document
from docx.shared import Pt

BUILD=Path(__file__).resolve().parent;ROOT=BUILD.parents[2];OUT=BUILD.parent/'entrega';OUT.mkdir(exist_ok=True,parents=True)
BASE=ROOT/'reports/monografia/versoes/v010/MayconGarciaSilva_monografia_v010.docx'
SHA=hashlib.sha256(BASE.read_bytes()).hexdigest();assert SHA=='1da5ea82344c177d75af723362017e3e558bbb127bd9995f7ec0cbd6964f81ed'
SRC=ROOT/'reports/apresentacao_banca_v010_fala_clara'
slides=json.loads((SRC/'build/conteudo.json').read_text(encoding='utf-8'))
raw=(BUILD/'falas.md').read_text(encoding='utf-8')
blocks=re.split(r'^## \d+\s*\n',raw,flags=re.M)[1:];assert len(blocks)==23
for s,b in zip(slides,blocks):
    s['paragraphs']=[p.strip() for p in b.strip().split('\n\n') if p.strip()]
    s['speech']=' '.join(s['paragraphs']);s['words']=len(s['speech'].split());s['wpm']=round(s['words']*60/s['seconds'])
for i,seconds in {20:75,21:60,22:50,23:60}.items(): slides[i-1]['seconds']=seconds
elapsed=0
for s in slides:
    s['start']=elapsed; elapsed+=s['seconds'];s['end']=elapsed
    stamp=lambda t:f'{t//60:02d}:{t%60:02d}'
    s['window']=stamp(s['start'])+'–'+stamp(s['end'])
    s['wpm']=round(s['words']*60/s['seconds'])
for i,title in {20:'O que o trabalho entregou',21:'Alcance dos resultados e próximos testes',23:'Conclusões para a PETR4'}.items():slides[i-1]['title']=title
assert elapsed==1500
(BUILD/'conteudo.json').write_text(json.dumps(slides,ensure_ascii=False,indent=2),encoding='utf-8')
# Preserve the current script template and its paragraph styles.
doc=Document(SRC/'entrega/Roteiro_ESNAUTO_v010_fala_clara.docx')
body=doc._element.body
for child in list(body):
    if child.tag.endswith('}sectPr'):continue
    body.remove(child)
doc.add_paragraph('Roteiro para apresentar a monografia ESNAUTO',style='Title')
doc.add_paragraph('Maycon Garcia Silva',style='Subtitle')
doc.add_paragraph('Fala revisada para apresentar os resultados e as contribuições com clareza. Acompanha os 23 slides e as notas atualizadas, com planejamento de 25 minutos e base na monografia v010.')
doc.add_heading('Como preparar a gravação',1)
for p in [
'Leia os blocos em voz alta para se familiarizar com a sequência. Depois, procure explicar cada ideia com seu jeito de falar. Não precisa decorar cada frase.',
'As falas estão separadas em parágrafos curtos. Faça uma pausa breve entre as ideias e dê tempo para a banca olhar os gráficos. As fontes e as orientações de consulta não entram na fala.',
f'O roteiro tem {sum(s["words"] for s in slides):,} palavras de fala.'.replace(',','.')+' Os intervalos continuam somando 25 minutos e incluem pausas e troca de slides. Faça um ensaio cronometrado: a duração real depende do seu ritmo.',
'Ao mostrar números, destaque a comparação e o que ela significa. Os valores completos ficam na tela. Se terminar um trecho antes do horário, use o tempo para apontar o gráfico e respirar, sem acelerar a troca de slides.',
'Abra o PowerPoint no modo de apresentação e grave a tela em 16:9. As notas desta cópia contêm a mesma fala do roteiro. Teste o áudio antes de gravar tudo.'
]:doc.add_paragraph(p)
doc.add_heading('Pontos de controle',1)
for p in ['05:10   Funcionamento da ESN','09:50   Sistema ESNAUTO','11:45   Resultados históricos','15:00   Rodada complementar','19:45   Respostas às hipóteses','24:00   Conclusão','25:00   Encerramento']:
    q=doc.add_paragraph(p);q.paragraph_format.space_after=Pt(3)
doc.add_heading('Base de consulta',1)
p=doc.add_paragraph('Monografia v010. As 45 execuções históricas, a rodada complementar DM e o lote ilustrativo de 200 gerações continuam separados. Os resultados e seus limites foram preservados.');p.runs[0].font.size=Pt(10)
doc.add_page_break()
for i,s in enumerate(slides):
    doc.add_heading(f'{s["number"]:02d}  {s["title"]}',1)
    q=doc.add_paragraph(f'{s["window"]}   Tempo reservado {s["seconds"]} s');q.runs[0].bold=True;q.runs[0].font.size=Pt(10)
    q=doc.add_paragraph('Fala');q.runs[0].bold=True;q.paragraph_format.space_after=Pt(3)
    for text in s['paragraphs']:doc.add_paragraph(text)
    q=doc.add_paragraph('Faça uma pausa e troque o slide.' if i<22 else 'Faça uma pausa breve e encerre a gravação.');q.runs[0].italic=True;q.runs[0].font.size=Pt(9)
    q=doc.add_paragraph('Consulta fora da fala: '+s['source']);q.runs[0].font.size=Pt(8)
    if i%2==1 and i<22:doc.add_page_break()
doc.save(OUT/'Roteiro_ESNAUTO_v010_resultados_claros.docx')
lines=['# Roteiro ESNAUTO com fala clara','','Base editorial v010. Planejamento de 25 minutos. Fontes e orientações ficam fora da fala. A duração real depende do ensaio.']
for s in slides:
    lines+=['',f'## {s["number"]:02d} {s["title"]}','',f'{s["window"]} · {s["seconds"]} segundos reservados','']
    for p in s['paragraphs']:lines+=[p,'']
    lines+=['Consulta fora da fala: '+s['source']]
(OUT/'Roteiro_ESNAUTO_v010_resultados_claros.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main'}
srcdeck=SRC/'entrega/Apresentacao_ESNAUTO_v010_notas_fala_clara.pptx'
changed=[]
with zipfile.ZipFile(srcdeck) as a,zipfile.ZipFile(BUILD/'candidate.pptx','w',zipfile.ZIP_DEFLATED) as b:
    for info in a.infolist():
        buf=a.read(info.filename)
        sm=re.fullmatch(r'ppt/slides/slide(\d+)\.xml',info.filename)
        edits=json.loads((BUILD/'textos_slides.json').read_text(encoding='utf-8'))
        if sm and sm[1] in edits:
            rt=E.fromstring(buf)
            for name,text in edits[sm[1]].items():
                shapes=rt.xpath('//p:sp[p:nvSpPr/p:cNvPr[@name="'+name+'"]]',namespaces=ns)
                assert len(shapes)==1,(sm[1],name)
                tt=shapes[0].xpath('.//a:t',namespaces=ns);assert len(tt)==1,(sm[1],name,len(tt))
                tt[0].text=text
            buf=E.tostring(rt,xml_declaration=True,encoding='UTF-8',standalone=True)
        m=re.fullmatch(r'ppt/notesSlides/notesSlide(\d+)\.xml',info.filename)
        if m:
            s=slides[int(m[1])-1];root=E.fromstring(buf)
            target=root.xpath('//p:sp[p:nvSpPr/p:nvPr/p:ph[@type="body"]]/p:txBody',namespaces=ns)
            assert len(target)==1
            tb=target[0];template=tb.find('a:p',ns);assert template is not None
            for p in list(tb.findall('a:p',ns)):tb.remove(p)
            paras=[f'{s["window"]} | Tempo reservado {s["seconds"]} s','',*s['paragraphs'],'',
                'Fonte e rastreabilidade: '+s['source'],f'Base v010 SHA256 {SHA}.',
                'Operação: transição por clique. As falas correspondem ao roteiro com linguagem clara. Para a gravação de 25 minutos, seguir a ordem numérica e conferir o tempo em ensaio.']
            for text in paras:
                p=copy.deepcopy(template)
                for c in list(p):
                    if c.tag!=f'{{{ns["a"]}}}pPr':p.remove(c)
                r=E.SubElement(p,f'{{{ns["a"]}}}r');t=E.SubElement(r,f'{{{ns["a"]}}}t');t.text=text
                tb.append(p)
            buf=E.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True);changed.append(info.filename)
        b.writestr(info,buf)
assert len(changed)==23
stats={'base':'v010','base_sha256':SHA,'slides':23,'segundos_planejados':1500,'palavras':sum(s['words'] for s in slides),'wpm':[{k:s[k] for k in ['number','words','seconds','wpm']} for s in slides],'partes_pptx_alteradas':changed,'origem_pptx_sha256':hashlib.sha256(srcdeck.read_bytes()).hexdigest()}
(BUILD/'rastreabilidade.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(stats,ensure_ascii=True,indent=2))
