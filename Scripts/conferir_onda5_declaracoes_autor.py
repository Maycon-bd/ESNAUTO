"""Busca documental somente leitura; não executa rotinas experimentais."""
from pathlib import Path
from zipfile import ZipFile,BadZipFile
import re,json,hashlib,io,subprocess,csv
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reports/esclarecimentos_autor_20261029';OUT.mkdir(exist_ok=True)
rx=re.compile(r'GA_RUN_00(?:5[3-9]|6[0-7])|0[.,]32839[5-8]|0[.,]49878[5-7]|Johnson[ _-]*SB|Dagum',re.I)
skip={'R-library','python-env','python_deps','__pycache__','site-packages'}
matches=[];checked=[];zips=[];binary=[]
def inspect(raw,loc):
 text=raw.decode('utf-8-sig',errors='replace')
 hits=[{'linha':i,'texto':t[:1600]} for i,t in enumerate(text.splitlines(),1) if rx.search(t)]
 checked.append(loc)
 if hits:matches.append({'arquivo':loc,'sha256':hashlib.sha256(raw).hexdigest(),'ocorrencias':hits})
def archive(raw,loc,depth=0):
 zips.append(loc)
 try:
  with ZipFile(io.BytesIO(raw)) as z:
   for x in z.infolist():
    if x.is_dir() or x.file_size>25_000_000:continue
    if any(p in skip for p in Path(x.filename).parts):continue
    suffix=Path(x.filename).suffix.lower()
    if suffix=='.zip' and depth<2:archive(z.read(x),loc+'::'+x.filename,depth+1)
    elif suffix in {'.csv','.txt','.log','.json'}:inspect(z.read(x),loc+'::'+x.filename)
 except BadZipFile:pass
for top in [ROOT/'Scripts/results',ROOT/'resultados_tcc']:
 for p in top.rglob('*'):
  if not p.is_file() or any(x in skip for x in p.parts):continue
  rel=p.relative_to(ROOT).as_posix()
  if p.suffix.lower() in {'.rds','.rdata','.rda'}:binary.append(rel)
  elif p.suffix.lower()=='.zip':archive(p.read_bytes(),rel)
  elif p.suffix.lower() in {'.csv','.txt','.log','.json'} and p.stat().st_size<25_000_000:inspect(p.read_bytes(),rel)
for p in ROOT.glob('*.zip'):archive(p.read_bytes(),p.name)
objects=subprocess.check_output(['git','rev-list','--objects','--all'],cwd=ROOT).decode('utf-8',errors='replace')
for line in objects.splitlines():
 oid,_,name=line.partition(' ')
 if name.lower().endswith('.zip'):archive(subprocess.check_output(['git','cat-file','blob',oid],cwd=ROOT),'git:'+oid+':'+name)
doc=ROOT/'docs/09_onda_5_ajustes_empiricos_easyfit.md'
rows=[]
for line in doc.read_text(encoding='utf-8').splitlines():
 if re.match(r'\| `GA_RUN_00(?:5[3-9]|6[0-7])`',line):rows.append([x.strip() for x in line.strip('|').split('|')])
assert len(rows)==15
with (OUT/'onda5_resultados_compilados_localizados.csv').open('w',encoding='utf-8',newline='') as f:
 w=csv.writer(f);w.writerow(['ID','Win','W','a','sr','initLen','Nx','Ridge','MAE_validacao','RMSE_validacao','MAE_teste','RMSE_teste','R2_teste','tempo']);w.writerows(rows)
result={'base':'v003','sha256_base':'eb31ed353550c8d13e388a7f51995917c1d20f52acdd946aa15a8908e0381785',
 'fontes_compiladas':{'arquivo':doc.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(doc.read_bytes()).hexdigest(),'registros':15,'ids':[r[0] for r in rows]},
 'busca':{'expressoes':rx.pattern,'arquivos_membros_examinados':len(checked),'zips_examinados_incluindo_copias':len(zips),'locais_examinados':checked,'ocorrencias':matches,'binarios_inventariados_sem_desserializacao':binary},
 'resultado':'As15linhas da Onda5 estão no relatório local e foram transcritas fielmente para facilitar localização. As ocorrências em CSVs de inventário histórico são índices de menções, não registros de execução. Nenhum novo registro primário dos15IDs foi identificado nesta busca.',
 'limites':'Busca lexical em texto até25MB,membros ZIP até25MB,profundidade2. RDS/RData apenas inventariados; não houve desserialização nem execução de R,treino,GA ou DM. Não prova inexistência dos artefatos em todo acervo.'}
(OUT/'conferencia_onda5.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'compilacao_localizada':15,'textos_examinados':len(checked),'zips':len(zips),'arquivos_com_ocorrencias':[x['arquivo'] for x in matches]},ensure_ascii=False))
