"""Revisão documental v002: incorpora as duas planilhas originais recuperadas."""
from pathlib import Path
from zipfile import ZipFile
from lxml import etree
from difflib import SequenceMatcher
from copy import deepcopy
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'reports/monografia/versoes/v002/MayconGarciaSilva_monografia_v002.docx'
DEST=ROOT/'reports/monografia/trabalho/revisao_fontes_drive_20261029_final.docx'
OUT=ROOT/'reports/fontes_drive_20261029'
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
W='{'+NS['w']+'}'
assert json.loads((ROOT/'docs/assistencia_monografia/versao_vigente.json').read_text(encoding='utf-8'))['vigente']=='v002'
assert hashlib.sha256(BASE.read_bytes()).hexdigest()=='d41a33359e19f974dfd48eb322cb2a3877ba3cbbac20c9db941a19985076a093'
assert DEST.read_bytes()==BASE.read_bytes(),'A cópia de trabalho já foi alterada; preservar antes de continuar.'
replacements={
358:('A revisão bibliográfica utiliza uma coleção',
     'A revisão bibliográfica utiliza uma coleção de 34 documentos disponíveis no acervo da pesquisa, reconstruída para permitir a conferência das fontes. As planilhas originais recuperadas declaram buscas em Scopus e Springer Nature Link em 23 de março de 2026, com 41 e 59 registros, respectivamente. Esses quantitativos são registros do processo relatado, sem confirmação por exportações diretas das plataformas. A coleção de 34 documentos corresponde ao material recuperado para análise e não equivale ao total inicial de resultados da busca.'),
319:('Os hiperparâmetros que controlaram',
     'Os hiperparâmetros otimizados pelo AG são apresentados no Quadro 3. As faixas e os 55 bits correspondem à codificação do ESNAUTO; as referências fundamentam os conceitos, sem fornecer esses intervalos específicos. Cardoso et al. (2022a, p. 203), por exemplo, utilizaram valores fixos de 1,25 para o raio espectral, 0,2 para a taxa de vazamento e 10⁻⁸ para a regularização, em um protocolo distinto.'),
451:('Esta pesquisa avaliou cinco ondas',
     'Cardoso et al. (2022a, p. 202–205) avaliaram a PETR4 com e sem fator de ajuste, com 5.197 observações e divisão de 75% para treino e 25% para teste. Com hiperparâmetros fixos, relataram RMSE de 11,1785 sem fator e de 0,4987 com fator. Esses valores contextualizam um estudo anterior, mas não constituem um teste de superioridade desta pesquisa: a partição, os hiperparâmetros e o procedimento de seleção diferem. O resultado com fator não deve ser atribuído à série sem ajuste.'),
359:('A documentação anterior descreve uma busca voltada',
     'Os registros bibliográficos originais foram recuperados no acervo do autor. A planilha methodi_ordinatio.xlsx declara busca em Scopus e Springer Nature Link em 23 de março de 2026, com critérios de idioma, período e tema. Seu portfólio contém 59 candidatos: 7 marcados para inclusão, 4 para exclusão e 48 sem decisão. A string de busca está vazia e as contagens de duplicatas e do fluxo precisam de conciliação. Esses registros documentam uma etapa intermediária, sem demonstrar uma seleção sistemática concluída dos 34 documentos analisados.'),
360:('O Methodi Ordinatio (Pagani;',
     'O Methodi Ordinatio (Pagani; Kovaleski; Resende, 2015) orientou a organização registrada na planilha original, com alfa igual a 5 e ano de referência 2026. A aba de 59 candidatos contém fórmulas de pontuação e ordenação, mas todos os campos de fator de impacto estão zerados. Outra aba reúne indicadores manuais, com um título duplicado e sem cálculo final preenchido. Esses registros não sustentam uma ordenação validada dos 34 documentos, nem permitem considerar os indicadores e suas datas de coleta integralmente conferidos.'),
361:('A documentação da pesquisa menciona as planilhas',
     'A planilha extracao_completa.xlsx preserva 34 registros de extração, com respostas às perguntas P1–P5, status e datas de processamento. Os nomes correspondem aos 34 PDFs locais. Essas respostas constituem registros intermediários de leitura, cuja fidelidade depende da conferência nos trabalhos originais. Por isso, a síntese desta monografia utiliza a matriz recodificada do Quadro 1, com localizadores, distinção entre evidência direta e secundária e marcação de informação insuficiente, preservando separadamente a extração histórica.')}

def text(p):return ''.join(p.xpath('.//w:t/text()',namespaces=NS))
def replace(p,new):
 old=text(p)
 for tag,a,b,c,d in reversed(SequenceMatcher(None,old,new,autojunk=False).get_opcodes()):
  if tag=='equal':continue
  offsets=[];pos=0
  for node in p.xpath('.//w:t',namespaces=NS):
   t=node.text or '';offsets.append((node,pos,pos+len(t)));pos+=len(t)
  if a==b:
   node,s,e=next(((n,s,e) for n,s,e in offsets if s<=a<=e),offsets[-1])
   t=node.text or '';node.text=t[:a-s]+new[c:d]+t[a-s:]
  else:
   for j,(node,s,e) in enumerate((n,s,e) for n,s,e in offsets if s<b and e>a):
    t=node.text or '';node.text=t[:max(0,a-s)]+(new[c:d] if j==0 else '')+t[min(len(t),b-s):]
 for n in p.xpath('.//w:t',namespaces=NS):n.set('{http://www.w3.org/XML/1998/namespace}space','preserve')
 assert text(p)==new
 # Estes parágrafos não contêm campos nem hyperlinks. Normalizar somente
 # o itálico textual e reaplicá-lo exatamente à expressão estrangeira.
 for r in list(p.findall(W+'r')):
  tnodes=r.findall(W+'t')
  if len(tnodes)!=1:continue
  value=tnodes[0].text or ''
  props=r.find(W+'rPr')
  if props is None:props=etree.Element(W+'rPr');r.insert(0,props)
  for prop in props.findall(W+'i'):props.remove(prop)
  no=etree.SubElement(props,W+'i');no.set(W+'val','0')
 # A expressão pode atravessar runs após a edição. Dividir pelos offsets
 # globais conserva as propriedades dos demais caracteres.
 for phrase in ['Methodi Ordinatio','et al.']:
  start=new.find(phrase);end=start+len(phrase)
  if start<0:continue
  pos=0
  for r in list(p.findall(W+'r')):
   nodes=r.findall(W+'t')
   if len(nodes)!=1:continue
   value=nodes[0].text or '';stop=pos+len(value)
   cuts=sorted({0,len(value),max(0,min(len(value),start-pos)),max(0,min(len(value),end-pos))})
   for a,b in zip(cuts,cuts[1:]):
    if a==b:continue
    clone=deepcopy(r);clone.find(W+'t').text=value[a:b]
    if pos+a>=start and pos+b<=end:clone.find(W+'rPr').find(W+'i').set(W+'val','1')
    r.addprevious(clone)
   p.remove(r);pos=stop
 assert text(p)==new

with ZipFile(BASE) as z:
 tree=etree.fromstring(z.read('word/document.xml'));body=tree.find(W+'body');ps=body.findall(W+'p')
 log=[]
 for i,(prefix,new) in replacements.items():
  old=text(ps[i]);assert old.startswith(prefix);assert len(new)<=700
  assert not ps[i].xpath('.//w:fldChar|.//w:hyperlink',namespaces=NS)
  replace(ps[i],new);log.append({'paragrafo_v002':i,'antes':old,'depois':new,'motivo':'F19: original RBras lido visualmente, p. 197–206; distinguidos conceitos, faixas locais e protocolos.' if i in (319,451) else 'F18/R01: planilhas originais recuperadas no Drive e conferidas; preservadas suas limitações.'})
 original=etree.fromstring(z.read('word/document.xml'));ops=original.find(W+'body').findall(W+'p')
 for i in replacements:ops[i].getparent().replace(ops[i],deepcopy(ps[i]))
 assert etree.tostring(original,method='c14n')==etree.tostring(tree,method='c14n')
 data=etree.tostring(tree,xml_declaration=True,encoding='UTF-8',standalone=True)
 tmp=DEST.with_suffix('.tmp.docx')
 with ZipFile(tmp,'w') as out:
  for info in z.infolist():out.writestr(info,data if info.filename=='word/document.xml' else z.read(info.filename))
 tmp.replace(DEST)
 (OUT/'alteracoes_word_final.json').write_text(json.dumps({'base':'v002','sha256_base':hashlib.sha256(BASE.read_bytes()).hexdigest(),'sha256_trabalho':hashlib.sha256(DEST.read_bytes()).hexdigest(),'alteracoes':log,'verificacao':'Somente seis parágrafos do corpo alterados; demais nós e partes OOXML preservados.'},ensure_ascii=False,indent=2),encoding='utf-8')
print('Seis parágrafos atualizados; estrutura e demais partes preservadas.')
