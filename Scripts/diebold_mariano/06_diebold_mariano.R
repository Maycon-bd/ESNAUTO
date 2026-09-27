# NOT EXECUTED IN PHASE I.2. Requires separately authorized scientific outputs.
source("Scripts/diebold_mariano/05_validate_predictions.R")
run_controlled_dm <- function(bundle_path, output) {
  if (Sys.getenv("ESNAUTO_AUTHORIZE_DM") != "YES") stop("DM requires separate authorization")
  b <- readRDS(bundle_path)
  stopifnot(identical(b$smoke, FALSE), b$seed == DM_SEED,
    b$protocol == "controlled_inferential_replication", b$h == 1L,
    identical(unname(b$input_md5), unname(tools::md5sum(unlist(b$input_files)))))
  verified <- validate_dm_predictions(b$input_files, FALSE)
  stopifnot(identical(verified$predictions, b$predictions))
  out <- dm_output(output, FALSE)
  p <- b$predictions; rows <- list()
  for (power in 1:2) for (baseline in c("gru", "lstm")) {
    e1 <- p$real - p$esn; e2 <- p$real - p[[baseline]]
    fit <- forecast::dm.test(e1, e2, h = 1, power = power,
      alternative = "two.sided", varestimator = "acf")
    stopifnot(is.finite(fit$statistic), is.finite(fit$p.value))
    l1 <- mean(abs(e1)^power); l2 <- mean(abs(e2)^power)
    lower <- if (l1 < l2) "ESN" else if (l1 > l2) toupper(baseline) else "empate"
    rows[[length(rows) + 1L]] <- data.frame(comparacao = paste("ESN x", toupper(baseline)),
      power = power, n = nrow(p), h = 1L, DM = unname(fit$statistic), p_valor = fit$p.value,
      perda_media_esn = l1, perda_media_baseline = l2, diferenca_media = l1 - l2,
      menor_perda = lower, decisao = if (fit$p.value < .05) paste("Rejeitar H0; menor perda:", lower)
        else "Nao foi encontrada evidencia estatistica suficiente para rejeitar igualdade de acuracia preditiva")
  }
  metrics <- do.call(rbind, lapply(c("esn", "gru", "lstm"), function(m) {
    e <- p$real - p[[m]]
    data.frame(modelo = m, n = length(e), MAE = mean(abs(e)), RMSE = sqrt(mean(e^2)))
  }))
  write.csv(do.call(rbind, rows), file.path(out, "resultados_dm.csv"), row.names = FALSE)
  write.csv(metrics, file.path(out, "metricas_mesmos_vetores.csv"), row.names = FALSE)
  writeLines(capture.output(sessionInfo()), file.path(out, "sessionInfo_R.txt"))
}
if (sys.nframe() == 0L) {
  a <- commandArgs(trailingOnly = TRUE)
  if (length(a) != 2L) stop("Usage: 06_diebold_mariano.R SCIENTIFIC_BUNDLE NEW_OUTPUT")
  run_controlled_dm(a[1], a[2])
}
