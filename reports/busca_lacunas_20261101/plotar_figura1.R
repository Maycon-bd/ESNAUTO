# Gr\u00e1fico descritivo da recodifica\u00e7\u00e3o editorial. N\u00e3o executa experimentos ESN.
root <- "reports/busca_lacunas_20261101"
tab <- read.csv(file.path(root, "contagens_recodificadas.csv"), check.names = FALSE)
stopifnot(nrow(tab) == 5, all(rowSums(tab[, -1]) == 34))
mat <- t(as.matrix(tab[, c("direta", "secundaria", "insuficiente", "nao_aplicavel")]))
labs <- c("P1  Win/W", "P2  Hiperpar\u00e2metros",
          "P3  S\u00e9ries temporais", "P4  LSTM/GRU/\nTransformer", "P5  Mercado/ativo")
cores <- c("#245B78", "#D18932", "#C3CAD0", "#EDF0F2")
for (fmt in c("png", "svg")) {
  target <- file.path(root, paste0("figura1_atualizada.", fmt))
  if (fmt == "png") png(target, width = 2100, height = 1260, res = 300, pointsize = 12, type = "cairo")
  else svg(target, width = 7, height = 4.2, pointsize = 12, family = "Arial")
  par(mar = c(7.3, 10.5, 2.6, 1), family = "Arial", las = 1,
      col.axis = "#38444E", col.lab = "#222222", xaxs = "i")
  y <- barplot(mat[, 5:1], horiz = TRUE, names.arg = labs[5:1],
               col = cores, border = "white", axes = FALSE, xlim = c(0, 34),
               space = 0.33, cex.names = 0.95,
               xlab = "N\u00famero de documentos (34 em cada dimens\u00e3o)")
  axis(1, at = c(0, 5, 10, 15, 20, 25, 30, 34), col = "#B8C1C8", col.ticks = "#B8C1C8")
  for (col in 1:5) {
    vals <- mat[, 6-col]
    centers <- cumsum(vals) - vals/2
    for (k in 1:4) if (vals[k] > 0) text(centers[k], y[col], vals[k],
         col = if (k == 1) "white" else "#17232B", cex = 0.98)
  }
  title(main = "Documenta\u00e7\u00e3o localizada por dimens\u00e3o", adj = 0, cex.main = 1.12)
  legend("bottom", inset = c(0, -0.60), xpd = NA, ncol = 2,
         fill = cores, border = NA, bty = "n", cex = 0.95,
         legend = c("D: direta", "S: secund\u00e1ria", "?: insuficiente", "N\u00e3o se aplica"))
  dev.off()
}
cat("Figura 1 PNG/SVG gerada com quatro estados, sem tratar insufici\u00eancia como aus\u00eancia.\n")
