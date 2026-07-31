library(tidyverse)

matches <- read_csv(
  "data/processed/benfica_matches_2026_27.csv",
  show_col_types = FALSE
)

summary_table <- matches |>
  count(venue, name = "number_of_matches")

print(summary_table)