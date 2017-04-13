import sys
from collections import defaultdict

class BAFTA:

	def __init__(self):
		#best picture
		file_object = open("./bafta_best_picture","r")
		lines = file_object.readlines();
		self.picturesWin = defaultdict(lambda: 0)
		self.picturesNom = defaultdict(lambda: 0)
		winner = True
		for line in lines:
			if winner: 
				self.picturesWin[line] += 1
				winner = False
			elif (line == "\n"):
				winner = True
			else:
				self.picturesNom[line] += 1

		#best director
		file_object = open("./bafta_best_director","r")
		lines = file_object.readlines();
		self.directorWin = defaultdict(lambda: 0)
		self.directorNom = defaultdict(lambda: 0)
		winner = True
		for line in lines:
			if winner: 
				self.directorWin[line] += 1
				winner = False
			elif (line == "\n"):
				winner = True
			else:
				self.directorNom[line] += 1


		#best actor
		file_object = open("./bafta_best_actor","r")
		lines = file_object.readlines();
		self.actorWin = defaultdict(lambda: 0)
		self.actorNom = defaultdict(lambda: 0)
		winner = True
		for line in lines:
			if winner: 
				self.actorWin[line] += 1
				winner = False
			elif (line == "\n"):
				winner = True
			else:
				self.actorNom[line] += 1


		#best actress
		file_object = open("./bafta_best_actress","r")
		lines = file_object.readlines();
		self.actressWin = defaultdict(lambda: 0)
		self.actressNom = defaultdict(lambda: 0)
		winner = True
		for line in lines:
			if winner: 
				self.actressWin[line] += 1
				winner = False
			elif (line == "\n"):
				winner = True
			else:
				self.actressNom[line] += 1


	def get_best_picture_winner(self, name):
		if not name in self.picturesNom:
			return 0
		return self.picturesWin[name]

	def get_best_picture_nom(self, name):
		if not name in self.picturesWin:
			#use this to see if the name was in the Bafta dictionary
			#print name
			return 0
		return self.picturesNom[name]

	def get_best_director_winner(self, name):
		if not name in self.directorWin:
			return 0
		return self.directorWin[name]

	def get_best_director_nom(self, name):
		if not name in self.directorNom:
			#print name
			return 0
		return self.directorNom[name]

	def get_best_actor_winner(self, name):
		if not name in self.actorWin:
			return 0
		return self.actorWin[name]

	def get_best_actor_nom(self, name):
		if not name in self.actorNom:
			#print name
			return 0
		return self.actorNom[name]


	def get_best_actress_winner(self, name):
		if not name in self.actressWin:
			return 0
		return self.actressWin[name]

	def get_best_actress_nom(self, name):
		if not name in self.actressNom:
			#print name
			return 0
		return self.actressNom[name]


def print_best_picture():
	file_object = open(sys.argv[1],"r")
	lines = file_object.readlines();
	current = 0
	ba = BAFTA();
	for line in lines:
		if "2002" <= line <= "2017":
			continue
		else:
			print "hello"

def print_best_director():
	file_object = open(sys.argv[1],"r")
	lines = file_object.readlines();
	current = 0
	ba = BAFTA();
	for line in lines:
		print ba.get_best_director_nom(line), ba.get_best_director_winner(line)

def print_best_actor():
	file_object = open(sys.argv[1],"r")
	lines = file_object.readlines();
	current = 0
	ba = BAFTA();
	for line in lines:
		print ba.get_best_actor_nom(line), ba.get_best_actor_winner(line)


def print_best_actress():
	file_object = open(sys.argv[1],"r")
	lines = file_object.readlines();
	current = 0
	ba = BAFTA();
	for line in lines:
		print ba.get_best_actress_nom(line), ba.get_best_actress_winner(line)

print_best_actress()
