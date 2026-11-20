"""Registra nova pesquisa sem alterar documentos ou evidências de revisões anteriores."""
import collections
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as E
import zipfile

os.environ['PYTHONIOENCODING'] = 'utf-8'
root = Path(__file__).resolve().parents[2]
task = Path(__file__).resolve().parent
out = task / 'rodada2'
out.mkdir(exist_ok=True)
base = json.loads(subprocess.check_output([sys.executable, str(root / 'Scripts/versao_monografia.py'), 'atual', '--json'], cwd=root))
assert base['id'] == 'v010', 'Conferir nova vigente antes de atualizar esta rodada.'
doc = root / base['arquivo']
sha = hashlib.sha256(doc.read_bytes()).hexdigest()
assert sha == base['sha256'] == '1da5ea82344c177d75af723362017e3e558bbb127bd9995f7ec0cbd6964f81ed'
ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
tree = E.fromstring(zipfile.ZipFile(doc).read('word/document.xml'))
matrices = []
for table in tree.findall('.//w:tbl', ns):
    rows = [[''.join(t.text or '' for t in c.findall('.//w:t', ns)) for c in tr.findall('w:tc', ns)] for tr in table.findall('w:tr', ns)]
    if len(rows) == 35 and len(rows[0]) == 6:
        matrices.append(rows)
assert len(matrices) == 1
old = json.loads((task / 'decisoes_41_em_consolidacao.json').read_text(encoding='utf-8'))['decisoes']
pending = []
for i, row in enumerate(matrices[0][1:], 1):
    for j, value in enumerate(row[1:], 1):
        if value != '?':
            continue
        entry = next(x for x in old if x['linha_word'] == i and x['dimensao'] == f'P{j}')
        assert entry['autor'] == row[0] and entry['proposta'] == '?'
        pdf = root / entry['pdf']
        assert hashlib.sha256(pdf.read_bytes()).hexdigest() == entry['sha256_pdf']
        pending.append({k: entry[k] for k in ['id', 'linha_word', 'autor', 'dimensao', 'pdf', 'sha256_pdf', 'localizador', 'sintese']})
assert len(pending) == 38

notes = [
    {'id': 'D15', 'dimensoes': ['P4'], 'alcance': 'Nova leitura do texto das nove páginas da versão local Scholarpedia, revisão 196567, inclusive referências e identificação da revisão.',
     'achado': 'O exemplo é um gerador de frequência, e as afirmações de desempenho são qualitativas. Não apresenta tabela nem números de contraste com LSTM/GRU/Transformer. A referência Evolino (2007) é listada, mas seus números não são reproduzidos aqui. Não transferir para Jaeger a comparação localizada em Millea.',
     'decisao': 'Mantido ?. Nenhuma evidência numérica qualificadora no texto integral consultado. O suplemento do gerador já foi lido na rodada anterior.'},
    {'id': 'D22', 'dimensoes': ['P1', 'P4'], 'alcance': 'Nova leitura do texto das 11 páginas, inclusive método, tabelas 1–5, conclusões e referências.',
     'achado': 'P1: pesos descritos como aleatórios/fixos; matriz de conectividade, tanh e ajuste de escala não individualizam lei dos elementos de Win/W. P4: LSTM aparece na revisão e nas referências 8/32, mas tabelas 2–5 comparam Lorenz e variantes ESN, sem arquitetura qualificadora. As tabelas 4 e 5 das páginas posteriores também foram verificadas no texto.',
     'decisao': 'Dois ? mantidos. Não apresentar resultados de obras citadas como se fossem números comparativos deste artigo.'},
    {'id': 'D16', 'dimensoes': ['P1'], 'alcance': 'PDF 11–14; célula 11 do código público já arquivada; fontes oficiais de ReservoirPy em 19 etiquetas de lançamento/pré-lançamento até novembro de 2024.',
     'achado': 'O notebook importa Reservoir de reservoirpy.nodes e não passa W/Win locais ao construtor. As 19 assinaturas conferidas usam W normal e Win Bernoulli simétrica (nomes antigos generate_internal_weights/generate_input_weights na série 0.3.0). Os respectivos geradores foram arquivados por etiqueta. Isso recupera o comportamento das versões públicas consultadas, mas não fixa o ambiente efetivamente usado por Kumar.',
     'decisao': 'Mantido ?. A inferência sobre os padrões públicos da biblioteca deve ficar identificada como condicional. Não atribuir distribuição uniforme ao modelo nem certificar a versão da execução. Próxima análise: distinguir documentação do exemplo público de prova da configuração histórica, conforme o protocolo já adotado.'},
    {'id': 'D26', 'dimensoes': ['P1', 'P2', 'P3'], 'alcance': 'Nova leitura do texto das 12 páginas, incluindo referências. Fluxograma da Figura 2 (PDF 4, impressa 512) e configuração da página 6 (impressa 514) conferidos visualmente.',
     'achado': 'P1: pesos descritos como aleatórios, sem família. P2: fixados 500 neurônios, raio 0.999 e esparsidade 0.02, sem procedimento de seleção. P3: coleta/limpeza aparece no fluxo, mas não há operação especificada; seleção do fechamento e partições não demonstram limpeza ou transformação. O fluxograma visível não contém operação adicional oculta na extração.',
     'decisao': 'Três ? mantidos após ampliar a conferência para todo o texto local. Não inventar operação a partir de diferenças numéricas entre tabelas.'},
    {'id': 'D21', 'dimensoes': ['P3', 'P4', 'P5'], 'alcance': 'Nova leitura integral do texto das duas páginas, inclusive dez referências.',
     'achado': 'Comunicação conceitual, sem dados identificados, preparação aplicada ou comparação numérica qualificadora. Os estudos listados nas referências são obras distintas; seus resultados não são resultados apresentados nesta comunicação.',
     'decisao': 'Três ? mantidos. Não há uma experiência incompleta do TCC a realizar para preencher estas células; faltam informações na obra examinada.'},
    {'id': 'D30', 'dimensoes': ['P4'], 'alcance': 'PDF local 1, 2, 17 e 25; tabelas 3/4 da página 17 conferidas visualmente; HTML da editora. Fonte de apoio Pagliaro (2025): seção 6.1.4, PDF/impressa 13, e referências da página 46; busca textual nas 48 páginas para 72/90 seguidos de percentual.',
     'achado': 'As tabelas 3 e 4 listam métricas e vantagens, sem resultados numéricos comparáveis. A referência 10 de Vishwas é Pagliaro; a menção a Hong como [10] no corpo é inconsistente com sua própria lista. Pagliaro atribui 72% a Google/horizonte de cinco dias e discute CNN em outra obra; não foi localizado 90% pela busca textual. Essa leitura não comprova contraste comum 72% versus 90%. Não é leitura integral nova de Pagliaro.',
     'decisao': 'Mantido ?. Retificar o localizador anterior: não existe uma Tabela 17 nesse ponto; são tabelas 3 e 4 na página 17. Preservar o relatório histórico e registrar esta retificação no novo relatório.'},
    {'id': 'D19', 'dimensoes': ['P3', 'P5'], 'alcance': 'Páginas 1–6, 48–49 e passagens de 64–80; busca dirigida por normalização, reescala, Forex, moedas e negociação no texto. PDF oficial de Groningen consultado, com 90 páginas, correspondente à estrutura local.',
     'achado': 'As alterações de feedback/matriz e o ruído de estado não são preparação da série. O resumo menciona Forex, mas o texto examinado e o sumário não identificam par de moedas/ativo de uma análise financeira. Um artigo posterior do mesmo autor, sobre Forex, é outra obra e não preenche automaticamente o campo da dissertação.',
     'decisao': 'Dois ? mantidos no escopo lido. Não declarar leitura integral das 90 páginas; persistem alternativas documentais a conferir.'},
    {'id': 'D02', 'dimensoes': ['P1', 'P4'], 'alcance': 'Páginas 1–9 da prova local; busca externa por título/código.',
     'achado': 'A descrição das cinco famílias e dos hiperparâmetros não individualiza sua geração em Win/W. A busca não forneceu um código do estudo com procedência demonstrada. Os scripts locais do TCC recebidos do orientador não têm ligação documental estabelecida com as execuções do artigo de Araújo.',
     'decisao': 'Dois ? mantidos. Não transportar a distribuição dos scripts do TCC para o artigo.'},
    {'id': 'D08', 'dimensoes': ['P1'], 'alcance': 'Texto das páginas 7–8 e 12–14.',
     'achado': 'Win/Wres/Wenc aleatórias e fixas; IS/SR escalonam as matrizes. Filtro gaussiano é aplicado à tensão, não define geração dos pesos.', 'decisao': 'Mantido ?.'},
    {'id': 'D27', 'dimensoes': ['P1'], 'alcance': 'Texto das páginas 1–5, incluindo método e passos SSA–ESN.',
     'achado': 'Famílias normais e sinais ±1 pertencem a Q/beta/A da SSA. Passo 3 apenas manda gerar Win/W aleatoriamente; não vincula essas famílias aos pesos.', 'decisao': 'Mantido ?.'},
    {'id': 'D34', 'dimensoes': ['P1', 'P2'], 'alcance': 'Texto das páginas 6–9, algoritmo OMP e configuração.',
     'achado': 'A matriz gaussiana é Phi de medição. OMP seleciona átomos e atualiza resíduos; a configuração fixa compressão de 50% e demais parâmetros. Não foi identificado procedimento de escolha dos hiperparâmetros da ESN nessas páginas.', 'decisao': 'Dois ? mantidos.'},
    {'id': 'D24', 'dimensoes': ['P3'], 'alcance': 'Busca em todo o texto por normalização, pré-processamento, escala, janelas e padronização; leitura das passagens recuperadas.',
     'achado': 'Escalas de entradas/saídas são listadas como parâmetros; normalização sináptica descreve conexões da rede. Nenhuma dessas passagens individualiza uma operação aplicada de preparação temporal.', 'decisao': 'Mantido ?. Busca lexical não é leitura integral nova.'},
    {'id': 'D03', 'dimensoes': ['P4'], 'alcance': 'Busca por LSTM/GRU/Transformer em todo o PDF e por referência 187 no corpo; passagens das páginas 21 e 48.',
     'achado': 'LSTM aparece no título da referência 187. A chamada no corpo integra uma enumeração de variantes IPSO, sem números de contraste com a arquitetura.', 'decisao': 'Mantido ?. Não atribuir a esta revisão uma tabela numérica da obra referenciada.'},
]
reviewed = sum(len(x['dimensoes']) for x in notes)
assert reviewed == 21
manifest = []
for p in sorted((task / 'suplementos/historico_reservoirpy').glob('*')):
    if p.is_file():
        manifest.append({'arquivo': str(p.relative_to(root)), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()})
data = {'base': base['id'], 'sha256_base': sha, 'word_alterado': False, 'insuficiencias_na_vigente': 38,
        'busca_integral_concluida': False, 'celulas_com_escopo_ampliado_nesta_rodada': reviewed,
        'leitura_textual_integral_nova': ['D15: 9 páginas', 'D21: 2 páginas', 'D22: 11 páginas', 'D26: 12 páginas'],
        'leituras': notes, 'pendentes_na_vigente': pending, 'manifesto_codigo_oficial': manifest,
        'limites': ['Os arquivos de código foram apenas lidos; nenhum notebook, treino, GA ou DM executado.',
                   'Sem edição do Word: não criar versão v011 por esta auditoria.',
                   'Nenhuma das 38 células recebeu nova classificação aprovada nesta rodada.']}
(out / 'evidencias.json').write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
lines = ['# Continuação da pesquisa das lacunas — rodada 2', '', f"Versão examinada: **{base['id']}**, SHA256 `{sha}`.", '',
         f'A rodada anterior foi progresso: três respostas foram incorporadas na v010. Nesta rodada, foram ampliadas as evidências de {reviewed} células em {len(notes)} fontes. Nenhuma recebeu nova classificação suficiente para editar o Word. As 38 células permanecem; a meta integral está ativa.', '',
         'Houve nova leitura do texto integral de Jaeger (9 páginas), Ping (2 páginas), Seddik (11 páginas) e Sun (12 páginas); as demais leituras têm alcance delimitado abaixo. Não se apresenta busca lexical como leitura integral, nem detalhes de biblioteca como configuração histórica certificada.', '']
for n in notes:
    lines += [f"## {n['id']} / {', '.join(n['dimensoes'])}", '', '**Alcance:** '+n['alcance'], '', '**Evidência:** '+n['achado'], '', '**Decisão:** '+n['decisao'], '']
lines += ['## Fontes complementares preservadas', '',
          '- Código oficial de ReservoirPy em 19 etiquetas até novembro de 2024, com geradores e hashes: `suplementos/historico_reservoirpy/`. Não é uma cópia do ambiente original de Kumar.',
          '- Pagliaro (2025), DOI 10.3390/electronics14091721, PDF da editora e hash em `suplementos/Pagliaro_procedencia.json`. Apoio ao rastreio da referência 10 de Vishwas; não é um novo item do portfólio.',
          '- Imagens de conferência: `visuais/Sun_p4.png`, `visuais/Sun_p6.png`, `visuais/Vishwas_p17.png` e `visuais/Pagliaro_p13.png`.', '',
          '## O que ainda impede preencher cada campo', '',
          'P1 exige lei ligada a Win/W, não apenas a palavra aleatório. P2 exige como os valores foram selecionados. P3 exige operação de preparação aplicada. P4 exige comparação quantitativa identificável com as arquiteturas previstas pelo critério; a mera existência de LSTM na bibliografia não atende. P5 exige mercado e ativo ligados à análise.', '',
          'Se a publicação não especifica a informação, preencher com um resultado de outra obra ou inventar um experimento alteraria a pesquisa. A indisponibilidade deve permanecer documentada. A leitura integral nova de Sun e Ping restringe a lacuna à informação não fornecida no texto, sem provar inexistência universal de material complementar.', '',
          '| Fonte | Campos ainda insuficientes |', '|---|---|']
groups = collections.defaultdict(list)
for x in pending:
    groups[x['autor']].append(x['dimensao'])
for author, dims in groups.items():
    lines.append(f"| {author} | {', '.join(dims)} |")
lines += ['', '## Continuidade', '',
          'Priorizar conferência integral dos textos ainda lidos parcialmente e respectivas figuras/suplementos; começar pelos resultados completos de Araújo, Timbó e Zhang. Jaeger, Seddik, Ping e Sun tiveram texto integral lido nesta rodada; as células neles ainda não se fecham. Em Kumar, a lei nos padrões públicos consultados foi recuperada, mas o ambiente efetivamente usado não foi identificado: manter essa distinção na decisão. Não alterar os critérios para eliminar sinais. Não repetir experimentos. Consultar a vigente antes de qualquer incorporação.', '',
          'A auditoria não depende de confirmação intermediária do autor. Não há processo de download/exportação ainda em execução. Não foi estabelecido bloqueio repetido da meta integral.', '']
(out / 'relatorio.md').write_text('\n'.join(lines), encoding='utf-8')
print(json.dumps({'base':base['id'], 'celulas_reexaminadas':reviewed, 'fontes':len(notes), 'insuficientes':38, 'novos_codigos':len(manifest)}, ensure_ascii=False))
