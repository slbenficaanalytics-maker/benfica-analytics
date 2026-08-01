library(tidyverse)

squad <- read_csv(
  "data/processed/benfica_squad_current.csv",
  show_col_types = FALSE
)

squad_summary <- squad |>
  count(position, name = "number_of_players") |>
  arrange(desc(number_of_players))

print(squad_summary)

cat(
  "\nTotal de jogadores:",
  nrow(squad),
  "\n"
)