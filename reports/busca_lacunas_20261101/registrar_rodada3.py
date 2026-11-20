"""Pesquisa documental: preserva Word e relatórios históricos, confere identidades."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

os.environ['PYTHONIOENCODING'] = 'utf-8'
root = Path(__file__).resolve().parents[2]
task = Path(__file__).resolve().parent
out = task / 'rodada3'
out.mkdir(exist_ok=True)
base = json.loads(subprocess.check_output([sys.executable, str(root / 'Scripts/versao_monografia.py'), 'atual', '--json'], cwd=root))
assert base['id'] == 'v010', 'Base avançou: conciliar antes de emitir diagnóstico.'
sha = hashlib.sha256((root / base['arquivo']).read_bytes()).hexdigest()
assert sha == base['sha256'] == '1da5ea82344c177d75af723362017e3e558bbb127bd9995f7ec0cbd6964f81ed'
previous = json.loads((task / 'rodada2/evidencias.json').read_text(encoding='utf-8'))
pending = previous['pendentes_na_vigente']
assert len(pending) == 38
sources = {x['id']: x for x in pending}
for x in sources.values():
    assert hashlib.sha256((root / x['pdf']).read_bytes()).hexdigest() == x['sha256_pdf']

notes = [
    {'id': 'D01', 'dimensoes': ['P3'], 'paginas_textuais_nesta_rodada': [9, 11, 13, 14],
     'cobertura_anterior': 'PDF integral já registrado no lote 14, com limitação da extração de fórmulas. Nesta rodada foram consultados também HTML oficial, Gjika/RPubs e arquivos originais do OSF.',
     'conclusao': 'A referência Cyber/heart failure está trocada entre as chamadas 44/45 do artigo. A página de Gjika explicitamente substitui zeros por 0.01 para ajuste da variável avg.report.length; não foi demonstrado que Abebe aplicou essa regra. O link OSF de Gjika aponta a uma figura, cujo projeto público contém o CSV original e dois Rmd. O CSV tem 366 semanas e três zeros. Retirar zeros e dividir por 100 produz 363 valores com Q1=3.985, mediana=5.1 e Q3=6.545, iguais à Tabela 5. A média calculada é 5.381322, contra 5.3810 publicado, e os momentos padronizados consultados não coincidem com os coeficientes da tabela. Essa concordância parcial não comprova uma receita histórica única. Rmd de terceiros foi apenas lido; nenhum modelo foi executado.',
     'visual': ['D01_p11.png'], 'decisao': 'Manter P3 como ?. Há evidência nova concreta sobre a origem e hipóteses de preparação; falta atribuir com segurança o procedimento realmente usado na amostra de 363 valores. Não contar tratamento de Gjika/Bakdash como operação executada por Abebe.'},
    {'id': 'D02', 'dimensoes': ['P1', 'P4'], 'paginas_textuais_nesta_rodada': list(range(10, 18)),
     'cobertura_anterior': 'PDF 1–9 lido na rodada 2; leitura integral histórica documentada no lote 6, com o mesmo hash.',
     'conclusao': 'As tabelas 1–4 comparam cinco famílias e fitness MAE/RMSE da ESN. A prosa e o fluxograma não ligam individualmente uma lei à geração dos elementos de Win/W. Não há contraste numérico com LSTM/GRU/Transformer nas tabelas e discussão. A referência 6 sobre GA-LSTM não é uma experiência apresentada no capítulo.',
     'visual': ['D02_p9.png'], 'decisao': 'Manter P1/P4 como ?. A leitura foi ampliada sem preencher informação que a prova local não explicita.'},
    {'id': 'D28', 'dimensoes': ['P4'], 'paginas_textuais_nesta_rodada': list(range(1, 12)),
     'cobertura_anterior': 'O lote 10 já documentava leitura integral deste mesmo PDF; esta rodada fez releitura sequencial.',
     'conclusao': 'O método usa regressão linear múltipla por mínimos quadrados. A função da Figura 2 é linear. A comparação da Figura 3 é previsão versus observado. A discussão compara ARIMA, fuzzy, AG e uma ANN não individualizada como arquitetura qualificadora; não apresenta comparação quantitativa com LSTM/GRU/Transformer. Não converter a sigla ANN em LSTM por hipótese.',
     'visual': ['D28_p7.png', 'D28_p9.png'], 'decisao': 'Manter P4 como ?.'},
    {'id': 'D34', 'dimensoes': ['P1', 'P2', 'P4'], 'paginas_textuais_nesta_rodada': list(range(1, 6)) + list(range(10, 16)),
     'cobertura_anterior': 'PDF 6–9 foi lido na rodada 2; o lote 13 já documentava as 15 páginas do mesmo PDF.',
     'conclusao': 'As Figuras 2 e 5 inicializam Win/W sem especificar família ou procedimento de seleção. O algoritmo OMP escolhe átomos para reconstrução; os experimentos fixam parâmetros e compressão de 50%, sem escolher esse valor por busca ou sensibilidade descrita. As tabelas 2/3 e os gráficos comparam ESN versus CS-ESN. Z-score/min-max são preparação dos dados; matriz gaussiana de medição e reescala de estados não são lei dos pesos.',
     'visual': ['D34_p4.png', 'D34_p5.png'], 'decisao': 'Manter três ?. Nenhum código qualificador localizado nos canais consultados; a busca negativa não prova inexistência universal.'},
    {'id': 'D30', 'dimensoes': ['P1', 'P4'], 'paginas_textuais_nesta_rodada': list(range(2, 17)) + list(range(18, 27)),
     'cobertura_anterior': 'Páginas 1 e 17 lidas integralmente na rodada 2; os blocos desta rodada completam o texto das 26 páginas. A Figura 1 e a Tabela 5 foram abertas visualmente.',
     'conclusao': 'As sugestões de pyESN/EsnTorch são possibilidades de implementação, sem vincular uma versão/código do estudo revisto à lei de Win/W. A taxonomia não contém resultados numéricos. Além dos 72%/90% já investigados, foi rastreada a afirmação de ganho de até 18% por HQNN (p.5,18,24) à referência 9. O resumo oficial indexado de Gandhudi descreve rede quântica híbrida com AG e conclui que a influência dos tweets é limitada; não confirma o ganho de 18% nem que se trate de um contraste quantitativo LSTM. Abertura direta da página retornou 403; esta conferência da fonte de apoio é parcial, sem leitura integral certificada.',
     'visual': ['D30_p9.png', 'D30_p18.png'], 'decisao': 'Manter P1/P4 como ?. Não aproveitar o percentual não confirmado apenas para eliminar a célula.'},
    {'id': 'D19', 'dimensoes': ['P3', 'P5'], 'paginas_textuais_nesta_rodada': list(range(84, 91)),
     'cobertura_anterior': 'Registro histórico do lote 21 lista leitura do corpo PDF 1–83. Houve nova leitura dirigida de método/resultados nas rodadas anteriores; esta rodada lê a bibliografia restante sem truncamento.',
     'conclusao': 'A bibliografia inclui Maciel et al. sobre câmbio, mas não identifica um ativo/par de moedas analisado pela própria dissertação. O resumo menciona Forex, enquanto o corpo examinado trabalha com MSO, Mackey-Glass, Sunspots e Laser. O artigo de Sarsa-ESN no site do autor é outra obra. Sua identificação de EURUSD não pode ser atribuída automaticamente à dissertação. As transformações da matriz e o ruído de estado não individualizam preparação da série.',
     'visual': [], 'decisao': 'Manter P3/P5 como ?. Não trocar a dissertação por artigo distinto sem registrar mudança de corpus.'},
]
reviewed = sum(len(x['dimensoes']) for x in notes)
assert reviewed == 11

history_map = {
    'D01': 'leituras_abebe_ribeiro_lote14_parcial.json',
    'D02': 'leitura_D02_araujo_lote6.json', 'D03': 'leitura_behera_concluida_lote20.json',
    'D07': 'leituras_costa_lunkes_lote15.json', 'D08': 'leituras_tian_deng_lote9.json',
    'D12': 'leituras_ecer_timbo_lote10.json', 'D13': 'leituras_liu_hariharan_xiao_lote12.json',
    'D15': 'leituras_fundamentos_lote3.json', 'D16': 'leitura_D16_kumar.json',
    'D17': 'leituras_liu_lin_rojas_lote19.json', 'D19': 'leitura_millea_lote21_parcial.json',
    'D22': 'leituras_chaos_lote4.json', 'D23': 'leituras_sharma_duttilo_lote7.json',
    'D24': 'leituras_dewick_nelson_soltani_lote8.json', 'D26': 'leitura_D26_sun.json',
    'D27': 'leituras_tian_deng_lote9.json', 'D28': 'leituras_ecer_timbo_lote10.json',
    'D29': 'leituras_ribeiro_wang_zhang_lote13.json', 'D30': 'conferencia_matriz_vishwas_lote31.json',
    'D31': 'leituras_wang_bu_huang_lote16.json', 'D34': 'leituras_ribeiro_wang_zhang_lote13.json',
}
history = []
for ident, source in sources.items():
    if ident in {'D15', 'D21', 'D22'}:
        p = task / 'rodada2/evidencias.json'
    else:
        p = root / 'reports/fechamento_integral_20261029' / history_map[ident]
    raw = p.read_bytes()
    j = json.loads(raw)
    # This tests source identity only; it is not an automatic test of human reading.
    assert source['sha256_pdf'] in json.dumps(j, ensure_ascii=False), (ident, p)
    history.append({'id': ident, 'autor': source['autor'], 'pdf': source['pdf'],
                    'sha256_pdf_confirmado': source['sha256_pdf'],
                    'registro_previo': str(p.relative_to(root)),
                    'sha256_registro': hashlib.sha256(raw).hexdigest(),
                    'limite': 'Registro de leitura/escopo anterior do mesmo PDF. Não converter esta conferência de identidade em nova leitura ou aprovação integral.'})
assert len(history) == 22

external = [
    {'fonte': 'Abebe e Goshu (2024)', 'url': 'https://www.frontiersin.org/journals/applied-mathematics-and-statistics/articles/10.3389/fams.2024.1398137/full',
     'alcance': 'Seção 8.2.1, Tabela 5 e referências 44/45 consultadas. A inconsistência das chamadas existe também no HTML oficial.'},
    {'fonte': 'Gjika (2021)', 'url': 'https://rpubs.com/Eraldagjika/715261',
     'alcance': 'Página e documento incorporado recuperados por HTTP público e arquivados por hash. Foram lidos início, importação, resumos, gráficos descritos e tratamento de zeros; feita busca dirigida no restante. Não se afirma leitura integral de todas as saídas de ajuste ou imagens. Nenhum R executado.'},
    {'fonte': 'OSF — dados e análises originais', 'url': 'https://osf.io/rq82a/',
     'alcance': 'Identidade do projeto recuperada pela API pública a partir do arquivo aj7vr. CSV e dois Rmd arquivados com procedência. Foram lidos o CSV por completo e os blocos de importação/preparação dos Rmd, sem executar os modelos. A aritmética descritiva de conferência foi registrada separadamente como reconstrução atual.'},
    {'fonte': 'Zhang (2021)', 'url': 'https://www.sciencedirect.com/science/article/pii/S1007570421001696',
     'alcance': 'Resultado oficial indexado consultado; abertura direta falhou. Conteúdo analisado provém do PDF local completo. Não foi recuperado suplemento qualificador na busca por título/DOI/código.'},
    {'fonte': 'Araújo (2025)', 'url': 'https://link.springer.com/chapter/10.1007/978-3-031-77738-7_26',
     'alcance': 'Página oficial consultada; não substitui a leitura da versão publicada integral pela prova local. Resultados genéricos de repositórios com MAE no nome não foram atribuídos aos autores.'},
    {'fonte': 'Timbó (2016)', 'url': 'https://aircconline.com/ijaia/V7N1/7116ijaia03.pdf',
     'alcance': 'PDF oficial localizado na busca; não há conteúdo novo recuperado que substitua a cópia local.'},
    {'fonte': 'Gandhudi et al. (2024)', 'doi': '10.1016/j.compeleceng.2024.109302',
     'url': 'https://www.sciencedirect.com/science/article/pii/S0045790624002301',
     'alcance': 'Resumo e prévia indexados da página da editora consultados na busca. Abertura da variante /abs/ retornou 403. Não foi obtido texto integral; a suposta melhora de 18% não foi confirmada. Fonte de apoio, sem ampliar o portfólio de 34.'},
    {'fonte': 'Millea — alternativa de versão', 'url': 'https://m3t4n01a.github.io/rl_esn.pdf',
     'alcance': 'Busca por versão alternativa da dissertação em Groningen e pelo título/Forex retornou também artigo distinto. Não há prova de que seja capítulo faltante da dissertação; não transportar seus ativos ou operações.'},
]
data = {'base': base['id'], 'sha256_base': sha, 'word_alterado': False,
        'celulas_com_escopo_ampliado': reviewed, 'fontes_da_rodada': len(notes),
        'insuficiencias_restantes': 38, 'busca_integral_concluida': False,
        'leituras': notes, 'conciliacao_historico_por_hash': history, 'fontes_externas': external,
        'sem_experimentos': True, 'classificacao_turno_anterior': 'progresso',
        'fundamento_progresso': 'Novas fontes e leitura/inspeção ampliadas; confronto adicional do percentual de 18%; inventário histórico ligado aos 22 PDFs por hash, evitando releituras sem hipótese nova.'}
(out / 'evidencias.json').write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
lines = ['# Pesquisa das lacunas — rodada 3', '', f"Base: **{base['id']}**, SHA256 `{sha}`.", '',
         'Foram ampliadas as evidências de 11 células em seis fontes. Foram recuperados o material de origem de Gjika, o CSV e dois Rmd originais do OSF. Nenhuma nova substituição foi sustentada. A matriz permanece com 38 informações insuficientes. Word, imagens da monografia e resultados experimentais não foram alterados.', '',
         '## Achados', '']
for n in notes:
    source = sources[n['id']]
    lines += [f"### {source['autor']} — {', '.join(n['dimensoes'])}", '',
              '**Leitura nesta rodada:** PDF '+', '.join(map(str, n['paginas_textuais_nesta_rodada']))+'.', '',
              '**Cobertura anterior:** '+n['cobertura_anterior'], '', n['conclusao'], '', '**Decisão:** '+n['decisao'], '']
lines += ['## Conciliação de evidências existentes', '',
          'Os registros anteriores já documentavam leituras amplas de vários artigos. Foram vinculados registros das 22 fontes que ainda possuem “?” aos respectivos PDFs, com conferência dos hashes. Este índice identifica evidências existentes; não é prova automática de leitura integral nem dispensa conferir o alcance declarado. Não repetir a leitura de um PDF apenas porque um relatório de outra rodada se limitou a passagens dirigidas.', '',
          '## Alternativas externas', '']
for x in external:
    lines += [f"- [{x['fonte']}]({x['url']}): {x['alcance']}"]
lines += ['', '## O que permanece aberto', '',
          'A informação não localizada não pode ser substituída por uma experiência de outro artigo nem pela configuração presumida de uma biblioteca. Parte das células descreve temas que a obra não documenta suficientemente, e não experiências que faltam executar nesta monografia. As leituras desta rodada não eliminam os 38 sinais nem demonstram conclusão da busca integral.', '',
          'As rotas ainda úteis são verificar material complementar específico e esclarecer ambiguidades documentais. Em Abebe, a origem agora foi recuperada: falta comprovar o procedimento que resultou nos 363 valores e seus coeficientes publicados, não localizar novamente o CSV. A hipótese de excluir três zeros e dividir por 100 é parcialmente compatível, sem provar o protocolo. Continuar código/protocolo de origem para as leis de pesos e escolhas de hiperparâmetros ainda não declaradas. Não solicitar treinamento ou experimento novo para preencher a matriz bibliográfica. Não contactar autores sem instrução explícita do usuário.', '',
          '## Verificação', '',
          '- Identidade da v010 conferida por SHA256; sem nova versão Word por esta auditoria.',
          '- Os 22 PDFs das células restantes continuam com os hashes do inventário.',
          '- Oito páginas de fontes foram renderizadas e abertas: Abebe 11; Araújo 9; Timbó 7/9; Zhang 4/5; Vishwas 9/18.',
          '- A triagem de links em todos os PDFs está em `triagem_suplementos.json`. Busca lexical serve para localizar canais, sem substituir leitura.',
          '- Sem treinamento, busca genética, teste DM ou execução de códigos de terceiros.', '']
(out / 'relatorio.md').write_text('\n'.join(lines), encoding='utf-8')
print(json.dumps({'base': base['id'], 'celulas': reviewed, 'fontes':len(notes), 'pdfs_historicos_conciliados':len(history), 'restantes':38}, ensure_ascii=False))
