library(tidyverse)

squad <- read_csv(
  "data/processed/benfica_confirmed_squad.csv",
  show_col_types = FALSE
)

player_integration <- squad |>
  mutate(
    arrival_date = as.Date(arrival_date),
    reference_date = Sys.Date(),
    days_since_arrival = as.integer(
      reference_date - arrival_date
    )
  ) |>
  filter(new_signing_2026_27 == TRUE) |>
  select(
    player_id,
    player_name,
    api_position,
    arrival_date,
    previous_club,
    reference_date,
    days_since_arrival
  )

write_csv(
  player_integration,
  "data/processed/player_integration.csv",
  na = ""
)

print(player_integration, n = Inf)