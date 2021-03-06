df.0 <- read.csv("Data/Original Model.csv")
df.1 <- read.csv("Data/Send Home.csv")
library(ggplot2)
ggplot(df.0, aes(x=Longest.Wait, y=Total.Wait)) + geom_point()
ggplot(df.0, aes(x=Longest.Wait, y=Efficiency)) + geom_point()
ggplot(df.0, aes(x=Total.Wait, y=Efficiency)) + geom_point() + stat_smooth(se = FALSE, method = 'loess', formula = y~x) + + labs(x = "Longest Wait", y = "Total Wait") + theme(legend.position = "none", text = element_text(size=20))
ggplot(df.1, aes(x=Longest.Wait, y=Total.Wait)) + geom_point() + labs(x = "Longest Wait", y = "Total Wait") + theme(legend.position = "none", text = element_text(size=20))
ggplot(df.1, aes(x=Longest.Wait, y=Efficiency)) + geom_point() + labs(x = "Longest Wait") + theme(legend.position = "none", text = element_text(size=20))
ggplot(df.1, aes(x=Total.Wait, y=Efficiency)) + geom_point() + labs(x = "Total Wait") + theme(legend.position = "none", text = element_text(size=20))

