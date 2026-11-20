"""Incorpora precisão de Ping e Sudiatmika na mesma cópia da v005."""
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile
from lxml import etree
import incorporar_fechamento_integral_lote1 as helper

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reports/fechamento_integral_20261029'
DEST=ROOT/'reports/monografia/trabalho/fechamento_integral_20261029.docx'

def main():
    prev=json.loads((OUT/'incorporacao_lote1.json').read_text(encoding='utf-8'))
    assert hashlib.sha256(DEST.read_bytes()).hexdigest()==prev['sha256_apos_lote']
    findings=json.loads((OUT/'achados_leituras_lote2.json').read_text(encoding='utf-8'))
    inv=json.loads((OUT/'inventario_unidades.json').read_text(encoding='utf-8'));lookup={x['id']:x for x in inv['unidades']}
    with ZipFile(DEST) as z:infos=z.infolist();parts={x.filename:z.read(x.filename) for x in infos}
    before=dict(parts);root=etree.fromstring(parts['word/document.xml']);pars=root.xpath('//w:p',namespaces=helper.NS)
    helper.ITALIC_PHRASES=helper.ITALIC_PHRASES+('feedforward',)
    changes=[]
    for x in findings['propostas']:
        u=lookup[x['unidade']];p=pars[u['indice_paragrafo_xml']];assert helper.visible(p)==x['texto_anterior']
        helper.replace_text(p,x['proposta']);helper.format_revised_prose(p,u['indice_paragrafo_xml'])
        x['estado']='incorporado_em_copia_de_trabalho_pendente_conferencia_nativa'
        changes.append({'unidade':u['id'],'antes':x['texto_anterior'],'depois':helper.visible(p),'evidencia':'achados_leituras_lote2.json'})
    parts['word/document.xml']=etree.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
    assert [k for k in parts if before[k]!=parts[k]]==['word/document.xml']
    temp=DEST.with_suffix('.tmp.docx')
    with ZipFile(temp,'w') as z:
        for info in infos:z.writestr(info,parts[info.filename])
    temp.replace(DEST)
    data={'base':'v005','sha256_antes_lote':prev['sha256_apos_lote'],'sha256_apos_lote':hashlib.sha256(DEST.read_bytes()).hexdigest(),'alteracoes':changes,'estado':'rascunho_nao_promovido','resultados_experimentais_alterados':False}
    for name,obj in [('incorporacao_lote2.json',data),('achados_leituras_lote2.json',findings)]:
        (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    state=json.loads((OUT/'estado_meta.json').read_text(encoding='utf-8'));state['correcoes_word_incorporadas_nesta_meta']=7
    (OUT/'estado_meta.json').write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Três ajustes de precisão incorporados; total6parágrafos e1referência. Cópia ainda em auditoria.')

if __name__=='__main__':main()
