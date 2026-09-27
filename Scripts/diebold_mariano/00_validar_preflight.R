# Fase I: somente dados, indices e metadados. Nao carrega codigo de modelos.
if (.Platform$OS.type == "windows") invisible(Sys.setlocale("LC_CTYPE", "English_United States.utf8"))
out <- "Scripts/results/diebold_mariano/preflight_fase_I"
dir.create(out, recursive = TRUE, showWarnings = FALSE)
targets <- file.path(out, c("validacao_serie.csv", "alinhamento_previsto.csv", "ambiente_R.txt", "dependencias.csv"))
if (any(file.exists(targets))) stop("Saidas PRE-FLIGHT existentes: nao sobrescrever.")
p <- "Scripts/data/PETR4_close com factor_2000-2020.txt"
q <- "Scripts/data/PETR4_close com factor_2000-2020_com data.csv"
y <- scan(p, quiet = TRUE, dec = ".")
d <- read.table(q, sep = ";", dec = ".", colClasses = c("character", "numeric"))
dates <- as.Date(d[[1]])
stopifnot(length(y) == 5198L, nrow(d) == 5198L, !anyNA(y), !anyNA(d),
  !anyNA(dates), all(is.finite(y)), all(is.finite(d[[2]])),
  !anyDuplicated(dates), all(diff(dates) > 0), max(abs(y - d[[2]])) < 1e-10,
  dates[1] == as.Date("2000-01-03"), tail(dates, 1) == as.Date("2020-12-30"))
train <- 2600L; val <- 1299L; test <- 1299L
# Derivacao de indices a partir das expressoes dos modulos, sem prever valores.
tt <- c(seq_len(train), (train + val + 1L):(train + val + test))
esn <- tt[(train + 2L):(train + test)]
timesteps <- 10L
target_windows <- (seq_len(length(tt) - timesteps) + timesteps)
dl <- tt[target_windows[(train - timesteps + 1L):length(target_windows)]]
common <- intersect(esn, dl)
stopifnot(length(esn) == 1298L, length(dl) == 1299L, identical(common, 3901:5198))
alignment <- data.frame(indice = dl, data = dates[dl],
  esn_alvo = dl %in% esn, gru_alvo = TRUE, lstm_alvo = TRUE,
  indice_origem = tt[match(dl, tt) - 1L],
  janela_cruza_lacuna = vapply(match(dl, tt), function(i)
    any(diff(tt[(i - timesteps):(i - 1L)]) != 1L), logical(1)))
# A janela inicial contem apenas treino; a descontinuidade esta entre origem e alvo.
alignment$origem_nao_consecutiva <- alignment$indice_origem != alignment$indice - 1L
alignment$data_origem <- dates[alignment$indice_origem]
write.csv(alignment, targets[2], row.names = FALSE)
summary <- data.frame(n_total = length(y), primeira_data = dates[1], ultima_data = tail(dates, 1),
  treino_n = train, validacao_n = val, teste_n = test,
  teste_inicio = dates[train + val + 1L], teste_fim = dates[train + val + test],
  na_valores = sum(is.na(y)), na_datas = sum(is.na(dates)), datas_duplicadas = sum(duplicated(dates)),
  diferenca_maxima_arquivos = max(abs(y - d[[2]])), n_esn = length(esn), n_gru = length(dl),
  n_lstm = length(dl), n_comum_previsto = length(common),
  alinhamento_inicio = dates[min(common)], alinhamento_fim = dates[max(common)])
write.csv(summary, targets[1], row.names = FALSE)
pkgs <- c("forecast", "keras3", "tensorflow", "reticulate", "jsonlite", "pracma")
installed <- installed.packages()
write.csv(data.frame(package = pkgs, installed = pkgs %in% installed[, "Package"],
  version = installed[match(pkgs, installed[, "Package"]), "Version"]), targets[4], row.names = FALSE)
writeLines(c(capture.output(sessionInfo()), "", ".libPaths():", .libPaths(),
  "", "RNGkind atual (nao alterado):", RNGkind(),
  "Nenhuma seed aplicada; nenhuma matriz gerada; nenhum modelo ou DM executado."), targets[3])
print(summary)
cat("PRE-FLIGHT dados/indices: PASS. Nenhum modelo ou DM executado.\n")
