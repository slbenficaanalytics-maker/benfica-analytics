library(tidyverse)

performance <- read_csv(
  "data/fbref/processed/benfica_2026_27_match_performance.csv",
  show_col_types = FALSE
)

schedule <- read_csv(
  "data/fbref/processed/benfica_2026_27_schedule.csv",
  show_col_types = FALSE
)

match_context <- performance |>
  left_join(
    schedule |>
      select(
        date,
        opponent,
        time,
        possession,
        attendance,
        captain,
        formation,
        opponent_formation,
        referee,
        notes
      ),
    by = c("date", "opponent")
  ) |>
  mutate(
    possession_against = if_else(
      !is.na(possession),
      100 - possession,
      NA_real_
    )
  ) |>
  arrange(date)

write_csv(
  match_context,
  "data/fbref/processed/benfica_2026_27_match_context.csv",
  na = ""
)

match_context |>
  select(
    date,
    opponent,
    competition,
    goals_for,
    goals_against,
    possession,
    possession_against,
    shots,
    shots_against,
    formation,
    opponent_formation,
    captain,
    referee
  ) |>
  print(n = Inf, width = Inf)