"""Consulta metadados públicos de disponibilidade; não contorna acesso editorial."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError

OUT=Path(__file__).resolve().parent
targets={
 'Sharma_publicado':'10.1007/978-981-95-4109-6_25',
 'Gandhudi_apoio_D30':'10.1016/j.compeleceng.2024.109302',
}
def check(pair):
 name,doi=pair
 url='https://api.openalex.org/works/doi:'+doi
 record={'nome':name,'doi':doi,'url':url,'consultado_em_utc':datetime.now(timezone.utc).isoformat()}
 try:
  with urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=30) as response: raw=response.read()
  data=json.loads(raw)
  (OUT/(name+'_OpenAlex.json')).write_bytes(raw)
  record.update(sha256=hashlib.sha256(raw).hexdigest(),titulo=data.get('title'),acesso=data.get('open_access'),
   locais=[{k:x.get(k) for k in ['landing_page_url','pdf_url','is_oa','version']} for x in data.get('locations',[])])
 except (URLError,TimeoutError,ValueError) as exc:record['falha']=str(exc)
 return record
with ThreadPoolExecutor(max_workers=2) as pool:records=list(pool.map(check,targets.items()))
(OUT/'resultado_acesso.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(records,ensure_ascii=True))
