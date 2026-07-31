library(tidyverse)

benfica_matches <- read_csv(
  "data/raw/benfica_primeira_liga_2026_27.csv",
  show_col_types = FALSE
)

benfica_matches_clean <- benfica_matches |>
  mutate(
    date = as.Date(utcDate),
    
    opponent = if_else(
      home_team == "Sport Lisboa e Benfica",
      away_team,
      home_team
    ),
    
    venue = if_else(
      home_team == "Sport Lisboa e Benfica",
      "Home",
      "Away"
    ),
    
    goals_for = if_else(
      home_team == "Sport Lisboa e Benfica",
      home_goals,
      away_goals
    ),
    
    goals_against = if_else(
      home_team == "Sport Lisboa e Benfica",
      away_goals,
      home_goals
    ),
    
    result = case_when(
      is.na(goals_for) | is.na(goals_against) ~ NA_character_,
      goals_for > goals_against ~ "Win",
      goals_for < goals_against ~ "Loss",
      TRUE ~ "Draw"
    )
  ) |>
  select(
    match_id = id,
    date,
    status,
    matchday,
    opponent,
    venue,
    goals_for,
    goals_against,
    result,
    home_team,
    away_team
  )

write_csv(
  benfica_matches_clean,
  "data/processed/benfica_matches_2026_27.csv"
)

print(benfica_matches_clean, n = 10)