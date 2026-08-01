library(tidyverse)

matches <- read_csv(
  "data/processed/benfica_matches_all_seasons.csv",
  show_col_types = FALSE
)

club_name_map <- matches |>
  distinct(opponent) |>
  arrange(opponent) |>
  mutate(
    clubelo_name = NA_character_
  )

write_csv(
  club_name_map,
  "data/processed/club_name_map.csv",
  na = ""
)

print(club_name_map, n = Inf)