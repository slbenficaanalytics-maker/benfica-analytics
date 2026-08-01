library(httr2)
library(tidyverse)

token <- Sys.getenv("FOOTBALL_DATA_TOKEN")

team_matches_request <- request(
  "https://api.football-data.org/v4/teams/1903/matches"
) |>
  req_url_query(
    dateFrom = "2026-07-01",
    dateTo = "2026-08-31"
  ) |>
  req_headers("X-Auth-Token" = token)

team_matches_response <- req_perform(team_matches_request)

team_matches_data <- team_matches_response |>
  resp_body_json(simplifyVector = TRUE)

print(team_matches_data$resultSet$count)
print(team_matches_data$matches)