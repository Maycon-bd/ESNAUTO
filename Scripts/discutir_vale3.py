"""Consolida evidências auditadas e insere a extensão VALE3 em cópia da monografia."""
from pathlib import Path
from copy import deepcopy
import json, hashlib
import pandas as pd
import numpy as np
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]/'reports/vale3_comparacao/python_deps'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from docx import Document
from docx.text.paragraph import Paragraph
from docx.oxml import OxmlElement
from docx.shared import Cm, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reports/vale3_comparacao'
SOURCE=ROOT/'reports/monografia/MayconGarciaSilva_monografia_bibliometria_VALE3.docx'
DEST=SOURCE.with_name('MayconGarciaSilva_monografia_resultados_VALE3.docx')
t=pd.read_csv(OUT/'execucoes_auditadas.csv')
b=pd.read_csv(OUT/'escalas_e_persistencia.csv').set_index('acao')
order=[('Normal','Normal'),('Uniforme','Uniforme'),('GED','Uniforme'),('GED','Normal')]
labels=[f'{x} × {y}' for x,y in order]
t['cenario']=t.Win+' × '+t.W
g=t.groupby('cenario').agg(MAE_media=('MAE_teste','mean'),MAE_dp=('MAE_teste','std'),
    RMSE_media=('RMSE_teste','mean'),RMSE_dp=('RMSE_teste','std'),NMAE_media=('NMAE_pct','mean'),
    NMAE_dp=('NMAE_pct','std'),valida_media=('MAE_valida','mean'),tempo_medio=('tempo_s','mean')).reindex(labels)
g.to_csv(OUT/'resumo_distribuicoes.csv')
best=t.loc[t.fitness.idxmax()]
assert len(t)==12 and t.groupby('cenario').size().eq(3).all()
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10})
fig,axs=plt.subplots(1,2,figsize=(10,3.5),layout='constrained')
for ax,key,title in zip(axs,['MAE_valida','MAE_teste'],['Validação','Teste']):
    for i,label in enumerate(labels):
        vals=t.loc[t.cenario==label,key].to_numpy()
        ax.scatter(i+np.array([-.12,0,.12]),vals,s=38,color='#25638c')
        ax.plot([i-.2,i+.2],[vals.mean()]*2,color='#111111',lw=2)
    ax.set_xticks(range(4),['Normal\nNormal','Uniforme\nUniforme','GED\nUniforme','GED\nNormal'])
    ax.set_title(title);ax.set_ylabel('MAE');ax.grid(axis='y',alpha=.25)
axs[1].axhline(b.loc['VALE3','MAE_persistencia'],color='#a84c24',ls='--',label='Persistência')
axs[1].legend(fontsize=8)
fig.savefig(OUT/'fig5_variacao_rodadas.png',dpi=200);fig.savefig(OUT/'fig5_variacao_rodadas.pdf');plt.close(fig)
p=pd.read_csv(OUT/f'{best.id}_previsoes.csv')
fig,axs=plt.subplots(2,1,figsize=(9,4.3),sharex=True,layout='constrained',gridspec_kw={'height_ratios':[2,1]})
axs[0].plot(p.indice,p.real,color='#1b1b1b',lw=1,label='Observado')
axs[0].plot(p.indice,p.previsto,color='#287ca3',lw=.85,alpha=.8,label='Previsto')
axs[0].set_ylabel('Preço com fator');axs[0].legend(ncol=2,fontsize=9)
axs[1].plot(p.indice,p.erro,color='#a84c24',lw=.8);axs[1].axhline(0,color='black',lw=.5)
axs[1].set_ylabel('Erro');axs[1].set_xlabel('Índice da observação na série VALE3')
for ax in axs:ax.grid(alpha=.2)
fig.savefig(OUT/'fig6_previsao_selecao_fitness.png',dpi=200);fig.savefig(OUT/'fig6_previsao_selecao_fitness.pdf');plt.close(fig)

fmt=lambda x,n=6:f'{x:.{n}f}'.replace('.',',')
paragraphs=[
 'A extensão experimental para VALE3 compreendeu 12 execuções adicionais de ESN, realizadas entre 12 e 13 de outubro de 2026: Normal × Normal, Uniforme × Uniforme, GED × Uniforme e GED × Normal, com três sementes distintas por combinação. As 45 execuções históricas de PETR4 permanecem como estudo principal; a extensão não reproduz as cinco ondas nem inclui novos experimentos LSTM ou GRU.',
 'Foi empregado o motor atual do ESNAUTO, com população de 10 indivíduos, inicialização LHS, mutação cataclísmica, limite de 10.000 gerações e parada após 3.500 gerações sem melhora. A função objetivo maximiza o negativo da soma ponderada de MAE de treino (40%) e validação (60%). Os pesos e hiperparâmetros foram otimizados para VALE3; os parâmetros dos geradores foram mantidos: Normal com média zero e desvio padrão um, Uniforme em [−1, 1] e GED com média 14,573152, desvio padrão 8,032086 e forma 7,686645. A GED foi utilizada como configuração fixa de transferência do projeto, sem nova estimação na VALE3.',
 'A série de 5.192 valores foi dividida em 2.596 observações de treino, 1.298 de validação e 1.298 de teste. A avaliação de um passo à frente preservou o procedimento do motor: 1.297 pares no teste, com uso do valor observado anterior como entrada. O primeiro ponto do bloco de teste não integra a métrica. O estado do reservatório é reconstruído no treino e a avaliação passa ao teste sem percorrer o bloco de validação; esta convenção deve ser considerada na reprodução e na comparação. Não foram atribuídas datas às observações, pois o arquivo de entrada não contém uma coluna de datas.',
 f'As execuções atingiram entre {int(t.geracoes.min()):,} e {int(t.geracoes.max()):,} gerações, totalizando {fmt(t.tempo_s.sum()/3600,2)} horas de busca genética. As sementes, matrizes Win, W e Wout, objetos do GA, previsões e métricas foram preservados por rodada. O salvamento entre cenários permite retomar os pendentes após interrupções; ele não recupera uma geração interrompida dentro de uma rodada.',
 'A Tabela 10 apresenta média e desvio padrão amostral das três rodadas por combinação. A Figura 5 mostra cada execução, evitando que a média oculte resultados discrepantes. As diferenças são descritivas: três rodadas não sustentam, por si, conclusões de superioridade estatística.',
 f'Normal × Normal apresentou MAE médio de teste de {fmt(g.loc[labels[0],"MAE_media"])} e desvio padrão de {fmt(g.loc[labels[0],"MAE_dp"])}. GED × Uniforme apresentou MAE médio de {fmt(g.loc[labels[2],"MAE_media"])} e desvio padrão de {fmt(g.loc[labels[2],"MAE_dp"])}. Na terceira rodada desta combinação, o MAE de teste foi 4,359181 e o R² foi 0,801793, apesar de MAE de validação de 0,409615. Essa execução foi mantida na análise. O contraste evidencia que validação próxima não assegurou estabilidade fora da amostra; a causa específica exige investigação adicional.',
 f'A escolha pelo maior fitness de treino/validação selecionou GED × Uniforme na primeira rodada, semente {int(best.seed)}, com a = {fmt(best.a)}, raio espectral = {fmt(best.sr)}, lavagem de {int(best.initLen)} passos, {int(best.Nx)} neurônios e regularização {best.reg:.6e}. Seu MAE de validação foi {fmt(best.MAE_valida)} e o MAE de teste foi {fmt(best.MAE_teste)}. A Figura 6 apresenta suas previsões e resíduos. Normal × Normal teve menor erro médio no teste, mas esse resultado é uma observação posterior, e não um critério de seleção aplicado antes do teste.',
 f'Para contextualizar o desempenho, foi calculada uma previsão de persistência, na qual o próximo preço previsto é igual ao último observado, sobre os mesmos 1.297 pares. Seu MAE foi {fmt(b.loc["VALE3","MAE_persistencia"])} e RMSE foi {fmt(b.loc["VALE3","RMSE_persistencia"])}. Nenhuma das 12 execuções de ESN apresentou MAE de teste inferior ao dessa referência. Portanto, os R² elevados nas demais rodadas não demonstram ganho preditivo sobre a persistência, especialmente em séries de preços em nível.',
 f'Para a comparação descritiva entre ativos, definiu-se NMAE = 100 × MAE / média dos módulos dos preços observados no teste. As médias utilizadas foram {fmt(b.loc["PETR4","media_teste"])} para PETR4 e {fmt(b.loc["VALE3","media_teste"])} para VALE3. O controle histórico Normal × Normal da PETR4, GA_RUN_0046, apresentou MAE de 0,328365, equivalente a NMAE de {fmt(100*.328365/b.loc["PETR4","media_teste"],3)}%. Para Normal × Normal da VALE3, o NMAE médio foi {fmt(g.loc[labels[0],"NMAE_media"],3)}%. A diferença entre os MAEs absolutos reflete parcialmente as escalas dos preços; esses valores normalizados não constituem evidência de que um ativo seja mais previsível.',
 'A comparação utiliza o controle de produção Normal × Normal da PETR4, com uma execução histórica, e três rodadas da VALE3, sem pareamento de sementes ou alinhamento diário demonstrado. Resultados legados de 200 gerações e outro motor não integram as médias. A ausência de registros equivalentes para os demais pares impede uma comparação controlada entre ativos. As conclusões sobre LSTM e GRU permanecem restritas à PETR4; não foram realizados testes de significância entre ações.'
]
(OUT/'discussao_resultados.md').write_text('# Resultados da extensão VALE3\n\n'+'\n\n'.join(paragraphs)+'\n\n'+g.to_string(),encoding='utf-8')
d=Document(SOURCE);original=list(d.paragraphs);source_hash=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
def replace(p,text):
    props=deepcopy(p.runs[0]._r.rPr) if p.runs and p.runs[0]._r.rPr is not None else None
    p.clear();r=p.add_run(text)
    if props is not None:r._r.insert(0,props)
replace(original[400],'A seleção da ação foi integrada à interface Shiny e à execução em lote, com resultados separados por ativo. Além das verificações funcionais, foi realizada uma extensão experimental com 12 execuções de ESN na VALE3, em quatro combinações de distribuições e três rodadas por combinação. Seus resultados são discutidos na Seção 4.11. As cinco ondas históricas, os baselines LSTM/GRU e a análise inferencial anterior permanecem referentes à PETR4.')
replace(original[525],original[525].text.replace('As verificações funcionais dessa extensão demonstram o funcionamento do fluxo de seleção, mas não estabelecem desempenho preditivo na VALE3.','A extensão experimental para VALE3 preservou integralmente os resultados de 12 execuções de ESN, permitindo avaliar desempenho e variação entre rodadas no segundo ativo.'))
replace(original[539],'A avaliação foi ampliada com 12 execuções de ESN na VALE3. Essa extensão cobre quatro combinações e três rodadas por combinação, sem repetir integralmente as cinco ondas da PETR4 ou os baselines LSTM/GRU. A ausência de datas na série VALE3, o número limitado de ativos e de repetições e a falta de pareamento das execuções históricas restringem a generalização. A comparação normalizada e a referência de persistência complementam a análise, sem estabelecer superioridade estatística entre ativos.')
for p in original:
    if p.text.startswith('A avaliação experimental considera um único ativo'):
        replace(p,p.text.replace('A avaliação experimental considera um único ativo, a PETR4','O estudo principal considera a PETR4'))
replace(original[545],'Como continuidade experimental, propõe-se ampliar a VALE3 às demais ondas e aos baselines LSTM e GRU, com maior número de sementes e alinhamento temporal auditável. Os parâmetros de distribuições ajustados à PETR4, inclusive na Onda 5, requerem nova estimação somente no treino da VALE3 ou identificação explícita como transferência. Também se recomenda investigar a rodada discrepante GED × Uniforme e a sensibilidade à saturação do reservatório, preservando o resultado observado e avaliando mudanças em um novo protocolo.')
replace(original[551],original[551].text.replace('permanecendo pendente a avaliação experimental completa da VALE3.','com avaliação complementar de 12 execuções da ESN na VALE3. Essa extensão identificou variação entre rodadas e não apresentou ganho de MAE sobre a persistência no teste; a avaliação das demais distribuições e de LSTM/GRU no segundo ativo permanece como continuidade.'))
anchor=original[527]
def before(text='',style='Normal'):
    el=OxmlElement('w:p');anchor._p.addprevious(el);p=Paragraph(el,anchor._parent);p.style=style
    if style=='Normal' and original[526]._p.pPr is not None:p._p.insert(0,deepcopy(original[526]._p.pPr))
    p.add_run(text)
    for r in p.runs:r.font.name='Times New Roman';r.font.size=Pt(12)
    p.paragraph_format.widow_control=True
    return p
h=before('EXTENSÃO EXPERIMENTAL PARA VALE3 E COMPARAÇÃO COM PETR4','SEÇÃO TCC')
for txt in paragraphs[:5]:before(txt)
before('Tabela 10 – Resultados de teste da VALE3 por combinação de distribuições','Caption').paragraph_format.keep_with_next=True
table=d.add_table(rows=1,cols=4);table.autofit=False
anchor._p.addprevious(table._tbl)
for c,txt in zip(table.rows[0].cells,['Win × W','MAE média ± DP','RMSE média ± DP','NMAE médio (%)']):c.text=txt
for label in labels:
    row=table.add_row().cells;r=g.loc[label]
    for c,txt in zip(row,[label,f'{fmt(r.MAE_media)} ± {fmt(r.MAE_dp)}',f'{fmt(r.RMSE_media)} ± {fmt(r.RMSE_dp)}',fmt(r.NMAE_media,3)]):c.text=txt
for row in table.rows:
    for c in row.cells:
        for p in c.paragraphs:
            p.alignment=WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.first_line_indent=Cm(0)
            p.paragraph_format.space_after=Pt(3);p.paragraph_format.space_before=Pt(3)
            for r in p.runs:r.font.name='Times New Roman';r.font.size=Pt(10)
        borders=OxmlElement('w:tcBorders')
        for side in ['top','left','bottom','right']:
            e=OxmlElement('w:'+side);e.set('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val','single');e.set('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}sz','4');e.set('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}color','D9D9D9');borders.append(e)
        c._tc.get_or_add_tcPr().append(borders)
for c in table.rows[0].cells:
    sh=OxmlElement('w:shd');sh.set('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}fill','E8EDF2');c._tc.get_or_add_tcPr().append(sh)
    for r in c.paragraphs[0].runs:r.bold=True
before('Fonte: Elaborado pelo autor (2026). DP: desvio padrão amostral; três rodadas por combinação. NMAE normalizado pela média dos módulos dos preços observados no teste.').paragraph_format.first_line_indent=Cm(0)
captions=['Figura 5 – Variação dos erros entre as rodadas da VALE3','Figura 6 – Previsões e resíduos da VALE3 na execução selecionada pelo fitness']
def figure(cap,path):
    p=before(cap,'Caption');p.paragraph_format.keep_with_next=True
    p=before();p.paragraph_format.first_line_indent=Cm(0);p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    p.add_run().add_picture(str(path),width=Cm(15));p.paragraph_format.keep_with_next=True
    p=before('Fonte: Elaborado pelo autor (2026).');p.paragraph_format.first_line_indent=Cm(0)
figure(captions[0],OUT/'fig5_variacao_rodadas.png')
for txt in paragraphs[5:7]:before(txt)
figure(captions[1],OUT/'fig6_previsao_selecao_fitness.png')
for txt in paragraphs[7:]:before(txt)
# Acrescenta entradas às listas estáticas existentes; Word atualizará a paginação.
def list_entry(template,text):
    el=deepcopy(template._p);template._p.addnext(el);p=Paragraph(el,template._parent);replace(p,text);return p
f4=next(p for p in original if p.text.startswith('Figura 4') and '\t' in p.text)
f5=list_entry(f4,captions[0]+'\t0');list_entry(f5,captions[1]+'\t0')
tab9=next(p for p in original if p.text.startswith('Tabela 9') and '\t' in p.text)
list_entry(tab9,'Tabela 10 – Resultados de teste da VALE3 por combinação de distribuições\t0')
toc=next(p for p in original if p.text.startswith('4.10') and '\t' in p.text)
list_entry(toc,'4.11\tEXTENSÃO EXPERIMENTAL PARA VALE3 E COMPARAÇÃO COM PETR4\t0')
d.save(DEST)
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==source_hash
audit={'original_preservado':True,'source_sha256':source_hash,'execucoes':12,'figuras':len(d.inline_shapes),'documento':str(DEST),'selecionado_por_fitness':str(best.id),'horas_ga':float(t.tempo_s.sum()/3600)}
(OUT/'validacao_edicao.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
print(DEST)
