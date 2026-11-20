"""Corrige a unidade de seleção do comparador no estudo de Wang et al."""
import hashlib,json
from pathlib import Path
from docx import Document
root=Path(__file__).resolve().parents[1]
doc=root/'reports/monografia/trabalho/fechamento_integral_20261029.docx'; out=root/'reports/fechamento_integral_20261029'; sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
oldhash='63ca3ec4031dafe5a78b6785f2a5d7581f5deacc461c9096c392dedc5963b62e'; assert sha(doc)==oldhash
idx=json.loads((out/'indice_citacoes_atuais_lote36.json').read_text(encoding='utf8'));ref=next(x for x in idx['registros'] if x['id']=='R47');assert sha(root/ref['arquivo_fonte'])==ref['sha256_fonte']
d=Document(doc);p=d.paragraphs[208];assert len(p.runs)==1
old=p.text;before='seleciona o melhor comparador para cada série';after='apresenta o melhor comparador por horizonte de previsão';assert old.count(before)==1
p.runs[0].text=old.replace(before,after);d.save(doc)
record={'base':'v005','sha256_base':'2af31abca4e3ba9fd5caf7cd161e55472dc94edc136cdf89732c0d0401118d6b','sha256_antes':oldhash,'sha256_apos_edicao':sha(doc),'paragrafo':'P_atual0208','antes':old,'depois':p.text,'fonte':ref['arquivo_fonte'],'sha256_fonte':ref['sha256_fonte'],'localizador':'PDF 8, seção 5','evidencia':'A fonte declara Lasso como melhor baseline para um passo e LSTM para quatro e dez passos; não afirma selecionar um modelo distinto para cada série.','estado':'corrigido_na_copia_de_trabalho_pendente_exportacao_e_inspecao'}
(out/'incorporacao_lote38.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print('Parágrafo corrigido; exportação e inspeção pendentes.')
