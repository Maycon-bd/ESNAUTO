from pathlib import Path
import hashlib,json
p=Path(__file__).resolve().parent;root=p.parents[1]
v=json.loads((p/'verificacao_estrutural.json').read_text(encoding='utf-8'))
c=json.loads((p/'comparacao_visual.json').read_text(encoding='utf-8'))
pag=json.loads((p/'paginacao_candidata.json').read_text(encoding='utf-8-sig'))
assert pag['pages']==c['paginas_total']==78
assert len(pag['titles'])==41 and len(pag['captions'])==19
inspected_pairs=[9,11,15,17,33,35,37,39,41,43,45,47,49,51,53,55,57,59,61,63,65,67,69,71,73,75,77]
inspected=sorted({x for n in inspected_pairs for x in [n,n+1]})
assert set(c['paginas_novas_ou_alteradas']).issubset(inspected)
qa={'sha256_docx':v['sha256_candidata'],'paginas_total':78,'paginas_inspecionadas_visualmente':inspected,'paginas_com_corpo_pixel_identico_a_base':[d['pagina'] for d in c['paginas'] if d['pagina_base_com_corpo_pixel_identico'] is not None],'cobertura':'Todas as páginas alteradas inspecionadas; demais páginas comparadas pixel a pixel excluindo cabeçalho.','resultado':'Sem cortes ou sobreposições observados. Figura1, três células, tabela de contagens, novo parágrafo e referências conferidos.','pdf_sha256':hashlib.sha256((p/'candidata.pdf').read_bytes()).hexdigest(),'fontes_visuais':['visuais/Millea_p30.png','visuais/Evolino_p16.png']}
(p/'inspecao_visual.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf-8')
report=f'''# Incorporação de três respostas documentadas

Base: v009, SHA256 `{v['sha256_base']}`.
Cópia revisada: `reports/monografia/trabalho/busca_lacunas_20261101.docx`, SHA256 `{v['sha256_candidata']}`.

## Resultado desta etapa

Foram substituídas três das41marcações da matriz. A busca integral solicitada pelo autor permanece em andamento:38células ainda não têm informação suficiente no escopo consultado. Esta entrega intermediária não afirma que todos os sinais foram preenchidos, que todas as fontes foram lidas integralmente nesta rodada ou que não existam alternativas documentais adicionais.

| Fonte e dimensão | Alteração | Sustentação |
|---|---|---|
| Jaeger2007/P1 | ? → D | Código oficial vinculado ao exemplo: Win uniforme em[-1,1); elementos não nulos deWgerados por sprand e deslocados por-0.5antes da normalização espectral. A matriz efetiva é transformada pelo reescalamento; não se confunde a lei inicial com a final. |
| Jaeger2007/P3 | ? → D | Código vinculado constrói canal de viés e canal de entrada e aplica transformações afins às sequências de entrada/alvo do gerador de frequência. Não é tratamento de preços financeiros. |
| Millea2014/P4 | ? → S | Os quatro NRMSE de Evolino na tabela3.1(0.00415,0.00804,0.110,0.166) coincidem com a tabela2de Schmidhuber et al.2007, p.772, que identifica PI-Evolino baseado emLSTM. É resultado importado, sem novo experimentoLSTM porMillea. Tabelas inspecionadas visualmente. |

O suplemento de Jaeger possui revisões posteriores ao artigo2007(inclui revisão2014e nota2015); essa condição está registrada. Sua inclusão documental foi explicitada na prosa. O arquivo foi apenas lido, sem execução. O trabalho original de Evolino e o suplemento verificam duas fontes existentes; não acrescentam itens à coleção de34documentos.

No repositório deKumar, matrizes locais uniformes são construídas mas não entregues ao objeto Reservoir que produz as previsões. Não foi atribuída essa lei ao modelo executado. A ausência de versão fixada da biblioteca mantém a insuficiência dessa célula.

## Conciliação do documento

Atualizados Quadro1, Tabela1, Figura1e o parágrafo de descrição de frequências. Incluídos o parágrafo que explicita o escopo complementar, o endereço do suplemento deJaeger e a referência original deEvolino. O gráfico foi gerado com fonteArial. As contagens foram recalculadas a partir das170células da v009, sem reutilizar totais históricos de versões antigas.

| Dimensão | Direta | Secundária | Insuficiente | Não aplicável |
|---|---:|---:|---:|---:|
| P1 |6|0|12|16|
| P2 |11|5|3|15|
| P3 |27|2|5|0|
| P4 |10|3|15|6|
| P5 |25|3|3|3|

## Verificações

O pacoteDOCX mudou somente em document.xml e na imagem daFigura1. Os14objetos de tabela permanecem, com alterações apenas nas duas tabelas bibliográficas; as outras12tabelas permanecem idênticas. As cinco outras imagens e o XML da introdução e dos capítulos3–6permanecem idênticos à base. As50referências anteriores foram preservadas(com endereço suplementar acrescido à entradaJaeger); há uma referência adicional, totalizando51. Não foram realizados experimentos, treinos, buscasGA ou testesDM.

O Word exportou78páginas. Os41títulos e19legendas foram medidos na paginação real. As60entradas do sumário e das listas foram conciliadas;48referências de página mudaram. As45páginas novas/alteradas foram inspecionadas visualmente, incluindo o fluxo posterior;33páginas têm corpo com pixels idênticos à exportação da v009, excluindo cabeçalho. Nenhum corte ou sobreposição foi observado. A Figura1e a notação matemática do parágrafo foram conferidas após preservar a formatação dos runs originais.

## Continuidade obrigatória

As38insuficiências permanecem listadas individualmente em `decisoes_41_em_consolidacao.json` e `relatorio_em_andamento.md`, com fonte, página e alcance. Falta concluir as alternativas pertinentes e distinguir informações recuperáveis de detalhes não especificados pelas publicações. A presença de um PDF não garante que ele contenha cada informação exigida pela matriz; não foram substituídas lacunas por suposições. A meta geral permanece ativa. Esta revisão não é aprovação acadêmica nem auditoria universal de todas as fontes.
'''
(p/'relatorio_incorporacao.md').write_text(report,encoding='utf-8')
print('Evidências da incorporação prontas; pesquisa geral continua.')
