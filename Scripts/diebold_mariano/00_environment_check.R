source("Scripts/diebold_mariano/common_controlled.R")
dm_seed(TRUE)
tf <- reticulate::import("tensorflow"); k <- reticulate::import("keras")
stopifnot(k$backend$backend() == "tensorflow")
writeLines(capture.output(sessionInfo()), file.path(DM_ENV, "R_version.txt"))
writeLines(capture.output(installed.packages()[, c("Package", "Version", "LibPath")]),
  file.path(DM_ENV, "R_packages.txt"))
write.csv(installed.packages()[, c("Package", "Version", "LibPath")],
  file.path(DM_ENV, "R_packages_lock.csv"), row.names = FALSE)
writeLines(reticulate::py_eval("__import__('sys').version"), file.path(DM_ENV, "python_version.txt"))
writeLines(tf$`__version__`, file.path(DM_ENV, "tensorflow_version.txt"))
writeLines(k$`__version__`, file.path(DM_ENV, "keras_version.txt"))
writeLines(reticulate::py_eval("chr(10).join(sorted(d.metadata['Name'] + '==' + d.version for d in __import__('importlib.metadata', fromlist=['distributions']).distributions()))"),
  file.path(DM_ENV, "python_packages.txt"))
jsonlite::write_json(list(R = as.character(getRversion()),
  Python = reticulate::py_eval("__import__('platform').python_version()"),
  TensorFlow = tf$`__version__`, Keras = k$`__version__`,
  NumPy = reticulate::import("numpy")$`__version__`,
  R_packages = setNames(lapply(c("forecast", "keras3", "tensorflow", "jsonlite", "reticulate", "pracma"),
    function(p) as.character(packageVersion(p))), c("forecast", "keras3", "tensorflow", "jsonlite", "reticulate", "pracma")),
  visible_GPU_count = length(tf$config$get_visible_devices("GPU")), seed = DM_SEED),
  file.path(DM_ENV, "versions.json"), auto_unbox = TRUE, pretty = TRUE)
cat("Environment initialized: CPU; deterministic ops; seed", DM_SEED, "\n")
