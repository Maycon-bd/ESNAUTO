# Execute da raiz do repositorio. Auditoria conservadora: nunca substitui a ESN.
if (.Platform$OS.type == "windows") Sys.setlocale("LC_CTYPE", "English_United States.utf8")
options(warn = 2)
args <- commandArgs(trailingOnly = TRUE)
out <- if (length(args)) args[1] else "Scripts/results/diebold_mariano"
stopifnot(file.exists("app/utils/esn_core.R"))
if (dir.exists(out)) stop("Diretorio de saida existente; use um novo caminho. Nada sobrescrito.")
original <- list.files(".", recursive = TRUE, full.names = TRUE, all.files = TRUE)
original <- original[!grepl("^./.git/", original) & !dir.exists(original)]
hash_before <- tools::md5sum(original)
dir.create(out, recursive = TRUE)
writeLines(capture.output(sessionInfo()), file.path(out, "sessionInfo_R.txt"))
write.csv(data.frame(path = original, md5 = unname(hash_before)),
          file.path(out, "inventario_arquivos.csv"), row.names = FALSE)

# Inventario de todos os ZIPs, incluindo conteudo de ZIPs aninhados.
zip_rows <- list(); text_hits <- list()
audit_zip <- function(path, label = path, depth = 0L) {
  if (depth > 10L) stop("Profundidade ZIP inesperada; intervencao necessaria.")
  entries <- unzip(path, list = TRUE)
  zip_rows[[length(zip_rows) + 1L]] <<- data.frame(
    archive = label, member = entries$Name, bytes = entries$Length)
  for (name in entries$Name[!grepl("/$", entries$Name)]) {
    con <- unz(path, name, open = "rb")
    bytes <- tryCatch(readBin(con, "raw", n = entries$Length[match(name, entries$Name)]),
                      finally = close(con))
    if (length(bytes) != entries$Length[match(name, entries$Name)]) stop("Membro ZIP incompleto: ", name)
    if (grepl("\\.zip$", name, ignore.case = TRUE)) {
      tmp <- tempfile(fileext = ".zip")
      writeBin(bytes, tmp)
      tryCatch(audit_zip(tmp, paste(label, name, sep = "::"), depth + 1L),
               finally = unlink(tmp))
    } else if (grepl("\\.(csv|json|log|txt|md|R|py)$", name, ignore.case = TRUE)) {
      s <- strsplit(rawToChar(bytes), "\n", fixed = TRUE)[[1]]
      hits <- grep("GA_RUN_0030|Laplace", s, useBytes = TRUE)
      if (length(hits)) text_hits[[length(text_hits) + 1L]] <<- data.frame(
        source = paste(label, name, sep = "::"), line = hits, text = s[hits])
    }
  }
}
for (z in original[grepl("\\.zip$", original, ignore.case = TRUE)]) audit_zip(z)
write.csv(do.call(rbind, zip_rows), file.path(out, "inventario_zips.csv"), row.names = FALSE)
for (f in original[grepl("\\.(csv|json|log|txt|md|R|py)$", original, ignore.case = TRUE)]) {
  s <- readLines(f, warn = FALSE, encoding = "UTF-8")
  hits <- grep("GA_RUN_0030|Laplace", s, useBytes = TRUE)
  if (length(hits)) text_hits[[length(text_hits) + 1L]] <- data.frame(source = f, line = hits, text = s[hits])
}
write.csv(do.call(rbind, text_hits), file.path(out, "ocorrencias_historicas.csv"), row.names = FALSE)

# Recuperacao dos registros agregados; nao sao previsoes nem pesos.
archive <- "entrega_tfc_maycon_garcia_silva.zip"
read_history <- function(name) {
  con <- unz(archive, paste0("Scripts/results/", name), open = "r")
  on.exit(close(con))
  read.table(con, header = TRUE, sep = ";", dec = ".", quote = '"',
             comment.char = "", stringsAsFactors = FALSE)
}
ga <- read_history("historico_otimizacoes_ga.csv")
dl <- read_history("historico_dl_benchmark.csv")
champ <- ga[ga$id_execucao == "GA_RUN_0030", ]
stopifnot(nrow(champ) == 1L, champ$dist_win == "Laplace", champ$dist_w == "Normal",
          champ$tam_reservoir == 22L)
write.csv(champ, file.path(out, "registro_GA_RUN_0030.csv"), row.names = FALSE)
write.csv(dl, file.path(out, "historico_dl_recuperado.csv"), row.names = FALSE)

# Leitura explicita do ponto decimal. read.csv2 usa virgula por padrao.
value_path <- "Scripts/data/PETR4_close com factor_2000-2020.txt"
date_path <- "Scripts/data/PETR4_close com factor_2000-2020_com data.csv"
values <- scan(value_path, quiet = TRUE, dec = ".")
dated <- read.table(date_path, sep = ";", dec = ".", colClasses = c("character", "numeric"))
dates <- as.Date(dated[[1]])
stopifnot(length(values) == 5198L, nrow(dated) == 5198L,
          all(is.finite(values)), all(is.finite(dated[[2]])), !anyNA(dates),
          !anyDuplicated(dates), all(diff(dates) > 0),
          dates[1] == as.Date("2000-01-03"), dates[5198] == as.Date("2020-12-30"),
          max(abs(values - dated[[2]])) < 1e-10)
idx <- 3900:5198
alignment <- data.frame(index = idx, data = dates[idx], real = values[idx],
  esn_target_by_code = idx >= 3901L, gru_lstm_target_by_code = TRUE,
  gru_lstm_window_crosses_gap = idx <= 3909L,
  last_input_index = c(2600L, 3900:5197))
write.csv(alignment, file.path(out, "auditoria_indices_datas.csv"), row.names = FALSE)
dims <- do.call(rbind, lapply(c("Win", "W", "Wout"), function(n) {
  path <- paste0("Scripts/results/melhor_recorde_global/matriz_", n, "_recorde.txt")
  m <- as.matrix(read.table(path))
  stopifnot(all(is.finite(m)))
  data.frame(matrix = n, rows = nrow(m), cols = ncol(m), path = path)
}))
write.csv(dims, file.path(out, "auditoria_matrizes.csv"), row.names = FALSE)
packages <- c("forecast", "jsonlite", "keras3", "tensorflow", "reticulate")
write.csv(data.frame(package = packages, available = vapply(packages,
  requireNamespace, logical(1), quietly = TRUE)), file.path(out, "dependencias.csv"), row.names = FALSE)

# Ponto de parada especifico desta auditoria: nao inferir identidade por nome.
# Mesmo matrizes com dimensoes compativeis exigiriam vinculo documental e reproducao.
config <- c('{',
  '  "status": "blocked_missing_historical_matrices",',
  '  "serie": "PETR4 com Fator de Ajuste; arquivos locais oficiais",',
  '  "treino_n": 2600, "validacao_n": 1299, "teste_n": 1299,',
  '  "h": 1, "alpha": 0.05, "alternative": "two.sided",',
  '  "seed": null, "seed_status": "nenhum treinamento executado",',
  '  "esn_source": "unavailable", "esn_metadata_source": "historical_recovered",',
  '  "gru_source": "unavailable", "lstm_source": "unavailable",',
  '  "historical_run": "GA_RUN_0030", "n_aligned": null,',
  '  "expected_n_by_code": 1298, "metric_tolerance_absolute": 0.000001,',
  '  "controlled_rerun_executed": false, "dm_executed": false', '}')
writeLines(config, file.path(out, "configuracao_experimento.json"))
result <- data.frame(comparacao = rep(c("ESN x GRU", "ESN x LSTM"), 2),
  perda = rep(c("absoluta", "quadratica"), each = 2), power = rep(1:2, each = 2),
  n = NA_integer_, h = 1L, DM = NA_real_, p_valor = NA_real_,
  perda_media_esn = NA_real_, perda_media_baseline = NA_real_, diferenca_media = NA_real_,
  menor_perda = NA_character_, decisao = "NAO EXECUTADO: matrizes historicas ausentes")
write.csv(result, file.path(out, "resultados_dm.csv"), row.names = FALSE, na = "NA")
summary <- c("AUDITORIA DM - BLOQUEADA; nenhum teste estatistico executado.",
  "1. ESN historica recuperada? NAO. Apenas registro e hiperparametros recuperados do ZIP.",
  "2. Win/W/Wout da GA_RUN_0030 recuperadas? NAO. Matrizes locais: 16x2,16x16,1x18; esperadas:22x2,22x22,1x24.",
  "3. GRU oficial recuperada? NAO. Somente metricas agregadas de outras execucoes.",
  "4. LSTM oficial recuperada? NAO. Somente metricas agregadas de outras execucoes.",
  "5. Nova execucao controlada necessaria: GRU/LSTM, salvo recuperacao posterior. Nao iniciada pois ESN ausente.",
  "6. Numero final alinhado: indisponivel. 1298 alvos comuns previstos pela auditoria do codigo.",
  "7. MAE/RMSE recalculados: indisponiveis para os tres modelos.",
  "8. ESN x GRU MAE: DM=NA,p=NA; ESN x LSTM MAE: DM=NA,p=NA; ESN x GRU MSE: DM=NA,p=NA; ESN x LSTM MSE: DM=NA,p=NA.",
  "9. Significancia: nao avaliada; H1 nao avaliada inferencialmente.",
  "11. Limitacoes: falta de pesos/previsoes historicos; forecast/keras3/tensorflow ausentes; selecao posterior da campea.",
  "Solicitada intervencao: localizar backup da GA_RUN_0030. Nao executar novo GA como substituto.")
stopifnot(identical(unname(hash_before), unname(tools::md5sum(original))))
writeLines("PASS: hashes MD5 de todos os arquivos preexistentes preservados.", file.path(out, "validacao_preservacao.txt"))
summary <- c(summary, "10. Artefatos:", list.files(out, full.names = TRUE))
writeLines(summary, file.path(out, "resultado_dm.txt"))
cat(paste(summary, collapse = "\n"), "\n")
quit(status = 2L) # Bloqueio cientifico intencional; nunca sinalizar sucesso inferencial.
