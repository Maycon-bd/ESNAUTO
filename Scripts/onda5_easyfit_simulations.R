# =============================================================================
# onda5_easyfit_simulations.R
# 🌊 ONDA 5: AJUSTES PARAMÉTRICOS EMPÍRICOS (EASYFIT BEST-FITS PETR4 50%)
# Distribuições:
#   1. Power Function (alpha=0.50339, a=2.4759, b=34.548)
#   2. Dagum (4P)     (k=0.30596, alpha=2.0664, beta=17.968, gamma=2.4775)
#   3. Johnson SB     (gamma=0.56742, delta=0.49965, lambda=27.881, xi=1.9165)
# =============================================================================

if (dir.exists("app")) {
  setwd("app")
}

source("utils/data_prep.R", local = TRUE)
source("utils/metrics.R", local = TRUE)
source("utils/esn_core.R", local = TRUE)
source("utils/ga_engine.R", local = TRUE)

cat("=================================================================================\n")
cat("  🌊 ONDA 5: AJUSTES EMPÍRICOS EASYFIT (POWER FUNCTION, DAGUM 4P, JOHNSON SB)\n")
cat("=================================================================================\n\n")

# 1. Carregar dados
dados <- carregar_dados_petr4()
dados_split <- dividir_dados(dados)

cat(sprintf("Série: PETR4 com fator | Total: %d amostras\n", length(dados)))
cat(sprintf("Particionamento: Treino=%d (50%%) | Validação=%d (25%%) | Teste=%d (25%%)\n\n",
            dados_split$idx$treino_n, dados_split$idx$valida_n, dados_split$idx$teste_n))

# 2. Definição da Grade de Cenários da Onda 5
cenarios_onda5 <- list(
  # Bloco 1: Power Function
  list(win = "Power Function", w = "Normal",        tag = "Power × Normal"),
  list(win = "Power Function", w = "Uniforme",      tag = "Power × Uniforme"),
  list(win = "Power Function", w = "Power Function", tag = "Power × Power"),
  
  # Bloco 2: Dagum (4P)
  list(win = "Dagum (4P)",     w = "Normal",        tag = "Dagum4P × Normal"),
  list(win = "Dagum (4P)",     w = "Uniforme",      tag = "Dagum4P × Uniforme"),
  list(win = "Dagum (4P)",     w = "Dagum (4P)",    tag = "Dagum4P × Dagum4P"),
  
  # Bloco 3: Johnson SB
  list(win = "Johnson SB",     w = "Normal",        tag = "JohnsonSB × Normal"),
  list(win = "Johnson SB",     w = "Uniforme",      tag = "JohnsonSB × Uniforme"),
  list(win = "Johnson SB",     w = "Johnson SB",    tag = "JohnsonSB × JohnsonSB"),
  
  # Bloco 4: Híbridos Cruzados EasyFit
  list(win = "Power Function", w = "Dagum (4P)",    tag = "Power × Dagum4P"),
  list(win = "Dagum (4P)",     w = "Johnson SB",    tag = "Dagum4P × JohnsonSB"),
  list(win = "Johnson SB",     w = "Power Function", tag = "JohnsonSB × Power")
)

cat(sprintf("Total de Cenários a Executar: %d\n", length(cenarios_onda5)))
cat("Configuração GA: 200 Gerações | População: 16 | Inicialização: LHS | Anti-Estagnação: Cataclismo\n")
cat("---------------------------------------------------------------------------------\n\n")

resultados_lista <- list()

for (i in seq_along(cenarios_onda5)) {
  sc <- cenarios_onda5[[i]]
  cat(sprintf("[%02d/%02d] Executando GA para %s (Win: %s | W: %s)...\n", 
              i, length(cenarios_onda5), sc$tag, sc$win, sc$w))
  
  t0 <- proc.time()
  res_ga <- otimizar_esn_ga_live(
    dados = dados,
    win_dist = sc$win,
    w_dist = sc$w,
    maxiter = 200,
    pop_size = 16,
    anti_estagnacao = TRUE,
    set_progress = function(p, msg) {
      pct <- round(p * 100)
      if (pct %in% c(25, 50, 75, 100)) {
        cat(sprintf("    -> Progresso %d%% — %s\n", pct, msg))
      }
    }
  )
  
  p <- res_ga$params
  m_val <- res_ga$validacao$metricas_valida
  m_test <- res_ga$teste$metricas_teste
  tempo_sc <- (proc.time() - t0)["elapsed"]
  
  cat(sprintf("    ✔ Concluído em %.1fs | MAE Val: %.6f | MAE Teste: %.6f | RMSE Teste: %.6f | R² Teste: %.6f\n\n",
              tempo_sc, m_val$MAE, m_test$MAE, m_test$RMSE, m_test$R2))
  
  resultados_lista[[i]] <- data.frame(
    ID = sprintf("ONDA5_RUN_%02d", i),
    Win = sc$win,
    W = sc$w,
    Tag = sc$tag,
    a = p$a,
    sr = p$sr,
    initLen = p$initLen,
    Nx = p$tam_reservoir,
    lambda = p$reg,
    MAE_Valida = m_val$MAE,
    RMSE_Valida = m_val$RMSE,
    MAE_Teste = m_test$MAE,
    RMSE_Teste = m_test$RMSE,
    MAPE_Teste = m_test$MAPE,
    R2_Teste = m_test$R2,
    Tempo_s = tempo_sc,
    stringsAsFactors = FALSE
  )
}

df_resultados <- do.call(rbind, resultados_lista)

# Ordenar por MAE de Teste
df_ordenado <- df_resultados[order(df_resultados$MAE_Teste), ]

cat("\n=================================================================================\n")
cat("            🏆 TABELA CLASSIFICATÓRIA DA ONDA 5 (ORDENADA POR MAE TESTE)\n")
cat("=================================================================================\n\n")
print(df_ordenado[, c("Tag", "MAE_Valida", "MAE_Teste", "RMSE_Teste", "R2_Teste", "Nx", "a", "sr", "Tempo_s")], row.names = FALSE)

# Salvar relatório em Markdown
arquivo_relatorio <- "../docs/09_onda_5_ajustes_empiricos_easyfit.md"
if (!dir.exists("../docs")) {
  arquivo_relatorio <- "09_onda_5_ajustes_empiricos_easyfit.md"
}

cat(sprintf("\nSalvando consolidação em %s...\n", arquivo_relatorio))

md_content <- c(
  "# 🌊 Onda 5: Ajustes Paramétricos Empíricos do EasyFit (PETR4 2000–2020)",
  "## *Power Function, Dagum (4P) e Johnson SB sob GA + LHS + Cataclismo*",
  "",
  "> **Status**: ✅ **100% Concluído**  ",
  sprintf("> **Total de Cenários**: %d execuções  ", nrow(df_resultados)),
  "> **Parâmetros das Distribuições do EasyFit (Ajustadas na Série de Treino 50%)**:  ",
  "> - **Power Function**: $\\alpha = 0{,}50339, a = 2{,}4759, b = 34{,}548$",
  "> - **Dagum (4P)**: $k = 0{,}30596, \\alpha = 2{,}0664, \\beta = 17{,}968, \\gamma = 2{,}4775$",
  "> - **Johnson SB**: $\\gamma = 0{,}56742, \\delta = 0{,}49965, \\lambda = 27{,}881, \\xi = 1{,}9165$",
  "",
  "---",
  "",
  "### 📋 Tabela Comparativa Consolidada da Onda 5",
  "",
  "| ID | Combinação | $W_{in}$ | $W$ | $a$ | $sr$ | $initLen$ | $N_x$ | $\\lambda$ | MAE Val | MAE Teste | RMSE Teste | $R^2$ Teste | Tempo (s) |",
  "| :--- | :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |"
)

for (r in 1:nrow(df_resultados)) {
  row <- df_resultados[r, ]
  md_content <- c(md_content, sprintf(
    "| `%s` | **%s** | %s | %s | %.3f | %.3f | %d | %d | $%.2e$ | %.6f | **%.6f** | %.6f | %.4f | %.1fs |",
    row$ID, row$Tag, row$Win, row$W, row$a, row$sr, row$initLen, row$Nx, row$lambda,
    row$MAE_Valida, row$MAE_Teste, row$RMSE_Teste, row$R2_Teste, row$Tempo_s
  ))
}

writeLines(md_content, arquivo_relatorio)
cat("✅ Experimento da Onda 5 finalizado e relatório salvo com sucesso!\n")
