from pathlib import Path
import hashlib,json,os,subprocess,sys
B=Path(__file__).resolve().parent;R=B.parents[1]
cli=[sys.executable,str(R/'Scripts/versao_monografia.py')]
def run(args):return subprocess.run(cli+args,cwd=R,check=True,capture_output=True,encoding='utf-8',env={**os.environ,'PYTHONIOENCODING':'utf-8'}).stdout
current=json.loads(run(['atual','--json']));assert current['id']=='v013','Conciliar: base avançou.'
proof=json.loads((B/'conferencia_final.json').read_text(encoding='utf-8'))
work=R/'reports/monografia/trabalho/sumario_links_20261102.docx'
assert hashlib.sha256(work.read_bytes()).hexdigest()==proof['trabalho_sha256']
assert proof['paginas_diferentes']==[],proof['paginas_diferentes']
assert len(list((B/'render_final').glob('page-*.png')))==81
report=f'''# Links internos do sumário

Base editorial v013, SHA256 `{current['sha256']}`. Cópia conferida SHA256 `{proof['trabalho_sha256']}`. Revisão em 2 de novembro de 2026.

O usuário relatou que clicar nas entradas não abria as páginas respectivas. A auditoria da v013 confirmou zero elementos hyperlink e zero campos de sumário: títulos e páginas eram texto estático. Foram adicionados 42 hyperlinks internos, um por entrada do sumário, e 42 marcadores exclusivos nos títulos de destino. Referências e abertura de anexos também estão vinculadas. Os títulos repetidos de análise inferencial foram associados às respectivas entradas pela ordem e título, com páginas conferidas no Word.

Não foi alterado o texto, a numeração, a aparência ou a posição das entradas. Não foram adicionados botões, barras de navegação ou links visíveis extras. As listas de figuras, quadros e tabelas não fazem parte desta alteração. O sumário continua com paginação estática: futuras mudanças de conteúdo exigem conferir seus números novamente.

Validação funcional: o Word abriu a cópia somente para leitura e executou Hyperlink.Follow em cada um dos 42 links. Para todos, o início da seleção coincidiu com o marcador esperado e a página impressa coincidiu com a entrada. Resultados em teste_links_word.json; destinos em links.json. O documento foi fechado sem salvar alterações feitas pelo Word.

Validação estrutural: somente word/document.xml foi alterado. A remoção dos novos links/marcadores recupera exatamente o XML original; texto, propriedades e 15 tabelas preservados. Os 81 localizadores anteriores mantêm a paginação. São 81 páginas renderizadas com corpo e cabeçalho pixel a pixel idênticos à v013. As páginas do sumário foram inspecionadas após renderização para confirmar aparência preservada. O renderizador da skill de documentos processou as imagens atuais do Word; os PDFs por imagem são QA interno, não entrega PDF textual.

Uso: no Word em modo de edição, normalmente Ctrl + clique segue o link. O comportamento de um visualizador de prévia pode ser diferente. A validação funcional foi realizada no Word local, sem certificar o comportamento de todos os aplicativos ou conversores de PDF. Não houve experimentos nem alteração de conteúdo científico, e permanecem as pendências da base.
'''
(B/'relatorio.md').write_text(report,encoding='utf-8')
args=['registrar','--arquivo',str(work),'--base','v013','--responsavel','Codex para Maycon Garcia Silva','--resumo','Adiciona links internos às 42 entradas do sumário, inclusive referências e anexos. Corrige navegação antes inexistente; preserva conteúdo, aparência e paginação.','--estado','em_revisao','--validacao','42 hyperlinks seguidos no Word e conferidos por marcador e página de destino. 81 páginas renderizadas, todas pixel a pixel idênticas à v013; páginas do sumário inspecionadas. 81 localizadores, texto e 15 tabelas preservados. Só navegação interna adicionada em document.xml. Validação funcional no Word, sem certificação de outros visualizadores.']
for n in ['relatorio.md','conferencia_final.json','estrutura.json','links.json','teste_links_word.json']:args+=['--evidencia',str(B/n)]
(B/'registro_saida.txt').write_text(run(args),encoding='utf-8')
final=json.loads(run(['atual','--json']));assert final['anterior']=='v013' and final['sha256']==proof['trabalho_sha256']
assert hashlib.sha256(Path(final['caminho_absoluto']).read_bytes()).hexdigest()==final['sha256']
(B/'versao_entregue.json').write_text(json.dumps(final,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:final[k] for k in ['id','arquivo','sha256']},ensure_ascii=False))
