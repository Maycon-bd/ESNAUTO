"""Conferência aritmética de dados/vetores preservados; não executa modelos ou DM."""
import csv,hashlib,json,math,statistics
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reports/fechamento_integral_20261029'
RUN=ROOT/'Scripts/results/diebold_mariano/controlled_runs/seed_20260926'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def rows(p):return list(csv.DictReader(p.read_text(encoding='utf-8-sig').splitlines()))
def metrics(real,pred):
    error=[a-b for a,b in zip(real,pred)];mse=statistics.fmean(v*v for v in error)
    center=statistics.fmean(real);sst=sum((v-center)**2 for v in real)
    return dict(MAE=statistics.fmean(abs(v) for v in error),MSE=mse,RMSE=math.sqrt(mse),
                MAPE_percent=100*statistics.fmean(abs(v/y) for v,y in zip(error,real)),
                R2=1-sum(v*v for v in error)/sst)

def main():
    target=OUT/'conferencia_numerica_entradas_e_rodada_controlada.json';assert not target.exists()
    state=load(OUT/'estado_meta.json');draft=ROOT/state['copia_trabalho'];assert sha(draft)==state['sha256_copia_trabalho_atual']
    data_path=ROOT/'Scripts/data/PETR4_close com factor_2000-2020_com data.csv'
    text_path=ROOT/'Scripts/data/PETR4_close com factor_2000-2020.txt'
    data=list(csv.reader(data_path.read_text(encoding='utf-8-sig').splitlines(),delimiter=';'))
    dates=[r[0] for r in data];values=[float(r[1]) for r in data]
    actual=[float(s) for s in text_path.read_text(encoding='utf-8-sig').splitlines() if s.strip()]
    assert len(actual)==len(data)==5198 and len(set(dates))==5198
    assert dates==sorted(dates) and dates[0]=='2000-01-03' and dates[-1]=='2020-12-30'
    difference=max(abs(a-b) for a,b in zip(actual,values));assert difference<1e-12
    center=statistics.fmean(actual);m2=statistics.fmean((v-center)**2 for v in actual)
    desc=dict(media=center,desvio_padrao_amostral=statistics.stdev(actual),minimo=min(actual),maximo=max(actual),
              assimetria_momento=statistics.fmean((v-center)**3 for v in actual)/m2**1.5,
              curtose_excesso_momento=statistics.fmean((v-center)**4 for v in actual)/m2**2-3)
    assert [f'{v:.2f}' for v in desc.values()]==['13.28','7.11','2.48','34.55','0.22','-0.82']
    manifest=load(RUN/'execution_manifest.json');hashes=[]
    for f in [data_path,text_path]:
        relative=f.relative_to(ROOT).as_posix();assert sha(f)==manifest['hashes_sha256']['data'][relative]
        hashes.append(dict(arquivo=relative,sha256=sha(f),confere_manifesto=True))
    primary_files=[RUN/'predictions/previsoes_dm.csv',RUN/'metrics/metricas_teste_completo.csv',RUN/'metrics/metricas_janela_dm.csv']
    primary_files += [RUN/f'predictions/{name}_test_full.csv' for name in ['esn','gru','lstm']]
    for f in primary_files:
        relative=f.relative_to(RUN).as_posix();group=relative.split('/')[0]
        assert sha(f)==manifest['hashes_sha256'][group][relative]
        hashes.append(dict(arquivo=f.relative_to(ROOT).as_posix(),sha256=sha(f),confere_manifesto=True))
    common=rows(primary_files[0]);assert [r['data'] for r in common]==dates[3900:]
    assert max(abs(float(r['real'])-y) for r,y in zip(common,actual[3900:]))<1e-12
    summaries=[]
    for window,source_name in [('completa','metricas_teste_completo.csv'),('comum','metricas_janela_dm.csv')]:
        recorded={r['modelo']:r for r in rows(RUN/'metrics'/source_name)}
        for model in ['esn','gru','lstm']:
            full=rows(RUN/f'predictions/{model}_test_full.csv');assert [r['data'] for r in full]==dates[3899:]
            assert [r['origem_data'] for r in full]==dates[3898:-1]
            assert max(abs(float(r['real'])-y) for r,y in zip(full,actual[3899:]))<1e-12
            if window=='completa':real=[float(r['real']) for r in full];pred=[float(r['previsto']) for r in full]
            else:
                real=[float(r['real']) for r in common];pred=[float(r[model]) for r in common]
                assert max(abs(float(a['previsto'])-b) for a,b in zip(full[1:],pred))<1e-12
            assert all(math.isfinite(v) for v in real+pred)
            result=metrics(real,pred);r=recorded[model.upper()];assert len(real)==int(r['n'])
            assert r['inicio']==dates[3899 if window=='completa' else 3900] and r['fim']==dates[-1]
            delta={k:result[k]-float(r[k]) for k in result};assert max(map(abs,delta.values()))<1e-10
            summaries.append(dict(janela=window,modelo=model.upper(),n=len(real),inicio=r['inicio'],fim=r['fim'],calculado=result,diferenca_para_registro=delta))
    drive=[]
    for cached,original,dated in [('PETR4_drive.txt',text_path,False),('PETR4_drive_com_data.csv',data_path,True)]:
        f=ROOT/'reports/fontes_drive_20261029'/cached
        if dated:
            rr=list(csv.reader(f.read_text(encoding='utf-8-sig').splitlines(),delimiter=';'))
            assert [r[0] for r in rr]==dates;v=[float(r[1]) for r in rr];ref=values
        else:v=[float(x) for x in f.read_text(encoding='utf-8-sig').splitlines() if x.strip()];ref=actual
        assert len(v)==5198;maxdiff=max(abs(a-b) for a,b in zip(v,ref));assert maxdiff<1e-12
        drive.append(dict(arquivo=f.relative_to(ROOT).as_posix(),sha256=sha(f),identico_em_bytes=sha(f)==sha(original),n=len(v),maior_diferenca_numerica=maxdiff))
    scripts=[]
    for name in ['01_prepare_data.R','common_controlled.R']:
        p=RUN/'scripts'/name;expected=manifest['hashes_sha256']['scripts'][f'scripts/{name}'];assert sha(p)==expected
        q=ROOT/'Scripts/diebold_mariano'/name;scripts.append(dict(arquivo=p.relative_to(ROOT).as_posix(),sha256=sha(p),atual_identico_ao_arquivado=sha(q)==sha(p)))
    record=dict(base=state['base'],sha256_base=state['sha256_base'],sha256_rascunho=sha(draft),
      entradas=hashes,diferenca_maxima_csv_txt=difference,estatisticas=desc,estatisticas_confere_tabela2=True,
      datas=dict(n=5198,primeira=dates[0],ultima=dates[-1],unicas=True,crescentes=True),
      blocos=[dict(nome=k,inicio_indice=a+1,fim_indice=b,n=b-a,inicio=dates[a],fim=dates[b-1]) for k,a,b in [('treino',0,2600),('validacao',2600,3899),('teste',3899,5198)]],
      manifest=dict(arquivo=(RUN/'execution_manifest.json').relative_to(ROOT).as_posix(),sha256=sha(RUN/'execution_manifest.json'),seed_registrada=manifest['seed_base']),
      metricas_recalculadas=summaries,copias_drive=drive,scripts_de_preparacao=scripts,
      metodo='Leitura dos arquivos preservados e cálculo independente de estatísticas/erros com a biblioteca padrão Python. Nenhum modelo, GA, teste DM ou exportação original foi executado ou alterado.',
      limites='Não reconstrói ajuste corporativo, não transfere números entre a rodada controlada e as45execuções históricas e não prova que a cópia atual de cada script produziu toda execução histórica. Os testes de significância DM não foram recalculados. O hash de uma cópia diferente não é declarado idêntico apenas porque os valores numéricos coincidem.')
    target.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Entradas e Tabela2 conferidas; seis linhas de métricas(controlada completa/comum) compatíveis com os vetores preservados. Nenhum experimento executado.')

if __name__=='__main__':main()
