#!/usr/bin/python

"""
Extracts movie data (critic ratings, user ratings, etc.) from IMDB, metacritic,
and Rotten Tomatoes for a list of movies, and writes the data to movies.csv

The movies being looked up are listed in a dictionary at the bottom.

To run:
	make sure python 2 is installed on your computer, then just run
	python extract_movie_data.py

Dependencies:
	IMDbPY http://imdbpy.sourceforge.net/
	requests http://docs.python-requests.org/en/master/
"""

from imdb import IMDb
import requests

########### function defintions ###########
def get_imdb_info(movie_name):
	"""
	Gets movie information from IMDB.

	Parameters
	----------
	movie_name : str
		The name of the movie to search for on IMDB.

	Returns
	-------
	dictionary
		A dictionary containing the keys:
		rating -- the rating for the movie found on IMDB
		votes -- Number of votes used for the rating
		mpaa -- The movie's rating (PG-13, R, etc.)
		top-250-rank -- If the movie is in the top 250 on IMDB, this will be the
						specific rank that movie has
		genres -- A list of which genres the movie fits in (comedy, drama, etc.)
		director -- The director of the movie
	"""
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
			if key == "genres":
				movie_info[key] = ["-"]
			else:
				movie_info[key] = "-"

	return movie_info

def get_metacritic_info(movie_name):
	"""
	Gets critic and user scores from Metacric

	Parameters
	----------
	movie_name : str
		The name of the movie to search for on Metacritic

	Returns
	-------
	dictionary or None
		If everything goes well, then it will return a dictionary containing the
		keys:
		metascore -- The critic score for the given movie name
		num_metascore_positive -- The number of critic reviews that were positive
		num_metascore_miixed -- the number of critic reviews that were both
								positive and negative
		num_metascore_negative -- The number of critic reviews that were negative
		userscore -- The user score for the given movie name
		num_userscore_positive -- The number of user reviews that were positive
		num_userscore_miixed -- the number of user reviews that were both
								positive and negative
		num_userscore_negative -- The number of user reviews that were negative

		If there isn't a page for the given movie, then None will be returned
	"""
	# load the metacritic page for the movie
	r = requests.get('http://www.metacritic.com/movie/' + movie_name,
	                  headers={'User-Agent': 'Mozilla/5.0'})

	# use a dictionary to hold all the movie information
	metacritic_info = {}

	# If the page returns a 404, then that means that there isn't a page for
	# that movie. Since we won't be able to get any reviews or scores from a
	# page that doesn't exist, go ahead and return
	if r.status_code == 404:
		metacritic_info["metascore"] = "-"
		metacritic_info["num_metascore_positive"] = "-"
		metacritic_info["num_metascore_mixed"] = "-"
		metacritic_info["num_metascore_negative"] = "-"
		metacritic_info["userscore"] = "-"
		metacritic_info["num_userscore_positive"] = "-"
		metacritic_info["num_userscore_mixed"] = "-"
		metacritic_info["num_userscore_negative"] = "-"

		return(None)

	postfixes = ["Positive", "Mixed", "Negative"]

	##  get user score ##

	# metacritic shows the overall user score and then break it down to show
	# how many of the scores were positive, mixed, or negative
	try:
		metacritic_info["userscore"] = \
		        r.text \
		         .split("<div class=\"metascore_w user larger")[1] \
				 .split("\">")[1] \
		         .split("</div>")[0]
	# some movies don't have a user score
	except IndexError:
		metacritic_info["userscore"] = "-"

	# get the number of scores that were positive, mixed, and negative
	for postfix in postfixes:
		try:
			metacritic_info["num_userscore_" + postfix.lower()] = \
			        r.text \
			         .split("<div class=\"label fl\">" + postfix + ":")[2] \
					 .split("<div class=\"count fr\">")[1] \
					 .split("</div>")[0] \
					 .replace(',','')
		except IndexError:
			metacritic_info["num_userscore_" + postfix.lower()] = "-"

	## get metascore ##

	# same layout as user scores
	try:
		metacritic_info["metascore"] = \
		        r.text \
		         .split("<div class=\"metascore_w larger")[1] \
				 .split("\">")[1] \
		         .split("</div>")[0] \
				 .replace(',','')
	except IndexError:
		metacritic_info["metascore"] = "-"

	# get the number of scores that were positive, mixed, and negative
	for postfix in postfixes:
		try:
			metacritic_info["num_metascore_" + postfix.lower()] = \
			        r.text \
			         .split("<div class=\"label fl\">" + postfix + ":")[1] \
					 .split("<div class=\"count fr\">")[1] \
					 .split("</div>")[0] \
					 .replace(',','')
		except IndexError:
			metacritic_info["numb_metascore_" + postfix.lower()] = "-"

	return metacritic_info

def get_rotten_tomatoes_info(movie_name):
	"""
	Gets critic reviews from Rotten Tomatoes.

	Parameters
	----------
	movie_name : str
		The name of the movie to search for on rottentomatoes.

	Returns
	-------
	dictionary or None
		If everything goes well, then it will return a dictionary containing the
		keys:
		all-critics-numbers -- The movie rating using input from all of the critics
		all_Average_Rating -- The average rating from all of the critics on a scale from 1-10
		all_Reviews_Counted -- The numbers of critic's reviews that were used
		all_Fresh -- The number of critic's reviews that were positive
		all_Rotten -- The number of critic's reviews that were negative
		top-critics-numbers -- The movie rating using input from just the top critics
		top_Average_Rating -- The average rating from the top critics on a scale from 1-10
		top_Reviews_Counted -- The numbers of critic's reviews that were used
		top_Fresh -- The number of critic's reviews that were positive
		top_Rotten -- The number of critic's reviews that were negative
		rt_audience_score -- The audience's score for the movie

		If there isn't a page for the given movie, then None will be returned
	"""
	r = requests.get("https://www.rottentomatoes.com/m/" + movie_name,
	                  headers={'User-Agent': 'Mozilla/5.0'})

	# If the page returns a 404, then that means that there isn't a page for
	# that movie. Since we won't be able to get any reviews or scores from a
	# page that doesn't exist, go ahead and return
	if r.status_code == 404:
		return(None)


	rt_info = {}

	top_level = ["all", "top"]
	bottom_level = ["Average Rating:", "Reviews Counted:", "Fresh:", "Rotten:"]

	for top in top_level:
		full_string = top + "-critics-numbers"

		try:
			rt_info[full_string] = r.text.split(full_string)[2] \
			                             .split("meter-value superPageFontColor\"><span>")[1] \
										 .split("</span>")[0]

		except IndexError:
			rt_info[full_string] = "-"

		for bottom in bottom_level:
			dictionary_key = top + "_" + bottom.replace(" ", "_").replace(":", "")

			try:
				if dictionary_key.replace(top+"_", "") != "Average_Rating":
					rt_info[dictionary_key] = r.text.split(full_string)[2] \
							                        .split(bottom + " </span>")[1] \
													.split("<span>")[1] \
							                        .split("</")[0]
				else:
					rt_info[dictionary_key] = r.text.split(full_string)[2] \
							                        .split(bottom + " </span>")[1] \
													.split("\n")[1] \
													.split(" ")[-1] \
							                        .split("/")[0]
			except IndexError:
				rt_info[dictionary_key] = "-"

	try:
		rt_info["rt_audience_score"] = r.text.split("AUDIENCE SCORE")[1] \
										     .split("vertical-align:top\">")[1] \
											 .split("%")[0]
	except IndexError:
		rt_info["rt_audience_score"] = "-"

	return(rt_info)

def make_csv(dict_of_movies):
	"""
	Write movie information out to a csv named movie.csv

	Parameters
	----------
	dict_of_movies : dictionary int => str[]
		A dictionary where the key is the year of the movie, and the value is a
		list of movies for that came out in that year, where each movie does
		not contain any spaces or colons
	"""

	with open("movies.csv", 'w') as csv_file:
		# write headers
		csv_file.write("name,year,imdb_rating,num_imdb_votes,mpaa,top-250-rank," \
		             + "genres,director,metascore_rating,num_metascore_positive," \
					 + "num_metascore_mixed,num_metascore_negative,userscore_rating," \
					 + "num_userscore_positive,num_userscore_mixed," \
					 + "num_userscore_negative,all-critics-numbers," \
					 + "all_average_rating,all_reviews_counted,all_fresh," \
					 + "all_rotten,top-critics-numbers,top_average_rating," \
					 + "top_reviews_counted,top_fresh,top_rotten,rt_audience_score\n")

		# write info for each movie
		for year, movies in sorted(dict_of_movies.iteritems(), reverse=True):
			for movie in movies:
				print(str(year) + " - " + movie)

				# metacritic some times uses a different name than imdb
				metacritic_movie_name = movie + "-" + str(year)

				imdb_info = get_imdb_info(movie)

				# when metacritic uses a different name than imdb, it *seems*
				# to append the year that movie was released. So first see if
				# metacritic has a listing for movie name followed by its year,
				# but if it doesn't see if it has a listing for just the movie
				# name.
				metacritic_info = get_metacritic_info(metacritic_movie_name)
				if metacritic_info == None:
					metacritic_info = get_metacritic_info(movie)

				rotten_tomatoes_info = get_rotten_tomatoes_info(metacritic_movie_name)
				if rotten_tomatoes_info == None:
					rotten_tomatoes_info = get_rotten_tomatoes_info(movie)


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
			  				+ str(metacritic_info["num_userscore_negative"]) + ",")

				# # write the rotten tomatoes data
				csv_file.write( \
							  str(rotten_tomatoes_info["all-critics-numbers"]) + ","
							+ str(rotten_tomatoes_info["all_Average_Rating"]) + ","
							+ str(rotten_tomatoes_info["all_Reviews_Counted"]) + ","
							+ str(rotten_tomatoes_info["all_Fresh"]) + "," \
							+ str(rotten_tomatoes_info["all_Rotten"]) + ","
							+ str(rotten_tomatoes_info["top-critics-numbers"]) + "," \
							+ str(rotten_tomatoes_info["top_Average_Rating"]) + "," \
							+ str(rotten_tomatoes_info["top_Reviews_Counted"]) + "," \
							+ str(rotten_tomatoes_info["top_Fresh"]) + "," \
							+ str(rotten_tomatoes_info["top_Rotten"]) + "," \
							+ str(rotten_tomatoes_info["rt_audience_score"]) + "\n")

########### START ###########
movies = {}

# these are the movies that were nominated for best picture according to
# wikipedia: https://en.wikipedia.org/wiki/Academy_Award_for_Best_Picture .
# Movie names should NOT have any colons or spaces. Instead, they should be
# replaced with dashes (-)
movies[2016] = ["moonlight", "la-la-land", "arrival", "fences", "hacksaw-ridge", \
          "hell-or-high-water", "hidden-figures", "lion", "manchester-by-the-sea"]
movies[2015] = ["spotlight", "the-big-short", "bridge-of-spies", "brooklyn", \
		  "mad-max-fury-road", "the-martian", "the-revenant", "room"]
movies[2014] = ["birdman", "american-sniper", "boyhood",
          "the-grand-budapest-hotel", "the-imitation-game", "selma",
		  "the-theory-of-everything", "whiplash"]
movies[2013] = ["12-years-a-slave", "american-hustle", "dallas-buyers-club",
				"captain-phillips", "gravity", "nebraska", "philomena",
				"the-wolf-of-wall-street"]
movies[2012] = ["argo", "life-of-pi", "les-miserables", "lincoln",
				"django-unchained", "beasts-of-the-southern-wild",
				"silver-linings-playbook","zero-dark-thirty", "amour"]

make_csv(movies)
