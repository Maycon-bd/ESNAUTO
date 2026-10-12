# A partir da raiz: Rscript Scripts/abrir_biblioshiny_reconstruido.R
invisible(Sys.setlocale("LC_CTYPE", "English_United States.utf8"))
.libPaths(c(file.path(getwd(), "Scripts/results/bibliometria_ambiente/R-library"),
            "C:/Users/User/AppData/Local/R/win-library/4.6",
            file.path(getwd(), "Scripts/results/diebold_mariano/ambiente/R-library"), .libPaths()))
if (!requireNamespace("bibliometrix", quietly = TRUE)) stop("Execute primeiro Scripts/instalar_bibliometria_local.R")
cat("Em Data > Import or Load, escolha Load bibliometrix file(s).\n")
cat("Arquivo:", normalizePath("reports/bibliometria_reconstrucao/colecao_biblioshiny.RData", winslash = "/"), "\n")
cat("Para a rede, selecione Author Keywords; o conjunto tem 24 documentos com palavras-chave.\n")
bibliometrix::biblioshiny()
