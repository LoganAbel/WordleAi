import csv
from collections import Counter

def read(path):
	with open(path, 'r') as file:
		return [*csv.reader(file)]

def write(path, arr2d):
	with open(path, 'w', newline='') as file:
		file = csv.writer(file)
		for arr in arr2d:
			file.writerow(arr)

def score(guess, answer):
	pool = Counter(a for g, a in zip(guess, answer) if g != a)

	def score(g, a):
		if g == a:
			return 2
		if g in answer and pool[g] > 0:
			pool[g] -= 1
			return 1
		return 0

	return sum(3 ** i * score(g, a)
		for i, (g, a) in enumerate(zip(guess, answer)))

answers = read('answers.csv')[0]
guesses = read('guesses.csv')[0]

write('scores.csv', ((score(guess, answer) for answer in answers) for guess in guesses))
