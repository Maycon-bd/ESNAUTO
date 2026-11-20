from pathlib import Path
from collections import Counter
from zipfile import ZipFile
import hashlib,json,re,unicodedata
import pdfplumber
from lxml import etree as E

ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
A=json.loads((OUT/'estrutura.json').read_text(encoding='utf-8'))
PDF=ROOT/'reports/busca_lacunas_20261101/candidata.pdf'
checks=[]
def check(name,ok,detail):checks.append({'controle':name,'conforme':bool(ok),'evidencia':detail})
def on(v):return v is True or isinstance(v,dict) and v.get('val','1') not in ['0','false','off']
def norm(t):return ''.join(c for c in unicodedata.normalize('NFKC',t).casefold() if c.isalnum())
for i,s in enumerate(A['secoes'],1):
 check(f'A4 e margens seção{i}',s['pgSz']=={'w':'11906','h':'16838'} and all(s['pgMar'][k]==v for k,v in {'top':'1701','left':'1701','bottom':'1134','right':'1134'}.items()),s['pgMar'])
ps=A['paragrafos'];body=[p for p in ps if 166<p['indice']<502 and p['texto'] and p['estilo']=='Normal' and not p['texto'].startswith(('Fonte:','Nota:'))]
check('Corpo emTimesNewRoman12',all(r['propriedades'].get('rFonts',{}).get('ascii')=='Times New Roman' and r['propriedades'].get('sz',{}).get('val')=='24' for p in body for r in p['runs']),{'paragrafos':len(body),'runs':sum(len(p['runs']) for p in body)})
check('Texto preto',all(r['propriedades'].get('color',{}).get('val') in [None,'auto','000000'] for p in ps for r in p['runs']),'Todos os runs dos554parágrafos principais; verificação de tabelas separada')
check('Corpo justificado e1,5',all(p['paragrafo'].get('jc',{}).get('val')=='both' and p['paragrafo'].get('spacing',{}).get('line')=='360' for p in body),len(body))
check('Recuo do corpo1,25cm',all(p['paragrafo'].get('ind',{}).get('firstLine')=='709' for p in body),'709twips; alíneas têm deslocamento específico')
heads=[p for p in ps if p['estilo'] in ['TITULOTCC','SEOTCC','SUBO2']]
check('Hierarquia de41títulos',all(p['paragrafo'].get('jc',{}).get('val')==('center' if p['texto']=='REFERÊNCIAS' else 'both') and all(r['propriedades'].get('sz',{}).get('val')=='24' for r in p['runs']) and all(on(r['propriedades'].get('b'))==(p['estilo']!='SEOTCC') for r in p['runs']) for p in heads),len(heads))
check('Títulos vinculados ao próximo parágrafo',all(on(p['paragrafo'].get('keepNext')) for p in heads),len(heads))
intro=ps[167:182]
check('Introdução contínua semsubseções/objetos',all(p['estilo']=='Normal' and p['imagens']==0 and p['equacoes']==0 for p in intro),{'paragrafos':len(intro)})
check('Introdução semcitaçõesautor-data',not any(re.search(r'\b[A-ZÀ-Ý][a-zà-ÿ]+.{0,35}\(\d{4}[a-z]?\)',p['texto']) for p in intro),'Triagem dirigida dos15parágrafos; texto lido nas páginas18–20')
caps=[p for p in ps if p['estilo']=='Legenda']
check('19legendas10simplessem ponto',all(not p['texto'].rstrip().endswith('.') and p['paragrafo'].get('spacing',{}).get('line')=='240' and all(r['propriedades'].get('sz',{}).get('val')=='20' for r in p['runs']) for p in caps),len(caps))
sources=[p for p in ps if p['texto'].startswith('Fonte:')]
check('19fontes10simplescom ponto/ano',len(sources)==19 and all(p['texto'].endswith('.') and re.search(r'\b20\d\d[a-z]?\b',p['texto']) and p['paragrafo'].get('spacing',{}).get('line')=='240' and all(r['propriedades'].get('sz',{}).get('val')=='20' for r in p['runs']) for p in sources),len(sources))
for kind,total in [('Figura',6),('Quadro',6),('Tabela',7)]:
 nums=[int(re.match(r'\w+ (\d+)',p['texto'])[1]) for p in caps if p['texto'].startswith(kind)]
 check(f'Sequência{kind}',nums==list(range(1,total+1)),nums)
for i,t in enumerate(A['tabelas'][1:],1):
 allp=[p for row in t['linhas'] for c in row['celulas'] for p in c['paragrafos']]
 check(f'Tabela nativa{i}:fonte11/simples/cabeçalho',all(p['paragrafo'].get('spacing',{}).get('line')=='240' and all(r['propriedades'].get('sz',{}).get('val')=='22' for r in p['runs']) for p in allp) and all(on(r['propriedades'].get('b')) for c in t['linhas'][0]['celulas'] for p in c['paragrafos'] for r in p['runs']),{'linhas_incl_cabecalho':len(t['linhas']),'colunas':len(t['grid'])})
 check(f'Tabela nativa{i}:largura16cm',t['propriedades'].get('tblW')=={'w':'9071','type':'dxa'} and sum(map(int,t['grid']))==9071,'9071twips; inclui tabelas cuja largura não é fixada pelo modelo')
refs=[p for p in ps if p['estilo']=='Referencias']
check('51referências12simplesalinhadasàesquerda',len(refs)==51 and all(p['paragrafo'].get('jc',{}).get('val')=='left' and p['paragrafo'].get('spacing',{}).get('line')=='240' and all(r['propriedades'].get('sz',{}).get('val')=='24' for r in p['runs']) for p in refs),len(refs))
for idx in [41,44]:
 p=ps[idx];check(f'Resumo parágrafo{idx}:150–500palavras/12simples/semrecuo',150<=len(p['texto'].split())<=500 and p['paragrafo'].get('spacing',{}).get('line')=='240' and p['paragrafo'].get('ind',{}).get('firstLine')=='0',len(p['texto'].split()))
check('Cinco palavras-chave PT/EN',all(len(ps[i]['texto'].split(';'))==5 and ps[i]['texto'].endswith('.') for i in [42,45]),[ps[i]['texto'] for i in [42,45]])
check('Semrevisõespendentes',A['revisoes']=={'insercoes':0,'exclusoes':0},A['revisoes'])

pages=[];lines=[];stream='';positions=[];outside=[]
with pdfplumber.open(PDF) as pdf:
 for pi,page in enumerate(pdf.pages,1):
  words=page.extract_words();page_lines=page.extract_text_lines()
  page_text='\n'.join(x['text'] for x in page_lines)
  pages.append({'pagina_pdf':pi,'texto':page_text,'largura':page.width,'altura':page.height})
  header=[x['text'] for x in page_lines if x['top']<80]
  if pi<18:check(f'Paginação oculta p{pi}',not header,header)
  else:check(f'Número da página{pi}',header==[str(pi-1)],header)
  for li,line in enumerate(page_lines):
   if line['top']<80:continue
   item={'pagina_pdf':pi,'linha_pagina':li,'texto':line['text'],'top':line['top'],'bottom':line['bottom'],'x0':line['x0'],'x1':line['x1']}
   line_id=len(lines);lines.append(item)
   n=norm(line['text']);stream+=n;positions.extend([line_id]*len(n))
  for word in words:
   if word['x0']<84 or word['x1']>539.7 or word['bottom']>786.5:outside.append({'pagina_pdf':pi,**word})
check('PDF78páginasA4',len(pages)==78 and all(abs(p['largura']-595.3)<1 and abs(p['altura']-841.9)<1 for p in pages),len(pages))
check('TextoPDFdentrodamanchagráfica',not outside,{'ocorrencias':outside,'tolerancia_pontos':1.2})
render_pages={p['pagina_pdf']:norm('\n'.join(x['texto'] for x in lines if x['pagina_pdf']==p['pagina_pdf'])) for p in pages}
past=json.loads((ROOT/'reports/busca_lacunas_20261101/paginacao_candidata.json').read_text(encoding='utf-8-sig'))
entries=[]
for title in past['titles']:
 expected=(title.get('number') or '')+title['title']
 check('Título na página:'+expected,norm(expected) in render_pages[title['physicalPage']],{'pagina_pdf':title['physicalPage'],'pagina_exibida':title['page']})
for p in ps:
 if p['indice']>=166:continue
 if p['estilo'].startswith('Sumrio'):
  final=p['runs'][-1]['texto'];assert final.isdigit();expected=p['texto'][:-len(final)];number=int(final)
  ok=norm(expected) in render_pages.get(number+1,'')
  entries.append({'titulo':expected,'pagina_indicada':number,'conforme':ok,'tipo':'sumario'})
 elif re.match(r'^(Figura|Quadro|Tabela) \d+\s*[–-]',p['texto']):
  final=p['runs'][-1]['texto'];assert final.isdigit();expected=p['texto'][:-len(final)];number=int(final);ok=norm(expected) in render_pages.get(number+1,'')
  entries.append({'titulo':expected,'pagina_indicada':number,'conforme':ok,'tipo':'lista'})
check('60entradaslistas/sumárioconciliadas',len(entries)==60 and all(x['conforme'] for x in entries),{'total':len(entries),'falhas':[x for x in entries if not x['conforme']]})

# Comprimento real dos parágrafos: alinhamento exato ao texto PDF normalizado.
# Casos com equações ou diferenças de extração não são considerados aprovados.
paragraphs=[]
for p in body:
 n=norm(p['texto']);pos=stream.find(n);end=pos+len(n);method='correspondência integral normalizada'
 if pos<0 and len(n)>100:
  left=n[:45];right=n[-45:];start=stream.find(left);finish=stream.find(right,start+45)
  if start>=0 and finish>=0 and stream.find(left,start+1)<0 and stream.find(right,finish+1)<0 and .8*len(n)<finish+45-start<1.2*len(n):
   pos=start;end=finish+45;method='âncoras únicas de45caracteres no início/fim; intervalo limitado'
 if pos<0:
  paragraphs.append({'indice_xml':p['indice'],'inicio':p['texto'][:100],'medicao':'não localizada por correspondência exata'});continue
 ls=list(dict.fromkeys(positions[pos:end]));perpage=Counter(lines[i]['pagina_pdf'] for i in ls)
 paragraphs.append({'indice_xml':p['indice'],'inicio':p['texto'][:100],'linhas':len(ls),'por_pagina_pdf':dict(perpage),'metodo':method,'alinea':bool(re.match(r'^[a-f]\)',p['texto'])),'faixa_recomendada_4a7':4<=len(ls)<=7,'uma_linha_na_quebra':len(perpage)>1 and any(v==1 for v in perpage.values())})
result={'base':'v010','sha256_docx':A['sha256'],'pdf_sha256':hashlib.sha256(PDF.read_bytes()).hexdigest(),'controles':checks,'contagem':{'total':len(checks),'conformes':sum(x['conforme'] for x in checks),'falhas':sum(not x['conforme'] for x in checks)},'entradas':entries,'paragrafos_medidos':paragraphs,'paginas':pages}
(OUT/'conferencia.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'contagem':result['contagem'],'falhas':[x for x in checks if not x['conforme']],'paragrafos_medidos':sum('linhas' in x for x in paragraphs),'longos':sum(x.get('linhas',0)>7 for x in paragraphs),'curtos':sum(0<x.get('linhas',0)<4 for x in paragraphs),'uma_linha_na_quebra':[x for x in paragraphs if x.get('uma_linha_na_quebra')]},ensure_ascii=True))
