# Andamento da correção do parecer

Objetivo ativo: resolver F01–F25 e R01–R13 do parecer de 28/10/2026. Não concluído.

## Estado vigente do trabalho

- Registro oficial: v001, SHA256 2b233d00b880f0f8727baf587828419b591f45428b409be5ec680932d09805aa. Consultar novamente `Scripts/versao_monografia.py atual --json` em cada retomada.
- Rascunho: reports/monografia/trabalho/revisao_parecer_integridade.docx, derivado de v001 com origem adjacente. Último hash e evidências em estado_metadados_comparadores.json.
- Construtor cumulativo: Scripts/revisar_parecer_integridade_lote1.py. Recria a partir de v001, recusa rascunho alterado fora do construtor e base vigente diferente. Não editar o Word manualmente antes de conciliar o script.
- Aplicação atual: 99 parágrafos de corpo, 196 parágrafos de tabelas, Figura1 substituída/redimensionada, larguras do Quadro1 redistribuídas e uma linha da Tabela7 removida. Logs antes/depois/evidência em lote1_alteracoes.json.
- Nenhuma promoção; revisão integral e listas ainda pendentes. Não registrar como concluída ou conferida integralmente.

## Alterações mais recentes

1. R03/F17: resumo, abstract, método e conclusão agora descrevem arquivos recebidos como ajustados, sem atribuir a aplicação original ao autor. Removidas listas/exceções de eventos não demonstradas. Leitura dos dois arquivos confirmou 5198 observações, datas2000-01-03–2020-12-30 e valores concordantes (máxima diferença1E-14). Não comprova cadeia de ajuste ou autoria. Evidência: evidencia_procedencia_h4_h5.json.
2. R07/R08: preservadas hipóteses originais; resultados e conclusão distinguem integração LHS/cataclismo de diversidade não demonstrada; dispersão entre15 configurações da Onda5 de variabilidade entre sementes. Relatório compilado docs/09 contém IDs0053–0067, ausentes no CSV atual. Não usar reports/revisao_orientador_petr4/historico_ga.csv como histórico dessas15 execuções: pertence ao bloco ilustrativo. Sem restaurar ou regenerar resultados.
3. R12: título nas três folhas alinhado à previsão da PETR4 ajustada com ESNs e otimização genética. Datas/nomes da aprovação preservados, sem inventar aprovação.
4. F19: retirada linha Cardoso2022a e RMSE0,4987 da Tabela7 e das conclusões dependentes; comparação agora só com Lampugnani. As24 linhas de resultados da monografia Lampugnani confirmam mínimos MAE0,378706/Cauchy×Normal e RMSE0,568178/Cauchy×Uniforme. Não equiparar protocolos nem ausência de tratamento adicional a ausência de ajuste prévio. Evidência: evidencia_comparacao_lampugnani.json. Cardoso2022a permanece atribuído historicamente à Quadro3/P0328 e na referência P0510, ainda sem original para confirmação.
5. F20: fonte oficial Springer do DOI10.1007/978-3-031-77738-7_26 recomenda citação2025, páginas315–327, com publicação online14/11/2024. Corrigidos referência e todas as chamadas Araújo, inclusive Quadro1; P0252 distingue prova consultada dos metadados finais. Não houve leitura da edição final paga. Evidência: metadados_araujo_reconciliados.json. Base reconstruída e matriz anteriores são históricos; não os confundir com uma exportação editorial atualizada.

## PDF e inspeção

Último PDF: revisao_metadados_comparadores.pdf,76 páginas, hash no estado desta etapa. Não usar revisao_procedencia_hipoteses.pdf ou revisao_comparacao_fontes.pdf como a aplicação atual; são intermediários. Páginas físicas1,2,3,4,8,9,42,59,63,64,70,71,72 abertas visualmente nesta aplicação: sem recortes/sobreposições identificados. Imagens em qa_metadados_comparadores/. Inspeção integral ainda não realizada. PageMap Word usa paginação diferente da página física PDF; não confundir.

Exportar sem salvar pelo Word com Scripts/exportar_padronizacao_fasoft.ps1, sem -AtualizarListas. COM requer execução escalada no ambiente; aprovada nas exportações realizadas. Nunca abrir/modificar sessão existente do usuário. Atualização de listas salva o Word e precisa ser planejada após fim das alterações, conciliando o hash/construtor.

## Prioridades restantes

1. F14: conferir Ribeiro, WangF., Zhang, Xiao e demais usos contra fontes; não confundir a correção de um parágrafo com todas as ocorrências. Encerrar por evidência os itens já corrigidos após verificar o conjunto.
2. F21: decidir citações/referências Cardoso2025 e Jaeger2001 sem chamadas, usando as obras onde pertinentes ou removendo referências sem uso; não inserir chamadas decorativas.
3. R13: explicitar elementos herdados/adaptados/desenvolvidos e procedência do código. Scripts legados na raiz mencionam caminhos do orientador, mas isso não comprova autoria integral nem licença. Não inventar atribuições a partir de nomes de pastas.
4. F20: conferir metadados remanescentes, incluindo Deng/Kumar e correspondência global. A matriz170 está recodificada com43 células insuficientes explicitadas; preservar limites e não alegar leitura integral.
5. Pendências documentais a apresentar somente após avançar o restante: cadeia original de ajuste, exportações primárias Onda5, original RBras2022a (inclusive origem Quadro3), planilhas bibliográficas ausentes e atribuições de código não recuperáveis.
6. Revalidar integralmente F01–F25/R01–R13 (resolucao_achados.csv contém38 itens), siglas/itálicos e guia. Atualizar listas/campos, renderizar e inspecionar o conjunto final; só então registrar revisão em_revisao com verificações e pendências precisas. Não executar treino, GA, DM ou alterar dados experimentais.

Histórico detalhado anterior preservado em andamento_historico_ate_matriz170.md. Scripts, logs e estados anteriores preservam sua identidade; não representam automaticamente a aplicação atual.
