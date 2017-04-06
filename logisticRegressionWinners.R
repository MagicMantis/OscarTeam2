rm(list = ls())

# Author: Joseph Savold
# Date: April 6th, 2017
# Purpose: Determine probability of oscar winner with logistic regression

mydata <- read.csv("~/coding/482/project/sample_imdb_metacritic_data.csv", header = TRUE, sep = ",", quote = "\"",
  dec = ".", fill = TRUE, comment.char = "")

dim(mydata)
names(mydata)

attach(mydata)
summary(mydata)


probs <- glm(winner ~ imdb_rating, family = binomial)
summary(probs)

plot(imdb_rating, winner)
curve(predict(probs,data.frame(imdb_rating=x),type="resp"),add=TRUE) # draws a curve based on prediction from logistic regression model


m <- glm(winner ~ imdb_rating + income + student, family = binomial)
summary(m)

pred.data <- data.frame(balance = c(1000,2000,3000),income=1000, student="No")
predict(m, pred.data, type="response")

pred.probs <- predict (m, type = "response")
pred.default <- rep("No", nrow(Default))
pred.default[pred.probs > 0.5] <- "Yes"

confusion.matrix <- table(default, pred.default)
print(addmargins(confusion.matrix))

print(c("accuracy", (confusion.matrix[1,1] + confusion.matrix[2,2]) / 10000 ))
