library(tidyverse)

portugal_url <- "http://api.clubelo.com/POR"

portugal_ranking <- read_csv(
  portugal_url,
  show_col_types = FALSE
)

print(names(portugal_ranking))
print(portugal_ranking, n = Inf)