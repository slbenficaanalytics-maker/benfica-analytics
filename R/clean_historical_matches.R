library(tidyverse)

historical_matches <- read_csv(
  "data/raw/benfica_primeira_liga_2025_26.csv",
  show_col_types = FALSE
)

historical_matches_clean <- historical_matches |>
  mutate(
    season = "2025/26",
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
      goals_for > goals_against ~ "Win",
      goals_for < goals_against ~ "Loss",
      TRUE ~ "Draw"
    ),
    
    points = case_when(
      result == "Win" ~ 3,
      result == "Draw" ~ 1,
      result == "Loss" ~ 0
    )
  ) |>
  select(
    match_id = id,
    season,
    date,
    status,
    matchday,
    opponent,
    venue,
    goals_for,
    goals_against,
    result,
    points,
    home_team,
    away_team
  )

write_csv(
  historical_matches_clean,
  "data/processed/benfica_matches_2025_26.csv"
)

print(historical_matches_clean, n = 10)