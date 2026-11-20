"""Revisão complementar baseada no texto e nos balões dos modelos do guia.

Não executa experiências e preserva a cópia previamente entregue.
"""
from pathlib import Path
from copy import deepcopy
from collections import Counter
import re,json,hashlib
from docx import Document
from docx.shared import Cm,Pt,RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH as A,WD_TAB_ALIGNMENT,WD_TAB_LEADER
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ROW_HEIGHT_RULE
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'reports/monografia/MayconGarciaSilva_monografia_padronizada_FASOFT.docx'
DST=ROOT/'reports/monografia/MayconGarciaSilva_monografia_FASOFT_conferida.docx'
QA=ROOT/'reports/auditoria_integral_fasoft_20261028'
QA.mkdir(exist_ok=True)
d=Document(SRC);old=list(d.paragraphs);changes=[]
sourcehash=hashlib.sha256(SRC.read_bytes()).hexdigest()
def node(parent,tag,**attrs):
 x=parent.find(qn('w:'+tag))
 if x is None:x=OxmlElement('w:'+tag);parent.append(x)
 for k,v in attrs.items():x.set(qn('w:'+k),str(v))
 return x
def font(p,size=12,bold=None,italic=None):
 for r in p.runs:
  r.font.name='Times New Roman';r.font.size=Pt(size);r.font.color.rgb=RGBColor(0,0,0)
  if bold is not None:r.bold=bold
  if italic is not None:r.italic=italic
def record(p,text,reason):
 changes.append({'antes':p.text,'depois':text,'motivo':reason});p.clear();p.add_run(text)
def replace_range(p,a,b,text):
 # Substituição textual conservadora, preservando formatação das partes restantes.
 pos=0
 for r in list(p.runs):
  lo,hi=pos,pos+len(r.text);pos=hi
  if hi<=a or lo>=b:continue
  left=r.text[:max(0,a-lo)];right=r.text[max(0,b-lo):] if b<hi else ''
  r.text=left+(text if lo<=a<hi else '')+right
def simple(p,size=12,align=A.JUSTIFY,italic=None,bold=None):
 f=p.paragraph_format;f.line_spacing=1;f.first_line_indent=Cm(0);f.alignment=align
 font(p,size,bold,italic)

# Local e ano na parte inferior da mancha, como nos modelos pp. 37–38.
# Calibração pela exportação nativa: a última linha termina em aproximadamente
# 780 pt (2,2 cm acima da borda), sem invadir a margem inferior de 2 cm.
old[4].paragraph_format.space_before=Pt(394.25)
old[10].paragraph_format.space_before=Pt(247.5)
for i,points in [(20,36),(21,36),(22,60),(25,48),(28,48)]:
 old[i].paragraph_format.space_before=Pt(points)

# Ficha em branco por decisão expressa do autor; dimensões do modelo p. 39.
t=d.tables[0];t.alignment=WD_TABLE_ALIGNMENT.CENTER;t.autofit=False
t.columns[0].width=Cm(12.5);t.cell(0,0).width=Cm(12.5)
node(t._tbl.tblPr,'tblW',w=int(Cm(12.5).twips),type='dxa')
node(t._tbl.tblPr,'tblInd',w=0,type='dxa')
t.rows[0].height=Cm(7.5);t.rows[0].height_rule=WD_ROW_HEIGHT_RULE.EXACTLY
for p in old[13:17]:simple(p,11,A.CENTER,False,False)
# A instrução de deixar a ficha vazia também preserva o texto institucional existente.

# Modelos de dedicatória e epígrafe (pp. 41 e 43): bloco a 8 cm da margem.
for i in [31,38,39]:old[i].paragraph_format.left_indent=Cm(8)
simple(old[31],12,A.JUSTIFY,False,False)
simple(old[38],12,A.JUSTIFY,True,False)
simple(old[39],11,A.RIGHT,False,False)

# Folha de aprovação (p. 40): natureza em largura integral e banca em corpo 11.
for i in [17,18]:
 simple(old[i],12,A.CENTER,False,True);old[i].paragraph_format.line_spacing=1.5
p=old[19];simple(p,12,A.JUSTIFY,False,False)
p.paragraph_format.left_indent=Cm(0);p.paragraph_format.line_spacing=1.5
record(old[21],'BANCA EXAMINADORA','Modelo p. 40: título em maiúsculas e negrito.')
simple(old[21],12,A.CENTER,False,True)
for i in [22,25,28]:record(old[i],'.'*90,'Modelo p. 40: linha de assinatura com 90 pontos.');simple(old[i],11,A.CENTER,False,False)
for i in [23,24,26,27,29,30]:simple(old[i],11,A.CENTER,False,False)

# A natureza da folha de rosto deve conter área de concentração (p. 20).
if 'Área de concentração:' not in old[8].text:
 text=old[8].text+' Área de concentração: Engenharia de Software.'
 record(old[8],text,'Elemento da natureza exigido na p. 20, já informado na aprovação.');simple(old[8],11,A.JUSTIFY,False,False)

# Designação correta: mapa categórico e avaliação descritiva são quadros (p. 33).
mapping={('Tabela',1):('Tabela',1),('Tabela',2):('Quadro',1),('Tabela',3):('Tabela',2),
 ('Tabela',4):('Tabela',3),('Tabela',5):('Tabela',4),('Tabela',6):('Tabela',5),
 ('Tabela',7):('Tabela',6),('Tabela',8):('Quadro',5),('Tabela',9):('Tabela',7),
 ('Quadro',1):('Quadro',2),('Quadro',2):('Quadro',3),('Quadro',3):('Quadro',4)}
for p in d.paragraphs:
 text=p.text
 if re.search(r'Tabelas 1 e 2',text):
  # Combinação de uma tabela quantitativa e um quadro descritivo.
  for m in reversed(list(re.finditer(r'Tabelas 1 e 2',text))):replace_range(p,m.start(),m.end(),'__PAR_COBERTURA__')
  text=p.text
 matches=list(re.finditer(r'\b(Tabela|Quadro)\s+(\d+)\b',text,re.I))
 for m in reversed(matches):
  k=(m[1].capitalize(),int(m[2]));new=mapping.get(k)
  if not new:continue
  label=new[0]
  replace_range(p,m.start(),m.end(),label+' '+str(new[1]))
 for a,b in [('das __PAR_COBERTURA__','da Tabela 1 e do Quadro 1'),('__PAR_COBERTURA__','Tabela 1 e Quadro 1')]:
  for m in reversed(list(re.finditer(re.escape(a),p.text))):replace_range(p,m.start(),m.end(),b)
 # Concordância dos artigos após mudança de classificação.
 for a,b in [('A Quadro','O Quadro'),('a Quadro','o Quadro'),('na Quadro','no Quadro'),('da Quadro','do Quadro'),('à Quadro','ao Quadro')]:
  for m in reversed(list(re.finditer(re.escape(a),p.text))):replace_range(p,m.start(),m.end(),b)

# Citações autor–ano: grafia dos sobrenomes como nos exemplos do guia.
surname={'MILLEA':'Millea','PAGANI':'Pagani','KOVALESKI':'Kovaleski','RESENDE':'Resende',
 'VISHWAS':'Vishwas','SOLTANI':'Soltani','ARIA':'Aria','CUCCURULLO':'Cuccurullo',
 'CARDOSO':'Cardoso','TIMBÓ':'Timbó','JAEGER':'Jaeger'}
start=next(i for i,p in enumerate(d.paragraphs) if p.text=='INTRODUÇÃO')
end=next(i for i,p in enumerate(d.paragraphs) if p.text=='REFERÊNCIAS')
for p in d.paragraphs[start:end]:
 for m in reversed(list(re.finditer(r'\([^()]*\b(?:19|20)\d{2}[a-z]?[^()]*\)',p.text))):
  chunk=m[0];new=re.sub('|'.join(surname),lambda x:surname[x[0]],chunk)
  if new!=chunk:replace_range(p,m.start(),m.end(),new)

# Complementar primeiras ocorrências inequívocas sem alterar afirmações ou métricas.
first_defs={
 'via BPTT':'via retropropagação através do tempo (Backpropagation Through Time – BPTT)',
 'modelos como ARIMA e regressão linear':'modelos como o autorregressivo integrado de médias móveis (Autoregressive Integrated Moving Average – ARIMA) e a regressão linear',
 'comparam SVMs, LSTMs':'comparam máquinas de vetores de suporte (Support Vector Machines – SVMs), LSTMs',
 '(NMSE – Normalized Mean Squared Error)':'(Normalized Mean Squared Error – NMSE)',
 'introduz a GED no contexto financeiro por meio do modelo EGARCH':'introduz a Distribuição Generalizada de Erro (Generalized Error Distribution – GED) no contexto financeiro por meio do modelo exponencial autorregressivo de heterocedasticidade condicional generalizada (Exponential Generalized Autoregressive Conditional Heteroskedasticity – EGARCH)',
 'reduz drasticamente o MSE':'reduz drasticamente o erro quadrático médio (Mean Squared Error – MSE)',
 'critérios AIC, BIC e HQIC':'critérios de informação de Akaike (Akaike Information Criterion – AIC), bayesiano (Bayesian Information Criterion – BIC) e de Hannan–Quinn (Hannan–Quinn Information Criterion – HQIC)',
 'proposta deste TFC':'proposta deste Trabalho Final de Curso (TFC)',
 'método ACF':'método baseado na função de autocorrelação (Autocorrelation Function – ACF)',
 'realizadas em CPU, sem dependência de aceleração por GPU':'realizadas em unidade central de processamento (Central Processing Unit – CPU), sem dependência de aceleração por unidade de processamento gráfico (Graphics Processing Unit – GPU)',
 'do próprio PDF':'do próprio arquivo em formato de documento portátil (Portable Document Format – PDF)',
 'por DOI ou título':'por identificador digital de objeto (Digital Object Identifier – DOI) ou título',
 'fator de impacto (SJR)':'indicador de impacto SCImago Journal Rank (SJR)',
 'pelo teste de Diebold–Mariano':'pelo teste de Diebold–Mariano (DM)',
 'terceiro utiliza Power Function, Dagum 4P':'terceiro utiliza Power Function (PF), Dagum 4P',
 'como BP, Elman e LSTM':'como redes de retropropagação (Backpropagation – BP), Elman e LSTM',
 'arquitetura RNN Encoder-Decoder':'arquitetura de rede neural recorrente (Recurrent Neural Network – RNN) do tipo codificador–decodificador',
 'redes convolucionais temporais quânticas (QTCNN)':'redes convolucionais temporais quânticas (Quantum Temporal Convolutional Neural Networks – QTCNN)',
 'modelo híbrido HAR-PSO-ESN':'modelo híbrido autorregressivo heterogêneo (Heterogeneous Autoregressive – HAR), combinado com PSO e ESN (HAR-PSO-ESN)',
 'variante CS-ESN':'variante de ESN com sensoriamento compressivo (Compressed Sensing – CS-ESN)',
 'Lorenz, PCO, Chen e Mackey-Glass':'Lorenz, oscilador de Chen perturbado (Perturbed Chen Oscillator – PCO), Chen e Mackey-Glass',
 'modelo HAR-PSO-ESN':'modelo autorregressivo heterogêneo (Heterogeneous Autoregressive – HAR), combinado com PSO e ESN (HAR-PSO-ESN)',
 'células de combustível (PEMFCs)':'células de combustível de membrana de troca de prótons (Proton Exchange Membrane Fuel Cells – PEMFCs)',
 'mutação cataclísmica inspirada no CHC, denominação de Cross-generational elitist selection, Heterogeneous recombination and Cataclysmic mutation':'mutação cataclísmica inspirada no algoritmo Cross-generational elitist selection, Heterogeneous recombination and Cataclysmic mutation (CHC)',
}
used=set()
for p in d.paragraphs[start:end]:
 for a,b in first_defs.items():
  if a in used or a not in p.text:continue
  i=p.text.index(a);before=p.text;replace_range(p,i,i+len(a),b)
  changes.append({'antes':before,'depois':p.text,'motivo':'Primeira ocorrência e explicação de termo técnico, pp. 69 e 72.'});used.add(a)

# Metadados conferidos nos próprios PDFs (hashes D05/D06/D10/D11 da base).
all_pars=list(d.paragraphs)+[p for t in d.tables for row in t.rows for c in row.cells for p in c.paragraphs]
for p in all_pars:
 before=p.text
 if p.text.startswith('Fonte:') and 'PDFs' in p.text:
  for m in reversed(list(re.finditer('PDFs',p.text))):replace_range(p,m.start(),m.end(),'documentos')
 if p.text.startswith(('CHEN,','CORTESI,')):
  for m in reversed(list(re.finditer(r'(?<!\d)2025(?!\d)',p.text))):replace_range(p,m.start(),m.end(),'2026')
 else:
  for m in reversed(list(re.finditer(r'(?:Chen|Cortesi)(?:\s+et al\.)?[,]?\s*\(?(?P<ano>2024|2025)\)?',p.text))):replace_range(p,m.start('ano'),m.end('ano'),'2026')
 for a,b in [('Duttilo et al. (2023a)','Duttilo (2023)'),('Duttilo et al. (2023b)','Duttilo e Gattone (2022)'),('Duttilo (2023a)','Duttilo (2023)'),('Duttilo (2023b)','Duttilo e Gattone (2022)'),('Duttilo et al. (2023) modelam','Duttilo (2023) modela')]:
  for m in reversed(list(re.finditer(re.escape(a),p.text))):replace_range(p,m.start(),m.end(),b)
 if p.text.startswith('Trabalhos posteriores ampliam'):
  for a,b in [('e mostram que tais misturas','e mostra que tais misturas'),('Os autores recorrem','O autor recorre')]:
   if a in p.text:
    k=p.text.index(a);replace_range(p,k,k+len(a),b)
 for m in reversed(list(re.finditer(r'Duttilo et al\., 2023',p.text))):replace_range(p,m.start(),m.end(),'Duttilo, 2023')
 if p.text.startswith('CORTESI,') and 'arXiv:2603.02620v1' not in p.text:
  k=p.text.index('[Preprint]');replace_range(p,k,k+len('[Preprint]'),'(Preprint arXiv:2603.02620v1)')
 if p.style.name=='Referencias':
  for m in reversed(list(re.finditer(r'(?<!\.)\.\.(?!\.)',p.text))):replace_range(p,m.start(),m.end(),'.')
  for m in reversed(list(re.finditer(r'DUTTILO, P;',p.text))):replace_range(p,m.start(),m.end(),'DUTTILO, P.;')
 if before!=p.text:changes.append({'antes':before,'depois':p.text,'motivo':'Coerência entre citações e referências; anos e autoria conferidos nas fontes primárias D05, D06, D10 e D11.'})

# Resumos autossuficientes: explicar as medidas e evitar siglas sem apresentação.
for idx in [41,44]:
 p=old[idx]
 pairs=([('ajustado da PETR4','ajustado da ação preferencial da Petrobras (PETR4)'),('inspirado no CHC',''),('menor MAE de teste','menor erro médio absoluto (Mean Absolute Error – MAE) de teste'),('menor RMSE (','menor raiz do erro quadrático médio (Root Mean Squared Error – RMSE) ('),('maior R² (','maior coeficiente de determinação (R²) ('),('para GRU e LSTM','para as unidades recorrentes com portas (Gated Recurrent Units – GRU) e as redes de memória de longo e curto prazo (Long Short-Term Memory – LSTM)')]
 if idx==41 else [('price of PETR4','price of Petrobras preferred stock (PETR4)'),(' inspired by CHC',''),('lowest test MAE','lowest test mean absolute error (MAE)'),('lowest RMSE (','lowest root mean squared error (RMSE) ('),('highest R² (','highest coefficient of determination (R²) ('),('documented GRU and LSTM values','documented gated recurrent unit (GRU) and long short-term memory (LSTM) values')])
 for a,b in pairs:
  if a in p.text:
   k=p.text.index(a);before=p.text;replace_range(p,k,k+len(a),b);changes.append({'antes':before,'depois':p.text,'motivo':'Resumo autossuficiente, pp. 22–23; descrição do mecanismo permanece desenvolvida no corpo.'})
 # Retirar espaço deixado pela supressão de sigla não explicada.
 if 'cataclísmica .' in p.text:
  k=p.text.index('cataclísmica .');replace_range(p,k,k+len('cataclísmica .'),'cataclísmica.')

# Ordem alfabética e diagramação da lista de siglas, conforme pp. 23 e 48.
ps=list(d.paragraphs);a=next(i for i,p in enumerate(ps) if p.text=='LISTA DE ABREVIATURAS E SIGLAS');b=next(i for i,p in enumerate(ps) if p.text=='LISTA DE SÍMBOLOS')
entries={}
for p in ps[a+1:b]:
 m=re.match(r'^([A-Za-z0-9-]+)\s*[-–]\s*(.+)$',p.text.replace('\t',' '))
 if m:entries[m[1]]=m[2]
entries.update({'ACF':'Autocorrelation Function (Função de Autocorrelação)','AGED':'Asymmetric Generalized Error Distribution (Distribuição Generalizada de Erro Assimétrica)','AIC':'Akaike Information Criterion (Critério de Informação de Akaike)','BIC':'Bayesian Information Criterion (Critério de Informação Bayesiano)','CPU':'Central Processing Unit (Unidade Central de Processamento)','CS-ESN':'Compressed Sensing Echo State Network (Rede de Estados de Eco com Sensoriamento Compressivo)','DOI':'Digital Object Identifier (Identificador Digital de Objeto)','EGARCH':'Exponential Generalized Autoregressive Conditional Heteroskedasticity','GPU':'Graphics Processing Unit (Unidade de Processamento Gráfico)','HAR':'Heterogeneous Autoregressive (Autorregressivo Heterogêneo)','HONN':'Higher-Order Neural Network (Rede Neural de Ordem Superior)','HQIC':'Hannan–Quinn Information Criterion (Critério de Informação de Hannan–Quinn)','MAPE':'Mean Absolute Percentage Error (Erro Percentual Absoluto Médio)','MLP':'Multilayer Perceptron (Perceptron Multicamadas)','MSE':'Mean Squared Error (Erro Quadrático Médio)','NMSE':'Normalized Mean Squared Error (Erro Quadrático Médio Normalizado)','PCO':'Perturbed Chen Oscillator (Oscilador de Chen Perturbado)','PDF':'Portable Document Format (Formato de Documento Portátil)','QTCNN':'Quantum Temporal Convolutional Neural Network (Rede Convolucional Temporal Quântica)','TFC':'Trabalho Final de Curso'})
entries.update({'BPNN':'Backpropagation Neural Network (Rede Neural de Retropropagação)','ER':'Erdős–Rényi','HQNN':'Hybrid Quantum Neural Network (Rede Neural Quântico-Híbrida)','PEMFC':'Proton Exchange Membrane Fuel Cell (Célula de Combustível de Membrana de Troca de Prótons)','SF':'Scale-Free (Livre de Escala)','SJR':'SCImago Journal Rank','SW':'Small-World (Pequeno Mundo)'})
entries.update({'BP':'Backpropagation (Retropropagação)','TPE':'Tree Parzen Estimator'})
for p in ps[a+1:b]:p._p.getparent().remove(p._p)
for key,val in sorted(entries.items(),key=lambda x:x[0].casefold()):
 p=ps[b].insert_paragraph_before();simple(p,12,A.JUSTIFY,False,False);p.paragraph_format.line_spacing=1.5
 r=p.add_run(key+' – ');r.font.name='Times New Roman';r.font.size=Pt(12)
 cut=val.find(' (');cut=len(val) if cut<0 else cut
 r=p.add_run(val[:cut]);r.italic=key not in ['AG','B3','DM','ER','PETR4','RNR','SJR','TFC'];r.font.name='Times New Roman';r.font.size=Pt(12)
 if cut<len(val):r=p.add_run(val[cut:]);r.font.name='Times New Roman';r.font.size=Pt(12)
 p.paragraph_format.keep_with_next=False

# Todos os títulos de elementos recebem o mesmo estilo, inclusive a legenda
# originalmente armazenada como parágrafo Normal.
for p in d.paragraphs:
 if '\t' not in p.text and re.match(r'^(Tabela|Quadro|Figura)\s+\d+\s*[–—-]',p.text,re.I):
  p.style='Caption';simple(p,10,A.JUSTIFY,False,False)
  p.paragraph_format.keep_with_next=True;p.paragraph_format.left_indent=Cm(0);p.paragraph_format.right_indent=Cm(0)

# Listas independentes na ordem institucional: figuras, quadros, tabelas e siglas.
heads=['LISTA DE FIGURAS','LISTA DE QUADROS','LISTA DE TABELAS']
pars=d.paragraphs
block_start=next(i for i,p in enumerate(pars) if p.text=='LISTA DE TABELAS')
block_end=next(i for i,p in enumerate(pars) if p.text=='LISTA DE ABREVIATURAS E SIGLAS')
anchor=pars[block_end]
captions=[]
for p in pars[block_end:]:
 if '\t' not in p.text and re.match(r'^(Tabela|QUADRO|Figura)\s+\d+\s*[–—-]',p.text,re.I):captions.append(p)
for p in pars[block_start:block_end]:p._p.getparent().remove(p._p)
for title,kind in zip(heads,['Figura','Quadro','Tabela']):
 h=anchor.insert_paragraph_before(title,style='Normal');h.paragraph_format.page_break_before=True
 h.paragraph_format.alignment=A.CENTER;h.paragraph_format.first_line_indent=Cm(0)
 h.paragraph_format.line_spacing=1.5;h.paragraph_format.space_after=Pt(24);h.paragraph_format.keep_with_next=True;font(h,12,True,False)
 for cap in captions:
  if not cap.text.casefold().startswith(kind.casefold()+' '):continue
  p=anchor.insert_paragraph_before(cap.text+'\t0',style='Normal')
  simple(p,12,A.JUSTIFY,False,False);p.paragraph_format.line_spacing=1.5
  p.paragraph_format.tab_stops.add_tab_stop(Cm(16),WD_TAB_ALIGNMENT.RIGHT,WD_TAB_LEADER.DOTS)
for p in d.paragraphs:
 if p.style.name.startswith('toc ') or (p.text and '\t' in p.text and re.search(r'\t\d+$',p.text)):
  p.paragraph_format.alignment=A.JUSTIFY
 if p.style.name in ['TITULO TCC','SEÇÃO TCC','SUBÇÃO 2'] and p.text!='REFERÊNCIAS':p.paragraph_format.alignment=A.JUSTIFY

# Bordas: apenas quadros descritivos fechados nas laterais (pp. 53–54).
for ti,t in enumerate(d.tables):
 if ti==0:continue
 e=t._tbl.getprevious()
 while e is not None and not ''.join(e.xpath('.//w:t/text()')).strip():e=e.getprevious()
 title=''.join(e.xpath('.//w:t/text()')) if e is not None else ''
 quadro=title.lower().startswith('quadro')
 # A largura preferencial antiga não acompanhava as células; o Word reduzia
 # alguns quadros para cerca de 14,8 cm. Sincronizar tabela, grade e células.
 t.autofit=False;t.alignment=WD_TABLE_ALIGNMENT.CENTER
 node(t._tbl.tblPr,'tblW',w=int(Cm(16).twips),type='dxa')
 node(t._tbl.tblPr,'tblInd',w=0,type='dxa')
 raw=[c.width.twips for c in t.rows[0].cells];total=sum(raw)
 widths=[round(Cm(16).twips*x/total) for x in raw];widths[-1]=Cm(16).twips-sum(widths[:-1])
 from docx.shared import Twips
 for ci,w in enumerate(widths):
  t.columns[ci].width=Twips(w)
  for row in t.rows:row.cells[ci].width=Twips(w)
 if ti==6:
  for row in t.rows:
   for c in row.cells:
    for p in c.paragraphs:p.paragraph_format.keep_with_next=True
 for ri,row in enumerate(t.rows):
  for ci,c in enumerate(row.cells):
   borders=node(c._tc.get_or_add_tcPr(),'tcBorders')
   for edge in ['left','start','right','end']:
    side=(ci==0 and edge in ['left','start']) or (ci==len(row.cells)-1 and edge in ['right','end'])
    node(borders,edge,val='single' if quadro and side else 'nil',sz=6,color='000000')

# Fonte/itálico das novas expressões técnicas e preservação da notação Win/Wout.
new_foreign=[b for b in ['Backpropagation Through Time','Autoregressive Integrated Moving Average','Support Vector Machines','Exponential Generalized Autoregressive Conditional Heteroskedasticity','Generalized Error Distribution','Mean Absolute Error','Root Mean Squared Error','Mean Squared Error','Akaike Information Criterion','Bayesian Information Criterion','Hannan–Quinn Information Criterion','Autocorrelation Function','Central Processing Unit','Graphics Processing Unit','Portable Document Format','Digital Object Identifier','Genetic Algorithm','Recurrent Neural Network','Quantum Temporal Convolutional Neural Networks','Heterogeneous Autoregressive','Compressed Sensing','Perturbed Chen Oscillator','Gated Recurrent Units','Long Short-Term Memory']]
new_foreign.extend(['Proton Exchange Membrane Fuel Cells','Cross-generational elitist selection, Heterogeneous recombination and Cataclysmic mutation','Backpropagation','et al.','apud','ibidem','ibid.','opus citatum'])
foreign_re=re.compile('|'.join(re.escape(x) for x in sorted(new_foreign,key=len,reverse=True)))
for p in d.paragraphs:
 if p._p is old[44]._p or p.style.name=='Referencias':continue
 for m in reversed(list(foreign_re.finditer(p.text))):
  pos=0
  for r in list(p.runs):
   a,z=pos,pos+len(r.text);pos=z
   if a>=m.end() or z<=m.start():continue
   text=r.text;cuts=sorted({0,len(text),max(0,m.start()-a),min(len(text),m.end()-a)})
   for lo,hi in zip(cuts,cuts[1:]):
    nr=deepcopy(r._r)
    for child in list(nr):
     if child.tag!=qn('w:rPr'):nr.remove(child)
    t=OxmlElement('w:t');t.text=text[lo:hi];t.set(qn('xml:space'),'preserve');nr.append(t)
    if a+lo<m.end() and a+hi>m.start():node(nr.get_or_add_rPr(),'i',val=1)
    r._r.addprevious(nr)
   r._r.getparent().remove(r._r)

for r in old[44].runs:r.italic=False

def set_italic_span(p,a,b,value):
 offset=0
 for r in list(p.runs):
  lo,hi=offset,offset+len(r.text);offset=hi
  if hi<=a or lo>=b:continue
  cuts=sorted({0,len(r.text),max(0,a-lo),min(len(r.text),b-lo)})
  for x,y in zip(cuts,cuts[1:]):
   nr=deepcopy(r._r)
   for child in list(nr):
    if child.tag!=qn('w:rPr'):nr.remove(child)
   t=OxmlElement('w:t');t.text=r.text[x:y];t.set(qn('xml:space'),'preserve');nr.append(t)
   if lo+x<b and lo+y>a:node(nr.get_or_add_rPr(),'i',val=int(value))
   r._r.addprevious(nr)
  r._r.getparent().remove(r._r)

for p in d.paragraphs+[p for t in d.tables for row in t.rows for c in row.cells for p in c.paragraphs]:
 # A inicial de um autor não é a variável matemática W.
 for m in reversed(list(re.finditer(r'(?<=Wang )W(?=\.)',p.text))):set_italic_span(p,m.start(),m.end(),False)
 prefix='A camada de saída foi treinada por regressão linear regularizada ('
 if p.text.startswith(prefix):set_italic_span(p,0,len(prefix),False)

for p in d.paragraphs:
 if re.match(r'^H[1-5] - ',p.text):p.paragraph_format.left_indent=Cm(0)

# Parágrafos de 4–7 linhas são uma recomendação (p. 14), não motivo para
# inserir quebras artificiais dentro de uma frase. Dividir apenas entre frases.
linefile=QA/'paragrafos_word.json'
if linefile.exists():
 from functools import lru_cache
 stats=json.loads(linefile.read_text(encoding='utf-8-sig'))
 def key(s):return re.sub(r'\d','#',re.sub(r'\s+',' ',s))[:55]
 lookup={key(x['text']):x for x in stats if x['style']=='Normal' and not x['table']}
 active=False
 for p in list(d.paragraphs):
  if p.text=='INTRODUÇÃO':active=True
  if p.text=='REFERÊNCIAS':active=False
  st=lookup.get(key(p.text))
  if not active or p.style.name!='Normal' or not st or st['lines']<=7:continue
  if p._p.xpath('.//m:oMath | .//w:drawing | .//w:fldChar | .//w:hyperlink'):continue
  text=p.text;bounds=[0]+[m.end() for m in re.finditer(r'(?<=[.!?])\s+(?=[A-ZÁÀÂÃÉÊÍÓÔÕÚÇ])',text)]+[len(text)]
  if len(bounds)<=2:continue
  ratio=st['lines']/max(1,len(st['text']))
  @lru_cache(None)
  def best(i):
   if i==len(bounds)-1:return (0,[])
   choices=[]
   for j in range(i+1,len(bounds)):
    lines=len(text[bounds[i]:bounds[j]].strip())*ratio
    penalty=(max(0,lines-7)*8)**2+(max(0,4-lines)*3)**2+1+abs(lines-5.5)*.05
    rest,path=best(j);choices.append((penalty+rest,[j]+path))
   return min(choices,key=lambda x:x[0])
  _,path=best(0)
  if len(path)<2:continue
  starts=[0]+[bounds[j] for j in path[:-1]];ends=[bounds[j] for j in path]
  nodes=[];segments=[]
  for a,b in zip(starts,ends):
   while a<b and text[a].isspace():a+=1
   while b>a and text[b-1].isspace():b-=1
   np=OxmlElement('w:p')
   if p._p.pPr is not None:np.append(deepcopy(p._p.pPr))
   offset=0
   for r in p.runs:
    lo,hi=offset,offset+len(r.text);offset=hi
    if hi<=a or lo>=b:continue
    nr=OxmlElement('w:r')
    if r._r.rPr is not None:nr.append(deepcopy(r._r.rPr))
    t=OxmlElement('w:t');t.text=r.text[max(0,a-lo):min(len(r.text),b-lo)];t.set(qn('xml:space'),'preserve');nr.append(t);np.append(nr)
   nodes.append(np);segments.append(text[a:b])
  assert ' '.join(segments)==re.sub(r'\s+',' ',text).strip()
  for np in nodes:p._p.addprevious(np)
  p._p.getparent().remove(p._p)
  changes.append({'antes':text,'depois':segments,'motivo':'Recomendação de extensão dos parágrafos (p. 14); apenas separação entre frases, sem supressão ou reescrita.'})

# Fluxo enumerativo: introdução por dois-pontos e alíneas (pp. 11–12 e 51).
for p in list(d.paragraphs):
 if not p.text.startswith('Em eventual implantação, o risco de modelo'):continue
 before=p.text;head,rest=before.split(' inclui: ',1);flow,tail=rest.split('. A manutenção',1)
 items=[x.strip().removeprefix('e ') for x in flow.split(';')]
 p.clear();p.add_run(head+' inclui:');font(p,12,False,False)
 anchor=p._p
 for n,text in enumerate(items):
  np=OxmlElement('w:p');anchor.addnext(np);anchor=np
  from docx.text.paragraph import Paragraph
  q=Paragraph(np,p._parent);q.style='Normal';q.add_run(chr(97+n)+') '+text+('.' if n==len(items)-1 else ';'))
  f=q.paragraph_format;f.left_indent=Cm(1.26);f.first_line_indent=Cm(-.63);f.alignment=A.JUSTIFY;f.line_spacing=1.5;font(q,12,False,False)
 np=OxmlElement('w:p');anchor.addnext(np);q=Paragraph(np,p._parent);q.style='Normal';q.add_run('A manutenção'+tail);font(q,12,False,False)
 # Única expressão estrangeira desta passagem, com conservação do sentido.
 for m in reversed(list(re.finditer('rollback',q.text))):
  a,b=m.span();raw=q.text;q.clear();q.add_run(raw[:a]);q.add_run(raw[a:b]).italic=True;q.add_run(raw[b:]);font(q,12)
 changes.append({'antes':before,'depois':[p.text]+items+[q.text],'motivo':'Enumeração em alíneas segundo p. 51, com as mesmas etapas de governança.'})

# Tornar explícita, na conclusão, a remissão ao desenvolvimento já existente.
ps=list(d.paragraphs);ref=next(i for i,p in enumerate(ps) if p.text=='REFERÊNCIAS')
last=next(p for p in reversed(ps[:ref]) if p.text.strip())
before=last.text;last.add_run(' As demais possibilidades de continuidade são discutidas na Seção 5.3.');font(last,12)
changes.append({'antes':before,'depois':last.text,'motivo':'Remissão aos trabalhos futuros já existentes, em atendimento à p. 34.'})

# Remover recuos laterais legados em parágrafos da introdução, conservando
# os recuos próprios das alíneas e o formato menor das fontes e notas.
active=False
for p in d.paragraphs:
 if p.text=='INTRODUÇÃO':active=True
 if p.text=='REFERÊNCIAS':active=False
 if not active or p.style.name!='Normal' or not p.text.strip() or p.text.startswith(('Fonte:','Nota:')) or re.match(r'^[a-z]\) ',p.text):continue
 f=p.paragraph_format;f.left_indent=Cm(0);f.right_indent=Cm(0);f.first_line_indent=Cm(1.25);f.line_spacing=1.5;f.alignment=A.JUSTIFY;font(p,12)

# Evitar uma página quase vazia com a continuação final dos trabalhos futuros.
# Condensar apenas as duas apresentações repetidas da mesma evolução do software.
ps=list(d.paragraphs);i=next(i for i,p in enumerate(ps) if p.text=='TRABALHOS FUTUROS')
j=next(j for j in range(i+1,len(ps)) if ps[j].text.startswith('A evolução para JANUS'))
before=[p.text for p in ps[i+1:j]]
text=('A continuidade do artefato prevê revisar a interface, reorganizar a navegação, melhorar a apresentação dos resultados e consolidar a identidade da aplicação, amadurecendo a experiência de uso. '
      'Nessa etapa futura, o software adotará o nome JANUS, com o mesmo núcleo experimental do ESNAUTO e possibilidades de uso mais amplas. Nesta monografia, a versão dos experimentos permanece identificada como ESNAUTO.')
p=ps[i+1];p.clear();p.add_run(text);font(p,12,False,False)
for q in ps[i+2:j]:q._p.getparent().remove(q._p)
changes.append({'antes':before,'depois':text,'motivo':'Concisão e coesão (pp. 69–70), preservando todas as propostas e evitando três linhas isoladas em uma página no fim do capítulo.'})

decision_path=QA/'decisao_epigrafe.json'
if decision_path.exists() and json.loads(decision_path.read_text(encoding='utf-8')).get('estado')=='alternativa_adotada':
 from regularizar_epigrafe_fasoft import apply_decision
 apply_decision(d)
d.save(DST)
assert hashlib.sha256(SRC.read_bytes()).hexdigest()==sourcehash
data={'origem':str(SRC),'sha256_origem':sourcehash,'saida':str(DST),'alteracoes':changes,
 'classificacao_elementos':{'Tabela 2 original':'Quadro 1','Tabela 8 original':'Quadro 5'},
 'motivo':'Quadros organizam categorias e avaliações descritivas, pp. 32–33.',
 'estado':'Primeiro lote de correções; ainda sujeito à auditoria integral e renderização.'}
(QA/'alteracoes.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
print(DST)
