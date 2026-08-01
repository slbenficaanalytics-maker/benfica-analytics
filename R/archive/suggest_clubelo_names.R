library(tidyverse)
library(stringdist)

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

normalize_name <- function(x) {
  x |>
    str_to_lower() |>
    stringi::stri_trans_general("Latin-ASCII") |>
    str_replace_all(
      "\\b(fc|cf|cd|gd|sc|ac|clube|club|sporting|praia)\\b",
      " "
    ) |>
    str_replace_all("[^a-z0-9 ]", " ") |>
    str_squish()
}

opponents_normalized <- club_name_map |>
  mutate(
    opponent_normalized = normalize_name(opponent)
  )

clubelo_normalized <- clubelo_ranking |>
  mutate(
    clubelo_normalized = normalize_name(Club)
  )

name_candidates <- opponents_normalized |>
  select(opponent, opponent_normalized) |>
  crossing(
    clubelo_normalized |>
      select(
        clubelo_name = Club,
        clubelo_country = Country,
        clubelo_elo = Elo,
        clubelo_normalized
      )
  ) |>
  mutate(
    distance = stringdist(
      opponent_normalized,
      clubelo_normalized,
      method = "jw"
    )
  ) |>
  group_by(opponent) |>
  slice_min(
    order_by = distance,
    n = 5,
    with_ties = FALSE
  ) |>
  ungroup() |>
  arrange(opponent, distance)

write_csv(
  name_candidates,
  "data/processed/clubelo_name_candidates.csv"
)

print(name_candidates, n = Inf)