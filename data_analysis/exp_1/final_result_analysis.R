library(dplyr)
library(tidyr)
library(purrr)
library(ggplot2)
library(reshape2)

dir <- '../../final_results/final_csv'

# Create `top` dataframe consisting of the top 5 experiments per csv file containing ~2000 experiments.
# There are 25 csv files, therefore `top` will contain 125 experiments.

unifile <- paste(dir, '/unimodal.csv', sep='')
bifile <- paste(dir, '/bimodal.csv', sep='')

uni <- read.csv(unifile)
bi <- read.csv(bifile)

uni_dist_num <- 15
uni_mean <- uni %>% 
  group_by(Exp.Num %% uni_dist_num, Epoch) %>% 
  summarise(across(Resource:STD, list(mean=mean, sd=sd)))
  