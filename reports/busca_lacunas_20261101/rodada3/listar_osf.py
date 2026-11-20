import hashlib
import json
from pathlib import Path
import urllib.request
import urllib.error

out=Path(__file__).resolve().parent
attempts=[]
data=None
for url in ['https://api.osf.io/v2/nodes/aj7vr/files/osfstorage/', 'https://api.osf.io/v2/files/aj7vr/']:
    try:
        with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=40) as response:
            data=response.read()
        attempts.append({'url':url,'http':200})
        break
    except urllib.error.HTTPError as exc:
        attempts.append({'url':url,'http':exc.code})
        if exc.code != 404:
            break
    except urllib.error.URLError as exc:
        attempts.append({'url':url,'falha':str(exc)})
        break
if data is None:
    (out/'OSF_aj7vr_procedencia.json').write_text(json.dumps({'tentativas':attempts,'arquivo_recuperado':False},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'tentativas':attempts,'arquivo_recuperado':False}))
    raise SystemExit(0)
(out/'OSF_aj7vr_arquivos.json').write_bytes(data)
j=json.loads(data)
items=j.get('data',[])
if isinstance(items,dict):
    items=[items]
summary={'url':url,'sha256':hashlib.sha256(data).hexdigest(),'tentativas':attempts,
         'arquivos':[{'id':x['id'],'nome':x['attributes'].get('name'),'kind':x['attributes'].get('kind'),'links':x.get('links',{}),'relationships':x.get('relationships',{})} for x in items],
         'proxima_pagina':j.get('links',{}).get('next')}
(out/'OSF_aj7vr_procedencia.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False))
