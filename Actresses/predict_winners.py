with open("probs_of_winning.csv", 'r') as csv_file:
	lines = csv_file.readlines()
	for i in range(1, len(lines), 5):
		vals = []
		for line in lines[i:i+5]:
			vals += [line.strip().split(',')]
			print line.strip().split(',')
		print "Winner", max(vals, key=lambda x: float(x[2]))[1]
