from pathlib import Path
import hashlib, json, os, subprocess, sys

B = Path(__file__).resolve().parent
R = B.parents[1]
cli = [sys.executable, str(R / 'Scripts/versao_monografia.py')]
def run(args):
    return subprocess.run(cli + args, cwd=R, check=True, capture_output=True,
                          encoding='utf-8', env={**os.environ, 'PYTHONIOENCODING': 'utf-8'}).stdout
current = json.loads(run(['atual', '--json']))
assert current['id'] == 'v011', 'Conciliar: vigente avançou.'
proof = json.loads((B / 'conferencia_final.json').read_text(encoding='utf-8'))
work = R / 'reports/monografia/trabalho/declaracao_ia_reescrita_20261102.docx'
assert hashlib.sha256(work.read_bytes()).hexdigest() == proof['trabalho_sha256']
assert proof['paginas_a_inspecionar'] == [43, 81]
visual = {
    'candidato_sha256': proof['trabalho_sha256'],
    'paginas_renderizadas': 81, 'paginas_inspecionadas': [43, 81],
    'paginas_pixel_a_pixel_identicas_a_base': 79,
    'declaracao_separada': 'Uma página renderizada e inspecionada.',
    'resultado': 'Sem cortes, sobreposição ou quebra da declaração. Somente script está em itálico no parágrafo novo.'
}
(B / 'inspecao_visual.json').write_text(json.dumps(visual, ensure_ascii=False, indent=2), encoding='utf-8')
report = f'''# Reescrita da declaração de responsabilidade coletiva

Data: 2026-11-02. Base v011: `{current['sha256']}`.
Cópia conferida: `reports/monografia/trabalho/declaracao_ia_reescrita_20261102.docx`, SHA256 `{proof['trabalho_sha256']}`.

O autor pediu redação diferente da declaração do colega e informou: “Modelos usados sempre foram do Claude Opus 5.5 e do Codex foi o Sol 5.6”. Esses nomes foram registrados como relato do autor, sem inferência de identificadores de API ou verificação independente por logs. A informação anterior “Somente Codex nos testes” foi mantida. Gemini 2.5 Flash, temperatura 0, continua associado à extração por script Python.

Foram reescritos os dois parágrafos de responsabilidade e as descrições das quatro atividades, ferramentas, finalidades e conferências humanas. A estrutura de quatro colunas, os compromissos de responsabilidade humana e respeito à integridade e aos direitos de terceiros, os nomes dos declarantes e os campos de data/assinatura foram preservados. A reescrita dos parágrafos institucionais é uma adaptação expressamente solicitada pelo autor: não é transcrição literal do formulário fornecido nem aprovação de sua aceitação institucional. A referência à Portaria foi mantida do formulário, sem auditoria jurídica nesta tarefa.

O parágrafo de 3.1 foi ajustado para refletir os modelos informados. O Anexo A e a declaração separada têm a mesma redação substantiva. A nova redação registra a conferência de artigos pelo autor e as correções textuais do orientador, sem atribuir ao orientador execução de testes ou validações técnicas não informadas.

## Conferências realizadas

Somente `word/document.xml` mudou na monografia. A comparação de todos os elementos de corpo identifica quatro elementos alterados: parágrafo de 3.1, dois parágrafos de abertura da declaração e sua tabela. Os outros elementos, incluindo as 14 tabelas científicas, permanecem idênticos em XML. Os resultados e as referências não foram alterados. Não foram repetidos treinamentos, buscas genéticas ou testes DM.

O Word repaginou a cópia em 81 páginas. Todos os 81 localizadores registrados (incluindo entradas das listas) preservaram título e paginação. As 81 páginas foram renderizadas; 79 imagens são idênticas à v011. As duas páginas diferentes, físicas 43 e 81 (impressas 42 e 80), foram inspecionadas, assim como a declaração separada de uma página. Não há cortes ou sobreposições, e os campos de assinatura cabem na página. O itálico do parágrafo metodológico ficou restrito à palavra script após correção na iteração de QA. As imagens foram processadas também pelo renderizador da skill de documentos, usando a renderização atual do Word como origem.

Evidências finais: `conferencia_final.json`, `inspecao_visual.json`, `alteracoes.json`; imagens em `word_final`, `render_final` e `render_decl`. PDFs por imagem são intermediários internos de QA, não uma edição PDF textual para entrega.

## Pendências e alcance

A identificação dos modelos não é mais desconhecida: foi preenchida conforme o relato do autor. Data e assinaturas continuam vazias para os declarantes. As demais limitações científicas e formalidades registradas na base permanecem; esta revisão pontual não é nova auditoria integral de fontes ou do Guia nem certificação de integridade/autoria por IA.

Fontes de apresentação: Anexo 14 fornecido em Downloads, modelo na página 4; Guia FASOFT em `output/skills-docx/GUIA-FASOFT-UniRV.pdf`, abertura e identificação de anexo nas páginas 65–66. O arquivo do colega é somente exemplo histórico; não fornece ferramentas ou validações para Maycon.
'''
(B / 'relatorio.md').write_text(report, encoding='utf-8')
pending = [p for p in current['pendencias'] if not p.startswith('Declaração de uso de IAG preenchida')]
pending.append('Declaração de IAG reescrita a pedido do autor, com Claude Opus 5.5 e Codex Sol 5.6 informados por ele; somente Codex nos testes. Data e assinaturas do autor e orientador permanecem em branco. Redação adaptada do modelo institucional, sem aprovação institucional nesta revisão.')
args = ['registrar', '--arquivo', str(work), '--base', 'v011', '--responsavel', 'Codex para Maycon Garcia Silva',
        '--resumo', 'Reescreve declaração de responsabilidade coletiva e suas descrições conforme pedido do autor; informa Claude Opus 5.5 e Codex Sol 5.6, superando a pendência anterior de modelos desconhecidos. Atualiza indicação em 3.1. Preserva resultados, referências e paginação.',
        '--estado', 'em_revisao', '--validacao',
        '81 páginas renderizadas; 79 imagens idênticas à v011 e duas páginas alteradas inspecionadas. Declaração separada de uma página renderizada e inspecionada. 81 localizadores com paginação preservada; 14 tabelas científicas e demais elementos fora de quatro alterações preservados em XML. Modelos conforme relato do autor; sem novos experimentos ou aprovação institucional.']
for name in ['relatorio.md', 'conferencia_final.json', 'inspecao_visual.json', 'alteracoes.json']:
    args += ['--evidencia', str(B / name)]
for p in pending: args += ['--pendencia', p]
result = run(args)
(B / 'registro_saida.txt').write_text(result, encoding='utf-8')
final = json.loads(run(['atual', '--json']))
assert final['anterior'] == 'v011' and final['sha256'] == proof['trabalho_sha256']
assert hashlib.sha256(Path(final['caminho_absoluto']).read_bytes()).hexdigest() == final['sha256']
(B / 'versao_entregue.json').write_text(json.dumps(final, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({k: final[k] for k in ['id', 'arquivo', 'sha256']}, ensure_ascii=False))
