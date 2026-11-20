"""Baixa apenas a página pública de origem do conjunto Cyber; não executa R/HTML."""
import hashlib
import json
from pathlib import Path
import re
import urllib.error
import urllib.request

out = Path(__file__).resolve().parent
url = 'https://rpubs.com/Eraldagjika/715261'
entry = {'url':url, 'metodo':'Leitura HTTP de página pública; nenhum código de terceiros executado.'}
try:
    request = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
    with urllib.request.urlopen(request, timeout=40) as response:
        data = response.read()
        entry['url_final'] = response.url
        entry['status_http'] = response.status
    (out/'Gjika_RPubs_pagina.html').write_bytes(data)
    entry['sha256'] = hashlib.sha256(data).hexdigest()
    html = data.decode('utf-8', errors='replace')
    entry['frames'] = re.findall(r'<iframe[^>]+src=[\"\x27]([^\"\x27]+)', html, flags=re.I)
except (urllib.error.URLError, TimeoutError) as exc:
    entry['falha'] = str(exc)
(out/'Gjika_RPubs_procedencia.json').write_text(json.dumps(entry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(entry,ensure_ascii=False))
