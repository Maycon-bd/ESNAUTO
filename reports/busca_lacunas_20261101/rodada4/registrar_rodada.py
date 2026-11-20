"""Registra auditoria documental; não edita Word nem executa fontes de terceiros."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import tarfile
from collections import Counter
from xml.etree import ElementTree as ET
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
TASK = OUT.parent
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def save(name, value):
    (OUT/name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

registry = json.loads((ROOT/'docs/assistencia_monografia/versao_vigente.json').read_text(encoding='utf-8'))
# A seleção é conferida novamente pelo CLI antes da entrega. Aqui a identidade
# examinada é explícita e não é escolhida por nome/data de outros arquivos.
word = ROOT/'reports/monografia/versoes/v010/MayconGarciaSilva_monografia_v010.docx'
expected = '1da5ea82344c177d75af723362017e3e558bbb127bd9995f7ec0cbd6964f81ed'
assert sha(word) == expected
ns = {'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
with ZipFile(word) as archive:
    body = ET.fromstring(archive.read('word/document.xml')).find('w:body',ns)
    tables = body.findall('w:tbl', ns)
    candidates=[]
    for table in tables:
        rows=[]
        for row in table.findall('w:tr',ns):
            rows.append([''.join(n.text or '' for n in cell.findall('.//w:t',ns)) for cell in row.findall('w:tc',ns)])
        if len(rows)==35 and all(len(row)==6 for row in rows): candidates.append(rows)
    assert len(candidates)==1
    matrix=candidates[0]
    counts=Counter(c for row in matrix[1:] for c in row[1:])
    assert counts['?']==38 and sum(counts.values())==170

inventories=[]
for stem in ['2508.05416v1','2512.08963v1']:
    path=OUT/(stem+'_fonte.bin')
    with tarfile.open(path) as archive:
        members=[{'nome':m.name,'bytes':m.size,'arquivo':m.isfile()} for m in archive.getmembers()]
    inventories.append({'id':stem,'arquivo':str(path.relative_to(ROOT)), 'sha256':sha(path),'membros':members})
save('inventario_arquivos_arxiv.json',inventories)

decisions=[
 {'id':'D23','dimensao':'P1','codigo':'?',
  'fonte_nova':'2508.05416v1/samplepaper.tex',
  'localizadores':'linhas 217–246; 275–284 (comentários); 328–343; 564',
  'evidencia':'O método identifica ReservoirPy sem versão. A distribuição da tabela governa hiperparâmetros; o Gaussiano é ruído. A menção a inicializadores padrão está em comentário TeX excluído do texto publicado e trata do estado inicial, sem individualizar lei efetiva de Win/W.',
  'limite':'Não inferir pesos de padrões da biblioteca ou de comentários de rascunho. O capítulo Springer posterior foi localizado, mas o corpo não estava acessível na prévia.'},
 {'id':'D23','dimensao':'P4','codigo':'?',
  'fonte_nova':'2508.05416v1/samplepaper.tex',
  'localizadores':'linhas 139–155; 698–703; 774–784; 1000–1038',
  'evidencia':'A revisão menciona LSTM e Transformer qualitativamente. Baselines e resultados próprios individualizam Last Value e XGBoost, sem comparação numérica qualificadora com LSTM/GRU/Transformer.',
  'limite':'Não transportar resultados de Alessandretti ou Kenny só pela citação. Nenhum código de experimento consta do inventário de membros do pacote editorial consultado. Isso não prova inexistência de código externo.'},
 {'id':'D13','dimensao':'P4','codigo':'?',
  'fonte_nova':'2512.08963v1/revised_main_mod.tex',
  'localizadores':'linhas 392–410; 466–482; 591; inventário completo de membros',
  'evidencia':'As duas tabelas confrontam Conventional ESN, AEESN, DeepESN, BrESN e três topologias CESN; DeepESN não equivale a LSTM. A declaração de dados remete ao artigo. O pacote inclui texto, bibliografia, classes e imagens, sem scripts de experimentos identificados no inventário.',
  'limite':'Versão de autor identificada por título/autores/DOI, sem alegação de identidade byte a byte com a edição publicada local. Leitura dirigida do fonte, somada à leitura anterior do PDF; não nova leitura integral de 71 mil caracteres.'},
 {'id':'D08','dimensao':'P1','codigo':'?',
  'fonte_nova':'DTU Orbit e conteúdo público do site do autor Zhihua Deng',
  'localizadores':'DTU: Access to Document; assets/js/content.js: entrada DOI 10.1109/TTE.2021.3111906; PDF local método seção 3',
  'evidencia':'DTU disponibiliza manuscrito aceito; a entrada exata no site do autor vincula o DOI, sem repositório ou suplemento na entrada. O método local diferencia as conexões aleatórias do reservatório dos pesos aleatórios do autoencoder, sem lei probabilística qualificadora recuperada.',
  'limite':'Inspeção da entrada e dos URLs textuais do perfil; não execução do JavaScript. Buscas negativas são limitadas aos canais consultados, sem prova universal de ausência.'}
]
save('decisoes.json',decisions)
original=json.loads((TASK/'decisoes_41_em_consolidacao.json').read_text(encoding='utf-8'))
remaining=[]
for row in original['decisoes']:
    if row['proposta']!='?':continue
    rowword=matrix[row['linha_word']]
    assert rowword[int(row['dimensao'][1:])]=='?'
    pdf=ROOT/row['pdf']
    assert sha(pdf)==row['sha256_pdf']
    remaining.append({k:row[k] for k in ['id','linha_word','autor','dimensao','pdf','sha256_pdf','localizador','sintese']})
assert len(remaining)==38
save('pendencias38_conferidas.json',{'base':'v010','sha256_base':expected,'celulas':remaining,
    'alcance':'Inventário conciliado com Word e hashes dos PDFs; não representa nova leitura integral das 38 células nesta rodada.'})
evidence={
 'registrado_em_utc':datetime.now(timezone.utc).isoformat(),
 'base':'v010','arquivo':str(word.relative_to(ROOT)),'sha256_base':expected,
 'word_editado':False,'busca_integral_concluida':False,
 'celulas_ampliadas':len(decisions),'fontes_ampliadas':3,
 'insuficiencias_word':counts['?'],
 'canais_oficiais':[
  {'url':'https://arxiv.org/abs/2508.05416','resultado':'Histórico consultado: v1. Fonte editorial arquivada; leitura dirigida, sem compilação.'},
  {'url':'https://arxiv.org/abs/2512.08963','resultado':'Título/autores/DOI relacionados à publicação EPJ Plus conferidos; v1 consultada.'},
  {'url':'https://www.dfki.de/en/web/research/projects-and-publications/publication/17053','resultado':'Registro institucional identifica ICONIP, pp.365–380 e remete ao mesmo arXiv; não oferece ali um segundo texto integral.'},
  {'url':'https://link.springer.com/chapter/10.1007/978-981-95-4109-6_25','resultado':'Capítulo publicado localizado: online17/11/2025, pp365–380. Acesso apenas à prévia; resumo tem diferença de redação. Corpo não lido e não presumido idêntico à preprint.'},
  {'url':'https://orbit.dtu.dk/en/publications/degradation-prediction-of-pemfcs-using-stacked-echo-state-network/','resultado':'Metadados e acesso ao manuscrito aceito conferidos; nenhum link de código qualificador na ficha consultada.'},
  {'url':'https://api.github.com/repos/DZH001-energy/DZH001-energy.github.io/contents/assets/js/content.js','resultado':'Conteúdo obtido pelo conector GitHub e arquivado; entrada da publicação e URLs inspecionados. Nenhum JavaScript executado.'}
 ],
 'execucoes':'Somente leitura/arquivamento, inventário e conferência estrutural. Nenhum treino, GA, DM, R, notebook ou compilação TeX de terceiros.'
}
save('evidencias.json',evidence)
files=[p for p in OUT.iterdir() if p.is_file() and p.name!='manifesto_entrega.json']
save('manifesto_entrega.json',{'base':'v010','sha256_base':expected,'arquivos':[{'arquivo':str(p.relative_to(ROOT)),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(files)]})
print(json.dumps({'base':'v010','sha256':expected,'celulas_ampliadas':4,'permanecem':38,'word_editado':False}))
