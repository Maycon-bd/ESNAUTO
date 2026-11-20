import hashlib
import json
from pathlib import Path
import urllib.request

folder = Path(__file__).resolve().parent / 'suplementos'
url = 'https://mdpi-res.com/d_attachment/electronics/electronics-14-01721/article_deploy/electronics-14-01721.pdf'
dest = folder / 'Pagliaro_2025.pdf'
if not dest.exists():
    request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(request, timeout=45) as response:
        data = response.read()
    assert data.startswith(b'%PDF-')
    dest.write_bytes(data)
metadata = {'url': url, 'arquivo': dest.name, 'sha256': hashlib.sha256(dest.read_bytes()).hexdigest(),
            'papel': 'Fonte de apoio citada como referência 10 por Vishwas; não amplia o portfólio.',
            'metodo': 'Download oficial para leitura; nenhuma experiência executada.'}
(folder / 'Pagliaro_procedencia.json').write_text(json.dumps(metadata, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps(metadata, ensure_ascii=False))
