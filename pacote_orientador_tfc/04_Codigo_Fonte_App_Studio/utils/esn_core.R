# =============================================================================
# esn_core.R — Funções Centrais de Inferência, Validação e Teste da ESN
# =============================================================================

esn_validacao <- function(dados_split, params, Win, W, Wout = NULL) {
  treino <- dados_split$idx$treino_n
  valida <- dados_split$idx$valida_n
  treino_valida <- dados_split$treino_valida
  
  a <- params$a
  sr <- params$sr
  initLen <- params$initLen
  tam_reservoir <- params$tam_reservoir
  reg <- params$reg
  
  inSize <- 1
  outSize <- 1
  
  t_inicio <- proc.time()
  
  rhoW <- abs(eigen(W, only.values = TRUE)$values[1])
  if (is.na(rhoW) || rhoW == 0) rhoW <- 1
  W_scaled <- sr * W / rhoW
  
  X <- matrix(0, 1 + inSize + tam_reservoir, treino - initLen)
  Yt <- matrix(treino_valida[(initLen + 2):(treino + 1)], 1)
  x <- rep(0, tam_reservoir)
  
  for (t in 1:treino) {
    u <- treino_valida[t]
    x <- (1 - a) * x + a * tanh(Win %*% rbind(1, u) + W_scaled %*% x)
    if (t > initLen)
      X[, t - initLen] <- rbind(1, u, x)
  }
  
  if (is.null(Wout)) {
    X_T <- t(X)
    Wout <- tryCatch({
      Yt %*% X_T %*% solve(X %*% X_T + reg * diag(1 + inSize + tam_reservoir))
    }, error = function(e) {
      Yt %*% X_T %*% pracma::pinv(X %*% X_T + reg * diag(1 + inSize + tam_reservoir))
    })
  }
  
  # Previsão validação
  Y <- matrix(0, outSize, valida)
  u <- treino_valida[treino + 1]
  
  for (t in 1:valida) {
    x <- (1 - a) * x + a * tanh(Win %*% rbind(1, u) + W_scaled %*% x)
    y <- Wout %*% rbind(1, u, x)
    Y[, t] <- y
    u <- treino_valida[treino + t + 1]
  }
  
  # Previsão treino
  Ytr <- matrix(0, outSize, treino)
  u <- treino_valida[1]
  
  for (j in 1:treino) {
    x <- (1 - a) * x + a * tanh(Win %*% rbind(1, u) + W_scaled %*% x)
    y <- Wout %*% rbind(1, u, x)
    Ytr[, j] <- y
    u <- treino_valida[j + 1]
  }
  
  t_fim <- proc.time()
  tempo_exec <- (t_fim - t_inicio)["elapsed"]
  
  real_valida <- treino_valida[(treino + 2):(treino + valida)]
  prev_valida <- as.numeric(Y[outSize, 1:(valida - 1)])
  
  real_treino <- treino_valida[2:treino]
  prev_treino <- as.numeric(Ytr[outSize, 1:(treino - 1)])
  
  metricas_treino <- calcular_todas_metricas(real_treino, prev_treino, tempo_exec)
  metricas_valida <- calcular_todas_metricas(real_valida, prev_valida, tempo_exec)
  
  list(
    previsao_valida = as.numeric(Y),
    previsao_treino = as.numeric(Ytr),
    Wout = Wout,
    metricas_treino = metricas_treino,
    metricas_valida = metricas_valida,
    tempo = tempo_exec
  )
}

esn_teste <- function(dados_split, params, Win, W, Wout) {
  treino_n <- dados_split$idx$treino_n
  teste_n <- dados_split$idx$teste_n
  treina_testa <- dados_split$treina_testa
  
  a <- params$a
  sr <- params$sr
  initLen <- params$initLen
  tam_reservoir <- params$tam_reservoir
  
  inSize <- 1
  outSize <- 1
  
  t_inicio <- proc.time()
  
  rhoW <- abs(eigen(W, only.values = TRUE)$values[1])
  if (is.na(rhoW) || rhoW == 0) rhoW <- 1
  W_scaled <- sr * W / rhoW
  
  X <- matrix(0, 1 + inSize + tam_reservoir, treino_n - initLen)
  Yt <- matrix(treina_testa[(initLen + 2):(treino_n + 1)], 1)
  x <- rep(0, tam_reservoir)
  
  for (t in 1:treino_n) {
    u <- treina_testa[t]
    x <- (1 - a) * x + a * tanh(Win %*% rbind(1, u) + W_scaled %*% x)
    if (t > initLen)
      X[, t - initLen] <- rbind(1, u, x)
  }
  
  # Previsão teste
  Y <- matrix(0, outSize, teste_n)
  u <- treina_testa[treino_n + 1]
  
  for (t in 1:teste_n) {
    x <- (1 - a) * x + a * tanh(Win %*% rbind(1, u) + W_scaled %*% x)
    y <- Wout %*% rbind(1, u, x)
    Y[, t] <- y
    u <- treina_testa[treino_n + t + 1]
  }
  
  # Previsão treino
  Ytr <- matrix(0, outSize, treino_n)
  u <- treina_testa[1]
  
  for (j in 1:treino_n) {
    x <- (1 - a) * x + a * tanh(Win %*% rbind(1, u) + W_scaled %*% x)
    y <- Wout %*% rbind(1, u, x)
    Ytr[, j] <- y
    u <- treina_testa[j + 1]
  }
  
  t_fim <- proc.time()
  tempo_exec <- (t_fim - t_inicio)["elapsed"]
  
  real_teste <- treina_testa[(treino_n + 2):(treino_n + teste_n)]
  prev_teste <- as.numeric(Y[outSize, 1:(teste_n - 1)])
  
  real_treino <- treina_testa[2:treino_n]
  prev_treino <- as.numeric(Ytr[outSize, 1:(treino_n - 1)])
  
  metricas_treino <- calcular_todas_metricas(real_treino, prev_treino, tempo_exec)
  metricas_teste <- calcular_todas_metricas(real_teste, prev_teste, tempo_exec)
  
  list(
    previsao_teste = as.numeric(Y),
    previsao_treino = as.numeric(Ytr),
    metricas_treino = metricas_treino,
    metricas_teste = metricas_teste,
    tempo = tempo_exec
  )
}
