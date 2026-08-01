library(worldfootballR)
library(tidyverse)

benfica_url <- "https://fbref.com/en/squads/a77c513e/2025-2026/matchlogs/c32/shooting/Benfica-Match-Logs-Primeira-Liga"

fbref_matches <- fb_team_match_log_stats(
  team_urls = benfica_url,
  stat_type = "shooting",
  time_pause = 5
)

print(names(fbref_matches))
print(fbref_matches, n = 5)