library(tidyverse)
library(rvest)

url <- "http://www.allaboutgardening.com/types-of-flowers/"

html <- read_html(url)

english <- html %>%
  html_nodes("h2") %>%
  html_attr("id") %>%
  str_replace_all("-", " ") %>% 
  as_tibble() %>%
  drop_na() %>%
  slice(1:n()-1) %>%
  rename(english = value)

latin <- html %>%
  html_nodes("em") %>%
  html_text() %>%
  as_tibble() %>%
  filter(str_detect(value, "Scientific Name")) %>%
  mutate(value = str_replace(value, "Scientific Name:", "")) %>%
  mutate(value = str_trim(value, side="both")) %>%
  rename(latin = value)
  
df <- bind_cols(english, latin) %>%
  mutate(folder_name = str_replace_all(english," ", "-")) %>%
  mutate(latin = ifelse(latin == "",english,latin))

write_csv(df, "flower_names.csv")
