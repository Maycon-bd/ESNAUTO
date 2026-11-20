"""Concilia registros de revisão das células sem aprová-las automaticamente."""
import hashlib,json
from pathlib import Path
from collections import defaultdict
from docx import Document

root=Path(__file__).resolve().parents[1]; out=root/'reports/fechamento_integral_20261029'
doc=root/'reports/monografia/trabalho/fechamento_integral_20261029.docx'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(doc)=='ee6e179ab0ba157fb9f1348a1ac75c38813be767c3a27367481727f59641af50'
matrix=json.loads((out/'matriz_lote21/matriz_recodificada.json').read_text(encoding='utf8'))
decisions={(x['id'],x['dimensao']):x for x in matrix['decisoes']}; assert len(decisions)==170
evidence=defaultdict(list)
for f in sorted(out.glob('*.json')):
 try:d=json.loads(f.read_text(encoding='utf8'))
 except (ValueError,UnicodeError):continue
 if not isinstance(d,dict):continue
 for k in ['celulas_reexaminadas','celulas_revalidadas']:
  if not isinstance(d.get(k),list):continue
  for x in d[k]:
   if not isinstance(x,dict):continue
   key=(x.get('id') or x.get('fonte'),x.get('dimensao') or x.get('pergunta'))
   if key in decisions:evidence[key].append({'arquivo':str(f.relative_to(root)),'campo':k})
for code in ['D15','D21','D25']:
 for q in range(1,6):evidence[(code,'P'+str(q))].append({'arquivo':'reports/fechamento_integral_20261029/achados_leituras_lote2.json','campo':'revalidacao_celulas.'+code})
for code,name,field in [('D26','leitura_D26_sun.json','celulas'),('D01','leituras_abebe_ribeiro_lote14_parcial.json','matriz_D01')]:
 for q in range(1,6):evidence[(code,'P'+str(q))].append({'arquivo':str((out/name).relative_to(root)),'campo':field})
evidence[('D29','P4')].append({'arquivo':'reports/fechamento_integral_20261029/leituras_abebe_ribeiro_lote14_parcial.json','campo':'ribeiro_P4'})
claims={
 'P1':'A discussão de SSA-ESN no PDF 8 não especifica a distribuição que gera Win ou W; insuficiência no critério, não prova geral de ausência.',
 'P2':'PDF 8, 10 e 12 apresentam SSA para ajuste de ESN de Tian e Pei, descrito como revisão de trabalho de terceiros.',
 'P3':'PDF 8 e 15–16 descrevem normalização e outros procedimentos de estudos revisados; o artigo é revisão, não aplicação experimental própria.',
 'P4':'PDF 2 apresenta percentuais de LSTM e CNN sem demonstrar comparação pareada no mesmo problema; PDF 17 enumera métricas de modelos diferentes sem valores quantitativos pareados. Menção de superioridade na discussão SSA-ESN não acompanha números verificáveis nessa síntese.',
 'P5':'PDF 14, Tabela 1, nomeia S&P 500, NASDAQ e Dow Jones em uma caracterização de conjuntos históricos; trata-se de apresentação contextual, não experimento próprio.'}
source=root/'Artigos citados'/decisions[('D30','P1')]['arquivo_pdf']
assert sha(source)==decisions[('D30','P1')]['sha256_pdf']
row=[r for r in Document(doc).tables[2].rows if 'Vishwas' in r.cells[0].text]; assert len(row)==1
actual=[c.text.strip() for c in row[0].cells[1:6]]; expected=[decisions[('D30','P'+str(i))]['codigo'] for i in range(1,6)]; assert actual==expected==['?','S','S','?','S']
five=[]
for q in range(1,6):
 dim='P'+str(q); x=decisions[('D30',dim)]
 five.append({'dimensao':dim,'codigo_quadro':x['codigo'],'evidencia':claims[dim],'decisao':'manter'}); evidence[('D30',dim)].append({'arquivo':'reports/fechamento_integral_20261029/conferencia_matriz_vishwas_lote31.json','campo':dim})
report={'base':'v005','sha256_base':'2af31abca4e3ba9fd5caf7cd161e55472dc94edc136cdf89732c0d0401118d6b','sha256_rascunho':sha(doc),'fonte':str(source.relative_to(root)),'sha256_fonte':sha(source),'alcance':'Reexame dirigido das passagens em páginas 2, 8, 10, 12, 14–17 do PDF já objeto de leitura anterior; códigos confrontados com Quadro 1 atual. Não implica validação de todas as citações da monografia.', 'celulas_revalidadas':five,'resultado':'Cinco códigos mantidos; nenhuma alteração do Word.'}
f=out/'conferencia_matriz_vishwas_lote31.json'; assert not f.exists(); f.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
records=[]
for key,x in sorted(decisions.items()):
 assert evidence[key],key
 records.append({'fonte':key[0],'dimensao':key[1],'codigo_matriz_atual':x['codigo'],'localizador_matriz':x['localizador'],'registros':evidence[key]})
f2=out/'proveniencia_170_celulas_lote31.json'; assert not f2.exists()
f2.write_text(json.dumps({'sha256_rascunho':sha(doc),'n_celulas':len(records),'limites':'Reúne registros existentes e códigos do arquivo da matriz; não atualiza a avaliação de cada alegação nem aprova automaticamente o documento. Referências podem registrar situações anteriores e devem ser interpretadas à luz da decisão atual.', 'celulas':records},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
s=out/'estado_meta.json'; state=json.loads(s.read_text(encoding='utf8')); state['revalidacao_de_celulas_registrada']=170; state['ultimo_registro_de_leitura']=str(f.relative_to(root)); state['proveniencia_matriz']=str(f2.relative_to(root)); state['proxima_passagem']='Confrontar as afirmações atuais remanescentes e fontes suplementares; revisar Guia e similaridade contextual.'; s.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('170 células com registro identificado; cinco códigos D30 mantidos.')
