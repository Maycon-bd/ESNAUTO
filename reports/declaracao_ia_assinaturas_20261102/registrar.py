from pathlib import Path
import hashlib,json,os,subprocess,sys
B=Path(__file__).resolve().parent;R=B.parents[1]
cli=[sys.executable,str(R/'Scripts/versao_monografia.py')]
def run(args):return subprocess.run(cli+args,cwd=R,check=True,capture_output=True,encoding='utf-8',env={**os.environ,'PYTHONIOENCODING':'utf-8'}).stdout
current=json.loads(run(['atual','--json']));assert current['id']=='v012','Conciliar: base avançou.'
proof=json.loads((B/'conferencia_final.json').read_text(encoding='utf-8'))
work=R/'reports/monografia/trabalho/declaracao_ia_assinaturas_20261102.docx'
assert hashlib.sha256(work.read_bytes()).hexdigest()==proof['trabalho_sha256']
assert (B/'render_final/page-81.png').exists() and (B/'render_decl/page-1.png').exists()
report=f'''# Data e espaço para assinaturas da declaração

Revisão de 2 de novembro de 2026. Base v012, SHA256 `{current['sha256']}`. Cópia de trabalho conferida, SHA256 `{proof['trabalho_sha256']}`.

Atendidos os dois comentários do autor: data da declaração preenchida como “Rio Verde/GO, 2 de novembro de 2026.” e espaço anterior a cada linha de assinatura ampliado de 14 para 48 pontos. A data segue o contexto de horário do cliente America/Sao_Paulo. O mesmo ajuste foi aplicado à declaração separada. Atendido também o comentário posterior para retirar as referências à elaboração de slides e roteiro. Os espaços destinam-se ao posicionamento das assinaturas pelo gov.br; nenhuma assinatura foi aplicada, simulada ou certificada.

Somente word/document.xml mudou. Quatro elementos de corpo foram alterados: data, duas linhas de assinatura e a tabela da declaração. Nesta tabela, somente duas células foram reescritas para remover slides e roteiro e manter apenas a formatação da monografia e verificações documentais por scripts. As outras 14 tabelas permanecem idênticas em XML. O texto científico e os resultados não foram alterados; não foram executados experimentos.

O Word manteve 81 páginas e os 81 localizadores com a mesma paginação. As 81 páginas foram renderizadas: 80 imagens são idênticas à v012; apenas a página física 81 (impressa 80) mudou. A página alterada e a declaração separada de uma página foram inspecionadas após renderização. A disposição mantém espaço acima das duas linhas, sem cortes ou sobreposições; os nomes e campos de assinatura cabem na mesma página. O renderizador da skill de documentos também processou as imagens atuais do Word. Os PDFs por imagem são somente intermediários internos de QA.

Evidência estrutural em conferencia_final.json e alterações em alteracoes.json; imagens em word_final, render_final e render_decl. Data preenchida não equivale à assinatura nem à data de aprovação da monografia. Assinaturas permanecem a cargo dos declarantes e as demais pendências da base são preservadas. Sem nova auditoria integral de conteúdo ou formatação institucional.
'''
(B/'relatorio.md').write_text(report,encoding='utf-8')
pending=[]
for p in current['pendencias']:
 if p.startswith('Declaração de IAG reescrita'):
  p=p.replace('Data e assinaturas do autor e orientador permanecem em branco.','Data preenchida em 2 de novembro de 2026; assinaturas do autor e orientador permanecem em branco, com espaço ampliado.')
 pending.append(p)
args=['registrar','--arquivo',str(work),'--base','v012','--responsavel','Codex para Maycon Garcia Silva','--resumo','Preenche a data da declaração de IAG em 2 de novembro de 2026 e amplia o espaço antes das duas assinaturas de 14 para 48 pontos, atendendo aos comentários do autor. Retira da declaração a elaboração de slides e roteiro. Conteúdo científico e paginação preservados.','--estado','em_revisao','--validacao','81 páginas renderizadas; 80 imagens idênticas à v012 e somente página 81 alterada, inspecionada. Declaração separada de uma página inspecionada. 81 localizadores com paginação preservada; 14 tabelas e demais elementos fora da data, duas linhas de assinatura e duas células da declaração idênticos em XML. Sem assinatura aplicada ou aprovação institucional.']
for n in ['relatorio.md','conferencia_final.json','alteracoes.json']:args+=['--evidencia',str(B/n)]
for p in pending:args+=['--pendencia',p]
result=run(args);(B/'registro_saida.txt').write_text(result,encoding='utf-8')
final=json.loads(run(['atual','--json']));assert final['anterior']=='v012' and final['sha256']==proof['trabalho_sha256']
assert hashlib.sha256(Path(final['caminho_absoluto']).read_bytes()).hexdigest()==final['sha256']
(B/'versao_entregue.json').write_text(json.dumps(final,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:final[k] for k in ['id','arquivo','sha256']},ensure_ascii=False))
