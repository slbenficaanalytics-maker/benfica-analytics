library(tidyverse)

shooting_for <- read_csv(
  "data/fbref/processed/benfica_2026_27_shooting.csv",
  show_col_types = FALSE
)

shooting_against <- read_csv(
  "data/fbref/processed/benfica_2026_27_shooting_against.csv",
  show_col_types = FALSE
)

shooting_combined <- shooting_for |>
  left_join(
    shooting_against |>
      select(
        date,
        opponent,
        shots_against,
        shots_on_target_against,
        shot_on_target_pct_against,
        goals_per_shot_against,
        goals_per_shot_on_target_against,
        penalties_against,
        penalties_attempted_against
      ),
    by = c("date", "opponent")
  ) |>
  mutate(
    shot_difference = shots - shots_against,
    shots_on_target_difference =
      shots_on_target - shots_on_target_against,
    
    shot_accuracy = if_else(
      shots > 0,
      shots_on_target / shots,
      NA_real_
    ),
    
    opponent_shot_accuracy = if_else(
      shots_against > 0,
      shots_on_target_against / shots_against,
      NA_real_
    )
  ) |>
  arrange(date)

write_csv(
  shooting_combined,
  "data/fbref/processed/benfica_2026_27_shooting_combined.csv",
  na = ""
)

shooting_combined |>
  select(
    date,
    opponent,
    shots,
    shots_against,
    shot_difference,
    shots_on_target,
    shots_on_target_against,
    shots_on_target_difference,
    shot_accuracy,
    opponent_shot_accuracy
  ) |>
  print(n = Inf, width = Inf)