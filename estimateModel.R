rm(list=ls())

MyData <- read.csv(file="sample_imdb_metacritic_data.csv", header=TRUE, sep=",")
dim(MyData)
names(MyData)
attach(MyData)

line <- lm(metascore ~ imdb_rating)
plot(imdb_rating,metascore)
abline(line)
summary(line)
