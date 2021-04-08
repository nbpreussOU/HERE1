# Title     : VAMCv3 Analysis
# Objective : Determine the effects of standrad deviation upon wait times
# Created by: Nathan
# Created on: 4/8/2021

df.max <- read.csv("Data/v3_max_data.csv")
df.mean <- read.csv("Data/v3_mean_data.csv")
df.max$Model <- "Max"
df.mean$Model <- "Mean"
df <- rbind(df.max, df.mean)
head(df)

# linear methods, some good, some not so good
lm.efficiency.mean <- lm(df.mean$Efficiency ~ df.mean$Standard.Deviation)
lm.efficiency.max <- lm(df.max$Efficiency ~ df.max$Standard.Deviation)

# exponential graphs
lm.spwait.max.log <- lm(log(df.max$Longest.Wait) ~ df.max$Standard.Deviation)
lm.totalwait.max.log <- lm(log(df.max$Total.Wait) ~ df.max$Standard.Deviation)
lm.spwait.mean.log <- lm(log(df.mean$Longest.Wait) ~ df.mean$Standard.Deviation)
lm.totalwait.mean.log <- lm(log(df.mean$Total.Wait) ~ df.mean$Standard.Deviation)

summary(lm.efficiency.mean)
summary(lm.efficiency.max)
summary(lm.spwait.max.log)
summary(lm.totalwait.max.log)
summary(lm.spwait.mean.log)
summary(lm.totalwait.mean.log)

library(ggplot2)
# linear best fit
ggplot(data = df, aes(Standard.Deviation, Efficiency, fill=Model)) + stat_smooth(se = FALSE, method = 'loess', formula = y~x) + geom_point(pch=21) + ggtitle("Efficiency")
ggsave("Images/lmEfficiency.png")
# exponential best fit
ggplot(data = df, aes(Standard.Deviation, log(Longest.Wait), fill=Model)) + stat_smooth(se = FALSE, method = 'loess', formula = y~x) + geom_point(pch=21) + ggtitle("Log SP Wait")
ggsave("Images/LogLongestWait.png")
ggplot(data = df, aes(Standard.Deviation, log(Total.Wait), fill=Model)) + stat_smooth(se = FALSE, method = 'loess', formula = y~x) + geom_point(pch=21) + ggtitle("Log Total Wait")
ggsave("Images/LogTotalWait.png")
# glad to see that wait time increases exponentially as the standard deviation of the variables increases
# SD of 10 should mimic the base model

# still need to verify assumptions of SLR and stuff