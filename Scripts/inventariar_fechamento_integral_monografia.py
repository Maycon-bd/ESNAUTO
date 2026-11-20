"""Inventário verificável de cobertura; não aprova afirmações automaticamente."""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from zipfile import ZipFile
from lxml import etree
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reports/fechamento_integral_20261029'
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'm':'http://schemas.openxmlformats.org/officeDocument/2006/math'}

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,value):
    (OUT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
    r=subprocess.run([sys.executable,'-X','utf8',str(ROOT/'Scripts/versao_monografia.py'),'atual','--json'],cwd=ROOT,capture_output=True,text=True,encoding='utf-8',check=True)
    base=json.loads(r.stdout);doc=ROOT/base['arquivo'];assert sha(doc)==base['sha256']
    OUT.mkdir(exist_ok=True)
    assert not (OUT/'inventario_unidades.json').exists(), 'Inventário já existe; não apagar decisões humanas por reexecução.'
    save('base_examinada.json',base)
    units=[];parts=[]
    with ZipFile(doc) as z:
        for name in z.namelist():
            if not name.startswith('word/') or not name.endswith('.xml'):continue
            if not re.search(r'/(?:document|footnotes|endnotes|comments|header\d*|footer\d*)\.xml$',name):continue
            root=etree.fromstring(z.read(name));pars=root.xpath('//w:p',namespaces=NS);tree=root.getroottree();nonempty=0
            for pi,p in enumerate(pars):
                ts=p.xpath('.//w:t|.//m:t',namespaces=NS)
                # O parágrafo externo de uma caixa pode conter parágrafos internos.
                # Cada nó textual pertence só a seu ancestral w:p mais próximo.
                ts=[t for t in ts if next(a for a in t.iterancestors() if a.tag=='{'+NS['w']+'}p') is p]
                text=''.join(t.text or '' for t in ts)
                if not text.strip():continue
                style=p.xpath('./w:pPr/w:pStyle/@w:val',namespaces=NS)
                units.append({'id':f'U{len(units)+1:04d}','parte':name,'indice_paragrafo_xml':pi,'xpath':tree.getpath(p),'estilo':style[0] if style else None,'texto':text,'sha256_texto':hashlib.sha256(text.encode()).hexdigest(),'anos_detectados':re.findall(r'\b(?:19|20)\d{2}[a-z]?\b',text),'formulas_ooxml':len(p.xpath('.//m:oMath',namespaces=NS)),'status_conteudo':'nao_examinada_nesta_meta','afirmacoes':[],'limite_inventario':'Unidade textual, não decisão sobre número de afirmações ou correção da citação.'})
                nonempty+=1
            parts.append({'parte':name,'paragrafos_xml':len(pars),'paragrafos_com_texto':nonempty})
    save('inventario_unidades.json',{'base':base['id'],'sha256_base':base['sha256'],'partes':parts,'n_unidades':len(units),'unidades':units})
    cross=json.loads((ROOT/'reports/correcao_parecer_integridade/cruzamento_revisao_43_celulas_20261029.json').read_text(encoding='utf-8'))
    assert cross['sha256_alvo']==base['sha256']
    save('inventario_referencias.json',{'base':base['id'],'sha256_base':base['sha256'],'referencias':[{**x,'status_conferencia_integral':'nao_examinada_nesta_meta','fontes_primarias':[],'diagnosticos_por_afirmacao':[]} for x in cross['referencias']],'ocorrencias_nominais_historicas':cross['registros'],'limite':'As 151 correspondências nominais não comprovam fidelidade e não encerram o inventário de citações. Conferir formatos não reconhecidos, atribuições sem citação e conteúdo de tabelas/notas.'})
    sources=[];target=OUT/'fontes_extraidas';target.mkdir(exist_ok=True)
    for i,p in enumerate(sorted((ROOT/'Artigos citados').glob('*.pdf'),key=lambda p:p.name.casefold()),1):
        reader=PdfReader(p);pages=[{'pagina_pdf':j+1,'texto':pg.extract_text() or ''} for j,pg in enumerate(reader.pages)]
        sid=f'D{i:02}';(target/(sid+'_paginas.json')).write_text(json.dumps(pages,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        sources.append({'id':sid,'arquivo':str(p.relative_to(ROOT)),'sha256':sha(p),'paginas':len(pages),'caracteres_extraidos':sum(len(pg['texto']) for pg in pages),'estado_leitura':'extraido_para_localizacao_nao_equivale_a_leitura','log_leitura':[]})
    for sid,p in [('SUP_CARDOSO_TESE',ROOT/'reports/tese_Fabian_Correa_Cardoso.pdf'),('SUP_CARDOSO_RBRAS',ROOT/'reports/fontes_drive_20261029/Cardoso_RBras_2022_completo.pdf')]:
        if not p.exists():continue
        reader=PdfReader(p);pages=[{'pagina_pdf':j+1,'texto':pg.extract_text() or ''} for j,pg in enumerate(reader.pages)]
        (target/(sid+'_paginas.json')).write_text(json.dumps(pages,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        sources.append({'id':sid,'arquivo':str(p.relative_to(ROOT)),'sha256':sha(p),'paginas':len(pages),'estado_leitura':'nao_examinado_nesta_meta','log_leitura':[]})
    guide=Path('C:/Users/User/Downloads/GUIA_Padronizacao_Monografia_FASOFT_UniRV (1).pdf')
    if guide.exists():
        reader=PdfReader(guide);pages=[{'pagina_pdf':j+1,'texto':pg.extract_text() or ''} for j,pg in enumerate(reader.pages)]
        (target/'GUIA_paginas.json').write_text(json.dumps(pages,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        save('guia_identificado.json',{'arquivo':str(guide),'sha256':sha(guide),'paginas':len(pages),'estado':'extraido_nao_revalidado_nesta_meta'})
    save('manifesto_fontes.json',sources)
    save('estado_meta.json',{'objetivo':'Fechamento integral de conteúdo antes da correção de português','base':base['id'],'sha256_base':base['sha256'],'estado':'em_andamento','unidades_inventariadas':len(units),'referencias_inventariadas':len(cross['referencias']),'obras_pdf_locais':len(sources),'unidades_aprovadas_automaticamente':0,'criterio_conclusao':'Todas as unidades inventariadas classificadas e suas afirmações conferidas ou corrigidas/delimitadas com evidência; nenhuma correção substantiva conhecida pendente; cobertura explicitada, Guia revalidado e versão final registrada/renderizada/inspecionada. Limites de evidência não são certificação universal.','onda5':'Limitação aceita e documentada pelo autor; não solicitar reenvio nem repetir experimentos.','leituras_anteriores':'Evidências históricas podem ser reutilizadas somente com identidade de fonte/trecho conferida e alcance preservado.'})
    print(json.dumps({'base':base['id'],'unidades':len(units),'referencias':len(cross['referencias']),'pdfs':len(sources),'partes':parts},ensure_ascii=False))

if __name__=='__main__':main()
