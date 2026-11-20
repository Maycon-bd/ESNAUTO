"""Inventário somente leitura do acervo e ZIPs, inclusive objetos Git históricos.

Não executa código científico nem restaura arquivos do histórico.
"""
from pathlib import Path
import csv, hashlib, io, json, os, re, subprocess, zipfile
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'reports/rebusca_documental_20261029'
OUT.mkdir(exist_ok=True)
SKIP = {'.git', 'node_modules', '__pycache__', 'python-env', 'site-packages',
        'R-library', 'python_deps', '.venv', 'renv'}
inventory, archives, matches = [], [], []
rx = re.compile(r'GA_RUN_00(?:5[3-9]|6[0-7])|methodi[_ ]ordinatio|extrac[aã]o[_ ]completa', re.I)
TEXT = {'.csv', '.txt', '.md', '.json', '.R', '.py', '.bib', '.ris', '.sql'}

def inspect_zip(data, locator, depth=0):
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            entry = {'origem': locator, 'sha256': hashlib.sha256(data).hexdigest(),
                     'membros': [], 'ocorrencias': []}
            archives.append(entry)
            for item in z.infolist():
                if item.is_dir():
                    continue
                entry['membros'].append({'nome': item.filename, 'bytes': item.file_size})
                suffix = Path(item.filename).suffix
                if item.file_size > 80_000_000:
                    continue
                if suffix.lower() == '.zip' and depth < 2:
                    inspect_zip(z.read(item), locator + '::' + item.filename, depth + 1)
                elif suffix in TEXT or suffix.lower() in {'.csv','.txt','.md','.json','.r','.py','.bib','.ris','.sql'}:
                    raw = z.read(item)
                    text = raw.decode('utf-8-sig', errors='replace')
                    found = sorted(set(rx.findall(text)))
                    if found:
                        entry['ocorrencias'].append({'membro':item.filename,'termos':found})
    except (zipfile.BadZipFile, RuntimeError) as exc:
        archives.append({'origem':locator,'erro':str(exc)})

for base, dirs, names in os.walk(ROOT):
    dirs[:] = sorted(d for d in dirs if d not in SKIP)
    for name in sorted(names):
        p = Path(base) / name
        if OUT in p.parents:
            continue
        rel = p.relative_to(ROOT).as_posix()
        size = p.stat().st_size
        inventory.append({'arquivo':rel,'bytes':size})
        if p.suffix.lower() == '.zip' and size < 120_000_000:
            inspect_zip(p.read_bytes(), rel)
        elif p.suffix.lower() in {x.lower() for x in TEXT} and size < 12_000_000:
            text = p.read_text(encoding='utf-8-sig', errors='replace')
            lines = [{'linha':i,'texto':line[:1200]} for i,line in enumerate(text.splitlines(),1) if rx.search(line)]
            if lines:
                matches.append({'arquivo':rel,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'ocorrencias':lines})

raw = subprocess.check_output(['git','rev-list','--objects','--all'],cwd=ROOT).decode('utf-8',errors='replace')
git_candidates=[]
for line in raw.splitlines():
    oid, _, name = line.partition(' ')
    if Path(name).suffix.lower() in {'.zip','.xlsx','.xls','.csv','.bib','.ris','.pdf','.sql'}:
        git_candidates.append({'oid':oid,'arquivo':name})
        if name.lower().endswith('.zip'):
            data = subprocess.check_output(['git','cat-file','blob',oid],cwd=ROOT)
            inspect_zip(data,'git:'+oid+':'+name)

manifest={'data_utc':datetime.now(timezone.utc).isoformat(),
          'base':'v002','sha256_base':'d41a33359e19f974dfd48eb322cb2a3877ba3cbbac20c9db941a19985076a093',
          'exclusoes_de_diretorios':sorted(SKIP),'inventario':inventory,
          'ocorrencias_arquivos':matches,'objetos_git_candidatos':git_candidates,'arquivos_zip':archives,
          'limites':'Busca lexical e inventário; não certifica conteúdo integral nem recupera objetos Git não alcançáveis. ZIPs até 120 MB, membros até 80 MB, profundidade máxima 2.'}
(OUT/'inventario_e_busca.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'arquivos':len(inventory),'zips_inspecionados':len(archives),'ocorrencias_arquivos':len(matches),
                  'git_candidatos':git_candidates,'zips_com_ocorrencias':[{'origem':a['origem'],'ocorrencias':a.get('ocorrencias')} for a in archives if a.get('ocorrencias')],
                  'planilhas_acervo':[a for a in inventory if Path(a['arquivo']).suffix.lower() in {'.xlsx','.xls','.ris'}]},ensure_ascii=False,indent=2))
