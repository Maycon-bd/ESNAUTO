"""Confronta afirmações correntes com obras de redes recorrentes e ESN."""
import hashlib,json
from pathlib import Path
from docx import Document

root=Path(__file__).resolve().parents[1]; out=root/'reports/fechamento_integral_20261029'; doc=root/'reports/monografia/trabalho/fechamento_integral_20261029.docx'; sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(doc)=='63ca3ec4031dafe5a78b6785f2a5d7581f5deacc461c9096c392dedc5963b62e'
idx=json.loads((out/'indice_citacoes_atuais_lote36.json').read_text(encoding='utf8')); refs={r['id']:r for r in idx['registros']}; D=Document(doc)
supp={'R12':('reports/fechamento_integral_20261029/fontes_suplementares/Cho_2014_EMNLP.pdf','c948d89ccd33da2a48421b45445f1c30f5fe677a829af9e5e1b6f9ff75a14a81'),'R25':('reports/fechamento_integral_20261029/fontes_suplementares/Hochreiter_Schmidhuber_1997_copia_autor.pdf','51e319ebc53b96964bc167faa3a45d02eca61964eb7ed6bbc1cb2e70517064f2'),'R27':('reports/fechamento_integral_20261029/fontes_suplementares/Jaeger_2001_errata_2010.pdf','0a0296f586f86a0e49e651e4581ce2aef3a926ca9cb3d57653c8963b7b83e625')}
items=[
 (193,'R25','Hochreiter e Schmidhuber (1997)','PDF 1 e 6; resumo, introdução e seção 4','A cópia do coautor apresenta o problema das dependências longas, fluxo constante de erro, células de memória e portas de entrada/saída; não se atribui porta de esquecimento à publicação original.'),
 (193,'R12','Cho et al. (2014)','PDF 2–3, seções 2.2–2.3','O codificador–decodificador usa unidade com portas reset e update. A observação sobre ausência de garantia financeira é delimitação da monografia, não resultado atribuído à fonte.'),
 (203,'R27','Jaeger (2001)','PDF 3, resumo, e seções de aprendizagem por regressão','O relatório, na cópia com errata de 2010, apresenta algoritmo que ajusta conexões de saída a partir dos estados da rede recorrente.'),
 (203,'R28','Jaeger (2007)','PDF 1–2','Reservatório recorrente aleatório e fixo fornece respostas combinadas por saída treinável. A referência local é captura de revisão posterior do artigo Scholarpedia de 2007.'),
 (204,'R28','Jaeger, 2007','PDF 2–5','Descrição de regressão da saída, regularização e alternativas de treinamento. Redução do número de parâmetros treináveis e ausência de garantia de tempos universais são delimitadas como interpretação do texto atual.'),
 (257,'R28','Jaeger, 2007','PDF 1–2 e 5','O contraste entre saída treinável e abordagens que ajustam outras conexões é consistente; o texto evita traduzir isso como tempo universal ou estabilidade garantida.'),
 (200,'R29','Kumar (2025)','PDF 16–18, Tabela 3','Comparação própria de ARIMA, LSTM, GRU e RC para preços de petróleo; resultados numéricos pertencem ao protocolo da fonte, não implicam domínio em todas as métricas.'),
 (205,'R43','Sun et al. (2021)','PDF 5–6 e 8, Tabela 3','A fonte utiliza Kweichow Moutai e compara ESN com LSTM simplificada; apresenta colunas close e adjusted close, mas texto descreve fechamento sem comprovação inequívoca do uso da coluna ajustada.'),
 (212,'R24','Hassaan, Yacoub e Said (2025)','PDF 4–5 e 12–13, Tabela 2','Seis conjuntos financeiros e comparação entre ESN/GRU com métodos caóticos e não caóticos; métricas não identificam efeito isolado de uma lei probabilística.'),
 (212,'R39','Seddik, Routaib e Elhaddadi (2023)','PDF 4–7','Condições iniciais vinculadas a Bitcoin alimentam trajetórias de Lorenz; a página 7 menciona série decimada sem detalhar o procedimento. Não equivale a previsão direta do preço observado.'),
 (233,'R24','Hassaan, Yacoub e Said (2025)','PDF 7–8, Equações 9a/9b e Figura 4','As fórmulas representam He com randn e Xavier com rand uniforme reescalado; figura e texto seguinte descrevem Xavier de modo não coincidente. A monografia explicita a divergência.'),
 (251,'R24','Hassaan, Yacoub e Said (2025)','PDF 4–8 e 12–13','O estudo inclui dados financeiros e os sistemas citados; comparações permanecem vinculadas às condições do próprio artigo.'),
 (252,'R24','Hassaan, Yacoub e Said (2025)','PDF 7–8 e 13, Equações 9a/9b e Tabela 2','Valores reportados não são tratados como teste de significância ou efeito isolado; ressalva sobre Xavier corresponde à divergência identificada.'),
 (256,'R24','Hassaan, Yacoub e Said (2025)','PDF 12–13 e Tabela 2','A comparação ESN/GRU é própria do protocolo, sem autorização para concluir superioridade universal.'),
 (256,'R29','Kumar (2025)','PDF 16–18 e Tabela 3','RC, LSTM e GRU são comparados em petróleo; os tempos e métricas não são transferidos para o protocolo da monografia.'),
 (256,'R43','Sun et al. (2021)','PDF 5–8 e Tabela 3','Comparação própria com LSTM simplificada, limitada à configuração e ao conjunto examinados.')]
rows=[]
for p,r,anchor,loc,ev in items:
 text=D.paragraphs[p].text; assert anchor in text,(p,r)
 ref=refs[r]
 if r in supp: path,expected=supp[r]; sid='suplementar'
 else:path,expected,sid=ref['arquivo_fonte'],ref['sha256_fonte'],ref['fonte_id']
 assert sha(root/path)==expected
 rows.append({'ancora':f'P_atual{p:04}','texto_atual':text,'referencia':r,'fonte_id':sid,'arquivo_fonte':path,'sha256_fonte':expected,'localizador':loc,'evidencia':ev,'diagnostico':'condizente no escopo identificado'})
f=out/'afirmacoes_fundamentos_lote36.json'; assert not f.exists()
f.write_text(json.dumps({'base':'v005','sha256_base':'2af31abca4e3ba9fd5caf7cd161e55472dc94edc136cdf89732c0d0401118d6b','sha256_rascunho':sha(doc),'alcance':'16 relações de afirmação e fonte; parte das leituras reutiliza evidências anteriores com identidade de fonte e contexto verificados. Afirmações adicionais nos mesmos parágrafos permanecem sujeitas à conferência separada.','registros':rows,'acao':'Nenhuma edição adicional nos trechos examinados.'},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
s=out/'estado_meta.json';state=json.loads(s.read_text(encoding='utf8'));state['ultimo_registro_de_leitura']=str(f.relative_to(root));state['proxima_passagem']='Continuar confronto das afirmações restantes por fonte, e revisar requisitos do Guia na versão atual.';s.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print('16 relações registradas.')
