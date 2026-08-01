library(tidyverse)
library(janitor)

fbref_shooting_raw <- read_csv(
  "data/fbref/raw/benfica_2026_27_all_comps_shooting.csv",
  skip = 1,
  show_col_types = FALSE
)

fbref_shooting_clean <- fbref_shooting_raw |>
  clean_names() |>
  filter(!is.na(date)) |>
  mutate(
    date = as.Date(date),
    venue = recode(
      venue,
      "Home" = "Home",
      "Away" = "Away"
    ),
    goals_for = as.numeric(gf),
    goals_against = as.numeric(ga),
    shots = as.numeric(sh),
    shots_on_target = as.numeric(so_t),
    shot_on_target_pct = as.numeric(so_t_percent),
    goals_per_shot = as.numeric(g_sh),
    goals_per_shot_on_target = as.numeric(g_so_t)
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
    goals = gls,
    shots,
    shots_on_target,
    shot_on_target_pct,
    goals_per_shot,
    goals_per_shot_on_target,
    penalties_scored = pk,
    penalties_attempted = p_katt
  )

write_csv(
  fbref_shooting_clean,
  "data/fbref/processed/benfica_2026_27_shooting.csv",
  na = ""
)

print(fbref_shooting_clean, n = Inf)