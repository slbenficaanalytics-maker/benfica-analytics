library(tidyverse)

match_context <- read_csv(
  "data/fbref/processed/benfica_2026_27_match_context.csv",
  show_col_types = FALSE
)

possession_efficiency <- match_context |>
  mutate(
    total_match_shots = shots + shots_against,
    
    shot_share = if_else(
      total_match_shots > 0,
      shots / total_match_shots,
      NA_real_
    ),
    
    possession_share = possession / 100,
    
    possession_to_shot_gap =
      100 * (possession_share - shot_share),
    
    shots_per_10_possession_points = if_else(
      possession > 0,
      10 * shots / possession,
      NA_real_
    ),
    
    sterile_possession_flag = case_when(
      is.na(possession_to_shot_gap) ~ NA,
      possession >= 55 &
        possession_to_shot_gap >= 10 ~ TRUE,
      TRUE ~ FALSE
    )
  ) |>
  select(
    date,
    opponent,
    goals_for,
    goals_against,
    possession,
    shots,
    shots_against,
    shot_share,
    possession_to_shot_gap,
    shots_per_10_possession_points,
    sterile_possession_flag
  )

write_csv(
  possession_efficiency,
  "data/fbref/processed/benfica_2026_27_possession_efficiency.csv",
  na = ""
)

possession_efficiency |>
  mutate(
    shot_share = round(100 * shot_share, 1),
    possession_to_shot_gap = round(
      possession_to_shot_gap,
      1
    ),
    shots_per_10_possession_points = round(
      shots_per_10_possession_points,
      2
    )
  ) |>
  print(n = Inf, width = Inf)