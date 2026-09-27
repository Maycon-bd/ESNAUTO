source("Scripts/diebold_mariano/01_prepare_data.R")
dl_controlled <- function(d, cfg, smoke, out, kind) {
  p <- cfg[[kind]]
  epochs <- if (smoke) 1L else as.integer(p$epochs)
  stopifnot(if (smoke) epochs <= 2L else epochs == 80L)
  tr <- dm_windows(d, d$train[d$train > p$timesteps])
  va <- dm_windows(d, d$validation); te <- dm_windows(d, d$test)
  stopifnot(all(tr$targets %in% d$train), all(va$targets %in% d$validation),
    all(te$targets %in% d$test), identical(d$scale$fit_indices, d$train),
    all(te$input_indices[1, ] %in% tail(d$validation, p$timesteps)))
  model <- keras3::keras_model_sequential(input_shape = c(10L, 1L))
  if (kind == "gru") model <- keras3::layer_gru(model, units = 50L,
    activation = "tanh", recurrent_activation = "sigmoid", use_bias = TRUE,
    kernel_initializer = "glorot_uniform", recurrent_initializer = "orthogonal",
    bias_initializer = "zeros", dropout = 0, recurrent_dropout = 0,
    return_sequences = FALSE, reset_after = TRUE, stateful = FALSE, unroll = FALSE)
  else model <- keras3::layer_lstm(model, units = 50L,
    activation = "tanh", recurrent_activation = "sigmoid", use_bias = TRUE,
    kernel_initializer = "glorot_uniform", recurrent_initializer = "orthogonal",
    bias_initializer = "zeros", unit_forget_bias = TRUE, dropout = 0,
    recurrent_dropout = 0, return_sequences = FALSE, stateful = FALSE, unroll = FALSE)
  model <- keras3::layer_dropout(model, rate = .2)
  model <- keras3::layer_dense(model, units = 1L, activation = "linear")
  opt <- keras3::optimizer_adam(learning_rate = .001, beta_1 = .9, beta_2 = .999,
    epsilon = 1e-7, amsgrad = FALSE)
  keras3::compile(model, optimizer = opt, loss = "mean_squared_error", jit_compile = FALSE)
  history <- keras3::fit(model, tr$x, tr$y, epochs = epochs, batch_size = 16L,
    validation_data = list(va$x, va$y), shuffle = TRUE, verbose = 2L)
  pred <- as.numeric(stats::predict(model, te$x, verbose = 0L))
  pred <- pred * (d$scale$max - d$scale$min) + d$scale$min
  stopifnot(length(pred) == length(te$targets), all(is.finite(pred)))
  keras3::save_model(model, file.path(out, "model.keras"))
  writeLines(model$to_json(), file.path(out, "model_config.json"))
  weights <- keras3::get_weights(model)
  saveRDS(weights, file.path(out, "weights.rds"))
  saveRDS(as.data.frame(history), file.path(out, "training_history.rds"))
  saveRDS(d$scale, file.path(out, "normalization.rds"))
  list(predictions = data.frame(data = d$dates[te$targets], real = d$y[te$targets],
    previsto = pred, data_origem = d$dates[te$targets - 1L], h = 1L),
    train_target_indices = tr$targets, normalization_fit_indices = d$scale$fit_indices,
    test_input_indices = te$input_indices, epochs = epochs, n_train = length(d$train),
    source_md5 = d$source_md5)
}
