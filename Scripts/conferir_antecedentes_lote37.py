"""Rastreia afirmações sobre Araújo, BovDB e o estudo anterior de PETR4."""
import hashlib,json
from pathlib import Path
from docx import Document

root=Path(__file__).resolve().parents[1]; out=root/'reports/fechamento_integral_20261029'; doc=root/'reports/monografia/trabalho/fechamento_integral_20261029.docx'; sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(doc)=='63ca3ec4031dafe5a78b6785f2a5d7581f5deacc461c9096c392dedc5963b62e'
idx=json.loads((out/'indice_citacoes_atuais_lote36.json').read_text(encoding='utf8')); refs={r['id']:r for r in idx['registros']}; D=Document(doc)
rb=root/'reports/fontes_drive_20261029/Cardoso_RBras_2022_completo.pdf'
supp={'R06':(str(rb.relative_to(root)),sha(rb))}
items=[
 (221,'R02','Araújo et al. (2025)','PDF 4–5 e 7–10','Prova de autor descreve ESN, AG e distribuições com dados financeiros brasileiros; as frases seguintes descrevem o presente trabalho e não atribuem sua integração à fonte.'),
 (234,'R02','Araújo et al. (2025)','PDF 5 e 10','São nomeadas Normal, Uniforme, Student t, GED e Student t assimétrica; a prova não individualiza por completo a lei por matriz, e o parágrafo registra essa limitação.'),
 (234,'R40','Sharma et al. (2025)','PDF 7, Tabela 1','Uniforme discreta e log-uniforme descrevem amostragem dos hiperparâmetros, com função distinta da lei de geração de Win; a monografia preserva a distinção.'),
 (245,'R02','Araújo et al. (2025)','PDF 7–8 e 10','Prova compara MAE e RMSE como aptidão; descreve retornos de ITSA4, referência a variâncias diárias e divisão 60/20/20. A redação ressalva a prova e o protocolo distinto.'),
 (259,'R02','Araújo et al. (2025)','PDF 4–5 e 10','O trabalho anterior combina distribuições e ESN em série financeira; o parágrafo apresenta a motivação e a escolha da pesquisa atual sem alegar ineditismo universal.'),
 (260,'R02','Araújo et al. (2025)','PDF 4 e 7–10','ESN, distribuições e otimização aparecem no estudo anterior; não confundir o protocolo de ITSA4 com o da PETR4.'),
 (319,'R02','Araújo et al. (2025)','PDF 8–9','A prova registra cromossomo binário de 55 bits e lista cinco hiperparâmetros, sem repartir bits por parâmetro na passagem.'),
 (319,'R06','Cardoso, Berri e Mattos (2022a, p. 203)','p. 203 impressa, PDF 7','A página indica raio espectral 1,25, vazamento 0,2 e regularização 10⁻⁸. Inspeção visual direta da página preservada.'),
 (330,'R02','Araújo et al. (2025)','PDF 7–8; app/utils/ga_engine.R linhas 293–296','A prova descreve ponderação 40% treino e 60% validação tanto para MAE quanto RMSE; o código atual usa sinal negativo e MAE ponderado. Não se afirma que todas as saídas históricas preservam o código.'),
 (236,'R07','Cardoso et al. (2022b)','PDF 5, Figura 1; PDF 7','O esquema BovDB inclui Price.factor, EventPrice.factor e EventPrice.applied e a discussão descreve os fatores. O texto não atribui a transformação local ao autor.'),
 (237,'R07','Cardoso et al., 2022b','PDF 5 e 7, Figura 1 e equações 1–2','O fator isolado usa fechamento anterior sobre abertura no primeiro dia do evento, com fatores acumulados regressivos; applied distingue eventos considerados.'),
 (243,'R07','Cardoso et al. (2022b)','PDF 1, 5 e 7','O artigo apresenta BovDB para ações da B3 e descreve fator de ajuste. A relevância central ao trabalho é uma avaliação do autor da monografia.'),
 (451,'R06','Cardoso, Berri e Mattos (2022a, p. 202–205)','p. 202–205 impressas, PDF 6–9','O estudo informa 5.197 observações e partição 75/25; RMSE 11,1785 sem fator e 0,4987 com fator. A comparação não é tratada como teste de superioridade do ESNAUTO.')]
rows=[]
for p,r,anchor,loc,ev in items:
 text=D.paragraphs[p].text; assert anchor in text,(p,r)
 ref=refs[r];path,expected=supp[r] if r in supp else (ref['arquivo_fonte'],ref['sha256_fonte']); assert sha(root/path)==expected
 rows.append({'ancora':f'P_atual{p:04}','texto_atual':text,'referencia':r,'arquivo_fonte':path,'sha256_fonte':expected,'localizador':loc,'evidencia':ev,'diagnostico':'condizente na afirmação delimitada'})
f=out/'afirmacoes_antecedentes_lote37.json';assert not f.exists();f.write_text(json.dumps({'base':'v005','sha256_base':'2af31abca4e3ba9fd5caf7cd161e55472dc94edc136cdf89732c0d0401118d6b','sha256_rascunho':sha(doc),'escopo':'13 relações de citação e afirmação. Documento de Araújo consultado é prova de autor; vínculos e conclusões não são transferidos automaticamente para outros trechos.','registros':rows,'acao':'Nenhuma edição adicional nos pontos examinados.'},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
s=out/'estado_meta.json';state=json.loads(s.read_text(encoding='utf8'));state['ultimo_registro_de_leitura']=str(f.relative_to(root));state['proxima_passagem']='Continuar confronto de ocorrências não registradas por afirmação e revisar Guia.';s.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print('13 relações registradas.')
