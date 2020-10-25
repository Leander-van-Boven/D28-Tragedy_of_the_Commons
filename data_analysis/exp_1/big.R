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

# Get full data frame
d <- merge_csv(dir)

# Add agent count per epoch
d$no.agents <- d %>% 
  select(A:E) %>% 
  rowSums

no.params <- grep("Epoch", colnames(d))-1

meta <- d %>%
  group_by(Exp.Num) %>% 
  filter(max(Epoch)==max_epoch-1) %>% 
  ungroup %>% 
  group_by(across(0:no.params)) %>% 
  summarise(across(Resource:no.agents, list(mean=mean, sd=sd))) %>% 
  mutate(score=no.agents_mean/no.agents_sd) %>% 
  arrange(desc(score))
