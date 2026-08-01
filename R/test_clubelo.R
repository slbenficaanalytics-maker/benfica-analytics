library(tidyverse)

clubelo_url <- "http://api.clubelo.com/2026-08-01"

clubelo_ranking <- read_csv(
  clubelo_url,
  show_col_types = FALSE
)

print(names(clubelo_ranking))

clubelo_ranking |>
  filter(Country == "POR") |>
  select(Rank, Club, Country, Elo) |>
  print(n = Inf)