# Importação e gráficos reais com bibliometrix. Não usa métricas de citação.
invisible(Sys.setlocale("LC_CTYPE", "English_United States.utf8"))
.libPaths(c(file.path(getwd(), "Scripts/results/bibliometria_ambiente/R-library"),
            "C:/Users/User/AppData/Local/R/win-library/4.6",
            file.path(getwd(), "Scripts/results/diebold_mariano/ambiente/R-library"), .libPaths()))
suppressPackageStartupMessages(library(bibliometrix))
out <- "reports/bibliometria_reconstrucao"
fig <- file.path(out, "graficos")
dir.create(fig, showWarnings = FALSE)
base <- jsonlite::fromJSON(file.path(out, "base_reconstruida.json"), simplifyVector = FALSE)
records <- base$records

M <- convert2df(file.path(out, "artigos_reconstruidos.bib"), dbsource = "generic", format = "bibtex", remove.duplicates = FALSE)
stopifnot(nrow(M) == length(records), nrow(M) == 34)
# Relacionar os registros pelo título importado, não depender da ordem do conversor.
normalizar_titulo <- function(x) tolower(gsub("[^[:alnum:]]", "", iconv(x, to = "ASCII//TRANSLIT")))
ind <- match(normalizar_titulo(M$TI), normalizar_titulo(vapply(records, `[[`, "", "title")))
stopifnot(!anyNA(ind), !anyDuplicated(ind))
records <- records[ind]
stopifnot(!anyNA(M$AU), all(nzchar(M$AU)), !anyNA(M$TI), all(nzchar(M$TI)),
          identical(as.integer(M$PY), vapply(records, function(r) as.integer(r$year), 0L)))
M$LOCAL_ID <- vapply(records, `[[`, "", "id")
M$DB <- "RECONSTRUIDA_PDFS_CROSSREF"
M$TC <- NA_real_ # Ausência de contagem não equivale a zero citações.
M$CR <- NA_character_ # Não foram extraídas listas de referências para redes de citação.
M$SO <- toupper(vapply(records, `[[`, "", "source"))
M$DT <- toupper(vapply(records, `[[`, "", "type"))
M$LOCAL_PDF <- vapply(records, `[[`, "", "arquivo_pdf")
M$LOCAL_GRUPO <- vapply(records, `[[`, "", "grupo_temporal")
M$LOCAL_ORIGEM <- vapply(records, `[[`, "", "origem_metadados")
M$LOCAL_NOTA <- vapply(records, function(r) paste(unlist(r$notes), collapse = " | "), "")
M$PY <- vapply(records, function(r) as.integer(r$year), 0L)
M$DE <- gsub("\\&", "&", M$DE, fixed = TRUE)
M$DE <- gsub("\\%", "%", M$DE, fixed = TRUE)
stopifnot(sum(!is.na(M$DE) & nzchar(M$DE)) == base$n_com_keywords)
class(M) <- c("bibliometrixDB", "data.frame")
save(M, file = file.path(out, "colecao_biblioshiny.RData"))
saveRDS(M, file.path(out, "colecao_bibliometrix.rds"))

# Validar o mesmo carregador usado pelo Biblioshiny, sem iniciar um servidor web.
load_env <- new.env(parent = baseenv())
load(file.path(out, "colecao_biblioshiny.RData"), envir = load_env)
stopifnot(inherits(load_env$M, "bibliometrixDB"), nrow(load_env$M) == 34,
          all(is.na(load_env$M$TC)), identical(load_env$M$LOCAL_ID, M$LOCAL_ID))
utils_file <- system.file("biblioshiny/utils.R", package = "bibliometrix")
exprs <- parse(utils_file, encoding = "UTF-8")
loader <- Filter(function(e) is.call(e) && identical(e[[1]], as.name("<-")) && identical(e[[2]], as.name("smart_load")), as.list(exprs))
stopifnot(length(loader) == 1)
eval(loader[[1]], envir = load_env)
loaded <- load_env$smart_load(file.path(out, "colecao_biblioshiny.RData"))
stopifnot(identical(loaded, M))

com_kw <- !is.na(M$DE) & nzchar(M$DE)
K <- M[com_kw, ]
Net <- biblioNetwork(K, analysis = "co-occurrences", network = "author_keywords", sep = ";")
Net <- as.matrix(Net)
kw_docs <- lapply(records[com_kw], function(r) toupper(unlist(r$keywords_normalizadas)))
freq <- table(unlist(kw_docs))
# Conferir matriz independentemente a partir das palavras-chave por documento.
termos <- colnames(Net)
bin <- vapply(termos, function(t) vapply(kw_docs, function(k) as.integer(t %in% k), 0L), integer(length(kw_docs)))
expected <- crossprod(bin)
stopifnot(identical(dim(Net), dim(expected)), all(Net == expected))
saveRDS(Net, file.path(out, "matriz_coocorrencia.rds"))
freq <- sort(freq, decreasing = TRUE)
freq_records <- lapply(names(freq), function(t) list(termo = tolower(t), documentos = as.integer(freq[[t]])))

abrir <- function(nome, formato, w = 11, h = 7) {
  path <- file.path(fig, paste0(nome, ".", formato))
  if (formato == "png") png(path, width = w * 300, height = h * 300, res = 300)
  else svg(path, width = w, height = h, family = "sans")
}

set.seed(20261012)
selecionados <- names(freq)[freq >= 2]
A <- Net[selecionados, selecionados, drop = FALSE]
diag(A) <- 0
g <- igraph::graph_from_adjacency_matrix(A, mode = "undirected", weighted = TRUE, diag = FALSE)
layout <- igraph::layout_with_fr(g)
layout <- igraph::norm_coords(layout, xmin = -1, xmax = 1, ymin = -1, ymax = 1)
clusters <- igraph::membership(igraph::cluster_walktrap(g))
colors <- c("#24627A", "#AF653E", "#4D7C4F", "#74609B", "#735A48")
grupos <- colors[(clusters - 1) %% length(colors) + 1]
node_data <- data.frame(name = igraph::V(g)$name, x = layout[, 1], y = layout[, 2],
                        frequencia = as.numeric(freq[igraph::V(g)$name]),
                        grupo = factor(clusters), label = tolower(igraph::V(g)$name))
links <- igraph::as_data_frame(g, what = "edges")
links$x <- node_data$x[match(links$from, node_data$name)]
links$y <- node_data$y[match(links$from, node_data$name)]
links$xend <- node_data$x[match(links$to, node_data$name)]
links$yend <- node_data$y[match(links$to, node_data$name)]
p_network <- ggplot2::ggplot() +
  ggplot2::geom_segment(data = links, ggplot2::aes(x = x, y = y, xend = xend, yend = yend, linewidth = weight),
                        color = "#BBC7CE", alpha = 0.65) +
  ggplot2::geom_point(data = node_data, ggplot2::aes(x = x, y = y, size = frequencia, fill = grupo),
                      shape = 21, color = "white", stroke = 0.7) +
  ggrepel::geom_text_repel(data = node_data, ggplot2::aes(x = x, y = y, label = label),
                          family = "sans", size = 4.2, seed = 20261012,
                          box.padding = 0.65, point.padding = 1.1, max.overlaps = Inf,
                          min.segment.length = 0, segment.color = "#A0ADB5", color = "#172832") +
  ggplot2::scale_size_area(max_size = 14) +
  ggplot2::scale_fill_manual(values = colors) +
  ggplot2::scale_linewidth_continuous(range = c(0.5, 1.7)) +
  ggplot2::coord_equal(xlim = c(-1.5, 1.5), ylim = c(-1.4, 1.4), clip = "off") +
  ggplot2::labs(title = "Coocorrência de palavras-chave declaradas",
    subtitle = sprintf("24 documentos; termos presentes em pelo menos 2 documentos; bibliometrix %s", packageVersion("bibliometrix")),
    caption = "Área dos nós: frequência documental. Espessura das ligações: documentos compartilhados. Cores: comunidades Walktrap.") +
  ggplot2::theme_void(base_family = "sans") +
  ggplot2::theme(legend.position = "none", plot.background = ggplot2::element_rect(fill = "white", color = NA),
    plot.title = ggplot2::element_text(size = 18, face = "bold", hjust = 0),
    plot.subtitle = ggplot2::element_text(size = 12, color = "#59636B", margin = ggplot2::margin(t = 8)),
    plot.caption = ggplot2::element_text(size = 10, color = "#59636B", hjust = 0),
    plot.margin = ggplot2::margin(24, 40, 24, 40))

for (formato in c("png", "svg")) {
  abrir("figura_frequencia_palavras_chave", formato)
  show <- rev(freq[freq >= 2])
  par(mar = c(5, 20, 5, 2), family = "sans", las = 1)
  bars <- barplot(show, horiz = TRUE, names.arg = tolower(names(show)), col = "#24627A", border = NA,
                  xlim = c(0, max(show) + 2), axes = FALSE, xlab = "Documentos que declaram o termo")
  axis(1, at = seq(0, max(show) + 1, 2), col = "#B7C2C8")
  text(as.numeric(show) + 0.2, bars, labels = as.integer(show), adj = 0)
  title("Palavras-chave recorrentes", adj = 0, line = 2.8, cex.main = 1.2)
  mtext(sprintf("%d documentos com palavras-chave declaradas; %d documentos no conjunto", nrow(K), nrow(M)),
        side = 3, line = 1.2, adj = 0, cex = 0.9, col = "#59636B")
  dev.off()

  abrir("figura_rede_palavras_chave", formato, 13, 9)
  print(p_network)
  dev.off()

  abrir("figura_anos_reconstruidos", formato)
  anos <- sort(unique(M$PY))
  counts <- vapply(anos, function(y) sum(M$PY == y), 0L)
  par(mar = c(6, 5, 5, 2), family = "sans", las = 1)
  bars <- barplot(counts, names.arg = anos, col = ifelse(anos < 2021, "#929BA2", "#24627A"),
                  border = NA, ylim = c(0, max(counts) + 3), axes = FALSE,
                  xlab = "Ano da versão bibliográfica adotada", ylab = "Número de estudos")
  axis(2, at = seq(0, max(counts) + 2, 2), col = "#B7C2C8")
  text(bars, counts + 0.3, labels = counts)
  title("Distribuição temporal do conjunto reconstruído", adj = 0, line = 2.8, cex.main = 1.2)
  mtext("34 estudos; referências anteriores ao recorte preservadas e identificadas em cinza", side = 3, line = 1.2, adj = 0, cex = 0.85, col = "#59636B")
  mtext("Anos categóricos. Versões locais: Chen e Cortesi (2026), Soltani (2022) e Duttilo/SIS (2022).",
        side = 1, line = 4.5, adj = 0, cex = 0.75, col = "#59636B")
  dev.off()
}

summary <- list(bibliometrix_version = as.character(packageVersion("bibliometrix")), registros = nrow(M),
  registros_keywords = nrow(K), termos_distintos = length(freq), termos_rede = igraph::vcount(g),
  ligacoes_rede = igraph::ecount(g), frequencia_minima = 2L,
  data_source = unique(M$DB), importacao_bib_validada = TRUE,
  carregador_biblioshiny_validado = TRUE, matriz_validada_por_contagem_independente = TRUE,
  campos_nao_disponiveis = c("TC: citações recebidas", "CR: listas de referências", "C1: afiliações"),
  frequencias = freq_records)
jsonlite::write_json(summary, file.path(out, "validacao_bibliometrix.json"), auto_unbox = TRUE, pretty = TRUE)
writeLines(capture.output(sessionInfo()), file.path(out, "ambiente_R.txt"))
cat(sprintf("OK: %d registros; %d com keywords; %d nós e %d ligações.\n", nrow(M), nrow(K), igraph::vcount(g), igraph::ecount(g)))
