library(ggplot2)
library(reshape)
library(dplyr)

names <- c("Original", "Send Home", "Distribution")

Mean.Efficiency <- c(93.3, 95, 93.5)
Min.Efficiency <- c(55.2,65.3,64.9)

Mean.Single.Person.Wait.Time <-c(64.1, 61.4, 55.3)
Max.Single.Person.Wait.Time <- c(548, 576, 560)
Mean.Total.Wait.Time <- c(1142, 1021, 968)
Max.Total.Wait.Time <- c(12573, 7018, 5826)

df.mean <- data.frame(Mean.Efficiency, Mean.Single.Person.Wait.Time, Mean.Total.Wait.Time)
df.mean <- t(df.mean)
dfm.mean <- melt(df.mean)
colnames(dfm.mean) <- c("Metric", "Model", "Value")

dfm.mean$Model <- recode_factor(dfm.mean$Model, "1" = "Original", "2" = "Send Home", "3" = "Distribution")
df.max <- data.frame(Min.Efficiency, Max.Single.Person.Wait.Time, Max.Total.Wait.Time)
df.max <- t(df.max)
dfm.max <- melt(df.max)
colnames(dfm.max) <- c("Metric", "Model", "Value")

dfm.max$Model <- recode_factor(dfm.max$Model, "1" = "Original", "2" = "Send Home", "3" = "Distribution")


ggplot(subset(dfm.mean, Metric %in% c("Mean.Efficiency")), aes(x=Metric, y=Value, fill=Model)) + geom_bar(stat="identity", position="dodge") + 
  labs(x = "", y = "Percent", fill = "Model", title = "Mean Efficiency")
ggsave("MeanEfficiency.png")
ggplot(subset(dfm.mean, Metric %in% c("Mean.Single.Person.Wait.Time")), aes(x=Metric, y=Value, fill=Model)) + geom_bar(stat="identity", position="dodge") +
  labs(x = "", y = "Minutes", fill = "Model", title = "Mean Single Person Wait Time")
ggsave("Meanspwait.png")
ggplot(subset(dfm.mean, Metric %in% c("Mean.Total.Wait.Time")), aes(x=Metric, y=Value, fill=Model)) + geom_bar(stat="identity", position="dodge") + 
  labs(x = "", y = "Minutes", fill = "Model", title = "Mean Total Wait Time")
ggsave("MeanWait.png")
ggplot(subset(dfm.max, Metric %in% c("Min.Efficiency")), aes(x=Metric, y=Value, fill=Model)) + geom_bar(stat="identity", position="dodge") + 
  labs(x = "", y = "Percent", fill = "Model", title = "Min Efficiency")
ggsave("MinEfficiency.png")
ggplot(subset(dfm.max, Metric %in% c("Max.Single.Person.Wait.Time")), aes(x=Metric, y=Value, fill=Model)) + geom_bar(stat="identity", position="dodge") + 
  labs(x = "", y = "Minutes", fill = "Model", title = "Max Single Person Wait Time")
ggsave("Maxspwait.png")
ggplot(subset(dfm.max, Metric %in% c("Max.Total.Wait.Time")), aes(x=Metric, y=Value, fill=Model)) + geom_bar(stat="identity", position="dodge") + 
  labs(x = "", y = "Minutes", fill = "Model", title = "Max Total Wait Time")
ggsave("MaxWait.png")

