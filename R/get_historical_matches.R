library(httr2)
library(tidyverse)
library(jsonlite)

token <- Sys.getenv("FOOTBALL_DATA_TOKEN")

historical_request <- request(
  "https://api.football-data.org/v4/competitions/PPL/matches"
) |>
  req_url_query(season = 2025) |>
  req_headers("X-Auth-Token" = token)

historical_response <- req_perform(historical_request)

historical_data <- historical_response |>
  resp_body_json(simplifyVector = TRUE)

historical_table <- historical_data$matches |>
  as_tibble() |>
  mutate(
    home_team = homeTeam$name,
    away_team = awayTeam$name,
    home_goals = score$fullTime$home,
    away_goals = score$fullTime$away
  ) |>
  select(
    id,
    utcDate,
    status,
    matchday,
    home_team,
    away_team,
    home_goals,
    away_goals
  )

benfica_historical <- historical_table |>
  filter(
    home_team == "Sport Lisboa e Benfica" |
      away_team == "Sport Lisboa e Benfica"
  )

write_csv(
  benfica_historical,
  "data/raw/benfica_primeira_liga_2025_26.csv"
)

jsonlite::write_json(
  historical_data,
  "data/raw/primeira_liga_2025_26_raw.json",
  pretty = TRUE,
  auto_unbox = TRUE
)

print(benfica_historical, n = Inf)