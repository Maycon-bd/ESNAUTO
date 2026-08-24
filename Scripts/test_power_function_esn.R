# =============================================================================
# test_power_function_esn.R
# Execução e Avaliação da Distribuição Power Function na ESN (PETR4)
# =============================================================================

# Definir diretório de trabalho base
if (dir.exists("app")) {
  setwd("app")
}

source("utils/data_prep.R", local = TRUE)
source("utils/metrics.R", local = TRUE)
source("utils/esn_core.R", local = TRUE)
source("utils/ga_engine.R", local = TRUE)

cat("=================================================================\n")
cat("  EXPERIMENTO ESN COM DISTRIBUIÇÃO POWER FUNCTION (PETR4)\n")
cat("=================================================================\n\n")

# 1. Carregar Dados
dados <- carregar_dados_petr4()
dados_split <- dividir_dados(dados)

cat(sprintf("Total de Amostras: %d\n", length(dados)))
cat(sprintf("Treino: %d | Validação: %d | Teste Cego: %d\n\n", 
            dados_split$idx$treino_n, dados_split$idx$valida_n, dados_split$idx$teste_n))

# 2. Executar Otimização Rápida com GA + LHS + Cataclismo para Power Function
cat("-----------------------------------------------------------------\n")
cat("🚀 Rodando Otimização GA (LHS + Cataclismo - 200 Gerações, Pop=16)...\n")
cat("   Cenário 1: Win = Power Function | W = Normal\n")
cat("   Cenário 2: Win = Power Function | W = Power Function\n")
cat("-----------------------------------------------------------------\n\n")

cenarios_ga <- list(
  list(win = "Power Function", w = "Normal"),
  list(win = "Power Function", w = "Power Function"),
  list(win = "Normal", w = "Power Function")
)

resultados_resumo <- list()

for (sc in cenarios_ga) {
  nome_sc <- paste0("Win: ", sc$win, " | W: ", sc$w)
  cat(sprintf("\n>>> Otimizando %s...\n", nome_sc))
  
  res_ga <- otimizar_esn_ga_live(
    dados = dados,
    win_dist = sc$win,
    w_dist = sc$w,
    maxiter = 200,
    pop_size = 16,
    anti_estagnacao = TRUE,
    set_progress = function(p, msg) {
      if (round(p * 100) %% 25 == 0) {
        cat(sprintf("    [Progresso %.0f%%] %s\n", p * 100, msg))
      }
    }
  )
  
  p <- res_ga$params
  m_val <- res_ga$validacao$metricas_valida
  m_test <- res_ga$teste$metricas_teste
  
  cat(sprintf("\n  Parâmetros Ótimos Encontrados:\n"))
  cat(sprintf("    a = %.6f | sr = %.6f | initLen = %d | Nx = %d | reg = %.6e\n",
              p$a, p$sr, p$initLen, p$tam_reservoir, p$reg))
  cat(sprintf("  Métricas Validação: MAE = %.6f | RMSE = %.6f | R² = %.6f\n",
              m_val$MAE, m_val$RMSE, m_val$R2))
  cat(sprintf("  Métricas Teste:     MAE = %.6f | RMSE = %.6f | R² = %.6f\n",
              m_test$MAE, m_test$RMSE, m_test$R2))
  cat(sprintf("  Tempo de execução:  %.2f s\n", res_ga$tempo))
  
  resultados_resumo[[nome_sc]] <- data.frame(
    Cenario = nome_sc,
    a = p$a,
    sr = p$sr,
    initLen = p$initLen,
    Nx = p$tam_reservoir,
    lambda = p$reg,
    MAE_Valida = m_val$MAE,
    RMSE_Valida = m_val$RMSE,
    MAE_Teste = m_test$MAE,
    RMSE_Teste = m_test$RMSE,
    R2_Teste = m_test$R2,
    Tempo_s = res_ga$tempo
  )
}

# Consolidar Tabela
df_final <- do.call(rbind, resultados_resumo)

cat("\n=================================================================\n")
cat("                   TABELA FINAL DE RESULTADOS\n")
cat("=================================================================\n")
print(df_final, row.names = FALSE)
cat("\n=================================================================\n")
