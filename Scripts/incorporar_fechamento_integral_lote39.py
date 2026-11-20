"""Distingue configuração do motor preservado da execução histórica."""
import hashlib,json
from pathlib import Path
from docx import Document
root=Path(__file__).resolve().parents[1];out=root/'reports/fechamento_integral_20261029';doc=root/'reports/monografia/trabalho/fechamento_integral_20261029.docx';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
before='3765c2ca1972edb428ba95dcb1f7e88b049bdd11d01ef7b2222e2774d180bd38';assert sha(doc)==before
sources=['app/utils/ga_engine.R','Scripts/acoes_petr4_esn.R','docs/08_comparativo_quatro_ondas_estocasticas.md','docs/09_onda_5_ajustes_empiricos_easyfit.md','docs/BASE_ARTIGO_ESNAUTO_RESULTADOS_E_REFERENCIAS.md']
d=Document(doc);edits=[
 (319,0,'codificação de 55 bits utilizada no ESNAUTO','codificação de 55 bits implementada no motor atual do ESNAUTO'),
 (327,0,'O cromossomo utilizado possuía 55 bits:','No motor atual, o cromossomo possui 55 bits:'),
 (327,0,'A população foi inicializada por LHS nas cinco dimensões e convertida para a codificação binária. O operador empregou seleção por torneio,','A população é inicializada por LHS nas cinco dimensões e convertida para a codificação binária. O operador emprega seleção por torneio,'),
 (327,2,'no regime normal.','no regime normal. A correspondência desses parâmetros com cada execução histórica não foi estabelecida, conforme a Seção 3.8.'),
 (328,0,'Quando o limite adaptativo de estagnação foi atingido, a taxa de mutação foi elevada para 40%, preservando-se o melhor indivíduo e as matrizes associadas ao recorde. Como o método não implementou ','Quando habilitado o mecanismo antiestagnação, o motor atual eleva a taxa de mutação para 40% ao atingir o limite adaptativo e preserva o melhor indivíduo e as matrizes associadas ao recorde. Como o método não implementa '),
 (328,2,'foi caracterizado como Algoritmo Genético','é caracterizado como Algoritmo Genético'),
 (330,0,'A função de aptidão combinou erros de treino e validação:','No motor atual, a função de aptidão combina erros de treino e validação:'),
 (330,6,'O sinal negativo converteu a minimização em maximização para o pacote GA. A ponderação atribuiu maior peso à validação','O sinal negativo converte a minimização em maximização para o pacote GA. A ponderação atribui maior peso à validação')]
logs=[]
for i,run,a,b in edits:
 r=d.paragraphs[i].runs[run];assert r.text.count(a)==1,(i,run,a);r.text=r.text.replace(a,b);logs.append({'paragrafo':i,'antes':a,'depois':b})
d.save(doc);record={'base':'v005','sha256_base':'2af31abca4e3ba9fd5caf7cd161e55472dc94edc136cdf89732c0d0401118d6b','sha256_antes':before,'sha256_apos_edicao':sha(doc),'fontes':[{'arquivo':f,'sha256':sha(root/f)} for f in sources],'evidencia':'ga_engine.R linhas 28–65, 293–296 e 318–460 descreve a implementação atual. Script legado linhas 361–363 usa 59 bits, crossover 0,8 e mutação 0,1; documentação histórica registra diferença entre 35% e 40%. Relatórios das ondas não vinculam todos os parâmetros ao código de cada execução. Diferenças entre versões não provam qual versão gerou um resultado particular.','alteracoes':logs,'estado':'pendente_exportacao_e_inspecao'};(out/'incorporacao_lote39.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print('Quatro parágrafos precisados, exportação pendente.')
