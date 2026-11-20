"""Índice do texto corrente para auditoria humana de cada ocorrência."""
from collections import Counter
import hashlib,json
from pathlib import Path
from docx import Document

root=Path(__file__).resolve().parents[1]; out=root/'reports/fechamento_integral_20261029'
doc=root/'reports/monografia/trabalho/fechamento_integral_20261029.docx'; sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(doc)=='ee6e179ab0ba157fb9f1348a1ac75c38813be767c3a27367481727f59641af50'
x=json.loads((root/'reports/correcao_parecer_integridade/cruzamento_lote32.json').read_text(encoding='utf8'))
assert x['sha256_alvo']==sha(doc) and len(x['referencias'])==50 and not x['sem_correspondencia']
mapping={'R01':'D01','R02':'D02','R05':'D03','R07':'D04','R11':'D05','R13':'D06','R14':'D07','R15':'D08','R16':'D09','R19':'D10','R18':'D11','R20':'D12','R23':'D13','R24':'D14','R28':'D15','R29':'D16','R32':'D17','R31':'D18','R34':'D19','R35':'D20','R37':'D21','R39':'D22','R40':'D23','R41':'D24','R42':'D25','R43':'D26','R44':'D27','R45':'D28','R38':'D29','R46':'D30','R47':'D31','R48':'D32','R49':'D33','R50':'D34'}
assert len(mapping)==34 and len(set(mapping.values()))==34
M=json.loads((out/'proveniencia_170_celulas_lote31.json').read_text(encoding='utf8'))
base=json.loads((root/'reports/bibliometria_reconstrucao/base_reconstruida.json').read_text(encoding='utf8'))
docs={a['id']:a for a in base['records']}
loaded=Document(doc); cells={}; seen=set()
manual=[('R22',39,'Gleick, 1987, par. 1'),('R06',319,'Cardoso, Berri e Mattos (2022a, p. 203)'),('R10',392,'Cardoso (2025, p. 90)'),('R10',396,'Cardoso (2025, Figura 29)'),('R10',401,'Cardoso (2025, Figura 30)'),('R06',451,'Cardoso, Berri e Mattos (2022a, p. 202–205)')]
for ti,t in enumerate(loaded.tables):
 for ri,row in enumerate(t.rows):
  for ci,c in enumerate(row.cells):
   if c._tc in seen:continue
   seen.add(c._tc)
   for pi,p in enumerate(c.paragraphs): cells[f'T_atual{ti}/L{ri}/C{ci}/P{pi}']=p.text
def text_at(loc):
 if loc.startswith('P_atual'):return loaded.paragraphs[int(loc[7:])].text
 return cells[loc]
ref_records=[]
for ref in x['referencias']:
 r=ref['id']; citations=[{'local':o['local'],'chamada':o['citacao'],'contexto':text_at(o['local'])} for o in x['registros'] if r in o['referencias']]
 for target,idx,label in manual:
  if target==r:
   assert label.casefold() in loaded.paragraphs[idx].text.casefold()
   citations.append({'local':f'P_atual{idx:04d}','chamada':label,'contexto':loaded.paragraphs[idx].text,'identificacao':'conferência manual de chamada com localizador'})
 row={'id':r,'referencia_atual':ref['texto'],'ano_citado':ref['ano_bibliografico'],'ocorrencias':citations,'estado':'exige_confronto_do_contexto_nao_aprovado_automaticamente'}
 if r in mapping:
  sid=mapping[r]; original=docs[sid]; source=root/'Artigos citados'/original['arquivo_pdf']; assert sha(source)==original['sha256_pdf']
  row.update(fonte_id=sid,arquivo_fonte=str(source.relative_to(root)),sha256_fonte=sha(source),titulo_registro_historico=original['title'],ano_registro_historico=original['year'],evidencias_matriz=[z for z in M['celulas'] if z['fonte']==sid])
  if r in ['R02','R18']:row['nota_ano']='Registro bibliométrico histórico difere da referência atual; conferir a edição/versão documentada, não substituir o ano automaticamente.'
 else:
  row['fonte_id']='suplementar'; row['nota']='Consultar registros específicos de leitura; correspondência autor–ano não prova conteúdo nem acesso integral.'
 ref_records.append(row)
assert sum(len(r['ocorrencias']) for r in ref_records)==len(x['registros'])+len(manual)
f=out/'indice_citacoes_atuais_lote32.json'; assert not f.exists()
f.write_text(json.dumps({'base':'v005','sha256_base':'2af31abca4e3ba9fd5caf7cd161e55472dc94edc136cdf89732c0d0401118d6b','sha256_rascunho':sha(doc),'referencias':len(ref_records),'ocorrencias_reconhecidas':len(x['registros']),'ocorrencias_adicionadas_manualmente':len(manual),'correspondencias_ausentes':len(x['sem_correspondencia']),'limites':'Reconhecedor autor–ano guiado pelos nomes na lista pode deixar de detectar chamadas sem referência ou formatos diferentes; contexto e identidade precisam ser conferidos. Ligar um arquivo fonte ou uma célula da matriz não prova que a fonte apoia cada afirmação do contexto. Os 34 vínculos são de localização da fonte, não aprovação científica.','registros':ref_records},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
s=out/'estado_meta.json'; d=json.loads(s.read_text(encoding='utf8')); d['indice_citacoes_atual']=str(f.relative_to(root)); d['ultimo_registro_de_leitura']=str(f.relative_to(root)); d['proxima_passagem']='Confrontar os contextos do índice com os relatórios e fontes primárias, revisar chamadas que não correspondam ao padrão e fontes suplementares.'; s.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('Índice criado:',len(ref_records),'referências e',len(x['registros']),'ocorrências reconhecidas.')
