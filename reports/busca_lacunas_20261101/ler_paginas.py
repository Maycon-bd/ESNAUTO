import argparse, json, pathlib, sys
sys.stdout.reconfigure(encoding='utf-8')
p=argparse.ArgumentParser()
p.add_argument('id')
p.add_argument('paginas', help='1-3,5 or all')
p.add_argument('--busca')
a=p.parse_args()
root=pathlib.Path(__file__).resolve().parents[2]
pages=json.loads((pathlib.Path(__file__).resolve().parent/f'fontes_extraidas/{a.id}_paginas.json').read_text(encoding='utf-8'))
selected=set()
for part in a.paginas.split(','):
    if part=='all': selected.update(d['pagina_pdf'] for d in pages)
    elif '-' in part:
        lo,hi=map(int,part.split('-')); selected.update(range(lo,hi+1))
    else: selected.add(int(part))
import re
for d in pages:
    if d['pagina_pdf'] not in selected: continue
    txt=d['texto']
    if a.busca:
        matches=list(re.finditer(a.busca,txt,re.I))
        if not matches: continue
        spans=[]
        for m in matches:
            lo=max(0,m.start()-400); hi=min(len(txt),m.end()+650)
            if spans and lo<=spans[-1][1]: spans[-1][1]=max(hi,spans[-1][1])
            else: spans.append([lo,hi])
        txt='\n[…]\n'.join(txt[lo:hi] for lo,hi in spans)
    print(f'\n===== {a.id} PDF {d["pagina_pdf"]} =====\n{txt}')
