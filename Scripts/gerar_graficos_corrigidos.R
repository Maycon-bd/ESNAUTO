# ============================================================
# gerar_graficos_corrigidos.R
# Regenera os gráficos de Validação e Teste com ylim=c(0,40)
# Cenário: Win Normal | W Normal | N=3
# ============================================================
#
# USO — via terminal (na pasta raiz do projeto ESNAUTO):
#   Rscript Scripts/gerar_graficos_corrigidos.R
#
# OU — via RStudio:
#   Defina o working directory como a pasta raiz (ESNAUTO/)
#   e execute o script.
#
# Os gráficos serão salvos em:
#   resultados_tcc/grafico_validacao_corrigido.png
#   resultados_tcc/grafico_teste_corrigido.png
# ============================================================

# ── 1. Caminhos ──────────────────────────────────────────────
proj_root <- getwd()          # Deve ser a pasta raiz ESNAUTO/
data_dir  <- file.path(proj_root, "Scripts", "data")
out_dir   <- file.path(proj_root, "resultados_tcc")
dir.create(out_dir, showWarnings = FALSE, recursive = TRUE)

cat("Raiz do projeto:", proj_root, "\n")
cat("Pasta de dados: ", data_dir, "\n")
cat("Pasta de saida: ", out_dir, "\n\n")

# ── 2. Carregar dados ────────────────────────────────────────
data_fac_raw <- as.matrix(read.csv2(
  file.path(data_dir, "PETR4_close com factor_2000-2020.txt"),
  header = FALSE
))
data <- as.numeric(data_fac_raw)

data_date_fac <- as.matrix(read.csv2(
  file.path(data_dir, "PETR4_close com factor_2000-2020_com data.csv"),
  header = FALSE
))
n_rows         <- nrow(data_date_fac)
data_date_fac1 <- as.Date(as.character(data_date_fac[1:n_rows, 1]))

cat("Dados carregados:", length(data), "registros\n")
cat("Range dos dados: ", min(data), "a", max(data), "\n")

# ── 3. Partições ─────────────────────────────────────────────
treino <- 2600   # 50%
valida <- 1299   # 25%
teste  <- 1299   # 25%

inSize  <- 1
outSize <- 1

# ── 4. Hiperparâmetros do cenário Win Normal | W Normal | N=3 ─
a             <- 0.870902030197374
sr            <- 0.406802420062409
initLen       <- 9
tam_reservoir <- 3
reg           <- 2.2289743444227e-05

cat("\nHiperparâmetros:\n")
cat("  a =", a, "| sr =", sr, "| initLen =", initLen,
    "| N =", tam_reservoir, "| reg =", reg, "\n\n")

# ── 5. Matrizes Win e W (Normal, seed fixo) ──────────────────
set.seed(42)
Win <- matrix(rnorm(tam_reservoir * 2, mean = 0, sd = 1),
              nrow = tam_reservoir, ncol = 2)
W_base <- matrix(rnorm(tam_reservoir^2, mean = 0, sd = 1),
                 nrow = tam_reservoir, ncol = tam_reservoir)

# Normalizar para raio espectral = 1
rhoW_base <- abs(eigen(W_base, only.values = TRUE)$values[1])
W_base    <- W_base / rhoW_base

# ── 6. VALIDAÇÃO ─────────────────────────────────────────────
cat("Executando Validacao...\n")
treino_valida <- data[1:(treino + valida)]

W_v <- sr * W_base   # raio espectral = sr

# Coleta de estados (washout + treino)
X_v <- matrix(0, 1 + inSize + tam_reservoir, treino - initLen)
x   <- rep(0, tam_reservoir)
for (t in 1:treino) {
  u <- treino_valida[t]
  x <- (1 - a) * x + a * tanh(Win %*% rbind(1, u) + W_v %*% x)
  if (t > initLen) X_v[, t - initLen] <- rbind(1, u, x)
}

# Wout por Ridge Regression
Yt_v  <- matrix(treino_valida[(initLen + 2):(treino + 1)], 1)
Wout_v <- Yt_v %*% t(X_v) %*% solve(X_v %*% t(X_v) +
            reg * diag(1 + inSize + tam_reservoir))

# Previsão na validação
Y_val <- matrix(0, outSize, valida)
u     <- treino_valida[treino + 1]
for (t in 1:valida) {
  x        <- (1 - a) * x + a * tanh(Win %*% rbind(1, u) + W_v %*% x)
  y        <- Wout_v %*% rbind(1, u, x)
  Y_val[, t] <- y
  u        <- treino_valida[treino + t + 1]
}

mae_valida  <- mean(abs(treino_valida[(treino + 2):(treino + valida)] -
                         Y_val[outSize, 1:(valida - 1)]))
rmse_valida <- sqrt(mean((treino_valida[(treino + 2):(treino + valida)] -
                           Y_val[outSize, 1:(valida - 1)])^2))
cat("  MAE  Validacao =", round(mae_valida,  6), "\n")
cat("  RMSE Validacao =", round(rmse_valida, 6), "\n\n")

# ── 7. TESTE ─────────────────────────────────────────────────
cat("Executando Teste...\n")
treina_testa <- c(data[1:treino],
                  data[(treino + valida + 1):(treino + valida + teste)])

W_t <- sr * W_base   # mesmo W reescalado

X_t <- matrix(0, 1 + inSize + tam_reservoir, treino - initLen)
x   <- rep(0, tam_reservoir)
for (t in 1:treino) {
  u <- treina_testa[t]
  x <- (1 - a) * x + a * tanh(Win %*% rbind(1, u) + W_t %*% x)
  if (t > initLen) X_t[, t - initLen] <- rbind(1, u, x)
}

Yt_t  <- matrix(treina_testa[(initLen + 2):(treino + 1)], 1)
Wout_t <- Yt_t %*% t(X_t) %*% solve(X_t %*% t(X_t) +
            reg * diag(1 + inSize + tam_reservoir))

Y_tst <- matrix(0, outSize, teste)
u     <- treina_testa[treino + 1]
for (t in 1:teste) {
  x        <- (1 - a) * x + a * tanh(Win %*% rbind(1, u) + W_t %*% x)
  y        <- Wout_t %*% rbind(1, u, x)
  Y_tst[, t] <- y
  u        <- treina_testa[treino + t + 1]
}

mae_teste  <- mean(abs(treina_testa[(treino + 2):(treino + teste)] -
                        Y_tst[outSize, 1:(teste - 1)]))
rmse_teste <- sqrt(mean((treina_testa[(treino + 2):(treino + teste)] -
                          Y_tst[outSize, 1:(teste - 1)])^2))
cat("  MAE  Teste =", round(mae_teste,  6), "\n")
cat("  RMSE Teste =", round(rmse_teste, 6), "\n\n")

# ── 8. Índices de datas ───────────────────────────────────────
max_d      <- length(data_date_fac1)

# Validação: posições treino+1 até treino+valida
idx_val    <- (treino + 1):(treino + valida)
idx_val    <- idx_val[idx_val <= max_d]
datas_val  <- data_date_fac1[idx_val]
n_val      <- length(idx_val)

# Teste: posições treino+valida+1 até treino+valida+teste
idx_tst    <- (treino + valida + 1):(treino + valida + teste)
idx_tst    <- idx_tst[idx_tst <= max_d]
datas_tst  <- data_date_fac1[idx_tst]
n_tst      <- length(idx_tst)

# ── 9. GRÁFICO VALIDAÇÃO — ylim c(0,40) ──────────────────────
out_val <- file.path(out_dir, "grafico_validacao_corrigido.png")
png(out_val, width = 1200, height = 700, res = 120)

plot(
  x    = datas_val,
  y    = treino_valida[idx_val],
  ylim = c(0, 40),
  type = "l",
  col  = "green",
  lwd  = 2,
  xlab = "Data",
  ylab = "Precos observados e previstos com factor (R$)",
  main = "Validacao — ESN PETR4 | Win Normal | W Normal | N=3"
)
lines(datas_val, c(Y_val[outSize, 1:n_val]), col = "black", lwd = 1)
legend(
  "topright",
  legend = c("Serie alvo", "Serie prevista"),
  col    = c("green", "black"),
  lty    = 1,
  bty    = "n"
)
dev.off()
cat("Grafico Validacao salvo:", out_val, "\n")

# ── 10. GRÁFICO TESTE — ylim c(0,40) ─────────────────────────
out_tst <- file.path(out_dir, "grafico_teste_corrigido.png")
png(out_tst, width = 1200, height = 700, res = 120)

plot(
  x    = datas_tst,
  y    = data[idx_tst],
  ylim = c(0, 40),
  type = "l",
  col  = "green",
  lwd  = 2,
  xlab = "Data",
  ylab = "Precos observados com factor e previstos com factor (R$)",
  main = "Teste — ESN PETR4 | Win Normal | W Normal | N=3"
)
lines(datas_tst, c(Y_tst[outSize, 1:n_tst]), col = "black", lwd = 1)
legend(
  "topleft",
  legend = c("Serie alvo", "Serie prevista"),
  col    = c("green", "black"),
  lty    = 1,
  bty    = "n"
)
dev.off()
cat("Grafico Teste salvo:     ", out_tst, "\n")

cat("\n=== CONCLUIDO ===\n")
cat("Ambos os graficos com ylim=c(0,40) salvos em:\n")
cat(" ", out_dir, "\n")
