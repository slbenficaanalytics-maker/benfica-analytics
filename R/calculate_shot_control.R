library(tidyverse)

shooting <- read_csv(
  "data/fbref/processed/benfica_2026_27_shooting_combined.csv",
  show_col_types = FALSE
)

shot_control <- shooting |>
  mutate(
    total_match_shots = shots + shots_against,
    
    shot_share = if_else(
      total_match_shots > 0,
      shots / total_match_shots,
      NA_real_
    ),
    
    total_match_shots_on_target =
      shots_on_target + shots_on_target_against,
    
    shot_on_target_share = if_else(
      total_match_shots_on_target > 0,
      shots_on_target / total_match_shots_on_target,
      NA_real_
    ),
    
    shot_control_index =
      100 * (
        0.5 * shot_share +
          0.5 * shot_on_target_share
      )
  ) |>
  select(
    date,
    opponent,
    goals_for,
    goals_against,
    shots,
    shots_against,
    shots_on_target,
    shots_on_target_against,
    shot_share,
    shot_on_target_share,
    shot_control_index
  )

write_csv(
  shot_control,
  "data/fbref/processed/benfica_2026_27_shot_control.csv",
  na = ""
)

shot_control |>
  mutate(
    shot_share = round(100 * shot_share, 1),
    shot_on_target_share =
      round(100 * shot_on_target_share, 1),
    shot_control_index =
      round(shot_control_index, 1)
  ) |>
  print(n = Inf, width = Inf)