library(ggplot2)
library(reshape)
library(dplyr)

# creates graphs for the project

# read in data
df.0 <- read.csv("Data/Original Model.csv")
df.1 <- read.csv("Data/Send Home.csv")
df.max <- read.csv("Data/v3_max_data.csv")
df.mean <- read.csv("Data/v3_mean_data.csv")
df.max$Model <- "Max"
df.mean$Model <- "Mean"
df <- rbind(df.max, df.mean)

# make histogram graphs
ggplot(df.0, aes(x=Efficiency, fill = ..x..)) + geom_histogram(binwidth = 1) + scale_fill_gradient(low = "red", high = "blue") +
  labs(x = "Percent Efficient", y = "Count") + theme(legend.position = "none", text = element_text(size=20))
ggsave("Images/EfficiencyBase.png")

ggplot(df.1, aes(x=Efficiency, fill = ..x..)) + geom_histogram(binwidth = 1) + scale_fill_gradient(low = "red", high = "blue") +
  labs(x = "Percent Efficient", y = "Count") + theme(legend.position = "none", text = element_text(size=20))
ggsave("Images/EfficiencySH.png")

# make correlation graphs
ggplot(df.0, aes(x=Longest.Wait, y=Total.Wait)) + geom_point() +
  labs(x = "Longest Single Patient Wait Time", y = "Total Wait") + theme(legend.position = "none", text = element_text(size=20))
ggsave("Images/LWTWBase.png")

ggplot(df.1, aes(x=Longest.Wait, y=Total.Wait)) + geom_point() +
  labs(x = "Longest Single Patient Wait Time", y = "Total Wait") + theme(legend.position = "none", text = element_text(size=20))
ggsave("Images/LWTWSH.png")

# linear best fit
ggplot(data = df, aes(x=Standard.Deviation, y=Efficiency, fill=Model)) + stat_smooth(se = FALSE, method = 'loess', formula = y~x) +
  geom_point(pch=21) + theme(text = element_text(size=20)) +   labs(x = "Standard Deviation", y = "Efficiency")
ggsave("Images/lmEfficiency.png")
# exponential best fit
ggplot(data = df, aes(x=Standard.Deviation, y=log(Longest.Wait), fill=Model)) + stat_smooth(se = FALSE, method = 'loess', formula = y~x) +
  geom_point(pch=21) + theme(text = element_text(size=20)) + labs(x = "Standard Deviation", y = "Longest Single Patient Wait Time")
ggsave("Images/LogLongestWait.png")
ggplot(data = df, aes(x=Standard.Deviation, y=log(Total.Wait), fill=Model)) + stat_smooth(se = FALSE, method = 'loess', formula = y~x) +
  geom_point(pch=21) + theme(text = element_text(size=20)) + labs(x = "Standard Deviation", y = "Total Wait Time")
ggsave("Images/LogTotalWait.png")