# Script para obter jogos do Benfica através de uma API
library(httr2)
library(tidyverse)

token <- Sys.getenv("FOOTBALL_DATA_TOKEN")

request <- request("https://api.football-data.org/v4/competitions") |>
  req_headers("X-Auth-Token" = token)

response <- req_perform(request)

competitions <- response |>
  resp_body_json(simplifyVector = TRUE)

competitions_table <- competitions$competitions |>
  as_tibble() |>
  select(id, name, code, type)

print(competitions_table, n = Inf)

matches_request <- request(
  "https://api.football-data.org/v4/competitions/PPL/matches"
) |>
  req_headers("X-Auth-Token" = token)

matches_response <- req_perform(matches_request)

matches_data <- matches_response |>
  resp_body_json(simplifyVector = TRUE)

matches_simple <- matches_table |>
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

print(matches_simple, n = 20)

benfica_matches <- matches_simple |>
  filter(
    home_team == "Sport Lisboa e Benfica" |
      away_team == "Sport Lisboa e Benfica"
  )

print(benfica_matches, n = Inf)

write_csv(
  benfica_matches,
  "data/raw/benfica_primeira_liga_2026_27.csv"
)

jsonlite::write_json(
  matches_data,
  "data/raw/primeira_liga_2026_27_raw.json",
  pretty = TRUE,
  auto_unbox = TRUE
)