from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import urllib.request

out=Path(__file__).resolve().parent
requests=[('OSF_rq82a_node.json','https://api.osf.io/v2/nodes/rq82a/'),
          ('OSF_rq82a_arquivos.json','https://api.osf.io/v2/nodes/rq82a/files/osfstorage/')]
def read(item):
    name,url=item
    with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=40) as response:
        data=response.read()
    (out/name).write_bytes(data)
    return name,url,data
records=[]
with ThreadPoolExecutor(max_workers=2) as pool:
    for name,url,data in pool.map(read,requests):
        j=json.loads(data);record={'url':url,'arquivo':name,'sha256':hashlib.sha256(data).hexdigest()}
        if isinstance(j['data'],dict):
            record['titulo']=j['data']['attributes'].get('title')
            record['descricao']=j['data']['attributes'].get('description')
        else:
            record['itens']=[{'id':x['id'],'nome':x['attributes']['name'],'kind':x['attributes']['kind'],
                              'download':x.get('links',{}).get('download'),
                              'files':x.get('relationships',{}).get('files',{}).get('links',{}).get('related')} for x in j['data']]
            record['next']=j.get('links',{}).get('next')
        records.append(record)
(out/'OSF_rq82a_procedencia.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(records,ensure_ascii=False))
