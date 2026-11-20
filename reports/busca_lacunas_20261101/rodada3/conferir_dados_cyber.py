"""Aritmética descritiva de conferência; não ajusta modelos nem executa R."""
import csv
import hashlib
import json
from pathlib import Path
import statistics as st

out = Path(__file__).resolve().parent
path = out / 'cyber_event_binned_data.csv'
assert hashlib.sha256(path.read_bytes()).hexdigest() == '16b0ed9fdb4d9336eaa05f27332eae9cb1289754c7f899aa21f726c3490f1a0f'
rows = list(csv.DictReader(path.open(encoding='utf-8-sig')))
x = [float(row['avg.report.length']) for row in rows]

def summary(values):
    mean = st.mean(values)
    quartiles = st.quantiles(values, n=4, method='inclusive')
    variance = st.mean((v-mean)**2 for v in values)
    return {'n':len(values), 'mean':mean, 'Q1':quartiles[0], 'median':st.median(values), 'Q3':quartiles[2],
            'skew_moment':st.mean((v-mean)**3 for v in values)/variance**1.5,
            'kurtosis_pearson':st.mean((v-mean)**4 for v in values)/variance**2}

data = {'metodo':'Aritmética descritiva sobre CSV público, sem ajuste de modelos. Quartis inclusivos equivalentes ao tipo 7 de R. Momentos padronizados populacionais; não presumir a mesma definição de gamma3/gamma4 da publicação.',
        'limite':'Hipóteses de transformação não equivalem ao protocolo original de Abebe. Não atribuir exclusão de zeros ou divisão por 100 aos autores sem evidência adicional.',
        'csv_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
        'csv':summary(x), 'zeros':sum(v==0 for v in x),
        'positive_div100':summary([v/100 for v in x if v>0]),
        'rpubs_zero001':summary([0.01 if v==0 else v for v in x]),
        'tabela5_abebe':{'n':363, 'mean':5.3810, 'Q1':3.9850, 'median':5.1000, 'Q3':6.5450, 'skew':0.7249, 'kurtosis':3.6930}}
assert len(x)==366 and data['zeros']==3
candidate = data['positive_div100']
assert candidate['n']==363
assert all(abs(candidate[k]-data['tabela5_abebe'][k])<1e-12 for k in ['Q1','median','Q3'])
assert round(candidate['mean'],4) != data['tabela5_abebe']['mean']
(out/'conferencia_descritiva_cyber.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'n_original':len(x),'zeros':data['zeros'],'n_hipotese':candidate['n'],'quartis_coincidem':True,'media_4_casas_nao_coincide':True,'protocolo_original_comprovado':False},ensure_ascii=False))
