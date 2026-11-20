"""Primeiro lote: atribuições de Vishwas e metadados, sobre cópia da v005."""
import ast
import hashlib
import json
import re
from copy import deepcopy
from difflib import SequenceMatcher
from pathlib import Path
from zipfile import ZipFile
from lxml import etree

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reports/fechamento_integral_20261029'
DEST=ROOT/'reports/monografia/trabalho/fechamento_integral_20261029.docx'
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
W='{'+NS['w']+'}'
XMLSPACE='{http://www.w3.org/XML/1998/namespace}space'

source=ast.parse((ROOT/'Scripts/revisar_parecer_integridade_lote1.py').read_text(encoding='utf-8'))
for node in source.body:
    if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='ITALIC_PHRASES' for t in node.targets):
        exec(compile(ast.Module(body=[node],type_ignores=[]),'<lista de estrangeirismos>','exec'))
    if isinstance(node,ast.FunctionDef) and node.name in {'visible','replace_text','format_revised_prose'}:
        exec(compile(ast.Module(body=[node],type_ignores=[]),'<helper OOXML>','exec'))

def main():
    base=json.loads((OUT/'base_examinada.json').read_text(encoding='utf-8'))
    assert base['id']=='v005' and hashlib.sha256(DEST.read_bytes()).hexdigest()==base['sha256']
    with ZipFile(DEST) as z:infos=z.infolist();parts={i.filename:z.read(i.filename) for i in infos}
    before=dict(parts);root=etree.fromstring(parts['word/document.xml']);pars=root.xpath('//w:p',namespaces=NS)
    findings=json.loads((OUT/'achados_D30_vishwas.json').read_text(encoding='utf-8'))
    inv=json.loads((OUT/'inventario_unidades.json').read_text(encoding='utf-8'))
    lookup={x['id']:x for x in inv['unidades']};log=[]
    for item in findings['alteracoes_propostas']:
        u=lookup[item['unidade']];p=pars[u['indice_paragrafo_xml']]
        assert visible(p)==item['texto_anterior']
        replace_text(p,item['proposta']);format_revised_prose(p,u['indice_paragrafo_xml'])
        item['estado']='incorporado_em_copia_de_trabalho_pendente_conferencia_nativa'
        log.append({'unidade':u['id'],'antes':item['texto_anterior'],'depois':visible(p),'evidencia':'achados_D30_vishwas.json'})
    targets=[p for p in pars if visible(p).startswith('VISHWAS, H. N.; USHA, B. A.; SANGEETHA, K. N.')]
    assert len(targets)==1;p=targets[0];old=visible(p);assert 'v. 11, 2025.' in old
    replace_text(p,old.replace('v. 11, 2025.','v. 11, n. 4, p. 204-229, 2025.'))
    log.append({'elemento':'R46, referência Vishwas','antes':old,'depois':visible(p),'evidencia':'https://www.extrica.com/article/24861; metadados confirmados em achados_D30_vishwas.json'})
    parts['word/document.xml']=etree.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
    assert [x for x in parts if parts[x]!=before[x]]==['word/document.xml']
    temp=DEST.with_suffix('.tmp.docx')
    with ZipFile(temp,'w') as z:
        for info in infos:z.writestr(info,parts[info.filename])
    temp.replace(DEST)
    (OUT/'incorporacao_lote1.json').write_text(json.dumps({'base':base['id'],'sha256_base':base['sha256'],'copia_trabalho':str(DEST.relative_to(ROOT)),'sha256_apos_lote':hashlib.sha256(DEST.read_bytes()).hexdigest(),'alteracoes':log,'estado':'incorporado_pendente_validacao_final_e_registro','sem_resultados_experimentais_alterados':True},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (OUT/'achados_D30_vishwas.json').write_text(json.dumps(findings,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    state=json.loads((OUT/'estado_meta.json').read_text(encoding='utf-8'));state.update(correcoes_word_incorporadas_nesta_meta=4,copia_trabalho=str(DEST.relative_to(ROOT)),estado_copia='rascunho_nao_promovido_pendente_fechamento_integral');(OUT/'estado_meta.json').write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Incorporados três parágrafos e a referência R46 na cópia de trabalho; v005 preservada.')

if __name__=='__main__':main()
