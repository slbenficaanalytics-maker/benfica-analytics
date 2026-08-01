library(tidyverse)

player_metadata <- read_csv(
  "data/processed/player_metadata.csv",
  show_col_types = FALSE
)

squad_audit <- player_metadata |>
  transmute(
    player_id,
    player_name,
    api_position = position,
    current_squad = NA_character_,
    detailed_position = NA_character_,
    new_signing_2026_27,
    arrival_date,
    previous_club,
    academy_player,
    validation_source = NA_character_,
    validation_date = as.Date(NA),
    notes
  ) |>
  arrange(api_position, player_name)

write_csv(
  squad_audit,
  "data/processed/squad_audit.csv",
  na = ""
)

print(squad_audit, n = Inf)