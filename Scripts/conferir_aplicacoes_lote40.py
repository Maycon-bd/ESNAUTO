"""Vincula redação atual a leituras anteriores e trechos primários de aplicações."""
import hashlib,json
from pathlib import Path
from docx import Document
root=Path(__file__).resolve().parents[1];out=root/'reports/fechamento_integral_20261029';doc=root/'reports/monografia/trabalho/fechamento_integral_20261029.docx';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(doc)=='4cf48044445c0760210b1206c185487b8406af3eaecb541de6db381cdbf735b0'
idx=json.loads((out/'indice_citacoes_atuais_lote39.json').read_text(encoding='utf8'));refs={r['id']:r for r in idx['registros']};D=Document(doc)
items=[
 (187,'R45','Timbó et al. (2016)','PDF 4–8, Tabelas 2–3','Regressão múltipla para PETR4; correlação de Pearson apoia seleção de indicadores. O sucesso é tolerância de erro absoluto até 0,50, sem identificação com acerto de direção. A fonte contém outras inconsistências de contagem não reproduzidas.'),
 (188,'R14','Costa e Lunkes (2025)','PDF 13–15 e 19','SVM classifica com indicadores técnicos e fundamentalistas; F1 é 72,74% na amostra e a recomendação inclui redes e ensembles. A fonte tem divergências de datas e contagens, não transferidas ao texto.'),
 (199,'R11','Chen et al. (2026)','PDF 13–14, Tabela 6','No conjunto JPX, Sharpe da QTCNN é 0,538 versus 0,313 Transformer, 0,044 LSTM e 0,412 TConv-MLP, em avaliação de 22 dias. Circuitos simulados; não se extrapola a superioridade.'),
 (201,'R05','Behera, Nayak e Kumar (2023)','PDF 1 e 12–33','Revisão de HONNs e métodos evolucionários para séries financeiras; seu conjunto reúne pesquisas heterogêneas. Não relata um novo experimento comparativo universal.'),
 (213,'R40','Sharma et al. (2025)','PDF 7–8, 11–12, Tabela 3 e Figura 8; inspeção visual de PDF 6','Prevê Bitcoin e compara ESN, XGBoost e previsão ingênua; Mann–Whitney compara razões ESN/XGBoost entre grupos de caos, com diferença nas janelas 30 e 60, não em 15. A camada textual indevida da página 6 foi excluída na leitura.'),
 (217,'R44','Tian e Pei (2024)','PDF 4–6 e 9–12, Tabelas 1–3','SSA ajusta ESN; 10 ações dos EUA e 10 da China; comparação inclui BP, Elman, LSTM e ESN. Página 5 diz que ESN e SSA-ESN usam as mesmas matrizes Win e W.'),
 (218,'R15','Deng et al. (2022)','PDF 10–13 e 20, Tabela 6','AG seleciona escalonamento de entrada, raio espectral e vazamento para ESNs empilhadas em PEMFC. A tabela credita comparadores LSTM, ARIMA e Fusion à referência 36; a monografia não os apresenta como experimento direto independente.'),
 (219,'R20','Ecer et al. (2020)','PDF 5–11, seções 3.1–3.3','O estudo BIST 100 compara MLP, MLP-GA e MLP-PSO, com funções e populações diferentes; não é uma ESN nem prova estabilidade universal.'),
 (219,'R05','Behera, Nayak e Kumar (2023)','PDF 1 e seções de revisão','Fonte resume trabalhos sobre redes de ordem superior e otimização evolucionária; o trecho atual não atribui a ela consenso universal.'),
 (220,'R41','Soltani, Benmohamed e Ltifi (2022)','PDF 2 e 8–14, Tabela 5','Pré-print apresenta revisão de 74 estudos e associa PSO a 16 trabalhos e AG a dez; a frequência é relato da revisão, não ranking de eficácia ou contagem independentemente refeita.'),
 (239,'R14','Costa e Lunkes (2025)','PDF 12, dados e variáveis','Descreve preços ajustados por desdobramentos e dividendos na classe e indicadores; uso do ajuste não demonstra desempenho geral de qualquer modelo.'),
 (250,'R44','Tian e Pei (2024)','PDF 3–6 e 9–12','Comparadores, tarefa, SSA e 20 ações são confirmados; as distribuições de atualização da SSA não são automaticamente leis dos pesos da ESN.'),
 (253,'R40','Sharma et al. (2025)','PDF 7–8, Tabela 1','TPE/Hyperopt seleciona hiperparâmetros; treinamento 15/30/60 observações, teste 10 e avanço 1. Os comprimentos das janelas não equivalem a horizontes de previsão.'),
 (258,'R15','Deng et al. (2022)','PDF 10–13','AG otimiza parâmetros das ESNs empilhadas na tarefa de degradação; os efeitos são restritos ao protocolo estudado.'),
 (258,'R44','Tian e Pei (2024)','PDF 4–6','A seleção de hiperparâmetros por SSA está descrita; uso de heurística não comprova ótimo global.'),
 (258,'R40','Sharma et al. (2025)','PDF 7–8','Otimização Bayesiana via TPE para hiperparâmetros, sem inferência de garantia de ótimo global.'),
 (258,'R41','Soltani, Benmohamed e Ltifi (2022)','PDF 8–14','A revisão reúne técnicas distintas; diversidade de uso não demonstra consenso de superioridade.')]
rows=[]
for p,r,anchor,loc,evidence in items:
 t=D.paragraphs[p].text;assert anchor in t,(p,r);ref=refs[r];path=root/ref['arquivo_fonte'];assert sha(path)==ref['sha256_fonte'];rows.append({'ancora':f'P_atual{p:04}','texto_atual':t,'referencia':r,'fonte_id':ref['fonte_id'],'arquivo_fonte':ref['arquivo_fonte'],'sha256_fonte':ref['sha256_fonte'],'localizador':loc,'evidencia':evidence,'diagnostico':'condizente na afirmação delimitada'})
f=out/'afirmacoes_aplicacoes_lote40.json';assert not f.exists();f.write_text(json.dumps({'base':'v005','sha256_base':'2af31abca4e3ba9fd5caf7cd161e55472dc94edc136cdf89732c0d0401118d6b','sha256_rascunho':sha(doc),'escopo':'17 relações de afirmação e fonte; leituras primárias e evidências anteriores foram confrontadas com as passagens atuais. Outras afirmações do mesmo parágrafo não são automaticamente aprovadas.','registros':rows,'acao':'Nenhuma edição nos pontos examinados.'},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
s=out/'estado_meta.json';state=json.loads(s.read_text(encoding='utf8'));state['ultimo_registro_de_leitura']=str(f.relative_to(root));state['proxima_passagem']='Conferir demais ocorrências e revalidar Guia na cópia atual.';s.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print('17 relações registradas.')
