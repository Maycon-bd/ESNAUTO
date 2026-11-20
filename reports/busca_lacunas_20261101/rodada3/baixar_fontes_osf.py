from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import urllib.request

out=Path(__file__).resolve().parent
listing=json.loads((out/'OSF_rq82a_arquivos.json').read_text(encoding='utf-8'))
names={'cyber_event_binned_data.csv','Modified_01_mar_2017_malware_forecasting.Rmd','06.05.2018.Forecasting_CyberEvents_Bayesian_model.Rmd'}
items=[x for x in listing['data'] if x['attributes']['name'] in names]
assert len(items)==3
def download(item):
    name=item['attributes']['name'];url=item['links']['download']
    assert url.startswith('https://osf.io/download/')
    with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=40) as response:
        data=response.read()
    (out/name).write_bytes(data)
    return {'arquivo':name,'url':url,'id_osf':item['id'],'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data),
            'criado_em':item['attributes'].get('date_created'),'modificado_em':item['attributes'].get('date_modified'),
            'metodo':'Download de arquivo público para inspeção textual; código R não executado.'}
with ThreadPoolExecutor(max_workers=3) as pool:
    records=list(pool.map(download,items))
(out/'OSF_downloads_procedencia.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(records,ensure_ascii=False))
