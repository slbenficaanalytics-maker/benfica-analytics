library(tidyverse)

shooting <- read_csv(
  "data/fbref/processed/benfica_2026_27_shooting_combined.csv",
  show_col_types = FALSE
)

goalkeeping <- read_csv(
  "data/fbref/processed/benfica_2026_27_goalkeeping.csv",
  show_col_types = FALSE
)

match_performance <- shooting |>
  left_join(
    goalkeeping |>
      select(
        date,
        opponent,
        saves,
        save_percentage,
        clean_sheet
      ),
    by = c("date", "opponent")
  ) |>
  mutate(
    defensive_exposure = if_else(
      shots_against > 0,
      shots_on_target_against / shots_against,
      NA_real_
    ),
    
    goalkeeper_workload = shots_on_target_against,
    
    saves_per_10_opponent_shots = if_else(
      shots_against > 0,
      10 * saves / shots_against,
      NA_real_
    )
  ) |>
  arrange(date)

write_csv(
  match_performance,
  "data/fbref/processed/benfica_2026_27_match_performance.csv",
  na = ""
)

match_performance |>
  select(
    date,
    opponent,
    goals_for,
    goals_against,
    shots_against,
    shots_on_target_against,
    defensive_exposure,
    goalkeeper_workload,
    saves,
    save_percentage,
    saves_per_10_opponent_shots,
    clean_sheet
  ) |>
  mutate(
    defensive_exposure = round(
      100 * defensive_exposure,
      1
    ),
    saves_per_10_opponent_shots = round(
      saves_per_10_opponent_shots,
      2
    )
  ) |>
  print(n = Inf, width = Inf)