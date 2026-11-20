from html.parser import HTMLParser
import hashlib
import json
from pathlib import Path
import urllib.request

out = Path(__file__).resolve().parent
parent = json.loads((out/'Gjika_RPubs_procedencia.json').read_text(encoding='utf-8'))
url = 'https:' + parent['frames'][0]
assert url == 'https://rstudio-pubs-static.s3.amazonaws.com/715261_74a3c81aea9c4220a19d61297463c15e.html'
with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'}), timeout=40) as response:
    data = response.read()
(out/'Gjika_documento.html').write_bytes(data)

class Visible(HTMLParser):
    def __init__(self):
        super().__init__()
        self.skip = 0
        self.parts = []
    def handle_starttag(self, tag, attrs):
        if tag in {'script','style'}:
            self.skip += 1
        if tag in {'p','pre','div','h1','h2','h3','li'} and not self.skip:
            self.parts.append('\n')
    def handle_endtag(self, tag):
        if tag in {'script','style'}:
            self.skip -= 1
    def handle_data(self, text):
        if not self.skip:
            self.parts.append(text)

parser = Visible()
parser.feed(data.decode('utf-8', errors='replace'))
text = ''.join(parser.parts)
(out/'Gjika_texto.txt').write_text(text,encoding='utf-8')
meta={'url':url,'origem':parent['url'], 'sha256_html':hashlib.sha256(data).hexdigest(),
      'sha256_texto':hashlib.sha256(text.encode('utf-8')).hexdigest(),
      'bytes_html':len(data),'caracteres_textuais':len(text),
      'metodo':'Somente leitura do documento público vinculado por iframe; script/estilo ignorados; nenhum R ou JavaScript executado.'}
(out/'Gjika_documento_procedencia.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(meta,ensure_ascii=False))
