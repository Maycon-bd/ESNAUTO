# =============================================================================
# mod_lstm.R — Módulo LSTM (Long Short-Term Memory) para Shiny
# Usa keras3/tensorflow para treinar e prever
# =============================================================================

source("utils/data_prep.R", local = TRUE)
source("utils/metrics.R", local = TRUE)

# =============================================================================
# UI SHINY DO MÓDULO LSTM
# =============================================================================

lstm_ui <- function(id) {
  ns <- NS(id)
  
  tagList(
    fluidRow(
      column(4,
        div(class = "well model-card-lstm",
          div(class = "section-subtitle", "HIPERPARÂMETROS DEEP LEARNING"),
          h4(style = "margin-top:0; color: var(--lstm-color); font-weight: 800;", "📈 LSTM Architecture"),
          hr(),
          
          sliderInput(ns("units"), "Neurônios (Units - 1ª camada):", 
                      min = 10, max = 200, value = 50, step = 10),
          sliderInput(ns("timesteps"), "Janela Temporal (Timesteps):", 
                      min = 5, max = 60, value = 10, step = 5),
          sliderInput(ns("dropout"), "Taxa de Dropout:", 
                      min = 0.0, max = 0.5, value = 0.2, step = 0.05),
          sliderInput(ns("epochs"), "Épocas de Treinamento:", 
                      min = 10, max = 300, value = 50, step = 10),
          
          fluidRow(
            column(6,
              selectInput(ns("batch_size"), "Batch Size:", choices = c(8, 16, 32, 64), selected = 16)
            ),
            column(6,
              selectInput(ns("optimizer"), "Otimizador:", choices = c("adam", "rmsprop", "sgd"), selected = "adam")
            )
          ),
          
          checkboxInput(ns("segunda_camada"), "Adicionar 2ª Camada Recorrente", value = FALSE),
          conditionalPanel(
            condition = paste0("input['", ns("segunda_camada"), "']"),
            sliderInput(ns("units2"), "Neurônios (Units - 2ª camada):", min = 10, max = 100, value = 25, step = 5)
          ),
          
          hr(),
          actionButton(ns("btn_rodar"), "🚀 Treinar Modelo LSTM", 
                       class = "btn-primary btn-block",
                       style = "width:100%; height: 46px;")
        )
      ),
      column(8,
        div(class = "well",
          tabsetPanel(
            tabPanel("📊 Métricas de Desempenho",
              br(),
              verbatimTextOutput(ns("resultados_texto")),
              hr(),
              h5(style = "font-weight: 700;", "📋 Tabela de Resumo:"),
              tableOutput(ns("tabela_metricas"))
            ),
            tabPanel("📈 Validação (In-sample)",
              br(),
              plotOutput(ns("grafico_validacao"), height = "380px")
            ),
            tabPanel("📉 Teste (Out-of-sample)",
              br(),
              plotOutput(ns("grafico_teste"), height = "380px")
            ),
            tabPanel("📉 Curva de Perda (Loss)",
              br(),
              plotOutput(ns("grafico_loss"), height = "380px")
            )
          )
        )
      )
    )
  )
}

# =============================================================================
# SERVER SHINY DO MÓDULO LSTM
# =============================================================================

lstm_server <- function(id, dados_reativo) {
  moduleServer(id, function(input, output, session) {
    ns <- session$ns
    
    resultados <- reactiveValues(
      validacao = NULL,
      teste = NULL,
      metricas = NULL,
      historico = NULL
    )
    
    observeEvent(input$btn_rodar, {
      req(dados_reativo())
      
      # Verificar se keras3 está disponível
      if (!requireNamespace("keras3", quietly = TRUE)) {
        showNotification("❌ Pacote 'keras3' não instalado. Instale com install.packages('keras3') e keras3::install_keras()", 
                         type = "error", duration = 10)
        return()
      }
      
      library(keras3)
      
      withProgress(message = "Treinando LSTM...", value = 0, {
        dados <- dados_reativo()
        timesteps <- input$timesteps
        batch_size <- as.integer(input$batch_size)
        
        # =============================================
        # Preparar dados para LSTM
        # =============================================
        setProgress(0.1, detail = "Preparando dados...")
        
        treino_n <- 2600
        valida_n <- 1299
        teste_n <- 1299
        
        # Normalizar usando apenas treino
        treino_raw <- dados[1:treino_n]
        min_val <- min(treino_raw)
        max_val <- max(treino_raw)
        
        dados_norm <- (dados - min_val) / (max_val - min_val)
        
        # --- Dados de Treino + Validação ---
        treino_valida_norm <- dados_norm[1:(treino_n + valida_n)]
        
        n_tv <- length(treino_valida_norm)
        n_janelas_tv <- n_tv - timesteps
        
        X_tv <- array(0, dim = c(n_janelas_tv, timesteps, 1))
        y_tv <- numeric(n_janelas_tv)
        for (i in 1:n_janelas_tv) {
          X_tv[i, , 1] <- treino_valida_norm[i:(i + timesteps - 1)]
          y_tv[i] <- treino_valida_norm[i + timesteps]
        }
        
        # Separar treino e validação
        n_treino_j <- treino_n - timesteps
        
        X_treino <- X_tv[1:n_treino_j, , , drop = FALSE]
        y_treino <- y_tv[1:n_treino_j]
        
        X_valida <- X_tv[(n_treino_j + 1):n_janelas_tv, , , drop = FALSE]
        y_valida <- y_tv[(n_treino_j + 1):n_janelas_tv]
        
        # --- Dados de Treino + Teste (pulando validação) ---
        treina_testa_norm <- c(dados_norm[1:treino_n], 
                               dados_norm[(treino_n + valida_n + 1):(treino_n + valida_n + teste_n)])
        n_tt <- length(treina_testa_norm)
        n_janelas_tt <- n_tt - timesteps
        
        X_tt <- array(0, dim = c(n_janelas_tt, timesteps, 1))
        y_tt <- numeric(n_janelas_tt)
        for (i in 1:n_janelas_tt) {
          X_tt[i, , 1] <- treina_testa_norm[i:(i + timesteps - 1)]
          y_tt[i] <- treina_testa_norm[i + timesteps]
        }
        
        # Janelas de teste começam após treino
        idx_teste_inicio <- n_treino_j + 1
        X_teste <- X_tt[idx_teste_inicio:n_janelas_tt, , , drop = FALSE]
        y_teste <- y_tt[idx_teste_inicio:n_janelas_tt]
        
        # =============================================
        # Construir modelo LSTM
        # =============================================
        setProgress(0.2, detail = "Construindo modelo...")
        
        model <- keras_model_sequential()
        
        if (input$segunda_camada) {
          model %>%
            layer_lstm(units = input$units, input_shape = c(timesteps, 1),
                       return_sequences = TRUE) %>%
            layer_dropout(rate = input$dropout) %>%
            layer_lstm(units = input$units2, return_sequences = FALSE) %>%
            layer_dropout(rate = input$dropout) %>%
            layer_dense(units = 1)
        } else {
          model %>%
            layer_lstm(units = input$units, input_shape = c(timesteps, 1),
                       return_sequences = FALSE) %>%
            layer_dropout(rate = input$dropout) %>%
            layer_dense(units = 1)
        }
        
        model %>% compile(
          loss = 'mean_squared_error',
          optimizer = input$optimizer
        )
        
        # =============================================
        # Treinar
        # =============================================
        setProgress(0.3, detail = "Treinando (pode demorar)...")
        
        t_inicio <- proc.time()
        
        historico <- model %>% fit(
          X_treino, y_treino,
          epochs = input$epochs,
          batch_size = batch_size,
          validation_data = list(X_valida, y_valida),
          verbose = 0
        )
        
        t_fim <- proc.time()
        tempo_total <- (t_fim - t_inicio)["elapsed"]
        
        # =============================================
        # Previsões
        # =============================================
        setProgress(0.8, detail = "Gerando previsões...")
        
        # Validação
        pred_valida_norm <- as.numeric(predict(model, X_valida, verbose = 0))
        pred_valida <- pred_valida_norm * (max_val - min_val) + min_val
        real_valida <- y_valida * (max_val - min_val) + min_val
        
        # Teste
        pred_teste_norm <- as.numeric(predict(model, X_teste, verbose = 0))
        pred_teste <- pred_teste_norm * (max_val - min_val) + min_val
        real_teste <- y_teste * (max_val - min_val) + min_val
        
        # Métricas
        metricas_valida <- calcular_todas_metricas(real_valida, pred_valida, tempo_total)
        metricas_teste <- calcular_todas_metricas(real_teste, pred_teste, tempo_total)
        
        setProgress(0.95, detail = "Finalizando...")
        
        resultados$validacao <- list(
          real = real_valida,
          previsto = pred_valida,
          metricas = metricas_valida
        )
        resultados$teste <- list(
          real = real_teste,
          previsto = pred_teste,
          metricas = metricas_teste
        )
        resultados$historico <- historico
        resultados$tempo <- tempo_total
        resultados$metricas <- list(
          modelo = "LSTM",
          validacao = metricas_valida,
          teste = metricas_teste,
          tempo = tempo_total
        )
      })
      
      showNotification("✅ LSTM treinado com sucesso!", type = "message")
    })
    
    # --- Saídas ---
    output$resultados_texto <- renderPrint({
      req(resultados$validacao)
      cat("========== RESULTADOS LSTM ==========\n\n")
      cat("--- Métricas Validação ---\n")
      cat(sprintf("  MAE:  %.6f\n", resultados$validacao$metricas$MAE))
      cat(sprintf("  RMSE: %.6f\n", resultados$validacao$metricas$RMSE))
      cat(sprintf("  MAPE: %.4f%%\n", resultados$validacao$metricas$MAPE))
      cat(sprintf("  R²:   %.6f\n", resultados$validacao$metricas$R2))
      cat(sprintf("\n--- Métricas Teste ---\n"))
      cat(sprintf("  MAE:  %.6f\n", resultados$teste$metricas$MAE))
      cat(sprintf("  RMSE: %.6f\n", resultados$teste$metricas$RMSE))
      cat(sprintf("  MAPE: %.4f%%\n", resultados$teste$metricas$MAPE))
      cat(sprintf("  R²:   %.6f\n", resultados$teste$metricas$R2))
      cat(sprintf("\n  Tempo total: %.2f s\n", resultados$tempo))
    })
    
    output$tabela_metricas <- renderTable({
      req(resultados$validacao)
      rbind(
        data.frame(Fase = "Validação", resultados$validacao$metricas),
        data.frame(Fase = "Teste", resultados$teste$metricas)
      )
    }, digits = 6)
    
    output$grafico_validacao <- renderPlot({
      req(resultados$validacao)
      real <- resultados$validacao$real
      prev <- resultados$validacao$previsto
      
      par(mar = c(3.5, 4, 2, 1), bg = "transparent")
      plot(real, type = 'l', col = '#0f172a', lwd = 2,
           ylab = "Preço PETR4 (R$)", xlab = "Dias",
           main = "LSTM — Previsão na Fase de Validação", axes = FALSE, col.main = "#0f172a")
      axis(1, col = "#cbd5e1", col.axis = "#475569")
      axis(2, col = "#cbd5e1", col.axis = "#475569")
      grid(col = "#e2e8f0", lty = "dotted")
      
      lines(prev, col = '#2563eb', lwd = 1.8)
      legend('topright', legend = c('Série Real', 'LSTM Previsto'),
             col = c('#0f172a', '#2563eb'), lty = 1, lwd = c(2, 1.8), bty = 'n', text.col = '#0f172a')
    })
    
    output$grafico_teste <- renderPlot({
      req(resultados$teste)
      real <- resultados$teste$real
      prev <- resultados$teste$previsto
      
      par(mar = c(3.5, 4, 2, 1), bg = "transparent")
      plot(real, type = 'l', col = '#0f172a', lwd = 2,
           ylab = "Preço PETR4 (R$)", xlab = "Dias",
           main = "LSTM — Previsão na Fase de Teste", axes = FALSE, col.main = "#0f172a")
      axis(1, col = "#cbd5e1", col.axis = "#475569")
      axis(2, col = "#cbd5e1", col.axis = "#475569")
      grid(col = "#e2e8f0", lty = "dotted")
      
      lines(prev, col = '#2563eb', lwd = 1.8)
      legend('topright', legend = c('Série Real', 'LSTM Previsto'),
             col = c('#0f172a', '#2563eb'), lty = 1, lwd = c(2, 1.8), bty = 'n', text.col = '#0f172a')
    })
    
    output$grafico_loss <- renderPlot({
      req(resultados$historico)
      par(mar = c(3.5, 4, 2, 1), bg = "transparent")
      plot(resultados$historico)
    })
    
    # Retornar métricas para comparação
    reactive(resultados$metricas)
  })
}
