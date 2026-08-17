# =============================================================================
# app.R — Aplicação Shiny: Comparação ESN vs LSTM vs GRU (UI/UX Premium)
# TFC - Maycon G Silva
# Suporta Otimização Live por Algoritmo Genético (GA) e Histórico em CSV
# =============================================================================

library(shiny)

# Carregar módulos e utilitários
source("utils/data_prep.R", local = TRUE)
source("utils/metrics.R", local = TRUE)
source("utils/history_tracker.R", local = TRUE)
source("utils/ga_engine.R", local = TRUE)
source("modules/mod_esn.R", local = TRUE)
source("modules/mod_lstm.R", local = TRUE)
source("modules/mod_gru.R", local = TRUE)
source("modules/mod_comparacao.R", local = TRUE)

# =============================================================================
# UI
# =============================================================================

ui <- navbarPage(
  id = "main_navbar",
  title = div(
    style = "display: flex; align-items: center; gap: 10px;",
    span(style = "font-size: 1.25rem;", "⚡"),
    span(style = "font-weight: 800; letter-spacing: -0.02em;", "ESNAUTO Benchmark Studio"),
    span(style = "font-size: 0.75rem; background: rgba(255,255,255,0.15); padding: 2px 8px; border-radius: 12px; font-weight: 600;", "ESN vs Deep Learning")
  ),
  theme = NULL,
  
  header = tagList(
    tags$head(
      tags$link(rel = "stylesheet", type = "text/css", href = "custom.css")
    ),
    div(
      class = "global-hero-banner",
      div(
        style = "display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px; padding: 18px 24px;",
        div(
          style = "display: flex; flex-direction: column; gap: 4px;",
          div(
            style = "display: flex; align-items: center; gap: 10px;",
            span(style = "display: inline-block; width: 10px; height: 10px; border-radius: 50%; background: #10b981; box-shadow: 0 0 10px #10b981;"),
            span(style = "font-weight: 800; font-size: 1.15rem; color: #0f172a;", "Série Histórica PETR4 (2000–2020)"),
            span(class = "badge-tag badge-esn", "5.198 Amostras")
          ),
          div(
            style = "font-size: 0.92rem; color: #64748b;",
            "Particionamento Oficial: ",
            strong("Treino (2.600 | 50%)"), " • ",
            strong("Validação (1.299 | 25%)"), " • ",
            strong("Teste Out-of-Sample (1.299 | 25%)")
          )
        ),
        div(
          style = "display: flex; align-items: center; gap: 14px;",
          actionButton("btn_abrir_modal_universal", 
                       "⚡ EXECUTAR BENCHMARK COMPLETO (ESN + GA + LSTM + GRU)", 
                       class = "btn-gradient-universal", 
                       style = "min-height: 52px; padding: 12px 28px; font-size: 1.05rem; font-weight: 800; border-radius: 12px;")
        )
      )
    )
  ),
  
  # ============================
  # ABA 1: DADOS
  # ============================
  tabPanel("📊 Dados PETR4", value = "tab_dados",
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
              div(style = "margin-top: 25px;",
                actionButton("btn_carregar_default", "⚡ Carregar Série Padrão PETR4 (2000-2020)",
                             class = "btn-info btn-block",
                             style = "height: 52px; font-size: 1.02rem; font-weight: 700; border-radius: 12px;")
              )
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
  tabPanel("🧠 ESN (Reservoir)", value = "tab_esn",
    esn_ui("esn")
  ),
  
  # ============================
  # ABA 3: LSTM
  # ============================
  tabPanel("📈 LSTM Network", value = "tab_lstm",
    lstm_ui("lstm")
  ),
  
  # ============================
  # ABA 4: GRU
  # ============================
  tabPanel("📉 GRU Network", value = "tab_gru",
    gru_ui("gru")
  ),
  
  # ============================
  # ABA 5: COMPARAÇÃO
  # ============================
  tabPanel("⚖️ Comparativo & Custo-Benefício", value = "tab_comparacao",
    comparacao_ui("comparacao")
  ),
  
  # ============================
  # ABA 6: DISTRIBUIÇÕES
  # ============================
  tabPanel("🎲 Distribuições da ESN", value = "tab_dist",
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
  
  # Holders reativos para sincronização da execução universal
  resultado_esn_externo  <- reactiveVal(NULL)
  resultado_lstm_externo <- reactiveVal(NULL)
  resultado_gru_externo  <- reactiveVal(NULL)
  
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
  
  # =============================================================================
  # ORQUESTRADOR DO BOTÃO UNIVERSAL (BENCHMARK COMPLETO)
  # =============================================================================
  
  executar_benchmark_completo <- function(modo_esn = "preset",
                                         ga_generations = 60,
                                         ga_win = c("GED"),
                                         ga_w = c("Normal"),
                                         ga_anti_estag = TRUE,
                                         epochs_dl = 25, 
                                         timesteps_dl = 10) {
    if (is.null(dados())) {
      showNotification("❌ Carregue os dados da PETR4 antes de iniciar o benchmark!", type = "error")
      return()
    }
    
    d <- dados()
    
    withProgress(message = "⚡ Benchmark Unificado em Andamento...", value = 0, {
      # 1. ESN
      if (modo_esn == "ga_live") {
        # Gerar todas as combinações selecionadas de Win e W
        grade_comb <- expand.grid(win = ga_win, w = ga_w, stringsAsFactors = FALSE)
        n_comb <- nrow(grade_comb)
        
        resultados_ga_lista <- list()
        melhor_res_esn <- NULL
        melhor_fitness <- -Inf
        
        for (k in 1:n_comb) {
          atual_win <- grade_comb$win[k]
          atual_w <- grade_comb$w[k]
          
          # ESN GA ocupa 0% a 50% do progresso total
          pct_base <- ((k - 1) / n_comb) * 0.50
          pct_amplitude <- 0.50 / n_comb
          
          res_ga_k <- otimizar_esn_ga_live(
            dados = d,
            win_dist = atual_win,
            w_dist = atual_w,
            maxiter = ga_generations,
            pop_size = 12,
            anti_estagnacao = ga_anti_estag,
            set_progress = function(val, msg) {
              prog_total <- pct_base + val * pct_amplitude
              setProgress(
                value = prog_total,
                message = sprintf("⚡ Benchmark [Total: %.0f%%]", prog_total * 100),
                detail = sprintf("[Etapa 1/3: ESN GA %d/%d — %s+%s] %s", k, n_comb, atual_win, atual_w, msg)
              )
            }
          )
          
          resultados_ga_lista[[k]] <- res_ga_k
          
          if (res_ga_k$fitness > melhor_fitness) {
            melhor_fitness <- res_ga_k$fitness
            melhor_res_esn <- res_ga_k
          }
        }
        
        res_esn <- melhor_res_esn
        res_esn$todas_combinacoes <- resultados_ga_lista
      } else {
        setProgress(0.15, message = "⚡ Benchmark [Total: 15%]", detail = "[Etapa 1/3: ESN Preset] Executando ESN com parâmetros ótimos do TCC...")
        res_esn <- executar_modelo_esn(
          dados = d, 
          cenario_id = "9220_GED_Normal_15", 
          set_progress = function(val, msg) {
            prog_total <- 0.10 + val * 0.40
            setProgress(
              value = prog_total,
              message = sprintf("⚡ Benchmark [Total: %.0f%%]", prog_total * 100),
              detail = paste0("[Etapa 1/3: ESN Preset] ", msg)
            )
          }
        )
      }
      resultado_esn_externo(res_esn)
      
      # 2. LSTM (50% a 75%)
      res_lstm <- treinar_modelo_lstm(
        dados = d, 
        units = 50, 
        timesteps = timesteps_dl, 
        dropout = 0.2, 
        epochs = epochs_dl, 
        batch_size = 16, 
        optimizer = "adam",
        set_progress = function(val, msg) {
          prog_total <- 0.50 + val * 0.25
          setProgress(
            value = prog_total,
            message = sprintf("⚡ Benchmark [Total: %.0f%%]", prog_total * 100),
            detail = sprintf("[Etapa 2/3: LSTM (%d épocas)] %s", epochs_dl, msg)
          )
        }
      )
      resultado_lstm_externo(res_lstm)
      
      # 3. GRU (75% a 98%)
      res_gru <- treinar_modelo_gru(
        dados = d, 
        units = 50, 
        timesteps = timesteps_dl, 
        dropout = 0.2, 
        epochs = epochs_dl, 
        batch_size = 16, 
        optimizer = "adam",
        set_progress = function(val, msg) {
          prog_total <- 0.75 + val * 0.23
          setProgress(
            value = prog_total,
            message = sprintf("⚡ Benchmark [Total: %.0f%%]", prog_total * 100),
            detail = sprintf("[Etapa 3/3: GRU (%d épocas)] %s", epochs_dl, msg)
          )
        }
      )
      resultado_gru_externo(res_gru)
      
      setProgress(1.0, message = "⚡ Benchmark [Total: 100%]", detail = "Consolidando gráficos e comparativo...")
    })
    
    updateNavbarPage(session, "main_navbar", selected = "tab_comparacao")
    
    if (modo_esn == "ga_live") {
      n_tot <- if (exists("n_comb")) n_comb else 1
      if (n_tot > 1) {
        showNotification(sprintf("🎉 Benchmark Concluído! %d combinações de distribuições testadas pelo GA. Campeã: Win=%s + W=%s", 
                                 n_tot, res_esn$dist_win, res_esn$dist_w), 
                         type = "message", duration = 10)
      } else if (!is.null(res_esn$registro) && isTRUE(res_esn$registro$eh_novo_recorde)) {
        showNotification("🏆 NOVO RECORDE HISTÓRICO GLOBAL ENCONTRADO PELO GA! Verifique o painel comparativo.", 
                         type = "message", duration = 12)
      } else {
        showNotification("🎉 Benchmark Completo Concluído! Todos os modelos foram executados e comparados.", 
                         type = "message", duration = 8)
      }
    } else {
      showNotification("🎉 Benchmark Completo Concluído! Todos os modelos foram executados e comparados.", 
                       type = "message", duration = 8)
    }
  }
  
  # Modal de configuração e confirmação do Benchmark
  observeEvent(input$btn_abrir_modal_universal, {
    showModal(modalDialog(
      title = div(style = "display: flex; align-items: center; gap: 8px; font-weight: 800; color: #0f172a;",
                  span(style = "font-size: 1.4rem;", "⚡"), "Executar Benchmark Completo Unificado"),
      size = "m",
      easyClose = TRUE,
      footer = tagList(
        modalButton("Cancelar"),
        actionButton("btn_iniciar_universal", "🚀 Iniciar Benchmark Agora", 
                     class = "btn-primary", 
                     style = "font-weight: 700; height: 46px; padding: 0 24px; font-size: 1rem; border-radius: 10px;")
      ),
      div(
        p("Esta ação executará todos os modelos sequencialmente sob as **mesmas condições experimentais** (Série PETR4 2000-2020, Splits 50/25/25):"),
        hr(),
        
        radioButtons("tipo_execucao_esn", "Modo de Execução da ESN:",
                     choices = c(
                       "⚡ Usar Melhor Modelo Pré-Otimizado (Rápido — ~30s)" = "preset",
                       "🧬 Otimizar ESN ao Vivo com Algoritmo Genético (GA Live)" = "ga_live"
                     ),
                     selected = "preset"),
        
        conditionalPanel(
          condition = "input.tipo_execucao_esn == 'ga_live'",
          div(style = "background: #f0fdf4; border: 1px solid #bbf7d0; padding: 14px; border-radius: 10px; margin: 10px 0;",
            h5(style = "margin: 0 0 10px 0; color: #166534; font-weight: 800;", "🧬 Configuração do GA Live:"),
            fluidRow(
              column(6, 
                selectizeInput("modal_ga_win", "Distribuição(ões) Win (Entrada):", 
                               choices = c("GED", "Normal", "Uniforme", "t de Student", "Normal Esparsa", "Cauchy"), 
                               selected = c("GED"), 
                               multiple = TRUE,
                               options = list(plugins = list('remove_button'), placeholder = 'Selecione uma ou mais...'))
              ),
              column(6, 
                selectizeInput("modal_ga_w", "Distribuição(ões) W (Reservatório):", 
                               choices = c("Normal", "Uniforme", "GED", "t de Student", "Normal Esparsa"), 
                               selected = c("Normal"), 
                               multiple = TRUE,
                               options = list(plugins = list('remove_button'), placeholder = 'Selecione uma ou mais...'))
              )
            ),
            div(style = "display: flex; gap: 8px; margin-bottom: 12px; flex-wrap: wrap;",
              actionButton("btn_modal_ga_preset_tcc", "⚡ 4 Cenários TCC", class = "btn-default btn-xs", style = "font-size: 0.78rem; padding: 3px 8px;"),
              actionButton("btn_modal_ga_all_win", "+ Todos Win", class = "btn-default btn-xs", style = "font-size: 0.78rem; padding: 3px 8px;"),
              actionButton("btn_modal_ga_all_w", "+ Todos W", class = "btn-default btn-xs", style = "font-size: 0.78rem; padding: 3px 8px;")
            ),
            uiOutput("modal_ga_combinations_info"),
            sliderInput("modal_ga_generations", "Número de Gerações GA:", min = 20, max = 2000, value = 60, step = 20),
            checkboxInput("modal_ga_anti_estag", "Ativar Exploração Anti-Estagnação (Cataclismo)", value = TRUE)
          )
        ),
        
        hr(),
        radioButtons("perfil_dl", "Perfil de Treinamento Deep Learning (LSTM / GRU):",
                     choices = c(
                       "⚡ DL Rápido (25 épocas — Duração: ~15s)" = "rapido",
                       "🏆 DL Produção (80 épocas — Duração: ~40s)" = "producao",
                       "⚙️ DL Personalizado" = "custom"
                     ),
                     selected = "rapido"),
        conditionalPanel(
          condition = "input.perfil_dl == 'custom'",
          sliderInput("custom_epochs", "Épocas para LSTM e GRU:", min = 10, max = 200, value = 50, step = 10),
          sliderInput("custom_timesteps", "Janela Temporal (Timesteps):", min = 5, max = 30, value = 10, step = 5)
        ),
        div(style = "background: #f8fafc; padding: 12px; border-radius: 8px; font-size: 0.85rem; color: #64748b; border: 1px solid #e2e8f0; margin-top: 12px;",
            "💡 Todos os resultados do GA serão gravados no arquivo persistente historico_otimizacoes_ga.csv e comparados com o recorde histórico!")
      )
    ))
  })
  
  # Ações rápidas dos botões no Modal
  observeEvent(input$btn_modal_ga_preset_tcc, {
    updateSelectizeInput(session, "modal_ga_win", selected = c("GED", "Normal", "Uniforme"))
    updateSelectizeInput(session, "modal_ga_w", selected = c("Normal", "Uniforme"))
  })
  
  observeEvent(input$btn_modal_ga_all_win, {
    updateSelectizeInput(session, "modal_ga_win", selected = c("GED", "Normal", "Uniforme", "t de Student", "Normal Esparsa", "Cauchy"))
  })
  
  observeEvent(input$btn_modal_ga_all_w, {
    updateSelectizeInput(session, "modal_ga_w", selected = c("Normal", "Uniforme", "GED", "t de Student", "Normal Esparsa"))
  })
  
  output$modal_ga_combinations_info <- renderUI({
    n_win <- length(input$modal_ga_win)
    n_w <- length(input$modal_ga_w)
    tot <- max(1, n_win * n_w)
    div(style = "background: #dcfce7; border: 1px solid #86efac; border-radius: 6px; padding: 6px 12px; font-size: 0.85rem; color: #166534; font-weight: 700; margin-bottom: 10px;",
        sprintf("📊 Total de Combinações a Testar: %d (%d Win × %d W)", tot, n_win, n_w))
  })
  
  observeEvent(input$btn_iniciar_universal, {
    removeModal()
    
    modo_esn <- input$tipo_execucao_esn
    ga_gen <- if (modo_esn == "ga_live") input$modal_ga_generations else 60
    ga_win <- if (modo_esn == "ga_live") {
      if (is.null(input$modal_ga_win) || length(input$modal_ga_win) == 0) c("GED") else input$modal_ga_win
    } else "GED"
    
    ga_w <- if (modo_esn == "ga_live") {
      if (is.null(input$modal_ga_w) || length(input$modal_ga_w) == 0) c("Normal") else input$modal_ga_w
    } else "Normal"
    
    ga_anti <- if (modo_esn == "ga_live") input$modal_ga_anti_estag else TRUE
    
    ep <- switch(input$perfil_dl,
                 "rapido" = 25,
                 "producao" = 80,
                 "custom" = input$custom_epochs)
    ts <- if (input$perfil_dl == "custom") input$custom_timesteps else 10
    
    executar_benchmark_completo(
      modo_esn = modo_esn,
      ga_generations = ga_gen,
      ga_win = ga_win,
      ga_w = ga_w,
      ga_anti_estag = ga_anti,
      epochs_dl = ep,
      timesteps_dl = ts
    )
  })
  
  # Módulos com passagem dos canais reativos
  metricas_esn  <- esn_server("esn", dados, resultado_esn_externo)
  metricas_lstm <- lstm_server("lstm", dados, resultado_lstm_externo)
  metricas_gru  <- gru_server("gru", dados, resultado_gru_externo)
  
  # Módulo de comparação com callback de execução rápida
  comparacao_server("comparacao", metricas_esn, metricas_lstm, metricas_gru, 
                    on_executar_tudo = function() {
                      executar_benchmark_completo(modo_esn = "preset", epochs_dl = 25, timesteps_dl = 10)
                    })
  
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
