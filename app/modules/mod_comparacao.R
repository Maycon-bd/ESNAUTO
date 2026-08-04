# =============================================================================
# mod_comparacao.R — Módulo de Comparação ESN vs LSTM vs GRU
# =============================================================================

source("utils/metrics.R", local = TRUE)

# =============================================================================
# UI
# =============================================================================

comparacao_ui <- function(id) {
  ns <- NS(id)
  
  tagList(
    fluidRow(
      column(12,
        h3("⚖️ Comparação de Modelos", style = "text-align: center; margin-bottom: 20px;"),
        
        # Cards de resumo no topo
        fluidRow(
          column(4,
            wellPanel(
              style = "background: linear-gradient(135deg, #e74c3c22, #e74c3c11); border-left: 4px solid #e74c3c;",
              h4("🧠 ESN", style = "color: #e74c3c;"),
              uiOutput(ns("card_esn"))
            )
          ),
          column(4,
            wellPanel(
              style = "background: linear-gradient(135deg, #3498db22, #3498db11); border-left: 4px solid #3498db;",
              h4("📈 LSTM", style = "color: #3498db;"),
              uiOutput(ns("card_lstm"))
            )
          ),
          column(4,
            wellPanel(
              style = "background: linear-gradient(135deg, #9b59b622, #9b59b611); border-left: 4px solid #9b59b6;",
              h4("📉 GRU", style = "color: #9b59b6;"),
              uiOutput(ns("card_gru"))
            )
          )
        ),
        
        hr(),
        
        # Tabela comparativa
        h4("📋 Tabela Comparativa — Validação"),
        tableOutput(ns("tabela_validacao")),
        
        h4("📋 Tabela Comparativa — Teste"),
        tableOutput(ns("tabela_teste")),
        
        hr(),
        
        # Gráficos
        fluidRow(
          column(6,
            h4("📊 Comparação de Métricas (Teste)", style = "text-align: center;"),
            plotOutput(ns("grafico_barras"), height = "400px")
          ),
          column(6,
            h4("⏱️ Tempo de Execução", style = "text-align: center;"),
            plotOutput(ns("grafico_tempo"), height = "400px")
          )
        ),
        
        hr(),
        
        h4("🏆 Conclusão"),
        wellPanel(
          style = "background: #f8f9fa; border: 2px solid #27ae60;",
          uiOutput(ns("conclusao"))
        )
      )
    )
  )
}

# =============================================================================
# SERVER
# =============================================================================

comparacao_server <- function(id, metricas_esn, metricas_lstm, metricas_gru) {
  moduleServer(id, function(input, output, session) {
    ns <- session$ns
    
    # --- Cards de resumo ---
    output$card_esn <- renderUI({
      m <- metricas_esn()
      if (is.null(m)) return(tags$p("Ainda não executado", style = "color: gray;"))
      tagList(
        tags$p(sprintf("MAE Teste: %.4f", m$teste$MAE), style = "font-weight: bold;"),
        tags$p(sprintf("RMSE Teste: %.4f", m$teste$RMSE)),
        tags$p(sprintf("Tempo: %.2f s", m$tempo), style = "color: #666;")
      )
    })
    
    output$card_lstm <- renderUI({
      m <- metricas_lstm()
      if (is.null(m)) return(tags$p("Ainda não executado", style = "color: gray;"))
      tagList(
        tags$p(sprintf("MAE Teste: %.4f", m$teste$MAE), style = "font-weight: bold;"),
        tags$p(sprintf("RMSE Teste: %.4f", m$teste$RMSE)),
        tags$p(sprintf("Tempo: %.2f s", m$tempo), style = "color: #666;")
      )
    })
    
    output$card_gru <- renderUI({
      m <- metricas_gru()
      if (is.null(m)) return(tags$p("Ainda não executado", style = "color: gray;"))
      tagList(
        tags$p(sprintf("MAE Teste: %.4f", m$teste$MAE), style = "font-weight: bold;"),
        tags$p(sprintf("RMSE Teste: %.4f", m$teste$RMSE)),
        tags$p(sprintf("Tempo: %.2f s", m$tempo), style = "color: #666;")
      )
    })
    
    # --- Tabela Validação ---
    output$tabela_validacao <- renderTable({
      modelos <- list(
        ESN  = metricas_esn(),
        LSTM = metricas_lstm(),
        GRU  = metricas_gru()
      )
      
      # Filtrar modelos que já foram executados
      modelos <- modelos[!sapply(modelos, is.null)]
      if (length(modelos) == 0) return(data.frame(Mensagem = "Execute pelo menos um modelo primeiro."))
      
      do.call(rbind, lapply(names(modelos), function(nome) {
        m <- modelos[[nome]]
        data.frame(
          Modelo = nome,
          MAE    = m$validacao$MAE,
          RMSE   = m$validacao$RMSE,
          MAPE   = m$validacao$MAPE,
          R2     = m$validacao$R2,
          Tempo_s = m$tempo,
          stringsAsFactors = FALSE
        )
      }))
    }, digits = 6)
    
    # --- Tabela Teste ---
    output$tabela_teste <- renderTable({
      modelos <- list(
        ESN  = metricas_esn(),
        LSTM = metricas_lstm(),
        GRU  = metricas_gru()
      )
      
      modelos <- modelos[!sapply(modelos, is.null)]
      if (length(modelos) == 0) return(data.frame(Mensagem = "Execute pelo menos um modelo primeiro."))
      
      do.call(rbind, lapply(names(modelos), function(nome) {
        m <- modelos[[nome]]
        data.frame(
          Modelo = nome,
          MAE    = m$teste$MAE,
          RMSE   = m$teste$RMSE,
          MAPE   = m$teste$MAPE,
          R2     = m$teste$R2,
          Tempo_s = m$tempo,
          stringsAsFactors = FALSE
        )
      }))
    }, digits = 6)
    
    # --- Gráfico de barras comparativo ---
    output$grafico_barras <- renderPlot({
      modelos <- list(
        ESN  = metricas_esn(),
        LSTM = metricas_lstm(),
        GRU  = metricas_gru()
      )
      modelos <- modelos[!sapply(modelos, is.null)]
      if (length(modelos) < 2) {
        plot.new()
        text(0.5, 0.5, "Execute pelo menos 2 modelos\npara comparar", cex = 1.5, col = "gray")
        return()
      }
      
      nomes <- names(modelos)
      cores <- c(ESN = "#e74c3c", LSTM = "#3498db", GRU = "#9b59b6")
      
      mae_vals  <- sapply(modelos, function(m) m$teste$MAE)
      rmse_vals <- sapply(modelos, function(m) m$teste$RMSE)
      
      par(mfrow = c(1, 2), mar = c(5, 4, 3, 1))
      
      # MAE
      bp1 <- barplot(mae_vals, col = cores[nomes], main = "MAE (Teste)",
                     ylab = "MAE", border = NA, ylim = c(0, max(mae_vals) * 1.2))
      text(bp1, mae_vals, labels = round(mae_vals, 4), pos = 3, cex = 0.9)
      
      # RMSE
      bp2 <- barplot(rmse_vals, col = cores[nomes], main = "RMSE (Teste)",
                     ylab = "RMSE", border = NA, ylim = c(0, max(rmse_vals) * 1.2))
      text(bp2, rmse_vals, labels = round(rmse_vals, 4), pos = 3, cex = 0.9)
    })
    
    # --- Gráfico de tempo ---
    output$grafico_tempo <- renderPlot({
      modelos <- list(
        ESN  = metricas_esn(),
        LSTM = metricas_lstm(),
        GRU  = metricas_gru()
      )
      modelos <- modelos[!sapply(modelos, is.null)]
      if (length(modelos) < 2) {
        plot.new()
        text(0.5, 0.5, "Execute pelo menos 2 modelos\npara comparar", cex = 1.5, col = "gray")
        return()
      }
      
      nomes <- names(modelos)
      cores <- c(ESN = "#e74c3c", LSTM = "#3498db", GRU = "#9b59b6")
      tempos <- sapply(modelos, function(m) m$tempo)
      
      bp <- barplot(tempos, col = cores[nomes], main = "Tempo de Execução (s)",
                    ylab = "Segundos", border = NA, ylim = c(0, max(tempos) * 1.3))
      text(bp, tempos, labels = paste0(round(tempos, 2), "s"), pos = 3, cex = 1)
      
      # Mostrar razão se ESN existir
      if ("ESN" %in% nomes && tempos["ESN"] > 0) {
        razoes <- tempos / tempos["ESN"]
        mtext(paste0(nomes, ": ", round(razoes, 1), "x"), side = 1, line = 2.5, 
              at = bp, cex = 0.85, col = cores[nomes])
      }
    })
    
    # --- Conclusão automática ---
    output$conclusao <- renderUI({
      modelos <- list(
        ESN  = metricas_esn(),
        LSTM = metricas_lstm(),
        GRU  = metricas_gru()
      )
      modelos <- modelos[!sapply(modelos, is.null)]
      
      if (length(modelos) < 2) {
        return(tags$p("Execute pelo menos 2 modelos para gerar a comparação.", style = "color: gray;"))
      }
      
      nomes <- names(modelos)
      mae_teste <- sapply(modelos, function(m) m$teste$MAE)
      tempos <- sapply(modelos, function(m) m$tempo)
      
      melhor_mae <- names(which.min(mae_teste))
      melhor_tempo <- names(which.min(tempos))
      
      tagList(
        tags$p(
          tags$strong("Melhor MAE (Teste): "), 
          tags$span(melhor_mae, style = paste0("color: ", c(ESN="#e74c3c", LSTM="#3498db", GRU="#9b59b6")[melhor_mae], "; font-weight: bold;")),
          sprintf(" (%.6f)", mae_teste[melhor_mae])
        ),
        tags$p(
          tags$strong("Mais rápido: "),
          tags$span(melhor_tempo, style = paste0("color: ", c(ESN="#e74c3c", LSTM="#3498db", GRU="#9b59b6")[melhor_tempo], "; font-weight: bold;")),
          sprintf(" (%.4f s)", tempos[melhor_tempo])
        ),
        if ("ESN" %in% nomes) {
          # Análise custo-benefício
          razao_mae_lstm <- if ("LSTM" %in% nomes) mae_teste["ESN"] / mae_teste["LSTM"] else NA
          razao_mae_gru  <- if ("GRU" %in% nomes)  mae_teste["ESN"] / mae_teste["GRU"] else NA
          razao_tempo_lstm <- if ("LSTM" %in% nomes) tempos["LSTM"] / tempos["ESN"] else NA
          razao_tempo_gru  <- if ("GRU" %in% nomes)  tempos["GRU"] / tempos["ESN"] else NA
          
          analise <- tags$div(
            tags$hr(),
            tags$h5("📐 Análise Custo-Benefício (ESN como referência):"),
            if (!is.na(razao_mae_lstm)) {
              esn_melhor <- mae_teste["ESN"] <= mae_teste["LSTM"]
              tags$p(
                sprintf("ESN vs LSTM: MAE ratio = %.3f | LSTM é %.1fx mais lento", 
                        razao_mae_lstm, razao_tempo_lstm),
                if (esn_melhor) tags$span(" ✅ ESN igual ou melhor!", style = "color: #27ae60; font-weight: bold;")
                else tags$span(sprintf(" ⚠️ LSTM %.1f%% melhor em MAE", (1 - razao_mae_lstm) * 100), style = "color: #e67e22;")
              )
            },
            if (!is.na(razao_mae_gru)) {
              esn_melhor <- mae_teste["ESN"] <= mae_teste["GRU"]
              tags$p(
                sprintf("ESN vs GRU:  MAE ratio = %.3f | GRU é %.1fx mais lento", 
                        razao_mae_gru, razao_tempo_gru),
                if (esn_melhor) tags$span(" ✅ ESN igual ou melhor!", style = "color: #27ae60; font-weight: bold;")
                else tags$span(sprintf(" ⚠️ GRU %.1f%% melhor em MAE", (1 - razao_mae_gru) * 100), style = "color: #e67e22;")
              )
            }
          )
          analise
        }
      )
    })
    
  })
}
