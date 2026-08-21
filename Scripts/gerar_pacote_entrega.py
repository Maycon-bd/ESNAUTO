import os
import zipfile
import shutil

print("===================================================================")
print("[PACOTE] GERANDO PACOTE DE ENTREGA OFICIAL DO TFC (ZIP & DIRETORIO)")
print("===================================================================")

base_dir = r"d:\MAYCON\PROJETOS\ESNAUTO"
out_zip = os.path.join(base_dir, "entrega_tfc_maycon_garcia_silva.zip")

arquivos_incluir = [
    # Documentos e Artigo
    "docs/artigo_completo_tfc_esn_petr4.md",
    "docs/artigo_completo_tfc_esn_petr4.tex",
    "docs/08_comparativo_quatro_ondas_estocasticas.md",
    "docs/06_secao_artigo_tfc_otimizacao_ga.md",
    "docs/INDEX.md",
    "README.md",
    
    # Resultados e Histórico
    "Scripts/results/historico_otimizacoes_ga.csv",
    "Scripts/results/historico_dl_benchmark.csv",
    
    # Figuras de Alta Resolução
    "reports/figures/fig1_boxplot_mae_ondas.png",
    "reports/figures/fig1_boxplot_mae_ondas.pdf",
    "reports/figures/fig2_tempo_treinamento_speedup.png",
    "reports/figures/fig2_tempo_treinamento_speedup.pdf",
    "reports/figures/fig3_campeoes_teste_serie.png",
    "reports/figures/fig3_campeoes_teste_serie.pdf",
    "reports/figures/fig4_dispersao_residuos.png",
    "reports/figures/fig4_dispersao_residuos.pdf",
    "reports/figures/fig5_ranking_multicriterio.png",
    "reports/figures/fig5_ranking_multicriterio.pdf",
    
    # Scripts de Reprodução
    "Scripts/gerar_graficos_artigo_finais.R",
    "Scripts/data/PETR4_close com factor_2000-2020.txt",
    
    # Código Fonte do App Studio
    "app/app.R",
    "app/utils/data_prep.R",
    "app/utils/metrics.R",
    "app/utils/history_tracker.R",
    "app/utils/ga_engine.R",
    "app/modules/mod_comparacao.R",
    "app/modules/mod_lstm.R",
    "app/modules/mod_gru.R",
    "app/modules/mod_esn.R"
]

with zipfile.ZipFile(out_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
    for rel_path in arquivos_incluir:
        full_path = os.path.join(base_dir, rel_path)
        if os.path.exists(full_path):
            zf.write(full_path, arcname=rel_path)
            print(f"  + Adicionado: {rel_path}")
        else:
            print(f"  ! Arquivo não encontrado: {rel_path}")

print(f"\n[SUCESSO] PACOTE CRIADO COM SUCESSO:")
print(f"   Localizacao: {out_zip}")
print(f"   Tamanho: {os.path.getsize(out_zip) / 1024:.1f} KB")
