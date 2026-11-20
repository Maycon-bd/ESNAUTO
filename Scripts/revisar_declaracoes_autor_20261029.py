"""Incorpora declarações diretas do autor na base v003, sem alterar resultados."""
from pathlib import Path
from zipfile import ZipFile
from lxml import etree
from difflib import SequenceMatcher
from copy import deepcopy
import ast,json,hashlib,re
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'reports/monografia/versoes/v003/MayconGarciaSilva_monografia_v003.docx'
DEST=ROOT/'reports/monografia/trabalho/revisao_declaracoes_autor_20261029.docx'
OUT=ROOT/'reports/esclarecimentos_autor_20261029';OUT.mkdir(exist_ok=True)
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
W='{'+NS['w']+'}';XMLSPACE='{http://www.w3.org/XML/1998/namespace}space'
assert json.loads((ROOT/'docs/assistencia_monografia/versao_vigente.json').read_text(encoding='utf-8'))['vigente']=='v003'
assert hashlib.sha256(BASE.read_bytes()).hexdigest()=='eb31ed353550c8d13e388a7f51995917c1d20f52acdd946aa15a8908e0381785'
assert DEST.read_bytes()==BASE.read_bytes(),'Cópia já alterada: preservar antes de continuar.'
# Reutilização somente das funções puras de edição/formatação já verificadas.
# O construtor histórico não é importado nem executado.
source=ast.parse((ROOT/'Scripts/revisar_parecer_integridade_lote1.py').read_text(encoding='utf-8-sig'))
for node in source.body:
 if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='ITALIC_PHRASES' for t in node.targets):ITALIC_PHRASES=ast.literal_eval(node.value)
 if isinstance(node,ast.FunctionDef) and node.name in {'visible','replace_text','format_revised_prose'}:
  exec(compile(ast.Module(body=[node],type_ignores=[]),'<funcoes_editoriais_puras>','exec'),globals())
replacements={
244:('O ajuste de eventos corporativos pode reduzir',
     'O ajuste de eventos corporativos pode reduzir descontinuidades nos preços históricos. Nesta pesquisa, a série atribuída ao BovDB foi fornecida pelo orientador já ajustada e utilizada como entrada dos modelos. O autor não reivindica a execução da transformação original. Como não houve comparação controlada entre séries bruta e ajustada neste protocolo, não se estima o efeito causal isolado desse tratamento sobre os erros de previsão.'),
299:('Os executores de ESN preservados foram escritos',
     'A implementação partiu de códigos em R fornecidos pelo orientador, adaptados pelo autor ao contexto da pesquisa, com desenvolvimento da interface do ESNAUTO. Os fundamentos da ESN seguem Jaeger (2007). Foram empregados GA na busca genética; PerformanceAnalytics nas medidas descritivas; fGarch, PearsonDS e StockDistFit nas distribuições; fitdistrplus e MASS no ajuste; pracma na medição de tempo; e ggplot2 na visualização. O Quadro 6 distingue a base recebida e a contribuição de adaptação e interface.'),
302:('A pesquisa utiliza arquivos locais da série PETR4',
     'A pesquisa utiliza arquivos locais da série PETR4 fornecidos pelo orientador, Prof. Dr. Fabian Corrêa Cardoso, já ajustados por eventos corporativos. A procedência da série é atribuída ao BovDB (Cardoso et al., 2022b). O ativo é a ação preferencial da Petróleo Brasileiro S.A. (PETROBRAS PN). A preparação original dos arquivos antecede seu uso nesta pesquisa; a modelagem partiu dos valores recebidos.'),
304:('Os executores consultados importam os valores',
     'Os executores importam os valores de PETR4_close com factor_2000-2020.txt e PETR4_close com factor_2000-2020_com data.csv. Esses arquivos foram recebidos já ajustados do orientador, conforme esclarecimento do autor. O escopo desta pesquisa compreende sua utilização nos modelos e a organização das partições temporais. A cadeia original que liga cotações e eventos do BovDB à geração desses arquivos não foi reconstruída nesta auditoria.'),
358:('A revisão bibliográfica utiliza uma coleção',
     'A revisão de literatura reúne 34 documentos selecionados para fundamentar o trabalho. O levantamento inicial em Scopus e Springer Nature Link foi complementado por buscas externas à string inicial, conforme esclarecimento do autor, para incorporar fontes pertinentes ao desenvolvimento da pesquisa. A seleção final não decorreu exclusivamente daquela consulta nem de um ranking InOrdinatio integralmente aplicado. A coleção é apresentada como revisão de literatura com buscas complementares, sem alegação de cobertura exaustiva.'),
359:('Os registros bibliográficos originais foram recuperados',
     'A planilha methodi_ordinatio.xlsx preserva uma etapa inicial do levantamento, com busca declarada em 23 de março de 2026 e 59 candidatos, dos quais 7 estão marcados para inclusão, 4 para exclusão e 48 sem decisão. O autor esclareceu que esses registros não foram mantidos de modo a representar integralmente a seleção final e suas buscas complementares. Por isso, as contagens da planilha não são utilizadas como um fluxo completo de seleção dos 34 documentos, nem as decisões faltantes são preenchidas retrospectivamente por inferência.'),
360:('O Methodi Ordinatio (Pagani;',
     'O Methodi Ordinatio (Pagani; Kovaleski; Resende, 2015) foi considerado na organização inicial do levantamento. A planilha contém fórmulas com alfa igual a 5 e ano de referência 2026, mas seus indicadores e decisões não documentam uma aplicação concluída do método à coleção final. Assim, as pontuações não são usadas para justificar a inclusão ou estabelecer a relevância relativa dos 34 documentos. Os registros originais são preservados como documentação intermediária do processo.'),
457:('A contribuição de software desta pesquisa surgiu',
     'O desenvolvimento do ESNAUTO partiu de códigos em R fornecidos pelo orientador. O autor adaptou essas rotinas ao contexto da pesquisa e construiu a interface para organizar a execução dos experimentos. A aplicação reúne seleção de configurações, acompanhamento de execuções, histórico e visualização dos resultados. Essa contribuição compreende adaptação e desenvolvimento da interface sobre uma base computacional recebida; não se apresenta toda a implementação matemática como criação original do autor.'),
486:('Foram investigadas famílias probabilísticas',
     'Foram investigadas famílias probabilísticas em Win e W, selecionados hiperparâmetros por AG e comparados resultados com ESN Normal × Normal, LSTM e GRU. O ESNAUTO organizou o processo e suas saídas, e H1 recebeu análise inferencial complementar pelo teste de Diebold-Mariano. A série foi fornecida já ajustada pelo orientador. A contribuição do autor compreendeu a adaptação dos códigos em R recebidos e o desenvolvimento da interface. Permanecem os limites de comparação e de preservação dos artefatos históricos.'),
493:('A contribuição de Engenharia de Software documentada',
     'A contribuição de Engenharia de Software compreendeu a adaptação dos códigos em R fornecidos pelo orientador ao contexto da pesquisa e a construção da interface do ESNAUTO. A aplicação organiza preparação dos dados recebidos, execução dos modelos, configurações, métricas, histórico e visualizações. O Quadro 6 distingue fundamentos anteriores, base computacional recebida e desenvolvimento do autor. Essa atribuição reconhece a procedência das rotinas sem reivindicar criação original das técnicas combinadas.')}
with ZipFile(BASE) as z:
 tree=etree.fromstring(z.read('word/document.xml'));body=tree.find(W+'body');ps=body.findall(W+'p');log=[]
 # Alterações pontuais nos resumos mantêm os demais trechos e seus runs.
 for i,pairs in {
 41:[('Os modelos receberam arquivos identificados como previamente ajustados por eventos corporativos. A documentação preservada não identifica a autoria da transformação original, e o efeito causal isolado do ajuste não foi estimado.',
       'Os dados foram fornecidos já ajustados por eventos corporativos pelo orientador; o efeito causal isolado do ajuste não foi estimado.'),
      ('Foi desenvolvido o ESNAUTO, infraestrutura experimental que integra',
       'A implementação do ESNAUTO adaptou códigos em R fornecidos pelo orientador e incluiu uma interface desenvolvida pelo autor, integrando')],
 44:[('The models received files identified as previously adjusted for corporate events. The preserved documentation does not identify who performed the original transformation, and the isolated causal effect of the adjustment was not estimated.',
       'The supervisor provided the data already adjusted for corporate events; the isolated causal effect of the adjustment was not estimated.'),
      ('ESNAUTO was developed as an experimental framework integrating',
       'The ESNAUTO implementation adapted R code provided by the supervisor and included an interface developed by the author, integrating')]
 }.items():
  old=visible(ps[i]);new=old
  for a,b in pairs:assert a in new;new=new.replace(a,b,1)
  assert re.findall(r'\d+(?:[.,]\d+)*',old)==re.findall(r'\d+(?:[.,]\d+)*',new)
  assert 150<=len(new.split())<=500
  replace_text(ps[i],new);log.append({'paragrafo_v003':i,'antes':old,'depois':new,'motivo':'Declarações2e4: fornecimento dos dados ajustados e códigos R pelo orientador; adaptação/interface pelo autor.'})
 for i,(prefix,new) in replacements.items():
  old=visible(ps[i]);assert old.startswith(prefix);assert len(new)<=700
  assert not ps[i].xpath('.//w:fldChar|.//w:hyperlink',namespaces=NS)
  replace_text(ps[i],new);format_revised_prose(ps[i],i)
  log.append({'paragrafo_v003':i,'antes':old,'depois':new,'motivo':'Declaração1: seleção com buscas complementares e registros intermediários.' if i in (358,359,360) else 'Declarações2e4: atribuição do fornecimento dos dados/códigos e da adaptação/interface.'})
 tables=body.findall(W+'tbl');table=tables[-1];row=table.findall(W+'tr')[-1];cells=row.findall(W+'tc');tl=[]
 for col,new in [(1,'Dados e códigos em R fornecidos pelo orientador'),(2,'Série recebida já ajustada. O autor adaptou as rotinas à pesquisa e desenvolveu a interface; a transformação original dos preços não foi reconstruída nesta auditoria.')]:
  p=cells[col].find(W+'p');old=visible(p);replace_text(p,new);format_revised_prose(p,8000+col);tl.append({'tabela':len(tables)-1,'linha':len(table.findall(W+'tr'))-1,'coluna':col,'antes':old,'depois':new})
 # Comparar a árvore inteira com a origem acrescida somente dos nós autorizados.
 original=etree.fromstring(z.read('word/document.xml'));ob=original.find(W+'body');ops=ob.findall(W+'p')
 for i in [41,44,*replacements]:ob.replace(ops[i],deepcopy(ps[i]))
 ot=ob.findall(W+'tbl')[-1];ot.getparent().replace(ot,deepcopy(table))
 assert etree.tostring(original,method='c14n')==etree.tostring(tree,method='c14n')
 tmp=DEST.with_suffix('.tmp.docx');raw=etree.tostring(tree,xml_declaration=True,encoding='UTF-8',standalone=True)
 with ZipFile(tmp,'w') as out:
  for item in z.infolist():out.writestr(item,raw if item.filename=='word/document.xml' else z.read(item.filename))
 tmp.replace(DEST)
 (OUT/'alteracoes_editoriais.json').write_text(json.dumps({'base':'v003','sha256_base':hashlib.sha256(BASE.read_bytes()).hexdigest(),'sha256_trabalho':hashlib.sha256(DEST.read_bytes()).hexdigest(),'paragrafos':log,'celulas':tl,'verificacao':'12parágrafos e2células autorizados; demais nós e partes OOXML preservados. Tokens numéricos dos resumos preservados.'},ensure_ascii=False,indent=2),encoding='utf-8')
print('12 parágrafos e duas células atualizados; base v003 preservada.')
