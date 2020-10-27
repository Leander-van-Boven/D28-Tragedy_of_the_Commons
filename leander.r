library(dplyr)

x <- seq(1,1000)
y <- seq(1,1000)

df <- data.frame(x, y)

for (i in 0:19){
    print(nrow(df[((i*10)+1):((i+1)*10),]))
}