"""Registra conferência dirigida de quatro referências sem alterar o Word."""
import hashlib
import json
from pathlib import Path
from docx import Document

root = Path(__file__).resolve().parents[1]
out = root / 'reports/fechamento_integral_20261029'
docx = root / 'reports/monografia/trabalho/fechamento_integral_20261029.docx'
digest = hashlib.sha256(docx.read_bytes()).hexdigest()
assert digest == 'fb5e2653547af740b586a95aee3d93259745df36ebc4f7c61c7cd2047b3a1ce7'
paragraphs = Document(docx).paragraphs
assert 'McKay, Beckman e Conover (1979)' in paragraphs[325].text
assert 'Eshelman (1991)' in paragraphs[326].text
assert 'Pagani; Kovaleski; Resende, 2015' in paragraphs[360].text
data = {
 'base': 'v005', 'sha256_base': '2af31abca4e3ba9fd5caf7cd161e55472dc94edc136cdf89732c0d0401118d6b',
 'sha256_rascunho': digest, 'escopo': 'Conferência dirigida dos trechos explicitamente associados às quatro fontes; não é leitura integral nem validação da auditoria como um todo.',
 'fontes': [
  {'id':'R33', 'fonte':'McKay, Beckman e Conover (1979)', 'ancora': paragraphs[325].text,
   'evidencia':'Artigo original, p. 239–240, introdução e seção 2; método divide cada distribuição marginal em estratos equiprováveis, sorteia um valor por estrato e combina as componentes aleatoriamente.',
   'url':'https://www.stat.cmu.edu/technometrics/70-79/VOL-21-02/v2102239.pdf',
   'diagnostico':'A atribuição do LHS e sua denominação são condizentes com o trecho original. A afirmação de uso no trabalho exige também evidência experimental própria.',
   'alcance':'Páginas 239–240 e conclusão p. 243 lidas; restante do artigo não conferido nesta passagem.',
   'aplicacao_no_projeto':'app/utils/ga_engine.R, gerar_populacao_lhs: estratifica cinco componentes por permutação com jitter e arredonda para codificação binária. O código atual não prova sozinho o mecanismo utilizado em cada execução histórica; verificação histórica separada.'},
  {'id':'R36', 'fonte':'Pagani, Kovaleski e Resende (2015)', 'ancora': paragraphs[360].text,
   'evidencia':'Resumo do artigo no site da editora: o Methodi Ordinatio combina seleção e ranqueamento pelo índice InOrdinatio; usa fator de impacto, ano e citações.',
   'url':'https://link.springer.com/article/10.1007/s11192-015-1744-x',
   'diagnostico':'A referência identifica o método. A descrição de como foi considerado na pesquisa e das limitações da planilha é uma afirmação própria, dependente dos registros locais e do relato do autor; a fonte não prova sua aplicação neste projeto.',
   'alcance':'Metadados e resumo da editora; texto integral não lido nesta passagem.'},
  {'id':'R21', 'fonte':'Eshelman (1991)', 'ancora': paragraphs[326].text,
   'evidencia':'Patente que identifica Eshelman como um dos inventores e nomeia o capítulo de 1991 descreve CHC e mutação diante de convergência ou estagnação.',
   'url':'https://patents.justia.com/patent/5390283',
   'diagnostico':'A relação geral com CHC encontra apoio em documento primário posterior do inventor; o texto corretamente diz que o mecanismo do trabalho é inspirado e não implementa o CHC completo. A implementação concreta deve ser conferida nos registros históricos.',
   'alcance':'Fonte primária posterior, não o capítulo original de 1991; validação da atribuição ao capítulo permanece parcial.'},
  {'id':'R26', 'fonte':'Holland (1975)', 'ancora': paragraphs[325].text,
   'evidencia':'Descrição do livro no editor da reedição identifica Holland e seu papel fundacional em algoritmos genéticos; fonte não permite verificar integralmente a edição de 1975.',
   'url':'https://doi.org/10.7551/MITPRESS/1090.001.0001',
   'diagnostico':'A atribuição geral é plausível e apoiada pela descrição editorial; permanece parcial até exame da obra de 1975 ou excerto pertinente.',
   'alcance':'Descrição editorial da reedição, não leitura do livro citado.'}
 ],
 'similaridade':'Os trechos conferidos são curtas atribuições em português e descrições próprias de metodologia; não foi identificado trecho literal extenso dessas quatro fontes. Isso não constitui verificação global ou certificação de ausência de plágio.',
 'acao':'Nenhuma alteração textual necessária com base nos trechos consultados; manter limites de acesso à fonte e de evidência histórica como pendências explícitas.',
}
path = out/'conferencia_metodologia_lote26.json'
assert not path.exists()
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
statepath=out/'estado_meta.json'; state=json.loads(statepath.read_text(encoding='utf-8'))
state['ultimo_registro_de_leitura']=str(path.relative_to(root)); state['proxima_passagem']='Conferir registros primários do uso histórico de LHS e cataclismo; continuar fontes suplementares e reconciliar inventário por afirmação.'
statepath.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(path)
