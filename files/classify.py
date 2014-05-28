from sklearn import svm
import numpy as np
from sklearn import cross_validation

clf = svm.SVC()
k = 10

# Read in training features and labels
featureFile = open('extracted/features.lsvm', 'r')
languageLabels = open('extracted/language_labels.txt', 'r')
genderLabels = open('extracted/gender_labels.txt', 'r')

featureLines = [line.strip('\n') for line in featureFile.readlines()]
features = []

for line in featureLines:
	tokens = line.split()[1:]
	tokens = [float(token.split(':')[1]) for token in tokens]
	features.append(tokens)

features = np.array(features)
languageLabels = np.array([int(line.strip('\n')) for line in languageLabels.readlines()])

# Choose subset of features
rowsToKeep = [0,1,2,3,4,5,6,7,8,9,10,11,12,15,16,31] # 0-indexed
colsToKeep = [1,2,5,6,7,9,10,11]                    # 0-indexed
featureSubset = np.empty([len(features), 128])

for i in range(len(features)):
	lineSubset = np.reshape(features[i], (32,12))
	lineSubset = lineSubset[rowsToKeep]
	lineSubset = lineSubset[:,colsToKeep]
	lineSubset = np.reshape(lineSubset, lineSubset.size)
	featureSubset[i] = lineSubset

print featureSubset
	

# Run k-fold cross-validation on classifier
scores = cross_validation.cross_val_score(clf, featureSubset, languageLabels, cv=k)
print scores
print scores.mean()
