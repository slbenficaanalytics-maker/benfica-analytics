library(tidyverse)

performance <- read_csv(
  "data/fbref/processed/benfica_2026_27_match_performance.csv",
  show_col_types = FALSE
)

defensive_exposure <- performance |>
  mutate(
    opponent_shot_share_on_target = if_else(
      shots_against > 0,
      shots_on_target_against / shots_against,
      NA_real_
    ),
    
    exposure_index =
      100 * opponent_shot_share_on_target,
    
    goalkeeper_dependency = if_else(
      shots_on_target_against > 0,
      saves / shots_on_target_against,
      NA_real_
    )
  ) |>
  select(
    date,
    opponent,
    goals_for,
    goals_against,
    shots_against,
    shots_on_target_against,
    saves,
    save_percentage,
    exposure_index,
    goalkeeper_dependency
  )

write_csv(
  defensive_exposure,
  "data/fbref/processed/benfica_2026_27_defensive_exposure.csv",
  na = ""
)

defensive_exposure |>
  mutate(
    exposure_index = round(exposure_index, 1),
    goalkeeper_dependency = round(
      100 * goalkeeper_dependency,
      1
    )
  ) |>
  print(n = Inf, width = Inf)