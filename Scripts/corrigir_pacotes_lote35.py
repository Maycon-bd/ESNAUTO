"""Distingue bibliotecas carregadas no legado e seu uso no motor atual."""
import hashlib,json,shutil
from pathlib import Path
from zipfile import ZipFile
from lxml import etree
from incorporar_fechamento_integral_lote1 import NS,visible,replace_text,format_revised_prose

root=Path(__file__).resolve().parents[1]; out=root/'reports/fechamento_integral_20261029'
doc=root/'reports/monografia/trabalho/fechamento_integral_20261029.docx'; sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(doc)=='ee6e179ab0ba157fb9f1348a1ac75c38813be767c3a27367481727f59641af50'
backup=out/'antes_lote35.docx'; assert not backup.exists(); shutil.copy2(doc,backup)
with ZipFile(doc) as z: infos=z.infolist(); parts={i.filename:z.read(i.filename) for i in infos}
before=dict(parts); tree=etree.fromstring(parts['word/document.xml'])
targets=[p for p in tree.xpath('//w:p',namespaces=NS) if visible(p).startswith('A implementação partiu de códigos em R fornecidos pelo orientador')]
assert len(targets)==1; p=targets[0]; old=visible(p)
phrase='Foram empregados GA na busca genética; PerformanceAnalytics nas medidas descritivas; fGarch, PearsonDS e StockDistFit nas distribuições; fitdistrplus e MASS no ajuste; pracma na medição de tempo; e ggplot2 na visualização.'
replacement=('O código atual usa GA na busca e geradores de distribuições com fGarch e PearsonDS. '
 'O script anterior carrega também PerformanceAnalytics, StockDistFit, fitdistrplus, MASS, pracma e ggplot2; '
 'os exemplos de ajuste encontrados estão comentados. No motor atual, proc.time mede o tempo e pracma fornece uma pseudoinversa alternativa.')
assert old.count(phrase)==1; new=old.replace(phrase,replacement); assert len(new)<=700
replace_text(p,new); format_revised_prose(p,0)
parts['word/document.xml']=etree.tostring(tree,xml_declaration=True,encoding='UTF-8',standalone=True)
assert [n for n in parts if parts[n]!=before[n]]==['word/document.xml']
tmp=doc.with_suffix('.tmp.docx')
with ZipFile(tmp,'w') as z:
 for i in infos:z.writestr(i,parts[i.filename])
tmp.replace(doc)
files=['Scripts/acoes_petr4_esn.R','app/utils/esn_core.R','app/utils/ga_engine.R','app/utils/data_prep.R']
data={'base':'v005','sha256_base':'2af31abca4e3ba9fd5caf7cd161e55472dc94edc136cdf89732c0d0401118d6b','sha256_rascunho_antes':sha(backup),'sha256_rascunho_apos_edicao':sha(doc),'local':'Material e Métodos, parágrafo sobre implementação','texto_antes':old,'texto_depois':new,
 'evidencias':[{'arquivo':p,'sha256':sha(root/p)} for p in files],
 'diagnostico':'Script anterior, linhas 26–34 e 90–96: bibliotecas carregadas; fitdist, fitdistr e ged_fit comentados. Usa tic/toc do pracma nas linhas 360–365. Motor atual: esn_core.R linhas 19–41 e 67 usa proc.time e pracma::pinv na alternativa em caso de erro; ga_engine.R usa GA e proc.time; data_prep.R documenta geradores fGarch/PearsonDS. Código atual não prova todos os detalhes das execuções históricas.',
 'limite':'Correção da descrição do código preservado, sem executar experimentos ou alterar dados; não infere ausência de outras rotinas de ajuste.', 'estado':'pendente_exportacao_validacao_e_inspecao'}
(out/'conferencia_pacotes_lote35.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print('Descrição dos pacotes corrigida; inspeção pendente.')
