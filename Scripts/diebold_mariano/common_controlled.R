# Isolated controlled protocol. Sources only definitions; no training on import.
if (.Platform$OS.type == "windows") invisible(Sys.setlocale("LC_CTYPE", "English_United States.utf8"))
DM_ROOT <- normalizePath(".", winslash = "/", mustWork = TRUE)
stopifnot(file.exists(file.path(DM_ROOT, "app/utils/esn_core.R")))
DM_BASE <- file.path(DM_ROOT, "Scripts/results/diebold_mariano")
DM_ENV <- file.path(DM_BASE, "ambiente")
.libPaths(c(file.path(DM_ENV, "R-library"), .Library))
DM_SEED <- 20260926L
Sys.setenv(RETICULATE_PYTHON = file.path(DM_ENV, "python-env/Scripts/python.exe"),
  RETICULATE_USE_MANAGED_VENV = "no", KERAS_BACKEND = "tensorflow",
  CUDA_VISIBLE_DEVICES = "-1", TF_DETERMINISTIC_OPS = "1", TF_ENABLE_ONEDNN_OPTS = "0",
  PYTHONHASHSEED = "20260926", OMP_NUM_THREADS = "1", OPENBLAS_NUM_THREADS = "1",
  MKL_NUM_THREADS = "1", TF_NUM_INTRAOP_THREADS = "1", TF_NUM_INTEROP_THREADS = "1")

dm_config <- function() {
  # A run-local snapshot records authorization without mutating the global
  # configuration before scientific persistence/reload validation succeeds.
  config_path <- Sys.getenv("ESNAUTO_CONFIG_PATH", file.path(DM_BASE, "configuracao_experimento.json"))
  cfg <- jsonlite::read_json(config_path, simplifyVector = TRUE)
  stopifnot(cfg$seed_base == DM_SEED, isTRUE(cfg$strict_train_target_boundary),
    isTRUE(cfg$chronological_test_context), cfg$esn$a == .111817, cfg$esn$sr == .215273,
    cfg$esn$initLen == 57, cfg$esn$tam_reservoir == 22,
    cfg$esn$reg == 5.71625418786693e-05, cfg$esn$win_dist == "Laplace", cfg$esn$w_dist == "Normal")
  for (m in c("gru", "lstm")) stopifnot(cfg[[m]]$units == 50, cfg[[m]]$timesteps == 10,
    cfg[[m]]$dropout == .2, cfg[[m]]$epochs == 80, cfg[[m]]$optimizer == "adam",
    identical(cfg[[m]]$segunda_camada, FALSE), cfg[[m]]$batch_size == 16)
  if (!is.null(cfg$versions)) {
    stopifnot(as.character(getRversion()) == cfg$versions$R)
    for (p in names(cfg$versions$R_packages))
      stopifnot(as.character(packageVersion(p)) == cfg$versions$R_packages[[p]])
  }
  cfg
}
dm_seed <- function(dl = FALSE) {
  RNGkind("Mersenne-Twister", "Inversion", "Rejection")
  set.seed(DM_SEED)
  if (dl) {
    tf <- reticulate::import("tensorflow", convert = TRUE)
    cfg <- dm_config()
    if (!is.null(cfg$versions)) {
      stopifnot(tf$`__version__` == cfg$versions$TensorFlow,
        reticulate::import("keras")$`__version__` == cfg$versions$Keras,
        reticulate::import("numpy")$`__version__` == cfg$versions$NumPy,
        reticulate::py_eval("__import__('platform').python_version()") == cfg$versions$Python)
    }
    stopifnot(reticulate::py_has_attr(tf$config$experimental, "enable_op_determinism"))
    tf$config$set_visible_devices(list(), "GPU")
    tf$config$threading$set_intra_op_parallelism_threads(1L)
    tf$config$threading$set_inter_op_parallelism_threads(1L)
    tf$config$experimental$enable_op_determinism()
    stopifnot(length(tf$config$get_visible_devices("GPU")) == 0L)
    keras3::set_random_seed(DM_SEED)
    reticulate::import("random")$seed(DM_SEED)
    reticulate::import("numpy")$random$seed(DM_SEED)
    tf$random$set_seed(DM_SEED)
    stopifnot(reticulate::py_eval("__import__('os').environ['PYTHONHASHSEED']") == "20260926")
  }
  invisible(DM_SEED)
}
dm_output <- function(path, smoke) {
  parent <- if (smoke) file.path(DM_BASE, "smoke_test") else file.path(DM_BASE, "controlled_runs")
  parent <- normalizePath(parent, winslash = "/", mustWork = FALSE)
  path <- normalizePath(path, winslash = "/", mustWork = FALSE)
  stopifnot(startsWith(tolower(path), paste0(tolower(parent), "/")))
  if (dir.exists(path) || file.exists(path)) stop("Output already exists; refusing overwrite")
  if (!smoke && Sys.getenv("ESNAUTO_AUTHORIZE_SCIENTIFIC") != "YES")
    stop("Scientific execution requires separate explicit authorization; Phase I.2 is smoke-only")
  if (!smoke && !isTRUE(dm_config()$apto_para_execucao_controlada)) stop("Protocol not ready")
  if (!smoke && !isTRUE(dm_config()$scientific_execution_authorized))
    stop("Scientific authorization not recorded in configuration")
  dir.create(path, recursive = TRUE)
  path
}
dm_record <- function(path, model, smoke, cfg) {
  writeLines(c(paste("R/Python/NumPy/TensorFlow/Keras seed-base:", DM_SEED),
    paste("Technical smoke test:", smoke), paste("Model:", model), paste("RNGkind:", paste(RNGkind(), collapse = ","))),
    file.path(path, "seeds.txt"))
  jsonlite::write_json(cfg, file.path(path, "config_snapshot.json"), auto_unbox = TRUE, pretty = TRUE)
  writeLines(capture.output(sessionInfo()), file.path(path, "sessionInfo_R.txt"))
}
dm_cli <- function(model, fun) {
  args <- commandArgs(trailingOnly = TRUE)
  if (length(args) != 2L || !args[1] %in% c("--smoke", "--scientific"))
    stop("Usage: script.R --smoke|--scientific NEW_OUTPUT_DIRECTORY")
  smoke <- args[1] == "--smoke"
  cfg <- dm_config()
  out <- dm_output(args[2], smoke)
  dm_seed(model != "esn")
  dm_record(out, model, smoke, cfg)
  d <- prepare_dm_data(smoke)
  fit <- fun(d, cfg, smoke, out)
  fit$seed <- DM_SEED; fit$smoke <- smoke; fit$model <- model
  fit$source <- "controlled_rerun"; fit$strict_train_target_boundary <- TRUE
  fit$chronological_test_context <- TRUE
  stopifnot(all(is.finite(fit$predictions$previsto)), !anyNA(fit$predictions))
  saveRDS(fit, file.path(out, "result.rds"))
  write.csv(fit$predictions, file.path(out, "predictions_by_date.csv"), row.names = FALSE)
  writeLines(capture.output(sessionInfo()), file.path(out, "sessionInfo_R.txt"))
  cat(model, "complete; smoke =", smoke, "; n =", nrow(fit$predictions), "\n")
}
