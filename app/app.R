# =============================================================================
# app.R — Aplicação Shiny: Comparação ESN vs LSTM vs GRU (UI/UX Premium)
# TFC - Maycon G Silva
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
  title = div(
    style = "display: flex; align-items: center; gap: 10px;",
    span(style = "font-size: 1.25rem;", "⚡"),
    span(style = "font-weight: 800; letter-spacing: -0.02em;", "ESNAUTO Benchmark Studio"),
    span(style = "font-size: 0.75rem; background: rgba(255,255,255,0.15); padding: 2px 8px; border-radius: 12px; font-weight: 600;", "ESN vs Deep Learning")
  ),
  theme = NULL,
  
  header = tags$head(
    tags$link(rel = "stylesheet", type = "text/css", href = "custom.css")
  ),
  
  # ============================
  # ABA 1: DADOS
  # ============================
  tabPanel("📊 Dados PETR4",
    fluidRow(
      column(12,
        div(class = "section-subtitle", "BASE DE DADOS & PREPARAÇÃO"),
        h3(class = "section-title", "Série Temporal PETR4 (Preços de Fechamento com Fator)"),
        
        # Action Card para Seleção de Dados
        div(class = "well",
          fluidRow(
            column(7,
              fileInput("arquivo_dados", "📂 Carregar Novo Arquivo (.txt / .csv):",
                        accept = c(".txt", ".csv"), width = "100%"),
              helpText("Formato esperado: Vetor de preços ou CSV com valores de fechamento ajustados.")
            ),
            column(5,
              actionButton("btn_carregar_default", "⚡ Carregar Série Padrão PETR4 (2000-2020)",
                           class = "btn-info",
                           style = "margin-top: 25px; width: 100%; height: 48px;")
            )
          )
        ),
        
        # KPI Cards Rápidos
        uiOutput("kpi_dados_summary"),
        
        br(),
        
        fluidRow(
          column(4,
            div(class = "well",
              h4(style = "margin-top:0;", "📐 Configuração dos Splits"),
              p(style = "color: var(--text-muted); font-size: 0.85rem;", "Defina o número de observações para cada partição:"),
              numericInput("treino_n", "Treino (50% por padrão):", value = 2600, min = 100),
              numericInput("valida_n", "Validação (25% por padrão):", value = 1299, min = 100),
              numericInput("teste_n", "Teste (25% por padrão):", value = 1299, min = 100),
              hr(),
              verbatimTextOutput("info_dados")
            )
          ),
          column(8,
            div(class = "well",
              h4(style = "margin-top:0;", "📈 Série Temporal Completa"),
              plotOutput("grafico_serie", height = "280px"),
              hr(),
              h4("🎯 Particionamento (Treino / Validação / Teste)"),
              plotOutput("grafico_splits", height = "240px")
            )
          )
        )
      )
    )
  ),
  
  # ============================
  # ABA 2: ESN
  # ============================
  tabPanel("🧠 ESN (Reservoir)",
    esn_ui("esn")
  ),
  
  # ============================
  # ABA 3: LSTM
  # ============================
  tabPanel("📈 LSTM Network",
    lstm_ui("lstm")
  ),
  
  # ============================
  # ABA 4: GRU
  # ============================
  tabPanel("📉 GRU Network",
    gru_ui("gru")
  ),
  
  # ============================
  # ABA 5: COMPARAÇÃO
  # ============================
  tabPanel("⚖️ Comparativo & Custo-Benefício",
    comparacao_ui("comparacao")
  ),
  
  # ============================
  # ABA 6: DISTRIBUIÇÕES
  # ============================
  tabPanel("🎲 Distribuições da ESN",
    fluidRow(
      column(12,
        div(class = "section-subtitle", "EXTENSIBILIDADE DE DISTRIBUIÇÕES"),
        h3(class = "section-title", "Catálogo de Distribuições Registradas"),
        p(style = "color: var(--text-muted);", "Estas distribuições estão disponíveis para inicialização das matrizes de pesos W_in e W da ESN:"),
        
        tableOutput("tabela_distribuicoes"),
        
        hr(),
        
        fluidRow(
          column(5,
            div(class = "well",
              h4(style = "margin-top:0;", "💡 Como Adicionar Novas Distribuições"),
              p(style = "font-size: 0.88rem; color: var(--text-secondary);", 
                "O projeto utiliza um sistema de registro desacoplado. Para registrar uma nova distribuição, chame no R:"),
              tags$pre(
                'registrar_distribuicao(\n',
                '  nome = "MinhaDistribuicao",\n',
                '  funcao = function(n, params) { ... },\n',
                '  params_default = list(...),\n',
                '  descricao = "..."\n',
                ')'
              )
            )
          ),
          column(7,
            div(class = "well",
              h4(style = "margin-top:0;", "📊 Visualizador de Amostragem Teórica"),
              fluidRow(
                column(7,
                  selectInput("dist_visualizar", "Selecione a Distribuição:", choices = NULL)
                ),
                column(5,
                  numericInput("dist_n_amostras", "Nº Amostras:", value = 2000, min = 100)
                )
              ),
              actionButton("btn_gerar_dist", "🎲 Gerar Amostras", class = "btn-info", style = "width: 100%; margin-bottom: 15px;"),
              plotOutput("grafico_distribuicao", height = "280px")
            )
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
  
  # Dados reativos
  dados <- reactiveVal(NULL)
  
  # Auto-carregar dados PETR4 ao inicializar
  observe({
    caminhos <- c(
      "../Scripts/data/PETR4_close com factor_2000-2020.txt",
      "Scripts/data/PETR4_close com factor_2000-2020.txt",
      "data/PETR4_close com factor_2000-2020.txt"
    )
    for (cp in caminhos) {
      if (file.exists(cp)) {
        tryCatch({
          data_fac <- as.matrix(read.csv2(cp, header = FALSE))
          dados(as.numeric(data_fac))
        }, error = function(e) {})
        break
      }
    }
  })
  
  # Carregar dados padrão por botão
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
      showNotification("❌ Arquivo PETR4_close com factor_2000-2020.txt não encontrado!", type = "error")
      return()
    }
    
    tryCatch({
      data_fac <- as.matrix(read.csv2(caminho_encontrado, header = FALSE))
      dados(as.numeric(data_fac))
      showNotification(paste("✅ Série PETR4 carregada com sucesso:", length(dados()), "amostras"), type = "message")
    }, error = function(e) {
      showNotification(paste("❌ Erro ao carregar:", e$message), type = "error")
    })
  })
  
  # Carregar arquivo customizado
  observeEvent(input$arquivo_dados, {
    req(input$arquivo_dados)
    tryCatch({
      data_fac <- as.matrix(read.csv2(input$arquivo_dados$datapath, header = FALSE))
      dados(as.numeric(data_fac))
      showNotification(paste("✅ Dados personalizados carregados:", length(dados()), "amostras"), type = "message")
    }, error = function(e) {
      showNotification(paste("❌ Erro ao carregar arquivo:", e$message), type = "error")
    })
  })
  
  # Summary KPI cards
  output$kpi_dados_summary <- renderUI({
    req(dados())
    d <- dados()
    n_total <- length(d)
    n_tr <- input$treino_n
    n_va <- input$valida_n
    n_te <- input$teste_n
    
    fluidRow(
      column(3,
        div(class = "kpi-card",
          div(class = "kpi-title", "Total de Amostras"),
          div(class = "kpi-value", sprintf("%d", n_total)),
          div(class = "kpi-subtitle", "Preços PETR4 com fator")
        )
      ),
      column(3,
        div(class = "kpi-card", style = "border-top: 3px solid #059669;",
          div(class = "kpi-title", "Partição Treino"),
          div(class = "kpi-value", sprintf("%d", n_tr)),
          div(class = "kpi-subtitle", sprintf("%.1f%% do dataset", (n_tr/n_total)*100))
        )
      ),
      column(3,
        div(class = "kpi-card", style = "border-top: 3px solid #d97706;",
          div(class = "kpi-title", "Partição Validação"),
          div(class = "kpi-value", sprintf("%d", n_va)),
          div(class = "kpi-subtitle", sprintf("%.1f%% do dataset", (n_va/n_total)*100))
        )
      ),
      column(3,
        div(class = "kpi-card", style = "border-top: 3px solid #dc2626;",
          div(class = "kpi-title", "Partição Teste"),
          div(class = "kpi-value", sprintf("%d", n_te)),
          div(class = "kpi-subtitle", sprintf("%.1f%% do dataset", (n_te/n_total)*100))
        )
      )
    )
  })
  
  # Text summary
  output$info_dados <- renderPrint({
    req(dados())
    d <- dados()
    cat(sprintf("• Mínimo:  R$ %.2f\n", min(d)))
    cat(sprintf("• Máximo:  R$ %.2f\n", max(d)))
    cat(sprintf("• Média:   R$ %.2f\n", mean(d)))
    cat(sprintf("• Desvio:  R$ %.2f\n", sd(d)))
  })
  
  # Gráfico da série temporal
  output$grafico_serie <- renderPlot({
    req(dados())
    d <- dados()
    par(mar = c(3.5, 4, 1.5, 1), bg = "transparent")
    plot(d, type = 'l', col = '#4f46e5', lwd = 1.5,
         xlab = "Dias", ylab = "Preço Ajustado (R$)",
         axes = FALSE)
    axis(1, col = "#cbd5e1", col.axis = "#475569")
    axis(2, col = "#cbd5e1", col.axis = "#475569")
    grid(col = "#e2e8f0", lty = "dotted")
  })
  
  # Gráfico dos splits
  output$grafico_splits <- renderPlot({
    req(dados())
    d <- dados()
    tn <- input$treino_n
    vn <- input$valida_n
    ten <- input$teste_n
    
    par(mar = c(3.5, 4, 1.5, 1), bg = "transparent")
    plot(d, type = 'n', xlab = "Dias", ylab = "Preço Ajustado (R$)", axes = FALSE)
    axis(1, col = "#cbd5e1", col.axis = "#475569")
    axis(2, col = "#cbd5e1", col.axis = "#475569")
    grid(col = "#e2e8f0", lty = "dotted")
    
    lines(1:tn, d[1:tn], col = '#059669', lwd = 2)
    lines((tn+1):(tn+vn), d[(tn+1):(tn+vn)], col = '#d97706', lwd = 2)
    if (tn + vn + ten <= length(d)) {
      lines((tn+vn+1):(tn+vn+ten), d[(tn+vn+1):(tn+vn+ten)], col = '#dc2626', lwd = 2)
    }
    
    abline(v = tn, col = '#059669', lty = 3, lwd = 1.5)
    abline(v = tn + vn, col = '#d97706', lty = 3, lwd = 1.5)
    
    legend('topleft', legend = c('Treino', 'Validação', 'Teste'),
           col = c('#059669', '#d97706', '#dc2626'), lty = 1, lwd = 2.5, bty = 'n', text.col = '#0f172a')
  })
  
  # Módulos
  metricas_esn  <- esn_server("esn", dados)
  metricas_lstm <- lstm_server("lstm", dados)
  metricas_gru  <- gru_server("gru", dados)
  
  comparacao_server("comparacao", metricas_esn, metricas_lstm, metricas_gru)
  
  # Distribuições
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
        "Distribuição" = nome,
        "Descrição" = d$descricao,
        "Parâmetros Padrão" = params_str,
        check.names = FALSE,
        stringsAsFactors = FALSE
      )
    }))
  })
  
  observeEvent(input$btn_gerar_dist, {
    req(input$dist_visualizar)
    output$grafico_distribuicao <- renderPlot({
      amostras <- gerar_amostras(input$dist_visualizar, input$dist_n_amostras)
      par(mfrow = c(1, 2), mar = c(3.5, 3.5, 2.5, 1), bg = "transparent")
      
      hist(amostras, breaks = 45, col = '#4f46e5', border = '#ffffff',
           main = paste("Histograma:", input$dist_visualizar),
           xlab = "Valor", ylab = "Frequência", col.main = "#0f172a")
      grid(col = "#e2e8f0")
      
      dens <- density(amostras)
      plot(dens, col = '#059669', lwd = 2.5,
           main = paste("Densidade:", input$dist_visualizar),
           xlab = "Valor", col.main = "#0f172a")
      polygon(dens, col = '#05966922', border = '#059669')
      grid(col = "#e2e8f0")
    })
  })
}

# =============================================================================
# EXECUTAR
# =============================================================================
shinyApp(ui = ui, server = server)
