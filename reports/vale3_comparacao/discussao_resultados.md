# Resultados da extensão VALE3

A extensão experimental para VALE3 compreendeu 12 execuções adicionais de ESN, realizadas entre 12 e 13 de outubro de 2026: Normal × Normal, Uniforme × Uniforme, GED × Uniforme e GED × Normal, com três sementes distintas por combinação. As 45 execuções históricas de PETR4 permanecem como estudo principal; a extensão não reproduz as cinco ondas nem inclui novos experimentos LSTM ou GRU.

Foi empregado o motor atual do ESNAUTO, com população de 10 indivíduos, inicialização LHS, mutação cataclísmica, limite de 10.000 gerações e parada após 3.500 gerações sem melhora. A função objetivo maximiza o negativo da soma ponderada de MAE de treino (40%) e validação (60%). Os pesos e hiperparâmetros foram otimizados para VALE3; os parâmetros dos geradores foram mantidos: Normal com média zero e desvio padrão um, Uniforme em [−1, 1] e GED com média 14,573152, desvio padrão 8,032086 e forma 7,686645. A GED foi utilizada como configuração fixa de transferência do projeto, sem nova estimação na VALE3.

A série de 5.192 valores foi dividida em 2.596 observações de treino, 1.298 de validação e 1.298 de teste. A avaliação de um passo à frente preservou o procedimento do motor: 1.297 pares no teste, com uso do valor observado anterior como entrada. O primeiro ponto do bloco de teste não integra a métrica. O estado do reservatório é reconstruído no treino e a avaliação passa ao teste sem percorrer o bloco de validação; esta convenção deve ser considerada na reprodução e na comparação. Não foram atribuídas datas às observações, pois o arquivo de entrada não contém uma coluna de datas.

As execuções atingiram entre 4,013 e 10,000 gerações, totalizando 8,53 horas de busca genética. As sementes, matrizes Win, W e Wout, objetos do GA, previsões e métricas foram preservados por rodada. O salvamento entre cenários permite retomar os pendentes após interrupções; ele não recupera uma geração interrompida dentro de uma rodada.

A Tabela 10 apresenta média e desvio padrão amostral das três rodadas por combinação. A Figura 5 mostra cada execução, evitando que a média oculte resultados discrepantes. As diferenças são descritivas: três rodadas não sustentam, por si, conclusões de superioridade estatística.

Normal × Normal apresentou MAE médio de teste de 0,678031 e desvio padrão de 0,004658. GED × Uniforme apresentou MAE médio de 1,931147 e desvio padrão de 2,102771. Na terceira rodada desta combinação, o MAE de teste foi 4,359181 e o R² foi 0,801793, apesar de MAE de validação de 0,409615. Essa execução foi mantida na análise. O contraste evidencia que validação próxima não assegurou estabilidade fora da amostra; a causa específica exige investigação adicional.

A escolha pelo maior fitness de treino/validação selecionou GED × Uniforme na primeira rodada, semente 20261115, com a = 0,697568, raio espectral = 0,217691, lavagem de 16 passos, 24 neurônios e regularização 9.900000e-09. Seu MAE de validação foi 0,408928 e o MAE de teste foi 0,728545. A Figura 6 apresenta suas previsões e resíduos. Normal × Normal teve menor erro médio no teste, mas esse resultado é uma observação posterior, e não um critério de seleção aplicado antes do teste.

Para contextualizar o desempenho, foi calculada uma previsão de persistência, na qual o próximo preço previsto é igual ao último observado, sobre os mesmos 1.297 pares. Seu MAE foi 0,673251 e RMSE foi 1,010382. Nenhuma das 12 execuções de ESN apresentou MAE de teste inferior ao dessa referência. Portanto, os R² elevados nas demais rodadas não demonstram ganho preditivo sobre a persistência, especialmente em séries de preços em nível.

Para a comparação descritiva entre ativos, definiu-se NMAE = 100 × MAE / média dos módulos dos preços observados no teste. As médias utilizadas foram 16,182037 para PETR4 e 35,737281 para VALE3. O controle histórico Normal × Normal da PETR4, GA_RUN_0046, apresentou MAE de 0,328365, equivalente a NMAE de 2,029%. Para Normal × Normal da VALE3, o NMAE médio foi 1,897%. A diferença entre os MAEs absolutos reflete parcialmente as escalas dos preços; esses valores normalizados não constituem evidência de que um ativo seja mais previsível.

A comparação utiliza o controle de produção Normal × Normal da PETR4, com uma execução histórica, e três rodadas da VALE3, sem pareamento de sementes ou alinhamento diário demonstrado. Resultados legados de 200 gerações e outro motor não integram as médias. A ausência de registros equivalentes para os demais pares impede uma comparação controlada entre ativos. As conclusões sobre LSTM e GRU permanecem restritas à PETR4; não foram realizados testes de significância entre ações.

                     MAE_media    MAE_dp  RMSE_media   RMSE_dp  NMAE_media   NMAE_dp  valida_media  tempo_medio
cenario                                                                                                        
Normal × Normal       0.678031  0.004658    1.018105  0.006627    1.897266  0.013035      0.409529  1803.400000
Uniforme × Uniforme   0.710010  0.031202    1.066247  0.046824    1.986749  0.087311      0.409319  2566.993333
GED × Uniforme        1.931147  2.102771    3.025849  3.415871    5.403731  5.883970      0.409375  3150.650000
GED × Normal          0.723021  0.017342    1.060260  0.017481    2.023156  0.048525      0.409611  2718.016667