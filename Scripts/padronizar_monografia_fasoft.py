"""Padronização institucional em cópia própria; não executa experimentos."""
from pathlib import Path
from copy import deepcopy
import re, json, hashlib
from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH as A, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'reports/monografia/MayconGarciaSilva_monografia_observacoes_atendidas.docx'
DEST=ROOT/'reports/monografia/MayconGarciaSilva_monografia_padronizada_FASOFT.docx'
QA=ROOT/'reports/padronizacao_fasoft_20261027'
QA.mkdir(exist_ok=True)
d=Document(SOURCE); old=list(d.paragraphs)
source_hash=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
changes=[]

def setnode(parent,tag,**attrs):
    node=parent.find(qn('w:'+tag))
    if node is None:node=OxmlElement('w:'+tag);parent.append(node)
    for k,v in attrs.items():node.set(qn('w:'+k),str(v))
    return node

def fonts(p,size=12,bold=None,italic=None):
    for r in p.runs:
        r.font.name='Times New Roman';r.font.size=Pt(size);r.font.color.rgb=RGBColor(0,0,0)
        if bold is not None:r.bold=bold
        if italic is not None:r.italic=italic

def pf(p,line=1.5,indent=1.25,align=A.JUSTIFY,before=0,after=0):
    f=p.paragraph_format;f.line_spacing=line;f.first_line_indent=Cm(indent)
    f.left_indent=Cm(0);f.right_indent=Cm(0);f.alignment=align
    f.space_before=Pt(before);f.space_after=Pt(after);f.widow_control=True
    f.keep_with_next=False;f.keep_together=False
    f.page_break_before=False

def replace(p,text,why):
    changes.append({'tipo':'texto','antes':p.text,'depois':text,'motivo':why})
    p.clear();p.add_run(text)

# Reorganização da introdução segundo pp. 13–14 e 25: sem citações, enumerações
# de objetivos nem antecipação dos resultados. As hipóteses permanecem literais.
intro=[
'A previsão de preços de ações reúne desafios de análise temporal, escolha de modelos e qualidade dos dados. No mercado brasileiro, esta pesquisa delimita esse problema à previsão de um passo à frente do preço de fechamento ajustado da ação preferencial da Petróleo Brasileiro S.A. (PETR4), negociada na Brasil, Bolsa, Balcão (B3). O interesse está em avaliar o desempenho preditivo e o custo computacional de configurações de redes neurais sob um protocolo experimental definido, sem interpretar a previsão de preços como demonstração de rentabilidade de uma estratégia de negociação.',
'A abordagem central emprega Redes Neurais de Estados de Eco (Echo State Networks – ESNs), pertencentes à Computação de Reservatório (Reservoir Computing – RC). Nessa arquitetura, as matrizes de entrada e do reservatório, designadas por Win e W, permanecem fixas durante o ajuste da camada de saída. Essa organização motiva o estudo de alternativas à otimização iterativa de todos os pesos. A escolha das distribuições de inicialização e dos hiperparâmetros, entretanto, integra o problema experimental e não permite pressupor superioridade de uma configuração antes de sua avaliação.',
'A pesquisa utiliza preços ajustados para lidar com descontinuidades associadas a eventos corporativos, sem isolar o efeito do Fator de Ajuste por uma ablação. Também distingue o custo da busca por hiperparâmetros do ajuste da configuração selecionada, delimitando a interpretação da acurácia e da eficiência computacional.',
'O problema de pesquisa consiste em investigar em que medida distribuições não gaussianas para Win e W, combinadas a um Algoritmo Genético (AG), alteram a acurácia e o custo computacional de uma ESN na previsão fora da amostra da PETR4 em comparação com inicializações canônicas e com redes Long Short-Term Memory (LSTM) e Gated Recurrent Unit (GRU). A justificativa está na necessidade de documentar essas escolhas de inicialização, avaliá-las em conjunto com os hiperparâmetros e explicitar as condições em que as comparações são sustentadas pelos registros disponíveis.',
'O objetivo geral é investigar o desempenho de ESNs na predição de um passo à frente do preço ajustado da PETR4, com ênfase nas distribuições aplicadas a Win e W e na otimização conjunta dos hiperparâmetros por AG. A busca utiliza inicialização por Amostragem por Hipercubo Latino (Latin Hypercube Sampling – LHS) e mutação cataclísmica inspirada no CHC, denominação de Cross-generational elitist selection, Heterogeneous recombination and Cataclysmic mutation. O mecanismo antiestagnação não corresponde à implementação do CHC completo.',
'Como objetivos específicos, pretende-se consolidar a revisão da literatura; empregar a série histórica ajustada; desenvolver o ESNAUTO, integrando ESN, regressão Ridge e busca genética; e investigar distribuições canônicas, de cauda pesada, assimétricas, esparsas e empiricamente ajustadas. Também se busca otimizar conjuntamente a taxa de vazamento, o raio espectral, o descarte inicial, o tamanho do reservatório e a regularização Ridge por meio de cromossomo binário de 55 bits.',
'A avaliação contempla o Erro Médio Absoluto (Mean Absolute Error – MAE), a Raiz do Erro Quadrático Médio (Root Mean Squared Error – RMSE) e o coeficiente de determinação (R²), a comparação com a ESN Normal × Normal e com LSTM e GRU e a separação entre custo de otimização e ajuste final. Inclui ainda o exame da estabilidade das execuções, a comparação inferencial complementar pelo teste de Diebold–Mariano, a documentação do procedimento e a discussão de limitações e condições de replicação.',
'Cinco hipóteses orientam a pesquisa e são apresentadas a seguir. Sua avaliação deve distinguir resultados descritivos, evidência inferencial e limites de atribuição causal.'
]
intro += [p.text for p in old[295:300]]
intro += ['O trabalho está organizado em revisão da literatura, material e métodos, resultados e discussão, discussão das limitações e conclusão. A revisão fundamenta os modelos e as escolhas de inicialização; a metodologia delimita os procedimentos e os blocos experimentais; os capítulos finais apresentam a avaliação e suas implicações. A extensão a outros ativos permanece como possibilidade de continuidade, preservando a PETR4 como objeto dos resultados principais desta monografia.']
for i,p in enumerate(old[266:301]):
    if i<len(intro):replace(p,intro[i],'Adequação da introdução ao guia, pp. 13–14 e 25; hipóteses preservadas.')
    else:p._p.getparent().remove(p._p)

# Margens reais uniformes; dedicatória e epígrafe posicionadas pelo parágrafo.
for s in d.sections:
    s.page_width=Cm(21);s.page_height=Cm(29.7)
    s.top_margin=Cm(3);s.left_margin=Cm(3);s.right_margin=Cm(2);s.bottom_margin=Cm(2)
    s.header_distance=Cm(2);s.footer_distance=Cm(1.25)
    setnode(s._sectPr,'pgNumType',fmt='decimal')

for name in ['Normal','Caption','Referencias','TITULO TCC','SEÇÃO TCC','SUBÇÃO 2','toc 1','toc 2','toc 3']:
    if name not in d.styles:continue
    st=d.styles[name];st.font.name='Times New Roman';st.font.size=Pt(12);st.font.color.rgb=RGBColor(0,0,0)
    st.paragraph_format.widow_control=True
    if name in ['TITULO TCC','SEÇÃO TCC','SUBÇÃO 2']:
        st.paragraph_format.left_indent=Cm(0);st.paragraph_format.first_line_indent=Cm(0)
for p in d.paragraphs:
    fonts(p)
    pf(p)
    # Remover quebras manuais antigas: quebras passam a ser propriedades de seção/título.
    for br in p._p.xpath('.//w:br[@w:type="page"]'):br.getparent().remove(br)

# Eliminar linhas vazias de diagramação, mantendo os marcos de seção e figuras.
for p in list(d.paragraphs):
    if not p.text.strip() and not p._p.xpath('.//w:drawing|.//m:oMath|.//w:sectPr|.//w:fldChar'):
        p._p.getparent().remove(p._p)

# Capa e folha de rosto: espaços simples previstos nos modelos (pp. 37–38).
for i in [0,1,9,20,47,48,49,70,86,87,95,99]:
    p=old[i];pf(p,1,0,A.CENTER);fonts(p,12,True,False)
old[9].paragraph_format.space_before=Pt(84)
old[20].paragraph_format.space_before=Pt(120)
old[47].paragraph_format.space_before=Pt(240)
old[49].paragraph_format.page_break_before=True
old[70].paragraph_format.space_before=Pt(240)
old[70].paragraph_format.line_spacing=1.5
for i in [75,77,103]:
    p=old[i];pf(p,1,0,A.JUSTIFY);p.paragraph_format.left_indent=Cm(8)
    fonts(p,11,False,False)
old[75].paragraph_format.space_before=Pt(24)
old[77].paragraph_format.space_before=Pt(12)
old[86].paragraph_format.space_before=Pt(108)

# Página da ficha: preserva o espaço oficial, sem inventar conteúdo da biblioteca.
for i in [88,89,90,92]:pf(old[i],1,0,A.CENTER);fonts(old[i],12,False,False)
old[88].paragraph_format.page_break_before=True
old[88].paragraph_format.space_before=Pt(0)
# Espaçamento anterior é suprimido pelo Word no início da página; usar um
# parágrafo de posicionamento dentro das margens, sem deslocar a seção inteira.
spacer=old[88].insert_paragraph_before('')
spacer.style=d.styles['Normal']
pf(spacer,1,0,A.LEFT);spacer.paragraph_format.page_break_before=True
spacer.paragraph_format.line_spacing=Pt(400)
old[88].paragraph_format.page_break_before=False
for i in [88,89,90]:old[i].paragraph_format.keep_with_next=True
old[95].paragraph_format.page_break_before=True
old[99].paragraph_format.space_before=Pt(36)
old[103].paragraph_format.space_before=Pt(30)
for i in [107,111,115,116,117,121,122,123,127,128,129]:
    pf(old[i],1,0,A.CENTER);fonts(old[i],12,False,False)
for i in [107,111,115,121,127]:old[i].paragraph_format.space_before=Pt(24)
for i in [130,140,141]:
    pf(old[i],1,0,A.JUSTIFY if i==130 else A.RIGHT);old[i].paragraph_format.left_indent=Cm(5)
old[130].paragraph_format.space_before=Pt(425)
old[140].paragraph_format.space_before=Pt(425)
old[140].paragraph_format.keep_with_next=True

preheads={'AGRADECIMENTOS','RESUMO','ABSTRACT','LISTA DE TABELAS','LISTA DE FIGURAS','LISTA DE QUADROS','LISTA DE ABREVIATURAS E SIGLAS','SUMÁRIO'}
for p in d.paragraphs:
    text=p.text.strip();sty=p.style.name
    if text in preheads:
        pf(p,1.5,0,A.CENTER,after=24);fonts(p,12,True,False)
        p.paragraph_format.page_break_before=text!='AGRADECIMENTOS'
        p.paragraph_format.keep_with_next=True
    elif sty in ['TITULO TCC','SEÇÃO TCC','SUBÇÃO 2']:
        pf(p,1.5,0,A.CENTER if text=='REFERÊNCIAS' else A.LEFT,before=0 if sty=='TITULO TCC' else 18,after=18)
        fonts(p,12,sty!='SEÇÃO TCC',False)
        if sty!='SUBÇÃO 2':
            for r in p.runs:r.text=r.text.upper()
        p.paragraph_format.page_break_before=sty=='TITULO TCC' and text!='INTRODUÇÃO'
        p.paragraph_format.keep_with_next=True
    elif sty=='Referencias':
        pf(p,1,0,A.LEFT,after=12);p.paragraph_format.keep_together=True
        fonts(p,12,False,False)
    elif text.startswith(('Fonte:','Nota:')):
        pf(p,1,0,A.JUSTIFY,after=24);fonts(p,10,False,False)
    elif sty=='Caption' or re.match(r'^(Tabela|QUADRO|Figura)\s+\d+\s*[–—-]',text):
        pf(p,1,0,A.JUSTIFY,before=12,after=6);fonts(p,10,False,False)
        p.paragraph_format.keep_with_next=True
        for r in p.runs:r.text=r.text.rstrip('.')

for i in [146,152]:pf(old[i],1,0,A.JUSTIFY)
for i in [148,154]:pf(old[i],1,0,A.JUSTIFY,before=12)
for i in [152,154]:fonts(old[i],12,False,False)
for p in old[188:220]:
    pf(p,1.5,0,A.LEFT)

# Separar símbolos matemáticos da relação de siglas e ordená-los alfabeticamente.
symbols=[old[218],old[217],old[219]]
header=old[220].insert_paragraph_before('LISTA DE SÍMBOLOS')
header.style=d.styles['Normal']
pf(header,1.5,0,A.CENTER,after=24);fonts(header,12,True,False)
header.paragraph_format.page_break_before=True;header.paragraph_format.keep_with_next=True
for p in symbols:old[220]._p.addprevious(p._p)

# Títulos autossuficientes, sem siglas técnicas nem código de negociação nos títulos.
caption_map={
'Tabela 1 – Síntese das dimensões investigadas no portfólio bibliográfico (n=34)':'Tabela 1 – Síntese das dimensões investigadas nos 34 estudos do portfólio bibliográfico',
'Tabela 3 – Caracterização estatística dos preços ajustados da PETR4 (2000–2020)':'Tabela 3 – Caracterização estatística dos preços ajustados da ação preferencial da Petrobras (2000–2020)',
'Tabela 9 – Comparação com trabalhos relacionados à PETR4':'Tabela 9 – Comparação com trabalhos relacionados à ação preferencial da Petrobras',
'Figura 1 – Cobertura das dimensões P1–P5 nos estudos':'Figura 1 – Cobertura das cinco dimensões analíticas nos estudos',
'Figura 5 – Evolução do fitness na execução preservada da PETR4 com 200 gerações':'Figura 5 – Evolução da função de aptidão na execução preservada da ação preferencial da Petrobras com 200 gerações',
'Figura 6 – Preços observados e previstos da PETR4 na mesma execução preservada':'Figura 6 – Preços observados e previstos da ação preferencial da Petrobras na mesma execução preservada',
}
for p in d.paragraphs:
    parts=p.text.split('\t')
    if parts[0] in caption_map:
        text=caption_map[parts[0]]+(''.join('\t'+x for x in parts[1:]))
        replace(p,text,'Título sem siglas, conforme modelos pp. 53–55.')
        if len(parts)==1:pf(p,1,0,A.JUSTIFY,12,6);fonts(p,10,False,False);p.paragraph_format.keep_with_next=True

# Listas e sumário: mesma família, corpo 12 e números à direita com pontilhado.
for p in d.paragraphs:
    if '\t' in p.text and re.search(r'\t\d+\s*$',p.text):
        pf(p,1.5,0,A.LEFT);fonts(p,12,None,False)
        f=p.paragraph_format;f.right_indent=Cm(.5)
        f.tab_stops.clear_all()
        if re.match(r'^\d+(?:\.\d+)*\t',p.text):
            f.left_indent=Cm(1.2);f.first_line_indent=Cm(-1.2)
            f.tab_stops.add_tab_stop(Cm(1.2))
        f.tab_stops.add_tab_stop(Cm(16),WD_TAB_ALIGNMENT.RIGHT,WD_TAB_LEADER.DOTS)
        if p.style.name.startswith('toc '):
            fonts(p,12,p.style.name in ['toc 1','toc 3'],False)

# Tabelas: tipo identificado pelo título anterior; corpo uniforme 11 simples.
table_data_before=[[c.text for row in t.rows for c in row.cells] for t in d.tables]
for ti,t in enumerate(d.tables):
    if ti==0:continue
    e=t._tbl.getprevious();title=''
    while e is not None:
        if e.tag==qn('w:p'):
            txt=''.join(e.xpath('.//w:t/text()'))
            if txt.strip():title=txt;break
        e=e.getprevious()
    quadro=title.startswith('QUADRO')
    t.autofit=False
    total=sum(c.width for c in t.columns)
    widths=[int(c.width*Cm(16)/total) for c in t.columns]
    for c,w in zip(t.columns,widths):c.width=w
    for ri,row in enumerate(t.rows):
        pr=row._tr.get_or_add_trPr();setnode(pr,'cantSplit')
        if ri==0:setnode(pr,'tblHeader')
        for ci,c in enumerate(row.cells):
            if ci<len(widths):c.width=widths[ci]
            borders=setnode(c._tc.get_or_add_tcPr(),'tcBorders')
            for edge in ['top','bottom','start','end','left','right']:
                val='nil'
                if (edge=='top' and ri==0) or (edge=='bottom' and ri in [0,len(t.rows)-1]):val='single'
                if quadro and ((edge in ['left','start'] and ci==0) or (edge in ['right','end'] and ci==len(row.cells)-1)):val='single'
                setnode(borders,edge,val=val,sz=6,color='000000')
            for p in c.paragraphs:
                pf(p,1,0,A.LEFT,2,2);fonts(p,11,True if ri==0 else None)
    b=setnode(t._tbl.tblPr,'tblBorders')
    for edge in ['top','bottom','left','right','insideH','insideV']:setnode(b,edge,val='nil')

# Fontes de imagens/tabelas devem ficar na mesma página do último elemento.
for p in d.paragraphs:
    if p._p.xpath('.//w:drawing'):
        pf(p,1,0,A.CENTER);p.paragraph_format.keep_with_next=True

# Exceções explicitamente exemplificadas no guia: retirar itálico somente da palavra.
exception=re.compile(r'(?<!\w)(download|feedback|marketing|on-line|off-line|bullying|campus|software|hardware|scripts?|input|output|pipeline|pool|network|training|performance|ranking|design|link|backup|bit|bits|byte|bytes|grid|loop|web|upload|checklist|desktop|browser|status|notebook)(?!\w)',re.I)
foreign=re.compile(r'(?<!\w)(Echo State Networks?|Reservoir Computing|Long Short-Term Memory|Gated Recurrent Unit|Latin Hypercube Sampling|Cross-generational elitist selection, Heterogeneous recombination and Cataclysmic mutation|Mean Absolute Error|Root Mean Squared Error|et al\.|apud)(?!\w)',re.I)
var=re.compile(r'(?<!\w)(Win|Wout|W)(?!\w)')
def runs_format(p):
    items=[];pos=0
    for r in p.runs:
        txt=r.text;items.append((r,pos,pos+len(txt)));pos+=len(txt)
    text=''.join(r.text for r,_,_ in items)
    spans=[(m.start(),m.end(),'normal') for m in exception.finditer(text)]
    spans += [(m.start(),m.end(),'italic') for m in foreign.finditer(text)]
    for m in var.finditer(text):
        spans.append((m.start(),m.start()+1,'italic'))
        if len(m[0])>1:spans.append((m.start()+1,m.end(),'sub'))
    for r,a,z in items:
        hits=[(x,y,k) for x,y,k in spans if x<z and y>a]
        if not hits or not r._r.xpath('./w:t') or r._r.xpath('./w:drawing|./w:fldChar'):continue
        cuts=sorted({0,len(r.text)}|{max(0,x-a) for x,y,k in hits}|{min(z,y)-a for x,y,k in hits})
        for x,y in zip(cuts,cuts[1:]):
            node=deepcopy(r._r)
            for el in list(node):
                if el.tag!=qn('w:rPr'):node.remove(el)
            t=OxmlElement('w:t');t.text=r.text[x:y];t.set(qn('xml:space'),'preserve');node.append(t)
            pr=node.find(qn('w:rPr'))
            if pr is None:pr=OxmlElement('w:rPr');node.insert(0,pr)
            for lo,hi,k in hits:
                if lo<a+y and hi>a+x:
                    setnode(pr,'i',val=0 if k=='normal' else 1)
                    if k=='sub':setnode(pr,'vertAlign',val='subscript')
            r._r.addprevious(node)
        r._r.getparent().remove(r._r)

abstract=False;refs=False
for p in d.paragraphs:
    if p.text=='ABSTRACT':abstract=True
    if p.text=='LISTA DE TABELAS':abstract=False
    if p.text=='REFERÊNCIAS':refs=True
    if not abstract and not refs:runs_format(p)
for t in d.tables[1:]:
    for row in t.rows:
        for c in row.cells:
            for p in c.paragraphs:runs_format(p)

# Realce bibliográfico uniforme: periódico, obra autônoma ou anais em itálico.
# Não confundir o idioma do título de artigo com o elemento bibliográfico de destaque.
ref_emphasis=[
'Frontiers in Applied Mathematics and Statistics','Expert Systems with Applications',
'Journal of Informetrics','Archives of Computational Methods in Engineering',
'Journal of Information and Data Management','Knowledge-Based Systems',
'IEEE Transactions on Transportation Electrification','Journal of Business & Economic Statistics',
'Journal of Risk and Financial Management','Contabilidad y Negocios','Entropy',
'The European Physical Journal Plus','Machine Learning and Knowledge Extraction',
'Neural Computation','Scholarpedia','Computational Economics','Optics Express',
'Technometrics','Econometrica','Scientometrics','Journal of Stock & Forex Trading',
'International Journal of Computational Methods and Experimental Measurements',
'Neural Processing Letters','ARRUS Journal of Engineering and Technology',
'Computer Systems Science and Engineering','International Journal of Dynamics and Control',
'International Journal of Artificial Intelligence & Applications','Mathematical Models in Engineering',
'International Journal of Computational Intelligence Systems',
'Communications in Nonlinear Science and Numerical Simulation',
'Foundations of Genetic Algorithms 1','IDEAL 2024',
'Modelo híbrido para previsão de séries temporais financeiras: ARIMA-ESN com algoritmo genético',
'Quantum Temporal Convolutional Neural Networks for Cross-Sectional Equity Return Prediction: A Comparative Benchmark Study',
'Same Error, Different Function: The Optimizer as an Implicit Prior in Financial Time Series',
'Modelling Financial Returns with Mixtures of Generalized Normal Distributions',
'Adaptation in Natural and Artificial Systems: An Introductory Analysis with Applications to Biology, Control, and Artificial Intelligence',
'The Echo State Approach to Analysing and Training Recurrent Neural Networks',
'Alteração das distribuições de probabilidade dos pesos de entrada da Echo State Network para previsão do preço de ações',
'Enhancing Trading Performance Through Sentiment Analysis with Large Language Models: Evidence from the S&P 500',
'Explorations in echo state networks',
'Anais [...]','Anais [...]','Proceedings','et al.',
]
ref_pattern=re.compile('|'.join(re.escape(x) for x in sorted(set(ref_emphasis),key=len,reverse=True)),re.I)
ref_checks=[]
for p in d.paragraphs:
    if p.style is None or p.style.name!='Referencias':continue
    text=p.text;matches=list(ref_pattern.finditer(text))
    # Artigo em evento ou manuscrito com referência incompleta: localizar o título
    # existente, sem preencher metadados ausentes.
    if not matches:
        for marker in ['51st Scientific Meeting of the Italian Statistical Society','Neural Information Processing (ICONIP 2025)','PROCEEDINGS OF EMNLP 2014','INTERNATIONAL CONFERENCE ON DIGITAL ECONOMY, BLOCKCHAIN AND ARTIFICIAL INTELLIGENCE']:
            if marker in text:matches=[re.search(re.escape(marker),text)];break
    ref_checks.append({'referencia':text,'realces':[m[0] for m in matches]})
    if matches:
        p.clear();pos=0
        for m in matches:
            if m.start()<pos:continue
            p.add_run(text[pos:m.start()]);p.add_run(m[0]).italic=True;pos=m.end()
        p.add_run(text[pos:]);fonts(p,12,False)

# Ordem alfabética pelo sobrenome de entrada, preservando o texto das referências.
import unicodedata
refs_paras=[p for p in d.paragraphs if p.style and p.style.name=='Referencias']
anchor=next(p for p in d.paragraphs if p.text=='REFERÊNCIAS')
def refkey(p):
    surname=p.text.split(',')[0]
    return ''.join(c for c in unicodedata.normalize('NFD',surname) if not unicodedata.combining(c)).casefold()
for p in sorted(refs_paras,key=refkey):
    anchor._p.addnext(p._p);anchor=p

pars=d.paragraphs
for a,b in zip(pars,pars[1:]):
    if a.text.startswith('Fonte:') and b.text.startswith('Nota:'):a.paragraph_format.space_after=Pt(0)
titles={p.text.casefold():p.text for p in d.paragraphs if p.style and p.style.name in ['TITULO TCC','SEÇÃO TCC','SUBÇÃO 2']}
for p in d.paragraphs:
    if p.style and p.style.name.startswith('toc ') and '\t' in p.text:
        parts=p.text.split('\t');key=parts[-2].casefold()
        if key in titles:
            for r in p.runs:r.text=r.text.replace(parts[-2],titles[key])

# Indicativos na margem esquerda; sufixo de espaço, conforme a hierarquia do guia.
for lvl in d.part.numbering_part.element.xpath('.//w:lvl'):
    setnode(lvl,'suff',val='space')
    pr=setnode(lvl,'pPr');setnode(pr,'ind',left=0,hanging=0)
    tabs=pr.find(qn('w:tabs'))
    if tabs is not None:pr.remove(tabs)

# A capa é excluída por início 0; seção textual continua a contagem, sem reinício.
setnode(d.sections[0]._sectPr,'pgNumType',start=0,fmt='decimal')
for s in list(d.sections)[1:]:
    n=s._sectPr.find(qn('w:pgNumType'))
    if n is not None:n.attrib.pop(qn('w:start'),None)
for s in d.sections:
    h=s.header
    paras=list(h.paragraphs)
    meaningful=[p for p in paras if p._p.xpath('.//w:fldChar|.//w:t')]
    keep=meaningful[0] if meaningful else paras[0]
    for p in paras:
        if p is not keep:p._p.getparent().remove(p._p)
    for p in h.paragraphs:
        pf(p,1,0,A.RIGHT);fonts(p,12,False,False)

d.save(DEST)
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==source_hash
check=Document(DEST)
assert len(check.inline_shapes)==len(Document(SOURCE).inline_shapes)==6
assert [[c.text for row in t.rows for c in row.cells] for t in check.tables]==table_data_before
record={'origem':str(SOURCE),'sha256_origem':source_hash,'saida':str(DEST),'alteracoes_textuais':changes,
'decisoes':['Base posterior com observações do orientador, preservando a base histórica do catálogo.',
'Margens reais 3/3/2/2 em todas as seções.', 'Fonte 11 em todas as tabelas e 10 em títulos e fontes conforme pedido posterior de aplicar o guia.',
'Quarto nível: regra textual da p. 12 prevalece sobre exemplo da p. 50; não há quarto nível no documento.',
'Ficha catalográfica permanece vazia: conteúdo deve ser emitido pela biblioteca.',
'Folha de aprovação mantém campos de data sem inventar aprovação.'],
'figuras_preservadas':6,'tabelas_preservadas':13,'experimentos_reexecutados':False}
(QA/'registro_alteracoes.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
(QA/'realces_referencias.json').write_text(json.dumps(ref_checks,ensure_ascii=False,indent=2),encoding='utf-8')
print(DEST)
