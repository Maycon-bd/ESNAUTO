"""Localiza evidências nos textos extraídos; leitura, sem executar experimentos."""
from pathlib import Path
import re,sys
sys.stdout.reconfigure(encoding='utf-8')
root=Path(__file__).resolve().parents[1]/'reports/auditoria_citacoes_integridade_20261028'
for spec in sys.argv[1:]:
    prefix,pattern=spec.split('::',1)
    for path in root.glob(prefix+'*.txt'):
        text=path.read_text(encoding='utf8').replace('\x00','')
        print('\nFONTE',path.name)
        count=0
        for page in re.split(r'(?=\[PÁGINA PDF \d+\])',text):
            matches=list(re.finditer(pattern,page,re.I))
            if not matches:continue
            print(page.split('\n')[0])
            intervals=[]
            for m in matches:
                a,b=max(0,m.start()-160),min(len(page),m.end()+360)
                if intervals and a<=intervals[-1][1]:intervals[-1]=(intervals[-1][0],max(b,intervals[-1][1]))
                else:intervals.append((a,b))
            for a,b in intervals[:3]:print(re.sub(r'\s+',' ',page[a:b]))
            count+=1
            if count>=7:break
