# Complementa a análise com títulos e reúne quatro figuras recomendadas.
invisible(Sys.setlocale("LC_CTYPE", "English_United States.utf8"))
.libPaths(c(file.path(getwd(), "Scripts/results/bibliometria_ambiente/R-library"),
            "C:/Users/User/AppData/Local/R/win-library/4.6",
            file.path(getwd(), "Scripts/results/diebold_mariano/ambiente/R-library"), .libPaths()))
suppressPackageStartupMessages(library(bibliometrix))
out <- "reports/bibliometria_reconstrucao"
bundle <- file.path(out, "conjunto_monografia")
dir.create(bundle, showWarnings = FALSE)
titles <- jsonlite::fromJSON(file.path(out, "expressoes_titulos.json"), simplifyVector = FALSE)
M <- readRDS(file.path(out, "colecao_bibliometrix.rds"))
ids <- vapply(titles$records, `[[`, "", "id")
index <- match(M$LOCAL_ID, ids)
stopifnot(nrow(M) == 34, !anyNA(index), !anyDuplicated(index))
docs <- titles$records[index]
M$LOCAL_TITULO_PARA_ANALISE <- vapply(docs, `[[`, "", "titulo_analisado")
M$LOCAL_ORIGEM_TITULO_ANALISE <- vapply(docs, `[[`, "", "origem_titulo")
M$TI_TM <- vapply(docs, function(r) paste(toupper(unlist(r$bigrams)), collapse = ";"), "")
# TI preserva o título bibliográfico; TI_TM identifica os pares extraídos para análise.
Net <- as.matrix(biblioNetwork(M, analysis = "co-occurrences", network = "titles", sep = ";"))
freq <- setNames(vapply(titles$frequencias, function(r) as.integer(r$documentos), 0L),
                 toupper(vapply(titles$frequencias, `[[`, "", "expressao")))
stopifnot(setequal(names(freq), colnames(Net)), all(diag(Net) == freq[colnames(Net)]))
binary <- vapply(colnames(Net), function(t) vapply(docs, function(r) as.integer(t %in% toupper(unlist(r$bigrams))), 0L), integer(length(docs)))
stopifnot(all(Net == crossprod(binary)))
saveRDS(Net, file.path(out, "matriz_expressoes_titulos.rds"))
save(M, file = file.path(out, "colecao_biblioshiny.RData"))
saveRDS(M, file.path(out, "colecao_bibliometrix.rds"))
check <- new.env(parent = emptyenv())
load(file.path(out, "colecao_biblioshiny.RData"), envir = check)
stopifnot(inherits(check$M, "bibliometrixDB"), identical(check$M$TI_TM, M$TI_TM),
          all(is.na(check$M$TC)), sum(!is.na(M$DE) & nzchar(M$DE)) == 24)

mostrar <- titles$frequencias[vapply(titles$frequencias, function(x) x$documentos >= 2, TRUE)]
data <- data.frame(expressao = vapply(mostrar, `[[`, "", "expressao"),
                   documentos = vapply(mostrar, function(r) as.integer(r$documentos), 0L))
data$expressao <- factor(data$expressao, levels = rev(data$expressao))
p <- ggplot2::ggplot(data, ggplot2::aes(x = documentos, y = expressao)) +
  ggplot2::geom_col(fill = "#24627A", width = 0.72) +
  ggplot2::geom_text(ggplot2::aes(label = documentos), hjust = -0.3, size = 4.1) +
  ggplot2::scale_x_continuous(breaks = seq(0, max(data$documentos) + 2, 2), limits = c(0, max(data$documentos) + 1.5), expand = c(0, 0)) +
  ggplot2::labs(title = "Expressões recorrentes nos títulos",
    subtitle = "34 documentos; pares adjacentes presentes em pelo menos 2 títulos",
    x = "Documentos cujo título contém a expressão", y = NULL,
    caption = "Uma contagem por documento. Sem expansão de siglas ou junção de singular e plural. Título inglês de Costa e Lunkes transcrito do PDF.") +
  ggplot2::theme_minimal(base_family = "sans", base_size = 13) +
  ggplot2::theme(panel.grid.major.y = ggplot2::element_blank(), panel.grid.minor = ggplot2::element_blank(),
    panel.grid.major.x = ggplot2::element_line(color = "#E6EBED", linewidth = 0.3),
    plot.title = ggplot2::element_text(face = "bold", size = 18),
    plot.subtitle = ggplot2::element_text(size = 11, color = "#59636B", margin = ggplot2::margin(t = 8, b = 14)),
    axis.text = ggplot2::element_text(color = "#172832"),
    plot.caption = ggplot2::element_text(size = 8.5, color = "#59636B", hjust = 0, margin = ggplot2::margin(t = 15)),
    plot.margin = ggplot2::margin(24, 30, 20, 20))
ggplot2::ggsave(file.path(bundle, "04_expressoes_titulos.png"), p, width = 11, height = 8.5, dpi = 300, bg = "white")
ggplot2::ggsave(file.path(bundle, "04_expressoes_titulos.svg"), p, width = 11, height = 8.5, device = grDevices::svg, bg = "white")

# Recriar P1–P5 a 300 dpi; não alterar classificações da tabela original.
coverage <- jsonlite::fromJSON("reports/figures_bibliograficas/base_tabela2.json")
stopifnot(coverage$n == 34, identical(as.integer(coverage$cobertura), c(16L,16L,31L,21L,30L)))
cd <- data.frame(dimensao = factor(c("P1  Inicialização dos pesos", "P2  Otimização de hiperparâmetros", "P3  Pré-processamento", "P4  Comparação com Deep Learning", "P5  Mercado e ativo"),
                                  levels = rev(c("P1  Inicialização dos pesos", "P2  Otimização de hiperparâmetros", "P3  Pré-processamento", "P4  Comparação com Deep Learning", "P5  Mercado e ativo"))),
                 documentos = coverage$cobertura)
cd$label <- chartr(".", ",", sprintf("%d (%.1f%%)", cd$documentos, 100 * cd$documentos/34))
cp <- ggplot2::ggplot(cd, ggplot2::aes(x = documentos, y = dimensao)) +
  ggplot2::geom_col(fill = "#24627A", width = 0.7) +
  ggplot2::geom_text(ggplot2::aes(label = label), hjust = -0.12, size = 4.4) +
  ggplot2::scale_x_continuous(breaks = seq(0, 35, 5), limits = c(0, 38), expand = c(0,0)) +
  ggplot2::labs(title = "Cobertura das dimensões analíticas",
    subtitle = "Matriz P1–P5 da monografia; 34 estudos listados",
    x = "Estudos com cobertura substantiva da dimensão", y = NULL,
    caption = "Classificação da Tabela 2 preservada. Um estudo pode cobrir várias dimensões; os percentuais não somam 100%.") +
  ggplot2::theme_minimal(base_family = "sans", base_size = 13) +
  ggplot2::theme(panel.grid.major.y = ggplot2::element_blank(), panel.grid.minor = ggplot2::element_blank(),
    panel.grid.major.x = ggplot2::element_line(color = "#E6EBED", linewidth = 0.3),
    plot.title = ggplot2::element_text(face = "bold", size = 18),
    plot.subtitle = ggplot2::element_text(size = 11, color = "#59636B", margin = ggplot2::margin(t = 8, b = 14)),
    axis.text = ggplot2::element_text(color = "#172832"),
    plot.caption = ggplot2::element_text(size = 9, color = "#59636B", hjust = 0),
    plot.margin = ggplot2::margin(24, 30, 20, 20))
ggplot2::ggsave(file.path(bundle,"01_cobertura_p1_p5.png"), cp, width = 11, height = 6.5, dpi = 300, bg = "white")
ggplot2::ggsave(file.path(bundle,"01_cobertura_p1_p5.svg"), cp, width = 11, height = 6.5, device = grDevices::svg, bg = "white")
for (ext in c("png", "svg")) {
  stopifnot(file.copy(file.path(out,"graficos",paste0("figura_frequencia_palavras_chave.",ext)),
                     file.path(bundle,paste0("02_frequencia_palavras_chave.",ext)), overwrite = TRUE))
  stopifnot(file.copy(file.path(out,"graficos",paste0("figura_rede_palavras_chave.",ext)),
                     file.path(bundle,paste0("03_rede_palavras_chave.",ext)), overwrite = TRUE))
}
jsonlite::write_json(list(documentos_titulos = nrow(M), expressoes_distintas = nrow(Net),
  expressoes_recorrentes = nrow(data), matriz_validada = TRUE, denominador_keywords = 24,
  denominador_p1_p5 = 34, denominador_titulos = 34, stemming = FALSE,
  origem_titulo_ingles_D07 = "PDF de Costa e Lunkes, página 2", stopwords = titles$stopwords),
  file.path(bundle,"validacao_conjunto.json"), pretty = TRUE, auto_unbox = TRUE)
cat(sprintf("OK: 4 figuras PNG/SVG; %d expressões recorrentes nos 34 títulos.\n",nrow(data)))
