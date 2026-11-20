"""Mapeia ocorrências reconhecidas ao escopo dos registros de evidência existentes."""
from collections import Counter
import hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parents[1];out=root/'reports/fechamento_integral_20261029';doc=root/'reports/monografia/trabalho/fechamento_integral_20261029.docx';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert sha(doc)=='61fac8da8ab082633bbaa113ed697fd32ccfd7d72c2142f003b18b5b10083e2a'
index=json.loads((out/'indice_citacoes_atuais_lote50.json').read_text(encoding='utf8'));assert index['sha256_rascunho']==sha(doc)
refs=index['registros'];by_source={r['fonte_id']:r['id'] for r in refs if r.get('fonte_id') not in (None,'suplementar')};evidence={}
for f in sorted(out.glob('afirmacoes_*lote*.json')):
 o=json.loads(f.read_text(encoding='utf8'))
 for r in o.get('registros',[]):
  rid=r.get('referencia') or by_source.get(r.get('fonte_id'));loc=r.get('ancora')
  if not rid or not loc:continue
  evidence.setdefault((rid,loc),[]).append({'arquivo':str(f.relative_to(root)),'sha256_registro':sha(f),'texto_examinado':r.get('texto_atual'),'evidencia':r.get('evidencia'),'localizador':r.get('localizador'),'diagnostico':r.get('diagnostico')})
rows=[]
for r in refs:
 for occurrence in r['ocorrencias']:
  loc=occurrence['local'];context=occurrence['contexto'];found=evidence.get((r['id'],loc),[])
  same=[e for e in found if e['texto_examinado']==context];different=[e for e in found if e['texto_examinado']!=context]
  if same:status='evidencia_dirigida_contexto_identico'
  elif different:status='evidencia_anterior_contexto_alterado_reavaliar'
  elif loc.startswith('T_atual2/') and r.get('fonte_id','').startswith('D'):status='linha_matriz_com_proveniencia_p1_p5_verificar_chamada'
  else:status='sem_vinculo_individual_neste_indice'
  rows.append({'referencia':r['id'],'fonte_id':r.get('fonte_id'),'local':loc,'chamada':occurrence['chamada'],'contexto_atual':context,'situacao':status,'evidencias':same or different,'proveniencia_matriz':'reports/fechamento_integral_20261029/proveniencia_170_celulas_lote31.json' if status.startswith('linha_matriz') else None})
counts=Counter(r['situacao'] for r in rows);f=out/'cobertura_citacoes_lote51.json';assert not f.exists();result={'base':'v005','sha256_base':'2af31abca4e3ba9fd5caf7cd161e55472dc94edc136cdf89732c0d0401118d6b','sha256_rascunho':sha(doc),'indice':str((out/'indice_citacoes_atuais_lote50.json').relative_to(root)),'quantidade_ocorrencias_no_indice':len(rows),'contagens':dict(counts),'registros':rows,'limites':'Vínculo automatizado por referência, âncora e texto exato não é julgamento de fidelidade: registros têm alcance delimitado e um parágrafo pode conter outras afirmações. Não identifica todas as citações fora do padrão e não substitui avaliação dos textos e tabelas. Outras evidências ainda não ligadas podem existir em relatórios anteriores. Contextos modificados precisam de revisão antes de reaproveitar o registro.','acao':'Priorizar ocorrências sem vínculo e contextos alterados; não considerar este inventário como auditoria concluída.'};f.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8');s=out/'estado_meta.json';state=json.loads(s.read_text(encoding='utf8'));state['cobertura_citacoes']=str(f.relative_to(root));state['proxima_passagem']='Revisar ocorrências sem vínculo individual e contextos alterados; manter limites do reconhecedor.';s.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print(json.dumps(counts,ensure_ascii=False))
