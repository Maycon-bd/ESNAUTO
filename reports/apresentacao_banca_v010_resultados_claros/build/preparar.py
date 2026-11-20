from pathlib import Path
import json,re
B=Path(__file__).resolve().parent;R=B.parents[2]
OLD=R/'reports/apresentacao_banca_v010_fala_clara/build'
blocks=re.split(r'^## \d+\s*\n',(OLD/'falas.md').read_text(encoding='utf-8'),flags=re.M)[1:]
new={
19:'''Retomando as hipóteses, a primeira recebeu apoio: a ESN foi competitiva com GRU e LSTM nos resultados históricos, e a rodada complementar também apresentou diferenças favoráveis a ela. A segunda recebeu apoio pelo ajuste rápido da rede depois de escolhida a configuração.

A terceira mostrou que algumas combinações tiveram erro menor que a referência Normal com Normal. A melhora foi pequena, mas está registrada. Isso ajuda a identificar configurações que merecem continuar sendo estudadas.

Na quarta, os recursos para explorar soluções foram incorporados ao sistema, mas sua contribuição isolada ainda precisa ser medida. Na quinta, observei erros próximos entre as configurações da última onda. Para afirmar estabilidade quando o sorteio dos pesos muda, serão necessárias repetições. Assim, o trabalho responde às hipóteses com resultados concretos e identifica quais perguntas ficam para os próximos testes.''',
20:'''O trabalho entregou uma avaliação de quarenta e cinco execuções históricas da ESN para a PETR4, organizada em cinco ondas. Essa comparação mostrou configurações competitivas e diferenças de erro que ajudam a orientar novas escolhas. Além disso, a rodada complementar permitiu comparar os erros nas mesmas datas e aplicar o teste estatístico.

Na Engenharia de Software, minha contribuição foi adaptar as rotinas em R fornecidas pelo orientador e desenvolver a interface do ESNAUTO. Com isso, configuração, acompanhamento das execuções, gráficos e consulta ao histórico ficaram reunidos no sistema.

Também foram preservados os arquivos da rodada complementar, incluindo previsões, modelos e informações das execuções. Portanto, existem resultados registrados e material para conferência. A preservação parcial se refere a parte dos arquivos necessários para repetir exatamente as execuções antigas; ela não significa que os resultados do trabalho foram perdidos.''',
21:'''Esses resultados se aplicam à PETR4, no período e nas condições estudadas. Para saber se o comportamento se mantém em outras situações, precisamos testar outras sementes, períodos e ações, com esforço comparável de escolha dos modelos.

As execuções antigas têm resultados registrados, mas parte das matrizes e dos vetores não foi preservada. A rodada complementar ficou com registros mais completos para conferência. A revisão bibliográfica também tem registros parciais de seleção.

Ainda precisamos separar a contribuição de cada componente e comparar com a previsão simples que repete o último preço. Estratégias de investimento e rentabilidade exigem outra avaliação. Aqui, as conclusões tratam do erro de previsão, do tempo de ajuste e da aplicação desenvolvida.''',
22:'''A partir desses resultados, o próximo passo é verificar quanto eles se mantêm quando mudamos as condições. Isso inclui repetir as configurações com outras sementes, testar outros períodos e comparar com a previsão simples que repete o último preço.

Também é importante comparar os modelos com esforço semelhante de otimização e avaliar os componentes da busca separadamente, mantendo as outras condições iguais.

No software, a evolução prevista é o JANUS, com melhorias na interface e na organização dos arquivos das execuções. A VALE3 aparece como extensão experimental, fora dos resultados principais desta apresentação. Essas frentes dão continuidade ao que foi construído e precisam de testes próprios.''',
23:'''O trabalho mostrou que a ESN foi uma alternativa competitiva para prever o fechamento ajustado da PETR4 nas condições estudadas. No histórico, quarenta e quatro das quarenta e cinco execuções tiveram MAE menor que os valores documentados para GRU e LSTM. Na rodada complementar, a ESN teve menor erro, com apoio dos testes estatísticos daquela execução.

Outro resultado foi o ajuste rápido da rede selecionada, com o custo da busca apresentado separadamente. Minha contribuição de Engenharia de Software foi adaptar as rotinas e desenvolver a interface do ESNAUTO, reunindo configuração, acompanhamento e análise dos testes.

O trabalho entrega resultados de previsão, uma aplicação e registros para conferência. Essa é a base construída para os próximos estudos. Agradeço a atenção da banca.'''
}
for i,s in new.items():blocks[i-1]=s
(B/'falas.md').write_text('\n\n'.join(f'## {i:02d}\n{s.strip()}' for i,s in enumerate(blocks,1))+'\n',encoding='utf-8')
changes={
19:{'text-2':'ESN competitiva no histórico e na rodada complementar',
    'text-4':'Ajuste rápido da ESN após a seleção',
    'text-6':'Algumas configurações superaram a referência Normal',
    'text-8':'Recursos implementados; efeito isolado ainda a avaliar',
    'text-10':'Erros próximos na Onda 5; estabilidade entre sementes a avaliar'},
20:{'text-0':'O que o trabalho entregou',
    'text-2':'45 execuções históricas e comparação estatística complementar',
    'text-4':'Rotinas adaptadas e interface do ESNAUTO desenvolvida',
    'text-5':'Previsões e modelos preservados na rodada complementar'},
21:{'text-0':'Alcance dos resultados e próximos testes',
    'text-2':'Resultados para PETR4, no período e nas condições estudadas',
    'text-4':'Ampliar sementes e comparar esforços de otimização',
    'text-6':'Histórico parcial; rodada DM com registros mais completos',
    'text-8':'Contribuição de cada componente ainda a isolar',
    'text-10':'Persistência e rentabilidade exigem avaliação própria'},
23:{'text-0':'Conclusões para a PETR4',
    'text-2':'Histórico: 44 de 45 ESNs com MAE menor que GRU e LSTM',
    'text-4':'Rodada complementar: menor erro e apoio estatístico',
    'text-6':'Ajuste final: 0,05 s; busca total: 37,9 h',
    'text-8':'ESNAUTO: adaptação das rotinas e interface desenvolvida'}
}
(B/'textos_slides.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2),encoding='utf-8')
s=(OLD/'criar.py').read_text(encoding='utf-8')
s=s.replace("SRC=ROOT/'reports/apresentacao_banca_v010_visual'","SRC=ROOT/'reports/apresentacao_banca_v010_fala_clara'")
s=s.replace("SRC/'entrega/Roteiro_video_ESNAUTO_25min_v010.docx'","SRC/'entrega/Roteiro_ESNAUTO_v010_fala_clara.docx'")
s=s.replace("srcdeck=SRC/'entrega/Apresentacao_ESNAUTO_banca_visual_v010.pptx'","srcdeck=SRC/'entrega/Apresentacao_ESNAUTO_v010_notas_fala_clara.pptx'")
s=s.replace("assert sum(s['seconds'] for s in slides)==1500",'''for i,seconds in {20:75,21:60,22:50,23:60}.items(): slides[i-1]['seconds']=seconds
elapsed=0
for s in slides:
    s['start']=elapsed; elapsed+=s['seconds'];s['end']=elapsed
    stamp=lambda t:f'{t//60:02d}:{t%60:02d}'
    s['window']=stamp(s['start'])+'–'+stamp(s['end'])
    s['wpm']=round(s['words']*60/s['seconds'])
for i,title in {20:'O que o trabalho entregou',21:'Alcance dos resultados e próximos testes',23:'Conclusões para a PETR4'}.items():slides[i-1]['title']=title
assert elapsed==1500''')
s=s.replace('Roteiro_ESNAUTO_v010_fala_clara','Roteiro_ESNAUTO_v010_resultados_claros')
s=s.replace("doc=Document(SRC/'entrega/Roteiro_ESNAUTO_v010_resultados_claros.docx')","doc=Document(SRC/'entrega/Roteiro_ESNAUTO_v010_fala_clara.docx')")
s=s.replace('24:15   Conclusão','24:00   Conclusão')
s=s.replace('Fala revisada para explicar o trabalho com clareza.','Fala revisada para apresentar os resultados e as contribuições com clareza.')
# Apply replacements inside existing text shapes; geometry, hyperlinks and all chart parts stay intact.
s=s.replace("m=re.fullmatch(r'ppt/notesSlides/notesSlide(\\d+)\\.xml',info.filename)",'''sm=re.fullmatch(r'ppt/slides/slide(\\d+)\\.xml',info.filename)
        edits=json.loads((BUILD/'textos_slides.json').read_text(encoding='utf-8'))
        if sm and sm[1] in edits:
            rt=E.fromstring(buf)
            for name,text in edits[sm[1]].items():
                shapes=rt.xpath('//p:sp[p:nvSpPr/p:cNvPr[@name="'+name+'"]]',namespaces=ns)
                assert len(shapes)==1,(sm[1],name)
                tt=shapes[0].xpath('.//a:t',namespaces=ns);assert len(tt)==1,(sm[1],name,len(tt))
                tt[0].text=text
            buf=E.tostring(rt,xml_declaration=True,encoding='UTF-8',standalone=True)
        m=re.fullmatch(r'ppt/notesSlides/notesSlide(\\d+)\\.xml',info.filename)''')
(B/'criar.py').write_text(s,encoding='utf-8')
for fn in ['finalizar.mjs','paginas_word.ps1','renderizar_roteiro.py','conferir_powerpoint.ps1']:
    s=(OLD/fn).read_text(encoding='utf-8-sig')
    s=s.replace('apresentacao_banca_v010_fala_clara','apresentacao_banca_v010_resultados_claros')
    s=s.replace('Roteiro_ESNAUTO_v010_fala_clara','Roteiro_ESNAUTO_v010_resultados_claros')
    s=s.replace('Apresentacao_ESNAUTO_v010_notas_fala_clara','Apresentacao_ESNAUTO_v010_resultados_claros')
    if fn=='finalizar.mjs':
        s=s.replace('../apresentacao_banca_v010_visual/entrega/Apresentacao_ESNAUTO_banca_visual_v010.pptx','../apresentacao_banca_v010_fala_clara/entrega/Apresentacao_ESNAUTO_v010_notas_fala_clara.pptx')
        s=s.replace('2be34ffb858391f2c0011f9683cb215adcfc520f7b58fcabed3ce9672ee62b3d','b0b2cdedebd712f1f33182ae533f98e2996f6aee456b4940520e4a0e6609a18b')
    (B/fn).write_text(s,encoding='utf-8-sig' if fn.endswith('ps1') else 'utf-8')
print('Textos e helpers preparados sem alterar arquivos anteriores')
