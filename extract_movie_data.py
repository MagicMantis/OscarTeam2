###
# Extract movie data (critic ratings, user ratings, etc.) from IMDB,
# metacritic, and Rotten Tomatoes (currently not implemented) for a list of
# movies
###

from imdb import IMDb
import requests

########### function defintions ###########
def get_imdb_info(movie_name):
	## get movie information from imdb.com ##

	ia = IMDb()

	# get all results from searching for the movie name
	list_of_movies = ia.search_movie(movie_name)

	# I believe the movies are listed in most recent order, so this assumes
	# that we want the most recent movie with that title
	movie = list_of_movies[0]

	ia.update(movie)

	# use a dictionary to hold all of the information
	movie_info = {}

	keys = ["rating", "votes", "mpaa", "top-250-rank", "genres", "director"]

	# get the movie information
	for key in keys:
		try:
			if key == "genres":
				movie_info[key] = movie[key]
			elif key == "director":
				movie_info[key] = str(movie[key][0])
			elif key == "top-250-rank":
				movie_info[key] = str(movie['top 250 rank'])
			else:
				movie_info[key] = str(movie[key])
		except KeyError:
			print("No " + key + " found for " + str(movie))

			if key == "genres":
				movie_info[key] = ["-"]
			else:
				movie_info[key] = "-"

	return movie_info

def get_metacritic_info(movie_name):
	# get movie information from metacritic.com ##

	# TODO: fix metascore_w urls to allow for perfect, moderate, and poor movies

	# load the metacritic page for the movie
	r = requests.get('http://www.metacritic.com/movie/' + movie_name,
	                  headers={'User-Agent': 'Mozilla/5.0'})

	# use a dictionary to hold all the movie information
	metacritic_info = {}

	postfixes = ["Positive", "Mixed", "Negative"]

	##  get user score ##

	# metacritic shows the overall user score and then break it down to show
	# how many of the scores were positive, mixed, or negative
	try:
		metacritic_info["userscore"] = \
		        r.text \
		         .split("<div class=\"metascore_w user larger movie positive\">")[1] \
		         .split("</div>")[0] \
				 .replace(',','')

		# get the number of scores that were positive, mixed, and negative
		for postfix in postfixes:
			metacritic_info["num_userscore_" + postfix.lower()] = \
			        r.text \
					 .split("<div class=\"metascore_w user larger movie positive\">")[1] \
			         .split("<div class=\"label fl\">" + postfix + ":")[1] \
					 .split("<div class=\"count fr\">")[1] \
					 .split("</div>")[0] \
					 .replace(',','')

	# some movies don't have a user score
	except IndexError:
		print("No userscore for " + movie_name)
		metacritic_info["userscore"] = "-"
		metacritic_info["num_userscore_positive"] = "-"
		metacritic_info["num_userscore_mixed"] = "-"
		metacritic_info["num_userscore_negative"] = "-"

	## get metascore ##

	# same layout as user scores
	metacritic_info["metascore"] = \
	        r.text \
	         .split("<div class=\"metascore_w larger movie positive\">")[1] \
	         .split("</div>")[0] \
			 .replace(',','')

	# get the number of scores that were positive, mixed, and negative
	for postfix in postfixes:
		metacritic_info["num_metascore_" + postfix.lower()] = \
		        r.text \
				 .split("<div class=\"metascore_w larger movie positive\">")[1] \
		         .split("<div class=\"label fl\">" + postfix + ":")[1] \
				 .split("<div class=\"count fr\">")[1] \
				 .split("</div>")[0] \
				 .replace(',','')

	return metacritic_info

# def get_rotten_tomatoes_info(movie_name):
# 	r = requests.get("https://www.rottentomatoes.com/m/" + movie_name,
# 	                  headers={'User-Agent': 'Mozilla/5.0'})
#
# 	rt_info = {}
#
# 	top_level = ["all", "top"]
# 	bottom_level = ["Average Rating:", "Reviews Counted:", "Fresh:", "Rotten:"]
#
# 	for top in top_level:
# 		full_string = top + "-critics-numbers"
# 		rt_info[full_string] = r.split("full_string")[2] \
# 		                        .split("meter-value superPageFontColor\"><span>")[1] \
# 								.split("</span>")[0]
#
# 		for bottom in bottom_level:


def make_csv(list_of_movies):
	## write a .csv file with all of the data from each of the movies ##

	with open("movies.csv", 'w') as csv_file:
		# write headers
		csv_file.write("name,year,imdb_rating,num_imdb_votes,mpaa,top-250-rank," \
		             + "genres,director,metascore,num_metascore_positive," \
					 + "num_metascore_mixed,num_metascore_negative,userscore," \
					 + "num_userscore_positive,num_userscore_mixed," \
					 + "num_userscore_negative\n")

		# write info for each movie
		# TODO: make this go in order from 2016 backwards in time
		for year in list_of_movies:
			for movie in list_of_movies[year]:
				# metacritic some times uses a different name than imdb
				metacritic_movie_name = movie + "-" + str(year)

				imdb_info = get_imdb_info(movie)

				# when metacritic uses a different name than imdb, it *seems*
				# to append the year that movie was released. So first see if
				# metacritic has a listing for movie name followed by its year,
				# but if it doesn't see if it has a listing for just the movie
				# name.
				try:
					metacritic_info = get_metacritic_info(metacritic_movie_name)
				except IndexError:
					metacritic_info = get_metacritic_info(movie)

				# start writing the data about the movie
				csv_file.write(movie + "," + str(year) + ","
				              + str(imdb_info["rating"]) + "," \
				              + str(imdb_info["votes"]) + "," + "\"" \
							  + str(imdb_info["mpaa"]) + "\"," \
							  + str(imdb_info["top-250-rank"]) + "," + "\"")

				# there are normally multiple genres, so we have to write
				# in a different way
				for genre in imdb_info["genres"]:
					csv_file.write(genre + ",")

				# continue writing the data
				csv_file.write("\","
				            + str(imdb_info["director"]) + "," \
			  				+ str(metacritic_info["metascore"]) + "," \
			  				+ str(metacritic_info["num_metascore_positive"]) + "," \
			  				+ str(metacritic_info["num_metascore_mixed"]) + "," \
			  				+ str(metacritic_info["num_metascore_negative"]) + "," \
			  				+ str(metacritic_info["userscore"]) + "," \
			  				+ str(metacritic_info["num_userscore_positive"]) + "," \
			  				+ str(metacritic_info["num_userscore_mixed"]) + "," \
			  				+ str(metacritic_info["num_userscore_negative"]) + "\n")

########### START ###########
movies = {}
movies[2016] = ["moonlight", "la-la-land", "arrival", "fences", "hacksaw-ridge", \
          "hell-or-high-water", "hidden-figures", "lion", "manchester-by-the-sea"]
movies[2015] = ["spotlight", "the-big-short", "bridge-of-spies", "brooklyn", \
		  "mad-max-fury-road", "the-martian", "the-revenant", "room"]
movies[2014] = ["birdman", "american-sniper",
          "the-grand-budapest-hotel", "the-imitation-game", "selma",
		  "the-theory-of-everything", "whiplash"] # purposely missing boyhood

make_csv(movies)
