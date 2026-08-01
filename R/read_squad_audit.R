library(tidyverse)

squad_audit <- read_delim(
  "data/processed/squad_audit.csv",
  delim = ";",
  show_col_types = FALSE,
  trim_ws = TRUE
)

audit_summary <- squad_audit |>
  count(
    current_squad,
    name = "number_of_players"
  )

print(audit_summary)

players_to_review <- squad_audit |>
  filter(current_squad != "Yes") |>
  select(
    player_id,
    player_name,
    api_position,
    current_squad
  )

print(players_to_review, n = Inf)

confirmed_squad <- squad_audit |>
  filter(current_squad == "Yes") |>
  select(
    player_id,
    player_name,
    api_position,
    detailed_position,
    new_signing_2026_27,
    arrival_date,
    previous_club,
    academy_player,
    notes
  ) |>
  arrange(api_position, player_name)

print(confirmed_squad, n = Inf)

write_csv(
  confirmed_squad,
  "data/processed/benfica_confirmed_squad.csv",
  na = ""
)