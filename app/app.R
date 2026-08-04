# =============================================================================
# app.R — Aplicação Shiny: Comparação ESN vs LSTM vs GRU
# TFC - Maycon G Silva
# =============================================================================
# Para executar: shiny::runApp("app")
# =============================================================================

library(shiny)

# Carregar módulos
source("utils/data_prep.R", local = TRUE)
source("utils/metrics.R", local = TRUE)
source("modules/mod_esn.R", local = TRUE)
source("modules/mod_lstm.R", local = TRUE)
source("modules/mod_gru.R", local = TRUE)
source("modules/mod_comparacao.R", local = TRUE)

# =============================================================================
# UI
# =============================================================================

ui <- navbarPage(
  title = "🔬 ESN vs LSTM vs GRU — Comparação de Modelos",
  theme = NULL,  # Usa tema padrão Shiny (leve e funcional)
  
  # CSS customizado para melhorar a aparência
  header = tags$head(
    tags$style(HTML("
      body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
      .navbar { background: linear-gradient(135deg, #2c3e50, #34495e) !important; }
      .navbar-default .navbar-brand { color: #ecf0f1 !important; font-weight: bold; }
      .navbar-default .navbar-nav > li > a { color: #bdc3c7 !important; }
      .navbar-default .navbar-nav > .active > a { background: #1abc9c !important; color: white !important; }
      .btn-success { background: #27ae60; border: none; }
      .btn-success:hover { background: #2ecc71; }
      .btn-primary { background: #2980b9; border: none; }
      .btn-primary:hover { background: #3498db; }
      .btn-warning { background: #8e44ad; border: none; color: white; }
      .btn-warning:hover { background: #9b59b6; color: white; }
      .well { border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
      h3, h4 { color: #2c3e50; }
      .tab-content { padding-top: 10px; }
      .nav-tabs > li.active > a { border-top: 3px solid #1abc9c; }
    "))
  ),
  
  # ============================
  # ABA 1: DADOS
  # ============================
  tabPanel("📊 Dados",
    fluidRow(
      column(12,
        h3("Série Temporal PETR4 — Preço de Fechamento com Fator"),
        wellPanel(
          fluidRow(
            column(6,
              fileInput("arquivo_dados", "Carregar arquivo de dados (.txt/.csv):",
                        accept = c(".txt", ".csv")),
              helpText("Ou use o arquivo padrão PETR4_close com factor_2000-2020.txt")
            ),
            column(6,
              actionButton("btn_carregar_default", "📂 Usar Dados Padrão PETR4",
                           class = "btn-info",
                           style = "margin-top: 25px; width: 100%; padding: 10px; font-size: 14px;")
            )
          )
        ),
        
        fluidRow(
          column(4,
            wellPanel(
              h5("📐 Divisão dos Dados"),
              numericInput("treino_n", "Treino (n):", value = 2600, min = 100),
              numericInput("valida_n", "Validação (n):", value = 1299, min = 100),
              numericInput("teste_n", "Teste (n):", value = 1299, min = 100),
              verbatimTextOutput("info_dados")
            )
          ),
          column(8,
            plotOutput("grafico_serie", height = "350px"),
            plotOutput("grafico_splits", height = "250px")
          )
        )
      )
    )
  ),
  
  # ============================
  # ABA 2: ESN
  # ============================
  tabPanel("🧠 ESN",
    esn_ui("esn")
  ),
  
  # ============================
  # ABA 3: LSTM
  # ============================
  tabPanel("📈 LSTM",
    lstm_ui("lstm")
  ),
  
  # ============================
  # ABA 4: GRU
  # ============================
  tabPanel("📉 GRU",
    gru_ui("gru")
  ),
  
  # ============================
  # ABA 5: COMPARAÇÃO
  # ============================
  tabPanel("⚖️ Comparação",
    comparacao_ui("comparacao")
  ),
  
  # ============================
  # ABA 6: DISTRIBUIÇÕES
  # ============================
  tabPanel("🎲 Distribuições",
    fluidRow(
      column(12,
        h3("📋 Distribuições Registradas"),
        helpText("Sistema extensível: novas distribuições podem ser adicionadas via registrar_distribuicao()"),
        tableOutput("tabela_distribuicoes"),
        hr(),
        h4("🔧 Como adicionar uma nova distribuição"),
        wellPanel(
          tags$pre(
            style = "background: #2c3e50; color: #ecf0f1; padding: 15px; border-radius: 5px;",
            '# Adicione no arquivo utils/data_prep.R ou no console R:\n',
            'registrar_distribuicao(\n',
            '  nome = "Cauchy",\n',
            '  funcao = function(n, params) {\n',
            '    rcauchy(n, location = params$location, scale = params$scale)\n',
            '  },\n',
            '  params_default = list(location = 0, scale = 1),\n',
            '  descricao = "Distribuição de Cauchy"\n',
            ')'
          )
        ),
        
        h4("📊 Visualização das Distribuições"),
        fluidRow(
          column(4,
            selectInput("dist_visualizar", "Selecione a distribuição:",
                        choices = NULL),
            numericInput("dist_n_amostras", "Nº de amostras:", value = 1000, min = 100, max = 10000),
            actionButton("btn_gerar_dist", "Gerar Amostras", class = "btn-info")
          ),
          column(8,
            plotOutput("grafico_distribuicao", height = "350px")
          )
        )
      )
    )
  )
)

# =============================================================================
# SERVER
# =============================================================================

server <- function(input, output, session) {
  
  # ============================================
  # Dados reativos
  # ============================================
  dados <- reactiveVal(NULL)
  
  # Carregar dados padrão
  observeEvent(input$btn_carregar_default, {
    caminhos <- c(
      "../Scripts/data/PETR4_close com factor_2000-2020.txt",
      "Scripts/data/PETR4_close com factor_2000-2020.txt",
      "data/PETR4_close com factor_2000-2020.txt"
    )
    
    caminho_encontrado <- NULL
    for (cp in caminhos) {
      if (file.exists(cp)) {
        caminho_encontrado <- cp
        break
      }
    }
    
    if (is.null(caminho_encontrado)) {
      showNotification("❌ Arquivo de dados padrão não encontrado!", type = "error")
      return()
    }
    
    tryCatch({
      data_fac <- as.matrix(read.csv2(caminho_encontrado, header = FALSE))
      dados(as.numeric(data_fac))
      showNotification(paste("✅ Dados carregados:", length(dados()), "observações"), type = "message")
    }, error = function(e) {
      showNotification(paste("❌ Erro ao carregar:", e$message), type = "error")
    })
  })
  
  # Carregar arquivo do usuário
  observeEvent(input$arquivo_dados, {
    req(input$arquivo_dados)
    tryCatch({
      data_fac <- as.matrix(read.csv2(input$arquivo_dados$datapath, header = FALSE))
      dados(as.numeric(data_fac))
      showNotification(paste("✅ Dados carregados:", length(dados()), "observações"), type = "message")
    }, error = function(e) {
      showNotification(paste("❌ Erro ao carregar:", e$message), type = "error")
    })
  })
  
  # Info dos dados
  output$info_dados <- renderPrint({
    req(dados())
    d <- dados()
    cat(sprintf("Total de observações: %d\n", length(d)))
    cat(sprintf("Treino:    %d (%.1f%%)\n", input$treino_n, input$treino_n/length(d)*100))
    cat(sprintf("Validação: %d (%.1f%%)\n", input$valida_n, input$valida_n/length(d)*100))
    cat(sprintf("Teste:     %d (%.1f%%)\n", input$teste_n, input$teste_n/length(d)*100))
    cat(sprintf("Usado:     %d / %d\n", input$treino_n + input$valida_n + input$teste_n, length(d)))
    cat(sprintf("\nMín: %.2f | Máx: %.2f | Média: %.2f\n", min(d), max(d), mean(d)))
  })
  
  # Gráfico da série completa
  output$grafico_serie <- renderPlot({
    req(dados())
    d <- dados()
    par(mar = c(4, 4, 3, 1))
    plot(d, type = 'l', col = '#2c3e50', lwd = 1,
         xlab = "Tempo (dias)", ylab = "Preço com fator (R$)",
         main = "Série Temporal Completa — PETR4")
    grid(col = "#ecf0f1")
  })
  
  # Gráfico dos splits
  output$grafico_splits <- renderPlot({
    req(dados())
    d <- dados()
    tn <- input$treino_n
    vn <- input$valida_n
    ten <- input$teste_n
    
    par(mar = c(4, 4, 2, 1))
    plot(d, type = 'n', xlab = "Tempo (dias)", ylab = "Preço (R$)",
         main = "Divisão: Treino | Validação | Teste")
    
    # Treino
    lines(1:tn, d[1:tn], col = '#27ae60', lwd = 1.5)
    # Validação
    lines((tn+1):(tn+vn), d[(tn+1):(tn+vn)], col = '#f39c12', lwd = 1.5)
    # Teste
    if (tn + vn + ten <= length(d)) {
      lines((tn+vn+1):(tn+vn+ten), d[(tn+vn+1):(tn+vn+ten)], col = '#e74c3c', lwd = 1.5)
    }
    
    abline(v = tn, col = '#27ae60', lty = 2)
    abline(v = tn + vn, col = '#f39c12', lty = 2)
    
    legend('topright', legend = c('Treino', 'Validação', 'Teste'),
           col = c('#27ae60', '#f39c12', '#e74c3c'), lty = 1, lwd = 2, bty = 'n')
  })
  
  # ============================================
  # Módulos dos modelos
  # ============================================
  metricas_esn  <- esn_server("esn", dados)
  metricas_lstm <- lstm_server("lstm", dados)
  metricas_gru  <- gru_server("gru", dados)
  
  # ============================================
  # Módulo de comparação
  # ============================================
  comparacao_server("comparacao", metricas_esn, metricas_lstm, metricas_gru)
  
  # ============================================
  # Aba Distribuições
  # ============================================
  observe({
    dists <- listar_distribuicoes()
    updateSelectInput(session, "dist_visualizar", choices = dists)
  })
  
  output$tabela_distribuicoes <- renderTable({
    dists <- listar_distribuicoes()
    if (length(dists) == 0) return(data.frame(Mensagem = "Nenhuma distribuição registrada."))
    
    do.call(rbind, lapply(dists, function(nome) {
      d <- obter_distribuicao(nome)
      params_str <- paste(names(d$params_default), "=", d$params_default, collapse = ", ")
      data.frame(
        Nome = nome,
        Descricao = d$descricao,
        Parametros_Default = params_str,
        stringsAsFactors = FALSE
      )
    }))
  })
  
  observeEvent(input$btn_gerar_dist, {
    req(input$dist_visualizar)
    output$grafico_distribuicao <- renderPlot({
      amostras <- gerar_amostras(input$dist_visualizar, input$dist_n_amostras)
      par(mfrow = c(1, 2), mar = c(4, 4, 3, 1))
      hist(amostras, breaks = 50, col = '#3498db', border = 'white',
           main = paste("Histograma -", input$dist_visualizar),
           xlab = "Valor", ylab = "Frequência")
      plot(density(amostras), col = '#e74c3c', lwd = 2,
           main = paste("Densidade -", input$dist_visualizar),
           xlab = "Valor")
      polygon(density(amostras), col = '#e74c3c33', border = '#e74c3c')
    })
  })
}

# =============================================================================
# EXECUTAR
# =============================================================================
shinyApp(ui = ui, server = server)
