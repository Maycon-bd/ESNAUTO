"""Registra procedência bibliométrica e delimita metadado histórico no Word."""
import hashlib,json,shutil
from pathlib import Path
from zipfile import ZipFile
from lxml import etree
from incorporar_fechamento_integral_lote1 import NS,visible,replace_text,format_revised_prose

root=Path(__file__).resolve().parents[1]; out=root/'reports/fechamento_integral_20261029'
doc=root/'reports/monografia/trabalho/fechamento_integral_20261029.docx'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(doc)=='a5c3346495a63cd685209a9539258872cac941afef89660568d02c518922bc32'
backup=out/'antes_lote28.docx'; assert not backup.exists(); shutil.copy2(doc,backup)
base=json.loads((root/'reports/bibliometria_reconstrucao/base_reconstruida.json').read_text(encoding='utf8'))
item=next(r for r in base['records'] if r['id']=='D11'); assert item['year']==2023 and not item['keywords_originais']
with ZipFile(doc) as z: infos=z.infolist(); parts={i.filename:z.read(i.filename) for i in infos}
before=dict(parts); tree=etree.fromstring(parts['word/document.xml'])
targets=[p for p in tree.xpath('//w:p',namespaces=NS) if visible(p).startswith('Foram preservadas as informações das versões locais consultadas')]
assert len(targets)==1; p=targets[0]; old=visible(p)
addition=(' No arquivo histórico processado, a tese de Duttilo consta com ano 2023, enquanto a referência foi atualizada para 2024 conforme a versão consultada. As Figuras 2 a 4 usam palavras-chave ou títulos e não dependem desse ano.')
new=old+addition; assert len(new)<=700
replace_text(p,new); format_revised_prose(p,0)
parts['word/document.xml']=etree.tostring(tree,xml_declaration=True,encoding='UTF-8',standalone=True)
assert [x for x in parts if parts[x]!=before[x]]==['word/document.xml']
temp=doc.with_suffix('.tmp.docx')
with ZipFile(temp,'w') as z:
 for i in infos:z.writestr(i,parts[i.filename])
temp.replace(doc)
items=['Scripts/analisar_bibliometria_reconstruida.R','reports/bibliometria_reconstrucao/base_reconstruida.json','reports/bibliometria_reconstrucao/colecao_bibliometrix.rds','reports/bibliometria_reconstrucao/validacao_bibliometrix.json','Scripts/results/bibliometria_ambiente/R-library/bibliometrix/DESCRIPTION']
report={'base':'v005','sha256_base':'2af31abca4e3ba9fd5caf7cd161e55472dc94edc136cdf89732c0d0401118d6b','sha256_rascunho_antes':sha(backup),'sha256_rascunho_apos_edicao':sha(doc),
 'afirmacoes':[
  {'referencia':'Aria e Cuccurullo (2017)','localizacao':'3.8.3, descrição do bibliometrix','diagnostico':'Condizente com o resumo e a seção 4, p. 963, da publicação; biblioNetwork e coocorrências descritos nas p. 968–969. Conferência dirigida, não leitura integral.', 'fonte':'https://arquivos-producao.ufopa.edu.br/arquivos/202319207961ac761891c0c27aad4249/Aria__Cuccurullo_2017_Bibliometrix.pdf'},
  {'referencia':'Aria et al. (2026)','localizacao':'3.8.3, Biblioshiny','diagnostico':'A descrição da interface é apoiada pelo resumo do artigo e pelo relato de um dos autores; exame focal, não leitura integral.', 'fonte':'https://lucadaniello.github.io/blog/biblioshiny-saas/'},
  {'afirmacao':'Uso do bibliometrix 5.5.0, biblioNetwork e validação do carregador','diagnostico':'Convergência entre código de análise, DESCRIPTION local e relatório de validação; o carregador foi chamado como função em R, não há alegação de uso da interface gráfica.'},
  {'afirmacao':'Figuras 2 a 4 e metadados de Duttilo','diagnostico':'O JSON e a coleção RDS histórica identificam D11 com ano 2023 e sem palavras-chave; a referência atual usa 2024. Figuras 2 e 3 usam palavras-chave, figura 4 usa títulos; os scripts dessas análises não usam o ano como variável. A coleção antiga não foi modificada e o texto registra a diferença.'}],
 'arquivos_locais':[{'caminho':x,'sha256':sha(root/x)} for x in items],
 'texto_antes':old,'texto_depois':new,'limites':'Não foi refeita a análise bibliométrica, nem comprovada a identidade visual a partir do script neste lote. As citações do trecho foram examinadas no escopo descrito, sem selo de originalidade.',
 'estado':'pendente_exportacao_validacao_e_inspecao'}
(out/'conferencia_bibliometria_lote28.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('Conferência registrada e ressalva incorporada; pendente validação visual.')
