import os
import shutil
import zipfile

print("===================================================================")
print("[ETAPA] RECRIANDO PACOTE DO ORIENTADOR (COM LINK DO GITHUB)")
print("===================================================================")

base_dir = r"d:\MAYCON\PROJETOS\ESNAUTO"
staging_dir = os.path.join(base_dir, "pacote_orientador_tfc")
zip_output = os.path.join(base_dir, "PACOTE_TFC_ORIENTADOR_MAYCON_GARCIA_SILVA.zip")

# Limpar pasta de staging
if os.path.exists(staging_dir):
    shutil.rmtree(staging_dir)
os.makedirs(staging_dir, exist_ok=True)

# 1. Criar subpastas
pastas = [
    "01_Relatorios_Tecnicos_e_Metodologia",
    "02_Figuras_Alta_Resolucao",
    "03_Planilhas_e_Dados_Brutos"
]
for p in pastas:
    os.makedirs(os.path.join(staging_dir, p), exist_ok=True)

# 2. Copiar Relatórios Técnicos e Metodologia
relatorios = [
    ("docs/08_comparativo_quatro_ondas_estocasticas.md", "01_Relatorios_Tecnicos_e_Metodologia/Relatorio_Tecnico_4_Ondas_Estocasticas.md"),
    ("docs/06_secao_artigo_tfc_otimizacao_ga.md", "01_Relatorios_Tecnicos_e_Metodologia/Metodologia_GA_LHS_Cataclismo.md"),
    ("reports/MayconGarciaSilva_monografia.docx", "01_Relatorios_Tecnicos_e_Metodologia/Monografia_TFC_MayconGarciaSilva.docx"),
    ("reports/Relatorio_Automacao_ESN.docx", "01_Relatorios_Tecnicos_e_Metodologia/Relatorio_Automacao_ESN.docx")
]
for src, dst in relatorios:
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

# 5. Criar GUIA DO ORIENTADOR com Link Público do GitHub
guia_conteudo = """# GUIA DE AVALIACAO DOS RESULTADOS DO TFC — PARA O ORIENTADOR
## Tema: Previsao de Series Temporais Financeiras (PETR4) via Echo State Networks com Distribuicoes Nao-Gaussianas e Algoritmo Genetico Hibrido (LHS + Cataclismo)
Autor: Maycon Garcia Silva  
Data: Agosto / 2026  
Repositorio Publico no GitHub: https://github.com/Maycon-bd/ESNAUTO

---

### Prezado(a) Professor(a) Orientador(a),

Este pacote contem os relatorios tecnicos, dados brutos consolidados das 30 rodadas experimentais das 4 Ondas Estocasticas e figuras em alta resolucao desenvolvidos no Trabalho de Fim de Curso (TFC).

O codigo-fonte completo do aplicativo web (ESNAUTO Benchmark Studio) e os scripts de reproducao estao disponiveis publicamente no GitHub:
👉 https://github.com/Maycon-bd/ESNAUTO

---

### ESTRUTURA DESTE PACOTE

├── 01_Relatorios_Tecnicos_e_Metodologia/
│   ├── Relatorio_Tecnico_4_Ondas_Estocasticas.md      # Relatorio completo das 30 rodadas oficiais
│   ├── Metodologia_GA_LHS_Cataclismo.md              # Formulacao do GA (59 bits, LHS e CHC)
│   ├── Monografia_TFC_MayconGarciaSilva.docx         # Versao editavel em Word da Monografia
│   └── Relatorio_Automacao_ESN.docx                 # Relatorio tecnico do pipeline
│
├── 02_Figuras_Alta_Resolucao/
│   ├── fig1_boxplot_mae_ondas.png / .pdf             # Boxplot de erro MAE no teste cego vs DL
│   ├── fig2_tempo_treinamento_speedup.png / .pdf     # Speedup >500x da ESN vs LSTM/GRU (escala log)
│   ├── fig3_campeoes_teste_serie.png / .pdf          # Serie temporal teste out-of-sample vs real
│   ├── fig4_dispersao_residuos.png / .pdf            # Dispersao Real x Previsto (R²=0.9940) e residuos
│   └── fig5_ranking_multicriterio.png / .pdf         # Ranking oficial ponderado multicriterio (Score 0-100)
│
└── 03_Planilhas_e_Dados_Brutos/
    ├── historico_30_rodadas_ga_4_ondas.csv           # Dados brutos das 30 rodadas oficiais (GA 10.000 geracoes)
    ├── historico_baselines_dl_lstm_gru.csv           # Metricas dos baselines de Deep Learning (LSTM e GRU)
    ├── PETR4_close_com_factor_2000-2020.txt          # Serie temporal bruta PETR4 (5.198 cotacoes)
    └── PETR4_serie_temporal_com_datas.csv            # Serie temporal indexada por datas

---

### SINTESE DOS PRINCIPAIS RESULTADOS EXPERIMENTAIS

1. Volume Computacional: Foram realizadas 30 rodadas oficiais de producao de Algoritmo Genetico em busca profunda de 10.000 geracoes, totalizando mais de 25 horas e 40 minutos de processamento local em dataset de 5.198 amostras (50% Treino, 25% Validacao, 25% Teste Cego).
2. Superioridade sobre Deep Learning Recorrente: Todas as 30 configuracoes de ESN superaram a LSTM (MAE = 0.4521, R² = 0.9839) e a GRU (MAE = 0.3566, R² = 0.9912) em erro no teste cego.
3. Recordes Oficiais Obtidos:
   * Campea Geral de Teste: ESN Onda 2 (Laplace + Normal) -> MAE Teste = 0.3272, R² = 0.9940 (Score: 98.8 / 100).
   * Campea de Aderencia: ESN Onda 2 (Laplace + Cauchy) -> Menor RMSE = 0.4953, Maior R² = 0.9941.
   * Eficiencia: Tempo de treino Ridge da ESN: 0.05 segundos (>500x mais rapida que as redes profundas).

---

### CODIGO-FONTE E REPRODUCAO NO GITHUB

Todo o codigo-fonte do aplicativo web Shiny (ESNAUTO Studio), os modulos de redes neurais e os scripts de reproducao automatizada estao versionados e acessiveis no repositorio:
https://github.com/Maycon-bd/ESNAUTO

Atenciosamente,  
Maycon Garcia Silva
"""

with open(os.path.join(staging_dir, "GUIA_DO_ORIENTADOR.md"), "w", encoding="utf-8") as f:
    f.write(guia_conteudo)
print("  + GUIA_DO_ORIENTADOR.md criado com o link do GitHub!")

# 6. Compactar
print(f"\nCompactando pasta no arquivo {zip_output}...")
with zipfile.ZipFile(zip_output, 'w', zipfile.ZIP_DEFLATED) as zf:
    for root, dirs, files in os.walk(staging_dir):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, staging_dir)
            zf.write(full_path, arcname=rel_path)

print("\n===================================================================")
print(f"[SUCESSO] PACOTE FINAL GERADO COM SUCESSO!")
print(f"Localizacao: {zip_output}")
print(f"Tamanho: {os.path.getsize(zip_output) / 1024 / 1024:.2f} MB")
print("===================================================================")
