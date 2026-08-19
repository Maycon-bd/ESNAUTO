library(shiny)
library(httpuv)

# Test reading session$input directly
app <- shinyApp(
  ui = fluidPage(
    actionButton("btn_start", "Start"),
    actionButton("btn_cancel", "Cancel")
  ),
  server = function(input, output, session) {
    observeEvent(input$btn_start, {
      cat("Checking session$input$btn_cancel:", isolate(input$btn_cancel), "\n")
      # In the session environment, let's see how session$input is structured
      cat("session$input class:", class(session$input), "\n")
      cat("session$input names:", names(session$input), "\n")
    })
  }
)
