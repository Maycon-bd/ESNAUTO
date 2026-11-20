"""Corrige alcance da descrição do procedimento de reexecução."""
import hashlib,json
from pathlib import Path
from docx import Document
root=Path(__file__).resolve().parents[1];out=root/'reports/fechamento_integral_20261029';doc=root/'reports/monografia/trabalho/fechamento_integral_20261029.docx';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();before='4cf48044445c0760210b1206c185487b8406af3eaecb541de6db381cdbf735b0';assert sha(doc)==before
d=Document(doc);edits=[(371,0,'A reexecução documentada do protocolo partiu do mesmo núcleo matemático utilizado pelo ESNAUTO.','O procedimento para nova execução utiliza o núcleo matemático disponibilizado pelo ESNAUTO.'),(371,0,'Em seguida, foram definidas as distribuições de ','O motor atual permite definir as distribuições de '),(371,5,' e executado o Algoritmo Genético binário com cromossomo de 55 bits, população inicial por LHS, seleção por torneio, ',' e executar o Algoritmo Genético binário com cromossomo de 55 bits, população inicial por LHS, seleção por torneio, '),(374,0,'a reexecução do protocolo foi documentada','o procedimento para nova execução foi documentado')]
logs=[]
for i,r,a,b in edits:
 x=d.paragraphs[i].runs[r];assert x.text.count(a)==1,(i,r);x.text=x.text.replace(a,b);logs.append({'paragrafo':i,'antes':a,'depois':b})
d.save(doc);result={'base':'v005','sha256_base':'2af31abca4e3ba9fd5caf7cd161e55472dc94edc136cdf89732c0d0401118d6b','sha256_antes':before,'sha256_apos_edicao':sha(doc),'evidencia':'conferencia_motor_historico_lote27.json e app/utils/ga_engine.R: os valores caracterizam o motor atual; registros consolidados não demonstram sua versão exata em cada execução histórica. A partição temporal permanece amparada nos dados de entrada.','alteracoes':logs,'estado':'pendente_exportacao_e_inspecao'};(out/'incorporacao_lote44.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print('Descrição corrigida, exportação pendente.')
