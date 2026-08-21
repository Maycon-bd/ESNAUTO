# =============================================================================
# ga_engine.R — Motor Avançado de Otimização Live por Algoritmo Genético (GA)
# Hipercubo Latino (LHS na Largada) + Cataclismo Anti-Estagnação (CHC Adaptativo)
# =============================================================================

suppressPackageStartupMessages({
  if (!requireNamespace("GA", quietly = TRUE)) install.packages("GA")
  if (!requireNamespace("pracma", quietly = TRUE)) install.packages("pracma")
  library(GA)
  library(pracma)
})

source("utils/data_prep.R", local = TRUE)
source("utils/metrics.R", local = TRUE)
source("utils/esn_core.R", local = TRUE)
source("utils/history_tracker.R", local = TRUE)

# =============================================================================
# 1. GERADOR DE POPULAÇÃO INICIAL POR HIPERCUBO LATINO (LHS)
# =============================================================================

dec_to_binary_vector <- function(val, nbits) {
  val <- max(0, min(val, 2^nbits - 1))
  raw_bits <- as.numeric(intToBits(as.integer(val))[1:nbits])
  as.integer(rev(raw_bits))
}

gerar_populacao_lhs <- function(pop_size, nbits = 55) {
  # 5 Dimensões de Hiperparâmetros:
  # 1. a: 17 bits (1 a 131071)
  # 2. sr: 17 bits (1 a 131071)
  # 3. initLen: 7 bits (0 a 127) -> (+2 = 2 a 129)
  # 4. tam_reservoir: 5 bits (0 a 31) -> (+2 = 2 a 33)
  # 5. reg: 9 bits (0 a 511)
  # Total: 17 + 17 + 7 + 5 + 9 = 55 bits
  
  P <- pop_size
  
  # Estratificação Uniforme por Hipercubo Latino para cada dimensão
  lhs_sample <- function(max_val) {
    strata <- (sample(1:P) - 1 + runif(P)) / P
    round(strata * max_val)
  }
  
  a_vals   <- lhs_sample(131071)
  sr_vals  <- lhs_sample(131071)
  iL_vals  <- lhs_sample(127)
  tr_vals  <- lhs_sample(31)
  reg_vals <- lhs_sample(511)
  
  pop_matrix <- matrix(0, nrow = P, ncol = nbits)
  
  for (i in 1:P) {
    bits_a   <- dec_to_binary_vector(a_vals[i], 17)
    bits_sr  <- dec_to_binary_vector(sr_vals[i], 17)
    bits_iL  <- dec_to_binary_vector(iL_vals[i], 7)
    bits_tr  <- dec_to_binary_vector(tr_vals[i], 5)
    bits_reg <- dec_to_binary_vector(reg_vals[i], 9)
    
    crom <- c(bits_a, bits_sr, bits_iL, bits_tr, bits_reg)
    if (length(crom) < nbits) {
      crom <- c(crom, sample(0:1, nbits - length(crom), replace = TRUE))
    } else if (length(crom) > nbits) {
      crom <- crom[1:nbits]
    }
    
    pop_matrix[i, ] <- crom
  }
  
  pop_matrix
}

# =============================================================================
# CONTROLE GLOBAL DE EXECUÇÃO (PAUSAR / CANCELAR)
# =============================================================================

.controle_ga <- new.env(parent = emptyenv())
.controle_ga$pausado <- FALSE
.controle_ga$cancelar <- FALSE
.controle_ga$servidor_id <- NULL
.controle_ga$porta <- 8089

.flag_cancelar <- file.path(tempdir(), "ga_cancelar.flag")
.flag_pausar   <- file.path(tempdir(), "ga_pausar.flag")

pausar_ga <- function(pausar = TRUE) {
  .controle_ga$pausado <- pausar
  if (pausar) {
    tryCatch(file.create(.flag_pausar, showWarnings = FALSE), error = function(e) {})
  } else {
    if (file.exists(.flag_pausar)) tryCatch(unlink(.flag_pausar), error = function(e) {})
  }
}

cancelar_ga <- function() {
  .controle_ga$cancelar <- TRUE
  tryCatch(file.create(.flag_cancelar, showWarnings = FALSE), error = function(e) {})
}

resetar_controle_ga <- function() {
  .controle_ga$pausado <- FALSE
  .controle_ga$cancelar <- FALSE
  if (file.exists(.flag_cancelar)) tryCatch(unlink(.flag_cancelar), error = function(e) {})
  if (file.exists(.flag_pausar)) tryCatch(unlink(.flag_pausar), error = function(e) {})
}

obter_status_controle_ga <- function() {
  list(
    pausado = isTRUE(.controle_ga$pausado) || file.exists(.flag_pausar), 
    cancelar = isTRUE(.controle_ga$cancelar) || file.exists(.flag_cancelar)
  )
}

iniciar_servidor_controle <- function() {
  if (!is.null(.controle_ga$servidor_id)) {
    return(.controle_ga$porta)
  }
  
  portas_teste <- c(8089, 8090, 8091, 8092)
  for (p in portas_teste) {
    tryCatch({
      .controle_ga$servidor_id <- httpuv::startServer("127.0.0.1", p, list(
        call = function(req) {
          path <- req$PATH_INFO
          if (grepl("cancel", path)) {
            cancelar_ga()
          } else if (grepl("pause", path)) {
            pausar_ga(TRUE)
          } else if (grepl("resume", path)) {
            pausar_ga(FALSE)
          }
          
          status_json <- sprintf('{"pausado": %s, "cancelar": %s}', 
                                 tolower(as.character(isTRUE(.controle_ga$pausado) || file.exists(.flag_pausar))),
                                 tolower(as.character(isTRUE(.controle_ga$cancelar) || file.exists(.flag_cancelar))))
          
          list(
            status = 200L,
            headers = list(
              "Content-Type" = "application/json",
              "Access-Control-Allow-Origin" = "*",
              "Access-Control-Allow-Methods" = "GET, POST, OPTIONS",
              "Access-Control-Allow-Headers" = "*"
            ),
            body = status_json
          )
        }
      ))
      .controle_ga$porta <- p
      break
    }, error = function(e) {})
  }
  
  return(.controle_ga$porta)
}

parar_servidor_controle <- function() {
  if (!is.null(.controle_ga$servidor_id)) {
    tryCatch(httpuv::stopServer(.controle_ga$servidor_id), error = function(e) {})
    .controle_ga$servidor_id <- NULL
  }
}

# Iniciar servidor de controle em segundo plano
tryCatch(iniciar_servidor_controle(), error = function(e) {})

# =============================================================================
# 2. FUNÇÃO PRINCIPAL DE OTIMIZAÇÃO LIVE DO GA COM LHS + CATACLISMO
# =============================================================================

otimizar_esn_ga_live <- function(dados, 
                                 win_dist = "GED", 
                                 w_dist = "Normal", 
                                 maxiter = 200, 
                                 pop_size = 10,
                                 run_stop = NULL,
                                 anti_estagnacao = TRUE,
                                 limite_estagnacao = 30,
                                 set_progress = NULL,
                                 session = NULL) {
  
  if (is.null(run_stop)) {
    run_stop <- if (maxiter >= 5000) 3500 else maxiter
  }
  
  # Registrar referências iniciais de cancelamento / pausa para detecção de clique
  initial_cancel_ts <- if (!is.null(session)) tryCatch(isolate(session$input$btn_cancelar_execucao), error = function(e) NULL) else NULL
  initial_pause_ts  <- if (!is.null(session)) tryCatch(isolate(session$input$btn_pausar_execucao), error = function(e) NULL) else NULL
  initial_resume_ts <- if (!is.null(session)) tryCatch(isolate(session$input$btn_retomar_execucao), error = function(e) NULL) else NULL
  
  # Calibração adaptativa da sensibilidade do Cataclismo
  if (is.null(limite_estagnacao) || limite_estagnacao == 30) {
    limite_estagnacao <- if (maxiter >= 10000) 100 else if (maxiter >= 5000) 80 else if (maxiter >= 1000) 50 else 30
  }
  
  if (is.function(set_progress)) set_progress(0.05, "Inicializando Hipercubo Latino (LHS) e Partições...")
  
  dados_split <- dividir_dados(dados)
  treino <- dados_split$idx$treino_n
  valida <- dados_split$idx$valida_n
  teste  <- dados_split$idx$teste_n
  
  treino_valida <- dados_split$treino_valida
  treina_testa  <- dados_split$treina_testa
  
  inSize <- 1
  outSize <- 1
  
  # Ambiente de estado global do GA
  melhor_estado <- new.env(parent = emptyenv())
  melhor_estado$fitness <- -Inf
  melhor_estado$melhor_cromossomo <- NULL
  melhor_estado$params <- NULL
  melhor_estado$Win <- NULL
  melhor_estado$W <- NULL
  melhor_estado$Wout <- NULL
  melhor_estado$Y_valida <- NULL
  melhor_estado$Y_treino <- NULL
  melhor_estado$iter_sem_melhora <- 0
  melhor_estado$total_cataclismos <- 0
  melhor_estado$modo_cataclismo <- FALSE
  melhor_estado$iter_executadas <- 0
  
  # 1. Função de Fitness
  fitness_func <- function(cromossoma) {
    # Decodificação
    a_GA <- sum(cromossoma[1:17] * 2^(rev(seq(along = cromossoma[1:17])) - 1)) / 131071
    if (a_GA <= 0) a_GA <- 7.62939453125e-6
    
    sr_GA <- sum(cromossoma[18:34] * 2^(rev(seq(along = cromossoma[18:34])) - 1)) / 131071
    if (sr_GA <= 0) sr_GA <- 7.62939453125e-6
    
    initLen_GA <- sum(cromossoma[35:41] * 2^(rev(seq(along = cromossoma[35:41])) - 1)) + 2
    tam_res_GA <- sum(cromossoma[42:46] * 2^(rev(seq(along = cromossoma[42:46])) - 1)) + 2
    
    reg_GA <- sum(cromossoma[47:55] * 2^(rev(seq(along = cromossoma[47:55])) - 1)) / 511
    reg_GA <- (reg_GA + 1e-4) * (1e-4 - 1e-6)
    if (reg_GA <= 0) reg_GA <- 1e-9
    
    # Matrizes de Pesos
    Win_GA <- matrix(gerar_amostras(win_dist, tam_res_GA * (1 + inSize)), nrow = tam_res_GA)
    W_GA   <- matrix(gerar_amostras(w_dist, tam_res_GA * tam_res_GA), nrow = tam_res_GA, ncol = tam_res_GA)
    
    rhoW <- abs(eigen(W_GA, only.values = TRUE)$values[1])
    if (is.na(rhoW) || rhoW == 0) rhoW <- 1
    W_scaled <- sr_GA * W_GA / rhoW
    
    # Treino ESN
    X <- matrix(0, 1 + inSize + tam_res_GA, treino - initLen_GA)
    Yt <- matrix(treino_valida[(initLen_GA + 2):(treino + 1)], 1)
    x <- rep(0, tam_res_GA)
    
    for (t in 1:treino) {
      u <- treino_valida[t]
      x <- (1 - a_GA) * x + a_GA * tanh(Win_GA %*% rbind(1, u) + W_scaled %*% x)
      if (t > initLen_GA) {
        X[, t - initLen_GA] <- rbind(1, u, x)
      }
    }
    
    X_T <- t(X)
    Wout_GA <- tryCatch({
      Yt %*% X_T %*% solve(X %*% X_T + reg_GA * diag(1 + inSize + tam_res_GA))
    }, error = function(e) {
      Yt %*% X_T %*% pracma::pinv(X %*% X_T + reg_GA * diag(1 + inSize + tam_res_GA))
    })
    
    # Validação
    Y_val <- matrix(0, outSize, valida)
    u <- treino_valida[treino + 1]
    for (t in 1:valida) {
      x <- (1 - a_GA) * x + a_GA * tanh(Win_GA %*% rbind(1, u) + W_scaled %*% x)
      y <- Wout_GA %*% rbind(1, u, x)
      Y_val[, t] <- y
      u <- treino_valida[treino + t + 1]
    }
    
    # Treino
    Y_tr <- matrix(0, outSize, treino)
    u <- treino_valida[1]
    for (j in 1:treino) {
      x <- (1 - a_GA) * x + a_GA * tanh(Win_GA %*% rbind(1, u) + W_scaled %*% x)
      y <- Wout_GA %*% rbind(1, u, x)
      Y_tr[, j] <- y
      u <- treino_valida[j + 1]
    }
    
    real_tr <- treino_valida[2:treino]
    pred_tr <- Y_tr[outSize, 1:(treino - 1)]
    mae_tr <- mean(abs(real_tr - pred_tr))
    
    real_val <- treino_valida[(treino + 2):(treino + valida)]
    pred_val <- Y_val[outSize, 1:(valida - 1)]
    mae_val <- mean(abs(real_val - pred_val))
    
    fitness_val <- (-mae_tr * 0.4 - mae_val * 0.6)
    if (is.na(fitness_val)) fitness_val <- -9999
    
    # Salvar novo melhor estado
    if (fitness_val > melhor_estado$fitness) {
      melhor_estado$fitness <- fitness_val
      melhor_estado$melhor_cromossomo <- cromossoma
      melhor_estado$params <- list(
        a = a_GA, sr = sr_GA, initLen = initLen_GA,
        tam_reservoir = tam_res_GA, reg = reg_GA
      )
      melhor_estado$Win <- Win_GA
      melhor_estado$W <- W_GA
      melhor_estado$Wout <- Wout_GA
      melhor_estado$Y_valida <- as.numeric(Y_val)
      melhor_estado$Y_treino <- as.numeric(Y_tr)
      melhor_estado$iter_sem_melhora <- 0
    }
    
    return(fitness_val)
  }
  
  # 2. Mutação Adaptativa com Suporte a Cataclismo
  mutacao_adaptativa_cataclisma <- function(object, parent) {
    mutate <- parent <- as.vector(object@population[parent, ])
    n_bits <- length(parent)
    
    # Se estagnado e em modo cataclismo: taxa de mutação alta (40%) para exploração global
    p_mut <- if (isTRUE(melhor_estado$modo_cataclismo)) 0.40 else 0.12
    
    for (j in 1:n_bits) {
      if (runif(1) < p_mut) {
        mutate[j] <- 1 - mutate[j]
      }
    }
    return(mutate)
  }
  
  # 3. Monitor de Gerações, Interrupções e Ativador de Cataclismos
  monitor_ga_cataclisma <- function(obj) {
    iter_atual <- obj@iter
    melhor_estado$iter_executadas <- iter_atual
    melhor_estado$iter_sem_melhora <- melhor_estado$iter_sem_melhora + 1
    
    # Processar eventos assíncronos do Shiny e WebSocket (cliques em botões)
    if (requireNamespace("httpuv", quietly = TRUE)) {
      tryCatch(httpuv::service(10), error = function(e) {})
    }
    if (requireNamespace("later", quietly = TRUE)) {
      tryCatch(later::run_now(0.005), error = function(e) {})
    }
    
    # Sincronizar inputs da sessão Shiny em tempo real
    if (!is.null(session)) {
      if (session$isClosed()) {
        cancelar_ga()
      } else {
        cur_cancel <- tryCatch(isolate(session$input$btn_cancelar_execucao), error = function(e) NULL)
        if (!is.null(cur_cancel) && !identical(cur_cancel, initial_cancel_ts)) {
          cancelar_ga()
        }
        
        cur_pause <- tryCatch(isolate(session$input$btn_pausar_execucao), error = function(e) NULL)
        cur_resume <- tryCatch(isolate(session$input$btn_retomar_execucao), error = function(e) NULL)
        if (!is.null(cur_pause) && !identical(cur_pause, initial_pause_ts)) {
          if (is.null(cur_resume) || identical(cur_resume, initial_resume_ts) || (is.numeric(cur_pause) && is.numeric(cur_resume) && cur_pause > cur_resume)) {
            pausar_ga(TRUE)
          }
        }
        if (!is.null(cur_resume) && !identical(cur_resume, initial_resume_ts)) {
          if (is.null(cur_pause) || identical(cur_pause, initial_pause_ts) || (is.numeric(cur_resume) && is.numeric(cur_pause) && cur_resume >= cur_pause)) {
            pausar_ga(FALSE)
          }
        }
      }
    }
    
    # 1. Verificar Cancelamento (Flag em memória ou disco)
    if (isTRUE(.controle_ga$cancelar) || file.exists(.flag_cancelar)) {
      stop("BENCHMARK_CANCELADO_PELO_USUARIO")
    }
    
    # 2. Verificar Pausa (Flag em memória ou disco)
    if (isTRUE(.controle_ga$pausado) || file.exists(.flag_pausar)) {
      pct <- iter_atual / maxiter
      if (is.function(set_progress)) {
        set_progress(pct, sprintf("⏸️ [PAUSADO] Geração %d/%d — Clique em '▶️ Retomar' para continuar.", iter_atual, maxiter))
      }
      while ((isTRUE(.controle_ga$pausado) || file.exists(.flag_pausar)) && (!isTRUE(.controle_ga$cancelar) && !file.exists(.flag_cancelar))) {
        Sys.sleep(0.1)
        if (requireNamespace("httpuv", quietly = TRUE)) {
          tryCatch(httpuv::service(50), error = function(e) {})
        }
        if (requireNamespace("later", quietly = TRUE)) {
          tryCatch(later::run_now(0.01), error = function(e) {})
        }
        if (!is.null(session)) {
          if (session$isClosed()) {
            cancelar_ga()
            break
          }
          cur_cancel <- tryCatch(isolate(session$input$btn_cancelar_execucao), error = function(e) NULL)
          if (!is.null(cur_cancel) && !identical(cur_cancel, initial_cancel_ts)) {
            cancelar_ga()
            break
          }
          cur_resume <- tryCatch(isolate(session$input$btn_retomar_execucao), error = function(e) NULL)
          if (!is.null(cur_resume) && !identical(cur_resume, initial_resume_ts)) {
            pausar_ga(FALSE)
            break
          }
        }
      }
      if (isTRUE(.controle_ga$cancelar) || file.exists(.flag_cancelar)) {
        stop("BENCHMARK_CANCELADO_PELO_USUARIO")
      }
    }
    
    # Detecção de Estagnação -> Ativar Cataclismo
    if (anti_estagnacao && melhor_estado$iter_sem_melhora >= limite_estagnacao) {
      melhor_estado$total_cataclismos <- melhor_estado$total_cataclismos + 1
      melhor_estado$modo_cataclismo <- TRUE
      melhor_estado$iter_sem_melhora <- 0
      
      msg_extra <- sprintf("💥 [Cataclismo #%d] Saltando mínimos locais!", melhor_estado$total_cataclismos)
    } else {
      melhor_estado$modo_cataclismo <- FALSE
      msg_extra <- if (melhor_estado$total_cataclismos > 0) sprintf("(Cataclismos: %d)", melhor_estado$total_cataclismos) else ""
    }
    
    if (is.function(set_progress)) {
      pct <- iter_atual / maxiter
      msg <- sprintf("Geração %d/%d (%.0f%%) — Melhor Fitness: %.4f %s", iter_atual, maxiter, pct * 100, melhor_estado$fitness, msg_extra)
      set_progress(pct, msg)
    }
  }
  
  # 4. Inicializador por Hipercubo Latino (LHS)
  populacao_inicial_lhs <- function(object) {
    gerar_populacao_lhs(pop_size = object@popSize, nbits = object@nBits)
  }
  
  # 5. Execução do GA
  if (is.function(set_progress)) set_progress(0.02, "Iniciando Algoritmo Genético (LHS + Cataclismo)...")
  t_inicio <- proc.time()
  
  cancelado_usuario <- FALSE
  alg_gen <- NULL
  
  tryCatch({
    alg_gen <- ga(
      type = "binary",
      fitness = fitness_func,
      nBits = 55,
      popSize = pop_size,
      population = populacao_inicial_lhs,
      selection = gabin_tourSelection,
      crossover = gabin_spCrossover,
      mutation = mutacao_adaptativa_cataclisma,
      pcrossover = 0.85,
      elitism = max(1, round(pop_size * 0.1)),
      maxiter = maxiter,
      run = run_stop,
      keepBest = TRUE,
      monitor = monitor_ga_cataclisma,
      parallel = FALSE
    )
  }, error = function(e) {
    if (grepl("BENCHMARK_CANCELADO_PELO_USUARIO", e$message)) {
      cancelado_usuario <<- TRUE
    } else {
      stop(e)
    }
  })
  
  t_fim <- proc.time()
  tempo_exec <- (t_fim - t_inicio)["elapsed"]
  
  # Fallback de segurança se cancelado antes de qualquer indivíduo ser avaliado
  if (is.null(melhor_estado$params)) {
    if (!is.null(alg_gen) && !is.null(alg_gen@solution)) {
      solucao_bits <- alg_gen@solution[1, ]
      fitness_func(solucao_bits)
    } else {
      pop_init <- gerar_populacao_lhs(pop_size = pop_size, nbits = 55)
      fitness_func(pop_init[1, ])
    }
  }
  
  params_opt <- melhor_estado$params
  Win_opt <- melhor_estado$Win
  W_opt <- melhor_estado$W
  Wout_opt <- melhor_estado$Wout
  
  # 6. Avaliação na Validação
  if (is.function(set_progress)) set_progress(0.80, "Avaliando parâmetros ótimos na Validação...")
  res_valida <- esn_validacao(dados_split, params_opt, Win_opt, W_opt, Wout_opt)
  
  # 7. Avaliação no Teste Out-of-Sample (Blind Test)
  if (is.function(set_progress)) set_progress(0.90, "Avaliando desempenho no Teste Out-of-Sample...")
  res_teste <- esn_teste(dados_split, params_opt, Win_opt, W_opt, Wout_opt)
  
  # 8. Registro Persistente no CSV Histórico e Verificação de Recorde
  if (is.function(set_progress)) set_progress(0.95, "Gravando histórico no CSV e verificando recordes...")
  gen_registradas <- if (isTRUE(cancelado_usuario)) paste0(melhor_estado$iter_executadas, " (Cancelado)") else maxiter
  
  registro_info <- registrar_execucao_ga(
    params = params_opt,
    metricas_valida = res_valida$metricas_valida,
    metricas_teste = res_teste$metricas_teste,
    fitness = melhor_estado$fitness,
    geracoes = gen_registradas,
    pop_size = pop_size,
    dist_win = win_dist,
    dist_w = w_dist,
    tempo_s = tempo_exec,
    Win = Win_opt,
    W = W_opt,
    Wout = Wout_opt
  )
  
  list(
    modelo = "ESN",
    origem = "GA_LIVE_LHS_CATACLYSM",
    cancelado = cancelado_usuario,
    iter_executadas = melhor_estado$iter_executadas,
    params = params_opt,
    dist_win = win_dist,
    dist_w = w_dist,
    Win = Win_opt,
    W = W_opt,
    Wout = Wout_opt,
    validacao = res_valida,
    teste = res_teste,
    fitness = melhor_estado$fitness,
    total_cataclismos = melhor_estado$total_cataclismos,
    tempo = tempo_exec,
    ga_object = alg_gen,
    registro = registro_info,
    metricas = list(
      modelo = "ESN",
      treino = res_valida$metricas_treino,
      validacao = res_valida$metricas_valida,
      teste = res_teste$metricas_teste,
      tempo = tempo_exec
    )
  )
}
