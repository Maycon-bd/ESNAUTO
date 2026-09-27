# Creates integrity manifest only. Does not train, predict, reload, or run DM.
source("Scripts/diebold_mariano/01_prepare_data.R")
a <- commandArgs(trailingOnly = TRUE)
stopifnot(length(a) == 1L)
run <- normalizePath(a[1], winslash = "/", mustWork = TRUE)
manifest_path <- file.path(run, "execution_manifest.json")
if (file.exists(manifest_path)) stop("Manifest exists; immutable run refuses overwrite")
cfg <- jsonlite::read_json(file.path(run, "run_config.json"), simplifyVector = TRUE)
assertions <- jsonlite::read_json(file.path(run, "validation/assertions.json"), simplifyVector = TRUE)
events <- lapply(readLines(file.path(run, "logs/execution_events.jsonl")), jsonlite::fromJSON)
stopifnot(length(events) == 8L, all(vapply(events, function(x) x$attempt == 1 && x$exit_code == 0, logical(1))),
  isTRUE(assertions$status == "PASS"), !assertions$dm_executed,
  file.exists(file.path(run, "predictions/previsoes_dm.csv")))
metrics_full <- read.csv(file.path(run, "metrics/metricas_teste_completo.csv"))
metrics_dm <- read.csv(file.path(run, "metrics/metricas_janela_dm.csv"))
paths <- list(
  data = c("Scripts/data/PETR4_close com factor_2000-2020.txt",
    "Scripts/data/PETR4_close com factor_2000-2020_com data.csv"),
  scripts = list.files(file.path(run, "scripts"), full.names = TRUE),
  models = file.path(run, "models", c("gru_seed_20260926.keras", "lstm_seed_20260926.keras")),
  esn_matrices = file.path(run, "esn", c("Win.csv", "W.csv", "W_scaled.csv", "Wout.csv", "matrices.rds")),
  predictions = file.path(run, "predictions", c("esn_test_full.csv", "gru_test_full.csv",
    "lstm_test_full.csv", "previsoes_dm.csv")),
  validation = c(file.path(run, "validation/assertions.json"),
    file.path(run, "validation/validated_bundle.rds")),
  metrics = file.path(run, "metrics", c("metricas_teste_completo.csv", "metricas_janela_dm.csv")),
  report = file.path(run, "RELATORIO_EXECUCAO_CONTROLADA.md"))
stopifnot(all(file.exists(unlist(paths))))
hash_group <- function(x) as.list(setNames(unname(tools::sha256sum(x)),
  vapply(x, function(p) gsub("\\\\", "/", if (startsWith(p, run)) substring(p, nchar(run) + 2L) else p), character(1))))
hashes <- lapply(paths, hash_group)
d <- prepare_dm_data(FALSE)
dm <- read.csv(file.path(run, "predictions/previsoes_dm.csv")); dm$data <- as.Date(dm$data)
stopifnot(nrow(dm) == 1298L, identical(dm$data, d$common_dates), !anyNA(dm), !anyDuplicated(dm$data),
  all(diff(dm$data) > 0), all(vapply(dm[-1], function(x) all(is.finite(x)), logical(1))))
manifest <- list(
  scientific_execution = TRUE, dm_executed = FALSE, immutable_run = TRUE,
  start_utc = events[[1]]$start_utc, end_utc = events[[length(events)]]$end_utc,
  finalized_utc = format(Sys.time(), tz = "UTC", usetz = TRUE),
  seed_base = DM_SEED, alternative_seeds_tested = FALSE, automatic_retries = 0,
  versions = cfg$versions, hashes_sha256 = hashes,
  hyperparameters = list(esn = cfg$esn, gru = cfg$gru, lstm = cfg$lstm),
  partitions = list(n_total = 5198L, train = c(1L, 2600L), validation = c(2601L, 3899L),
    test = c(3900L, 5198L), n_train = 2600L, n_validation = 1299L, n_test = 1299L),
  predictions = list(test_full_n = 1299L, test_start = "2015-09-29", test_end = "2020-12-30",
    dm_n = 1298L, dm_start = "2015-09-30", dm_end = "2020-12-30",
    frozen_file = "predictions/previsoes_dm.csv", columns = names(dm)),
  metrics = list(test_full = metrics_full, dm_window = metrics_dm),
  assertions = assertions, execution_events = events,
  reload = assertions$reloads, protocol = "controlled_inferential_replication",
  historical_results_replaced = FALSE,
  status = "SCIENTIFIC_PREDICTIONS_FROZEN_DM_NOT_EXECUTED")
jsonlite::write_json(manifest, manifest_path, auto_unbox = TRUE, pretty = TRUE, digits = NA, null = "null")
stopifnot(jsonlite::validate(readLines(manifest_path, warn = FALSE)))
cat("Manifest created; DM NOT executed\n")
