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
