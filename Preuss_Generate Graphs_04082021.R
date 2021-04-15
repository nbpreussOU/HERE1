library(ggplot2)
library(reshape)
library(dplyr)

# create data
df.0 <- read.csv("Data/Original Model.csv")
df.1 <- read.csv("Data/Send Home.csv")

# make histogram graphs
ggplot(df.0, aes(x=Efficiency, fill = ..x..)) + geom_histogram(binwidth = 1) + scale_fill_gradient(low = "red", high = "blue") +
  labs(x = "Percent", y = "Count", title = "Efficiency in the Base Model") + theme(legend.position = "none")+ xlim(60,101) + ylim(-1, 280)
ggsave("Images/EfficiencyBase.png")
ggplot(df.0, aes(x=Longest.Wait, fill = ..x..)) + geom_histogram(binwidth = 30) + scale_fill_gradient(low = "red", high = "blue") +
  labs(x = "Minutes", y = "Count", title = "Max Single Person Wait Time in the Base Model") + theme(legend.position = "none")  + xlim(-30, 900) + ylim(-1, 250)
ggsave("Images/SPWaitBase.png")
ggplot(df.0, aes(x=Total.Wait, fill = ..x..)) + geom_histogram(binwidth = 300) + scale_fill_gradient(low = "red", high = "blue") +
  labs(x = "Minutes", y = "Count", title = "Max Total Wait Time in the Base Model") + theme(legend.position = "none") +xlim(-300, 9000) + ylim(-1, 250)
ggsave("Images/LongWaitBase.png")

ggplot(df.1, aes(x=Efficiency, fill = ..x..)) + geom_histogram(binwidth = 1) + scale_fill_gradient(low = "red", high = "blue") +
  labs(x = "Percent", y = "Count", title = "Efficiency in the Send Home Model") + theme(legend.position = "none") + xlim(60,101) + ylim(-1, 280)
ggsave("Images/EfficiencySH.png")
ggplot(df.1, aes(x=Longest.Wait, fill = ..x..)) + geom_histogram(binwidth = 30) + scale_fill_gradient(low = "red", high = "blue") +
  labs(x = "Minutes", y = "Count", title = "Max Single Person Wait Time in the Send Home Model") + theme(legend.position = "none") +xlim(-30, 900) + ylim(-1, 250)
ggsave("Images/SPWaitSH.png")
ggplot(df.1, aes(x=Total.Wait, fill = ..x..)) + geom_histogram(binwidth = 300) + scale_fill_gradient(low = "red", high = "blue") +
  labs(x = "Minutes", y = "Count", title = "Max Total Wait Time in the Send Home Model") + theme(legend.position = "none") +xlim(-300, 9000) + ylim(-1, 250)
ggsave("Images/LongWaitSH.png")
