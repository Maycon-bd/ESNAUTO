# =============================================================================
# history_tracker.R — Rastreador e Histórico Persistente de Otimizações do GA
# Salva em CSV, compara com execuções anteriores e mantém recordes globais
# =============================================================================

# Caminhos padrão do arquivo histórico CSV
OBTER_CAMINHO_HISTORICO_CSV <- function() {
  caminhos <- c(
    "../Scripts/results/historico_otimizacoes_ga.csv",
    "Scripts/results/historico_otimizacoes_ga.csv",
    "data/historico_otimizacoes_ga.csv",
    "../data/historico_otimizacoes_ga.csv"
  )
  for (cp in caminhos) {
    dir_pai <- dirname(cp)
    if (dir.exists(dir_pai)) {
      return(cp)
    }
  }
  # Fallback: criar no diretório atual
  if (!dir.exists("data")) dir.create("data", recursive = TRUE)
  return("data/historico_otimizacoes_ga.csv")
}

# Inicializar o arquivo CSV caso não exista
inicializar_historico_csv <- function() {
  caminho_csv <- OBTER_CAMINHO_HISTORICO_CSV()
  if (!file.exists(caminho_csv)) {
    cabecalhos <- data.frame(
      id_execucao = character(),
      timestamp = character(),
      geracoes = character(),
      pop_size = integer(),
      dist_win = character(),
      dist_w = character(),
      a = numeric(),
      sr = numeric(),
      initLen = integer(),
      tam_reservoir = integer(),
      reg = numeric(),
      fitness = numeric(),
      mae_valida = numeric(),
      rmse_valida = numeric(),
      mae_teste = numeric(),
      rmse_teste = numeric(),
      r2_teste = numeric(),
      tempo_segundos = numeric(),
      delta_anterior_pct = character(),
      delta_recorde_pct = character(),
      eh_novo_recorde = logical(),
      stringsAsFactors = FALSE
    )
    # Criar diretório se necessário
    dir.create(dirname(caminho_csv), recursive = TRUE, showWarnings = FALSE)
    write.table(cabecalhos, file = caminho_csv, sep = ";", row.names = FALSE, col.names = TRUE, dec = ".")
  }
  return(caminho_csv)
}

# Carregar o histórico completo de execuções
carregar_historico_ga <- function() {
  caminho_csv <- inicializar_historico_csv()
  tryCatch({
    df <- read.table(caminho_csv, sep = ";", header = TRUE, stringsAsFactors = FALSE, dec = ".")
    if (nrow(df) > 0) {
      df <- df[order(as.POSIXct(df$timestamp), decreasing = TRUE), ]
    }
    return(df)
  }, error = function(e) {
    return(data.frame())
  })
}

# Registrar uma nova execução do GA e calcular deltas contra o histórico
registrar_execucao_ga <- function(params, metricas_valida, metricas_teste, fitness, 
                                   geracoes, pop_size, dist_win, dist_w, tempo_s,
                                   Win = NULL, W = NULL, Wout = NULL) {
  caminho_csv <- inicializar_historico_csv()
  historico <- carregar_historico_ga()
  
  novo_id <- sprintf("GA_RUN_%04d", nrow(historico) + 1)
  ts_atual <- format(Sys.time(), "%Y-%m-%d %H:%M:%S")
  
  mae_atual_val <- metricas_valida$MAE
  mae_atual_teste <- metricas_teste$MAE
  
  delta_anterior_pct <- "— (Primeira Execução)"
  delta_recorde_pct <- "— (Primeiro Recorde)"
  eh_novo_recorde <- TRUE
  
  if (nrow(historico) > 0) {
    # 1. Comparação com a Execução Imediatamente Anterior
    ultima_exec <- historico[1, ]
    mae_ant_val <- as.numeric(ultima_exec$mae_valida)
    dif_ant <- ((mae_atual_val - mae_ant_val) / mae_ant_val) * 100
    
    if (dif_ant < 0) {
      delta_anterior_pct <- sprintf("🟢 %.2f%% melhor que a anterior", abs(dif_ant))
    } else if (dif_ant > 0) {
      delta_anterior_pct <- sprintf("🔴 +%.2f%% pior que a anterior", dif_ant)
    } else {
      delta_anterior_pct <- "⚪ Idêntico à anterior"
    }
    
    # 2. Comparação com o Melhor Recorde Global de Todos os Tempos (menor MAE de validação)
    melhor_mae_historico <- min(as.numeric(historico$mae_valida), na.rm = TRUE)
    
    if (mae_atual_val < melhor_mae_historico) {
      dif_rec <- ((mae_atual_val - melhor_mae_historico) / melhor_mae_historico) * 100
      delta_recorde_pct <- sprintf("🏆 NOVO RECORDE GLOBAL! (Superou em %.2f%%)", abs(dif_rec))
      eh_novo_recorde <- TRUE
    } else {
      dif_rec <- ((mae_atual_val - melhor_mae_historico) / melhor_mae_historico) * 100
      delta_recorde_pct <- sprintf("Recorde Atual: %.4f (+%.2f%%)", melhor_mae_historico, dif_rec)
      eh_novo_recorde <- FALSE
    }
  }
  
  # Nova linha para o CSV
  nova_linha <- data.frame(
    id_execucao = novo_id,
    timestamp = ts_atual,
    geracoes = as.character(geracoes),
    pop_size = as.integer(pop_size),
    dist_win = dist_win,
    dist_w = dist_w,
    a = round(as.numeric(params$a), 6),
    sr = round(as.numeric(params$sr), 6),
    initLen = as.integer(params$initLen),
    tam_reservoir = as.integer(params$tam_reservoir),
    reg = as.numeric(params$reg),
    fitness = round(as.numeric(fitness), 6),
    mae_valida = round(as.numeric(metricas_valida$MAE), 6),
    rmse_valida = round(as.numeric(metricas_valida$RMSE), 6),
    mae_teste = round(as.numeric(metricas_teste$MAE), 6),
    rmse_teste = round(as.numeric(metricas_teste$RMSE), 6),
    r2_teste = round(as.numeric(metricas_teste$R2), 4),
    tempo_segundos = round(as.numeric(tempo_s), 2),
    delta_anterior_pct = delta_anterior_pct,
    delta_recorde_pct = delta_recorde_pct,
    eh_novo_recorde = eh_novo_recorde,
    stringsAsFactors = FALSE
  )
  
  # Salvar no CSV (modo append)
  write.table(nova_linha, file = caminho_csv, sep = ";", row.names = FALSE, col.names = FALSE, 
              append = TRUE, dec = ".")
  
  # Se for novo recorde global e matrizes forem fornecidas, salvar matrizes oficiais
  if (eh_novo_recorde && !is.null(Win) && !is.null(W)) {
    dir_recorde <- file.path(dirname(caminho_csv), "melhor_recorde_global")
    dir.create(dir_recorde, recursive = TRUE, showWarnings = FALSE)
    
    write.table(Win, file = file.path(dir_recorde, "matriz_Win_recorde.txt"), row.names = FALSE, col.names = FALSE)
    write.table(W, file = file.path(dir_recorde, "matriz_W_recorde.txt"), row.names = FALSE, col.names = FALSE)
    if (!is.null(Wout)) {
      write.table(Wout, file = file.path(dir_recorde, "matriz_Wout_recorde.txt"), row.names = FALSE, col.names = FALSE)
    }
  }
  
  list(
    id = novo_id,
    timestamp = ts_atual,
    eh_novo_recorde = eh_novo_recorde,
    delta_anterior = delta_anterior_pct,
    delta_recorde = delta_recorde_pct,
    mae_valida = mae_atual_val,
    mae_teste = mae_atual_teste
  )
}
