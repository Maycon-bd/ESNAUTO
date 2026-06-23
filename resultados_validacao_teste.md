======================================================================

         RESULTADOS ESN — PETR4 TCC Maycon G Silva

         Relatório Gerado em: 2026-06-23 15:35:18

======================================================================



--- TABELA COMPARATIVA DOS 12 CENÁRIOS ---

As métricas a seguir foram obtidas avaliando as matrizes ótimas nas partições de validação e teste.



| Run | Distribuição Win | Distribuição W | MAE (Validação) | RMSE (Validação) | MAE (Teste) | RMSE (Teste) |
|-----|------------------|----------------|-----------------|------------------|-------------|--------------|
| 1   | Normal           | Normal         | 0.26298873220676 | 0.354088606915066 | 0.327753399193782 | 0.498237427328656 |
| 2   | Normal           | Normal         | 0.262678302532645 | 0.353765616019076 | 0.329318704574647 | 0.500718938900147 |
| 3   | **Normal**       | **Normal**     | 0.262529668011459 | 0.353379918120715 | **0.32747163804535** | 0.499603898525658 |
| 1   | Uniforme         | Uniforme       | 0.262586953584626 | 0.354004961529989 | 0.329109120279466 | 0.500849569983114 |
| 2   | Uniforme         | Uniforme       | 0.262753663898188 | 0.353714883823454 | 0.327522328236599 | 0.4982098735005 |
| 3   | **Uniforme**     | **Uniforme**   | 0.263092483529666 | 0.354225626770399 | 0.328366437256995 | **0.497529311770955** |
| 1   | GED              | Uniforme       | 0.26261574814034 | 0.353288931617119 | 0.328018562317869 | 0.498720218133032 |
| 2   | **GED**          | **Uniforme**   | **0.26231708772512** | **0.352963273425167** | 0.328367458657593 | 0.498908502774209 |
| 3   | GED              | Uniforme       | 0.262678971836972 | 0.353419288563406 | 0.327916872697785 | 0.498609863631295 |
| 1   | GED              | Normal         | 0.262635666150002 | 0.353439536353175 | 0.32781558770127 | 0.498586604675989 |
| 2   | GED              | Normal         | 0.262598655973632 | 0.35332729097702 | 0.327952966786408 | 0.498713551346167 |
| 3   | GED              | Normal         | 0.262566799856984 | 0.353549791926368 | 0.328016989055505 | 0.498591012328835 |


--- MELHOR CENÁRIO DE TESTE (Menor MAE de Teste) ---

Cenário:      Run 3 | Win Normal | W Normal

Época GA:     2754

Hiperparâmetros:

  a             = 0.768842840903022

  sr            = 0.682584248231874

  initLen       = 98

  tam_reservoir = 3

  reg           = 9.45539313111546e-05

Resultados:

  MAE  Validação = 0.262529668011459

  RMSE Validação = 0.353379918120715

  MAE  Teste     = 0.32747163804535

  RMSE Teste     = 0.499603898525658


--- MELHOR CENÁRIO DE TESTE (Menor RMSE de Teste) ---

Cenário:      Run 3 | Win Uniforme | W Uniforme

Época GA:     3658

Hiperparâmetros:

  a             = 0.879408870001755

  sr            = 0.427592678777151

  initLen       = 112

  tam_reservoir = 27

  reg           = 1.53151837573386e-05

Resultados:

  MAE  Validação = 0.263092483529666

  RMSE Validação = 0.354225626770399

  MAE  Teste     = 0.328366437256995

  RMSE Teste     = 0.497529311770955


--- MELHOR CENÁRIO DE VALIDAÇÃO (Menor MAE de Validação) ---

Cenário:      Run 2 | Win GED | W Uniforme

Época GA:     2000

Hiperparâmetros:

  a             = 0.379504238160997

  sr            = 0.128548649205392

  initLen       = 67

  tam_reservoir = 22

  reg           = 4.88318178082192e-05

Resultados:

  MAE  Validação = 0.26231708772512

  RMSE Validação = 0.352963273425167

  MAE  Teste     = 0.328367458657593

  RMSE Teste     = 0.498908502774209


--- CENÁRIO SELECIONADO PELO GA (Melhor Fitness) ---

Cenário:      Run 2 | Win GED | W Normal

Fitness GA:   -0.23753732723132

Época GA:     117

Hiperparâmetros:

  a             = 0.870902030197374

  sr            = 0.406802420062409

  initLen       = 9

  tam_reservoir = 27

  reg           = 2.2289743444227e-05

Resultados:

  MAE  Validação = 0.262598655973632

  RMSE Validação = 0.35332729097702

  MAE  Teste     = 0.327952966786408

  RMSE Teste     = 0.498713551346167
