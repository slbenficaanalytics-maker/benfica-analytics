library(tidyverse)

club_name_map <- read_delim(
  "data/processed/club_name_map.csv",
  delim = ";",
  show_col_types = FALSE,
  trim_ws = TRUE
)

clubelo_ranking <- read_csv(
  "http://api.clubelo.com/2026-08-01",
  show_col_types = FALSE
)

name_validation <- club_name_map |>
  left_join(
    clubelo_ranking |>
      select(
        clubelo_name = Club,
        clubelo_elo = Elo
      ),
    by = "clubelo_name"
  ) |>
  select(
    opponent,
    clubelo_name,
    clubelo_elo
  )

print(name_validation, n = Inf)