"""Registra confronto pontual de afirmações sobre distribuições financeiras."""
import hashlib,json
from pathlib import Path
from docx import Document

root=Path(__file__).resolve().parents[1]; out=root/'reports/fechamento_integral_20261029'
doc=root/'reports/monografia/trabalho/fechamento_integral_20261029.docx'; sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(doc)=='ee6e179ab0ba157fb9f1348a1ac75c38813be767c3a27367481727f59641af50'
D=Document(doc); idx=json.loads((out/'indice_citacoes_atuais_lote32.json').read_text(encoding='utf8'))
defs=[
 {'p':224,'referencia':'R35','fonte':'D20','fragmento':'caudas pesadas em retornos financeiros','localizador':'PDF 7–8, páginas impressas 352–353, e PDF 9, página impressa 354','evidencia':'Nelson descreve GED com caudas maiores ou menores que a Normal e usa GED para a inovação na modelagem de retornos e volatilidade de um índice. O restante do parágrafo separa essa evidência da hipótese própria sobre pesos de ESN.','diagnostico':'condizente com escopo e distinção registrados'},
 {'p':225,'referencia':'R35','fonte':'D20','fragmento':'Nelson (1991) empregou','localizador':'PDF 7–9, páginas impressas 352–354','evidencia':'A seção 2 descreve a GED e caudas; a seção 3 usa a GED em modelo de variância condicional e retornos de mercado. A fonte não é tomada como prova de aplicação da GED em pesos de ESN.','diagnostico':'condizente'},
 {'p':227,'referencia':'R19','fonte':'D10','fragmento':'Duttilo e Gattone (2022)','localizador':'PDF 1–2 e 4–5, introdução, aplicação empírica e Tabela 1, página impressa 1368','evidencia':'O resumo identifica DJIA entre 2016 e janeiro de 2022 e mistura de duas GED; introdução e Tabela 1 comparam duas Gaussianas, Gaussiana-Laplace e duas GED por verossimilhança e critérios, incluindo AIC, BIC e HQIC.','diagnostico':'condizente com o estudo e comparadores'},
 {'p':228,'referencia':'R01','fonte':'D01','fragmento':'Abebe e Goshu (2024)','localizador':'PDF 1–2 e 12, Tabelas 6–8','evidencia':'O artigo apresenta AGED; as três tabelas exibem AIC e BIC menores para AGED que para GED e Normal nos conjuntos de dados analisados. As conclusões se restringem aos três conjuntos.','diagnostico':'condizente quanto à família e aos critérios informados; não generalizar outros indicadores'},
 {'p':229,'referencia':'R16','fonte':'D09','fragmento':'Dewick (2022)','localizador':'PDF 2, 9–10 e 14, seções 2, 4 e conclusões','evidencia':'O texto trata de distribuições financeiras e modelagem de séries; o parágrafo evita atribuir ao artigo uma justificativa automática de distribuição para pesos de ESN.','diagnostico':'condizente quanto à atribuição a Dewick; afirmação sobre Soltani depende de sua própria conferência'}]
refs={r['id']:r for r in idx['registros']}; rows=[]
for d in defs:
 p=D.paragraphs[d['p']].text; assert d['fragmento'] in p
 ref=refs[d['referencia']]; assert ref['fonte_id']==d['fonte']
 source=root/ref['arquivo_fonte']; assert sha(source)==ref['sha256_fonte']
 rows.append({'ancora':f"P_atual{d['p']:04}",'texto_atual':p,'fonte_id':d['fonte'],'arquivo_fonte':ref['arquivo_fonte'],'sha256_fonte':sha(source),'localizador':d['localizador'],'evidencia':d['evidencia'],'diagnostico':d['diagnostico']})
f=out/'afirmacoes_distribuicoes_lote33.json'; assert not f.exists()
f.write_text(json.dumps({'base':'v005','sha256_base':'2af31abca4e3ba9fd5caf7cd161e55472dc94edc136cdf89732c0d0401118d6b','sha256_rascunho':sha(doc),'escopo':'Cinco parágrafos e quatro fontes; conferência dirigida dos trechos identificados com fonte local e limites. Não classifica os demais contextos nem valida toda a monografia.','registros':rows,'acao':'Nenhuma correção adicional identificada nos trechos examinados.'},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
s=out/'estado_meta.json'; state=json.loads(s.read_text(encoding='utf8')); state['ultimo_registro_de_leitura']=str(f.relative_to(root)); state['proxima_passagem']='Continuar conferência dos contextos do índice, incluindo Soltani no mesmo parágrafo e demais fontes; revalidar Guia.'; s.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf8'); print('Registradas cinco afirmações com fonte, página e limites.')
