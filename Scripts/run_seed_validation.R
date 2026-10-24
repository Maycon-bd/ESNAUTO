# =============================================================================
# run_seed_validation.R
# Validação estatística por sementes para configurações históricas do ESNAUTO
#
# Objetivo:
#   Medir a variabilidade causada exclusivamente pela geração estocástica de
#   Win e W, mantendo fixos os hiperparâmetros das configurações históricas.
#
# Protocolo:
#   1) ajuste em treino -> avaliação em validação;
#   2) refit em treino+validação -> avaliação final em teste contíguo;
#   3) mesmas seeds para todos os cenários (desenho pareado);
#   4) preservação das matrizes por seed em RDS;
#   5) CSV bruto, resumo descritivo e Wilcoxon pareado com correção de Holm.
#
# Uso:
#   Rscript Scripts/run_seed_validation.R
#   Rscript Scripts/run_seed_validation.R --asset PETR4 --seeds 30
#   Rscript Scripts/run_seed_validation.R --asset VALE3 --seeds 30 --seed-base 202700
# =============================================================================

args <- commandArgs(trailingOnly = TRUE)

arg_value <- function(flag, default = NULL) {
  idx <- which(args == flag)
  if (length(idx) == 0L || idx[1] == length(args)) return(default)
  args[idx[1] + 1L]
}

asset <- toupper(arg_value("--asset", "PETR4"))
n_seeds <- as.integer(arg_value("--seeds", "30"))
seed_base <- as.integer(arg_value("--seed-base", "202700"))
output_root <- arg_value("--output", file.path("Scripts", "results", "seed_validation"))
save_predictions <- tolower(arg_value("--save-predictions", "false")) %in% c("1", "true", "yes", "sim")

if (!is.finite(n_seeds) || n_seeds < 2L) stop("--seeds deve ser >= 2.")
if (!is.finite(seed_base)) stop("--seed-base inválido.")

# Executar sempre a partir da raiz do repositório.
source(file.path("app", "utils", "data_prep.R"))
source(file.path("app", "utils", "metrics.R"))

if (!asset %in% names(datasets_disponiveis)) {
  stop(sprintf("Ativo desconhecido: %s. Disponíveis: %s",
               asset, paste(names(datasets_disponiveis), collapse = ", ")))
}

# -----------------------------------------------------------------------------
# Configurações históricas fixas
# -----------------------------------------------------------------------------
# Estes parâmetros são os reportados nos resultados oficiais das Ondas 2 e 4.
# Eles NÃO são reotimizados nesta bateria. Isso isola a variabilidade de Win/W.
#
# GA_RUN_0046: Normal × Normal
# GA_RUN_0030: Laplace × Normal
# GA_RUN_0033: Laplace × Cauchy
# -----------------------------------------------------------------------------
scenarios <- list(
  NORMAL_NORMAL = list(
    historical_id = "GA_RUN_0046",
    win_dist = "Normal",
    w_dist = "Normal",
    params = list(a = 0.316, sr = 0.017, initLen = 57L,
                  tam_reservoir = 3L, reg = 2.97e-5)
  ),
  LAPLACE_NORMAL = list(
    historical_id = "GA_RUN_0030",
    win_dist = "Laplace",
    w_dist = "Normal",
    params = list(a = 0.112, sr = 0.215, initLen = 57L,
                  tam_reservoir = 22L, reg = 5.72e-5)
  ),
  LAPLACE_CAUCHY = list(
    historical_id = "GA_RUN_0033",
    win_dist = "Laplace",
    w_dist = "Cauchy",
    params = list(a = 0.924, sr = 0.652, initLen = 97L,
                  tam_reservoir = 28L, reg = 2.98e-5)
  )
)

# -----------------------------------------------------------------------------
# Geradores congelados para esta bateria
# -----------------------------------------------------------------------------
# Não dependem de futuras mudanças nos defaults do catálogo.
generate_weights <- function(dist_name, n) {
  switch(
    dist_name,
    "Normal" = rnorm(n, mean = 0, sd = 1),
    "Laplace" = {
      b <- 1 / sqrt(2) # sd = 1
      u <- runif(n) - 0.5
      -b * sign(u) * log(1 - 2 * abs(u))
    },
    "Cauchy" = rcauchy(n, location = 0, scale = 1),
    stop(sprintf("Distribuição não suportada nesta bateria: %s", dist_name))
  )
}

spectral_scale <- function(W, sr) {
  eig <- eigen(W, only.values = TRUE)$values
  rho <- max(Mod(eig))
  if (!is.finite(rho) || rho <= .Machine$double.eps) rho <- 1
  sr * W / rho
}

ridge_readout <- function(X, Yt, reg) {
  gram <- X %*% t(X) + reg * diag(nrow(X))
  inv <- tryCatch(
    solve(gram),
    error = function(e) {
      if (!requireNamespace("pracma", quietly = TRUE)) {
        stop("Falha em solve() e pacote 'pracma' não está instalado.")
      }
      pracma::pinv(gram)
    }
  )
  Yt %*% t(X) %*% inv
}

fit_esn <- function(series, params, Win, W_raw) {
  n <- length(series)
  a <- params$a
  initLen <- params$initLen
  Nx <- params$tam_reservoir
  reg <- params$reg
  W <- spectral_scale(W_raw, params$sr)

  if (initLen >= n - 1L) stop("initLen incompatível com o tamanho da série.")

  X <- matrix(0, nrow = 2L + Nx, ncol = n - initLen - 1L)
  Yt <- matrix(series[(initLen + 2L):n], nrow = 1L)
  x <- rep(0, Nx)

  col <- 1L
  for (t in 1:(n - 1L)) {
    u <- series[t]
    x <- (1 - a) * x + a * tanh(Win %*% c(1, u) + W %*% x)
    if (t > initLen) {
      X[, col] <- c(1, u, x)
      col <- col + 1L
    }
  }

  Wout <- ridge_readout(X, Yt, reg)

  # Estado ao final da série de ajuste. Necessário para continuação temporal.
  list(Wout = Wout, state = x, W_scaled = W)
}

forecast_one_step <- function(history, future, params, Win, W_scaled, Wout, state) {
  a <- params$a
  n_future <- length(future)
  pred <- numeric(n_future)
  x <- state
  u <- tail(history, 1L)

  # Previsão one-step-ahead com atualização pelo valor observado anterior.
  for (i in seq_len(n_future)) {
    x <- (1 - a) * x + a * tanh(Win %*% c(1, u) + W_scaled %*% x)
    pred[i] <- as.numeric(Wout %*% c(1, u, x))
    u <- future[i]
  }

  list(pred = pred, state = x)
}

evaluate_scenario_seed <- function(data, split, scenario_name, scenario, seed) {
  set.seed(seed)

  p <- scenario$params
  Nx <- p$tam_reservoir
  Win <- matrix(generate_weights(scenario$win_dist, Nx * 2L), nrow = Nx, ncol = 2L)
  W_raw <- matrix(generate_weights(scenario$w_dist, Nx * Nx), nrow = Nx, ncol = Nx)

  train <- split$treino
  valid <- split$validacao
  test <- split$teste

  t0 <- proc.time()[["elapsed"]]

  # 1) Treino -> validação.
  fit_train <- fit_esn(train, p, Win, W_raw)
  fc_valid <- forecast_one_step(
    history = train,
    future = valid,
    params = p,
    Win = Win,
    W_scaled = fit_train$W_scaled,
    Wout = fit_train$Wout,
    state = fit_train$state
  )
  m_valid <- calcular_todas_metricas(valid, fc_valid$pred)

  # 2) Refit em treino + validação, preservando a continuidade temporal.
  train_valid <- c(train, valid)
  fit_train_valid <- fit_esn(train_valid, p, Win, W_raw)
  fc_test <- forecast_one_step(
    history = train_valid,
    future = test,
    params = p,
    Win = Win,
    W_scaled = fit_train_valid$W_scaled,
    Wout = fit_train_valid$Wout,
    state = fit_train_valid$state
  )
  m_test <- calcular_todas_metricas(test, fc_test$pred)

  elapsed <- proc.time()[["elapsed"]] - t0

  list(
    row = data.frame(
      asset = asset,
      protocol = "fixed_hyperparams_seed_robustness_v1",
      scenario = scenario_name,
      historical_id = scenario$historical_id,
      win_distribution = scenario$win_dist,
      w_distribution = scenario$w_dist,
      seed = seed,
      a = p$a,
      sr = p$sr,
      initLen = p$initLen,
      reservoir_size = p$tam_reservoir,
      lambda = p$reg,
      mae_validation = m_valid$MAE,
      rmse_validation = m_valid$RMSE,
      r2_validation = m_valid$R2,
      mae_test = m_test$MAE,
      rmse_test = m_test$RMSE,
      r2_test = m_test$R2,
      fit_eval_time_s = elapsed,
      stringsAsFactors = FALSE
    ),
    matrices = list(
      Win = Win,
      W_raw = W_raw,
      W_scaled = fit_train_valid$W_scaled,
      Wout_train = fit_train$Wout,
      Wout_train_validation = fit_train_valid$Wout,
      params = p
    ),
    predictions = list(
      validation_real = valid,
      validation_pred = fc_valid$pred,
      test_real = test,
      test_pred = fc_test$pred
    )
  )
}

ci95 <- function(x) {
  x <- x[is.finite(x)]
  if (length(x) < 2L) return(c(NA_real_, NA_real_))
  m <- mean(x)
  e <- qt(0.975, df = length(x) - 1L) * sd(x) / sqrt(length(x))
  c(m - e, m + e)
}

summarise_metric <- function(df, metric) {
  x <- df[[metric]]
  ci <- ci95(x)
  data.frame(
    metric = metric,
    n = sum(is.finite(x)),
    mean = mean(x, na.rm = TRUE),
    median = median(x, na.rm = TRUE),
    sd = sd(x, na.rm = TRUE),
    ci95_low = ci[1],
    ci95_high = ci[2],
    min = min(x, na.rm = TRUE),
    max = max(x, na.rm = TRUE),
    stringsAsFactors = FALSE
  )
}

pairwise_wilcoxon <- function(raw, metric) {
  sc <- unique(raw$scenario)
  pairs <- combn(sc, 2L, simplify = FALSE)
  out <- lapply(pairs, function(pp) {
    a <- raw[raw$scenario == pp[1], c("seed", metric)]
    b <- raw[raw$scenario == pp[2], c("seed", metric)]
    names(a)[2] <- "a"
    names(b)[2] <- "b"
    z <- merge(a, b, by = "seed", all = FALSE)
    z <- z[is.finite(z$a) & is.finite(z$b), ]
    if (nrow(z) < 2L) return(NULL)
    wt <- suppressWarnings(wilcox.test(z$a, z$b, paired = TRUE, exact = FALSE))
    d <- z$a - z$b
    data.frame(
      metric = metric,
      scenario_a = pp[1],
      scenario_b = pp[2],
      n_pairs = nrow(z),
      median_diff_a_minus_b = median(d),
      mean_diff_a_minus_b = mean(d),
      p_value = wt$p.value,
      stringsAsFactors = FALSE
    )
  })
  do.call(rbind, out)
}

# -----------------------------------------------------------------------------
# Execução
# -----------------------------------------------------------------------------
data <- carregar_dados_acao(asset)
split <- dividir_dados(data)

timestamp <- format(Sys.time(), "%Y%m%d_%H%M%S")
run_dir <- file.path(output_root, paste0(asset, "_", timestamp))
dir.create(run_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(file.path(run_dir, "matrices"), recursive = TRUE, showWarnings = FALSE)
if (save_predictions) dir.create(file.path(run_dir, "predictions"), recursive = TRUE, showWarnings = FALSE)

seeds <- seed_base + seq_len(n_seeds) - 1L
rows <- list()
k <- 0L
total <- length(scenarios) * length(seeds)

cat(sprintf("\nESNAUTO seed validation\nAtivo: %s\nCenários: %d\nSeeds/cenário: %d\nTotal: %d\nSaída: %s\n\n",
            asset, length(scenarios), n_seeds, total, run_dir))

for (scenario_name in names(scenarios)) {
  scenario <- scenarios[[scenario_name]]
  scen_dir <- file.path(run_dir, "matrices", scenario_name)
  dir.create(scen_dir, recursive = TRUE, showWarnings = FALSE)
  if (save_predictions) {
    dir.create(file.path(run_dir, "predictions", scenario_name),
               recursive = TRUE, showWarnings = FALSE)
  }

  for (seed in seeds) {
    k <- k + 1L
    cat(sprintf("[%03d/%03d] %-16s seed=%d ... ",
                k, total, scenario_name, seed))
    flush.console()

    res <- tryCatch(
      evaluate_scenario_seed(data, split, scenario_name, scenario, seed),
      error = function(e) e
    )

    if (inherits(res, "error")) {
      cat(sprintf("ERRO: %s\n", res$message))
      rows[[length(rows) + 1L]] <- data.frame(
        asset = asset,
        protocol = "fixed_hyperparams_seed_robustness_v1",
        scenario = scenario_name,
        historical_id = scenario$historical_id,
        win_distribution = scenario$win_dist,
        w_distribution = scenario$w_dist,
        seed = seed,
        a = scenario$params$a,
        sr = scenario$params$sr,
        initLen = scenario$params$initLen,
        reservoir_size = scenario$params$tam_reservoir,
        lambda = scenario$params$reg,
        mae_validation = NA_real_, rmse_validation = NA_real_, r2_validation = NA_real_,
        mae_test = NA_real_, rmse_test = NA_real_, r2_test = NA_real_,
        fit_eval_time_s = NA_real_,
        error = res$message,
        stringsAsFactors = FALSE
      )
      next
    }

    matrix_file <- file.path(scen_dir, sprintf("seed_%d.rds", seed))
    saveRDS(res$matrices, matrix_file)

    if (save_predictions) {
      saveRDS(
        res$predictions,
        file.path(run_dir, "predictions", scenario_name, sprintf("seed_%d.rds", seed))
      )
    }

    res$row$matrix_file <- normalizePath(matrix_file, winslash = "/", mustWork = FALSE)
    res$row$error <- ""
    rows[[length(rows) + 1L]] <- res$row

    cat(sprintf("MAE val=%.6f | MAE test=%.6f | %.3fs\n",
                res$row$mae_validation, res$row$mae_test, res$row$fit_eval_time_s))
  }
}

raw <- do.call(rbind, rows)
raw_file <- file.path(run_dir, "seed_results_raw.csv")
write.csv(raw, raw_file, row.names = FALSE, fileEncoding = "UTF-8")

metrics <- c("mae_validation", "rmse_validation", "r2_validation",
             "mae_test", "rmse_test", "r2_test")

summary_rows <- list()
for (s in names(scenarios)) {
  d <- raw[raw$scenario == s, ]
  for (m in metrics) {
    sm <- summarise_metric(d, m)
    sm$scenario <- s
    sm$historical_id <- scenarios[[s]]$historical_id
    summary_rows[[length(summary_rows) + 1L]] <- sm
  }
}
summary_df <- do.call(rbind, summary_rows)
summary_df <- summary_df[, c("scenario", "historical_id", "metric", "n", "mean",
                             "median", "sd", "ci95_low", "ci95_high", "min", "max")]
write.csv(summary_df, file.path(run_dir, "seed_results_summary.csv"),
          row.names = FALSE, fileEncoding = "UTF-8")

test_metrics <- c("mae_test", "rmse_test", "r2_test")
tests <- do.call(rbind, lapply(test_metrics, function(m) pairwise_wilcoxon(raw, m)))
if (!is.null(tests) && nrow(tests) > 0L) {
  tests$p_holm <- ave(tests$p_value, tests$metric,
                      FUN = function(p) p.adjust(p, method = "holm"))
  write.csv(tests, file.path(run_dir, "pairwise_wilcoxon_test.csv"),
            row.names = FALSE, fileEncoding = "UTF-8")
}

manifest <- list(
  protocol = "fixed_hyperparams_seed_robustness_v1",
  created_at = format(Sys.time(), "%Y-%m-%dT%H:%M:%S%z"),
  asset = asset,
  observations = length(data),
  train_n = split$idx$treino_n,
  validation_n = split$idx$valida_n,
  test_n = split$idx$teste_n,
  seeds = seeds,
  n_seeds = n_seeds,
  seed_base = seed_base,
  scenarios = scenarios,
  distribution_parameters = list(
    Normal = list(mean = 0, sd = 1),
    Laplace = list(mean = 0, sd = 1),
    Cauchy = list(location = 0, scale = 1)
  ),
  test_protocol = paste(
    "Hyperparameters fixed from historical runs.",
    "Validation: fit on training only.",
    "Final test: same Win/W seed, refit readout on contiguous training+validation,",
    "then one-step-ahead evaluation on untouched test.",
    "No scenario is selected using the new test results."
  )
)

if (requireNamespace("jsonlite", quietly = TRUE)) {
  jsonlite::write_json(manifest, file.path(run_dir, "manifest.json"),
                       pretty = TRUE, auto_unbox = TRUE)
} else {
  dput(manifest, file = file.path(run_dir, "manifest.R"))
}

cat("\nConcluído.\n")
cat(sprintf("Resultados brutos: %s\n", raw_file))
cat(sprintf("Resumo: %s\n", file.path(run_dir, "seed_results_summary.csv")))
if (exists("tests") && !is.null(tests)) {
  cat(sprintf("Comparações pareadas: %s\n",
              file.path(run_dir, "pairwise_wilcoxon_test.csv")))
}
