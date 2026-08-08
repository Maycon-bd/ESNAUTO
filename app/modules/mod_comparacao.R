# =============================================================================
# mod_comparacao.R — Módulo de Comparação ESN vs LSTM vs GRU (UI/UX Redesign)
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
        div(class = "section-subtitle", "BENCHMARK DE MODELOS"),
        h3(class = "section-title", "⚖️ Comparação de Desempenho & Custo-Benefício"),
        p(style = "color: var(--text-muted); margin-bottom: 24px;",
          "Esta aba consolida as métricas dos modelos executados para provar a hipótese de eficiência computacional da ESN."),
        
        # Summary Model Cards Top Row
        fluidRow(
          column(4,
            div(class = "well model-card-esn",
              div(style = "display: flex; justify-space-between; align-items: center; margin-bottom: 12px;",
                h4(style = "margin: 0; color: var(--esn-color); font-weight: 800;", "🧠 ESN (Reservoir)"),
                span(class = "badge-tag badge-esn", "Echo State")
              ),
              uiOutput(ns("card_esn"))
            )
          ),
          column(4,
            div(class = "well model-card-lstm",
              div(style = "display: flex; justify-space-between; align-items: center; margin-bottom: 12px;",
                h4(style = "margin: 0; color: var(--lstm-color); font-weight: 800;", "📈 LSTM Network"),
                span(class = "badge-tag badge-lstm", "Deep Recurrent")
              ),
              uiOutput(ns("card_lstm"))
            )
          ),
          column(4,
            div(class = "well model-card-gru",
              div(style = "display: flex; justify-space-between; align-items: center; margin-bottom: 12px;",
                h4(style = "margin: 0; color: var(--gru-color); font-weight: 800;", "📉 GRU Network"),
                span(class = "badge-tag badge-gru", "Gated Recurrent")
              ),
              uiOutput(ns("card_gru"))
            )
          )
        ),
        
        hr(),
        
        # Tables
        fluidRow(
          column(6,
            div(class = "well",
              h4(style = "margin-top:0;", "📋 Métricas na Fase de Validação"),
              tableOutput(ns("tabela_validacao"))
            )
          ),
          column(6,
            div(class = "well",
              h4(style = "margin-top:0;", "🎯 Métricas na Fase de Teste (Out-of-sample)"),
              tableOutput(ns("tabela_teste"))
            )
          )
        ),
        
        hr(),
        
        # Plots
        fluidRow(
          column(6,
            div(class = "well",
              h4(style = "margin-top:0; text-align: center;", "📊 Erro Médio Absoluto (MAE & RMSE no Teste)"),
              plotOutput(ns("grafico_barras"), height = "360px")
            )
          ),
          column(6,
            div(class = "well",
              h4(style = "margin-top:0; text-align: center;", "⏱️ Tempo Total de Treinamento (Segundos)"),
              plotOutput(ns("grafico_tempo"), height = "360px")
            )
          )
        ),
        
        hr(),
        
        div(class = "well", style = "border-left: 6px solid #059669; background: #f0fdf4;",
          h4(style = "margin-top:0; color: #047857;", "🏆 Análise de Custo-Benefício Computacional"),
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
    
    # Cards de resumo
    output$card_esn <- renderUI({
      m <- metricas_esn()
      if (is.null(m)) {
        return(div(style = "color: var(--text-muted); font-size: 0.9rem; padding: 10px 0;", "⏳ Modelo ainda não foi executado. Vá na aba ESN e clique em Rodar."))
      }
      tagList(
        div(style = "margin-bottom: 6px;",
          span(style = "font-size: 0.8rem; color: var(--text-muted); text-transform: uppercase; font-weight: 700;", "MAE Teste: "),
          span(style = "font-family: var(--font-mono); font-size: 1.2rem; font-weight: 700; color: var(--esn-color);", sprintf("%.4f", m$teste$MAE))
        ),
        div(style = "margin-bottom: 6px;",
          span(style = "font-size: 0.8rem; color: var(--text-muted); text-transform: uppercase; font-weight: 700;", "RMSE Teste: "),
          span(style = "font-family: var(--font-mono); font-size: 1rem; font-weight: 600;", sprintf("%.4f", m$teste$RMSE))
        ),
        div(style = "margin-top: 10px; padding-top: 8px; border-top: 1px solid var(--border-color); font-size: 0.85rem; color: var(--text-secondary);",
          sprintf("⏱️ Tempo de treino: %.3f seg", m$tempo)
        )
      )
    })
    
    output$card_lstm <- renderUI({
      m <- metricas_lstm()
      if (is.null(m)) {
        return(div(style = "color: var(--text-muted); font-size: 0.9rem; padding: 10px 0;", "⏳ Modelo ainda não foi executado. Vá na aba LSTM e clique em Treinar."))
      }
      tagList(
        div(style = "margin-bottom: 6px;",
          span(style = "font-size: 0.8rem; color: var(--text-muted); text-transform: uppercase; font-weight: 700;", "MAE Teste: "),
          span(style = "font-family: var(--font-mono); font-size: 1.2rem; font-weight: 700; color: var(--lstm-color);", sprintf("%.4f", m$teste$MAE))
        ),
        div(style = "margin-bottom: 6px;",
          span(style = "font-size: 0.8rem; color: var(--text-muted); text-transform: uppercase; font-weight: 700;", "RMSE Teste: "),
          span(style = "font-family: var(--font-mono); font-size: 1rem; font-weight: 600;", sprintf("%.4f", m$teste$RMSE))
        ),
        div(style = "margin-top: 10px; padding-top: 8px; border-top: 1px solid var(--border-color); font-size: 0.85rem; color: var(--text-secondary);",
          sprintf("⏱️ Tempo de treino: %.2f seg", m$tempo)
        )
      )
    })
    
    output$card_gru <- renderUI({
      m <- metricas_gru()
      if (is.null(m)) {
        return(div(style = "color: var(--text-muted); font-size: 0.9rem; padding: 10px 0;", "⏳ Modelo ainda não foi executado. Vá na aba GRU e clique em Treinar."))
      }
      tagList(
        div(style = "margin-bottom: 6px;",
          span(style = "font-size: 0.8rem; color: var(--text-muted); text-transform: uppercase; font-weight: 700;", "MAE Teste: "),
          span(style = "font-family: var(--font-mono); font-size: 1.2rem; font-weight: 700; color: var(--gru-color);", sprintf("%.4f", m$teste$MAE))
        ),
        div(style = "margin-bottom: 6px;",
          span(style = "font-size: 0.8rem; color: var(--text-muted); text-transform: uppercase; font-weight: 700;", "RMSE Teste: "),
          span(style = "font-family: var(--font-mono); font-size: 1rem; font-weight: 600;", sprintf("%.4f", m$teste$RMSE))
        ),
        div(style = "margin-top: 10px; padding-top: 8px; border-top: 1px solid var(--border-color); font-size: 0.85rem; color: var(--text-secondary);",
          sprintf("⏱️ Tempo de treino: %.2f seg", m$tempo)
        )
      )
    })
    
    # Tabela Validação
    output$tabela_validacao <- renderTable({
      modelos <- list(
        ESN  = metricas_esn(),
        LSTM = metricas_lstm(),
        GRU  = metricas_gru()
      )
      modelos <- modelos[!sapply(modelos, is.null)]
      if (length(modelos) == 0) return(data.frame(Status = "Nenhum modelo foi executado ainda."))
      
      do.call(rbind, lapply(names(modelos), function(nome) {
        m <- modelos[[nome]]
        data.frame(
          "Modelo" = nome,
          "MAE"    = sprintf("%.6f", m$validacao$MAE),
          "RMSE"   = sprintf("%.6f", m$validacao$RMSE),
          "MAPE %" = sprintf("%.2f%%", m$validacao$MAPE),
          "R²"     = sprintf("%.4f", m$validacao$R2),
          "Tempo (s)" = sprintf("%.3f", m$tempo),
          check.names = FALSE,
          stringsAsFactors = FALSE
        )
      }))
    })
    
    # Tabela Teste
    output$tabela_teste <- renderTable({
      modelos <- list(
        ESN  = metricas_esn(),
        LSTM = metricas_lstm(),
        GRU  = metricas_gru()
      )
      modelos <- modelos[!sapply(modelos, is.null)]
      if (length(modelos) == 0) return(data.frame(Status = "Nenhum modelo foi executado ainda."))
      
      do.call(rbind, lapply(names(modelos), function(nome) {
        m <- modelos[[nome]]
        data.frame(
          "Modelo" = nome,
          "MAE"    = sprintf("%.6f", m$teste$MAE),
          "RMSE"   = sprintf("%.6f", m$teste$RMSE),
          "MAPE %" = sprintf("%.2f%%", m$teste$MAPE),
          "R²"     = sprintf("%.4f", m$teste$R2),
          "Tempo (s)" = sprintf("%.3f", m$tempo),
          check.names = FALSE,
          stringsAsFactors = FALSE
        )
      }))
    })
    
    # Gráfico de barras (MAE & RMSE)
    output$grafico_barras <- renderPlot({
      modelos <- list(
        ESN  = metricas_esn(),
        LSTM = metricas_lstm(),
        GRU  = metricas_gru()
      )
      modelos <- modelos[!sapply(modelos, is.null)]
      if (length(modelos) < 2) {
        par(bg = "transparent")
        plot.new()
        text(0.5, 0.5, "Execute pelo menos 2 modelos para gerar os gráficos comparativos.", 
             cex = 1.1, col = "#64748b", font = 2)
        return()
      }
      
      nomes <- names(modelos)
      cores <- c(ESN = "#059669", LSTM = "#2563eb", GRU = "#7c3aed")
      
      mae_vals  <- sapply(modelos, function(m) m$teste$MAE)
      rmse_vals <- sapply(modelos, function(m) m$teste$RMSE)
      
      par(mfrow = c(1, 2), mar = c(4, 4, 3, 1), bg = "transparent")
      
      bp1 <- barplot(mae_vals, col = cores[nomes], main = "MAE no Teste",
                     ylab = "Erro Absoluto Médio", border = NA, ylim = c(0, max(mae_vals) * 1.25),
                     col.main = "#0f172a")
      grid(col = "#e2e8f0", nx = NA, ny = NULL)
      text(bp1, mae_vals, labels = sprintf("%.4f", mae_vals), pos = 3, cex = 0.9, font = 2, col = "#0f172a")
      
      bp2 <- barplot(rmse_vals, col = cores[nomes], main = "RMSE no Teste",
                     ylab = "Raiz do Erro Quadrático", border = NA, ylim = c(0, max(rmse_vals) * 1.25),
                     col.main = "#0f172a")
      grid(col = "#e2e8f0", nx = NA, ny = NULL)
      text(bp2, rmse_vals, labels = sprintf("%.4f", rmse_vals), pos = 3, cex = 0.9, font = 2, col = "#0f172a")
    })
    
    # Gráfico de tempo
    output$grafico_tempo <- renderPlot({
      modelos <- list(
        ESN  = metricas_esn(),
        LSTM = metricas_lstm(),
        GRU  = metricas_gru()
      )
      modelos <- modelos[!sapply(modelos, is.null)]
      if (length(modelos) < 2) {
        par(bg = "transparent")
        plot.new()
        text(0.5, 0.5, "Execute pelo menos 2 modelos para comparar o tempo.", 
             cex = 1.1, col = "#64748b", font = 2)
        return()
      }
      
      nomes <- names(modelos)
      cores <- c(ESN = "#059669", LSTM = "#2563eb", GRU = "#7c3aed")
      tempos <- sapply(modelos, function(m) m$tempo)
      
      par(mar = c(4, 4, 3, 1), bg = "transparent")
      bp <- barplot(tempos, col = cores[nomes], main = "Tempo de Execução (Segundos)",
                    ylab = "Segundos", border = NA, ylim = c(0, max(tempos) * 1.3),
                    col.main = "#0f172a")
      grid(col = "#e2e8f0", nx = NA, ny = NULL)
      text(bp, tempos, labels = paste0(sprintf("%.2f", tempos), "s"), pos = 3, cex = 1, font = 2, col = "#0f172a")
      
      if ("ESN" %in% nomes && tempos["ESN"] > 0) {
        razoes <- tempos / tempos["ESN"]
        mtext(paste0(nomes, ": ", round(razoes, 1), "x"), side = 1, line = 2.5, 
              at = bp, cex = 0.9, font = 2, col = cores[nomes])
      }
    })
    
    # Conclusão automatizada
    output$conclusao <- renderUI({
      modelos <- list(
        ESN  = metricas_esn(),
        LSTM = metricas_lstm(),
        GRU  = metricas_gru()
      )
      modelos <- modelos[!sapply(modelos, is.null)]
      
      if (length(modelos) < 2) {
        return(div(style = "color: #64748b;", "Execute o modelo ESN e pelo menos um modelo de Deep Learning (LSTM ou GRU) para ver o relatório comparativo."))
      }
      
      nomes <- names(modelos)
      mae_teste <- sapply(modelos, function(m) m$teste$MAE)
      tempos <- sapply(modelos, function(m) m$tempo)
      
      melhor_mae <- names(which.min(mae_teste))
      melhor_tempo <- names(which.min(tempos))
      
      tagList(
        div(style = "font-size: 0.95rem; line-height: 1.7;",
          p(
            tags$strong("• Melhor Precisão (Menor MAE no Teste): "), 
            span(class = paste0("badge-tag badge-", tolower(melhor_mae)), melhor_mae),
            sprintf(" com MAE = %.6f", mae_teste[melhor_mae])
          ),
          p(
            tags$strong("• Maior Eficiência Computacional (Mais Rápido): "),
            span(class = paste0("badge-tag badge-", tolower(melhor_tempo)), melhor_tempo),
            sprintf(" com tempo total de %.3f segundos", tempos[melhor_tempo])
          ),
          if ("ESN" %in% nomes) {
            tagList(
              hr(style = "border-color: #a7f3d0; margin: 12px 0;"),
              h5(style = "font-weight: 800; color: #047857; margin-top: 8px;", "📌 Análise em Relação à ESN:"),
              if ("LSTM" %in% nomes) {
                diff_mae_pct <- ((mae_teste["ESN"] - mae_teste["LSTM"]) / mae_teste["LSTM"]) * 100
                speedup_lstm <- tempos["LSTM"] / tempos["ESN"]
                div(style = "margin-bottom: 8px;",
                  sprintf("• ESN vs LSTM: A ESN foi "),
                  tags$strong(sprintf("%.1f vezes mais rápida", speedup_lstm)),
                  sprintf(" que a LSTM. A diferença no erro MAE de teste é de apenas %.2f%%.", diff_mae_pct)
                )
              },
              if ("GRU" %in% nomes) {
                diff_mae_pct <- ((mae_teste["ESN"] - mae_teste["GRU"]) / mae_teste["GRU"]) * 100
                speedup_gru <- tempos["GRU"] / tempos["ESN"]
                div(style = "margin-bottom: 8px;",
                  sprintf("• ESN vs GRU: A ESN foi "),
                  tags$strong(sprintf("%.1f vezes mais rápida", speedup_gru)),
                  sprintf(" que a GRU. A diferença no erro MAE de teste é de apenas %.2f%%.", diff_mae_pct)
                )
              }
            )
          }
        )
      )
    })
  })
}
