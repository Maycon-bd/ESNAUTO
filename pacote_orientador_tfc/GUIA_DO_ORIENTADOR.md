# 🎓 GUIA DE AVALIAÇÃO DO TFC — PARA O ORIENTADOR
## **Tema:** Previsão de Séries Temporais Financeiras (PETR4) via Echo State Networks com Distribuições Não-Gaussianas e Algoritmo Genético Híbrido (LHS + Cataclismo)
**Autor:** Maycon Garcia Silva  
**Data:** Agosto / 2026

---

### Prezado(a) Professor(a) Orientador(a),

Este pacote contém todos os artefatos, dados brutos, gráficos em alta resolução, códigos-fonte e artigos resultantes da pesquisa experimental realizada no Trabalho de Fim de Curso (TFC).

---

### 📁 ESTRUTURA DESTE PACOTE

```
├── 01_Artigo_e_Monografia/
│   ├── Artigo_Completo_TFC_Maycon_Garcia_Silva.md    # Texto integral formatado com normas ABNT
│   ├── Artigo_LaTeX_IEEE_Maycon_Garcia_Silva.tex     # Template LaTeX pronto (para Overleaf/TeXStudio)
│   ├── Relatorio_Tecnico_4_Ondas_Estocasticas.md      # Detalhamento minucioso das 30 rodadas
│   ├── Metodologia_GA_LHS_Cataclismo.md              # Formulação de 59 bits e amostragem LHS
│   └── Monografia_TFC_MayconGarciaSilva.docx         # Versão editável em Word da Monografia
│
├── 02_Figuras_Alta_Resolucao/
│   ├── fig1_boxplot_mae_ondas.png / .pdf             # Boxplot de erro MAE no teste cego vs DL
│   ├── fig2_tempo_treinamento_speedup.png / .pdf     # Speedup >500x da ESN vs LSTM/GRU (escala log)
│   ├── fig3_campeoes_teste_serie.png / .pdf          # Série temporal teste out-of-sample vs real
│   ├── fig4_dispersao_residuos.png / .pdf            # Dispersão Real x Previsto (R²=0.9940) e resíduos
│   └── fig5_ranking_multicriterio.png / .pdf         # Ranking ponderado multicritério (Score 0-100)
│
├── 03_Planilhas_e_Dados_Brutos/
│   ├── historico_30_rodadas_ga_4_ondas.csv           # Dados brutos das 30 rodadas oficiais (GA 10.000 gerações)
│   ├── historico_baselines_dl_lstm_gru.csv           # Métricas dos baselines de Deep Learning
│   ├── PETR4_close_com_factor_2000-2020.txt          # Série temporal bruta PETR4 (5.198 cotações)
│   └── PETR4_serie_temporal_com_datas.csv            # Série temporal indexada por datas
│
├── 04_Codigo_Fonte_App_Studio/
│   └── (Aplicação R Shiny completa ESNAUTO Benchmark Studio)
│
└── 05_Scripts_de_Reproducao/
    ├── gerar_todas_as_figuras.R                      # Script R que gera automaticamente todas as figuras
    └── ESN_Acoes_petr4_v2.8.1.2.R                    # Implementação canônica da ESN
```

---

### 🏆 SÍNTESE DOS PRINCIPAIS RESULTADOS CIENTÍFICOS

1. **Volume Computacional:** Foram realizadas **30 rodadas oficiais de produção** de Algoritmo Genético em busca profunda de **10.000 gerações**, totalizando mais de **25 horas e 40 minutos** de processamento local em dataset de 5.198 amostras (50% Treino, 25% Validação, 25% Teste Cego).
2. **Superioridade sobre Deep Learning Recorrente:** Todas as 30 configurações de ESN superaram a **LSTM** ($MAE = 0.4521, R^2 = 0.9839$) e a **GRU** ($MAE = 0.3566, R^2 = 0.9912$) em erro no teste cego.
3. **Recordes Oficiais Obtidos:**
   * **Campeã Geral de Teste:** ESN Onda 2 (*Laplace + Normal*) $ightarrow$ **MAE Teste = 0.3272**, **$R^2$ = 0.9940** (Score: **98.8 / 100**).
   * **Campeã de Aderência:** ESN Onda 2 (*Laplace + Cauchy*) $ightarrow$ **Menor RMSE = 0.4953**, **Maior $R^2$ = 0.9941**.
   * **Eficiência:** Tempo de treino Ridge da ESN: **0.05 segundos** (**>500x mais rápida** que as redes profundas).

---

### 🚀 COMO EXECUTAR O APLICATIVO WEB OU REPRODUZIR AS FIGURAS

* **Para abrir o aplicativo interativo no R / RStudio:**
  ```r
  shiny::runApp("04_Codigo_Fonte_App_Studio", port = 8080)
  ```
* **Para regenerar todas as figuras em PDF/PNG:**
  ```bash
  Rscript 05_Scripts_de_Reproducao/gerar_todas_as_figuras.R
  ```

Estou à total disposição para eventuais dúvidas ou esclarecimentos!

Atenciosamente,  
**Maycon Garcia Silva**
