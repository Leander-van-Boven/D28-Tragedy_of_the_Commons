library(dplyr)
library(tidyr)
library(purrr)
library(ggplot2)

# Repository root folder: ../../

# Merge all CSV files in directory `dir` into single data frame.
merge_csv <- function(dir){
  list.files(dir, full.names=TRUE) %>% 
    lapply(read.csv) %>% 
    bind_rows
}

for (i in seq(3e+06, 24e+06, 1e+06)){
  print(i/1e+06)
  j <- i + 1e+06
  if (j > nrow(d)){
    j <- nrow(d)
  }
  fn <- paste('../_', as.character(i/1e+06), '.csv', sep='')
  d_sub <- d %>% slice((i+1):j)
  write.csv(d_sub, file=fn)
}



d1 <- merge_csv('../../big_test', 1, 2000)


# Parameters:
dir <- '../../big_test'
max_epoch <- 500
no_params <- 9

d <- read.csv('../_full.csv')

# Filter out all experiments where all agents died
d <- d %>% 
  mutate(no.agents=A+B+C+D+E) %>% 
  group_by(Exp.Num) %>% 
  filter(max(Epoch)==max_epoch-1) %>% 
  ungroup 
write.csv(d, '../_full.csv')

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


d_gr <- d %>% 
  slice_sample(n=1000) %>% 
  arrange(Exp.Num) %>% 
  mutate(Exp.Id = 0) %>% 
  mutate(
    Exp.Id = coalesce(ifelse(Exp.Num==lag(Exp.Num), lag(Exp.Id), lag(Exp.Id)+1), 1)
    ) %>% 
  select(Exp.Num, Exp.Id)






test <- function(curr, lag){
  switch(as.character(curr==lag), "NA"=0, "TRUE"=1, "FALSE"=2)
}



analyze_exp <- function(dir, max_epoch, no_params){
  merge_csv(dir) %>% 
    mutate(no.agents=A+B+C+D+E) %>% 
    group_by(Exp.Num) %>% 
    filter(max(Epoch)==max_epoch-1) %>% 
    ungroup %>% 
    group_by(across(0:no_params+1)) %>% 
    summarise(across(Resource:no.agents, list(mean=mean, sd=sd))) %>% 
    mutate(score=no.agents_mean/no.agents_sd) %>% 
    arrange(desc(score))
}

