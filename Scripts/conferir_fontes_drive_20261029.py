"""Confere fontes recuperadas do Drive sem modificar planilhas ou experimentos."""
from pathlib import Path
from collections import Counter
import json, hashlib, unicodedata, re
import openpyxl

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reports/fontes_drive_20261029'
def norm(s):
    return re.sub(r'[^a-z0-9]','',unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

wf=openpyxl.load_workbook(OUT/'methodi_ordinatio.xlsx',data_only=False,read_only=True)
wc=openpyxl.load_workbook(OUT/'methodi_ordinatio.xlsx',data_only=True,read_only=True)
s=wf['2. InOrdinatio']
records=[]
for row in range(4,63):
    records.append({'linha':row,'titulo':s.cell(row,5).value,'fonte':s.cell(row,3).value,
                    'ano':s.cell(row,4).value,'doi':s.cell(row,9).value,
                    'if_sjr':s.cell(row,10).value,'decisao':s.cell(row,18).value,
                    'formula_ci':s.cell(row,13).value,'formula_score':s.cell(row,14).value,
                    'formula_rank':s.cell(row,15).value,
                    'score_cache':wc[s.title].cell(row,14).value})
ew=openpyxl.load_workbook(OUT/'extracao_completa.xlsx',data_only=False,read_only=True)
es=ew['Extração RSL']
extractions=[]
pdfs={norm(p.name):p for p in (ROOT/'Artigos citados').glob('*.pdf')}
for row in range(2,es.max_row+1):
    name=es.cell(row,1).value
    target=pdfs.get(norm(name or ''))
    extractions.append({'linha':row,'arquivo_registrado':name,'status':es.cell(row,8).value,
                        'erro':es.cell(row,9).value,'data_processamento':str(es.cell(row,10).value),
                        'pdf_local':target.relative_to(ROOT).as_posix() if target else None,
                        'sha256_pdf_local':sha(target) if target else None})
fp=wf['Fator de Impacto']
titles=[(r,fp.cell(r,2).value) for r in range(3,fp.max_row+1) if fp.cell(r,2).value]
duplicates=[]
for i,(r,t) in enumerate(titles):
    for rr,tt in titles[i+1:]:
        if norm(t)==norm(tt):duplicates.append({'linhas':[r,rr],'titulo':t})
formulas_fp=[c.coordinate for row in fp for c in row if c.data_type=='f']
summary={
 'base':'v002','sha256_base':'d41a33359e19f974dfd48eb322cb2a3877ba3cbbac20c9db941a19985076a093',
 'arquivos':[{'arquivo':p.name,'sha256':sha(p)} for p in [OUT/'methodi_ordinatio.xlsx',OUT/'extracao_completa.xlsx']],
 'protocolo':{'data_busca_declarada':wf['1. Protocolo RSL']['D7'].value,
             'bases_declaradas':wf['1. Protocolo RSL']['D8'].value,
             'string_A13':wf['1. Protocolo RSL']['A13'].value,
             'observacao_string':'Célula contém somente espaço; não foi recuperada uma consulta executável nesta aba.',
             'formula_descrita_A23':wf['1. Protocolo RSL']['A23'].value,
             'fluxo':'41 + 59 recuperados; 24 + 35 após triagem; 5 duplicatas declaradas; portfólio final informado como 59, com abstracts pendentes. 24+35-5=54, não 59; documentação requer conciliação.'},
 'candidatos':{'total':len(records),'decisoes':dict(Counter(x['decisao'] for x in records)),
               'fontes':dict(Counter(x['fonte'] for x in records)),
               'if_sjr_todos_zero':all(x['if_sjr']==0 for x in records),
               'registros':records},
 'aba_fator_impacto':{'registros':len(titles),'duplicatas_titulo':duplicates,'celulas_com_formula':formulas_fp,
                      'limite':'Dados manuais preservados; valores SJR, anos e citações não validados por simples presença. Coluna J de cálculo sem fórmulas nesta aba.'},
 'extracao':{'registros':len(extractions),'status':dict(Counter(x['status'] for x in extractions)),
             'pdfs_correspondentes':sum(x['pdf_local'] is not None for x in extractions),
             'registros_detalhados':extractions,
             'limite':'Localiza o registro histórico de extração, mas seu conteúdo é secundário e não substitui conferência nos PDFs. Não sobrescrever a matriz recodificada da v002.'},
 'comparacao_series':[],
 'limites':'Leitura somente. Não recalcula nem corrige o workbook original. Valores cache não equivalem a nova execução das fórmulas. Nenhum treino, GA ou DM executado.'}
for a,b in [('PETR4_drive.txt','Scripts/data/PETR4_close com factor_2000-2020.txt'),
            ('PETR4_drive_com_data.csv','Scripts/data/PETR4_close com factor_2000-2020_com data.csv')]:
    pa,pb=OUT/a,ROOT/b
    summary['comparacao_series'].append({'drive':a,'local':b,'sha256_drive':sha(pa),'sha256_local':sha(pb),
      'bytes_identicos':pa.read_bytes()==pb.read_bytes(),
      'texto_identico_apos_normalizar_utf8_bom_quebras_linha':pa.read_text(encoding='utf-8-sig')==pb.read_text(encoding='utf-8-sig'),
      'limite':'Identidade do conteúdo transportado não estabelece autoria da transformação original.'})
(OUT/'conferencia_planilhas_procedencia.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2,default=str),encoding='utf-8')
print(json.dumps({'candidatos':len(records),'decisoes':summary['candidatos']['decisoes'],'extracao':len(extractions),
 'pdfs_correspondentes':summary['extracao']['pdfs_correspondentes'],'duplicatas_fator':duplicates,
 'series_texto_igual':[x['texto_identico_apos_normalizar_utf8_bom_quebras_linha'] for x in summary['comparacao_series']]},ensure_ascii=False))
