root <- normalizePath(commandArgs(TRUE)[1], winslash = "/")
setwd(file.path(root, "app"))
Sys.setlocale("LC_CTYPE", "Portuguese_Brazil.utf8")
source("utils/data_prep.R", encoding = "UTF-8")
source("utils/metrics.R", encoding = "UTF-8")
out <- file.path(root, "reports/vale3_comparacao")
dir.create(out, recursive = TRUE, showWarnings = FALSE)
files <- list.files(file.path(root, "Scripts/results/VALE3/producao_comparacao"), "^rodada_.*\\.rds$", full.names = TRUE)
stopifnot(length(files) == 12)
d <- carregar_dados_acao("VALE3"); s <- dividir_dados(d)
nt <- s$idx$treino_n; nv <- s$idx$valida_n; ne <- s$idx$teste_n
real <- s$treina_testa[(nt+2):(nt+ne)]
realval <- s$treino_valida[(nt+2):(nt+nv)]
rows <- lapply(files, function(f) {
  x <- readRDS(f); r <- x$resultado
  pred <- head(r$teste$previsao_teste, ne-1)
  pv <- head(r$validacao$previsao_valida, nv-1)
  stopifnot(all(is.finite(pred)), abs(mean(abs(real-pred))-r$teste$metricas_teste$MAE)<1e-9,
            abs(mean(abs(realval-pv))-r$validacao$metricas_valida$MAE)<1e-9)
  write.csv(data.frame(indice = (nt+nv+2):(nt+nv+ne), real=real, previsto=pred, erro=real-pred),
            file.path(out,paste0(x$id,"_previsoes.csv")), row.names=FALSE)
  p <- r$params
  data.frame(id=x$id, rodada=x$rodada, Win=x$win, W=x$w, seed=x$seed,
             fitness=r$fitness, geracoes=r$iter_executadas, cataclismos=r$total_cataclismos,
             a=p$a, sr=p$sr, initLen=p$initLen, Nx=p$tam_reservoir, reg=p$reg,
             MAE_valida=r$validacao$metricas_valida$MAE, RMSE_valida=r$validacao$metricas_valida$RMSE,
             MAE_teste=mean(abs(real-pred)), RMSE_teste=sqrt(mean((real-pred)^2)),
             NMAE_pct=100*mean(abs(real-pred))/mean(abs(real)),
             NRMSE_pct=100*sqrt(mean((real-pred)^2))/mean(abs(real)),
             R2=r$teste$metricas_teste$R2, tempo_s=r$tempo)
})
write.csv(do.call(rbind,rows),file.path(out,"execucoes_auditadas.csv"),row.names=FALSE)
base <- lapply(c("PETR4","VALE3"), function(a) {
  sp <- dividir_dados(carregar_dados_acao(a)); n <- sp$idx$treino_n; k <- sp$idx$teste_n
  y <- sp$treina_testa[(n+2):(n+k)]; persist <- sp$treina_testa[(n+1):(n+k-1)]
  data.frame(acao=a, treino_n=n,valida_n=sp$idx$valida_n,teste_n=k,avaliados=length(y),
             media_teste=mean(abs(y)),MAE_persistencia=mean(abs(y-persist)),
             RMSE_persistencia=sqrt(mean((y-persist)^2)))
})
write.csv(do.call(rbind,base),file.path(out,"escalas_e_persistencia.csv"),row.names=FALSE)
cat("Auditoria: 12 previsões e métricas conferidas.\n")
