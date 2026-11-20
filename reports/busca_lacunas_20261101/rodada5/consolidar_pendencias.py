"""Consolida requisitos documentais humanos; não infere respostas científicas."""
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json

ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
TASK=OUT.parent
questions={
 'D01/P3':'Qual vetor de363observações foi efetivamente analisado e qual código documenta exclusão/tratamento de zeros e mudança de escala? Ver perguntas específicas da rodada3; a reconstrução parcial não comprova o protocolo.',
 'D02/P1':'A quais matrizes Win/W se aplicam as famílias testadas, com quais escalas e transformações? É necessário trecho de método/código associado ao experimento, não apenas o nome das famílias.',
 'D02/P4':'Há tabela/suplemento do mesmo trabalho com métricas de previsão envolvendo LSTM, GRU ou Transformer? A comparação entre famílias ESN não responde ao critério.',
 'D03/P1':'Qual passagem substantiva da revisão ou suplemento vincula uma lei probabilística à geração de Win/W, distinguindo pesos de variáveis do otimizador?',
 'D03/P4':'A revisão reproduz comparação numérica de previsão com LSTM/GRU/Transformer? Localizar tabela e fonte original; a referência187 isolada não basta.',
 'D07/P4':'Existe comparação numérica de previsão com LSTM/GRU/Transformer além dos três modelos SVM descritos? Caso não tenha sido realizada/reportada, não é possível reconstruí-la como resultado do artigo.',
 'D08/P1':'Qual lei gerou os valores dos pesos do reservatório, com qual escala/reescalamento? Especificar separadamente as matrizes do autoencoder; o site do autor e a fichaDTU não fornecem essa resposta.',
 'D12/P4':'Há resultado LSTM/GRU/Transformer no mesmo protocolo além das13configurações MLP/MLP-GA/MLP-PSO? É necessária a evidência numérica correspondente.',
 'D13/P4':'Existe suplemento com contraste quantitativo LSTM/GRU/Transformer além das variantesESN das duas tabelas? O pacote editorialarXiv consultado não contém essa evidência.',
 'D15/P4':'Há comparação numérica LSTM/GRU/Transformer nesta obra/suplemento de geração de frequência? Discussão de vantagens de treino não substitui o contraste.',
 'D16/P1':'Qual ambiente/versão de ReservoirPy e código efetivamente produziram os resultados? As matrizes locais uniformes foram passadas ao modelo em outra versão ou foram usados os inicializadores da biblioteca?',
 'D17/P4':'Existe contraste de previsão temporal com Transformer, separável do uso deGPT-2/FinBERT para sentimento e dos retornos das estratégias combinadas? Identificar alvo, métrica e protocolo.',
 'D19/P3':'Qual transformação concreta foi aplicada às séries de entrada, além de geração, divisão e washout? Localizar eventual código correspondente à dissertação, sem importar procedimento de outro artigo do autor.',
 'D19/P5':'Qual ativo/mercado financeiro foi efetivamente analisado na dissertação e onde estão seus dados/resultados? A referência genérica aForex no resumo não individualiza o experimento.',
 'D21/P3':'Há descrição suplementar de preparação concreta de série temporal identificada? O texto conceitual de duas páginas não a documenta.',
 'D21/P4':'Há resultados numéricos de previsão com LSTM/GRU/Transformer vinculados a esta comunicação, além de referências a outros artigos?',
 'D21/P5':'Qual mercado e ativo identificados foram objeto de análise, em vez de exemplos genéricos de finanças?',
 'D22/P1':'Qual lei probabilística foi empregada para gerar Win/W, distinta da dinâmicaLorenz e da esparsidade?',
 'D22/P4':'Há contraste numérico LSTM/GRU/Transformer no protocolo do artigo, além de Lorenz e variantesESN?',
 'D23/P1':'Na versão publicada ou código correspondente, qual lei e versão de biblioteca geraram Win/W? As distribuições de hiperparâmetros e o ruído não respondem.',
 'D23/P4':'A versão publicada contém comparação numérica LSTM/GRU/Transformer ausente da preprint examinada? Obter primeiro o corpo do capítuloDOI10.1007/978-981-95-4109-6_25; não presumir que o tenha.',
 'D24/P1':'Qual passagem da revisão/suplemento identifica a distribuição dos valores de Win/W? Representação binária da topologia não é lei dos pesos.',
 'D24/P3':'Que preparação concreta de séries é documentada na revisão para os benchmarks, além de hiperparâmetros de escala?',
 'D24/P4':'Qual tabela ou passagem reproduz contraste numérico com LSTM/GRU/Transformer, com fonte e tarefa identificáveis?',
 'D24/P5':'Qual mercado/ativo identificado aparece efetivamente na análise sintetizada, além dos benchmarks sintéticos/físicos?',
 'D26/P1':'Qual família e escala geraram Win e pesos recorrentes/feedback? A inicialização aleatória genérica é insuficiente.',
 'D26/P2':'Qual busca, sensibilidade com critério ou seleção manual escolheu500neurônios, raio0.999e esparsidade0.02?',
 'D26/P3':'Que operações concretas de limpeza/transformação foram aplicadas aos dadosYahooFinance? O rótulo limpeza no fluxo não especifica a operação.',
 'D27/P1':'Qual lei gerou os elementos de Win/W, separadamente das variáveis normais/bipolares do otimizadorSSA?',
 'D28/P4':'Há contraste quantitativo LSTM/GRU/Transformer associado ao trabalhoPETR4, além de regressão linear e previsão versus observado?',
 'D29/P4':'Há suplemento com contraste quantitativo LSTM/GRU/Transformer além deGS-ARIMA,PSO-ESN,HAR-PSO-ESN,HAR eGS-MLP?',
 'D30/P1':'Qual passagem substantiva ou fonte primária explicitamente ligada fornece lei/escala de Win/W? Citar possibilidade de usarpyESN/EsnTorch não identifica a configuração do estudo.',
 'D30/P4':'Quais resultados e protocolos originais sustentam72%/90%e18%, e onde está o contraste quantitativo qualificador? Conferir fonteGandhudi integral; resumo/preview não demonstram os números nem o contraste.',
 'D31/P1':'Qual distribuição/escala deWin e qual procedimento físico correspondente são explicitamente documentados? O repositório de correlações consultado não os fornece.',
 'D31/P2':'Qual procedimento e critério escolheram os ganhos de entrada/feedback do reservatório óptico? Não transportar gridsearch dos comparadoresML.',
 'D34/P1':'Qual família e escala geraram Win/W, distinta da matriz de observação gaussiana do compressed sensing?',
 'D34/P2':'Como foram escolhidos os hiperparâmetrosESN e a compressão50%? OMP e valores fixados não individualizam seleção por busca/sensibilidade.',
 'D34/P4':'Há suplemento com comparação quantitativa LSTM/GRU/Transformer além do contrasteESN versusCS-ESN?'
}
base=json.loads((TASK/'rodada4/pendencias38_conferidas.json').read_text(encoding='utf-8'))
rows=base['celulas'];assert len(rows)==38
assert set(questions)=={x['id']+'/'+x['dimensao'] for x in rows}
word=ROOT/'reports/monografia/versoes/v010/MayconGarciaSilva_monografia_v010.docx'
assert hashlib.sha256(word.read_bytes()).hexdigest()==base['sha256_base']
output=[]
for row in rows:
 path=ROOT/row['pdf'];assert hashlib.sha256(path.read_bytes()).hexdigest()==row['sha256_pdf']
 key=row['id']+'/'+row['dimensao']
 item={**row,'pergunta_documental':questions[key], 'resposta_comprovada':False}
 if key=='D30/P4':
  item['correcao_de_localizador']='O registro histórico diz tabela17; o correto é tabelas3e4na páginaPDF17, conforme rodada2. Tabela5na página18 foi inspecionada na rodada3.'
 output.append(item)
payload={'base':base['base'],'sha256_base':base['sha256_base'],'registrado_em_utc':datetime.now(timezone.utc).isoformat(),
 'alcance':'Perguntas derivadas das insuficiências documentadas; não são resposta de autores nem prova de ausência universal. Nenhum contato externo realizado.',
 'contagens':dict(Counter(x['dimensao'] for x in rows)), 'celulas':output}
(OUT/'requisitos_documentais38.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
text=['# Informação necessária nas38células restantes','',f"Basev010; SHA256 `{base['sha256_base']}`.",'',
 'Este inventário descreve exatamente o que falta comprovar. Os PDFs existentes foram identificados por hash. Acesso ao artigo não garante que ele reporte cada informação. As perguntas não exigem novos experimentos, não presumem que exista material adicional e não foram enviadas a autores.', '',
 '| Fonte | Dimensão | Evidência documental necessária |','|---|---|---|']
for x in output:text.append(f"| {x['autor']} ({x['id']}) | {x['dimensao']} | {x['pergunta_documental']} |")
text+=['','Não alterar os critérios para eliminar sinais. Se a informação não foi reportada nem puder ser documentada, conservar a insuficiência é mais fiel que inventar uma resposta. Isso não transforma o objetivo de preencher todas as células em objetivo concluído. A eventual aceitação acadêmica desse limite é decisão distinta da recuperação das informações.']
(OUT/'requisitos_documentais38.md').write_text('\n'.join(text)+'\n',encoding='utf-8')
print(json.dumps({'celulas':len(output),'fontes':len(set(x['id'] for x in rows)), 'contagens':payload['contagens']}))
