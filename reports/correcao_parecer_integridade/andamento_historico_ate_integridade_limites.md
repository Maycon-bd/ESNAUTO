# Andamento atual da correção do parecer

Objetivo ativo F01–F25/R01–R13. Não concluído, nenhuma promoção da revisão.

## Última aplicação: integridade e limites

- Vigente oficial v001, hash2b233d00b880f0f8727baf587828419b591f45428b409be5ec680932d09805aa. Consultar registro a cada retomada.
- Rascunho reports/monografia/trabalho/revisao_parecer_integridade.docx. Hash atual e vínculo PDF em estado_integridade_limites.json e lote1_alteracoes.json.
- Construtor cumulativo Scripts/revisar_parecer_integridade_lote1.py:111 parágrafos originais do corpo e196 de tabelas; alterações de mídia/largura, remoção de linha e novoQuadro6 preservados. Os P dos logs são da basev001, não índices atuais (a lista inserida desloca+1 apósP0058, legenda/fonte+2 antesP0504). Não editar Word e depois reconstruir sem conciliar.
- Último PDF revisao_integridade_limites.pdf,78páginas. Hash no estado. Anteriores revisao_fidelidade_quadro6.pdf(77p) e derivados são históricos. Listas/sumário ainda NÃO atualizados; novoQuadro6 passou à física73/impressa72 mas entrada de lista ainda71. Não promover nem entregar como final.

## Avanços verificados

1. Comparador novo Scripts/comparar_integridade_rascunho.py recebe alvo/saída, recusa sobrescrever pasta de relatório e valida39fontes e contagens de extração contra manifesto inicial. Nunca executar o antigo auditar_integridade_textual_fasoft.py no lugar dele: antigo está preso ao original e sobrescreve auditoria histórica.
2. Resultado atual em integridade_rascunho_03/:6janelas/3blocos; nomesLSTM/GRU+autores, expansãoRNN e nomeAIC. Contextos do alvo e fontes examinados, sem apropriação indevida demonstrada nesses blocos. Nenhuma troca de terminologia apenas para reduzir coincidência. 38958pares de parágrafos corpoLampugnani/alvo(151×258,15+palavras), nenhum>=0,40 SequenceMatcher/autojunkFalse. Limites e interpretação no relatório: não percentual de plágio, semOCRintegral, tradução ou detecção semântica/universal. Nelson segue sem texto extraível, e código não foi submetido a detector de origem. Primeira tentativa de pares falhou antes de gravar por título numerado e tabela aninhadaLampugnani; rotina atual aceita1INTRODUÇÃO e comparação de pares explicitamente só corpo. Busca de janelas inclui tabelas do alvo.
3. Scripts/cruzar_referencias_rascunho.py:50referências,149ocorrências reconhecidas,nenhumaórfã e nenhuma referência semchamada. Extrai ano bibliográfico antesDOI/URL/notaerrata, sem usar anoIDEAL2024 para ediçãoAraújo2025. Regras/limites e todos os registros em cruzamento_referencias_rascunho.json. Não comprova sustentação científica nem detecta todo formato universalmente.
4. F20 encerrado no escopo específico: Deng accepted manuscript2021 tem folhaDTU indicando fascículo2022/8(1)/1454–1466; Kumar online2024 tem cabeçalhoedição2025/66/2543–2563. Anos atuais corretos, sem edição adicional. Evidência/hash metadados_deng_kumar.json, mais arquivos Araújo e logs de iniciais anteriores.
5. R09 conferido: P0340/P0484 conservam limitação de orçamento desigual; DM não remove a assimetria. R11: P0476 agora explicita que erro/R² não comprovam ganho sobre último preço, comparador ausente dos quatro contrastescontrolados. P0485 mantém ausência de estratégia,custos/retorno e validaçãoprodução. Sem novo treino/GA/DM. Corrigida concordância do resumo “a menor raiz”, sem alterar números.
6. Auditoria estrutural parcial auditoria_estrutural_rascunho_parcial.json:38checks aprovados(margens/A4,150–500palavrasresumos,tabelas11pt,cabeçalhosnegrito,legendas/fontes10pt,títulossem siglas/pontofinal). Não prova conformidade integral ou inspeção final.
7. Visual atual: físicas67/68/73 abertas, sem colisão/recortes nos trechos examinados. p8rasterizada em qa_integridade_limites mas ainda não aberta nesta aplicação. Nova expansão da discussão levou a78páginas. Conferências anteriores têm seus hashes próprios e não substituem inspeção global da aplicação atual.

## Próximas ações

1. Abrir resumo8 e continuar fechamento requisito por requisito dos38itens. F21/F20 já resolvidos no escopo; outros têm redação corrigida mas registro ainda parcial. Ler CSV/parecer e evidência, não encerrar automaticamente por presença de uma edição.
2. Conferir abrangência de F14 e demais usos/citações atuais. Metadados substantivos agora reconciliados, mas não chamar toda a bibliografia de integralmente lida. R10 requer conferir escopoDM em todo o conjunto.
3. Auditar guia, siglas, itálico e apresentação no conjunto; atualizar listas/campos após terminar texto, renderizar e inspecionar todas78+ páginas. Planejar salvamento nativo/conciliação do hash e do construtor para não apagar a atualização se reconstruir. Exportador sem-AtualizarListas não salvaDOCX; -AtualizarListas salva. Mantém sessãoWord do usuário protegida.
4. Pendências documentais específicas a apresentar após avançar tudo: cadeia original de ajuste/autoria; primáriosOnda5 IDs0053–0067 ausentes doCSVatual; originalRBras2022a ainda atribuído ao Quadro3/P0328; planilhas bibliográficas originais; origem individual de rotinaslegadas. Quadro6 explicita limites, não resolve autoria histórica. Não restaurar/regenerar resultados para preencher lacunas.
5. Finalizar matriz38itens, relatório de correções+pendências específicas e versão em_revisao pelo controle após QAfinal. Objetivo não completo ainda.

Históricos detalhados: andamento_historico_ate_quadro6.md, andamento_historico_ate_metadados_comparadores.md e andamento_historico_ate_matriz170.md. Todas correções anteriores continuam aplicadas.
