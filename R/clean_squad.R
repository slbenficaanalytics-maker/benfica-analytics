library(tidyverse)

squad_raw <- read_csv(
  "data/raw/benfica_squad_current.csv",
  show_col_types = FALSE
)

squad_clean <- squad_raw |>
  mutate(
    date_of_birth = as.Date(date_of_birth),
    snapshot_date = Sys.Date(),
    age = floor(
      as.numeric(snapshot_date - date_of_birth) / 365.25
    )
  ) |>
  arrange(position, player_name)

write_csv(
  squad_clean,
  "data/processed/benfica_squad_current.csv"
)

snapshot_filename <- paste0(
  "data/processed/benfica_squad_",
  format(Sys.Date(), "%Y_%m_%d"),
  ".csv"
)

write_csv(
  squad_clean,
  snapshot_filename
)

message(
  "Fotografia do plantel guardada em: ",
  snapshot_filename
)

print(squad_clean, n = Inf)