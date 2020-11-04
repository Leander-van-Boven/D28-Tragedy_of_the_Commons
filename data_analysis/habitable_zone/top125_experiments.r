library(dplyr)
library(tidyr)
library(purrr)
library(ggplot2)
library(reshape2)

dir <- '../../../CSV'

# Create `top` dataframe consisting of the top 5 experiments per csv file containing ~2000 experiments.
# There are 25 csv files, therefore `top` will contain 125 experiments.
top <- data.frame()
for (file in list.files(dir, full.names=TRUE)){
  print(file)
  
  top <- rbind(top, 
               file %>% 
                read.csv %>% 
                group_by(Exp.Num) %>% 
                mutate(score=mean(no.agents)/sd(no.agents)) %>%  # Calculate score for each experiment
                ungroup() %>% 
                mutate(rank = dense_rank(desc(score))) %>%  # Rank experiments based on their score
                filter(rank %in% 1:5) %>%  # Pick top 5 experiments
                select(-rank))
}

# Sort top 125 experiments based on their score
top <- top %>% 
  group_by(Exp.Num) %>% 
  arrange(desc(score))

# Create top 5 experiments dataframe for plotting
top5 <- top %>% 
  ungroup() %>% 
  mutate(rank = dense_rank(desc(score))) %>% 
  filter(rank %in% 1:5)

# Plot top 5 experiments
worst <- top[(118*500+1):(123*500),]
worst %>% 
  group_by(Exp.Num) %>% 
  arrange(desc(score)) %>%
  melt(id.vars=c('Exp.Num', 'Epoch'), measure.vars=c('A', 'B', 'C', 'D', 'E')) %>% 
  group_by(Exp.Num) %>% 
  ggplot(aes(x=Epoch, y=value, fill=variable)) +
  geom_area() +
  facet_wrap(~factor(Exp.Num, levels=unique(Exp.Num), labels=paste("Exp num:", unique(Exp.Num))), ncol=2) +
  theme_minimal() +
  guides(fill=guide_legend(title='SVO dist')) +
  scale_fill_discrete(labels=c('[0,.2]', '[.2,.4]', '[.4,.6]', '[.6,.8]', '[.8,1]')) +
  labs(title='Top 5 habitable zone experiments based on mean(no.agents) / sd(no.agents)', x='Epoch', y='Agent count')

# Save top 125 experiments
write.csv(top, file='../top125_habitable_experiments.csv')

# Obtain parameters of these experiments, sorted by score
top_params <- top %>% 
  group_by(Exp.Num) %>% 
  slice_head(n=1) %>% 
  arrange(desc(score))

write.csv(top_params, file='../top125_habitable_params.csv')

top5[1:10,] %>% 
  melt(id.vars=c('Exp.Num', 'Epoch'), measure.vars=c('A', 'B', 'C', 'D', 'E')) %>% 
  ggplot(aes(x=Epoch, y=value, fill=variable)) +
  geom_area() +
  theme_minimal()


top5_batch_path <- '../../top5_batch'
top5_batch_params <- data.frame()

i <- 1
for (file in list.files(top5_batch_path, full.names=TRUE)){
  print(file)
  f <- file %>% 
    read.csv() %>% 
    mutate(no.agents=A+B+C+D+E) %>%
    group_by(Exp.Num) %>% 
    mutate(score = mean(no.agents)/sd(no.agents))
  top5_batch_params <- rbind(top5_batch_params,
                             data.frame(i, mean(f$score)))
  i <- i+1
}

top125 <- read.csv('../top125_habitable_params.csv')
top125 %>% 
  ggplot(aes(x=score)) +
  geom_histogram(binwidth = 1, fill='blue') +
  theme_minimal() +
  scale_x_continuous(breaks=seq(10,34,2)) +
  scale_y_continuous(breaks=seq(0,30,5)) +
  labs(title='Histogram of simulation score of top 125 simulations', x='Score', y='Simulation Count')
