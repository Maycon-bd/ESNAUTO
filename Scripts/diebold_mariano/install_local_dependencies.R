# Preparacao explicita, isolada. Nao executa modelos.
invisible(Sys.setlocale("LC_CTYPE", "English_United States.utf8"))
root <- normalizePath("Scripts/results/diebold_mariano/ambiente", winslash = "/")
lib <- file.path(root, "R-library")
dir.create(lib, recursive = TRUE, showWarnings = FALSE)
.libPaths(c(lib, .libPaths()))
options(repos = c(CRAN = "https://cloud.r-project.org"), timeout = 600)
pkgs <- c("forecast", "keras3", "tensorflow", "jsonlite", "reticulate", "pracma")
missing <- setdiff(pkgs, rownames(installed.packages()))
if (length(missing)) install.packages(missing, lib = lib, type = "binary", dependencies = NA)
db <- installed.packages()
deps <- unique(c(pkgs, unlist(tools::package_dependencies(pkgs, db = db, recursive = TRUE))))
for (p in intersect(deps, rownames(db))) {
  source <- db[p, "LibPath"]
  if (!dir.exists(file.path(lib, p)) && !startsWith(source, R.home())) {
    if (!file.copy(file.path(source, p), lib, recursive = TRUE)) stop("Cannot isolate package: ", p)
  }
}
stopifnot(all(pkgs %in% rownames(installed.packages())))
write.csv(installed.packages()[, c("Package", "Version", "LibPath")],
          file.path(root, "R_packages_lock.csv"), row.names = FALSE)
