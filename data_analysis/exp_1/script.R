library(ggplot2)
library(dplyr)
library(reshape2)

df <- read.csv("..\\..\\out1.csv")

df %>% 
  melt(id.vars=c('Exp.Num', 'Epoch'), measure.vars=c('A', 'B', 'C', 'D', 'E')) %>% 
  group_by(Exp.Num) %>% 
  ggplot(aes(x=Epoch, y=value, fill=variable)) +
  geom_area() +
  facet_wrap(~Exp.Num, ncol=8)
