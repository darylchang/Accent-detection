import numpy as np
from sklearn import cross_validation, svm, tree
from sklearn.ensemble import RandomForestClassifier

# Set parameters for classification
rowsToKeep = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31] # 0-indexed
colsToKeep = [1,2,3,4,5,6,7,8,9,10,11]                    # 0-indexed
estimators = 59
k = 5
clf = RandomForestClassifier(n_estimators=estimators)
print "rows: ", rowsToKeep, ", cols: ", colsToKeep, ", estimators: ", estimators

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
genderLabels = np.array([line.strip('\n') for line in genderLabels.readlines()])

# Choose subset of features
numFeatures = len(rowsToKeep) * len(colsToKeep)
featureSubset = np.empty([len(features), numFeatures])

for i in range(len(features)):
	lineSubset = np.reshape(features[i], (32,12))
	lineSubset = lineSubset[rowsToKeep]
	lineSubset = lineSubset[:,colsToKeep]
	lineSubset = np.reshape(lineSubset, lineSubset.size)
	featureSubset[i] = lineSubset

# Separate into male and female
maleIndices = [i for i in range(len(genderLabels)) if genderLabels[i]=="m"]
maleFeatureSubset = featureSubset[maleIndices]
maleLanguageLabels = languageLabels[maleIndices]

femaleIndices = [i for i in range(len(genderLabels)) if genderLabels[i]=="f"]
femaleFeatureSubset = featureSubset[femaleIndices]
femaleLanguageLabels = languageLabels[femaleIndices]

# Write to prediction file
f = open('predictions/predictions_15.txt', 'w')

for i in range(len(features)):
	print i
	trainingFeatures = np.delete(features,(i), axis=0)
	trainingLabels = np.delete(languageLabels,(i),axis=0)
	testFeatures = features[i]
	testLabel = languageLabels[i]
	
	clf = RandomForestClassifier(n_estimators=estimators)
	clf.fit(trainingFeatures,trainingLabels)
	testPrediction = clf.predict(testFeatures)
	
	f.write(str(i) + ' ')
	f.write(str(testLabel) + ' ')
	f.write(str(testPrediction[0]) + ' ')
	f.write(str(testLabel == testPrediction[0]) + '\n')

f.close()
