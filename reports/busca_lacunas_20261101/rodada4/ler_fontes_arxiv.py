"""Arquiva fonte editorial pública e lê membros textuais em memória; nunca compila/executa."""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import io
import json
from pathlib import Path
import re
import tarfile
import urllib.error
import urllib.request

out=Path(__file__).resolve().parent
targets=['2508.05416v1','2512.08963v1']
def read(ident):
    url='https://arxiv.org/src/'+ident
    rec={'id':ident,'url':url,'metodo':'Leitura de fonte editorial pública; nenhuma compilação ou código executado.'}
    try:
        with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=45) as response:
            data=response.read()
        (out/(ident+'_fonte.bin')).write_bytes(data)
        rec['sha256']=hashlib.sha256(data).hexdigest();rec['bytes']=len(data)
        texts=[]
        try:
            with tarfile.open(fileobj=io.BytesIO(data),mode='r:*') as archive:
                for member in archive.getmembers():
                    if not member.isfile() or not member.name.lower().endswith(('.tex','.bib','.txt','.py','.m','.r','.ipynb')):
                        continue
                    if member.size>2_000_000:
                        continue
                    raw=archive.extractfile(member).read()
                    text=raw.decode('utf-8',errors='replace')
                    texts.append({'membro':member.name,'sha256':hashlib.sha256(raw).hexdigest(),'texto':text})
        except tarfile.ReadError:
            rec['formato_tar']=False
        rec['membros_textuais']=[{'membro':x['membro'],'sha256':x['sha256'],'caracteres':len(x['texto'])} for x in texts]
        (out/(ident+'_textos.json')).write_text(json.dumps(texts,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        hits=[]
        for item in texts:
            for match in re.finditer(r'github|gitlab|code.{0,30}availab|supplement|LSTM|GRU|Transformer',item['texto'],re.I):
                hits.append({'membro':item['membro'],'trecho':item['texto'][max(0,match.start()-100):match.end()+220]})
        (out/(ident+'_localizadores.json')).write_text(json.dumps(hits,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        rec['ocorrencias_localizadas']=len(hits)
    except (urllib.error.URLError,TimeoutError) as exc:
        rec['falha']=str(exc)
    return rec
with ThreadPoolExecutor(max_workers=2) as pool:
    records=list(pool.map(read,targets))
(out/'arxiv_procedencia.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(records,ensure_ascii=False))
