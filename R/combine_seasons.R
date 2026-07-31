library(tidyverse)

matches_2025_26 <- read_csv(
  "data/processed/benfica_matches_2025_26.csv",
  show_col_types = FALSE
)

matches_2026_27 <- read_csv(
  "data/processed/benfica_matches_2026_27.csv",
  show_col_types = FALSE
)

all_matches <- bind_rows(
  matches_2025_26,
  matches_2026_27
) |>
  arrange(date)

write_csv(
  all_matches,
  "data/processed/benfica_matches_all_seasons.csv"
)

season_summary <- all_matches |>
  count(season)

print(season_summary)