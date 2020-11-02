library(dplyr)

d <- read.csv('../trimodal.csv')
merge_csv <- function(dir, f, t){
  list.files(dir, full.names=TRUE)[t:f] %>% 
    lapply(read.csv) %>% 
    bind_rows
}
d1 <- merge_csv('../trimodal', 0, 8640)
d2 <- merge_csv('../trimodal', 8641, 17290)
d3 <- merge_csv('../trimodal', 17291, 25920)

write.csv(d1, '../trimodal/_1.csv')
write.csv(d2, '../trimodal/_2.csv')
write.csv(d3, '../trimodal/_3.csv')