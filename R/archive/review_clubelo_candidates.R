library(tidyverse)

name_candidates <- read_csv(
  "data/processed/clubelo_name_candidates.csv",
  show_col_types = FALSE
)

best_candidates <- name_candidates |>
  group_by(opponent) |>
  slice_min(
    order_by = distance,
    n = 1,
    with_ties = FALSE
  ) |>
  ungroup() |>
  select(
    opponent,
    clubelo_name,
    clubelo_country,
    clubelo_elo,
    distance
  ) |>
  arrange(distance)

print(best_candidates, n = Inf)