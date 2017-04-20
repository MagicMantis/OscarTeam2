rm(list = ls())

# Author: Joseph Savold
# Date: April 6th, 2017
# Purpose: Determine probability of oscar OscarWon with logistic regression

# read in data from file
mydata <- read.csv("~/coding/482/project/Actresses/actress_award_data_formatted.csv", header = TRUE, sep = ",", quote = "\"",
                   dec = ".", fill = TRUE, comment.char = "")

tail(mydata)
training_data <- mydata[mydata$Year!="2016",]
tail(training_data)

# checking the data
dim(mydata)
names(mydata)

attach(mydata)
summary(mydata)

# convert imdb_ratings from strings to numeric
OscarLost <- as.numeric(as.character(OscarLost))
OscarWon <- as.numeric(as.character(OscarWon))
GGDramaWon <- as.numeric(as.character(GGDramaWon))
GGDramaLost <- as.numeric(as.character(GGDramaLost))
GGMusicalWon <- as.numeric(as.character(GGMusicalWon))
GGMusicalLost <- as.numeric(as.character(GGMusicalLost))
CCWon <- as.numeric(as.character(CCWon))
CCLost <- as.numeric(as.character(CCLost))
SAGWon <- as.numeric(as.character(SAGWon))
SAGLost <- as.numeric(as.character(SAGLost))
BAFTAWon <- as.numeric(as.character(BAFTAWon))
BAFTALost <- as.numeric(as.character(BAFTALost))

attach(training_data)

# do logistic regression for Oscar Lost
probs <- glm(OscarWon ~ OscarLost, family = binomial)
summary(probs)

plot(OscarLost, OscarWon,xlab="OscarLost",ylab="Probability of Winning Oscar")
curve(predict(probs,data.frame(OscarLost=x),type="resp"),add=TRUE) # draws a curve based on prediction from logistic regression model

# do logistic regression for Golden Globe Won
probs <- glm(OscarWon ~ GGDramaWon, family = binomial)
summary(probs)

plot(GGDramaWon, OscarWon,xlab="GGDramaWon",ylab="Probability of Winning Oscar")
curve(predict(probs,data.frame(GGDramaWon=x),type="resp"),add=TRUE) # draws a curve based on prediction from logistic regression model

# do logistic regression for CCWon
probs <- glm(OscarWon ~ CCWon, family = binomial)
summary(probs)

plot(CCWon, OscarWon,xlab="CCWon",ylab="Probability of Winning Oscar")
curve(predict(probs,data.frame(CCWon=x),type="resp"),add=TRUE) # draws a curve based on prediction from logistic regression model

# do logistic regression for CCLost
probs <- glm(OscarWon ~ CCLost, family = binomial)
summary(probs)

plot(CCLost, OscarWon,xlab="CCLost",ylab="Probability of Winning Oscar")
curve(predict(probs,data.frame(CCLost=x),type="resp"),add=TRUE) # draws a curve based on prediction from logistic regression model

# do logistic regression for BAFTAWon
probs <- glm(OscarWon ~ BAFTAWon, family = binomial)
summary(probs)

plot(BAFTAWon, OscarWon,xlab="BAFTAWon",ylab="Probability of Winning Oscar")
curve(predict(probs,data.frame(BAFTAWon=x),type="resp"),add=TRUE) # draws a curve based on prediction from logistic regression model

# do logistic regression for BAFTALost
probs <- glm(OscarWon ~ BAFTALost, family = binomial)
summary(probs)

plot(BAFTALost, OscarWon,xlab="BAFTALost",ylab="Probability of Winning Oscar")
curve(predict(probs,data.frame(BAFTALost=x),type="resp"),add=TRUE) # draws a curve based on prediction from logistic regression model


# multi variable logistic regression
m <- glm(OscarWon ~ GGDramaWon + GGMusicalWon + CCWon + SAGWon + BAFTAWon, family = binomial)
summary(m)

###################################################################
# Accuracy / Precision Calculation + Visualization (not yet adapted)
###################################################################

attach(mydata)

pred.probs <- predict (m, mydata, type = "response")

data.frame(Name, Year, pred.probs, OscarWon)
write.csv(data.frame(Name, pred.probs, OscarWon, Year), file = "./probs_of_winning.csv")

confusion.matrix <- table(default, pred.default)
print(addmargins(confusion.matrix))

print(c("accuracy", (confusion.matrix[1,1] + confusion.matrix[2,2]) / 10000 ))

