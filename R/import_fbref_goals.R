library(tidyverse)
library(janitor)

process_goals <- function(path, goal_type) {
  
  read_csv(
    path,
    show_col_types = FALSE
  ) |>
    clean_names() |>
    mutate(
      goal_type = goal_type,
      
      date = as.Date(date),
      
      minute_text = as.character(minute),
      
      minute_base = as.numeric(
        str_extract(minute_text, "^\\d+")
      ),
      
      added_time = as.numeric(
        str_extract(minute_text, "(?<=\\+)\\d+")
      ),
      
      added_time = replace_na(added_time, 0),
      
      match_minute = minute_base + added_time,
      
      starter = case_when(
        str_detect(start, "^Y") ~ TRUE,
        start == "N" ~ FALSE,
        TRUE ~ NA
      ),
      
      score_before_home = as.numeric(
        str_extract(score, "^\\d+")
      ),
      
      score_before_away = as.numeric(
        str_extract(score, "\\d+$")
      )
    ) |>
    select(
      goal_type,
      date,
      comp,
      round,
      venue,
      scorer,
      opponent,
      starter,
      minute_text,
      minute_base,
      added_time,
      match_minute,
      score,
      score_before_home,
      score_before_away,
      goalkeeper,
      assist,
      notes
    )
}

goals_for <- process_goals(
  "data/fbref/raw/benfica_2025_26_goals_for.csv",
  "For"
)

goals_against <- process_goals(
  "data/fbref/raw/benfica_2025_26_goals_against.csv",
  "Against"
)

goals <- bind_rows(
  goals_for,
  goals_against
) |>
  arrange(
    date,
    match_minute,
    goal_type
  )

dir.create(
  "data/fbref/processed",
  recursive = TRUE,
  showWarnings = FALSE
)

write_csv(
  goals_for,
  "data/fbref/processed/benfica_2025_26_goals_for.csv"
)

write_csv(
  goals_against,
  "data/fbref/processed/benfica_2025_26_goals_against.csv"
)

write_csv(
  goals,
  "data/fbref/processed/benfica_2025_26_goals_combined.csv"
)

cat("Golos marcados:", nrow(goals_for), "\n")
cat("Golos sofridos:", nrow(goals_against), "\n")
cat("Total combinado:", nrow(goals), "\n")
cat(
  "Jogos distintos:",
  goals |>
    distinct(date, opponent) |>
    nrow(),
  "\n"
)