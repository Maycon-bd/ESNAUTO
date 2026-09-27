# Motor de inferencia. Requer bundle RDS previamente auditado; nao fabrica vetores.
# Ainda nao ha bundle historico recuperado neste projeto. Ver README.
args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 2L) stop("Uso: Rscript 02_executar_dm.R bundle_auditado.rds NOVO_DIRETORIO")
if (dir.exists(args[2])) stop("Saida existente; nenhuma sobrescrita permitida.")
b <- readRDS(args[1])
stopifnot(identical(b$run, "GA_RUN_0030"), identical(b$esn_source, "historical_recovered"),
          isTRUE(b$provenance_verified), identical(b$h, 1L),
          b$gru_source %in% c("historical_recovered", "controlled_rerun"),
          b$lstm_source %in% c("historical_recovered", "controlled_rerun"))
dated <- read.table("Scripts/data/PETR4_close com factor_2000-2020_com data.csv",
                    sep = ";", dec = ".", colClasses = c("character", "numeric"))
dates <- as.Date(dated[[1]])
stopifnot(nrow(dated) == 5198L, !anyNA(dates), !anyDuplicated(dates), all(diff(dates) > 0))
for (model in c("esn", "gru", "lstm")) {
  v <- b[[model]]
  stopifnot(all(c("data", "real", "previsto", "data_origem", "h") %in% names(v)))
  v$data <- as.Date(v$data); v$data_origem <- as.Date(v$data_origem)
  stopifnot(!anyNA(v), !anyDuplicated(v$data), all(diff(v$data) > 0),
            all(is.finite(v$real)), all(is.finite(v$previsto)), all(v$h == 1L))
  i <- match(v$data, dates); j <- match(v$data_origem, dates)
  stopifnot(!anyNA(i), !anyNA(j), all(i >= 3900L), all(i - j == 1L),
            max(abs(v$real - dated[[2]][i])) < 1e-10)
  b[[model]] <- v
}
p <- b$esn[, c("data", "real", "previsto")]; names(p)[3] <- "esn"
for (model in c("gru", "lstm")) {
  v <- b[[model]][, c("data", "previsto")]; names(v)[2] <- model
  p <- merge(p, v, by = "data", all = FALSE, sort = TRUE)
}
stopifnot(nrow(p) == 1298L, identical(p$data, dates[3901:5198]), !anyNA(p),
          !anyDuplicated(p$data), all(diff(p$data) > 0))
metrics <- do.call(rbind, lapply(c("esn", "gru", "lstm"), function(m) {
  e <- p$real - p[[m]]
  data.frame(modelo = m, n = length(e), MAE = mean(abs(e)), RMSE = sqrt(mean(e^2)))
}))
stopifnot(abs(metrics$MAE[1] - 0.327224) <= 1e-6,
          abs(metrics$RMSE[1] - 0.498527) <= 1e-6)
if (!requireNamespace("forecast", quietly = TRUE))
  stop("Instale forecast em ambiente R documentado: install.packages('forecast'). Nenhum DM executado.")
results <- list()
for (power in 1:2) for (model in c("gru", "lstm")) {
  e1 <- p$real - p$esn; e2 <- p$real - p[[model]]
  fit <- forecast::dm.test(e1, e2, h = 1, power = power,
                           alternative = "two.sided", varestimator = "acf")
  stopifnot(is.finite(fit$statistic), is.finite(fit$p.value))
  delta <- mean(abs(e1)^power) - mean(abs(e2)^power)
  lower <- if (delta < 0) "ESN" else if (delta > 0) toupper(model) else "empate"
  decision <- if (fit$p.value < .05) paste("Rejeitar H0; menor perda:", lower) else
    "Nao foi encontrada evidencia estatistica suficiente para rejeitar a hipotese de igualdade de acuracia preditiva"
  results[[length(results) + 1L]] <- data.frame(comparacao = paste("ESN x", toupper(model)),
    perda = if (power == 1) "absoluta" else "quadratica", power = power,
    n = nrow(p), h = 1L, DM = unname(fit$statistic), p_valor = fit$p.value,
    perda_media_esn = mean(abs(e1)^power), perda_media_baseline = mean(abs(e2)^power),
    diferenca_media = delta, menor_perda = lower, decisao = decision)
}
dir.create(args[2], recursive = TRUE)
write.csv(p, file.path(args[2], "previsoes_dm.csv"), row.names = FALSE)
write.csv(metrics, file.path(args[2], "metricas_mesmos_vetores.csv"), row.names = FALSE)
write.csv(do.call(rbind, results), file.path(args[2], "resultados_dm.csv"), row.names = FALSE)
writeLines(capture.output(sessionInfo()), file.path(args[2], "sessionInfo_R.txt"))
file.copy(args[1], file.path(args[2], "bundle_auditado.rds"), overwrite = FALSE)
print(metrics); print(do.call(rbind, results))
