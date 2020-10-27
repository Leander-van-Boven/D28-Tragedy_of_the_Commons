library(dplyr)
library(tidyr)
library(purrr)
library(ggplot2)

# Repository root folder: ../../

# Parameters:
dir <- '../../big_test'
max_epoch <- 500
no_params <- 9

# Merge all CSV files in directory `dir` into single data frame.
merge_csv <- function(dir){
  list.files(dir, full.names=TRUE) %>% 
    lapply(read.csv) %>% 
    bind_rows
}

# Read full csv
d <- read.csv('../_full.csv')

# Filter out all experiments where all agents died
d <- d %>% 
  mutate(no.agents=A+B+C+D+E) %>% 
  group_by(Exp.Num) %>% 
  filter(max(Epoch)==max_epoch-1) %>% 
  ungroup 
write.csv(d, '../_full.csv')


# From full csv, split into groups of 2000 experiments
iter <- max_epoch * 2000
final <- (nrow(d) %/% iter) * iter
for (i in seq(0, final, iter)){
  print(i/iter)
  j <- i + iter
  if (j > nrow(d)){
    j <- nrow(d)
  }
  fn <- paste('../_', as.character(i/iter), '.csv', sep='')
  d_sub <- d %>% slice((i+1):j)
  write.csv(d_sub, file=fn)
}

# Summarize and score each experiment. Warning: This WILL use >28GB of memory.
# If you don't have at least 32GB or memory, R will crash.
d %>% 
  group_by(across(0:no_params+1)) %>% 
  summarise(across(Resource:no.agents, list(mean=mean, sd=sd))) %>% 
  mutate(score=no.agents_mean/no.agents_sd) %>% 
  arrange(desc(score))
  


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

