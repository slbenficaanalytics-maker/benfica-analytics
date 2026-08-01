library(tidyverse)
library(janitor)

fbref_against_raw <- read_csv(
  "data/fbref/raw/benfica_2026_27_all_comps_shooting_against.csv",
  skip = 1,
  show_col_types = FALSE
)

fbref_against_clean <- fbref_against_raw |>
  clean_names() |>
  filter(!is.na(date)) |>
  mutate(
    date = as.Date(date),
    goals_against = as.numeric(gf),
    goals_for = as.numeric(ga),
    shots_against = as.numeric(sh),
    shots_on_target_against = as.numeric(so_t),
    shot_on_target_pct_against = as.numeric(so_t_percent),
    goals_per_shot_against = as.numeric(g_sh),
    goals_per_shot_on_target_against = as.numeric(g_so_t)
  ) |>
  select(
    date,
    competition = comp,
    round,
    venue,
    result,
    goals_for,
    goals_against,
    opponent,
    shots_against,
    shots_on_target_against,
    shot_on_target_pct_against,
    goals_per_shot_against,
    goals_per_shot_on_target_against,
    penalties_against = pk,
    penalties_attempted_against = p_katt
  )

write_csv(
  fbref_against_clean,
  "data/fbref/processed/benfica_2026_27_shooting_against.csv",
  na = ""
)

print(fbref_against_clean, n = Inf, width = Inf)