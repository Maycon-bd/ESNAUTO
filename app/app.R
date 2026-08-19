# =============================================================================
# app.R — Aplicação Shiny: Comparação ESN vs LSTM vs GRU (UI/UX Premium)
# TFC - Maycon G Silva
# Suporta Otimização Live por Algoritmo Genético (GA) e Histórico em CSV
# =============================================================================

library(shiny)

# Carregar módulos e utilitários
source("utils/data_prep.R", local = TRUE)
source("utils/metrics.R", local = TRUE)
source("utils/esn_core.R", local = TRUE)
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
      tags$link(rel = "stylesheet", type = "text/css", href = "custom.css"),
      tags$script(HTML("
        var isBenchmarkPaused = false;

        function notifyControlServer(action) {
          fetch('http://127.0.0.1:8089/' + action, {mode: 'no-cors'}).catch(function(e) {
            fetch('http://127.0.0.1:8090/' + action, {mode: 'no-cors'}).catch(function(err) {});
          });
        }

        function togglePauseBenchmark(btn) {
          var badge = document.getElementById('bfw_status_badge');
          if (!isBenchmarkPaused) {
            isBenchmarkPaused = true;
            btn.innerHTML = '▶️ Retomar';
            btn.className = 'btn btn-success';
            if (badge) { badge.className = 'bfw-badge bfw-badge-paused'; badge.innerText = '⏸️ Pausado'; }
            notifyControlServer('pause');
            Shiny.setInputValue('btn_pausar_execucao', Date.now(), {priority: 'event'});
          } else {
            isBenchmarkPaused = false;
            btn.innerHTML = '⏸️ Pausar';
            btn.className = 'btn btn-warning';
            if (badge) { badge.className = 'bfw-badge bfw-badge-running'; badge.innerText = '🟢 Executando'; }
            notifyControlServer('resume');
            Shiny.setInputValue('btn_retomar_execucao', Date.now(), {priority: 'event'});
          }
        }

        function cancelBenchmark(btn) {
          btn.innerHTML = '⏹️ Cancelando...';
          btn.disabled = true;
          var badge = document.getElementById('bfw_status_badge');
          if (badge) { badge.className = 'bfw-badge bfw-badge-paused'; badge.innerText = '⏹️ Cancelando & Salvando'; }
          var detail = document.getElementById('bfw_detail');
          if (detail) detail.innerText = '⏹️ Interrompendo GA, avaliando melhor modelo e salvando no CSV...';
          notifyControlServer('cancel');
          Shiny.setInputValue('btn_cancelar_execucao', Date.now(), {priority: 'event'});
        }

        Shiny.addCustomMessageHandler('show_benchmark_widget', function(msg) {
          var el = document.getElementById('benchmark_floating_widget');
          if (el) el.style.display = 'block';
          isBenchmarkPaused = false;
          var pBtn = document.getElementById('btn_pause_toggle_js');
          if (pBtn) {
            pBtn.innerHTML = '⏸️ Pausar';
            pBtn.className = 'btn btn-warning';
            pBtn.disabled = false;
          }
          var cBtn = document.getElementById('btn_cancel_js');
          if (cBtn) {
            cBtn.innerHTML = '⏹️ Cancelar & Salvar';
            cBtn.disabled = false;
          }
          var badge = document.getElementById('bfw_status_badge');
          if (badge) { badge.className = 'bfw-badge bfw-badge-running'; badge.innerText = '🟢 Executando'; }
        });

        Shiny.addCustomMessageHandler('hide_benchmark_widget', function(msg) {
          var el = document.getElementById('benchmark_floating_widget');
          if (el) el.style.display = 'none';
        });

        Shiny.addCustomMessageHandler('update_benchmark_widget', function(data) {
          var el = document.getElementById('benchmark_floating_widget');
          if (el) el.style.display = 'block';
          var fill = document.getElementById('bfw_progress_fill');
          if (fill) fill.style.width = data.pct + '%';
          var detail = document.getElementById('bfw_detail');
          if (detail) detail.innerText = data.detail;
          var badge = document.getElementById('bfw_status_badge');
          var pBtn = document.getElementById('btn_pause_toggle_js');
          if (data.status === 'paused') {
            if (badge) { badge.className = 'bfw-badge bfw-badge-paused'; badge.innerText = '⏸️ Pausado'; }
            if (pBtn) { pBtn.innerHTML = '▶️ Retomar'; pBtn.className = 'btn btn-success'; }
            isBenchmarkPaused = true;
          } else {
            if (badge) { badge.className = 'bfw-badge bfw-badge-running'; badge.innerText = '🟢 Executando (' + data.pct + '%)'; }
            if (pBtn && !isBenchmarkPaused) { pBtn.innerHTML = '⏸️ Pausar'; pBtn.className = 'btn btn-warning'; }
          }
        });
      "))
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
    ),
    # Floating Widget persistente no canto inferior direito
    div(
      id = "benchmark_floating_widget",
      class = "benchmark-floating-widget",
      style = "display: none;",
      div(class = "bfw-header",
        span(id = "bfw_status_badge", class = "bfw-badge bfw-badge-running", "🟢 Executando"),
        span(style = "font-weight: 800; font-size: 0.95rem; color: #f8fafc;", "⚡ Benchmark ao Vivo")
      ),
      div(id = "bfw_detail", class = "bfw-detail", "Iniciando processamento..."),
      div(class = "bfw-progress-bar-container",
        div(id = "bfw_progress_fill", class = "bfw-progress-bar-fill", style = "width: 0%;")
      ),
      div(class = "bfw-actions",
        tags$button(id = "btn_pause_toggle_js", type = "button", class = "btn btn-warning", 
                    onclick = "togglePauseBenchmark(this);", "⏸️ Pausar"),
        tags$button(id = "btn_cancel_js", type = "button", class = "btn btn-danger", 
                    onclick = "cancelBenchmark(this);", "⏹️ Cancelar & Salvar")
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
  ),
  
  # ============================
  # ABA 7: DOCUMENTAÇÃO & TFC
  # ============================
  tabPanel("📚 Documentação & TFC", value = "tab_docs",
    withMathJax(),
    fluidRow(
      column(12,
        div(class = "section-subtitle", "FUNDAMENTAÇÃO ACADÊMICA & MANUAL DO SISTEMA"),
        h3(class = "section-title", "Documentação Metodológica do TFC (Maycon Garcia Silva)"),
        p(style = "color: var(--text-muted); font-size: 1rem;", 
          "Visão unificada da arquitetura do projeto, modelagem matemática da ESN, Algoritmo Genético com Cataclismo, controle ao vivo e referências ABNT:"),
        
        tabsetPanel(type = "tabs",
          
          # Sub-Aba 1: Metodologia GA
          tabPanel("🧬 GA, LHS & Mapeamento 55-Bits",
            div(class = "well", style = "margin-top: 15px;",
              h4(style = "color: #4f46e5; font-weight: 800;", "1. Mapeamento Cromossômico da ESN (55 Bits)"),
              p("A otimização simultânea dos hiperparâmetros da Echo State Network é codificada em um vetor binário de exatamente 55 bits $\\mathbf{c} \\in \\{0, 1\\}^{55}$, particionado em 5 genes:"),
              tags$table(class = "table table-bordered table-striped",
                tags$thead(
                  tags$tr(
                    tags$th("Hiperparâmetro"),
                    tags$th("Bits"),
                    tags$th("Tamanho"),
                    tags$th("Domínio Discreto / Contínuo"),
                    tags$th("Impacto Fisiológico na ESN")
                  )
                ),
                tags$tbody(
                  tags$tr(
                    tags$td(strong("Taxa de Vazamento (a)")),
                    tags$td("Bits 1 a 17"),
                    tags$td("17 bits"),
                    tags$td("$$a \\in (0, 1]$$"),
                    tags$td("Inércia temporal e memória de longo prazo dos neurônios do reservatório.")
                  ),
                  tags$tr(
                    tags$td(strong("Raio Espectral (sr)")),
                    tags$td("Bits 18 a 34"),
                    tags$td("17 bits"),
                    tags$td("$$\\rho(W) \\in (0, 1]$$"),
                    tags$td("Garante a Condição de Estado de Eco (ESP) e estabilidade não-linear assintótica.")
                  ),
                  tags$tr(
                    tags$td(strong("Período de Lavagem (initLen)")),
                    tags$td("Bits 35 a 41"),
                    tags$td("7 bits"),
                    tags$td("$$\\text{initLen} \\in [2, 129]$$"),
                    tags$td("Descarte de transientes iniciais arbitrários de ativação do reservatório.")
                  ),
                  tags$tr(
                    tags$td(strong("Tamanho do Reservatório (tam_reservoir)")),
                    tags$td("Bits 42 a 46"),
                    tags$td("5 bits"),
                    tags$td("$$N_x \\in [2, 33]$$"),
                    tags$td("Dimensão do espaço de estados e riqueza das projeções não-lineares.")
                  ),
                  tags$tr(
                    tags$td(strong("Regularização Ridge (reg)")),
                    tags$td("Bits 47 a 55"),
                    tags$td("9 bits"),
                    tags$td("$$\\lambda \\in [10^{-9}, 10^{-4}]$$"),
                    tags$td("Penalidade $L_2$ de Tikhonov na regressão linear da camada de saída $$W_{\\text{out}}$$.")
                  )
                )
              ),
              hr(),
              h4(style = "color: #4f46e5; font-weight: 800;", "2. Inicialização por Hipercubo Latino (LHS)"),
              p("Para evitar o viés da inicialização pseudoaleatória pura e cobrir uniformemente o espaço de busca de $$2^{55} \\approx 3{,}60 \\times 10^{16}$$ estados, a Geração 0 é populada via Amostragem por Hipercubo Latino estratificada em $$P$$ intervalos equiprováveis por gene.")
            )
          ),
          
          # Sub-Aba 2: Cataclismo & 15.000 Gerações
          tabPanel("💥 Cataclismo & 15.000+ Gerações",
            div(class = "well", style = "margin-top: 15px;",
              h4(style = "color: #d97706; font-weight: 800;", "1. O Operador de Reinicialização Cataclísmica Adaptativa (CHC)"),
              p("Inspirado no algoritmo CHC (Eshelman, 1991), o operador anti-estagnação detecta quando a diversidade genética da população cai e o melhor fitness estaciona por $$k$$ gerações:"),
              tags$blockquote(
                p(strong("Elitismo Estrito:"), " O indivíduo recordista $$\\mathbf{c}^*$$ é integralmente preservado na posição 1."),
                p(strong("Hipermutação Controlada:"), " Os demais $$P - 1$$ indivíduos sofrem mutação binária estocástica a uma taxa de $$40\\%$$, executando um salto quântico para novas bacias de atração inexploradas.")
              ),
              hr(),
              h4(style = "color: #d97706; font-weight: 800;", "2. Calibração Adaptativa do Limiar de Estagnação ($$\\theta_{\\text{limiar}}$$)"),
              tags$table(class = "table table-bordered table-striped",
                tags$thead(
                  tags$tr(
                    tags$th("Horizonte de Busca"),
                    tags$th("Nº de Gerações"),
                    tags$th("Limiar sem Melhora (\\(\\theta_{\\text{limiar}}\\))"),
                    tags$th("Comportamento Evolutivo")
                  )
                ),
                tags$tbody(
                  tags$tr(
                    tags$td(span(class = "badge-tag badge-lstm", "🔬 Rápido")),
                    tags$td("$$\\le 500$$ gerações"),
                    tags$td(strong("30 gerações")),
                    tags$td("Sensibilidade ágil para triagem e screening de matrizes.")
                  ),
                  tags$tr(
                    tags$td(span(class = "badge-tag badge-gru", "⚙️ Intermediário")),
                    tags$td("$$1.000$$ a $$4.999$$"),
                    tags$td(strong("50 gerações")),
                    tags$td("Equilíbrio entre exploração local e saltos de vale.")
                  ),
                  tags$tr(
                    tags$td(span(class = "badge-tag badge-esn", "🏆 Produção Oficial")),
                    tags$td("$$5.000$$ a $$9.999$$"),
                    tags$td(strong("80 gerações")),
                    tags$td("Exploração profunda de cada atrator multimodal.")
                  ),
                  tags$tr(
                    tags$td(span(class = "badge-tag badge-best", "🌊 Produção Estendida")),
                    tags$td("$$\\ge 10.000$$ gerações"),
                    tags$td(strong("100 gerações")),
                    tags$td("Refinamento exaustivo e máximo aproveitamento de 15.000+ gerações.")
                  )
                )
              ),
              hr(),
              h4(style = "color: #d97706; font-weight: 800;", "3. Por que 15.000+ Gerações são Eficazes com Cataclismo?"),
              p("Em GAs clássicos sem cataclismo, a busca satura após ~2.000 iterações por perda de diversidade alélica. Com o cataclismo ativo, o algoritmo executa ciclos sucessivos de:"),
              div(style = "background: #f8fafc; padding: 14px; border-radius: 8px; border: 1px solid #cbd5e1; font-family: monospace; font-size: 0.95rem; text-align: center; color: #0f172a; margin: 10px 0;",
                  "Exploração Global (LHS) ➔ Refinamento Local ➔ Estagnação Detectada ➔ Salto Cataclísmico (40%) ➔ Novo Vale de Atração"),
              p("Em 15.000 gerações, ocorrem entre 20 e 40 ciclos de cataclismo, permitindo encontrar combinações raras de matrizes de cauda pesada (Laplace, Pearson V, GED) que superam recordes históricos.")
            )
          ),
          
          # Sub-Aba 3: Live Controller & Arquitetura
          tabPanel("🎛️ Live Controller & Tempo Real",
            div(class = "well", style = "margin-top: 15px;",
              h4(style = "color: #059669; font-weight: 800;", "1. Arquitetura de Controle em Tempo Real"),
              p("Para contornar a natureza síncrona single-threaded do R durante loops pesados de CPU, o ESNAUTO Benchmark Studio utiliza uma arquitetura de comunicação em 3 níveis:"),
              tags$ul(
                tags$li(strong("Bomba de Rede WebSocket (httpuv::service):"), " A cada iteração do GA, o R consome pacotes pendentes do socket TCP, lendo cliques instantaneamente."),
                tags$li(strong("Servidor HTTP Auxiliar em Background:"), " Opera nas portas 8089-8092 para receber sinalizações HTTP diretas do navegador."),
                tags$li(strong("Sinalização IPC Atômica (Flags de Arquivo):"), " Criação instantânea de flags no disco (", code("ga_cancelar.flag"), " e ", code("ga_pausar.flag"), "), garantindo resposta com latência inferior a 1 milissegundo.")
              ),
              hr(),
              h4(style = "color: #059669; font-weight: 800;", "2. Operações do Widget Flutuante"),
              tags$ul(
                tags$li(strong("Botão Único Dinâmico:"), " Alterna de forma estrita e sem ambiguidade entre ", span(class = "badge-tag badge-esn", "⏸️ Pausar"), " e ", span(class = "badge-tag badge-best", "▶️ Retomar"), "."),
                tags$li(strong("Cancelamento com Salvamento Seguro:"), " Ao clicar em ", span(class = "badge-tag badge-lstm", "⏹️ Cancelar & Salvar"), ", o GA não perde o progresso: recupera o melhor modelo até aquela geração, avalia nas partições de teste cego e grava no arquivo ", code("historico_otimizacoes_ga.csv"), " com a tag (Cancelado).")
              )
            )
          ),
          
          # Sub-Aba 4: Benchmark e Resultados
          tabPanel("📊 Comparativo & Custo-Benefício",
            div(class = "well", style = "margin-top: 15px;",
              h4(style = "color: #0f172a; font-weight: 800;", "Exemplo de Comparativo & Referência Preliminar"),
              p("Abaixo está um exemplo de referência com dados de baterias preliminares na série PETR4 (2000–2020) sob a partição oficial 50/25/25:"),
              div(class = "alert alert-info", style = "font-size: 0.9rem;",
                strong("📌 Nota Importante:"), " Os valores abaixo servem como modelo ilustrativo da metodologia. Os ", strong("resultados oficiais e definitivos"), " do seu TFC serão gerados e exibidos dinamicamente na aba ", strong("⚖️ Comparativo & Custo-Benefício"), " e registrados no arquivo ", code("historico_otimizacoes_ga.csv"), " assim que você disparar as execuções de produção."
              ),
              tags$table(class = "table table-bordered table-hover",
                tags$thead(
                  tags$tr(
                    tags$th("Modelo"),
                    tags$th("MAE Teste (R$)"),
                    tags$th("RMSE Teste"),
                    tags$th("MAPE (%)"),
                    tags$th("R² Score"),
                    tags$th("Tempo Inferência"),
                    tags$th("Referência")
                  )
                ),
                tags$tbody(
                  tags$tr(style = "background: #f0fdf4; font-weight: 700;",
                    tags$td("🧠 ESN (GA + LHS + Cataclismo)"),
                    tags$td("~0.3272"),
                    tags$td("~0.4812"),
                    tags$td("~1.89%"),
                    tags$td("~0.9942"),
                    tags$td("< 0.5 s"),
                    tags$td(span(class = "badge-tag badge-best", "🏆 Teste Piloto"))
                  ),
                  tags$tr(
                    tags$td("📉 GRU Network (80 épocas)"),
                    tags$td("~0.3566"),
                    tags$td("~0.5489"),
                    tags$td("~2.04%"),
                    tags$td("~0.9912"),
                    tags$td("~60 s"),
                    tags$td(span(class = "badge-tag badge-gru", "Teste Piloto"))
                  ),
                  tags$tr(
                    tags$td("📈 LSTM Network (80 épocas)"),
                    tags$td("~0.4521"),
                    tags$td("~0.8166"),
                    tags$td("~2.54%"),
                    tags$td("~0.9839"),
                    tags$td("~50 s"),
                    tags$td(span(class = "badge-tag badge-lstm", "Teste Piloto"))
                  )
                )
              )
            )
          ),
          
          # Sub-Aba 5: Referências ABNT
          tabPanel("📑 Referências Bibliográficas (ABNT)",
            div(class = "well", style = "margin-top: 15px;",
              h4(style = "color: #0f172a; font-weight: 800;", "Referências Formais para o TFC"),
              tags$ul(style = "line-height: 1.8;",
                tags$li(strong("CHO, K. et al."), " Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation. ", tags$em("Proceedings of EMNLP"), ", p. 1724–1734, 2014."),
                tags$li(strong("ESHELMAN, L. J."), " The CHC Adaptive Search Algorithm: How to Have Safe Search When Engaging in Alternative Genetic Selection. ", tags$em("Foundations of Genetic Algorithms"), ", v. 1, p. 265–283, 1991."),
                tags$li(strong("GOLDBERG, D. E."), " ", tags$em("Genetic Algorithms in Search, Optimization, and Machine Learning"), ". Boston: Addison-Wesley, 1989."),
                tags$li(strong("HOCHREITER, S.; SCHMIDHUBER, J."), " Long Short-Term Memory. ", tags$em("Neural Computation"), ", v. 9, n. 8, p. 1735–1780, 1997."),
                tags$li(strong("JAEGER, H."), " ", tags$em("The “echo state” approach to analysing and training recurrent neural networks"), ". GMD Report 148, German National Research Center for Information Technology, 2001."),
                tags$li(strong("KRISHNAKUMAR, K."), " Micro-genetic algorithms for stationary and non-stationary function optimization. ", tags$em("SPIE Proceedings: Intelligent Control and Adaptive Systems"), ", v. 1196, p. 289–296, 1989."),
                tags$li(strong("LUKOŠEVIČIUS, M.; JAEGER, H."), " Reservoir computing approaches to recurrent neural network training. ", tags$em("Computer Science Review"), ", v. 3, n. 3, p. 127–149, 2009."),
                tags$li(strong("McKAY, M. D.; BECKMAN, R. J.; CONOVER, W. J."), " A Comparison of Three Methods for Selecting Values of Input Variables in the Analysis of Output from a Computer Code. ", tags$em("Technometrics"), ", v. 21, n. 2, p. 239–245, 1979.")
              )
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
  
  # Estado ao vivo do Benchmark (Pausar / Cancelar)
  benchmark_ativo   <- reactiveVal(FALSE)
  benchmark_pausado <- reactiveVal(FALSE)
  benchmark_pct     <- reactiveVal(0)
  benchmark_msg     <- reactiveVal("Iniciando benchmark...")
  
  # Painel de controle ao vivo (Pausar / Retomar / Cancelar)
  output$benchmark_live_control_panel <- renderUI({
    req(benchmark_ativo())
    
    pausado <- benchmark_pausado()
    pct <- benchmark_pct()
    msg <- benchmark_msg()
    
    div(class = "benchmark-live-card",
      fluidRow(
        column(8,
          div(style = "display: flex; align-items: center; gap: 10px; margin-bottom: 8px; flex-wrap: wrap;",
            if (pausado) {
              span(style = "background: #f59e0b; color: #78350f; font-weight: 800; padding: 4px 12px; border-radius: 6px; font-size: 0.82rem; letter-spacing: 0.02em;", "⏸️ OTIMIZAÇÃO PAUSADA")
            } else {
              span(style = "background: #10b981; color: #064e3b; font-weight: 800; padding: 4px 12px; border-radius: 6px; font-size: 0.82rem; letter-spacing: 0.02em;", "🟢 PROCESSANDO AO VIVO")
            },
            span(style = "font-weight: 800; font-size: 1.1rem; color: #ffffff;", sprintf("⚡ Benchmark em Andamento [%d%%]", pct))
          ),
          div(style = "font-size: 0.92rem; color: #e2e8f0; margin-bottom: 10px; font-weight: 500;", msg),
          div(class = "progress", style = "height: 12px; border-radius: 6px; background: rgba(255,255,255,0.15); margin: 0; overflow: hidden;",
            div(class = paste0("progress-bar progress-bar-striped ", if (pausado) "progress-bar-warning" else "active progress-bar-info"),
                role = "progressbar", style = sprintf("width: %d%%; transition: width 0.3s ease;", pct))
          )
        ),
        column(4, style = "display: flex; align-items: center; justify-content: flex-end; gap: 12px; height: 100%; margin-top: 10px; flex-wrap: wrap;",
          if (!pausado) {
            actionButton("btn_pausar_execucao", "⏸️ Pausar", class = "btn-live-pause")
          } else {
            actionButton("btn_retomar_execucao", "▶️ Retomar", class = "btn-live-resume")
          },
          actionButton("btn_cancelar_execucao", "⏹️ Cancelar & Salvar", class = "btn-live-cancel")
        )
      )
    )
  })
  
  observeEvent(input$btn_pausar_execucao, {
    pausar_ga(TRUE)
    benchmark_pausado(TRUE)
    tryCatch(session$sendCustomMessage("update_benchmark_widget", list(
      pct = benchmark_pct(),
      detail = paste0("⏸️ [PAUSADO] ", benchmark_msg()),
      status = "paused"
    )), error = function(e) {})
    showNotification("⏸️ Otimização PAUSADA! Clique em '▶️ Retomar' quando desejar continuar.", type = "warning", duration = 4)
  }, ignoreInit = TRUE)
  
  observeEvent(input$btn_retomar_execucao, {
    pausar_ga(FALSE)
    benchmark_pausado(FALSE)
    tryCatch(session$sendCustomMessage("update_benchmark_widget", list(
      pct = benchmark_pct(),
      detail = benchmark_msg(),
      status = "running"
    )), error = function(e) {})
    showNotification("▶️ Otimização RETOMADA com sucesso!", type = "message", duration = 4)
  }, ignoreInit = TRUE)
  
  observeEvent(input$btn_cancelar_execucao, {
    cancelar_ga()
    tryCatch(session$sendCustomMessage("update_benchmark_widget", list(
      pct = benchmark_pct(),
      detail = "⏹️ Cancelando execução e salvando melhor resultado...",
      status = "paused"
    )), error = function(e) {})
    showNotification("⏹️ Interrupção solicitada! Consolidando e salvando o melhor resultado encontrado até o momento...", type = "error", duration = 6)
  }, ignoreInit = TRUE)
  
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
  
  executar_benchmark_completo <- function(modo_esn = "ga_producao",
                                         ga_generations = 10000,
                                         ga_pop_size = 10,
                                         ga_run_stop = 3500,
                                         ga_win = c("GED"),
                                         ga_w = c("Normal"),
                                         ga_anti_estag = TRUE,
                                         epochs_dl = 80, 
                                         timesteps_dl = 10) {
    if (is.null(dados())) {
      showNotification("❌ Carregue os dados da PETR4 antes de iniciar o benchmark!", type = "error")
      return()
    }
    
    d <- dados()
    
    safe_set_rv <- function(rv, val) {
      tryCatch({
        if (!is.null(session) && !session$isClosed()) rv(val)
      }, error = function(e) {})
    }
    
    # Inicializar controle ao vivo
    resetar_controle_ga()
    safe_set_rv(benchmark_ativo, TRUE)
    safe_set_rv(benchmark_pausado, FALSE)
    safe_set_rv(benchmark_pct, 1)
    safe_set_rv(benchmark_msg, "Inicializando benchmark unificado...")
    tryCatch(session$sendCustomMessage("show_benchmark_widget", list()), error = function(e) {})
    
    on.exit({
      safe_set_rv(benchmark_ativo, FALSE)
      safe_set_rv(benchmark_pausado, FALSE)
      resetar_controle_ga()
      tryCatch(session$sendCustomMessage("hide_benchmark_widget", list()), error = function(e) {})
    }, add = TRUE)
    
    withProgress(message = "⚡ Benchmark Unificado em Andamento...", value = 0, {
      # 1. ESN
      if (modo_esn != "preset") {
        # Gerar todas as combinações selecionadas de Win e W
        grade_comb <- expand.grid(win = ga_win, w = ga_w, stringsAsFactors = FALSE)
        n_comb <- nrow(grade_comb)
        
        resultados_ga_lista <- list()
        melhor_res_esn <- NULL
        melhor_fitness <- -Inf
        
        for (k in 1:n_comb) {
          if (isTRUE(obter_status_controle_ga()$cancelar)) break
          if (!is.null(session) && session$isClosed()) {
            cancelar_ga()
            break
          }
          
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
            pop_size = ga_pop_size,
            run_stop = ga_run_stop,
            anti_estagnacao = ga_anti_estag,
            session = session,
            set_progress = function(val, msg) {
              prog_total <- pct_base + val * pct_amplitude
              pct_int <- min(99, max(1, round(prog_total * 100)))
              safe_set_rv(benchmark_pct, pct_int)
              detalhe_msg <- sprintf("[Etapa 1/3: ESN GA %d/%d — %s+%s] %s", k, n_comb, atual_win, atual_w, msg)
              safe_set_rv(benchmark_msg, detalhe_msg)
              
              tryCatch(session$sendCustomMessage("update_benchmark_widget", list(
                pct = pct_int,
                detail = detalhe_msg,
                status = if (benchmark_pausado()) "paused" else "running"
              )), error = function(e) {})
              
              setProgress(
                value = prog_total,
                message = sprintf("⚡ Benchmark [Total: %.0f%%]", prog_total * 100),
                detail = detalhe_msg
              )
            }
          )
          
          resultados_ga_lista[[k]] <- res_ga_k
          
          if (!is.null(res_ga_k$fitness) && res_ga_k$fitness > melhor_fitness) {
            melhor_fitness <- res_ga_k$fitness
            melhor_res_esn <- res_ga_k
          }
          
          if (isTRUE(res_ga_k$cancelado) || isTRUE(obter_status_controle_ga()$cancelar)) {
            showNotification("⏹️ Execução interrompida pelo usuário! Consolidando os melhores modelos...", type = "warning", duration = 8)
            break
          }
        }
        
        res_esn <- if (!is.null(melhor_res_esn)) melhor_res_esn else resultados_ga_lista[[1]]
        if (!is.null(res_esn)) {
          res_esn$todas_combinacoes <- resultados_ga_lista
        }
      } else {
        safe_set_rv(benchmark_pct, 15)
        safe_set_rv(benchmark_msg, "[Etapa 1/3: ESN Preset] Executando inferência com pesos ótimos do TCC...")
        setProgress(0.15, message = "⚡ Benchmark [Total: 15%]", detail = "[Etapa 1/3: ESN Preset] Executando ESN com parâmetros ótimos do TCC...")
        res_esn <- executar_modelo_esn(
          dados = d, 
          cenario_id = "9220_GED_Normal_15", 
          set_progress = function(val, msg) {
            prog_total <- 0.10 + val * 0.40
            pct_int <- min(99, max(10, round(prog_total * 100)))
            safe_set_rv(benchmark_pct, pct_int)
            safe_set_rv(benchmark_msg, paste0("[Etapa 1/3: ESN Preset] ", msg))
            tryCatch(session$sendCustomMessage("update_benchmark_widget", list(
              pct = pct_int,
              detail = paste0("[Etapa 1/3: ESN Preset] ", msg),
              status = "running"
            )), error = function(e) {})
            setProgress(
              value = prog_total,
              message = sprintf("⚡ Benchmark [Total: %.0f%%]", prog_total * 100),
              detail = paste0("[Etapa 1/3: ESN Preset] ", msg)
            )
          }
        )
      }
      
      if (!is.null(res_esn)) {
        tryCatch(resultado_esn_externo(res_esn), error = function(e) {})
      }
      
      # 2. LSTM (50% a 75%) — apenas se não cancelado
      if (!isTRUE(obter_status_controle_ga()$cancelar) && (!is.null(session) && !session$isClosed())) {
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
            pct_int <- min(99, max(50, round(prog_total * 100)))
            safe_set_rv(benchmark_pct, pct_int)
            detalhe_msg <- sprintf("[Etapa 2/3: LSTM (%d épocas)] %s", epochs_dl, msg)
            safe_set_rv(benchmark_msg, detalhe_msg)
            tryCatch(session$sendCustomMessage("update_benchmark_widget", list(
              pct = pct_int,
              detail = detalhe_msg,
              status = "running"
            )), error = function(e) {})
            setProgress(
              value = prog_total,
              message = sprintf("⚡ Benchmark [Total: %.0f%%]", prog_total * 100),
              detail = detalhe_msg
            )
          }
        )
        tryCatch(resultado_lstm_externo(res_lstm), error = function(e) {})
      }
      
      # 3. GRU (75% a 98%) — apenas se não cancelado
      if (!isTRUE(obter_status_controle_ga()$cancelar) && (!is.null(session) && !session$isClosed())) {
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
            pct_int <- min(99, max(75, round(prog_total * 100)))
            safe_set_rv(benchmark_pct, pct_int)
            detalhe_msg <- sprintf("[Etapa 3/3: GRU (%d épocas)] %s", epochs_dl, msg)
            safe_set_rv(benchmark_msg, detalhe_msg)
            tryCatch(session$sendCustomMessage("update_benchmark_widget", list(
              pct = pct_int,
              detail = detalhe_msg,
              status = "running"
            )), error = function(e) {})
            setProgress(
              value = prog_total,
              message = sprintf("⚡ Benchmark [Total: %.0f%%]", prog_total * 100),
              detail = detalhe_msg
            )
          }
        )
        tryCatch(resultado_gru_externo(res_gru), error = function(e) {})
      }
      
      safe_set_rv(benchmark_pct, 100)
      safe_set_rv(benchmark_msg, "Consolidando gráficos, comparativo e recordes...")
      tryCatch(session$sendCustomMessage("update_benchmark_widget", list(
        pct = 100,
        detail = "Consolidando gráficos e comparativo...",
        status = "running"
      )), error = function(e) {})
      setProgress(1.0, message = "⚡ Benchmark [Total: 100%]", detail = "Consolidando gráficos e comparativo...")
    })
    
    updateNavbarPage(session, "main_navbar", selected = "tab_comparacao")
    
    if (modo_esn != "preset") {
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
      size = "l",
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
        
        radioButtons("tipo_execucao_esn", "Modo de Otimização da ESN:",
                     choices = c(
                       "🏆 Opção A — Produção Completa (Padrão TCC Oficial — 10.000 Gerações, Parada run=3.500)" = "ga_producao",
                       "🔬 Opção B — Otimização Rápida de Demonstração (60 a 200 Gerações — ~30s a 2min)" = "ga_rapido",
                       "⚙️ Opção C — GA Personalizado (Escolha Gerações, População e Parada)" = "ga_custom",
                       "⚡ Opção D — Preset Histórico Instantâneo (~5s — Melhores Pesos TCC)" = "preset"
                     ),
                     selected = "ga_producao"),
        
        conditionalPanel(
          condition = "input.tipo_execucao_esn != 'preset'",
          div(style = "background: #f0fdf4; border: 1px solid #bbf7d0; padding: 16px; border-radius: 10px; margin: 12px 0;",
            h5(style = "margin: 0 0 10px 0; color: #166534; font-weight: 800;", "🧬 Configuração das Distribuições Estocásticas:"),
            
            # Atalhos Rápidos por Onda
            div(style = "margin-bottom: 12px;",
              span(style = "font-size: 0.82rem; font-weight: 700; color: #166534; display: block; margin-bottom: 6px;", "⚡ Atalhos de Seleção por Onda Estratégica:"),
              div(style = "display: flex; gap: 6px; flex-wrap: wrap;",
                actionButton("btn_modal_ga_preset_tcc", "⚡ 4 Cenários TCC", class = "btn-default btn-xs", style = "font-size: 0.78rem; font-weight: 600;"),
                actionButton("btn_modal_ga_onda1", "🌊 Onda 1: Caudas Pesadas", class = "btn-default btn-xs", style = "font-size: 0.78rem; font-weight: 600; background: #e0f2fe; color: #0369a1;"),
                actionButton("btn_modal_ga_onda2", "🌊 Onda 2: Shocks & Assimetrias", class = "btn-default btn-xs", style = "font-size: 0.78rem; font-weight: 600; background: #fef3c7; color: #b45309;"),
                actionButton("btn_modal_ga_onda3", "🌊 Onda 3: Esparsidade & Snedecor", class = "btn-default btn-xs", style = "font-size: 0.78rem; font-weight: 600; background: #f3e8ff; color: #7e22ce;"),
                actionButton("btn_modal_ga_onda4", "🌊 Onda 4: Híbridos", class = "btn-default btn-xs", style = "font-size: 0.78rem; font-weight: 600; background: #fae8ff; color: #a21caf;"),
                actionButton("btn_modal_ga_all_win", "+ Todos Win", class = "btn-default btn-xs", style = "font-size: 0.78rem;"),
                actionButton("btn_modal_ga_all_w", "+ Todos W", class = "btn-default btn-xs", style = "font-size: 0.78rem;")
              )
            ),
            
            fluidRow(
              column(6, 
                selectizeInput("modal_ga_win", "Distribuição(ões) Win (Entrada):", 
                               choices = c("GED", "Normal", "Uniforme", "t de Student", "t de Student Assimétrica", "Cauchy", "Pearson V", "Laplace", "Normal Esparsa"), 
                               selected = c("GED"), 
                               multiple = TRUE,
                               options = list(plugins = list('remove_button'), placeholder = 'Selecione uma ou mais...'))
              ),
              column(6, 
                selectizeInput("modal_ga_w", "Distribuição(ões) W (Reservatório):", 
                               choices = c("Normal", "Uniforme", "GED", "t de Student", "t de Student Assimétrica", "Cauchy", "Laplace", "Normal Esparsa", "F de Snedecor"), 
                               selected = c("Normal"), 
                               multiple = TRUE,
                               options = list(plugins = list('remove_button'), placeholder = 'Selecione uma ou mais...'))
              )
            ),
            
            uiOutput("modal_ga_combinations_info"),
            
            conditionalPanel(
              condition = "input.tipo_execucao_esn == 'ga_producao'",
              div(style = "background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 8px; padding: 10px 14px; font-size: 0.88rem; color: #1e40af; margin-top: 8px;",
                  strong("🏆 Modo de Produção Oficial TCC: "), 
                  "Executa até 10.000 gerações com população de 10 indivíduos e critério de parada automático se ficar 3.500 iterações sem melhora (run=3500).")
            ),
            
            conditionalPanel(
              condition = "input.tipo_execucao_esn == 'ga_rapido'",
              sliderInput("modal_ga_generations_rapido", "Número de Gerações GA (Demonstração):", min = 20, max = 500, value = 80, step = 20)
            ),
            
            conditionalPanel(
              condition = "input.tipo_execucao_esn == 'ga_custom'",
              fluidRow(
                column(4, sliderInput("modal_ga_generations_custom", "Gerações Máximas:", min = 100, max = 15000, value = 5000, step = 500)),
                column(4, sliderInput("modal_ga_pop_custom", "Tamanho População:", min = 6, max = 50, value = 10, step = 2)),
                column(4, sliderInput("modal_ga_run_custom", "Parada sem Melhora (run):", min = 100, max = 5000, value = 1500, step = 100))
              )
            ),
            
            checkboxInput("modal_ga_anti_estag", "Ativar Exploração Anti-Estagnação por Cataclismo (Hipermutação Adaptativa)", value = TRUE)
          )
        ),
        
        hr(),
        radioButtons("perfil_dl", "Perfil de Treinamento Deep Learning (LSTM / GRU):",
                     choices = c(
                       "⚡ DL Rápido (25 épocas — Duração: ~15s)" = "rapido",
                       "🏆 DL Produção (80 épocas — Duração: ~40s)" = "producao",
                       "⚙️ DL Personalizado" = "custom"
                     ),
                     selected = "producao"),
        conditionalPanel(
          condition = "input.perfil_dl == 'custom'",
          sliderInput("custom_epochs", "Épocas para LSTM e GRU:", min = 10, max = 200, value = 80, step = 10),
          sliderInput("custom_timesteps", "Janela Temporal (Timesteps):", min = 5, max = 30, value = 10, step = 5)
        ),
        div(style = "background: #f8fafc; padding: 12px; border-radius: 8px; font-size: 0.85rem; color: #64748b; border: 1px solid #e2e8f0; margin-top: 12px;",
            "💡 Todos os resultados do GA serão gravados no arquivo persistente historico_otimizacoes_ga.csv e comparados com o recorde histórico global!")
      )
    ))
  })
  
  # Ações rápidas dos botões no Modal
  observeEvent(input$btn_modal_ga_preset_tcc, {
    updateSelectizeInput(session, "modal_ga_win", selected = c("GED", "Normal", "Uniforme"))
    updateSelectizeInput(session, "modal_ga_w", selected = c("Normal", "Uniforme"))
  })
  
  observeEvent(input$btn_modal_ga_onda1, {
    updateSelectizeInput(session, "modal_ga_win", selected = c("Pearson V", "t de Student", "Laplace"))
    updateSelectizeInput(session, "modal_ga_w", selected = c("Normal", "Uniforme", "t de Student"))
  })
  
  observeEvent(input$btn_modal_ga_onda2, {
    updateSelectizeInput(session, "modal_ga_win", selected = c("Cauchy", "t de Student Assimétrica", "Laplace"))
    updateSelectizeInput(session, "modal_ga_w", selected = c("Normal", "Cauchy", "Laplace"))
  })
  
  observeEvent(input$btn_modal_ga_onda3, {
    updateSelectizeInput(session, "modal_ga_win", selected = c("Normal Esparsa", "GED"))
    updateSelectizeInput(session, "modal_ga_w", selected = c("Normal Esparsa", "F de Snedecor", "GED"))
  })
  
  observeEvent(input$btn_modal_ga_onda4, {
    updateSelectizeInput(session, "modal_ga_win", selected = c("Normal", "Uniforme", "Normal Esparsa"))
    updateSelectizeInput(session, "modal_ga_w", selected = c("Uniforme", "Normal"))
  })
  
  observeEvent(input$btn_modal_ga_all_win, {
    updateSelectizeInput(session, "modal_ga_win", selected = c("GED", "Normal", "Uniforme", "t de Student", "t de Student Assimétrica", "Cauchy", "Pearson V", "Laplace", "Normal Esparsa"))
  })
  
  observeEvent(input$btn_modal_ga_all_w, {
    updateSelectizeInput(session, "modal_ga_w", selected = c("Normal", "Uniforme", "GED", "t de Student", "t de Student Assimétrica", "Cauchy", "Laplace", "Normal Esparsa", "F de Snedecor"))
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
    
    tipo <- input$tipo_execucao_esn
    
    ga_gen <- switch(tipo,
                     "ga_producao" = 10000,
                     "ga_rapido"   = input$modal_ga_generations_rapido,
                     "ga_custom"   = input$modal_ga_generations_custom,
                     60)
    
    ga_pop <- switch(tipo,
                    "ga_producao" = 10,
                    "ga_rapido"   = 12,
                    "ga_custom"   = input$modal_ga_pop_custom,
                    10)
                    
    ga_run <- switch(tipo,
                    "ga_producao" = 3500,
                    "ga_rapido"   = input$modal_ga_generations_rapido,
                    "ga_custom"   = input$modal_ga_run_custom,
                    3500)
    
    ga_win <- if (tipo != "preset") {
      if (is.null(input$modal_ga_win) || length(input$modal_ga_win) == 0) c("GED") else input$modal_ga_win
    } else "GED"
    
    ga_w <- if (tipo != "preset") {
      if (is.null(input$modal_ga_w) || length(input$modal_ga_w) == 0) c("Normal") else input$modal_ga_w
    } else "Normal"
    
    ga_anti <- if (tipo != "preset") input$modal_ga_anti_estag else TRUE
    
    ep <- switch(input$perfil_dl,
                 "rapido" = 25,
                 "producao" = 80,
                 "custom" = input$custom_epochs)
    ts <- if (input$perfil_dl == "custom") input$custom_timesteps else 10
    
    executar_benchmark_completo(
      modo_esn = tipo,
      ga_generations = ga_gen,
      ga_pop_size = ga_pop,
      ga_run_stop = ga_run,
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
