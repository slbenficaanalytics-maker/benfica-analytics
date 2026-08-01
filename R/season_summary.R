library(tidyverse)

matches <- read_csv(
  "data/processed/benfica_matches_all_seasons.csv",
  show_col_types = FALSE
)

season_summary <- matches |>
  filter(
    season == "2025/26",
    status == "FINISHED"
  ) |>
  summarise(
    games = n(),
    wins = sum(result == "Win"),
    draws = sum(result == "Draw"),
    losses = sum(result == "Loss"),
    goals_for = sum(goals_for),
    goals_against = sum(goals_against),
    goal_difference = goals_for - goals_against,
    points = sum(points),
    points_per_game = round(points / games, 2)
  )

print(season_summary)