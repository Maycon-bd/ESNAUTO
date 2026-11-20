from pathlib import Path
import hashlib,json,os,subprocess,sys
B=Path(__file__).resolve().parent;R=B.parents[1]
cli=[sys.executable,str(R/'Scripts/versao_monografia.py')]
def run(args):return subprocess.run(cli+args,cwd=R,check=True,capture_output=True,encoding='utf-8',env={**os.environ,'PYTHONIOENCODING':'utf-8'}).stdout
current=json.loads(run(['atual','--json']));assert current['id']=='v014','Conciliar: vigente avançou.'
proof=json.loads((B/'conferencia_final.json').read_text(encoding='utf-8'))
work=R/'reports/monografia/trabalho/listas_links_20261102.docx'
assert hashlib.sha256(work.read_bytes()).hexdigest()==proof['trabalho_sha256']
assert proof['paginas_diferentes']==[]
assert len(list((B/'render_final').glob('page-*.png')))==81
report=f'''# Links das listas de figuras, quadros e tabelas

Data: 2 de novembro de 2026. Base v014, SHA256 `{current['sha256']}`. Cópia conferida: `{proof['trabalho_sha256']}`.

Foram adicionados 19 hyperlinks internos nas listas: seis figuras, seis quadros e sete tabelas. Cada entrada completa aponta para um novo marcador na legenda correspondente. Os 42 links do sumário foram preservados. As referências visíveis, o conteúdo científico, a declaração e os números de página não foram alterados.

O Word abriu a cópia somente para leitura e executou Hyperlink.Follow nos 61 links: todos chegaram ao início do marcador correto e à página impressa indicada. O teste inclui os 19 links novos e os 42 anteriores. Destinos em links.json e resultados funcionais em teste_links_word.json. O Word foi fechado sem salvar.

A alteração está restrita a word/document.xml. Remover exclusivamente os 19 hyperlinks e marcadores novos recupera exatamente o XML da base. O texto e as 15 tabelas foram preservados; os 81 localizadores mantiveram a mesma paginação. Foram renderizadas 81 páginas, todas pixel a pixel idênticas à v014. As três páginas das listas (físicas 10, 11 e 12) foram inspecionadas após renderização; aparência preservada e sem defeito introduzido. O renderizador da skill de documentos processou as imagens atuais do Word. PDFs por imagem são apenas QA interno.

Conferência estrutural em estrutura.json e conferencia_final.json. No Word em edição, normalmente Ctrl + clique segue o link. A validação funcional é do Word local, sem certificação do comportamento de outros visualizadores ou conversores de PDF. A paginação das listas continua estática e deve ser conferida após futuras alterações editoriais. Não foram executados novos experimentos, treinamentos, buscas genéticas ou testes DM. Pendências científicas e institucionais herdadas da base permanecem.
'''
(B/'relatorio.md').write_text(report,encoding='utf-8')
args=['registrar','--arquivo',str(work),'--base','v014','--responsavel','Codex para Maycon Garcia Silva','--resumo','Adiciona 19 links internos às listas de figuras (6), quadros (6) e tabelas (7), preservando os 42 links do sumário. Conteúdo, aparência e paginação mantidos.','--estado','em_revisao','--validacao','61 hyperlinks seguidos no Word com marcador e página corretos, incluindo os 19 novos e os 42 do sumário. 81 páginas renderizadas, todas pixel a pixel idênticas à v014; páginas das listas inspecionadas. Texto, 15 tabelas e 81 localizadores preservados. Apenas navegação adicionada em document.xml. Validação funcional no Word, sem certificação de outros visualizadores.']
for n in ['relatorio.md','conferencia_final.json','estrutura.json','links.json','teste_links_word.json']:args+=['--evidencia',str(B/n)]
(B/'registro_saida.txt').write_text(run(args),encoding='utf-8')
final=json.loads(run(['atual','--json']));assert final['anterior']=='v014' and final['sha256']==proof['trabalho_sha256']
assert hashlib.sha256(Path(final['caminho_absoluto']).read_bytes()).hexdigest()==final['sha256']
(B/'versao_entregue.json').write_text(json.dumps(final,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:final[k] for k in ['id','arquivo','sha256']},ensure_ascii=False))
