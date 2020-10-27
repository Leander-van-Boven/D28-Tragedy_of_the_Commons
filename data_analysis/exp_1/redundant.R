library(dplyr)
library(tidyr)
library(purrr)
library(ggplot2)


# Split the data up into blocks of five experiments
no_row <- (max_epoch * 2000) + 1
d_gr <- d %>%
  arrange(Exp.Num) %>% 
  group_by(row_number()-1 %/% no_row) %>% 
  nest %>% pull(data)

# Function to cope with hiati in Exp.Num
Num.To.Id <- function(x){
  x$Exp.Id <- 1
  x$Exp.Id[1] <- 1
  for (i in 2:nrow(x)){
    if (x$Exp.Num[i-1]==x$Exp.Num[i]){
      x$Exp.Id[i] = x$Exp.Id[i-1]
    } else {
      x$Exp.Id[i] = x$Exp.Id[i-1] + 1
    }
  }
  return(x)
}

d_gr <- Num.To.Id(d %>% arrange(Exp.Num)) %>% 
  group_by((Exp.Id) %/% (length(unique(Exp.Id))/20)) %>%
  nest %>% pull(data)

# Split into 20 parts
dspl <- d %>% 
  arrange(Exp.Num) %>% 
  group_by((Exp.Num) %/% (length(unique(Exp.Num))/2)) %>%
  nest %>% pull(data)

test <- function(curr, lag){
  switch(as.character(curr==lag), "NA"=0, "TRUE"=1, "FALSE"=2)
}


d_gr <- d %>% 
  slice_sample(n=1000) %>% 
  arrange(Exp.Num) %>% 
  mutate(Exp.Id = 0) %>% 
  mutate(
    Exp.Id = coalesce(ifelse(Exp.Num==lag(Exp.Num), lag(Exp.Id), lag(Exp.Id)+1), 1)
  ) %>% 
  select(Exp.Num, Exp.Id)



