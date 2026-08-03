library(tidyverse)
library(janitor)

read_fbref_player_table <- function(path, prefix) {
  
  read_csv(
    path,
    skip = 1,
    show_col_types = FALSE
  ) |>
    clean_names() |>
    filter(
      !is.na(player),
      player != ""
    ) |>
    rename(
      player_id = x9999
    ) |>
    select(
      -matches
    ) |>
    rename_with(
      ~ paste0(prefix, "__", .x),
      -c(
        player,
        nation,
        pos,
        age,
        player_id
      )
    )
}

standard <- read_fbref_player_table(
  "data/fbref/raw/benfica_2025_26_standard.csv",
  "standard"
)

playing_time <- read_fbref_player_table(
  "data/fbref/raw/benfica_2025_26_playing_time.csv",
  "playing_time"
)

miscellaneous <- read_fbref_player_table(
  "data/fbref/raw/benfica_2025_26_miscellaneous.csv",
  "miscellaneous"
)

players <- standard |>
  full_join(
    playing_time,
    by = c(
      "player",
      "nation",
      "pos",
      "age",
      "player_id"
    )
  ) |>
  full_join(
    miscellaneous,
    by = c(
      "player",
      "nation",
      "pos",
      "age",
      "player_id"
    )
  ) |>
  arrange(
    desc(standard__min),
    player
  )

dir.create(
  "data/fbref/processed",
  recursive = TRUE,
  showWarnings = FALSE
)

write_csv(
  standard,
  "data/fbref/processed/benfica_2025_26_standard.csv"
)

write_csv(
  playing_time,
  "data/fbref/processed/benfica_2025_26_playing_time.csv"
)

write_csv(
  miscellaneous,
  "data/fbref/processed/benfica_2025_26_miscellaneous.csv"
)

write_csv(
  players,
  "data/fbref/processed/benfica_2025_26_player_season.csv"
)

cat("Jogadores em Standard:", nrow(standard), "\n")
cat("Jogadores em Playing Time:", nrow(playing_time), "\n")
cat("Jogadores em Miscellaneous:", nrow(miscellaneous), "\n")
cat("Jogadores combinados:", nrow(players), "\n")
cat("Colunas combinadas:", ncol(players), "\n")