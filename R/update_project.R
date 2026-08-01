source("R/get_matches.R")
source("R/clean_matches.R")
source("R/clean_historical_matches.R")
source("R/combine_seasons.R")

source("R/update_fbref_data.R")

system("quarto render")

message("Projeto e website atualizados com sucesso.")