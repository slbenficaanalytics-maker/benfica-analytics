library(tidyverse)

squad <- read_csv(
  "data/processed/benfica_squad_current.csv",
  show_col_types = FALSE
)

player_metadata <- squad |>
  transmute(
    player_id,
    player_name,
    position,
    api_snapshot_date = Sys.Date(),
    squad_status = "To validate",
    new_signing_2026_27 = NA,
    arrival_date = as.Date(NA),
    previous_club = NA_character_,
    academy_player = NA,
    notes = NA_character_
  )

write_csv(
  player_metadata,
  "data/processed/player_metadata.csv",
  na = ""
)

print(player_metadata, n = Inf)