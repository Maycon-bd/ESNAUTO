# =============================================================================
# mod_esn.R — Módulo ESN (Echo State Network) para Shiny
# Baseado em: ESN Acoes-petr4 v2.8.1.2 Maycon G Silva.R
# Suporta Otimização Live por Algoritmo Genético (GA) e Histórico em CSV
# =============================================================================

# Carregar utilitários
source("utils/data_prep.R", local = TRUE)
source("utils/metrics.R", local = TRUE)
source("utils/esn_core.R", local = TRUE)
source("utils/history_tracker.R", local = TRUE)
source("utils/ga_engine.R", local = TRUE)

# =============================================================================
# CENÁRIOS PRÉ-OTIMIZADOS (extraídos do código original)
# =============================================================================

criar_cenarios_pre_otimizados <- function() {
  cenarios <- list()
  
  # --- Cenário 1: Run 10000_1, Win GED + W Normal, tam_reservoir=15 ---
  cenarios[["9220_GED_Normal_15"]] <- list(
    nome = "Run 9220 | Win GED | W Normal | Reservatório=15",
    a = 0.926230821463176,
    sr = 0.642384661748213,
    initLen = 8,
    tam_reservoir = 15,
    reg = 7.05304479452055e-5,
    dist_win = "GED",
    dist_w = "Normal",
    Win = matrix(nrow = 15, ncol = 2, c(
      23.8286867301219, 22.4774576127917, 20.137075934452, 10.847853681893, 22.2399796703719,
      19.3539696610378, 21.4438801194363, 25.0486196609061, 2.34994991185052, 13.727298132811,
      11.7019238511075, 22.4658697689091, 6.40210724749221, 16.5860217383057, 16.0964937029461,
      28.5150792598598, -0.62785271777741, 26.4983446916728, 11.3542536470011, 7.96905393969021,
      3.25133304555825, 27.0253828824319, 7.80240259855172, 22.5794404626722, 12.4584294249808,
      8.4270479971493, 19.1529332579111, 20.6835014320524, -0.963910718562021, 24.183662141808)),
    W = matrix(nrow = 15, ncol = 15, c(
      -0.0605578027386505, 0.0613606233447933, -0.108692177280012, -0.146118401859457, -0.104668593402887,
      0.0931393976224093, -0.196125216421737, 0.199516288619675, -0.149144246241641, 0.240076793045162,
      -0.31373343697169, -0.252344907593781, -0.0417714038253541, 0.0268083525527564, -0.105520093493446,
      -0.0594530357925119, -0.150491379100068, 0.282687430160602, -0.0834665207232748, 0.088965206518118,
      -0.0335701947086064, -0.124696796017321, -0.0345479866499681, 0.125941167711635, 0.122789346644619,
      -0.0300511088808818, -0.107262337086775, -0.107500332745508, -0.0740638968920839, 0.0867402457592548,
      0.139392475540952, -0.166967255069514, -0.0274290373966007, -0.0617772851779337, -0.171465955266278,
      -0.141565042806367, -0.0564615261389467, 0.0786758681885605, -0.189035387252306, 0.114766835927005,
      -0.207910138226126, 0.178368225906427, -0.0236086063240226, -0.0721756990621309, -0.0521044608660359,
      0.207742975754988, 0.146147716556039, -0.0109507190521363, 0.2253489210143, 0.175605811748501,
      0.0287666699405999, 0.031651228164254, 0.147851233053217, -0.0109401904072624, 0.0270523474265416,
      0.279589242263415, 0.0560802339246532, -0.0571999167186198, 0.0480295457498267, -0.00712236102546574,
      0.128896666418112, 0.0213902689563876, 0.0389252379594335, 0.0820219776195539, -0.0894563820294327,
      -0.00768870815808686, 0.00885286318124391, -0.174127311350024, -0.128175557533053, 0.442004023611293,
      0.29921019846169, -0.0957418354085728, -0.302107494350921, -0.246208629483895, 0.0224395858606767,
      -0.338130372482041, -0.0665621993238663, 0.0699285328416198, 0.227252631302676, -0.41824338574719,
      -0.189554356521799, -0.108592726485719, -0.350475812352884, -0.0144884258604386, -0.253613936275334,
      0.120262738998331, -0.0344940672710521, 0.0800680639376176, -0.13465639682736, 0.152271211405007,
      0.136039043160873, -0.0648068474363471, -0.0415221384457807, -0.0687131896646887, -0.129641758707413,
      0.0915414819135286, 0.071083520941652, 0.0670647820836911, -0.203971124609106, 0.17530556780431,
      -0.0981834464736943, 0.188817526161609, 0.00503067586114325, -0.239610508215445, 0.219920671461572,
      0.143153487656889, -0.0251161906276346, 0.145711655959611, 0.0894339330182637, -0.341240294583937,
      -0.162391309739654, -0.286317493789089, 0.00623808256993354, 0.02216909447318, -0.0429351282749543,
      -0.0124480048837041, 0.155096967344624, 0.2583667839895, 0.0674561852675031, 0.0665180067246987,
      -0.0124900737937065, 0.138034761161821, 0.291436908003999, 0.163490854040274, -0.0476141559133726,
      -0.0094051272230872, -0.199213318238398, -0.109514619644921, 0.0408437473516281, 0.0443523730480857,
      0.0924732101700962, 0.00514612137927645, -0.332399053489197, 0.126147706969379, -0.0986108851351968,
      -0.150672254371928, 0.16110355202604, -0.257120084490043, -0.128263664630006, -0.032794762859908,
      0.0721063460316991, 0.0255039558182129, 0.171900571237003, -0.0742504497947241, -0.251079259435687,
      -0.210347823481703, -0.10308429458622, -0.176019239900964, 0.139410889290823, -0.309641884196467,
      0.0479255897435308, 0.15930944066402, 0.222125232323247, 0.0953543582561722, 0.0511010997553698,
      -0.186554813082587, -0.0104136791100989, -0.193446304541751, -0.00887897800955654, -0.107143122624087,
      0.0181970577879041, 0.0904291618578397, -0.0067953620976761, -0.168999598332065, -0.0263959259818122,
      0.0838266221979811, -0.0335416279324124, -0.150634756609104, 0.0228041134481417, -0.0838536036244564,
      -0.0905032439288794, -0.376789201528017, 0.0103807943623318, -0.0801659559095068, 0.43074437596383,
      -0.306887178668079, 0.36910354182698, 0.0129520244510901, -0.0844416680698095, -0.0581238732941944,
      -0.0859155919765276, -0.0319352595923491, -0.141238772933404, -0.0199315623497406, 0.182649530538737,
      -0.100199520807889, 0.120329094464645, -0.199649051195628, -0.0261477231551985, -0.129899285040569,
      -0.0366301667163647, -0.0997198327664473, -0.111549338320662, 0.113821729176482, 0.153604107029243,
      -0.0403517624613573, 0.129691531401488, 0.0183857546774572, 0.206385321687794, 0.0766013364291768,
      -0.247289756761986, -0.350160317972371, 0.00495602030341325, 0.197865601913143, 0.315738590241367,
      0.0974145541693093, 0.0181751699063103, 0.0448112710522807, 0.102508096486815, -0.0796952041939838,
      0.100678546495824, 0.0737132809984029, 0.0776312058440861, -0.0575848180407413, -0.306182966035017,
      -0.132573963544067, 0.0911986475010883, 0.218012308041569, 0.0762936459550168, -0.0264959975026127,
      -0.0839407813964129, -0.014696538241568, -0.297229467524563, -0.156310996707144, 0.110439082156438)),
    Wout = matrix(nrow = 1, ncol = 17, c(
      -0.234560750424862, 1.000500792519, -0.234560750424862, 3.27989162095946,
      -0.234560839831829, -0.234560631215572, -0.234560750424862, -0.234560690820217,
      -0.234560690820217, -0.234560750424862, -0.23456072062254, -0.234560705721378,
      -0.234560675919056, -0.234560810029507, -0.234560806304216, 0.0115933330581974,
      -0.234560787677765))
  )
  
  # --- Cenário 2: MELHOR — Run 2563, Win GED + W Normal, tam_reservoir=27 ---
  cenarios[["2563_GED_Normal_27"]] <- list(
    nome = "★ MELHOR: Run 2563 | Win GED | W Normal | Reservatório=27",
    a = 0.870902030197374,
    sr = 0.406802420062409,
    initLen = 9,
    tam_reservoir = 27,
    reg = 2.2289743444227e-05,
    dist_win = "GED",
    dist_w = "Normal",
    Win = matrix(nrow = 27, ncol = 2, c(
      9.77227059626767, 21.9406967182875, 7.56098533994042, 16.3427300152356, 20.5227110728847,
      16.7502082492526, 25.3271232653089, 20.8815145270364, 27.3411246269884, -3.12756182997085,
      22.3881181164667, 10.8018698732015, 8.47396701430825, 6.2030008252043, 14.4037951773676,
      19.9210735696691, -0.721022433098833, 20.7171838453202, 12.3480840628286, 4.68081118580138,
      25.6696599730835, 22.4333858836393, 19.5231982340921, 10.3402217853663, 20.288808571131,
      15.3022949236274, 22.5870113330856,
      21.0608352530002, -0.608163163607692, 4.87984703659724, 25.6157756006469, 20.524944436405,
      13.1767258231873, 18.0568801406273, 14.1624523561748, 25.2928179349979, 2.09587370676452,
      25.0578452770533, 27.7599742514216, 16.4529483605758, 15.5440579294674, 13.7353968506056,
      16.749572323559, 17.9452141402836, 25.8668954545981, -0.95742681487415, 20.9284525176176,
      8.11888901413491, 28.4362512908884, 20.2032578713083, 1.39732762135297, -1.31661481111454,
      6.72050438063485, 4.16973383732967)),
    W = NULL,
    Wout = matrix(nrow = 1, ncol = 29, c(
      0.058057114481926, 1.0010269188183, 0.058059349656105, 1.47258765713951,
      0.0580595061182976, 0.0580593273043633, 0.0580594465136528, 0.0580596253275871,
      0.0580596253275871, 0.0580595433712006, 0.0580596253275871, -2.87848351965658,
      0.0580594837665558, 0.0580592751502991, 0.0580597519874573, 0.0580596178770065,
      0.0580593794584274, 0.0580594539642334, 0.0580596327781677, 0.0580594539642334,
      -0.0031974782866584, 0.0580597966909409, 0.0580594688653946, 0.0580596774816513,
      0.0580585524439812, 0.0580595508217812, 0.019107758673556,
      0.0580587759613991, 0.0580587387084961))
  )
  
  # --- Cenário 3: Run 4943, Win Normal + W Normal, tam_reservoir=3 ---
  cenarios[["4943_Normal_Normal_3"]] <- list(
    nome = "Run 4943 | Win Normal | W Normal | Reservatório=3",
    a = 0.774015609860305,
    sr = 0.279199822996696,
    initLen = 19,
    tam_reservoir = 3,
    reg = 3.56576495107632e-5,
    dist_win = "Normal",
    dist_w = "Normal",
    Win = matrix(nrow = 3, ncol = 2, c(
      0.364242033841954, 1.49111727680063, -0.579628748641589,
      -0.0059982963110041, -0.0900987970699551, -0.744462167076191)),
    W = matrix(nrow = 3, ncol = 3, c(
      -0.0289452346432446, 0.0556342361500467, -0.063152597232525,
      -0.0253346917687517, -0.275236350594416, -0.017321638865367,
       0.10817939987002, -0.115372944330111, 0.038073032068389)),
    Wout = matrix(nrow = 1, ncol = 5, c(
      -12.7763519119471, 1.24875741361757, 42.4309823848307,
       1.16381403038395, -2.23999445140362))
  )
  
  cenarios
}

# =============================================================================
# FUNÇÕES CORE DA ESN
# =============================================================================

esn_validacao <- function(dados_split, params, Win, W, Wout = NULL) {
  treino <- dados_split$idx$treino_n
  valida <- dados_split$idx$valida_n
  treino_valida <- dados_split$treino_valida
  
  a <- params$a
  sr <- params$sr
  initLen <- params$initLen
  tam_reservoir <- params$tam_reservoir
  reg <- params$reg
  
  inSize <- 1
  outSize <- 1
  
  t_inicio <- proc.time()
  
  rhoW <- abs(eigen(W, only.values = TRUE)$values[1])
  if (is.na(rhoW) || rhoW == 0) rhoW <- 1
  W_scaled <- sr * W / rhoW
  
  X <- matrix(0, 1 + inSize + tam_reservoir, treino - initLen)
  Yt <- matrix(treino_valida[(initLen + 2):(treino + 1)], 1)
  x <- rep(0, tam_reservoir)
  
  for (t in 1:treino) {
    u <- treino_valida[t]
    x <- (1 - a) * x + a * tanh(Win %*% rbind(1, u) + W_scaled %*% x)
    if (t > initLen)
      X[, t - initLen] <- rbind(1, u, x)
  }
  
  if (is.null(Wout)) {
    X_T <- t(X)
    Wout <- tryCatch({
      Yt %*% X_T %*% solve(X %*% X_T + reg * diag(1 + inSize + tam_reservoir))
    }, error = function(e) {
      Yt %*% X_T %*% pracma::pinv(X %*% X_T + reg * diag(1 + inSize + tam_reservoir))
    })
  }
  
  # Previsão validação
  Y <- matrix(0, outSize, valida)
  u <- treino_valida[treino + 1]
  
  for (t in 1:valida) {
    x <- (1 - a) * x + a * tanh(Win %*% rbind(1, u) + W_scaled %*% x)
    y <- Wout %*% rbind(1, u, x)
    Y[, t] <- y
    u <- treino_valida[treino + t + 1]
  }
  
  # Previsão treino
  Ytr <- matrix(0, outSize, treino)
  u <- treino_valida[1]
  
  for (j in 1:treino) {
    x <- (1 - a) * x + a * tanh(Win %*% rbind(1, u) + W_scaled %*% x)
    y <- Wout %*% rbind(1, u, x)
    Ytr[, j] <- y
    u <- treino_valida[j + 1]
  }
  
  t_fim <- proc.time()
  tempo_exec <- (t_fim - t_inicio)["elapsed"]
  
  real_valida <- treino_valida[(treino + 2):(treino + valida)]
  prev_valida <- as.numeric(Y[outSize, 1:(valida - 1)])
  
  real_treino <- treino_valida[2:treino]
  prev_treino <- as.numeric(Ytr[outSize, 1:(treino - 1)])
  
  metricas_treino <- calcular_todas_metricas(real_treino, prev_treino, tempo_exec)
  metricas_valida <- calcular_todas_metricas(real_valida, prev_valida, tempo_exec)
  
  list(
    previsao_valida = as.numeric(Y),
    previsao_treino = as.numeric(Ytr),
    Wout = Wout,
    metricas_treino = metricas_treino,
    metricas_valida = metricas_valida,
    tempo = tempo_exec
  )
}

esn_teste <- function(dados_split, params, Win, W, Wout) {
  treino_n <- dados_split$idx$treino_n
  teste_n <- dados_split$idx$teste_n
  treina_testa <- dados_split$treina_testa
  
  a <- params$a
  sr <- params$sr
  initLen <- params$initLen
  tam_reservoir <- params$tam_reservoir
  
  inSize <- 1
  outSize <- 1
  
  t_inicio <- proc.time()
  
  rhoW <- abs(eigen(W, only.values = TRUE)$values[1])
  if (is.na(rhoW) || rhoW == 0) rhoW <- 1
  W_scaled <- sr * W / rhoW
  
  X <- matrix(0, 1 + inSize + tam_reservoir, treino_n - initLen)
  Yt <- matrix(treina_testa[(initLen + 2):(treino_n + 1)], 1)
  x <- rep(0, tam_reservoir)
  
  for (t in 1:treino_n) {
    u <- treina_testa[t]
    x <- (1 - a) * x + a * tanh(Win %*% rbind(1, u) + W_scaled %*% x)
    if (t > initLen)
      X[, t - initLen] <- rbind(1, u, x)
  }
  
  # Previsão teste
  Y <- matrix(0, outSize, teste_n)
  u <- treina_testa[treino_n + 1]
  
  for (t in 1:teste_n) {
    x <- (1 - a) * x + a * tanh(Win %*% rbind(1, u) + W_scaled %*% x)
    y <- Wout %*% rbind(1, u, x)
    Y[, t] <- y
    u <- treina_testa[treino_n + t + 1]
  }
  
  # Previsão treino
  Ytr <- matrix(0, outSize, treino_n)
  u <- treina_testa[1]
  
  for (j in 1:treino_n) {
    x <- (1 - a) * x + a * tanh(Win %*% rbind(1, u) + W_scaled %*% x)
    y <- Wout %*% rbind(1, u, x)
    Ytr[, j] <- y
    u <- treina_testa[j + 1]
  }
  
  t_fim <- proc.time()
  tempo_exec <- (t_fim - t_inicio)["elapsed"]
  
  real_teste <- treina_testa[(treino_n + 2):(treino_n + teste_n)]
  prev_teste <- as.numeric(Y[outSize, 1:(teste_n - 1)])
  
  real_treino <- treina_testa[2:treino_n]
  prev_treino <- as.numeric(Ytr[outSize, 1:(treino_n - 1)])
  
  metricas_treino <- calcular_todas_metricas(real_treino, prev_treino, tempo_exec)
  metricas_teste <- calcular_todas_metricas(real_teste, prev_teste, tempo_exec)
  
  list(
    previsao_teste = as.numeric(Y),
    previsao_treino = as.numeric(Ytr),
    metricas_treino = metricas_treino,
    metricas_teste = metricas_teste,
    tempo = tempo_exec
  )
}

# =============================================================================
# FUNÇÃO CENTRAL DE EXECUÇÃO ESN (reutilizável)
# =============================================================================

executar_modelo_esn <- function(dados, cenario_id = "9220_GED_Normal_15", set_progress = NULL) {
  dados_split <- dividir_dados(dados)
  cenarios <- criar_cenarios_pre_otimizados()
  cen <- cenarios[[cenario_id]]
  if (is.null(cen) || is.null(cen$W)) {
    cen <- cenarios[["9220_GED_Normal_15"]]
  }
  
  params <- list(
    a = cen$a, sr = cen$sr, initLen = cen$initLen,
    tam_reservoir = cen$tam_reservoir, reg = cen$reg
  )
  
  if (is.function(set_progress)) set_progress(0.3, "Calculando Validação da ESN...")
  res_val <- esn_validacao(dados_split, params, cen$Win, cen$W, cen$Wout)
  
  if (is.function(set_progress)) set_progress(0.6, "Calculando Teste Out-of-Sample da ESN...")
  res_teste <- esn_teste(dados_split, params, cen$Win, cen$W, cen$Wout)
  
  list(
    modelo = "ESN",
    origem = "PRESET",
    validacao = res_val,
    teste = res_teste,
    tempo = res_val$tempo + res_teste$tempo,
    metricas = list(
      modelo = "ESN",
      treino = res_val$metricas_treino,
      validacao = res_val$metricas_valida,
      teste = res_teste$metricas_teste,
      tempo = res_val$tempo + res_teste$tempo
    )
  )
}

# =============================================================================
# UI SHINY DO MÓDULO ESN
# =============================================================================

esn_ui <- function(id) {
  ns <- NS(id)
  
  tagList(
    fluidRow(
      column(4,
        div(class = "well model-card-esn",
          div(class = "section-subtitle", "PARÂMETROS DA REDE"),
          h4(style = "margin-top:0; color: var(--esn-color); font-weight: 800;", "🧠 Echo State Network"),
          hr(),
          
          radioButtons(ns("modo_operacao"), "Modo de Configuração:",
                       choices = c(
                         "🏆 Usar Cenário Pré-Otimizado (GA)" = "preset",
                         "🎲 Distribuições Customizadas (Manual)" = "custom",
                         "🧬 Otimizar ao Vivo com Algoritmo Genético (GA)" = "ga_live"
                       ),
                       selected = "preset"),
          
          conditionalPanel(
            condition = paste0("input['", ns("modo_operacao"), "'] == 'preset'"),
            selectInput(ns("cenario"), "Selecione o Cenário:", choices = NULL)
          ),
          
          conditionalPanel(
            condition = paste0("input['", ns("modo_operacao"), "'] == 'custom'"),
            div(style = "background: var(--bg-app); padding: 14px; border-radius: var(--radius-md); margin-bottom: 14px;",
              h5(style = "margin-top:0; font-weight:700;", "🎲 Distribuições dos Pesos:"),
              selectInput(ns("dist_win"), "Distribuição W_in (Entrada):", choices = NULL),
              selectInput(ns("dist_w"), "Distribuição W (Reservatório):", choices = NULL)
            )
          ),
          
          conditionalPanel(
            condition = paste0("input['", ns("modo_operacao"), "'] == 'ga_live'"),
            div(style = "background: #f0fdf4; border: 1px solid #bbf7d0; padding: 14px; border-radius: var(--radius-md); margin-bottom: 14px;",
              h5(style = "margin-top:0; color: #166534; font-weight: 800;", "🧬 Configuração do GA Live:"),
              selectizeInput(ns("ga_win_dist"), "Distribuição(ões) W_in (Entrada):", 
                             choices = c("GED", "Normal", "Uniforme", "t de Student", "Normal Esparsa", "Cauchy"), 
                             selected = c("GED"), 
                             multiple = TRUE,
                             options = list(plugins = list('remove_button'), placeholder = 'Selecione distribuições...')),
              selectizeInput(ns("ga_w_dist"), "Distribuição(ões) W (Reservatório):", 
                             choices = c("Normal", "Uniforme", "GED", "t de Student", "Normal Esparsa"), 
                             selected = c("Normal"), 
                             multiple = TRUE,
                             options = list(plugins = list('remove_button'), placeholder = 'Selecione distribuições...')),
              div(style = "display: flex; gap: 6px; margin-bottom: 10px; flex-wrap: wrap;",
                actionButton(ns("btn_ga_preset_tcc"), "⚡ 4 Cenários TCC", class = "btn-default btn-xs", style = "font-size: 0.75rem; padding: 2px 6px;"),
                actionButton(ns("btn_ga_all_win"), "+ Todos Win", class = "btn-default btn-xs", style = "font-size: 0.75rem; padding: 2px 6px;"),
                actionButton(ns("btn_ga_all_w"), "+ Todos W", class = "btn-default btn-xs", style = "font-size: 0.75rem; padding: 2px 6px;")
              ),
              uiOutput(ns("ga_live_comb_info")),
              sliderInput(ns("ga_maxiter"), "Número de Gerações:", min = 20, max = 2000, value = 100, step = 20),
              sliderInput(ns("ga_popsize"), "Tamanho da População:", min = 8, max = 40, value = 12, step = 2),
              checkboxInput(ns("ga_anti_estag"), "Mecanismo Anti-Estagnação (Cataclismo)", value = TRUE)
            )
          ),
          
          hr(),
          actionButton(ns("btn_rodar"), "🚀 Executar Modelo ESN", 
                       class = "btn-success btn-block",
                       style = "width:100%; height: 52px; font-size: 1.05rem; font-weight: 800; border-radius: 12px;")
        )
      ),
      column(8,
        div(class = "well",
          tabsetPanel(
            tabPanel("📊 Métricas de Desempenho",
              br(),
              uiOutput(ns("banner_recorde")),
              verbatimTextOutput(ns("resultados_texto")),
              hr(),
              h5(style = "font-weight: 700;", "📋 Tabela de Resumo:"),
              tableOutput(ns("tabela_metricas"))
            ),
            tabPanel("🏆 Comparativo de Distribuições",
              br(),
              h4(style = "font-weight: 800; color: #0f172a;", "🏆 Ranking das Distribuições Testadas nesta Rodada"),
              p(style = "color: var(--text-muted); font-size: 0.9rem;", 
                "Quando múltiplas distribuições são selecionadas, todas as combinações são testadas e comparadas aqui por Fitness e MAE:"),
              uiOutput(ns("painel_comparativo_dists")),
              tableOutput(ns("tabela_comparativo_dists"))
            ),
            tabPanel("📈 Validação (In-sample)",
              br(),
              plotOutput(ns("grafico_validacao"), height = "380px")
            ),
            tabPanel("📉 Teste (Out-of-sample)",
              br(),
              plotOutput(ns("grafico_teste"), height = "380px")
            ),
            tabPanel("📜 Histórico CSV do GA",
              br(),
              div(style = "display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;",
                h4(style = "margin: 0; font-weight: 800;", "📜 Registro Histórico Permanente de Otimizações"),
                actionButton(ns("btn_atualizar_csv"), "🔄 Atualizar Tabela", class = "btn-default", style = "font-size: 0.85rem;")
              ),
              p(style = "color: var(--text-muted); font-size: 0.9rem;", 
                "Cada vez que o GA roda, ele salva uma nova linha no arquivo ", 
                tags$code("historico_otimizacoes_ga.csv"), 
                " e compara com os recordes históricos de todas as rodadas passadas."),
              div(style = "overflow-x: auto; max-height: 420px;",
                tableOutput(ns("tabela_historico_ga"))
              )
            )
          )
        )
      )
    )
  )
}

# =============================================================================
# SERVER SHINY DO MÓDULO ESN
# =============================================================================

esn_server <- function(id, dados_reativo, resultados_externos = NULL) {
  moduleServer(id, function(input, output, session) {
    ns <- session$ns
    cenarios <- criar_cenarios_pre_otimizados()
    
    # Preencher dropdown de cenários
    observe({
      escolhas <- setNames(names(cenarios), sapply(cenarios, function(x) x$nome))
      updateSelectInput(session, "cenario", choices = escolhas, selected = "9220_GED_Normal_15")
    })
    
    # Preencher distribuições disponíveis
    observe({
      dists <- listar_distribuicoes()
      updateSelectInput(session, "dist_win", choices = dists, selected = "GED")
      updateSelectInput(session, "dist_w", choices = dists, selected = "Normal")
    })
    
    # Ações rápidas dos botões de distribuição GA
    observeEvent(input$btn_ga_preset_tcc, {
      updateSelectizeInput(session, "ga_win_dist", selected = c("GED", "Normal", "Uniforme"))
      updateSelectizeInput(session, "ga_w_dist", selected = c("Normal", "Uniforme"))
    })
    
    observeEvent(input$btn_ga_all_win, {
      updateSelectizeInput(session, "ga_win_dist", selected = c("GED", "Normal", "Uniforme", "t de Student", "Normal Esparsa", "Cauchy"))
    })
    
    observeEvent(input$btn_ga_all_w, {
      updateSelectizeInput(session, "ga_w_dist", selected = c("Normal", "Uniforme", "GED", "t de Student", "Normal Esparsa"))
    })
    
    output$ga_live_comb_info <- renderUI({
      n_win <- length(input$ga_win_dist)
      n_w <- length(input$ga_w_dist)
      tot <- max(1, n_win * n_w)
      div(style = "font-size: 0.82rem; color: #166534; font-weight: 700; margin-bottom: 8px;",
          sprintf("📊 %d Combinação(ões) a testar (%d Win × %d W)", tot, n_win, n_w))
    })
    
    # Resultados reativos
    resultados <- reactiveValues(
      validacao = NULL,
      teste = NULL,
      metricas = NULL,
      registro = NULL,
      todas_combinacoes = NULL,
      origem = "PRESET"
    )
    
    # Sincronizar caso receba execução de um botão universal externo
    if (!is.null(resultados_externos)) {
      observe({
        res <- resultados_externos()
        req(res)
        if (identical(res$modelo, "ESN")) {
          resultados$validacao <- res$validacao
          resultados$teste <- res$teste
          resultados$metricas <- res$metricas
          resultados$registro <- res$registro
          resultados$todas_combinacoes <- res$todas_combinacoes
          resultados$origem <- if (!is.null(res$origem)) res$origem else "UNIVERSAL"
        }
      })
    }
    
    # Rodar ESN
    observeEvent(input$btn_rodar, {
      req(dados_reativo())
      dados <- dados_reativo()
      
      if (input$modo_operacao == "ga_live") {
        # Otimização Live por Algoritmo Genético (com suporte a múltiplas distribuições)
        win_list <- if (is.null(input$ga_win_dist) || length(input$ga_win_dist) == 0) c("GED") else input$ga_win_dist
        w_list <- if (is.null(input$ga_w_dist) || length(input$ga_w_dist) == 0) c("Normal") else input$ga_w_dist
        grade_comb <- expand.grid(win = win_list, w = w_list, stringsAsFactors = FALSE)
        n_comb <- nrow(grade_comb)
        
        withProgress(message = "🧬 Otimizando ESN via Algoritmo Genético...", value = 0, {
          melhor_res_ga <- NULL
          melhor_fitness <- -Inf
          lista_resultados_ga <- list()
          
          for (k in 1:n_comb) {
            cur_win <- grade_comb$win[k]
            cur_w <- grade_comb$w[k]
            
            pct_base <- (k - 1) / n_comb
            pct_range <- 1 / n_comb
            
            res_ga_k <- otimizar_esn_ga_live(
              dados = dados,
              win_dist = cur_win,
              w_dist = cur_w,
              maxiter = input$ga_maxiter,
              pop_size = input$ga_popsize,
              anti_estagnacao = input$ga_anti_estag,
              session = session,
              set_progress = function(val, msg) {
                setProgress(pct_base + val * pct_range, 
                            detail = sprintf("[%d/%d] Win: %s + W: %s — %s", k, n_comb, cur_win, cur_w, msg))
              }
            )
            
            lista_resultados_ga[[k]] <- res_ga_k
            
            if (!is.null(res_ga_k$fitness) && res_ga_k$fitness > melhor_fitness) {
              melhor_fitness <- res_ga_k$fitness
              melhor_res_ga <- res_ga_k
            }
            
            if (isTRUE(res_ga_k$cancelado) || isTRUE(obter_status_controle_ga()$cancelar)) {
              showNotification("⏹️ Otimização interrompida pelo usuário! Melhor modelo salvo no histórico.", type = "warning", duration = 8)
              break
            }
          }
          
          resultados$validacao <- melhor_res_ga$validacao
          resultados$teste <- melhor_res_ga$teste
          resultados$registro <- melhor_res_ga$registro
          resultados$origem <- "GA_LIVE"
          resultados$metricas <- melhor_res_ga$metricas
          resultados$todas_combinacoes <- lista_resultados_ga
        })
        
        if (n_comb > 1) {
          showNotification(sprintf("✅ GA finalizado com sucesso para %d combinações! Campeã: Win=%s, W=%s (Fitness: %.4f)", 
                                   n_comb, melhor_res_ga$dist_win, melhor_res_ga$dist_w, melhor_fitness), 
                           type = "message", duration = 10)
        } else if (!is.null(resultados$registro) && isTRUE(resultados$registro$eh_novo_recorde)) {
          showNotification("🏆 NOVO RECORDE GLOBAL HISTÓRICO ENCONTRADO E SALVO NO CSV!", 
                           type = "message", duration = 10)
        } else {
          showNotification("✅ Otimização GA concluída e registrada no histórico CSV!", type = "message")
        }
        
      } else {
        # Execução padrão (Preset ou Custom)
        withProgress(message = "Executando ESN...", value = 0, {
          dados_split <- dividir_dados(dados)
          
          if (input$modo_operacao == "preset") {
            cen <- cenarios[[input$cenario]]
            if (is.null(cen) || is.null(cen$W)) {
              cen <- cenarios[["9220_GED_Normal_15"]]
            }
            
            params <- list(
              a = cen$a, sr = cen$sr, initLen = cen$initLen,
              tam_reservoir = cen$tam_reservoir, reg = cen$reg
            )
            
            setProgress(0.3, detail = "Calculando Validação...")
            res_val <- esn_validacao(dados_split, params, cen$Win, cen$W, cen$Wout)
            
            setProgress(0.6, detail = "Calculando Teste...")
            res_teste <- esn_teste(dados_split, params, cen$Win, cen$W, cen$Wout)
            
          } else {
            tam_r <- 27
            params <- list(a = 0.87, sr = 0.4, initLen = 9, tam_reservoir = tam_r, reg = 2.2e-05)
            
            Win_new <- matrix(gerar_amostras(input$dist_win, tam_r * 2), nrow = tam_r, ncol = 2)
            W_new <- matrix(gerar_amostras(input$dist_w, tam_r * tam_r), nrow = tam_r, ncol = tam_r)
            
            setProgress(0.3, detail = "Calculando Validação...")
            res_val <- esn_validacao(dados_split, params, Win_new, W_new, Wout = NULL)
            
            setProgress(0.6, detail = "Calculando Teste...")
            res_teste <- esn_teste(dados_split, params, Win_new, W_new, res_val$Wout)
          }
          
          setProgress(0.9, detail = "Finalizando...")
          resultados$validacao <- res_val
          resultados$teste <- res_teste
          resultados$origem <- input$modo_operacao
          resultados$todas_combinacoes <- NULL
          resultados$metricas <- list(
            modelo = "ESN",
            treino = res_val$metricas_treino,
            validacao = res_val$metricas_valida,
            teste = res_teste$metricas_teste,
            tempo = res_val$tempo + res_teste$tempo
          )
        })
        
        showNotification("✅ ESN executada com sucesso!", type = "message")
      }
    })
    
    # Painel e Tabela de Comparativo de Distribuições
    output$painel_comparativo_dists <- renderUI({
      if (is.null(resultados$todas_combinacoes) || length(resultados$todas_combinacoes) <= 1) {
        div(style = "background: #f8fafc; border: 1px dashed #cbd5e1; border-radius: 8px; padding: 14px; margin-bottom: 14px;",
            "💡 Dica: Selecione mais de uma distribuição para Win ou W e clique em Executar para comparar automaticamente todas as combinações!")
      } else {
        campea <- resultados$todas_combinacoes[[which.max(sapply(resultados$todas_combinacoes, function(x) x$fitness))]]
        div(style = "background: #ecfdf5; border: 1px solid #6ee7b7; border-radius: 8px; padding: 12px 16px; margin-bottom: 14px;",
            strong(style = "color: #065f46; font-size: 1rem;", sprintf("🏆 Distribuição Campeã: Win = %s | W = %s", campea$dist_win, campea$dist_w)),
            p(style = "margin: 4px 0 0 0; color: #047857; font-size: 0.88rem;",
              sprintf("Menor MAE de Validação: %.6f | Fitness GA: %.4f | Reservatório: %d neurônios",
                      campea$validacao$metricas_valida$MAE, campea$fitness, campea$params$tam_reservoir)))
      }
    })
    
    output$tabela_comparativo_dists <- renderTable({
      req(resultados$todas_combinacoes)
      if (length(resultados$todas_combinacoes) == 0) return(NULL)
      
      lista <- resultados$todas_combinacoes
      max_fit <- max(sapply(lista, function(x) x$fitness))
      
      df_comp <- do.call(rbind, lapply(1:length(lista), function(i) {
        item <- lista[[i]]
        eh_campea <- identical(item$fitness, max_fit)
        data.frame(
          "Posição" = if (eh_campea) "🏆 #1 (Campeã)" else paste0("#", i),
          "Distribuição Win" = item$dist_win,
          "Distribuição W" = item$dist_w,
          "Reservatório" = item$params$tam_reservoir,
          "MAE Validação" = sprintf("%.6f", item$validacao$metricas_valida$MAE),
          "RMSE Validação" = sprintf("%.6f", item$validacao$metricas_valida$RMSE),
          "MAE Teste" = sprintf("%.6f", item$teste$metricas_teste$MAE),
          "R² Teste" = sprintf("%.4f", item$teste$metricas_teste$R2),
          "Fitness GA" = sprintf("%.4f", item$fitness),
          "Tempo (s)" = sprintf("%.2f", item$tempo),
          check.names = FALSE,
          stringsAsFactors = FALSE
        )
      }))
      
      # Ordenar por MAE Validação (crescente)
      df_comp[order(as.numeric(df_comp$`MAE Validação`)), ]
    })
    
    # Banner de Recorde Histórico
    output$banner_recorde <- renderUI({
      req(resultados$registro)
      reg <- resultados$registro
      
      if (isTRUE(reg$eh_novo_recorde)) {
        div(style = "background: #fefce8; border: 2px solid #eab308; border-radius: 12px; padding: 16px; margin-bottom: 16px;",
          div(style = "display: flex; align-items: center; gap: 10px;",
            span(style = "font-size: 1.8rem;", "🏆"),
            div(
              h4(style = "margin: 0; color: #854d0e; font-weight: 800;", "NOVO RECORDE HISTÓRICO GLOBAL ENCONTRADO!"),
              p(style = "margin: 4px 0 0 0; color: #a16207; font-size: 0.95rem;",
                sprintf("ID: %s • MAE Validação: %.6f • %s", reg$id, reg$mae_valida, reg$delta_recorde))
            )
          )
        )
      } else {
        div(style = "background: #f8fafc; border: 1px solid #e2e8f0; border-left: 4px solid #059669; border-radius: 8px; padding: 12px 16px; margin-bottom: 16px;",
          div(style = "display: flex; justify-content: space-between; align-items: center;",
            div(
              strong(style = "color: #0f172a;", sprintf("Execução Registrada (%s):", reg$id)),
              span(style = "color: #475569; font-size: 0.9rem;", sprintf(" %s | %s", reg$delta_anterior, reg$delta_recorde))
            ),
            span(class = "badge-tag badge-esn", "Histórico Salvo em CSV")
          )
        )
      }
    })
    
    # Saídas
    output$resultados_texto <- renderPrint({
      req(resultados$validacao)
      cat("=====================================================\n")
      cat("  MÉTRICAS DETALHADAS — ECHO STATE NETWORK (ESN)\n")
      cat("=====================================================\n\n")
      cat(sprintf("• Origem da Configuração: %s\n\n", resultados$origem))
      cat("• FASE DE VALIDAÇÃO (In-Sample):\n")
      cat(sprintf("  - MAE:   %.6f\n", resultados$validacao$metricas_valida$MAE))
      cat(sprintf("  - RMSE:  %.6f\n", resultados$validacao$metricas_valida$RMSE))
      cat(sprintf("  - MAPE:  %.2f%%\n", resultados$validacao$metricas_valida$MAPE))
      cat(sprintf("  - R²:    %.4f\n", resultados$validacao$metricas_valida$R2))
      cat(sprintf("  - Tempo: %.4f segundos\n\n", resultados$validacao$tempo))
      cat("• FASE DE TESTE (Out-of-Sample):\n")
      cat(sprintf("  - MAE:   %.6f\n", resultados$teste$metricas_teste$MAE))
      cat(sprintf("  - RMSE:  %.6f\n", resultados$teste$metricas_teste$RMSE))
      cat(sprintf("  - MAPE:  %.2f%%\n", resultados$teste$metricas_teste$MAPE))
      cat(sprintf("  - R²:    %.4f\n", resultados$teste$metricas_teste$R2))
      cat(sprintf("  - Tempo: %.4f segundos\n", resultados$teste$tempo))
    })
    
    output$tabela_metricas <- renderTable({
      req(resultados$validacao)
      data.frame(
        "Fase" = c("Validação", "Teste"),
        "MAE"  = sprintf("%.6f", c(resultados$validacao$metricas_valida$MAE, resultados$teste$metricas_teste$MAE)),
        "RMSE" = sprintf("%.6f", c(resultados$validacao$metricas_valida$RMSE, resultados$teste$metricas_teste$RMSE)),
        "MAPE %" = sprintf("%.2f%%", c(resultados$validacao$metricas_valida$MAPE, resultados$teste$metricas_teste$MAPE)),
        "R²"   = sprintf("%.4f", c(resultados$validacao$metricas_valida$R2, resultados$teste$metricas_teste$R2)),
        "Tempo (s)" = sprintf("%.4f", c(resultados$validacao$tempo, resultados$teste$tempo)),
        check.names = FALSE,
        stringsAsFactors = FALSE
      )
    })
    
    output$grafico_validacao <- renderPlot({
      req(resultados$validacao)
      dados <- dados_reativo()
      ds <- dividir_dados(dados)
      real <- ds$treino_valida[(ds$idx$treino_n + 1):(ds$idx$treino_n + ds$idx$valida_n)]
      prev <- resultados$validacao$previsao_valida
      
      par(mar = c(3.5, 4, 2, 1), bg = "transparent")
      plot(real, type = 'l', col = '#0f172a', lwd = 2,
           ylab = "Preço PETR4 (R$)", xlab = "Dias",
           main = "ESN — Previsão na Fase de Validação", axes = FALSE, col.main = "#0f172a")
      axis(1, col = "#cbd5e1", col.axis = "#475569")
      axis(2, col = "#cbd5e1", col.axis = "#475569")
      grid(col = "#e2e8f0", lty = "dotted")
      
      lines(prev, col = '#059669', lwd = 1.8)
      legend('topright', legend = c('Série Real', 'ESN Prevista'),
             col = c('#0f172a', '#059669'), lty = 1, lwd = c(2, 1.8), bty = 'n', text.col = '#0f172a')
    })
    
    output$grafico_teste <- renderPlot({
      req(resultados$teste)
      dados <- dados_reativo()
      ds <- dividir_dados(dados)
      real <- ds$treina_testa[(ds$idx$treino_n + 1):(ds$idx$treino_n + ds$idx$teste_n)]
      prev <- resultados$teste$previsao_teste
      
      par(mar = c(3.5, 4, 2, 1), bg = "transparent")
      plot(real, type = 'l', col = '#0f172a', lwd = 2,
           ylab = "Preço PETR4 (R$)", xlab = "Dias",
           main = "ESN — Previsão na Fase de Teste", axes = FALSE, col.main = "#0f172a")
      axis(1, col = "#cbd5e1", col.axis = "#475569")
      axis(2, col = "#cbd5e1", col.axis = "#475569")
      grid(col = "#e2e8f0", lty = "dotted")
      
      lines(prev, col = '#059669', lwd = 1.8)
      legend('topright', legend = c('Série Real', 'ESN Prevista'),
             col = c('#0f172a', '#059669'), lty = 1, lwd = c(2, 1.8), bty = 'n', text.col = '#0f172a')
    })
    
    # Tabela do Histórico CSV
    historico_reativo <- reactiveVal(carregar_historico_ga())
    
    observeEvent(input$btn_atualizar_csv, {
      historico_reativo(carregar_historico_ga())
    })
    
    output$tabela_historico_ga <- renderTable({
      df <- historico_reativo()
      if (nrow(df) == 0) {
        return(data.frame(Mensagem = "Nenhuma otimização registrada ainda. Execute o GA Live para gravar no histórico!"))
      }
      
      cols_exibir <- c("id_execucao", "timestamp", "geracoes", "dist_win", "dist_w", 
                       "tam_reservoir", "mae_valida", "mae_teste", "delta_recorde_pct")
      
      df_sub <- df[, intersect(cols_exibir, names(df))]
      names(df_sub) <- c("ID", "Data/Hora", "Gerações", "Win", "W", "Reservatório", 
                         "MAE Valida", "MAE Teste", "Comparativo com Recorde")[1:ncol(df_sub)]
      df_sub
    })
    
    # Retornar métricas para comparação
    reactive(resultados$metricas)
  })
}
