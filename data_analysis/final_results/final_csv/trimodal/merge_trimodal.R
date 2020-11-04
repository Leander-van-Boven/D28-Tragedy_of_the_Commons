library(dplyr)

merge_csv <- function(dir, f, t){
  list.files(dir, full.names=TRUE)[t:f] %>% 
    lapply(read.csv) %>% 
    bind_rows
}
# Local CSV files produced by multi-threaded experiments
d1 <- merge_csv('../trimodal', 0, 8640)
d2 <- merge_csv('../trimodal', 8641, 17290)
d3 <- merge_csv('../trimodal', 17291, 25920)

write.csv(d1, '_1.csv')
write.csv(d2, '_2.csv')
write.csv(d3, '_3.csv')