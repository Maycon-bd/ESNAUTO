# =============================================================================
# data_prep.R — Preparação de dados e registro extensível de distribuições
# =============================================================================

# =============================================================================
# SISTEMA DE REGISTRO DE DISTRIBUIÇÕES (extensível)
# =============================================================================
# Para adicionar uma nova distribuição no futuro, basta chamar:
#   registrar_distribuicao("NomeDist", funcao_geradora, lista_de_parametros_default)
#
# Exemplo:
#   registrar_distribuicao(
#     nome = "Cauchy",
#     funcao = function(n, params) rcauchy(n, location = params$location, scale = params$scale),
#     params_default = list(location = 0, scale = 1),
#     descricao = "Distribuição Cauchy"
#   )
# =============================================================================

# Registro global de distribuições (environment para mutabilidade)
.registro_distribuicoes <- new.env(parent = emptyenv())
.registro_distribuicoes$distribuicoes <- list()

#' Registra uma nova distribuição no sistema
#' @param nome Nome identificador da distribuição (ex: "Normal", "GED")
#' @param funcao Função geradora que recebe (n, params) e retorna n amostras
#' @param params_default Lista com parâmetros padrão da distribuição
#' @param descricao Descrição legível da distribuição
registrar_distribuicao <- function(nome, funcao, params_default = list(), descricao = "") {
  .registro_distribuicoes$distribuicoes[[nome]] <- list(
    nome = nome,
    funcao = funcao,
    params_default = params_default,
    descricao = descricao
  )
}

#' Lista todas as distribuições registradas
#' @return Vetor com nomes das distribuições disponíveis
listar_distribuicoes <- function() {
  names(.registro_distribuicoes$distribuicoes)
}

#' Obtém uma distribuição registrada
#' @param nome Nome da distribuição
#' @return Lista com funcao, params_default, descricao
obter_distribuicao <- function(nome) {
  dist <- .registro_distribuicoes$distribuicoes[[nome]]
  if (is.null(dist)) stop(paste("Distribuição não encontrada:", nome))
  dist
}

#' Gera amostras de uma distribuição registrada
#' @param nome Nome da distribuição
#' @param n Número de amostras
#' @param params Lista de parâmetros (usa defaults se não fornecido)
#' @return Vetor com n amostras
gerar_amostras <- function(nome, n, params = NULL) {
  dist <- obter_distribuicao(nome)
  if (is.null(params)) params <- dist$params_default
  dist$funcao(n, params)
}

#' Obtém os parâmetros padrão de uma distribuição
#' @param nome Nome da distribuição
#' @return Lista com parâmetros padrão
obter_params_default <- function(nome) {
  dist <- obter_distribuicao(nome)
  dist$params_default
}

# =============================================================================
# REGISTRAR DISTRIBUIÇÕES PADRÃO
# =============================================================================

# Normal (média=0, desvio_padrão=1) — usado originalmente para W
registrar_distribuicao(
  nome = "Normal",
  funcao = function(n, params) {
    rnorm(n, mean = params$mean, sd = params$sd)
  },
  params_default = list(mean = 0, sd = 1),
  descricao = "Distribuição Normal (Gaussiana)"
)

# Uniforme (limite_inf=-1, limite_sup=1) — usado originalmente para Win e W
registrar_distribuicao(
  nome = "Uniforme",
  funcao = function(n, params) {
    runif(n, min = params$min, max = params$max)
  },
  params_default = list(min = -1.0, max = 1.0),
  descricao = "Distribuição Uniforme"
)

# GED (Generalized Error Distribution) — distribuição modificada para Win
# Requer pacote fGarch
registrar_distribuicao(
  nome = "GED",
  funcao = function(n, params) {
    if (!requireNamespace("fGarch", quietly = TRUE)) {
      stop("Pacote 'fGarch' necessário para distribuição GED. Instale com: install.packages('fGarch')")
    }
    fGarch::rged(n, mean = params$mean, sd = params$sd, nu = params$nu)
  },
  params_default = list(mean = 14.573152, sd = 8.032086, nu = 7.686645),
  descricao = "Distribuição GED (Generalized Error Distribution)"
)

# t de Student
registrar_distribuicao(
  nome = "t de Student",
  funcao = function(n, params) {
    if (!requireNamespace("fGarch", quietly = TRUE)) {
      stop("Pacote 'fGarch' necessário. Instale com: install.packages('fGarch')")
    }
    fGarch::rstd(n, mean = params$mean, sd = params$sd, nu = params$nu)
  },
  params_default = list(mean = 0, sd = 1, nu = 5),
  descricao = "Distribuição t de Student (parâmetros: mean, sd, nu)"
)

# t de Student Assimétrica
registrar_distribuicao(
  nome = "t de Student Assimétrica",
  funcao = function(n, params) {
    if (!requireNamespace("fGarch", quietly = TRUE)) {
      stop("Pacote 'fGarch' necessário. Instale com: install.packages('fGarch')")
    }
    fGarch::rsstd(n, mean = params$mean, sd = params$sd, nu = params$nu, xi = params$xi)
  },
  params_default = list(mean = 0, sd = 1, nu = 5, xi = 1.5),
  descricao = "Distribuição t de Student Assimétrica (parâmetros: mean, sd, nu, xi)"
)

# Normal Esparsa (Sparse Normal)
registrar_distribuicao(
  nome = "Normal Esparsa",
  funcao = function(n, params) {
    pesos <- rnorm(n, mean = params$mean, sd = params$sd)
    mascara <- rbinom(n, size = 1, prob = params$densidade)
    pesos * mascara
  },
  params_default = list(mean = 0, sd = 1, densidade = 0.2),
  descricao = "Normal Esparsa (20% de conexões ativas por padrão)"
)

# Cauchy
registrar_distribuicao(
  nome = "Cauchy",
  funcao = function(n, params) {
    rcauchy(n, location = params$location, scale = params$scale)
  },
  params_default = list(location = 0, scale = 1),
  descricao = "Distribuição de Cauchy (caudas extremamente pesadas)"
)

# Laplace (Dupla Exponencial)
registrar_distribuicao(
  nome = "Laplace",
  funcao = function(n, params) {
    b <- params$sd / sqrt(2)
    u <- runif(n) - 0.5
    params$mean - b * sign(u) * log(1 - 2 * abs(u))
  },
  params_default = list(mean = 0, sd = 1),
  descricao = "Distribuição de Laplace / Dupla Exponencial"
)




# =============================================================================
# FUNÇÕES DE PREPARAÇÃO DE DADOS
# =============================================================================

#' Carrega os dados PETR4 com fator
#' @param caminho Caminho para o arquivo de dados
#' @return Vetor numérico com os preços de fechamento
carregar_dados_petr4 <- function(caminho = NULL) {
  if (is.null(caminho)) {
    # Tenta encontrar o arquivo automaticamente
    caminhos_possiveis <- c(
      "Scripts/data/PETR4_close com factor_2000-2020.txt",
      "../Scripts/data/PETR4_close com factor_2000-2020.txt",
      "data/PETR4_close com factor_2000-2020.txt"
    )
    for (cp in caminhos_possiveis) {
      if (file.exists(cp)) {
        caminho <- cp
        break
      }
    }
    if (is.null(caminho)) stop("Arquivo de dados PETR4 não encontrado. Especifique o caminho.")
  }
  
  data_fac <- as.matrix(read.csv2(caminho, header = FALSE))
  as.numeric(data_fac)
}

#' Carrega os dados PETR4 com datas
#' @param caminho Caminho para o arquivo CSV com datas
#' @return Data frame com colunas 'data' e 'preco'
carregar_dados_petr4_com_datas <- function(caminho = NULL) {
  if (is.null(caminho)) {
    caminhos_possiveis <- c(
      "Scripts/data/PETR4_close com factor_2000-2020_com data.csv",
      "../Scripts/data/PETR4_close com factor_2000-2020_com data.csv",
      "data/PETR4_close com factor_2000-2020_com data.csv"
    )
    for (cp in caminhos_possiveis) {
      if (file.exists(cp)) {
        caminho <- cp
        break
      }
    }
    if (is.null(caminho)) return(NULL)
  }
  
  data_date_fac <- as.matrix(read.csv2(caminho, header = FALSE))
  data.frame(
    data  = as.Date(data_date_fac[, 1]),
    preco = as.numeric(data_date_fac[, 2]),
    stringsAsFactors = FALSE
  )
}

#' Divide os dados em treino, validação e teste
#' @param dados Vetor numérico de dados
#' @param treino_pct Percentual de treino (default 50%)
#' @param valida_pct Percentual de validação (default 25%)
#' @return Lista com vetores treino, validacao, teste e seus índices
dividir_dados <- function(dados, treino_n = 2600, valida_n = 1299, teste_n = 1299) {
  n <- length(dados)
  
  # Validar
  if (treino_n + valida_n + teste_n > n) {
    stop(paste("Dados insuficientes. Total:", n, "Requisitado:", treino_n + valida_n + teste_n))
  }
  
  list(
    treino    = dados[1:treino_n],
    validacao = dados[(treino_n + 1):(treino_n + valida_n)],
    teste     = dados[(treino_n + valida_n + 1):(treino_n + valida_n + teste_n)],
    treino_valida = dados[1:(treino_n + valida_n)],
    treina_testa  = c(dados[1:treino_n], dados[(treino_n + valida_n + 1):(treino_n + valida_n + teste_n)]),
    idx = list(
      treino_n = treino_n,
      valida_n = valida_n,
      teste_n  = teste_n
    )
  )
}

#' Normaliza dados usando min-max scaling (necessário para LSTM/GRU)
#' @param dados Vetor numérico
#' @param min_val Valor mínimo para scaling (NULL = calcula dos dados)
#' @param max_val Valor máximo para scaling (NULL = calcula dos dados)
#' @return Lista com dados normalizados e parâmetros de scaling
normalizar_minmax <- function(dados, min_val = NULL, max_val = NULL) {
  if (is.null(min_val)) min_val <- min(dados)
  if (is.null(max_val)) max_val <- max(dados)
  
  dados_norm <- (dados - min_val) / (max_val - min_val)
  
  list(
    dados = dados_norm,
    min_val = min_val,
    max_val = max_val
  )
}

#' Desnormaliza dados
#' @param dados_norm Vetor normalizado
#' @param min_val Mínimo original
#' @param max_val Máximo original
#' @return Vetor com escala original
desnormalizar_minmax <- function(dados_norm, min_val, max_val) {
  dados_norm * (max_val - min_val) + min_val
}

#' Cria janelas deslizantes para LSTM/GRU (formato 3D)
#' @param dados Vetor numérico da série temporal
#' @param timesteps Número de passos de tempo (tamanho da janela)
#' @return Lista com X (array 3D) e y (vetor de alvos)
criar_janelas_deslizantes <- function(dados, timesteps = 10) {
  n <- length(dados)
  n_amostras <- n - timesteps
  
  X <- array(0, dim = c(n_amostras, timesteps, 1))
  y <- numeric(n_amostras)
  
  for (i in 1:n_amostras) {
    X[i, , 1] <- dados[i:(i + timesteps - 1)]
    y[i] <- dados[i + timesteps]
  }
  
  list(X = X, y = y)
}

#' Prepara dados completos para LSTM/GRU
#' @param dados Vetor numérico da série
#' @param timesteps Tamanho da janela deslizante
#' @param treino_n Tamanho do treino
#' @param valida_n Tamanho da validação
#' @param teste_n Tamanho do teste
#' @return Lista com X_treino, y_treino, X_valida, y_valida, X_teste, y_teste, scaling
preparar_dados_lstm_gru <- function(dados, timesteps = 10, 
                                     treino_n = 2600, valida_n = 1299, teste_n = 1299) {
  # Normalizar usando apenas dados de treino
  treino_raw <- dados[1:treino_n]
  scaling <- normalizar_minmax(treino_raw)
  
  # Normalizar todos os dados com os parâmetros do treino
  todos_norm <- normalizar_minmax(dados, scaling$min_val, scaling$max_val)$dados
  
  # Dados de treino + validação
  treino_valida_norm <- todos_norm[1:(treino_n + valida_n)]
  janelas_tv <- criar_janelas_deslizantes(treino_valida_norm, timesteps)
  
  # Separar treino e validação
  n_treino_janelas <- treino_n - timesteps
  
  X_treino <- janelas_tv$X[1:n_treino_janelas, , , drop = FALSE]
  y_treino <- janelas_tv$y[1:n_treino_janelas]
  
  X_valida <- janelas_tv$X[(n_treino_janelas + 1):nrow(janelas_tv$X), , , drop = FALSE]
  y_valida <- janelas_tv$y[(n_treino_janelas + 1):length(janelas_tv$y)]
  
  # Dados de teste (usando treino + teste, ignorando validação)
  treina_testa_norm <- c(todos_norm[1:treino_n], 
                         todos_norm[(treino_n + valida_n + 1):(treino_n + valida_n + teste_n)])
  janelas_tt <- criar_janelas_deslizantes(treina_testa_norm, timesteps)
  
  n_teste_janelas <- teste_n - timesteps  
  # As janelas de teste começam após o treino
  idx_inicio_teste <- treino_n - timesteps + 1
  
  X_teste <- janelas_tt$X[idx_inicio_teste:nrow(janelas_tt$X), , , drop = FALSE]
  y_teste <- janelas_tt$y[idx_inicio_teste:length(janelas_tt$y)]
  
  list(
    X_treino = X_treino,
    y_treino = y_treino,
    X_valida = X_valida,
    y_valida = y_valida,
    X_teste  = X_teste,
    y_teste  = y_teste,
    scaling  = scaling,
    timesteps = timesteps
  )
}
