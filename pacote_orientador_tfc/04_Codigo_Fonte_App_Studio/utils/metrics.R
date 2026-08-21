# =============================================================================
# metrics.R — Funções de métricas padronizadas para comparação de modelos
# =============================================================================

#' Calcula MAE (Mean Absolute Error)
#' @param real Vetor de valores reais
#' @param previsto Vetor de valores previstos
#' @return Valor do MAE
calcular_mae <- function(real, previsto) {
  mean(abs(real - previsto))
}

#' Calcula RMSE (Root Mean Squared Error)
#' @param real Vetor de valores reais
#' @param previsto Vetor de valores previstos
#' @return Valor do RMSE
calcular_rmse <- function(real, previsto) {
  sqrt(mean((real - previsto)^2))
}

#' Calcula MAPE (Mean Absolute Percentage Error)
#' @param real Vetor de valores reais
#' @param previsto Vetor de valores previstos
#' @return Valor do MAPE em percentual
calcular_mape <- function(real, previsto) {
  # Evita divisão por zero
  idx <- which(real != 0)
  if (length(idx) == 0) return(NA)
  mean(abs((real[idx] - previsto[idx]) / real[idx])) * 100
}

#' Calcula R² (Coeficiente de Determinação)
#' @param real Vetor de valores reais
#' @param previsto Vetor de valores previstos
#' @return Valor do R²
calcular_r2 <- function(real, previsto) {
  ss_res <- sum((real - previsto)^2)
  ss_tot <- sum((real - mean(real))^2)
  if (ss_tot == 0) return(NA)
  1 - (ss_res / ss_tot)
}

#' Calcula todas as métricas de uma vez
#' @param real Vetor de valores reais
#' @param previsto Vetor de valores previstos
#' @param tempo_exec Tempo de execução em segundos (opcional)
#' @return Data frame com todas as métricas
calcular_todas_metricas <- function(real, previsto, tempo_exec = NA) {
  data.frame(
    MAE   = calcular_mae(real, previsto),
    RMSE  = calcular_rmse(real, previsto),
    MAPE  = calcular_mape(real, previsto),
    R2    = calcular_r2(real, previsto),
    Tempo_s = tempo_exec,
    stringsAsFactors = FALSE
  )
}

#' Formata tempo em segundos para formato legível (HH:MM:SS ou mm ss)
#' @param segundos Tempo em segundos
#' @return String formatada amigável
formatar_tempo_hms <- function(segundos) {
  if (is.null(segundos) || is.na(segundos) || !is.numeric(segundos)) return("00s")
  seg <- as.numeric(segundos)
  if (seg < 60) {
    return(sprintf("%.1f seg", seg))
  } else if (seg < 3600) {
    minutos <- floor(seg / 60)
    segs <- round(seg %% 60)
    return(sprintf("%02dm %02ds", minutos, segs))
  } else {
    horas <- floor(seg / 3600)
    resto <- seg %% 3600
    minutos <- floor(resto / 60)
    segs <- round(resto %% 60)
    return(sprintf("%02dh %02dm %02ds", horas, minutos, segs))
  }
}

#' Calcula Pontuação Multicritério Ponderada (0 a 100) para ranking de modelos
#' @param mae_val Vetor de MAE de validação
#' @param rmse_val Vetor de RMSE de validação
#' @param mae_teste Vetor de MAE de teste
#' @param rmse_teste Vetor de RMSE de teste
#' @param r2_teste Vetor de R2 de teste
#' @param tempo Vetor de tempo de execução
#' @param pesos Lista com pesos de ponderação (soma deve ser 1.0 ou será normalizada)
#' @return Vetor numérico com scores de 0 a 100 para cada modelo
calcular_score_multicriterio <- function(mae_val, rmse_val, mae_teste, rmse_teste, r2_teste, tempo,
                                         pesos = list(mae_teste = 0.30, rmse_teste = 0.20, r2_teste = 0.20,
                                                      mae_val = 0.10, rmse_val = 0.10, tempo = 0.10)) {
  n <- length(mae_teste)
  if (n == 0) return(numeric(0))
  if (n == 1) return(c(100.0))
  
  norm_menor_melhor <- function(v) {
    v <- as.numeric(v)
    v[is.na(v)] <- max(v, na.rm = TRUE)
    min_v <- min(v, na.rm = TRUE)
    max_v <- max(v, na.rm = TRUE)
    if (max_v == min_v) return(rep(1.0, length(v)))
    (max_v - v) / (max_v - min_v)
  }
  
  norm_maior_melhor <- function(v) {
    v <- as.numeric(v)
    v[is.na(v)] <- min(v, na.rm = TRUE)
    min_v <- min(v, na.rm = TRUE)
    max_v <- max(v, na.rm = TRUE)
    if (max_v == min_v) return(rep(1.0, length(v)))
    (v - min_v) / (max_v - min_v)
  }
  
  s_mae_val   <- norm_menor_melhor(mae_val)
  s_rmse_val  <- norm_menor_melhor(rmse_val)
  s_mae_teste <- norm_menor_melhor(mae_teste)
  s_rmse_teste<- norm_menor_melhor(rmse_teste)
  s_r2_teste  <- norm_maior_melhor(r2_teste)
  s_tempo     <- norm_menor_melhor(tempo)
  
  soma_pesos <- sum(unlist(pesos))
  w <- lapply(pesos, function(x) x / soma_pesos)
  
  score <- (
    w$mae_teste  * s_mae_teste +
    w$rmse_teste * s_rmse_teste +
    w$r2_teste   * s_r2_teste +
    w$mae_val    * s_mae_val +
    w$rmse_val   * s_rmse_val +
    w$tempo      * s_tempo
  ) * 100
  
  return(round(score, 1))
}


