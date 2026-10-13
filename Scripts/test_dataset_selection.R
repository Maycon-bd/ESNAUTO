# Execute a partir da raiz do projeto: Rscript Scripts/test_dataset_selection.R
invisible(Sys.setlocale("LC_CTYPE", "English_United States.utf8"))
local_lib <- file.path(Sys.getenv("LOCALAPPDATA"), "R/win-library", paste(R.version$major, strsplit(R.version$minor, ".", fixed = TRUE)[[1]][1], sep = "."))
if (dir.exists(local_lib)) .libPaths(c(local_lib, .libPaths()))
source("app/utils/data_prep.R", encoding = "UTF-8")
petr <- carregar_dados_acao("PETR4")
vale <- carregar_dados_acao("VALE3")
stopifnot(length(petr) == 5198, length(vale) == 5192,
          identical(unname(unlist(particoes_dados(vale))), c(2596, 1298, 1298)),
          all(is.finite(vale)), all(vale > 0))
stopifnot(inherits(try(carregar_dados_acao("INVALIDA"), silent = TRUE), "try-error"))
attr(vale, "particoes") <- list(treino_n = 200L, valida_n = 100L, teste_n = 100L)
stopifnot(length(dividir_dados(vale)$teste) == 100L)
attr(vale, "particoes") <- list(treino_n = 3000L, valida_n = 2000L, teste_n = 1000L)
stopifnot(inherits(try(dividir_dados(vale), silent = TRUE), "try-error"))

setwd("app")
source("app.R", encoding = "UTF-8")
# Isolar arquivos de histórico dos dados científicos existentes.
test_dir <- tempfile("dataset_test_")
dir.create(test_dir)
OBTER_CAMINHO_HISTORICO_CSV <- function() caminho_por_acao(file.path(test_dir, "ga.csv"))
OBTER_CAMINHO_HISTORICO_DL_CSV <- function() caminho_por_acao(file.path(test_dir, "dl.csv"))
# Reproduzir a abertura real: testServer isola implicitamente a criação do
# servidor e, sozinho, não detecta leituras reativas indevidas na inicialização.
startup_session <- shiny::MockShinySession$new()
shiny::withReactiveDomain(startup_session, {
  server(startup_session$input, startup_session$output, startup_session)
})
startup_session$close()
shiny::testServer(server, {
  session$setInputs(acao_dataset = "PETR4", treino_n = 2600, valida_n = 1299, teste_n = 1299)
  stopifnot(length(dados()) == 5198, acao_atual() == "PETR4")
  resultado_esn_externo(list(modelo = "ESN", metricas = list(modelo = "ESN")))
  ultimo_benchmark_executado(list(acao = "PETR4"))
  session$flushReact()
  session$setInputs(acao_dataset = "VALE3", treino_n = 2596, valida_n = 1298, teste_n = 1298)
  stopifnot(length(dados()) == 5192, acao_atual() == "VALE3",
            is.null(resultado_esn_externo()), is.null(ultimo_benchmark_executado()),
            is.null(metricas_esn()), is.null(metricas_lstm()), is.null(metricas_gru()),
            grepl("VALE3", OBTER_CAMINHO_HISTORICO_CSV()),
            nrow(carregar_historico_ga()) == 0, is.null(carregar_resultado_dl("LSTM")))
  met <- list(MAE = 1, RMSE = 2, R2 = 0.5)
  salvar_resultado_dl("LSTM", met, met, 1)
  stopifnot(carregar_resultado_dl("LSTM")$teste$metricas$MAE == 1)
  session$userData$execucao_ativa <- TRUE
  session$setInputs(acao_dataset = "PETR4")
  stopifnot(acao_atual() == "VALE3", length(dados()) == 5192)
  session$userData$execucao_ativa <- FALSE
  session$setInputs(acao_dataset = "PETR4", treino_n = 2600, valida_n = 1299, teste_n = 1299)
  stopifnot(acao_atual() == "PETR4", is.null(carregar_resultado_dl("LSTM")))
})
# Inferência real da ESN com reservatório pequeno nos dois datasets.
set.seed(123)
params <- list(a = 0.8, sr = 0.4, initLen = 10, tam_reservoir = 8, reg = 0.001)
win <- matrix(runif(16, -0.1, 0.1), 8, 2)
w <- matrix(runif(64, -0.1, 0.1), 8, 8)
for (acao in names(datasets_disponiveis)) {
  ds <- dividir_dados(carregar_dados_acao(acao))
  validacao <- esn_validacao(ds, params, win, w)
  teste <- esn_teste(ds, params, win, w, validacao$Wout)
  stopifnot(length(validacao$previsao_valida) == ds$idx$valida_n,
            length(teste$previsao_teste) == ds$idx$teste_n,
            all(is.finite(validacao$previsao_valida)), all(is.finite(teste$previsao_teste)),
            is.finite(validacao$metricas_valida$MAE), is.finite(teste$metricas_teste$MAE))
}
unlink(test_dir, recursive = TRUE)
cat("OK: leitura, partições, troca de ação, bloqueio durante execução, históricos separados e inferência ESN.\n")
