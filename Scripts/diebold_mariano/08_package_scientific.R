# Persist readable scientific artifacts; no training or DM.
source("Scripts/diebold_mariano/05_validate_predictions.R")
a <- commandArgs(trailingOnly = TRUE)
stopifnot(length(a) == 2L, a[1] %in% c("--models", "--freeze"))
run <- normalizePath(a[2], winslash = "/", mustWork = TRUE)
cfg <- dm_config(); d <- prepare_dm_data(FALSE)
stopifnot(isTRUE(cfg$scientific_execution_authorized), Sys.getenv("ESNAUTO_AUTHORIZE_SCIENTIFIC") == "YES")
files <- setNames(lapply(c("esn", "gru", "lstm"), function(m) file.path(run, m, "result.rds")), c("esn", "gru", "lstm"))
b <- validate_dm_predictions(files, FALSE)
values <- lapply(files, readRDS)
# Stronger run-specific gates beyond the generic validator.
stopifnot(identical(values$esn$state_origins, 58:2599),
  identical(values$esn$train_target_indices, 59:2600), length(values$esn$train_target_indices) == 2542L)
for (m in c("gru", "lstm")) {
  r <- values[[m]]; h <- readRDS(file.path(run, m, "training_history.rds"))
  # Keras history's data frame is long: epoch/value/metric.
  stopifnot(r$epochs == 80L, identical(r$train_target_indices, 11:2600),
    identical(readRDS(file.path(run, m, "normalization.rds")), d$scale),
    identical(as.integer(r$test_input_indices[1, ]), 3890:3899),
    identical(r$test_input_indices, dm_windows(d, d$test)$input_indices))
  if ("epoch" %in% names(h)) stopifnot(length(unique(h$epoch)) == 80L)
  else stopifnot(nrow(h) == 80L)
}
fresh <- function(path) { if (file.exists(path)) stop("Artifact already exists: ", path); path }
if (a[1] == "--models") {
  mats <- readRDS(file.path(run, "esn/matrices.rds"))
  for (name in names(mats)) {
    mat <- mats[[name]]
    path <- fresh(file.path(run, "esn", paste0(name, ".csv")))
    lines <- apply(mat, 1L, function(x) paste(sprintf("%.17g", x), collapse = ","))
    writeLines(c(paste0("col", seq_len(ncol(mat)), collapse = ","), lines), path)
    stopifnot(max(abs(as.matrix(read.csv(path)) - mat)) <= 1e-12)
  }
  jsonlite::write_json(list(model = "ESN", seed = DM_SEED, params = cfg$esn,
    train_origins = c(58L, 2599L), train_targets = c(59L, 2600L), n_pairs = 2542L,
    ridge_solver = values$esn$solver, Wout_frozen_through_validation_test = TRUE),
    fresh(file.path(run, "esn/config.json")), pretty = TRUE, auto_unbox = TRUE)
  for (m in c("gru", "lstm")) {
    stopifnot(file.copy(file.path(run, m, "model.keras"),
      fresh(file.path(run, "models", paste0(m, "_seed_20260926.keras"))), overwrite = FALSE))
    h <- readRDS(file.path(run, m, "training_history.rds"))
    write.csv(h, fresh(file.path(run, m, "history.csv")), row.names = FALSE)
    architecture <- jsonlite::read_json(file.path(run, m, "model_config.json"))
    jsonlite::write_json(list(model = toupper(m), seed = DM_SEED, params = cfg[[m]],
      min_train = d$scale$min, max_train = d$scale$max, normalization_fit_indices = c(1L,2600L),
      epochs_completed = 80L, weights_selected = "final_epoch_80", early_stopping = FALSE,
      architecture_and_optimizer = architecture), fresh(file.path(run, m, "config.json")),
      pretty = TRUE, auto_unbox = TRUE, digits = NA)
  }
  cat("Model packaging PASS; no frozen predictions yet\n")
} else {
  reloads <- lapply(names(files), function(m) jsonlite::read_json(
    file.path(run, "validation", paste0(m, "_reload"), "reload_status.json"), simplifyVector = TRUE))
  stopifnot(all(vapply(reloads, function(r) r$status == "PASS" && !r$retrained, logical(1))))
  for (m in names(files)) {
    p <- values[[m]]$predictions; e <- p$real - p$previsto
    full <- data.frame(data = p$data, real = p$real, previsto = p$previsto,
      erro = e, erro_absoluto = abs(e), erro_quadratico = e^2, origem_data = p$data_origem)
    stopifnot(!anyNA(full), all(vapply(full[2:6], function(x) all(is.finite(x)), logical(1))))
    write.csv(full, fresh(file.path(run, "predictions", paste0(m, "_test_full.csv"))), row.names = FALSE)
  }
  metric <- function(real, pred) {
    e <- real - pred
    stopifnot(all(is.finite(e)), all(real != 0), sum((real - mean(real))^2) > 0)
    c(MAE = mean(abs(e)), RMSE = sqrt(mean(e^2)), MSE = mean(e^2),
      MAPE_percent = 100 * mean(abs(e / real)), R2 = 1 - sum(e^2)/sum((real - mean(real))^2))
  }
  for (scope in c("teste_completo", "janela_dm")) {
    metrics <- do.call(rbind, lapply(names(files), function(m) {
      p <- values[[m]]$predictions
      if (scope == "janela_dm") p <- p[p$data %in% b$predictions$data, ]
      data.frame(modelo = toupper(m), n = nrow(p), inicio = min(p$data), fim = max(p$data),
        as.list(metric(p$real, p$previsto)), check.names = FALSE)
    }))
    write.csv(metrics, fresh(file.path(run, "metrics", paste0("metricas_", scope, ".csv"))), row.names = FALSE)
    print(metrics)
  }
  # Last gate: roundtrip the CSV in staging before giving it the frozen filename.
  pending <- fresh(file.path(run, "validation/previsoes_dm_pending.csv"))
  write.csv(b$predictions, pending, row.names = FALSE)
  check <- read.csv(pending); check$data <- as.Date(check$data)
  stopifnot(identical(names(check), c("data", "real", "esn", "gru", "lstm")),
    identical(check$data, d$common_dates), !anyNA(check), !anyDuplicated(check$data),
    all(diff(check$data) > 0), all(vapply(check[-1], function(x) all(is.finite(x)), logical(1))),
    max(abs(as.matrix(check[-1]) - as.matrix(b$predictions[-1]))) <= 1e-10)
  stopifnot(file.rename(pending, fresh(file.path(run, "predictions/previsoes_dm.csv"))))
  saveRDS(b, fresh(file.path(run, "validation/validated_bundle.rds")))
  jsonlite::write_json(list(status = "PASS", n_test_full = length(d$test), n_common = length(d$common_dates),
    full_dates_start = as.character(min(d$dates[d$test])), full_dates_end = as.character(max(d$dates[d$test])),
    common_start = as.character(min(d$common_dates)), common_end = as.character(max(d$common_dates)),
    strict_train_target_boundary = TRUE, chronological_test_context = TRUE,
    same_real_and_dates = TRUE, finite_values = TRUE, date_join = TRUE, seed = DM_SEED,
    h = 1L, no_future_information = TRUE, CSV_roundtrip_tolerance = 1e-10,
    reloads = reloads, dm_executed = FALSE), fresh(file.path(run, "validation/assertions.json")),
    auto_unbox = TRUE, pretty = TRUE, digits = NA)
  cat("Predictions frozen; DM NOT executed\n")
}
