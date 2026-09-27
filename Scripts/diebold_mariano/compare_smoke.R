# Only compares technical artifacts and exercises rejection assertions. No DM.
source("Scripts/diebold_mariano/05_validate_predictions.R")
base <- file.path(DM_BASE, "smoke_test")
rows <- list()
compare <- function(label, x, y) {
  stopifnot(identical(dim(x), dim(y)), length(x) == length(y),
    all(is.finite(x)), all(is.finite(y)))
  data.frame(item = label, identical = identical(x, y), max_abs_difference = max(abs(x - y)))
}
for (m in c("esn", "gru", "lstm")) {
  a <- readRDS(file.path(base, "run1", m, "result.rds"))
  b <- readRDS(file.path(base, "run2", m, "result.rds"))
  stopifnot(a$seed == DM_SEED, b$seed == DM_SEED, a$smoke, b$smoke,
    identical(a$predictions$data, b$predictions$data))
  rows[[length(rows) + 1L]] <- compare(paste(m, "predictions"), a$predictions$previsto, b$predictions$previsto)
  file <- if (m == "esn") "matrices.rds" else "weights.rds"
  x <- readRDS(file.path(base, "run1", m, file)); y <- readRDS(file.path(base, "run2", m, file))
  for (i in seq_along(x)) rows[[length(rows) + 1L]] <- compare(
    paste(m, if (m == "esn") names(x)[i] else paste("weight", i)), x[[i]], y[[i]])
}
results <- do.call(rbind, rows)
write.csv(results, file.path(base, "determinism_comparison.csv"), row.names = FALSE)
stopifnot(all(results$max_abs_difference == 0))
for (run in c("run1", "run2")) {
  files <- setNames(lapply(c("esn", "gru", "lstm"), function(m) file.path(base, run, m, "result.rds")), c("esn", "gru", "lstm"))
  bundle <- validate_dm_predictions(files, TRUE)
  saveRDS(bundle, file.path(base, run, "validated_bundle.rds"))
  write.csv(bundle$predictions, file.path(base, run, "technical_aligned.csv"), row.names = FALSE)
}
# Perturb only copies of smoke artifacts to test that provenance/date gates fail.
bad_dir <- file.path(base, "negative_cases")
dir.create(bad_dir, showWarnings = FALSE)
files <- setNames(lapply(c("esn", "gru", "lstm"), function(m) file.path(base, "run1", m, "result.rds")), c("esn", "gru", "lstm"))
original <- readRDS(files$esn)
mutations <- list(
  wrong_seed = function(x) { x$seed <- NA_integer_; x },
  duplicate_date = function(x) { x$predictions$data[2] <- x$predictions$data[1]; x },
  wrong_origin = function(x) { x$predictions$data_origem[1] <- x$predictions$data[1]; x },
  missing_value = function(x) { x$predictions$previsto[1] <- NA_real_; x },
  infinite_value = function(x) { x$predictions$previsto[1] <- Inf; x },
  validation_target_leak = function(x) { x$train_target_indices[1] <- 71L; x })
tests <- character()
for (name in names(mutations)) {
  f <- file.path(bad_dir, paste0(name, ".rds"))
  saveRDS(mutations[[name]](original), f)
  writeLines("Technical negative test only", file.path(bad_dir, "seeds.txt"))
  ff <- files; ff$esn <- f
  failed <- inherits(try(validate_dm_predictions(ff, TRUE), silent = TRUE), "try-error")
  stopifnot(failed); tests <- c(tests, paste("PASS rejection:", name))
}
d <- prepare_dm_data(FALSE)
w <- dm_windows(d, d$test)
stopifnot(identical(as.integer(w$input_indices[1, ]), 3890:3899),
  all(apply(w$input_indices, 1L, function(x) all(diff(x) == 1))),
  max(d$train) == 2600L, max(d$validation) == 3899L)
writeLines(c(tests, "PASS: official data only; chronological first test window 3890:3899",
  "PASS: independent smoke processes; numerical differences zero; no DM executed"),
  file.path(base, "assertion_tests.txt"))
print(results)
