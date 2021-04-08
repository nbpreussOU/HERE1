library(ggplot2)
library(reshape)
library(dplyr)

# create data
df.0 <- read.csv("Data/v0_data.csv")
df.1 <- read.csv("Data/v1_data.csv")
df.2 <- read.csv("Data/v2_data.csv")

# make histogram graphs
ggplot(df.0, aes(x=Efficiency, fill = ..x..)) + geom_histogram(binwidth = 1) + scale_fill_gradient(low = "red", high = "blue") +
  labs(x = "", y = "Count", title = "Efficiency in the Base Model") + theme(legend.position = "none")
ggsave("Images/EfficiencyBase.png")
ggplot(df.0, aes(x=Longest.Wait, fill = ..x..)) + geom_histogram(binwidth = 15) + scale_fill_gradient(low = "red", high = "blue") +
  labs(x = "", y = "Count", title = "Max Single Person Wait Time in the Base Model") + theme(legend.position = "none")
ggsave("Images/SPWaitBase.png")
ggplot(df.0, aes(x=Total.Wait, fill = ..x..)) + geom_histogram(binwidth = 300) + scale_fill_gradient(low = "red", high = "blue") +
  labs(x = "", y = "Count", title = "Max Total Wait Time in the Base Model") + theme(legend.position = "none")
ggsave("Images/LongWaitBase.png")

ggplot(df.1, aes(x=Efficiency, fill = ..x..)) + geom_histogram(binwidth = 1) + scale_fill_gradient(low = "red", high = "blue") +
  labs(x = "", y = "Count", title = "Efficiency in the Send Home Model") + theme(legend.position = "none")
ggsave("Images/EfficiencySH.png")
ggplot(df.1, aes(x=Longest.Wait, fill = ..x..)) + geom_histogram(binwidth = 20) + scale_fill_gradient(low = "red", high = "blue") +
  labs(x = "", y = "Count", title = "Max Single Person Wait Time in the Send Home Model") + theme(legend.position = "none")
ggsave("Images/SPWaitSH.png")
ggplot(df.1, aes(x=Total.Wait, fill = ..x..)) + geom_histogram(binwidth = 200) + scale_fill_gradient(low = "red", high = "blue") +
  labs(x = "", y = "Count", title = "Max Total Wait Time in the Send Home Model") + theme(legend.position = "none")
ggsave("Images/LongWaitSH.png")

ggplot(df.2, aes(x=Efficiency, fill = ..x..)) + geom_histogram(binwidth = .75) + scale_fill_gradient(low = "red", high = "blue") +
  labs(x = "", y = "Count", title = "Efficiency in the Distribution Change Model") + theme(legend.position = "none")
ggsave("Images/EfficiencyDist.png")
ggplot(df.2, aes(x=Longest.Wait, fill = ..x..)) + geom_histogram(binwidth = 20) + scale_fill_gradient(low = "red", high = "blue") +
  labs(x = "", y = "Count", title = "Max Single Person Wait Time in the Distribution Change Model") + theme(legend.position = "none")
ggsave("Images/SPWaitDist.png")
ggplot(df.2, aes(x=Total.Wait, fill = ..x..)) + geom_histogram(binwidth = 150) + scale_fill_gradient(low = "red", high = "blue") +
  labs(x = "", y = "Count", title = "Max Total Wait Time in the Distribution Model") + theme(legend.position = "none")
ggsave("Images/LongWaitDist.png")
