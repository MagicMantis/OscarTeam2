with open("probs_of_winning.csv", 'r') as csv_file:
	lines = csv_file.readlines()
	i = 1
	tot = 0
	wrong = 0
	year = "2002"
	while i < len(lines):
		vals = []
		while lines[i].strip().split(',')[4] == year:
			vals += [lines[i].strip().split(',')]
			print lines[i].strip().split(',')
			i += 1
			if (i >= len(lines)): break
		if i < len(lines): year = lines[i].strip().split(',')[4]
		correct = "Correct!"
		tot += 1
		if max(vals, key=lambda x: float(x[2]))[3] == '0':
			correct = "Incorrect!"
			wrong += 1
		print "Winner", max(vals, key=lambda x: float(x[2]))[1], correct
	print tot-wrong, " correct out of ", tot