source("Scripts/diebold_mariano/common_controlled.R")
prepare_dm_data <- function(smoke = FALSE) {
  cfg <- dm_config()
  p <- "Scripts/data/PETR4_close com factor_2000-2020.txt"
  q <- "Scripts/data/PETR4_close com factor_2000-2020_com data.csv"
  y <- scan(p, quiet = TRUE, dec = ".")
  tab <- read.table(q, sep = ";", dec = ".", colClasses = c("character", "numeric"))
  dates <- as.Date(tab[[1]])
  if (!is.null(cfg$official_data_md5)) stopifnot(
    tolower(unname(tools::md5sum(p))) == tolower(cfg$official_data_md5$values),
    tolower(unname(tools::md5sum(q))) == tolower(cfg$official_data_md5$dates))
  stopifnot(length(y) == 5198L, nrow(tab) == 5198L, !anyNA(dates),
    !anyDuplicated(dates), all(diff(dates) > 0), all(is.finite(y)), all(is.finite(tab[[2]])),
    max(abs(y - tab[[2]])) < 1e-10, dates[1] == as.Date("2000-01-03"),
    tail(dates, 1) == as.Date("2020-12-30"),
    cfg$treino_n == 2600, cfg$validacao_n == 1299, cfg$teste_n == 1299)
  sizes <- c(2600L, 1299L, 1299L)
  if (smoke) { y <- y[1:100]; dates <- dates[1:100]; sizes <- c(70L, 15L, 15L) }
  ntrain <- sizes[1]; nval <- sizes[2]
  train <- seq_len(ntrain); validation <- (ntrain + 1L):(ntrain + nval)
  test <- (ntrain + nval + 1L):length(y)
  stopifnot(identical(c(train, validation, test), seq_along(y)))
  scale <- list(min = min(y[train]), max = max(y[train]), fit_indices = train)
  stopifnot(identical(scale$fit_indices, train), scale$max > scale$min)
  common_start <- if (smoke) dates[test[2]] else as.Date(cfg$test_common_start)
  common_dates <- dates[test][dates[test] >= common_start]
  stopifnot(length(common_dates) > 1L, common_start %in% dates[test])
  list(y = y, dates = dates, train = train, validation = validation, test = test,
    scale = scale, common_dates = common_dates, smoke = smoke,
    source_md5 = as.list(tools::md5sum(c(p, q))))
}
dm_windows <- function(d, target, timesteps = 10L) {
  stopifnot(all(target > timesteps), all(target <= length(d$y)), !anyDuplicated(target))
  stopifnot(identical(d$scale$fit_indices, d$train),
    d$scale$min == min(d$y[d$train]), d$scale$max == max(d$y[d$train]))
  # Indices refer to the FULL chronological series, never train+test concatenation.
  indices <- t(vapply(target, function(i) seq.int(i - timesteps, i - 1L), integer(timesteps)))
  stopifnot(all(indices[, timesteps] == target - 1L), all(indices < target),
    all(apply(indices, 1, function(x) all(diff(x) == 1L))))
  z <- (d$y - d$scale$min) / (d$scale$max - d$scale$min)
  X <- array(z[indices], dim = c(length(target), timesteps, 1L))
  stopifnot(all(is.finite(X)), all(is.finite(z[target])))
  list(x = X, y = z[target], targets = target, input_indices = indices)
}
if (sys.nframe() == 0L) {
  d <- prepare_dm_data(FALSE)
  w <- dm_windows(d, d$test)
  stopifnot(identical(as.integer(w$input_indices[1, ]), 3890:3899))
  cat("Data-only check: ", length(d$y), "observations;", length(d$common_dates),
    "common dates; first test context", paste(w$input_indices[1, ], collapse = ","), "\n")
}
