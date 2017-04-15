import sys
from collections import defaultdict

class BAFTA:

	def __init__(self):
		#best picture
		file_object = open("./golden-globe-musical","r")
		lines = file_object.readlines();
		self.picturesWin = defaultdict(lambda: 0)
		self.picturesNom = defaultdict(lambda: 0)
		winner = True
		for line in lines:
			if winner: 
				self.picturesWin[line.strip()] += 1
				self.picturesNom[line.strip()] += 1
				winner = False
			elif (line == "\n"):
				winner = True
			else:
				self.picturesNom[line.strip()] += 1

		#best drama
		file_object = open("./golden-globe-drama","r")
		lines = file_object.readlines();
		self.dramaWin = defaultdict(lambda: 0)
		self.dramaNom = defaultdict(lambda: 0)
		winner = True
		for line in lines:
			if winner: 
				self.dramaWin[line.strip()] += 1
				self.dramaNom[line.strip()] += 1
				winner = False
			elif (line == "\n"):
				winner = True
			else:
				self.dramaNom[line.strip()] += 1


	def get_best_picture_winner(self, name):
		if not name in self.picturesWin:
			return 0
		return self.picturesWin[name]

	def get_best_picture_nom(self, name):
		if not (name in self.picturesNom or name in self.picturesWin or name in self.dramaWin or name in self.dramaNom):
			#use this to see if the name was in the Bafta dictionary
			#print name
			pass
		return self.picturesNom[name]

	def get_best_drama_winner(self, name):
		if not name in self.dramaWin:
			return 0
		return self.dramaWin[name]

	def get_best_drama_nom(self, name):
		if not (name in self.picturesNom or name in self.picturesWin or name in self.dramaWin or name in self.dramaNom):
			#print name
			pass
		return self.dramaNom[name]


def print_best_picture():
	file_object = open(sys.argv[1],"r")
	lines = file_object.readlines();
	current = 0
	ba = BAFTA();
	for line in lines:
		line = line.strip()
		if "2002" <= line <= "2017":
			continue
		else:
			print ba.get_best_picture_nom(line), ba.get_best_picture_winner(line)

def print_best_drama():
	file_object = open(sys.argv[1],"r")
	lines = file_object.readlines();
	current = 0
	ba = BAFTA();
	for line in lines:
		line = line.strip()
		if "2002" <= line <= "2017":
			continue
		else:
			print ba.get_best_drama_nom(line), ba.get_best_drama_winner(line)

print_best_picture()
