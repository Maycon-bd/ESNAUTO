from pathlib import Path
import json

base = Path(__file__).resolve().parent
data = json.loads((base / 'conteudo.json').read_text(encoding='utf-8'))
data = [d for d in data if d['title'] != 'Demonstração breve do ESNAUTO']
data[0]['notes'] = data[0]['notes'].replace('e mostrar brevemente o ESNAUTO, aplicação que desenvolvi como apoio aos experimentos', 'e apresentar a contribuição do ESNAUTO como infraestrutura de apoio aos experimentos')
data[16]['notes'] = data[16]['notes'].replace('Vou mostrar brevemente como o aplicativo apresenta o fluxo experimental, mantendo o foco da defesa na pesquisa.', 'Essa contribuição de software complementa a pesquisa experimental. A seguir, retomo as limitações e as possibilidades de continuidade do estudo.')
extras = {
5: ' Para interpretar o processo, é útil distinguir o indivíduo da população e a execução completa. Cada indivíduo representa uma combinação de hiperparâmetros. A população reúne candidatos que o algoritmo avalia e modifica ao longo das gerações. Ao final, preserva-se a configuração selecionada pelo critério de treino e validação. A avaliação de teste informa seu comportamento posterior. Assim, muitas gerações dentro de uma busca não equivalem a muitas repetições independentes do experimento.',
8: ' Para ler a tabela, comparo primeiro uma coluna de cada vez. O MAE resume a magnitude média dos desvios. O RMSE cresce mais quando há erros elevados. Essa diferença explica por que uma configuração pode liderar uma métrica e outra configuração liderar a segunda. O R quadrado próximo de um deve ser interpretado junto desses erros e da persistência da série. Os valores consolidados descrevem as execuções disponíveis e não constituem uma garantia de desempenho em qualquer período futuro.',
14: ' Há também uma diferença entre significância estatística e tamanho do efeito. O teste informa se a diferença de perda é compatível com a hipótese nula sob suas condições. Para avaliar a magnitude prática, volto aos valores de MAE e RMSE na janela comum. Por isso apresentei primeiro o gráfico de erros e depois os contrastes estatísticos: as duas leituras são complementares e precisam permanecer ligadas ao mesmo protocolo.',
17: ' Uma extensão experimental pode organizar essas limitações em perguntas específicas. Repetições com diferentes sementes permitiriam caracterizar a variabilidade do reservatório. Janelas temporais sucessivas ajudariam a verificar a sensibilidade ao período de avaliação. Ablações permitiriam comparar versões com e sem um componente mantendo as demais escolhas controladas. Essas etapas são propostas de continuidade, sem serem apresentadas como experimentos já realizados nesta monografia.'
}
for i, extra in extras.items():
    data[i]['seconds'] += 30
    data[i]['notes'] += extra
(base / 'conteudo_sem_demo.json').write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
script = (base / 'criar.mjs').read_text(encoding='utf-8-sig')
script = script.replace('build/conteudo.json', 'build/conteudo_sem_demo.json')
script = script.replace('data[19].seconds', 'data[data.length-1].seconds')
script = script.replace('build/previews', 'build/previews_sem_demo')
script = script.replace('incluindo demonstração breve', 'dedicados à exposição da pesquisa')
script = script.replace('trocar de tela', 'avançar os slides')
script = script.replace('O aplicativo é apoio experimental. Deixe-o iniciado e prepare um resultado cuja procedência seja conhecida. Não execute buscas ou treinamentos durante a apresentação. Se houver falha, explique o fluxo pelo slide 18.', 'Este roteiro se destina ao vídeo e não inclui demonstração do aplicativo. A demonstração do sistema ficará para a defesa, conforme a orientação do autor.')
script = script.replace('Roteiro de apresentação — defesa da monografia', 'Roteiro do vídeo de apresentação da monografia')
script = script.replace('MayconGarciaSilva_Roteiro_Defesa.md', 'MayconGarciaSilva_Roteiro_Video_sem_demonstracao.md')
script = script.replace('MayconGarciaSilva_Apresentacao.pptx', 'MayconGarciaSilva_Apresentacao_sem_demonstracao.pptx')
script = script.replace('explicitTotalSlideCount:20', 'explicitTotalSlideCount:19')
script = script.replace('build/candidate.pptx', 'build/candidate_sem_demo.pptx')
script = script.replace('build/cronograma.json', 'build/cronograma_sem_demo.json')
script = script.replace('build/validacao.json', 'build/validacao_sem_demo.json')
(base / 'criar_sem_demo.mjs').write_text(script, encoding='utf-8')
print('Revisão preparada: 19 slides, sem demonstração do aplicativo.')
