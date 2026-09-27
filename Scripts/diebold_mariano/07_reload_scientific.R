# Fresh-process reload only. No fit, random matrices, ridge estimation or DM.
source("Scripts/diebold_mariano/01_prepare_data.R")
a <- commandArgs(trailingOnly = TRUE)
stopifnot(length(a) == 2L, a[1] %in% c("esn", "gru", "lstm"))
m <- a[1]; run <- normalizePath(a[2], winslash = "/", mustWork = TRUE)
stopifnot(Sys.getenv("ESNAUTO_AUTHORIZE_SCIENTIFIC") == "YES")
out <- file.path(run, "validation", paste0(m, "_reload"))
if (dir.exists(out)) stop("Reload output already exists; refusing overwrite")
dir.create(out)
dm_seed(m != "esn")
d <- prepare_dm_data(FALSE); cfg <- dm_config()
original <- readRDS(file.path(run, m, "result.rds"))
stopifnot(!original$smoke, original$seed == DM_SEED)
if (m == "esn") {
  mat <- readRDS(file.path(run, "esn/matrices.rds"))
  Win <- mat$Win; W <- mat$W; Wout <- mat$Wout; Ws <- mat$W_scaled
  stopifnot(identical(dim(Win), c(22L, 2L)), identical(dim(W), c(22L, 22L)),
    identical(dim(Wout), c(1L, 24L)),
    max(abs(Ws - cfg$esn$sr * W / max(Mod(eigen(W, only.values = TRUE)$values)))) < 1e-14)
  state <- rep(0, 22); pred <- numeric(length(d$test)); used <- integer()
  for (t in seq_len(length(d$y) - 1L)) {
    state <- (1 - cfg$esn$a) * state + cfg$esn$a * tanh(Win %*% c(1, d$y[t]) + Ws %*% state)
    if ((t + 1L) %in% d$test) {
      pred[match(t + 1L, d$test)] <- as.numeric(Wout %*% c(1, d$y[t], state))
      used <- c(used, t)
    }
  }
  stopifnot(identical(used, d$test - 1L))
} else {
  scale <- readRDS(file.path(run, m, "normalization.rds"))
  stopifnot(identical(scale, d$scale))
  w <- dm_windows(d, d$test)
  model <- keras3::load_model(file.path(run, "models", paste0(m, "_seed_20260926.keras")))
  pred <- as.numeric(predict(model, w$x, verbose = 0L)) * (scale$max - scale$min) + scale$min
  stopifnot(identical(original$test_input_indices, w$input_indices))
}
stopifnot(length(pred) == nrow(original$predictions), all(is.finite(pred)))
delta <- max(abs(pred - original$predictions$previsto))
# Predeclared reload tolerance: R double 1e-12; DL float32 predictions 1e-6.
tol <- if (m == "esn") 1e-12 else 1e-6
stopifnot(delta <= tol)
write.csv(data.frame(data = d$dates[d$test], previsto_reload = pred),
  file.path(out, "predictions_reload.csv"), row.names = FALSE)
jsonlite::write_json(list(model = m, n = length(pred), max_abs_diff_reload = delta,
  tolerance = tol, exact_numerical_match = identical(pred, original$predictions$previsto),
  status = "PASS", retrained = FALSE, fresh_process = TRUE),
  file.path(out, "reload_status.json"), auto_unbox = TRUE, pretty = TRUE)
cat(m, "reload PASS; max_abs_diff =", format(delta, digits = 17), "\n")
