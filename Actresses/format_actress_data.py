# Author: Joseph
# Purpose: Change director csv (with award data) to usable format
# for the R script to train a model for Oscar nominations

awards = {}

with open("actress_data_raw.csv", 'r') as input_file:
	lines = input_file.readlines()

	# print headers
	print lines[0].strip()

	for line in lines[1:]:
		vals = line.strip().split(',')
		awards[vals[0]] = vals[1:]

with open("best_actress_nominations.txt", 'r') as input_file:
	for line in input_file:
		line = line.strip()

		try:
			pline = line
			for val in awards[line]:
				pline += "," + val;
			print pline
		except KeyError:
			continue
