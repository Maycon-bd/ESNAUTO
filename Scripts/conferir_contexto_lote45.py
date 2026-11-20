"""Confronta estudos de mercado, RNR e inicialização com trechos atuais."""
import hashlib,json
from pathlib import Path
from docx import Document
root=Path(__file__).resolve().parents[1];out=root/'reports/fechamento_integral_20261029';doc=root/'reports/monografia/trabalho/fechamento_integral_20261029.docx';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert sha(doc)=='4c9110f8995438f956f965db10ae5f26391c91f45757322758c1e4c83a6f2742'
idx=json.loads((out/'indice_citacoes_atuais_lote44.json').read_text(encoding='utf8'));refs={r['id']:r for r in idx['registros']};D=Document(doc)
items=[
 (183,'R46','Vishwas, Usha e Sangeetha (2025)','PDF 1, 3–4 e 12–16','Revisão discute ruído, não estacionariedade, sobreajuste, interpretabilidade, custos e infraestrutura em cenários financeiros; questões são qualitativas e referem-se a vários estudos.'),
 (185,'R37','Ping (2023)','PDF 1–2, aplicações e conclusão','Relata usos de previsões de volatilidade em gestão de risco, precificação de opções e alocação. Não demonstra rentabilidade da previsão do fechamento de PETR4.'),
 (192,'R42','Sudiatmika e Putra (2024)','PDF 2–3, seção 2.1','Descreve memória recorrente e dependência de estados e entradas anteriores. O parágrafo preserva a ressalva sobre dependências longas.'),
 (194,'R42','Sudiatmika e Putra (2024)','PDF 3–4 e 7–8','Descreve portas de LSTM e GRU; eficiência e sequências curtas são mencionadas na discussão de trabalhos anteriores. Resultados próprios de ouro são de erro, não medições de tempo.'),
 (196,'R46','Vishwas, Usha e Sangeetha (2025)','PDF 4 e 11–16','A revisão apresenta desafios qualitativos de custo, infraestrutura e latência; não sustenta proibição universal de LSTM/GRU por retropropagação.'),
 (211,'R23','Hariharan, Suresh e Chandrasekar (2025)','PDF 2–4, 8–10 e 16–17','Grupos de reservatório correspondem a variáveis e permitem conexões entre grupos, com variação entre topologias; inclui dados de NIFTYBEES. Não estabelece domínio universal.'),
 (216,'R34','Millea (2014)','PDF 10, 20–21 e 28–31, Tabela 3.3','Analisa matrizes ortonormais e aleatórias reescaladas em problema MSO; testes da Tabela 3.3 dependem do limiar de erro; conectividade e tamanho também são discutidos.'),
 (223,'R34','Millea (2014)','PDF 10 e 28–31','Experimentos de inicialização em séries MSO não quantificam frequência de distribuições em pesquisas financeiras.'),
 (238,'R13','Cortesi et al. (2026)','PDF 17–18, descrição dos dados e cfacpr','Tabela lista fator de ajuste por eventos corporativos nos dados CRSP. A existência desse campo, por si, não identifica uso efetivo da coluna ajustada para cada variável.'),
 (257,'R46','Vishwas, Usha e Sangeetha (2025)','PDF 4, 11–16','Custo e infraestrutura aparecem na revisão como desafios; a distinção entre busca e ajuste é critério de análise próprio da monografia, não medição importada da revisão.')]
rows=[]
for p,r,anchor,loc,e in items:
 t=D.paragraphs[p].text;assert anchor in t;ref=refs[r];assert sha(root/ref['arquivo_fonte'])==ref['sha256_fonte'];rows.append({'ancora':f'P_atual{p:04}','texto_atual':t,'referencia':r,'fonte_id':ref['fonte_id'],'arquivo_fonte':ref['arquivo_fonte'],'sha256_fonte':ref['sha256_fonte'],'localizador':loc,'evidencia':e,'diagnostico':'condizente na afirmação delimitada'})
f=out/'afirmacoes_contexto_lote45.json';assert not f.exists();f.write_text(json.dumps({'base':'v005','sha256_base':'2af31abca4e3ba9fd5caf7cd161e55472dc94edc136cdf89732c0d0401118d6b','sha256_rascunho':sha(doc),'registros':rows,'limite':'Confronto dos trechos delimitados, com uso das leituras e páginas primárias identificadas; demais afirmações compostas exigem evidência própria.','acao':'Nenhuma edição adicional nesses pontos.'},ensure_ascii=False,indent=2)+'\n',encoding='utf8');s=out/'estado_meta.json';state=json.loads(s.read_text(encoding='utf8'));state['ultimo_registro_de_leitura']=str(f.relative_to(root));state['proxima_passagem']='Confrontar demais citações metodológicas e requisitos qualitativos do Guia.';s.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print('10 relações com fontes registradas.')
