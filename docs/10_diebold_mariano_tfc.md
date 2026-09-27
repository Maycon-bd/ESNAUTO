# Teste de Diebold-Mariano

## 1. Contexto da análise complementar

Esta seção documenta uma análise inferencial complementar aos resultados consolidados do TFC sobre Echo State Networks aplicadas à previsão de PETR4. Os resultados históricos permanecem os principais resultados experimentais da pesquisa. O teste de Diebold–Mariano (DM) aqui apresentado foi aplicado a uma **nova execução controlada**, pré-especificada e reprodutível, com seed 20260926. Portanto, seus p-valores não devem ser associados diretamente aos vetores históricos que originaram as métricas da monografia.

## 2. Por que o DM histórico não pôde ser recuperado

A auditoria do repositório, de arquivos compactados e do histórico Git recuperou o registro agregado da GA_RUN_0030, configuração Laplace × Normal, mas não suas matrizes Win, W e Wout nem suas previsões ponto a ponto. Também não foram recuperados os vetores históricos oficiais de GRU e LSTM. As matrizes disponíveis no projeto tinham dimensões incompatíveis com o reservatório de 22 neurônios da execução de interesse.

Não se reconstruíram artificialmente os pesos históricos, não se produziram vetores a partir de MAE/RMSE agregados e não se declarou uma execução diferente como se fosse a GA_RUN_0030. Essa ausência inviabilizou um DM retrospectivo das execuções originais.

## 3. Protocolo da execução controlada

Foi realizada uma única execução científica com seed-base 20260926, sem testar seeds alternativas e sem nova otimização por algoritmo genético. A ESN usou os hiperparâmetros registrados da GA_RUN_0030: Win Laplace, W Normal, a=0,111817, sr=0,215273, initLen=57, reservatório=22 e reg=5,71625418786693×10⁻⁵. Os valores a e sr estavam disponíveis somente com seis casas decimais. Novas matrizes foram geradas; Wout foi estimada exclusivamente com alvos do treino, índices 59–2600.

GRU e LSTM usaram uma camada recorrente de 50 unidades, janela 10, Dropout separado de 0,2, Adam, MSE, batch 16, shuffle=TRUE e 80 épocas. O Min-Max foi ajustado apenas nas 2.600 observações de treino. A validação foi usada como `validation_data`, sem early stopping ou seleção de checkpoint. Nos três modelos, a continuidade treino → validação → teste foi preservada. As primeiras janelas de teste usaram a cauda da validação; a ESN propagou seu estado pela validação sem reestimar Wout.

Cada modelo gerou 1.299 previsões de teste. A junção ocorreu exclusivamente por data e a janela prospectivamente congelada para o DM foi de 30/09/2015 a 30/12/2020, com 1.298 observações. O arquivo foi congelado com SHA-256 `0DD4007600D58047913F2C10BA8CE4F3801E5EE37F4C0E759BC46D2BFF070D5E`. Modelos e matrizes foram recarregados sem retreinamento, reproduzindo as previsões com diferença máxima zero.

## 4. Teste Diebold-Mariano

Definiram-se os erros como e[t]=real[t]−previsão[t]. Foram executadas quatro comparações bilaterais previamente estabelecidas: ESN × GRU e ESN × LSTM sob perda absoluta (power=1) e quadrática (power=2). Utilizou-se `forecast::dm.test()` versão 9.0.2, com horizonte h=1, `alternative="two.sided"`, `varestimator="acf"` e α=0,05.

A hipótese nula, em cada teste, foi a igualdade da acurácia preditiva esperada sob a perda especificada; a alternativa foi a diferença de acurácia. A direção foi avaliada separadamente pelo diferencial d[t]=perda_ESN[t]−perda_baseline[t]. Valores médios negativos indicam menor perda média da ESN. O sinal da estatística DM, isoladamente, não foi usado para afirmar direção.

Os quatro testes foram definidos antes da observação dos p-valores. Manteve-se α individual de 5%, sem correção de multiplicidade nos resultados principais. Essa escolha deve ser considerada ao interpretar o conjunto de decisões.

## 5. Resultados

Tabela – Teste de Diebold-Mariano na execução controlada complementar

| Comparação | Função de perda | n | Estatística DM | p-valor | Menor perda média | Decisão a 5% |
|---|---|---:|---:|---:|---|---|
| ESN × GRU | Absoluta | 1.298 | −11,870611 | 6,296×10⁻³¹ | ESN | Rejeitar H0 |
| ESN × LSTM | Absoluta | 1.298 | −15,496644 | 8,008×10⁻⁵⁰ | ESN | Rejeitar H0 |
| ESN × GRU | Quadrática | 1.298 | −9,846951 | 4,117×10⁻²² | ESN | Rejeitar H0 |
| ESN × LSTM | Quadrática | 1.298 | −9,208792 | 1,285×10⁻¹⁹ | ESN | Rejeitar H0 |

Na perda absoluta, a ESN apresentou perda média de 0,328850, contra 0,418175 da GRU (mean_d=−0,089325) e 0,466612 da LSTM (mean_d=−0,137762). Na perda quadrática, a média da ESN foi 0,248455, contra 0,351000 da GRU (mean_d=−0,102545) e 0,403590 da LSTM (mean_d=−0,155135).

Auditoria descritiva dos mesmos 1.298 erros:

| Modelo | Erro médio | MAE | MSE | RMSE |
|---|---:|---:|---:|---:|
| ESN | 0,001526 | 0,328850 | 0,248455 | 0,498452 |
| GRU | −0,281320 | 0,418175 | 0,351000 | 0,592452 |
| LSTM | −0,367635 | 0,466612 | 0,403590 | 0,635287 |

As identidades MAE=mean(|e|) e RMSE=√MSE foram verificadas numericamente.

## 6. Interpretação

Nas quatro comparações, encontrou-se diferença estatisticamente significativa entre as previsões, acompanhada por diferencial médio de perda negativo. Assim, a ESN apresentou menor perda média que a GRU e a LSTM tanto no critério absoluto quanto no quadrático, nesta execução controlada complementar.

Essa conclusão se limita aos vetores congelados da rodada com seed 20260926. Ela não transforma os p-valores em evidência direta sobre as execuções históricas, cujos vetores não estavam disponíveis, nem mede variabilidade entre inicializações.

## 7. Impacto sobre H1

- ESN × GRU, perda absoluta: H1 apoiada; H0 foi rejeitada e a ESN teve menor perda média.
- ESN × LSTM, perda absoluta: H1 apoiada; H0 foi rejeitada e a ESN teve menor perda média.
- ESN × GRU, perda quadrática: H1 apoiada; H0 foi rejeitada e a ESN teve menor perda média.
- ESN × LSTM, perda quadrática: H1 apoiada; H0 foi rejeitada e a ESN teve menor perda média.

Os quatro resultados são convergentes nesta execução complementar. Ainda assim, a redação científica deve distinguir esse apoio inferencial da evidência descritiva histórica.

## 8. Limitações

Os vetores históricos originais não foram recuperados; os testes usam pesos novos e uma única seed. A fronteira treino/validação e o contexto cronológico foram corrigidos em relação ao código histórico, impedindo classificar a rodada como reprodução exata. A configuração Laplace × Normal foi escolhida após a experimentação histórica, de modo que esta análise não é uma validação inteiramente independente da seleção do modelo. Os quatro testes usam α individual de 5% sem ajuste de multiplicidade. Por fim, uma única inicialização não caracteriza a distribuição de desempenho entre seeds.

## 9. Texto sugerido para Material e Métodos

> Como análise inferencial complementar, realizou-se uma execução controlada e pré-especificada dos modelos ESN, GRU e LSTM, com seed-base 20260926. Como os vetores de previsão e as matrizes da execução histórica GA_RUN_0030 não estavam disponíveis, foram gerados novos pesos sem reotimização de hiperparâmetros. A saída da ESN foi estimada exclusivamente com alvos do treino, e a continuidade cronológica entre treino, validação e teste foi preservada nos três modelos. Após alinhamento por data, analisaram-se 1.298 previsões one-step-ahead, de 30/09/2015 a 30/12/2020. Aplicou-se o teste bilateral de Diebold–Mariano, por meio de `forecast::dm.test()` 9.0.2, com h=1, estimador de variância `acf` e α=0,05, comparando a ESN à GRU e à LSTM sob perdas absoluta e quadrática. A direção foi determinada pela média de d[t]=L_ESN[t]−L_baseline[t]. Os quatro testes haviam sido definidos previamente e não se aplicou ajuste de multiplicidade aos resultados principais.

## 10. Texto sugerido para Resultados e Discussão

> Na execução controlada complementar, a ESN apresentou MAE de 0,328850 e RMSE de 0,498452 na janela comum, enquanto GRU e LSTM obtiveram, respectivamente, MAE de 0,418175 e 0,466612 e RMSE de 0,592452 e 0,635287. O teste bilateral de Diebold–Mariano rejeitou a hipótese de igualdade de acurácia preditiva nas quatro comparações: ESN × GRU sob perda absoluta (DM=−11,870611; p=6,296×10⁻³¹), ESN × LSTM sob perda absoluta (DM=−15,496644; p=8,008×10⁻⁵⁰), ESN × GRU sob perda quadrática (DM=−9,846951; p=4,117×10⁻²²) e ESN × LSTM sob perda quadrática (DM=−9,208792; p=1,285×10⁻¹⁹). Em todos os casos, o diferencial médio de perda foi negativo, indicando menor perda média da ESN. Esses achados apoiam H1 na rodada controlada, mas não constituem teste retrospectivo das execuções históricas, cujos vetores não foram recuperados.

## 11. Texto sugerido para Conclusão

> Além da vantagem descritiva observada nos resultados históricos, uma execução controlada complementar com seed 20260926 apresentou evidência de diferença de acurácia preditiva entre a ESN e ambos os baselines, sob perdas absoluta e quadrática, sempre com menor perda média da ESN. Essa evidência apoia H1 para os quatro contrastes pré-especificados, devendo ser interpretada como complementar, pois utilizou novos pesos, uma única inicialização e um protocolo cronológico corrigido, e não os vetores das execuções históricas originais.

## 12. Eventual frase para o Resumo

> Em uma execução controlada complementar, testes bilaterais de Diebold–Mariano indicaram diferenças significativas entre a ESN e os baselines GRU/LSTM sob perdas absoluta e quadrática, com menor perda média para a ESN em todos os contrastes.

Essa frase deve ser acompanhada, no corpo do trabalho, das limitações sobre novos pesos, seed única e indisponibilidade dos vetores históricos.
