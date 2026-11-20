"""Delimita evidência histórica do motor sem repetir experimentos."""
import hashlib
import json
import shutil
from pathlib import Path
from zipfile import ZipFile
from lxml import etree
from incorporar_fechamento_integral_lote1 import NS, visible, replace_text, format_revised_prose

root=Path(__file__).resolve().parents[1]
folder=root/'reports/fechamento_integral_20261029'
dest=root/'reports/monografia/trabalho/fechamento_integral_20261029.docx'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(dest)=='fb5e2653547af740b586a95aee3d93259745df36ebc4f7c61c7cd2047b3a1ce7'
backup=folder/'antes_lote27.docx'; assert not backup.exists(); shutil.copy2(dest,backup)
with ZipFile(dest) as z:
    infos=z.infolist(); parts={i.filename:z.read(i.filename) for i in infos}
before=dict(parts); tree=etree.fromstring(parts['word/document.xml'])
paragraphs=tree.xpath('//w:p',namespaces=NS)
targets=[p for p in paragraphs if visible(p).startswith('As execuções oficiais foram realizadas em rotinas automatizadas em lote,')]
assert len(targets)==1
p=targets[0]; old=visible(p)
first=('As execuções oficiais foram realizadas em rotinas automatizadas em lote, utilizando o mesmo motor empregado pela interface Shiny. O conjunto final compreendeu 45 execuções de produção, organizadas em cinco ondas, com limite de 10.000 gerações por rodada.')
revised=('Os relatórios consolidados associam as execuções oficiais ao motor com LHS e mecanismo antiestagnação. O projeto também contém uma interface Shiny e rotinas em lote; contudo, a correspondência do código preservado com cada execução histórica não pôde ser verificada individualmente. Segundo esses relatórios, o conjunto final compreendeu 45 execuções de produção, organizadas em cinco ondas, com limite de 10.000 gerações por rodada.')
assert old.startswith(first)
new=revised+old[len(first):]
assert len(new)<=700
replace_text(p,new); format_revised_prose(p,0)
parts['word/document.xml']=etree.tostring(tree,xml_declaration=True,encoding='UTF-8',standalone=True)
assert [x for x in parts if parts[x]!=before[x]]==['word/document.xml']
temp=dest.with_suffix('.tmp.docx')
with ZipFile(temp,'w') as z:
    for i in infos: z.writestr(i,parts[i.filename])
temp.replace(dest)
report={'base':'v005','sha256_base':'2af31abca4e3ba9fd5caf7cd161e55472dc94edc136cdf89732c0d0401118d6b',
 'sha256_rascunho_antes':sha(backup),'sha256_rascunho_apos_edicao':sha(dest),
 'ancora':'3.8.4 Procedimento de re-execução dos experimentos','antes':old,'depois':new,
 'evidencia':[
  {'arquivo':'docs/08_comparativo_quatro_ondas_estocasticas.md','sha256':sha(root/'docs/08_comparativo_quatro_ondas_estocasticas.md'),'achado':'Relatório consolidado declara 30 rodadas, LHS, cataclismo e teto de 10.000 gerações.'},
  {'arquivo':'docs/09_onda_5_ajustes_empiricos_easyfit.md','sha256':sha(root/'docs/09_onda_5_ajustes_empiricos_easyfit.md'),'achado':'Relatório consolidado declara 15 rodadas, LHS, cataclismo e teto de 10.000 gerações.'},
  {'arquivo':'Scripts/onda5_easyfit_simulations.R','sha256':sha(root/'Scripts/onda5_easyfit_simulations.R'),'achado':'Roteiro localizado define 12 cenários e 200 gerações; não identifica as 15 rodadas de produção e não demonstra sua execução.'},
  {'arquivo':'app/utils/ga_engine.R','sha256':sha(root/'app/utils/ga_engine.R'),'achado':'Código atual contém inicializador LHS e mecanismo antiestagnação; versão b30ef22b419aee844a7d35354c32848ab4369c74 já contém funções correspondentes. Isso não prova qual versão foi usada em cada execução.'},
  {'arquivo':'reports/esclarecimentos_autor_20261029/conferencia_onda5.json','sha256':sha(root/'reports/esclarecimentos_autor_20261029/conferencia_onda5.json'),'achado':'Busca anterior registrou resultados compilados e alcance da tentativa de localizar saídas por execução.'}],
 'interpretacao':'Limitação de rastreabilidade não prova que as rodadas ou mecanismos não existiram. Os resultados consolidados permanecem, sem atribuir ao roteiro de 200 gerações as 15 rodadas.',
 'estado':'pendente_exportacao_validacao_e_inspecao_visual'}
(folder/'conferencia_motor_historico_lote27.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Texto delimitado; necessita validação e inspeção visual.')
