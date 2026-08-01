library(tidyverse)

match_input_template <- tibble(
  match_id = numeric(),
  date = as.Date(character()),
  opponent = character(),
  venue = character(),
  
  goals_for = numeric(),
  goals_against = numeric(),
  
  possession_for = numeric(),
  possession_against = numeric(),
  
  shots_for = numeric(),
  shots_against = numeric(),
  
  shots_on_target_for = numeric(),
  shots_on_target_against = numeric(),
  
  shots_inside_box_for = numeric(),
  shots_inside_box_against = numeric(),
  
  big_chances_for = numeric(),
  big_chances_against = numeric(),
  
  xg_for = numeric(),
  xg_against = numeric(),
  
  corners_for = numeric(),
  corners_against = numeric(),
  
  lineup_changes = numeric(),
  new_signings_starting = numeric(),
  new_signings_minutes = numeric(),
  
  scored_first = logical(),
  minute_first_goal = numeric(),
  
  red_card_for = numeric(),
  red_card_against = numeric(),
  
  data_source = character(),
  notes = character()
)

write_csv(
  match_input_template,
  "data/manual/match_input.csv",
  na = ""
)