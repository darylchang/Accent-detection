import random

data = [line.split() for line in open('../predictions/15_downsample.txt').readlines()]
guessDict = {}

# Extract data
for line in data:
	language = line[1]
	isCorrect = line[3]
	if language not in guessDict:
		guessDict[language] = [isCorrect]
	else:
		guessDict[language].append(isCorrect)

# Simulate game
numCorrect = 0.
numGames = 100000
for i in range(numGames):
	language = random.choice(guessDict.keys())
	isCorrect = random.choice(guessDict[language])=='True'
	numCorrect += isCorrect

print "Accuracy: {}".format(numCorrect/numGames)

	
