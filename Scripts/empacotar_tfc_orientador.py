import os
import shutil
import zipfile

print("===================================================================")
print("[ETAPA] CRIANDO PACOTE ESTRUTURADO PARA O ORIENTADOR")
print("===================================================================")

base_dir = r"d:\MAYCON\PROJETOS\ESNAUTO"
staging_dir = os.path.join(base_dir, "pacote_orientador_tfc")
zip_output = os.path.join(base_dir, "PACOTE_TFC_ORIENTADOR_MAYCON_GARCIA_SILVA.zip")

# Limpar pasta de staging se já existir
if os.path.exists(staging_dir):
    shutil.rmtree(staging_dir)
os.makedirs(staging_dir, exist_ok=True)

# 1. Criar subpastas organizadas
pastas = [
    "01_Artigo_e_Monografia",
    "02_Figuras_Alta_Resolucao",
    "03_Planilhas_e_Dados_Brutos",
    "04_Codigo_Fonte_App_Studio",
    "05_Scripts_de_Reproducao"
]
for p in pastas:
    os.makedirs(os.path.join(staging_dir, p), exist_ok=True)

# 2. Copiar Artigos e Textos Acadêmicos
artigos = [
    ("docs/artigo_completo_tfc_esn_petr4.md", "01_Artigo_e_Monografia/Artigo_Completo_TFC_Maycon_Garcia_Silva.md"),
    ("docs/artigo_completo_tfc_esn_petr4.tex", "01_Artigo_e_Monografia/Artigo_LaTeX_IEEE_Maycon_Garcia_Silva.tex"),
    ("docs/08_comparativo_quatro_ondas_estocasticas.md", "01_Artigo_e_Monografia/Relatorio_Tecnico_4_Ondas_Estocasticas.md"),
    ("docs/06_secao_artigo_tfc_otimizacao_ga.md", "01_Artigo_e_Monografia/Metodologia_GA_LHS_Cataclismo.md"),
    ("reports/MayconGarciaSilva_monografia.docx", "01_Artigo_e_Monografia/Monografia_TFC_MayconGarciaSilva.docx"),
    ("reports/Relatorio_Automacao_ESN.docx", "01_Artigo_e_Monografia/Relatorio_Automacao_ESN.docx")
]
for src, dst in artigos:
    s = os.path.join(base_dir, src)
    if os.path.exists(s):
        shutil.copy2(s, os.path.join(staging_dir, dst))
        print(f"  + [01] {dst}")

# 3. Copiar Figuras
figuras_dir = os.path.join(base_dir, "reports/figures")
if os.path.exists(figuras_dir):
    for f in os.listdir(figuras_dir):
        shutil.copy2(os.path.join(figuras_dir, f), os.path.join(staging_dir, "02_Figuras_Alta_Resolucao", f))
        print(f"  + [02] 02_Figuras_Alta_Resolucao/{f}")

# 4. Copiar Dados e Resultados
dados = [
    ("Scripts/results/historico_otimizacoes_ga.csv", "03_Planilhas_e_Dados_Brutos/historico_30_rodadas_ga_4_ondas.csv"),
    ("Scripts/results/historico_dl_benchmark.csv", "03_Planilhas_e_Dados_Brutos/historico_baselines_dl_lstm_gru.csv"),
    ("Scripts/data/PETR4_close com factor_2000-2020.txt", "03_Planilhas_e_Dados_Brutos/PETR4_close_com_factor_2000-2020.txt"),
    ("Scripts/data/PETR4_close com factor_2000-2020_com data.csv", "03_Planilhas_e_Dados_Brutos/PETR4_serie_temporal_com_datas.csv")
]
for src, dst in dados:
    s = os.path.join(base_dir, src)
    if os.path.exists(s):
        shutil.copy2(s, os.path.join(staging_dir, dst))
        print(f"  + [03] {dst}")

# 5. Copiar Código Fonte do App Shiny
app_dir = os.path.join(base_dir, "app")
dst_app = os.path.join(staging_dir, "04_Codigo_Fonte_App_Studio")
for root, dirs, files in os.walk(app_dir):
    rel_root = os.path.relpath(root, app_dir)
    target_dir = os.path.join(dst_app, rel_root) if rel_root != "." else dst_app
    os.makedirs(target_dir, exist_ok=True)
    for f in files:
        shutil.copy2(os.path.join(root, f), os.path.join(target_dir, f))
print("  + [04] 04_Codigo_Fonte_App_Studio/ (Todo o código Shiny incluído)")

# 6. Copiar Scripts de Reprodução
scripts = [
    ("Scripts/gerar_graficos_artigo_finais.R", "05_Scripts_de_Reproducao/gerar_todas_as_figuras.R"),
    ("automate_simulations.py", "05_Scripts_de_Reproducao/automate_simulations.py"),
    ("ESN Acoes-petr4 v2.8.1.2 Maycon G Silva.R", "05_Scripts_de_Reproducao/ESN_Acoes_petr4_v2.8.1.2.R")
]
for src, dst in scripts:
    s = os.path.join(base_dir, src)
    if os.path.exists(s):
        shutil.copy2(s, os.path.join(staging_dir, dst))
        print(f"  + [05] {dst}")

# 7. Criar GUIA DO ORIENTADOR
guia_conteudo = """# 🎓 GUIA DE AVALIAÇÃO DO TFC — PARA O ORIENTADOR
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
   * **Campeã Geral de Teste:** ESN Onda 2 (*Laplace + Normal*) $\rightarrow$ **MAE Teste = 0.3272**, **$R^2$ = 0.9940** (Score: **98.8 / 100**).
   * **Campeã de Aderência:** ESN Onda 2 (*Laplace + Cauchy*) $\rightarrow$ **Menor RMSE = 0.4953**, **Maior $R^2$ = 0.9941**.
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
"""

with open(os.path.join(staging_dir, "GUIA_DO_ORIENTADOR.md"), "w", encoding="utf-8") as f:
    f.write(guia_conteudo)
print("  + GUIA_DO_ORIENTADOR.md criado com sucesso!")

# 8. Compactar tudo no ZIP final
print(f"\nCompactando pasta no arquivo {zip_output}...")
with zipfile.ZipFile(zip_output, 'w', zipfile.ZIP_DEFLATED) as zf:
    for root, dirs, files in os.walk(staging_dir):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, staging_dir)
            zf.write(full_path, arcname=rel_path)

print("\n===================================================================")
print(f"[SUCESSO] PACOTE FINAL DO ORIENTADOR GERADO COM SUCESSO!")
print(f"Localizacao: {zip_output}")
print(f"Tamanho: {os.path.getsize(zip_output) / 1024 / 1024:.2f} MB")
print("===================================================================")
