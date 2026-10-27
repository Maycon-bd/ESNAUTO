"""Extrai os registros históricos sem reexecutar a busca genética."""
from pathlib import Path
import json,re,hashlib
import numpy as np
import pandas as pd
from inject_and_test import extract_epoch_rows,build_r_matrix_win,build_r_matrix_w,build_r_matrix_wout
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reports/revisao_orientador_petr4'
OUT.mkdir(exist_ok=True)
session=ROOT/'Scripts/results/Run_20260815_140903_Test'
ranking=json.loads((session/'ranking.json').read_text(encoding='utf-8'))
sc=ranking['melhor_geral']; epoch=sc['epoca_matrizes']; n=sc['tam_reservoir']
paths={k:ROOT/sc[k].replace('\\','/') for k in ['win_file','w_file','wout_file']}
for key,dim in [('win_file',(2,n)),('w_file',(n,n)),('wout_file',(n+2,1))]:
    rows=extract_epoch_rows(str(paths[key]),epoch)
    if key!='wout_file':assert len(rows)==dim[0] and all(len(v)==dim[1] for v in rows.values())
    else:assert sum(map(len,rows.values()))==n+2
code=build_r_matrix_win(str(paths['win_file']),epoch,n)[0]+build_r_matrix_w(str(paths['w_file']),epoch,n)+build_r_matrix_wout(str(paths['wout_file']),epoch)
folder=ROOT/sc['folder_path'].replace('\\','/')
history=next(folder.glob('*resumo fitness*'))
records=[]
for line in history.read_text(encoding='utf-8').splitlines():
    m=re.match(r'"(\d+)"\s+c\(([^)]+)\)',line)
    if m:records.append([int(m[1])]+[float(v) for v in m[2].split(',')])
hist=pd.DataFrame(records,columns=['geracao','melhor_fitness','fitness_medio','fitness_minimo'])
assert len(hist)==200 and hist.geracao.tolist()==list(range(1,201))
assert abs(hist.melhor_fitness.max()-sc['fitness'])<1e-12
hist.to_csv(OUT/'historico_ga.csv',index=False)
head=f'''Sys.setlocale("LC_CTYPE", "Portuguese_Brazil.utf8")
root <- "{ROOT.as_posix()}"
out <- "{OUT.as_posix()}"
setwd(file.path(root,"app"))
source("utils/data_prep.R",encoding="UTF-8")
source("utils/metrics.R",encoding="UTF-8")
source("utils/esn_core.R",encoding="UTF-8")
tam_reservoir <- {n}
params <- list(a={sc['a']},sr={sc['sr']},initLen={sc['initLen']},tam_reservoir={n},reg={sc['reg']})
'''
tail='''
split <- dividir_dados(carregar_dados_acao("PETR4"))
v <- esn_validacao(split,params,Win,W,Wout)
t <- esn_teste(split,params,Win,W,Wout)
nt <- split$idx$treino_n; nv <- split$idx$valida_n; ne <- split$idx$teste_n
real <- split$treina_testa[(nt+2):(nt+ne)]
pred <- head(t$previsao_teste,ne-1)
datas <- read.csv2(file.path(root,"Scripts/data/PETR4_close com factor_2000-2020_com data.csv"),header=FALSE)
idx <- (nt+nv+2):(nt+nv+ne)
stopifnot(length(pred)==1298, all(is.finite(pred)))
stopifnot(abs(t$metricas_teste$MAE-0.327893716678893)<1e-9)
write.csv(data.frame(indice=idx,data=as.character(datas[idx,1]),observado=real,previsto=pred),file.path(out,"previsoes_teste.csv"),row.names=FALSE)
write.csv(data.frame(MAE_valida=v$metricas_valida$MAE,RMSE_valida=v$metricas_valida$RMSE,MAE_teste=t$metricas_teste$MAE,RMSE_teste=t$metricas_teste$RMSE),file.path(out,"metricas.csv"),row.names=FALSE)
cat("Previsões reproduzidas e conferidas contra relatório preservado.\\n")
'''
(OUT/'reproduzir_previsoes.R').write_text(head+code+tail,encoding='utf-8')
provenance={'cenario':sc,'historico_geracoes':200,'criterio_selecao':'maior fitness no lote preservado, sem seleção pelo teste',
 'original_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [*paths.values(),history]},
 'tese_referencia':'Cardoso (2025), página 90, Figuras 29 e 30 (página física 93 do PDF)',
 'limite':'Lote legado de 200 gerações; não reconstrói o melhor resultado histórico das 45 execuções de produção.'}
(OUT/'procedencia.json').write_text(json.dumps(provenance,ensure_ascii=False,indent=2),encoding='utf-8')
print(OUT)
