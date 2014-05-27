from sklearn import svm

# Read in training features and labels
featureFile = open('feats/train.lsvm', 'r')
labelFile = open('feats/train_labels.txt', 'r')

featureLines = [line.strip('\n') for line in featureFile.readlines()]
features = []

for line in featureLines:
	tokens = line.split()[1:]
	tokens = [float(token.split(':')[1]) for token in tokens]
	features.append(tokens)

labels = [int(line.strip('\n')) for line in labelFile.readlines()]

clf = svm.LinearSVC()
clf.fit(features, labels)

# Read in test features and labels
featureFile = open('feats/test.lsvm', 'r')
labelFile = open('feats/test_labels.txt', 'r')

featureLines = [line.strip('\n') for line in featureFile.readlines()]
features = []

for line in featureLines:
	tokens = line.split()[1:]
	tokens = [float(token.split(':')[1]) for token in tokens]
	features.append(tokens)

labels = [int(line.strip('\n')) for line in labelFile.readlines()]

predictions = clf.predict(features)
numCorrect = float(sum([x == y for x, y in zip(predictions, labels)]))
accuracy = numCorrect / len(labels)

print accuracy
