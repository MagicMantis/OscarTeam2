rm(list = ls())

# Author: Joseph Savold
# Date: April 6th, 2017
# Purpose: Determine probability of oscar winner with logistic regression

# read in data from file
mydata <- read.csv("~/coding/482/project/director_data_final.csv", header = TRUE, sep = ",", quote = "\"",
                   dec = ".", fill = TRUE, comment.char = "")

training_data <- mydata[1:70,]

# checking the data
dim(mydata)
names(mydata)

attach(mydata)
summary(mydata)

# convert imdb_ratings from strings to numeric
OscarLost <- as.numeric(as.character(OscarLost))
OscarWon <- as.numeric(as.character(OscarWon))
GGWon <- as.numeric(as.character(GGWon))
GGLost <- as.numeric(as.character(GGLost))
CCWon <- as.numeric(as.character(CCWon))
CCLost <- as.numeric(as.character(CCLost))
BAFTAWon <- as.numeric(as.character(BAFTAWon))
BAFTALost <- as.numeric(as.character(BAFTALost))
Winner <- as.numeric(as.character(Winner))

# do logistic regression for Oscar Lost
probs <- glm(Winner ~ OscarLost, family = binomial)
summary(probs)

plot(OscarLost, Winner,xlab="OscarLost",ylab="Probability of Winning Oscar")
curve(predict(probs,data.frame(OscarLost=x),type="resp"),add=TRUE) # draws a curve based on prediction from logistic regression model

# do logistic regression for Oscar Won
probs <- glm(Winner ~ OscarWon, family = binomial)
summary(probs)

plot(OscarWon, Winner,xlab="OscarWon",ylab="Probability of Winning Oscar")
curve(predict(probs,data.frame(OscarWon=x),type="resp"),add=TRUE) # draws a curve based on prediction from logistic regression model

# do logistic regression for Golden Globe Won
probs <- glm(Winner ~ GGWon, family = binomial)
summary(probs)

plot(GGWon, Winner,xlab="GGWon",ylab="Probability of Winning Oscar")
curve(predict(probs,data.frame(GGWon=x),type="resp"),add=TRUE) # draws a curve based on prediction from logistic regression model

# do logistic regression for GG Lost
probs <- glm(Winner ~ GGLost, family = binomial)
summary(probs)

plot(GGLost, Winner,xlab="GGLost",ylab="Probability of Winning Oscar")
curve(predict(probs,data.frame(GGLost=x),type="resp"),add=TRUE) # draws a curve based on prediction from logistic regression model

# do logistic regression for CCWon
probs <- glm(Winner ~ CCWon, family = binomial)
summary(probs)

plot(CCWon, Winner,xlab="CCWon",ylab="Probability of Winning Oscar")
curve(predict(probs,data.frame(CCWon=x),type="resp"),add=TRUE) # draws a curve based on prediction from logistic regression model

# do logistic regression for CCLost
probs <- glm(Winner ~ CCLost, family = binomial)
summary(probs)

plot(CCLost, Winner,xlab="CCLost",ylab="Probability of Winning Oscar")
curve(predict(probs,data.frame(CCLost=x),type="resp"),add=TRUE) # draws a curve based on prediction from logistic regression model

# do logistic regression for BAFTAWon
probs <- glm(Winner ~ BAFTAWon, family = binomial)
summary(probs)

plot(BAFTAWon, Winner,xlab="BAFTAWon",ylab="Probability of Winning Oscar")
curve(predict(probs,data.frame(BAFTAWon=x),type="resp"),add=TRUE) # draws a curve based on prediction from logistic regression model

# do logistic regression for BAFTALost
probs <- glm(Winner ~ BAFTALost, family = binomial)
summary(probs)

plot(BAFTALost, Winner,xlab="BAFTALost",ylab="Probability of Winning Oscar")
curve(predict(probs,data.frame(BAFTALost=x),type="resp"),add=TRUE) # draws a curve based on prediction from logistic regression model


# multi variable logistic regression
m <- glm(Winner ~ GGWon + GGLost + CCWon + CCLost + BAFTAWon + BAFTALost, family = binomial)
summary(m)

###################################################################
# Accuracy / Precision Calculation + Visualization (not yet adapted)
###################################################################

attach(mydata)

pred.data <- data.frame(balance = c(1000,2000,3000),income=1000, student="No")
predict(m, mydata, type="response")

pred.probs <- predict (m, mydata, type = "response")
pred.winner <- rep("No", nrow(mydata))
pred.winner[pred.probs > 0.5] <- "Yes"

data.frame(Director, pred.probs)
write.csv(data.frame(Director, pred.probs), file = "./Directors/probs_of_winning.csv")

confusion.matrix <- table(default, pred.default)
print(addmargins(confusion.matrix))

print(c("accuracy", (confusion.matrix[1,1] + confusion.matrix[2,2]) / 10000 ))
