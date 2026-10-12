# Instalação isolada; não modifica a biblioteca usada nas baterias anteriores.
invisible(Sys.setlocale("LC_CTYPE", "English_United States.utf8"))
lib <- file.path(getwd(), "Scripts/results/bibliometria_ambiente/R-library")
dir.create(lib, recursive = TRUE, showWarnings = FALSE)
.libPaths(c(lib, "C:/Users/User/AppData/Local/R/win-library/4.6",
            file.path(getwd(), "Scripts/results/diebold_mariano/ambiente/R-library"), .libPaths()))
options(repos = c(CRAN = "https://cloud.r-project.org"), timeout = 300)
if (!requireNamespace("bibliometrix", quietly = TRUE)) {
  install.packages("bibliometrix", lib = lib, dependencies = NA, type = "binary")
}
stopifnot(requireNamespace("bibliometrix", quietly = TRUE))
cat("bibliometrix", as.character(packageVersion("bibliometrix")), "disponível.\n")
