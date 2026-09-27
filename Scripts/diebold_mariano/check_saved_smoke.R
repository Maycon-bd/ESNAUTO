# Reloading existing smoke weights; no training, no scientific predictions.
source("Scripts/diebold_mariano/01_prepare_data.R")
a <- commandArgs(trailingOnly = TRUE)
stopifnot(length(a) == 1L, a %in% c("gru", "lstm"))
dm_seed(TRUE)
d <- prepare_dm_data(TRUE); w <- dm_windows(d, d$test)
out <- file.path(DM_BASE, "smoke_test/run1", a)
model <- keras3::load_model(file.path(out, "model.keras"))
y <- as.numeric(predict(model, w$x, verbose = 0L)) * (d$scale$max - d$scale$min) + d$scale$min
old <- readRDS(file.path(out, "result.rds"))$predictions$previsto
delta <- max(abs(y - old)); stopifnot(delta == 0)
writeLines(paste("Saved model reload: PASS; max_abs_difference =", delta),
  file.path(out, "reload_check.txt"))
