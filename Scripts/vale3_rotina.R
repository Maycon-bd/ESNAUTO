args <- commandArgs(trailingOnly = TRUE)
root <- normalizePath(args[1], winslash = "/", mustWork = TRUE)
out <- file.path(root, "Scripts/results/VALE3/producao_comparacao")
dir.create(out, recursive = TRUE, showWarnings = FALSE)
setwd(file.path(root, "app"))
Sys.setlocale("LC_CTYPE", "Portuguese_Brazil.utf8")
source("utils/ga_engine.R", encoding = "UTF-8")
# A rotina é independente de sessões Shiny e grava exclusivamente na VALE3.
acao_historico <- function() "VALE3"
dados <- carregar_dados_acao("VALE3")
split <- dividir_dados(dados)
grade <- data.frame(win = c("Normal", "Uniforme", "GED", "GED"),
                    w = c("Normal", "Uniforme", "Uniforme", "Normal"))
saveRDS(list(acao = "VALE3", amostras = length(dados), particoes = split$idx,
             md5 = tools::md5sum(file.path(root, "Scripts/data/VALE3_close com factor_2000-2020.txt")),
             grade = grade, rodadas = 3, maxiter = 10000, pop_size = 10,
             run_stop = 3500, anti_estagnacao = TRUE,
             sessionInfo = sessionInfo()), file.path(out, "protocolo.rds"))
for (rodada in 1:3) for (i in seq_len(nrow(grade))) {
  id <- sprintf("rodada_%d_cenario_%d", rodada, i)
  destino <- file.path(out, paste0(id, ".rds"))
  if (file.exists(destino)) {
    antigo <- readRDS(destino)
    if (identical(antigo$status, "concluido")) next
  }
  seed <- 20261012L + rodada * 100L + i
  set.seed(seed)
  writeLines(sprintf("Em execução: %s | Win %s | W %s | %s", id, grade$win[i], grade$w[i], Sys.time()),
             file.path(out, "status.txt"))
  cat(sprintf("\nINICIO %s Win=%s W=%s seed=%d\n", id, grade$win[i], grade$w[i], seed))
  flush.console()
  res <- otimizar_esn_ga_live(dados, win_dist = grade$win[i], w_dist = grade$w[i],
                            maxiter = 10000, pop_size = 10, run_stop = 3500,
                            anti_estagnacao = TRUE,
                            set_progress = function(p, msg) {
                              writeLines(sprintf("%s | %s | %s", id, Sys.time(), msg), file.path(out, "status.txt"))
                            })
  if (isTRUE(res$cancelado)) stop("Execução cancelada; cenário não marcado como concluído")
  registro <- list(status = "concluido", id = id, rodada = rodada, seed = seed,
                   win = grade$win[i], w = grade$w[i], fim = Sys.time(), resultado = res)
  saveRDS(registro, paste0(destino, ".tmp"))
  if (!file.rename(paste0(destino, ".tmp"), destino)) stop("Falha ao salvar resultado")
  m <- res$teste$metricas_teste
  v <- res$validacao$metricas_valida
  linha <- data.frame(id = id, rodada = rodada, seed = seed, Win = grade$win[i], W = grade$w[i],
                      geracoes_reais = res$iter_executadas, MAE_valida = v$MAE,
                      RMSE_valida = v$RMSE, MAE_teste = m$MAE, RMSE_teste = m$RMSE,
                      R2_teste = m$R2, tempo_s = res$tempo)
  write.csv(linha, file.path(out, paste0(id, ".csv")), row.names = FALSE)
  cat(sprintf("CONCLUIDO %s\n", id))
  flush.console()
}
arquivos <- list.files(out, pattern = "^rodada_.*\\.csv$", full.names = TRUE)
tabela <- do.call(rbind, lapply(arquivos, read.csv))
write.csv(tabela, file.path(out, "resultados_consolidados.csv"), row.names = FALSE)
writeLines(sprintf("CONCLUIDO: %d/12 cenários | %s", nrow(tabela), Sys.time()), file.path(out, "status.txt"))
