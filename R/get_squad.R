library(httr2)
library(tidyverse)

token <- Sys.getenv("FOOTBALL_DATA_TOKEN")

team_id <- 1903

squad_request <- request(
  paste0(
    "https://api.football-data.org/v4/teams/",
    team_id
  )
) |>
  req_headers("X-Auth-Token" = token)

squad_response <- req_perform(squad_request)

squad_data <- squad_response |>
  resp_body_json(simplifyVector = TRUE)

print(names(squad_data))
print(squad_data$name)
print(squad_data$squad)

squad_table <- squad_data$squad |>
  as_tibble() |>
  select(
    player_id = id,
    player_name = name,
    position,
    date_of_birth = dateOfBirth,
    nationality
  )

write_csv(
  squad_table,
  "data/raw/benfica_squad_current.csv"
)

print(squad_table, n = Inf)