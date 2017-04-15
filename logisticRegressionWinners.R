rm(list = ls())

# Author: Joseph Savold
# Date: April 6th, 2017
# Purpose: Determine probability of oscar winner with logistic regression

# read in data from file
mydata <- read.csv("~/coding/482/project/movies.csv", header = TRUE, sep = ",", quote = "\"",
  dec = ".", fill = TRUE, comment.char = "")

training_data <- mydata[6:nrow(mydata),]

# checking the data
dim(mydata)
names(mydata)

attach(mydata)
summary(mydata)

head(mydata)

# convert imdb_ratings from strings to numeric
imdb_rating <- as.numeric(as.character(imdb_rating))
num_imdb_votes <- as.numeric(as.character(num_imdb_votes))
metascore_rating <- as.numeric(as.character(metascore_rating))
num_metascore_positive <- as.numeric(as.character(num_metascore_positive))
num_metascore_mixed <- as.numeric(as.character(num_metascore_mixed))
num_metascore_negative <- as.numeric(as.character(num_metascore_negative))
num_userscore_positive <- as.numeric(as.character(num_userscore_positive))
num_userscore_mixed <- as.numeric(as.character(num_userscore_mixed))
num_userscore_negative <- as.numeric(as.character(num_userscore_negative))
all.critics.numbers <- as.numeric(as.character(all.critics.numbers))
top.critics.numbers <- as.numeric(as.character(top.critics.numbers))
top_average_rating <- as.numeric(as.character(top_average_rating))
top_reviews_counted <- as.numeric(as.character(top_reviews_counted))
top_fresh <- as.numeric(as.character(top_fresh))
top_rotten <- as.numeric(as.character(top_rotten))
rt_audience_score <- as.numeric(as.character(rt_audience_score))
winner <- as.numeric(as.character(winner))
bafta_winner <- as.numeric(as.character(bafta_winner))
bafta_loser <- as.numeric(as.character(bafta_loser))

attach(training_data)

##############################
# Tests for Numeric Predictors 
##############################

# do logistic regression for imdb rating
probs <- glm(winner ~ imdb_rating, family = binomial)
summary(probs)

plot(imdb_rating, winner,xlab="IMdB Rating",ylab="Probability of Winning Oscar")
curve(predict(probs,data.frame(imdb_rating=x),type="resp"),add=TRUE) # draws a curve based on prediction from logistic regression model

# do logistic regression for metascore
probs.meta <- glm(winner ~ metascore_rating, family = binomial)
summary(probs.meta)

plot(metascore_rating, winner,xlab="Metascore Rating",ylab="Probability of Winning Oscar")
curve(predict(probs.meta,data.frame(metascore_rating=x),type="resp"),add=TRUE) # draws a curve based on prediction from logistic regression model

# do logistic regression for negative metascore
probs.neg <- glm(winner ~ neg_, family = binomial)
summary(probs.meta)

plot(num_metascore_negative, winner,xlab="Metascore Rating",ylab="Probability of Winning Oscar")
curve(predict(probs.neg,data.frame(num_metascore_negative=x),type="resp"),add=TRUE) # draws a curve based on prediction from logistic regression model


# multi variable logistic regression
m <- glm(winner ~ imdb_rating + metascore_rating, family = binomial)
summary(m)

plot(imdb_rating + metascore_rating, winner,xlab="",ylab="Probability of Winning Oscar")
curve(predict(m,data.frame(metascore_rating=x),type="resp"),add=TRUE) # draws a curve based on prediction from logistic regression model

##################################################################
# Tests for Non-Numeric Predictors
##################################################################

# year test
m <- glm(winner ~ year, family = binomial)
summary(m)

# mpaa test
m <- glm(winner ~ mpaa, family = binomial)
summary(m)

# director test
m <- glm(winner ~ director, family = binomial)
summary(m)


##########################################
# Train Model On Multiple Predictors
##########################################

m <- glm(winner ~ imdb_rating + num_imdb_votes + metascore_rating, family = binomial)

###################################################################
# Accuracy / Precision Calculation + Visualization (not yet adapted)
###################################################################

pred.data <- data.frame(balance = c(1000,2000,3000),income=1000, student="No")
predict(m, pred.data, type="response")

pred.probs <- predict (m, type = "response")
pred.default <- rep("No", nrow(Default))
pred.default[pred.probs > 0.5] <- "Yes"

confusion.matrix <- table(default, pred.default)
print(addmargins(confusion.matrix))

print(c("accuracy", (confusion.matrix[1,1] + confusion.matrix[2,2]) / 10000 ))
