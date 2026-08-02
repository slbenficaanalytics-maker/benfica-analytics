library(tidyverse)
library(janitor)

fbref_schedule_raw <- read_csv(
  "data/fbref/raw/benfica_2026_27_all_comps_schedule.csv",
  show_col_types = FALSE
)

fbref_schedule_clean <- fbref_schedule_raw |>
  clean_names() |>
  filter(!is.na(date)) |>
  mutate(
    date = as.Date(date),
    goals_for = as.numeric(gf),
    goals_against = as.numeric(ga),
    possession = as.numeric(poss),
    attendance = as.numeric(attendance)
  ) |>
  select(
    date,
    time,
    competition = comp,
    round,
    day,
    venue,
    result,
    goals_for,
    goals_against,
    opponent,
    possession,
    attendance,
    captain,
    formation,
    opponent_formation = opp_formation,
    referee,
    notes
  )

write_csv(
  fbref_schedule_clean,
  "data/fbref/processed/benfica_2026_27_schedule.csv",
  na = ""
)

print(
  fbref_schedule_clean,
  n = Inf,
  width = Inf
)