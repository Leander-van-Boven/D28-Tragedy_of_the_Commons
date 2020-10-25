library(dplyr)
library(ggplot2)

# Repository root folder: ../../

# Merge all CSV files in directory `dir` into single data frame.
merge_csv <- function(dir){
  list.files(dir, full.names=TRUE) %>% 
    lapply(read.csv) %>% 
    bind_rows
}

# Parameters:
dir <- '../../big_test'
max_epoch <- 500
no_params <- 9

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

