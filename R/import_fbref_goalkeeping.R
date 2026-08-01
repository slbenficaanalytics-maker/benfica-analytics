library(tidyverse)
library(janitor)

fbref_goalkeeping_raw <- read_csv(
  "data/fbref/raw/benfica_2026_27_all_comps_goalkeeping.csv",
  skip = 1,
  show_col_types = FALSE
)

fbref_goalkeeping_clean <- fbref_goalkeeping_raw |>
  clean_names() |>
  filter(!is.na(date)) |>
  mutate(
    date = as.Date(date),
    goals_for = as.numeric(gf),
    goals_against = as.numeric(ga_9),
    shots_on_target_against = as.numeric(so_ta),
    saves = as.numeric(saves),
    save_percentage = as.numeric(save_percent),
    clean_sheet = as.numeric(cs),
    penalties_faced = as.numeric(p_katt),
    penalties_conceded = as.numeric(pka),
    penalties_saved = as.numeric(p_ksv),
    penalties_missed = as.numeric(p_km)
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
    shots_on_target_against,
    saves,
    save_percentage,
    clean_sheet,
    penalties_faced,
    penalties_conceded,
    penalties_saved,
    penalties_missed
  )

write_csv(
  fbref_goalkeeping_clean,
  "data/fbref/processed/benfica_2026_27_goalkeeping.csv",
  na = ""
)

print(
  fbref_goalkeeping_clean,
  n = Inf,
  width = Inf
)