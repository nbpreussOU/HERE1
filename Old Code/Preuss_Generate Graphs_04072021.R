library(ggplot2)
library(reshape)
library(dplyr)

# create data
Mean.Efficiency <- c(93.3, 95, 93.5)
Min.Efficiency <- c(55.2,65.3,64.9)
Mean.Single.Person.Wait.Time <-c(64.1, 61.4, 55.3)
Max.Single.Person.Wait.Time <- c(548, 576, 560)
Mean.Total.Wait.Time <- c(1142, 1021, 968)
Max.Total.Wait.Time <- c(12573, 7018, 5826)
SD.Efficiency <- c(8.7, 7.4, 7.0)
SD.Single.Person.Wait.Time <- c(94, 89, 76)
SD.Total.Wait.Time <- c(1733, 1464, 1146)

# fix the mean data frame
df.mean <- data.frame(Mean.Efficiency, Mean.Single.Person.Wait.Time, Mean.Total.Wait.Time)
df.mean <- t(df.mean)
dfm.mean <- melt(df.mean)
colnames(dfm.mean) <- c("Metric", "Model", "Value")
dfm.mean$Model <- recode_factor(dfm.mean$Model, "1" = "Original", "2" = "Send Home", "3" = "Distribution")

# fix the max data frame
df.max <- data.frame(Min.Efficiency, Max.Single.Person.Wait.Time, Max.Total.Wait.Time)
df.max <- t(df.max)
dfm.max <- melt(df.max)
colnames(dfm.max) <- c("Metric", "Model", "Value")
dfm.max$Model <- recode_factor(dfm.max$Model, "1" = "Original", "2" = "Send Home", "3" = "Distribution")

# fix the sd data frame
df.sd <- data.frame(SD.Efficiency, SD.Single.Person.Wait.Time, SD.Total.Wait.Time)
df.sd <- t(df.sd)
dfm.sd <- melt(df.sd)
colnames(dfm.sd) <- c("Metric", "Model", "Value")
dfm.sd$Model <- recode_factor(dfm.sd$Model, "1" = "Original", "2" = "Send Home", "3" = "Distribution")

#plot graphs
ggplot(subset(dfm.mean, Metric %in% "Mean.Efficiency"), aes(x=Metric, y=Value, fill=Model)) + geom_bar(stat="identity", position="dodge") +
  labs(x = "", y = "Percent", fill = "Model", title = "Mean Efficiency")
ggsave("../Images/MeanEfficiency.png")
ggplot(subset(dfm.mean, Metric %in% "Mean.Single.Person.Wait.Time"), aes(x=Metric, y=Value, fill=Model)) + geom_bar(stat="identity", position="dodge") +
  labs(x = "", y = "Minutes", fill = "Model", title = "Mean Single Person Wait Time")
ggsave("Images/Meanspwait.png")
ggplot(subset(dfm.mean, Metric %in% "Mean.Total.Wait.Time"), aes(x=Metric, y=Value, fill=Model)) + geom_bar(stat="identity", position="dodge") +
  labs(x = "", y = "Minutes", fill = "Model", title = "Mean Total Wait Time")
ggsave("Images/MeanWait.png")
ggplot(subset(dfm.max, Metric %in% "Min.Efficiency"), aes(x=Metric, y=Value, fill=Model)) + geom_bar(stat="identity", position="dodge") +
  labs(x = "", y = "Percent", fill = "Model", title = "Min Efficiency")
ggsave("Images/MinEfficiency.png")
ggplot(subset(dfm.max, Metric %in% "Max.Single.Person.Wait.Time"), aes(x=Metric, y=Value, fill=Model)) + geom_bar(stat="identity", position="dodge") +
  labs(x = "", y = "Minutes", fill = "Model", title = "Max Single Person Wait Time")
ggsave("Images/Maxspwait.png")
ggplot(subset(dfm.max, Metric %in% "Max.Total.Wait.Time"), aes(x=Metric, y=Value, fill=Model)) + geom_bar(stat="identity", position="dodge") +
  labs(x = "", y = "Minutes", fill = "Model", title = "Max Total Wait Time")
ggsave("Images/MaxWait.png")

ggplot(subset(dfm.sd, Metric %in% "Min.Efficiency"), aes(x=Metric, y=Value, fill=Model)) + geom_bar(stat="identity", position="dodge") +
  labs(x = "", y = "Percent", fill = "Model", title = "Standard Deviation Efficiency")
ggsave("Images/SDEfficiency.png")
ggplot(subset(dfm.max, Metric %in% "Max.Single.Person.Wait.Time"), aes(x=Metric, y=Value, fill=Model)) + geom_bar(stat="identity", position="dodge") +
  labs(x = "", y = "Minutes", fill = "Model", title = "Standard Deviation Single Person Wait Time")
ggsave("Images/SDspwait.png")
ggplot(subset(dfm.max, Metric %in% "Max.Total.Wait.Time"), aes(x=Metric, y=Value, fill=Model)) + geom_bar(stat="identity", position="dodge") +
  labs(x = "", y = "Minutes", fill = "Model", title = "Standard Deviation Total Wait Time")
ggsave("Images/SDWait.png")

