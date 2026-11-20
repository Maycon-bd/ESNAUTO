"""Aplica duas decisões bibliográficas e suas contagens em cópia da v004."""
import ast
import hashlib
import json
from difflib import SequenceMatcher
from pathlib import Path
from zipfile import ZipFile
from lxml import etree

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reports/revisao_43_celulas_20261029'
DEST=ROOT/'reports/monografia/trabalho/revisao_43_celulas_20261029.docx'
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
W='{'+NS['w']+'}'
XMLSPACE='{http://www.w3.org/XML/1998/namespace}space'
source=ast.parse((ROOT/'Scripts/revisar_parecer_integridade_lote1.py').read_text(encoding='utf-8'))
for node in source.body:
    if isinstance(node,ast.FunctionDef) and node.name in {'visible','replace_text'}:
        exec(compile(ast.Module(body=[node],type_ignores=[]),'<helper OOXML>','exec'))

def main():
    expected='110b1d19223e23f9e4b27e4c2b0ba74e92072ebcc3f1cd4ec4f0200bba059f5b'
    assert hashlib.sha256(DEST.read_bytes()).hexdigest()==expected
    with ZipFile(DEST) as z:infos=z.infolist();parts={x.filename:z.read(x.filename) for x in infos}
    before=dict(parts)
    root=etree.fromstring(parts['word/document.xml']);body=root.find(W+'body')
    ps=body.findall(W+'p');tables=body.findall(W+'tbl');log=[]
    def change(p,new,where):
        old=visible(p);assert old!=new;replace_text(p,new)
        log.append({'elemento':where,'antes':old,'depois':new})
    cell=tables[1].findall(W+'tr')[2].findall(W+'tc')[1].find(W+'p')
    assert visible(cell)=='10 D; 4 S; 5 ?; 15 —'
    change(cell,'11 D; 5 S; 3 ?; 15 —','Tabela 1, P2, contagens')
    for ri,label,new in [(14,'Hassaan','S'),(17,'Liu B.','D')]:
        cells=tables[2].findall(W+'tr')[ri].findall(W+'tc')
        assert label in ''.join(cells[0].xpath('.//w:t/text()',namespaces=NS))
        p=cells[2].find(W+'p');assert visible(p)=='?'
        change(p,new,f'Quadro 1, linha {ri}, P2')
    old=visible(ps[276]);fragment='comparações com LSTM, GRU ou Transformer e seleção de hiperparâmetros aparecem diretamente em dez documentos cada.'
    assert fragment in old
    change(ps[276],old.replace(fragment,'comparações com LSTM, GRU ou Transformer aparecem diretamente em dez documentos, e a seleção de hiperparâmetros, em onze.'),'Parágrafo explicativo da Figura 1')
    rid=ps[273].xpath('.//*[local-name()="blip"]/@*[local-name()="embed"]')[0]
    rels=etree.fromstring(parts['word/_rels/document.xml.rels'])
    media='word/'+next(x.get('Target') for x in rels if x.get('Id')==rid)
    parts[media]=(OUT/'figura1_recodificada.png').read_bytes()
    log.append({'elemento':'Figura 1','parte':media,'antes_sha256':hashlib.sha256(before[media]).hexdigest(),'depois_sha256':hashlib.sha256(parts[media]).hexdigest()})
    parts['word/document.xml']=etree.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
    assert {x for x in parts if parts[x]!=before[x]}=={'word/document.xml',media}
    temp=DEST.with_suffix('.tmp.docx')
    with ZipFile(temp,'w') as z:
        for info in infos:z.writestr(info,parts[info.filename])
    temp.replace(DEST)
    (OUT/'alteracoes_editoriais.json').write_text(json.dumps({'base':'v004','sha256_base':expected,'alteracoes':log,'sem_alteracao_de_resultados_experimentais':True},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (OUT/'antes_exportacao.docx').write_bytes(DEST.read_bytes())
    print('Quatro alterações textuais e uma figura; apenas document.xml e a mídia da Figura 1 alterados no pacote.')

if __name__=='__main__':main()
