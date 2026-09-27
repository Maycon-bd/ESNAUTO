source("Scripts/diebold_mariano/dl_controlled.R")
if (sys.nframe() == 0L) dm_cli("lstm", function(d, cfg, smoke, out) dl_controlled(d, cfg, smoke, out, "lstm"))
