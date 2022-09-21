import csv

def prog_bar(percent, prefix, length = 50):
	bar =  '█' * round(percent * length)
	bar += '-' * (length - len(bar))
	print(f'\r{prefix}\t |{bar}| {round(percent * 100)}% ', end='\r')

def read(path, prog = False):
	with open(path, 'r') as file:
		size = sum(1 for line in file)
	with open(path, 'r') as file:
		return [
			(prog and prog_bar(i/size, f'loading {path}:'), line)[1] 
			for i,line in enumerate(csv.reader(file))
		]

answers = read('answers.csv')[0]
guesses = read('guesses.csv')[0]
scores  = read('scores.csv', True)
print()
print('type "help" for a list of commands')
indices = [*range(len(answers))]

# ============================== wordle solver ============================

from collections import Counter
import math

weight = lambda prob: \
	0 if prob == 0 or prob == 1 \
	else - prob * math.log2(prob) - (1-prob) * math.log2(1-prob)

def rate(scores_row):
	return sum(weight(count / len(indices)) for count in Counter(scores_row[i] for i in indices).values())

def best_guess():
	ratings = [rate(scores[guess_i]) for guess_i in range(len(guesses))]

	best  = max(ratings)
	best_guesses = [guess for guess, rating in zip(guesses, ratings) if rating == best]
	guess_answers = [guess for guess in best_guesses if guess in (answers[i] for i in indices)]
	if len(guess_answers) > 1:
		return guess_answers
	return best_guesses

def hash_score(txt):
	return str(sum(3 ** i * (2 if v=='g' else 1 if v == 'y' else 0) for i, v in enumerate(txt)))

# ============================== input/output loop ============================

while 1:
	cmd, *args = input('> ').split(' ')

	if cmd == 'help':
		print("exit\nrestart\nshow answers\nshow guesses\nguess (guess) (score)")

	if cmd == 'restart':
		indices = [*range(len(answers))]

	if cmd == 'show': 
		if args[0] == 'answers':
			print("answers:", ' '.join(answers[i] for i in indices))
		if args[0] == 'guesses':
			print("best guesses:", ' '.join(best_guess()))

	if cmd == 'guess':
		guess, *score = args
		if len(score) == 0:
			score = [input('score: ')]
		score = score[0]

		scoring = hash_score(score)
		scores_row = scores[guesses.index(guess)]
		indices = [i for i in indices if scores_row[i] == scoring]

	if cmd == 'exit':
		break