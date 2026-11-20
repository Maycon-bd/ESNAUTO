"""Reconciliação autor–ano do rascunho; não valida sustentação científica."""
from pathlib import Path
from docx import Document
from collections import defaultdict
import hashlib,json,re,unicodedata,argparse

ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'reports/monografia/trabalho/revisao_parecer_integridade.docx'
OUT=ROOT/'reports/correcao_parecer_integridade'
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--docx',default=str(DOC))
parser.add_argument('--saida',default=str(OUT/'cruzamento_referencias_rascunho.json'))
args=parser.parse_args()
DOC=Path(args.docx).resolve()
TARGET=Path(args.saida).resolve()
assert DOC.is_relative_to(ROOT) and TARGET.is_relative_to(OUT)
def norm(s):return ''.join(c for c in unicodedata.normalize('NFD',s.casefold()) if not unicodedata.combining(c))
year=r'(?:19|20)\d{2}[a-z]?'
d=Document(DOC)
refs=[]
for i,p in enumerate(d.paragraphs):
    if p.style.name!='Referencias':continue
    main=re.split(r'DOI:|Disponível em:|Acesso em:|Versão com errata',p.text,flags=re.I)[0]
    years=re.findall(r'(?<!\d)'+year+r'(?!\w)',main)
    assert years,p.text
    refs.append({'id':f'R{len(refs)+1:02d}','paragrafo_atual':i,'autor':p.text.split(',')[0],
                 'ano_bibliografico':years[-1],'texto':p.text})
assert len(refs)==50
names=sorted({r['autor'] for r in refs},key=len,reverse=True)
lead=r'\b(?P<autor>(?:'+'|'.join(map(re.escape,names))+r'))(?:\s+[A-Z]\.)?(?:\s+et al\.)?(?:\s*(?:;|,|e\b|&)\s*[A-ZÀ-Ü][A-Za-zÀ-ü-]+)*'
patterns=[re.compile(lead+r'\s*\((?P<anos>'+year+r'(?:\s*,\s*'+year+r')*)\)',re.I),
          re.compile(lead+r'\s*,\s*(?P<anos>'+year+r')',re.I)]
items=[(f'P_atual{i:04d}',p) for i,p in enumerate(d.paragraphs)]
seen=set()
for ti,t in enumerate(d.tables):
    for ri,row in enumerate(t.rows):
        for ci,c in enumerate(row.cells):
            if c._tc in seen:continue
            seen.add(c._tc)
            items.extend((f'T_atual{ti}/L{ri}/C{ci}/P{pi}',p) for pi,p in enumerate(c.paragraphs))
records=[]
used=set()
for loc,p in items:
    if p.style.name=='Referencias':continue
    for pattern in patterns:
        for m in pattern.finditer(p.text):
            for y in re.findall(year,m['anos']):
                matches=[r for r in refs if norm(r['autor'])==norm(m['autor']) and r['ano_bibliografico']==y.lower()]
                used.update(r['id'] for r in matches)
                records.append({'local':loc,'citacao':m[0],'ano':y,'referencias':[r['id'] for r in matches]})
report={'alvo':str(DOC),'sha256_alvo':hashlib.sha256(DOC.read_bytes()).hexdigest(),
        'sha256_script':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'metodo':'Padrões autor–ano narrativos/parentéticos, incluindo anos múltiplos separados por vírgula. Ano bibliográfico extraído antes do DOI/URL/nota de versão; não confundir ano do evento no título com ano da edição. Inspeção do inventário de 50 referências acompanha a heurística.',
        'limites':'Correspondência nominal não comprova apoio científico; formatos não reconhecidos e citações ausentes não são detectados universalmente. Índices são do rascunho atual.',
        'referencias':refs,'ocorrencias_reconhecidas':len(records),'registros':records,
        'sem_correspondencia':[r for r in records if not r['referencias']],
        'referencias_sem_chamada_reconhecida':[r for r in refs if r['id'] not in used]}
target=TARGET
target.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('Referências:',len(refs),'ocorrências:',len(records),'sem correspondência:',len(report['sem_correspondencia']),
      'referências sem chamada:',len(report['referencias_sem_chamada_reconhecida']))
for r in report['sem_correspondencia']:print(r)
for r in report['referencias_sem_chamada_reconhecida']:print(r['id'],r['texto'][:100])
