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
  labs(x = "Percent", y = "Count") + theme(legend.position = "none", text = element_text(size=20))
ggsave("Images/EfficiencyBase.png")
ggplot(df.0, aes(x=Longest.Wait, fill = ..x..)) + geom_histogram(binwidth = 8) + scale_fill_gradient(low = "red", high = "blue") +
  labs(x = "Minutes", y = "Count") + theme(legend.position = "none", text = element_text(size=20))
ggsave("Images/SPWaitBase.png")
ggplot(df.0, aes(x=Total.Wait, fill = ..x..)) + geom_histogram(binwidth = 100) + scale_fill_gradient(low = "red", high = "blue") +
  labs(x = "Minutes", y = "Count") + theme(legend.position = "none", text = element_text(size=20))
ggsave("Images/LongWaitBase.png")

ggplot(df.1, aes(x=Efficiency, fill = ..x..)) + geom_histogram(binwidth = 1) + scale_fill_gradient(low = "red", high = "blue") +
  labs(x = "Percent", y = "Count") + theme(legend.position = "none", text = element_text(size=20))
ggsave("Images/EfficiencySH.png")
ggplot(df.1, aes(x=Longest.Wait, fill = ..x..)) + geom_histogram(binwidth = 8) + scale_fill_gradient(low = "red", high = "blue") +
  labs(x = "Minutes", y = "Count") + theme(legend.position = "none", text = element_text(size=20))
ggsave("Images/SPWaitSH.png")
ggplot(df.1, aes(x=Total.Wait, fill = ..x..)) + geom_histogram(binwidth = 100) + scale_fill_gradient(low = "red", high = "blue") +
  labs(x = "Minutes", y = "Count") + theme(legend.position = "none", text = element_text(size=20))
ggsave("Images/LongWaitSH.png")

# linear methods, some good, some not so good
#lm.efficiency.mean <- lm(df.mean$Efficiency ~ df.mean$Standard.Deviation)
#lm.efficiency.max <- lm(df.max$Efficiency ~ df.max$Standard.Deviation)

# exponential graphs
#lm.spwait.max.log <- lm(log(df.max$Longest.Wait) ~ df.max$Standard.Deviation)
#lm.totalwait.max.log <- lm(log(df.max$Total.Wait) ~ df.max$Standard.Deviation)
#lm.spwait.mean.log <- lm(log(df.mean$Longest.Wait) ~ df.mean$Standard.Deviation)
#lm.totalwait.mean.log <- lm(log(df.mean$Total.Wait) ~ df.mean$Standard.Deviation)

#summary(lm.efficiency.mean)
#summary(lm.efficiency.max)
#summary(lm.spwait.max.log)
#summary(lm.totalwait.max.log)
#summary(lm.spwait.mean.log)
#summary(lm.totalwait.mean.log)

# linear best fit
ggplot(data = df, aes(Standard.Deviation, Efficiency, fill=Model)) + stat_smooth(se = FALSE, method = 'loess', formula = y~x) + geom_point(pch=21) + theme(text = element_text(size=20))
ggsave("Images/lmEfficiency.png")
# exponential best fit
ggplot(data = df, aes(Standard.Deviation, log(Longest.Wait), fill=Model)) + stat_smooth(se = FALSE, method = 'loess', formula = y~x) + geom_point(pch=21) + theme(text = element_text(size=20))
ggsave("Images/LogLongestWait.png")
ggplot(data = df, aes(Standard.Deviation, log(Total.Wait), fill=Model)) + stat_smooth(se = FALSE, method = 'loess', formula = y~x) + geom_point(pch=21) + theme(text = element_text(size=20))
ggsave("Images/LogTotalWait.png")