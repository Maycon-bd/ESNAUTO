import hashlib,json,re,zipfile
from pathlib import Path
from lxml import etree as E

ROOT=Path(__file__).resolve().parents[3]
BUILD=Path(__file__).resolve().parent
OUT=BUILD.parent/'entrega'; OUT.mkdir(parents=True,exist_ok=True)
OLD='0daacd3ea1753bca97619df025923b92a44a047b5c1252a4677f802dfe870dad'
BASE=ROOT/'reports/monografia/versoes/v010/MayconGarciaSilva_monografia_v010.docx'
SHA=hashlib.sha256(BASE.read_bytes()).hexdigest()
assert SHA=='1da5ea82344c177d75af723362017e3e558bbb127bd9995f7ec0cbd6964f81ed'
DECK=ROOT/'reports/apresentacao_banca_v008_visual/entrega/Apresentacao_ESNAUTO_banca_visual.pptx'
DOC=ROOT/'reports/apresentacao_banca_v008/entrega/Roteiro_video_ESNAUTO_25min_v008.docx'
MD=DOC.with_suffix('.md')
data=json.loads((ROOT/'reports/apresentacao_banca_v008_visual/build/conteudo.json').read_text(encoding='utf-8'))
sources=[
'capa e resumo',
'Introdução, p. 17–19',
'Introdução, H1–H5, p. 17–19',
'cap. 2, p. 20–40, e seção 3.8.3, p. 51–53. Jaeger (2007), Araújo et al. (2025), Cardoso et al. (2022b), Lampugnani (2026)',
'seção 3.2, p. 42–43',
'seção 3.3, p. 44–45. Jaeger (2007)',
'seção 3.4, p. 46–47, e Quadro 3, p. 45',
'Quadro 2 e seção 3.3, p. 44–45',
'seções 3.6–3.8, p. 47–53, e 4.2, p. 55–57; procedencia.json do lote ilustrativo',
'seções 3.1, p. 41–42, e 4.10, p. 65–66; Quadro 6, p. 72',
'seção 3.6, p. 47–49, e Tabela 5, p. 60',
'resumo e Tabela 3, p. 55; registro_GA_RUN_0030.csv',
'Tabela 4, p. 58, resumo e seção 5.1, p. 67–68',
'Figura 6 e seção 4.2, p. 55–57; reports/revisao_orientador_petr4/procedencia.json',
'seção 3.7, p. 49–50; execution_manifest.json e previsoes_dm.csv do PETR4-DM',
'seção 4.8, p. 62–63; resultados_dm.csv e previsoes_dm.csv do PETR4-DM',
'seção 3.7, p. 49–50, e Tabela 6, p. 63; resultados_dm.csv. Diebold e Mariano (1995)',
'Tabela 5 e seção 4.6, p. 60–61',
'Quadro 5, p. 63, e Conclusão, p. 70–72',
'seção 4.10, p. 65–66, Quadro 6, p. 72, e Conclusão, p. 70–72',
'seções 3.8, p. 50–53, e 5.1–5.2, p. 67–69; Conclusão, p. 70–72',
'seção 5.3, p. 69; persistência e ablações também discutidas nas seções 5.1–5.2, p. 67–69',
'Conclusão, p. 70–72'
]
plain=json.loads((ROOT/'reports/apresentacao_banca_v008/build/conteudo.json').read_text(encoding='utf-8'))
mapping={}
new_sources=[]
for d,p,s in zip(data,plain,sources):
    suffix=d['source'][len(p['source']):] if d['source'].startswith(p['source']) else ''
    new='Monografia v010, '+s+suffix
    mapping[d['source']]=new; mapping[p['source']]=new
    new_sources.append(new)
def change(t):
    for old in sorted(mapping,key=len,reverse=True): t=t.replace(old,mapping[old])
    return t.replace('v008','v010').replace(OLD,SHA).replace('A tabela mostra os valores documentados','Os gráficos mostram os valores documentados')
def patch_package(src,dest,predicate):
    changed=[]
    with zipfile.ZipFile(src) as zin,zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            b=zin.read(info.filename)
            if predicate(info.filename):
                # Text-only substitution preserves all existing XML geometry and relationships.
                s=b.decode('utf-8'); new=change(s)
                if new!=s: changed.append(info.filename); b=new.encode('utf-8')
            zout.writestr(info,b)
    return changed
changed_ppt=patch_package(DECK,BUILD/'candidate.pptx',lambda n:bool(re.fullmatch(r'ppt/(?:slides/slide|notesSlides/notesSlide)\d+\.xml',n)))
changed_doc=patch_package(DOC,OUT/'Roteiro_video_ESNAUTO_25min_v010.docx',lambda n:n=='word/document.xml')
md=change(MD.read_text(encoding='utf-8'))
(OUT/'Roteiro_video_ESNAUTO_25min_v010.md').write_text(md,encoding='utf-8')
for d,s in zip(data,new_sources): d['source']=s
(BUILD/'conteudo.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
assert len(data)==23 and sum(d['seconds'] for d in data)==1500
with zipfile.ZipFile(DECK) as a, zipfile.ZipFile(BUILD/'candidate.pptx') as b:
    assert a.namelist()==b.namelist()
    for n in a.namelist():
        if n not in changed_ppt: assert a.read(n)==b.read(n),n
    charts=[n for n in a.namelist() if re.search(r'/charts/chart\d+\.xml$',n)]
    assert len(charts)==10
    ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
    for i,d in enumerate(data,1):
        notes=E.fromstring(b.read(f'ppt/notesSlides/notesSlide{i}.xml'))
        text=''.join(notes.xpath('//a:t/text()',namespaces=ns))
        assert d['speech'] in text,(i,'speech changed')
        assert d['source'] in text,(i,'source missing')
        assert SHA in text and 'v008' not in text
with zipfile.ZipFile(DOC) as a,zipfile.ZipFile(OUT/'Roteiro_video_ESNAUTO_25min_v010.docx') as b:
    ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    pa=E.fromstring(a.read('word/document.xml')).xpath('//w:p',namespaces=ns)
    pb=E.fromstring(b.read('word/document.xml')).xpath('//w:p',namespaces=ns)
    assert len(pa)==len(pb)
    for x,y in zip(pa,pb):
        ta=''.join(x.xpath('.//w:t/text()',namespaces=ns));tb=''.join(y.xpath('.//w:t/text()',namespaces=ns))
        assert change(ta)==tb
    tx='\n'.join(''.join(p.xpath('.//w:t/text()',namespaces=ns)) for p in pb)
    for d in data:
        assert d['speech'] in md
        assert d['source'] in tx
    assert 'v008' not in tx and not re.search(r'P0\d{3}',tx)
receipt={'base':'v010','base_sha256':SHA,'base_arquivo':str(BASE),'slides':23,'segundos_planejados':1500,
    'palavras_fala':sum(d['words'] for d in data),'fala_preservada':True,'graficos_preservados':10,
    'partes_pptx_alteradas':changed_ppt,'partes_docx_alteradas':changed_doc,
    'fontes_originais':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [DECK,DOC,MD]},
    'escopo':'Atualização de base e localizadores de consulta; falas das notas visuais preservadas. No roteiro, única mudança de fala: A tabela mostra → Os gráficos mostram (slide 12), sincronizando com o visual já existente. Dados e resultados preservados. Fontes dos slides 9/14 corrigidas para seção 4.2.'}
(BUILD/'rastreabilidade.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(receipt,ensure_ascii=True,indent=2))
