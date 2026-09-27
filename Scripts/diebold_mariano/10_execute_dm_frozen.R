# Final inferential stage: reads the single frozen CSV; never loads or runs models.
if (.Platform$OS.type == "windows") invisible(Sys.setlocale("LC_CTYPE", "English_United States.utf8"))
root <- normalizePath(".", winslash = "/", mustWork = TRUE)
lib <- file.path(root, "Scripts/results/diebold_mariano/ambiente/R-library")
.libPaths(c(lib, .Library))
stopifnot(as.character(packageVersion("forecast")) == "9.0.2",
  as.character(packageVersion("jsonlite")) == "2.0.0")
run <- file.path(root, "Scripts/results/diebold_mariano/controlled_runs/seed_20260926")
csv <- file.path(run, "predictions/previsoes_dm.csv")
expected_hash <- "0DD4007600D58047913F2C10BA8CE4F3801E5EE37F4C0E759BC46D2BFF070D5E"
actual_hash <- toupper(unname(tools::sha256sum(csv)))
if (!identical(actual_hash, expected_hash)) stop("FROZEN CSV HASH MISMATCH; DM NOT EXECUTED")
out <- file.path(run, "dm")
if (dir.exists(out) || file.exists(out)) stop("DM output already exists; refusing overwrite/re-execution")
dir.create(out)

# Record every protected scientific artifact before inference.
protected <- c(csv,
  file.path(run, "esn", c("Win.csv", "W.csv", "W_scaled.csv", "Wout.csv", "matrices.rds")),
  file.path(run, "models", c("gru_seed_20260926.keras", "lstm_seed_20260926.keras")),
  file.path(run, "metrics", c("metricas_teste_completo.csv", "metricas_janela_dm.csv")))
stopifnot(all(file.exists(protected)))
hash_before <- tools::sha256sum(protected)
write.csv(data.frame(path = sub(paste0("^", gsub("([\\.])", "\\\\\\1", run), "/?"), "", names(hash_before)),
  sha256 = toupper(unname(hash_before))), file.path(out, "protected_hashes_before.csv"), row.names = FALSE)

p <- read.csv(csv, colClasses = c("character", rep("numeric", 4)), check.names = FALSE)
p$data <- as.Date(p$data)
stopifnot(identical(names(p), c("data", "real", "esn", "gru", "lstm")),
  nrow(p) == 1298L, p$data[1] == as.Date("2015-09-30"),
  tail(p$data, 1) == as.Date("2020-12-30"), !anyNA(p), !anyDuplicated(p$data),
  all(diff(p$data) > 0), all(vapply(p[-1], function(x) all(is.finite(x)), logical(1))))

errors <- data.frame(esn = p$real - p$esn, gru = p$real - p$gru, lstm = p$real - p$lstm)
stopifnot(all(vapply(errors, function(x) all(is.finite(x)), logical(1))))
numeric_audit <- do.call(rbind, lapply(names(errors), function(m) {
  e <- errors[[m]]; mse <- mean(e^2); rmse <- sqrt(mse); mae <- mean(abs(e))
  stopifnot(abs(sqrt(mse) - rmse) < 1e-15, abs(mean(abs(e)) - mae) < 1e-15)
  data.frame(model = toupper(m), n = length(e), mean_error = mean(e),
    mean_absolute_error = mean(abs(e)), mean_squared_error = mse,
    MAE = mae, MSE = mse, RMSE = rmse)
}))
rownames(numeric_audit) <- NULL
expected <- list(esn = c(MAE=.328850012455254, RMSE=.498452314212457),
  gru = c(MAE=.418175291762921, RMSE=.592452440069539),
  lstm = c(MAE=.466612261009447, RMSE=.635287229246294))
for (m in names(expected)) {
  row <- numeric_audit[numeric_audit$model == toupper(m), ]
  stopifnot(abs(row$MAE - expected[[m]]["MAE"]) < 1e-12,
    abs(row$RMSE - expected[[m]]["RMSE"]) < 1e-12)
}
write.csv(numeric_audit, file.path(out, "auditoria_numerica.csv"), row.names = FALSE)

specs <- list(
  list(baseline="gru", comparison="ESN x GRU", loss="Absoluta", power=1L),
  list(baseline="lstm", comparison="ESN x LSTM", loss="Absoluta", power=1L),
  list(baseline="gru", comparison="ESN x GRU", loss="Quadrática", power=2L),
  list(baseline="lstm", comparison="ESN x LSTM", loss="Quadrática", power=2L))
rows <- vector("list", length(specs)); interpretations <- character(length(specs))
for (i in seq_along(specs)) {
  s <- specs[[i]]; e1 <- errors$esn; e2 <- errors[[s$baseline]]
  # Explicit arguments; no defaults determine the scientific protocol.
  fit <- forecast::dm.test(e1, e2, alternative = "two.sided", h = 1L,
    power = s$power, varestimator = "acf")
  loss_esn <- abs(e1)^s$power; loss_base <- abs(e2)^s$power
  differential <- loss_esn - loss_base
  mean_d <- mean(differential)
  lower <- if (mean_d < 0) "ESN" else if (mean_d > 0) toupper(s$baseline) else "Empate"
  reject <- unname(fit$p.value) < .05
  interpretations[i] <- if (!reject)
    "Não foi encontrada evidência estatística suficiente para rejeitar a hipótese nula de igualdade de acurácia preditiva no critério avaliado."
  else if (mean_d < 0)
    "Foi encontrada diferença estatisticamente significativa entre as previsões dos modelos, com menor perda média para a ESN no critério avaliado."
  else "Foi encontrada diferença estatisticamente significativa entre as previsões dos modelos, com menor perda média para o baseline no critério avaliado."
  rows[[i]] <- data.frame(comparison = s$comparison, loss = s$loss, power = s$power,
    n = length(e1), h = 1L, alternative = "two.sided", varestimator = "acf",
    dm_statistic = unname(fit$statistic), p_value = unname(fit$p.value), alpha = .05,
    mean_loss_esn = mean(loss_esn), mean_loss_baseline = mean(loss_base),
    mean_loss_difference = mean_d, lower_mean_loss_model = lower, reject_h0 = reject,
    interpretation = interpretations[i], stringsAsFactors = FALSE)
}
results <- do.call(rbind, rows); rownames(results) <- NULL
stopifnot(nrow(results) == 4L, all(is.finite(results$dm_statistic)),
  all(is.finite(results$p_value)), all(results$p_value >= 0 & results$p_value <= 1),
  identical(results$power, c(1L,1L,2L,2L)))
write.csv(results, file.path(out, "resultados_dm.csv"), row.names = FALSE)

fmt <- function(x, digits=9) formatC(x, format = "g", digits = digits)
decision <- ifelse(results$reject_h0, "Rejeitar H0", "Não rejeitar H0")
table_lines <- c(
  "# Teste de Diebold–Mariano — execução controlada complementar", "",
  "Tabela – Teste de Diebold-Mariano na execução controlada complementar", "",
  "| Comparação | Função de perda | n | Estatística DM | p-valor | Menor perda média | Decisão a 5% |",
  "|---|---|---:|---:|---:|---|---|",
  vapply(seq_len(nrow(results)), function(i) sprintf("| %s | %s | %d | %s | %s | %s | %s |",
    results$comparison[i], results$loss[i], results$n[i], fmt(results$dm_statistic[i]),
    fmt(results$p_value[i]), results$lower_mean_loss_model[i], decision[i]), character(1)),
  "", "## Diferenciais de perda e interpretação", "",
  unlist(lapply(seq_len(nrow(results)), function(i) c(
    sprintf("### %s — perda %s", results$comparison[i], tolower(results$loss[i])), "",
    sprintf("Perda média ESN = %s; perda média baseline = %s; mean_d = %s.",
      fmt(results$mean_loss_esn[i], 12), fmt(results$mean_loss_baseline[i], 12),
      fmt(results$mean_loss_difference[i], 12)), "", results$interpretation[i], ""))),
  "## Protocolo e limitação", "",
  "Foram executados somente os quatro testes bilaterais pré-especificados, com h=1, `forecast::dm.test()` 9.0.2, `varestimator=\"acf\"` e alpha individual de 5%. Não foi aplicada correção de multiplicidade aos resultados principais. Essa decisão foi definida antes dos p-valores e deve ser considerada uma limitação metodológica.", "",
  paste0("SHA-256 do CSV congelado: `", actual_hash, "`."))
writeLines(table_lines, file.path(out, "resultados_dm.md"), useBytes = TRUE)

summary_lines <- c("DIEBOLD-MARIANO — EXECUÇÃO CONTROLADA COMPLEMENTAR",
  paste("HASH VALIDADO: SIM —", actual_hash), "N: 1298", "PERÍODO: 2015-09-30 a 2020-12-30", "",
  unlist(lapply(seq_len(nrow(numeric_audit)), function(i) sprintf("%s: MAE=%.15g RMSE=%.15g MSE=%.15g ME=%.15g",
    numeric_audit$model[i], numeric_audit$MAE[i], numeric_audit$RMSE[i], numeric_audit$MSE[i], numeric_audit$mean_error[i]))), "",
  unlist(lapply(seq_len(nrow(results)), function(i) c(sprintf("TESTE %d — %s — perda %s", i,
    results$comparison[i], tolower(results$loss[i])), sprintf("DM=%.15g", results$dm_statistic[i]),
    sprintf("p=%.15g", results$p_value[i]), sprintf("mean_d=%.15g", results$mean_loss_difference[i]),
    paste("menor perda=", results$lower_mean_loss_model[i]),
    paste("H0 rejeitada a 5%:", ifelse(results$reject_h0[i], "SIM", "NÃO")), ""))),
  "DIEBOLD-MARIANO EXECUTADO E VALIDADO: SIM")
writeLines(summary_lines, file.path(out, "resultados_dm.txt"), useBytes = TRUE)

hash_after <- tools::sha256sum(protected)
stopifnot(identical(unname(hash_before), unname(hash_after)),
  identical(toupper(unname(hash_after[1])), expected_hash))
write.csv(data.frame(path = sub(paste0("^", gsub("([\\.])", "\\\\\\1", run), "/?"), "", names(hash_after)),
  sha256 = toupper(unname(hash_after))), file.path(out, "protected_hashes_after.csv"), row.names = FALSE)
writeLines(capture.output(sessionInfo()), file.path(out, "sessionInfo_dm.txt"))
execution <- list(
  status = "SUCCESS", dm_executed = TRUE, timestamp_utc = format(Sys.time(), tz="UTC", usetz=TRUE),
  frozen_csv = "predictions/previsoes_dm.csv", frozen_csv_sha256 = actual_hash,
  hash_validated = TRUE, protected_artifacts_unchanged = TRUE,
  n = nrow(p), period = list(start=as.character(min(p$data)), end=as.character(max(p$data))),
  implementation = list(package="forecast", version=as.character(packageVersion("forecast")),
    function_name="forecast::dm.test", h=1L, alternative="two.sided", varestimator="acf",
    alpha=.05, powers=c(1L,2L), multiplicity_adjustment="none; individual alpha 0.05; prespecified tests"),
  error_definition = "real - forecast", loss_differential = "loss_ESN - loss_baseline",
  numerical_audit = numeric_audit, results = results,
  models_or_predictions_reexecuted = FALSE, historical_results_replaced = FALSE)
jsonlite::write_json(execution, file.path(out, "dm_execution.json"), auto_unbox=TRUE,
  pretty=TRUE, digits=NA, null="null")
stopifnot(jsonlite::validate(readLines(file.path(out, "dm_execution.json"), warn=FALSE)))
cat(paste(summary_lines, collapse="\n"), "\n")
