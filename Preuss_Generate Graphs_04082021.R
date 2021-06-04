library(ggplot2)
library(reshape)
library(dplyr)

# create data
df.0 <- read.csv("Data/Original Model.csv")
df.1 <- read.csv("Data/Send Home.csv")

# make histogram graphs
ggplot(df.0, aes(x=Efficiency, fill = ..x..)) + geom_histogram(binwidth = 1) + scale_fill_gradient(low = "red", high = "blue") +
  labs(x = "Percent", y = "Count") + theme(legend.position = "none", text = element_text(size=20))
ggsave("Images/EfficiencyBase.png")
ggplot(df.0, aes(x=Longest.Wait, fill = ..x..)) + geom_histogram(binwidth = 9) + scale_fill_gradient(low = "red", high = "blue") +
  labs(x = "Minutes", y = "Count") + theme(legend.position = "none", text = element_text(size=20))
ggsave("Images/SPWaitBase.png")
ggplot(df.0, aes(x=Total.Wait, fill = ..x..)) + geom_histogram(binwidth = 150) + scale_fill_gradient(low = "red", high = "blue") +
  labs(x = "Minutes", y = "Count") + theme(legend.position = "none", text = element_text(size=20))
ggsave("Images/LongWaitBase.png")

ggplot(df.1, aes(x=Efficiency, fill = ..x..)) + geom_histogram(binwidth = 1) + scale_fill_gradient(low = "red", high = "blue") +
  labs(x = "Percent", y = "Count") + theme(legend.position = "none", text = element_text(size=20))
ggsave("Images/EfficiencySH.png")
ggplot(df.1, aes(x=Longest.Wait, fill = ..x..)) + geom_histogram(binwidth = 9) + scale_fill_gradient(low = "red", high = "blue") +
  labs(x = "Minutes", y = "Count") + theme(legend.position = "none", text = element_text(size=20))
ggsave("Images/SPWaitSH.png")
ggplot(df.1, aes(x=Total.Wait, fill = ..x..)) + geom_histogram(binwidth = 150) + scale_fill_gradient(low = "red", high = "blue") +
  labs(x = "Minutes", y = "Count") + theme(legend.position = "none", text = element_text(size=20))
ggsave("Images/LongWaitSH.png")
