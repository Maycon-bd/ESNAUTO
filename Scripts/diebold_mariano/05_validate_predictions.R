source("Scripts/diebold_mariano/01_prepare_data.R")
validate_dm_predictions <- function(files, smoke = FALSE) {
  stopifnot(length(files) == 3L, setequal(names(files), c("esn", "gru", "lstm")))
  d <- prepare_dm_data(smoke); values <- lapply(files, readRDS)
  aligned <- data.frame(data = d$common_dates)
  for (m in names(files)) {
    r <- values[[m]]; p <- r$predictions
    stopifnot(r$seed == DM_SEED, identical(r$smoke, smoke), identical(r$model, m),
      r$source == "controlled_rerun", isTRUE(r$strict_train_target_boundary),
      isTRUE(r$chronological_test_context), !anyNA(p), !anyDuplicated(p$data),
      all(diff(p$data) > 0), all(is.finite(p$real)), all(is.finite(p$previsto)), all(p$h == 1L),
      identical(as.Date(p$data), d$dates[d$test]),
      identical(as.Date(p$data_origem), d$dates[d$test - 1L]),
      max(abs(p$real - d$y[d$test])) < 1e-10,
      all(r$train_target_indices %in% d$train),
      identical(r$source_md5, d$source_md5), file.exists(file.path(dirname(files[[m]]), "seeds.txt")))
    if (m != "esn") stopifnot(identical(r$normalization_fit_indices, d$train))
    if (m != "esn" && !smoke) stopifnot(r$epochs == 80L)
    pred <- p[, c("data", "previsto")]; names(pred)[2] <- m
    aligned <- merge(aligned, pred, by = "data", all.x = TRUE, sort = TRUE)
  }
  stopifnot(identical(as.Date(aligned$data), d$common_dates), !anyNA(aligned),
    all(vapply(aligned[-1], function(x) all(is.finite(x)), logical(1))))
  aligned$real <- d$y[match(aligned$data, d$dates)]
  aligned <- aligned[, c("data", "real", "esn", "gru", "lstm")]
  list(predictions = aligned, seed = DM_SEED, smoke = smoke,
    sources = vapply(values, function(x) x$source, character(1)),
    h = 1L, protocol = "controlled_inferential_replication", input_files = files,
    input_md5 = tools::md5sum(unlist(files)))
}
if (sys.nframe() == 0L) {
  a <- commandArgs(trailingOnly = TRUE)
  if (length(a) != 5L || !a[1] %in% c("--smoke", "--scientific"))
    stop("Usage: --smoke|--scientific ESN_RDS GRU_RDS LSTM_RDS NEW_OUTPUT")
  smoke <- a[1] == "--smoke"
  out <- dm_output(a[5], smoke)
  b <- validate_dm_predictions(setNames(as.list(a[2:4]), c("esn", "gru", "lstm")), smoke)
  saveRDS(b, file.path(out, "validated_bundle.rds"))
  name <- if (smoke) "technical_aligned.csv" else "previsoes_dm.csv"
  write.csv(b$predictions, file.path(out, name), row.names = FALSE)
  cat("Date alignment validated:", nrow(b$predictions), "rows; smoke =", smoke, "\n")
}
