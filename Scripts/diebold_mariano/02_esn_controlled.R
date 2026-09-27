source("Scripts/diebold_mariano/01_prepare_data.R")
esn_controlled <- function(d, cfg, smoke, out) {
  p <- cfg$esn; n <- as.integer(p$tam_reservoir); end_train <- max(d$train)
  u <- runif(n * 2L) - .5
  Win <- matrix(-sign(u) * log(1 - 2 * abs(u)) / sqrt(2), nrow = n)
  W <- matrix(rnorm(n * n), nrow = n)
  rho <- max(Mod(eigen(W, only.values = TRUE)$values))
  stopifnot(is.finite(rho), rho > 0)
  Ws <- p$sr * W / rho
  origins <- seq.int(as.integer(p$initLen) + 1L, end_train - 1L)
  targets <- origins + 1L
  stopifnot(all(targets %in% d$train), !any(targets %in% c(d$validation, d$test)),
    all(targets <= end_train))
  X <- matrix(0, n + 2L, length(origins)); state <- rep(0, n)
  for (t in seq_len(end_train - 1L)) {
    state <- (1 - p$a) * state + p$a * tanh(Win %*% c(1, d$y[t]) + Ws %*% state)
    if (t > p$initLen) X[, t - p$initLen] <- c(1, d$y[t], state)
  }
  A <- X %*% t(X) + p$reg * diag(n + 2L)
  solver <- "solve"
  inv <- tryCatch(solve(A), error = function(e) { solver <<- "pracma::pinv"; pracma::pinv(A) })
  Wout <- matrix(d$y[targets], nrow = 1L) %*% t(X) %*% inv
  frozen <- Wout
  predictions <- numeric(length(d$test))
  # State currently consumed 1:(train_end-1). Consume remaining train then
  # every validation observation, and finally preceding test observations.
  for (t in seq.int(end_train, length(d$y) - 1L)) {
    state <- (1 - p$a) * state + p$a * tanh(Win %*% c(1, d$y[t]) + Ws %*% state)
    if ((t + 1L) %in% d$test) predictions[match(t + 1L, d$test)] <-
      as.numeric(Wout %*% c(1, d$y[t], state))
  }
  stopifnot(identical(Wout, frozen), all(is.finite(predictions)))
  saveRDS(list(Win = Win, W = W, W_scaled = Ws, Wout = Wout), file.path(out, "matrices.rds"))
  list(predictions = data.frame(data = d$dates[d$test], real = d$y[d$test],
    previsto = predictions, data_origem = d$dates[d$test - 1L], h = 1L),
    train_target_indices = targets, state_origins = origins, solver = solver,
    source_md5 = d$source_md5, n_train = length(d$train))
}
if (sys.nframe() == 0L) dm_cli("esn", esn_controlled)
