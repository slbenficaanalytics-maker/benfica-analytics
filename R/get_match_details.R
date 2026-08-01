library(httr2)
library(tidyverse)

token <- Sys.getenv("FOOTBALL_DATA_TOKEN")

match_id <- 545717

match_request <- request(
  paste0(
    "https://api.football-data.org/v4/matches/",
    match_id
  )
) |>
  req_headers(
    "X-Auth-Token" = token,
    "X-Unfold-Lineups" = "true",
    "X-Unfold-Bookings" = "true",
    "X-Unfold-Subs" = "true",
    "X-Unfold-Goals" = "true"
  )

match_response <- req_perform(match_request)

match_data <- match_response |>
  resp_body_json(simplifyVector = TRUE)

print(names(match_data))