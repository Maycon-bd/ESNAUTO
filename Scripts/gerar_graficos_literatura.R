# Executar a partir da raiz após extrair_base_graficos_literatura.py.
invisible(Sys.setlocale("LC_CTYPE", "English_United States.utf8"))
base_dir <- "reports/figures_bibliograficas"
base <- jsonlite::fromJSON(file.path(base_dir, "base_tabela2.json"))
n <- base$n
stopifnot(n > 0, sum(unlist(base$anos)) == n, all(base$cobertura <= n))
cor <- "#245B78"
cinza <- "#56616B"

abrir <- function(nome, formato) {
  path <- file.path(base_dir, paste0(nome, ".", formato))
  if (formato == "png") png(path, width = 2400, height = 1500, res = 250)
  else svg(path, width = 9.6, height = 6, family = "sans")
}

for (formato in c("png", "svg")) {
  abrir("figura_cobertura_p1_p5", formato)
  par(mar = c(4, 12, 4.5, 2), family = "sans", las = 1,
      col.axis = cinza, col.lab = "#222222", cex = 1)
  labels <- c("P1  Inicialização dos pesos", "P2  Otimização",
              "P3  Pré-processamento", "P4  Comparação com DL", "P5  Mercado e ativo")
  ordem <- 5:1
  alturas <- barplot(base$cobertura[ordem], horiz = TRUE, names.arg = labels[ordem],
                    xlim = c(0, n + 5), col = cor, border = NA, axes = FALSE,
                    xlab = "Número de estudos com cobertura substantiva")
  axis(1, at = seq(0, 35, 5), col = "#B8C1C8", col.ticks = "#B8C1C8")
  text(base$cobertura[ordem] + 0.5, alturas,
       chartr(".", ",", sprintf("%d (%.1f%%)", base$cobertura[ordem], 100 * base$cobertura[ordem] / n)),
       adj = 0, cex = 0.95, col = "#222222")
  title(main = "Cobertura das dimensões analíticas", adj = 0, line = 2.5, cex.main = 1.2)
  mtext(sprintf("Estudos listados na Tabela 2 da monografia (n = %d)", n),
        side = 3, line = 1, adj = 0, col = cinza, cex = 0.9)
  dev.off()

  abrir("figura_estudos_por_ano", formato)
  par(mar = c(6, 4.5, 4.5, 1.5), family = "sans", las = 1,
      col.axis = cinza, col.lab = "#222222", cex = 1)
  anos <- names(base$anos)
  contagens <- as.numeric(unlist(base$anos))
  limites <- c(0, max(contagens) + 2)
  alturas <- barplot(contagens, names.arg = anos, col = cor, border = NA,
                    ylim = limites, axes = FALSE, xlab = "Ano informado na tabela",
                    ylab = "Número de estudos")
  axis(2, at = seq(0, ceiling(max(contagens) + 1), 2), col = "#B8C1C8", col.ticks = "#B8C1C8")
  text(alturas, contagens + 0.35, labels = contagens, col = "#222222", cex = 1)
  title(main = "Distribuição dos estudos por ano", adj = 0, line = 2.5, cex.main = 1.2)
  mtext(sprintf("Estudos listados na Tabela 2 da monografia (n = %d)", n),
        side = 3, line = 1, adj = 0, col = cinza, cex = 0.9)
  mtext("Anos exibidos como categorias; anos sem registros não estão representados.",
        side = 1, line = 4.6, adj = 0, cex = 0.75, col = cinza)
  dev.off()
}
cat("Gráficos PNG e SVG gerados a partir da Tabela 2.\n")
