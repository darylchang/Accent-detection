import numpy as np
import pickle, random, re
from optparse import OptionParser
from sklearn import cross_validation, svm, tree
from sklearn.ensemble import RandomForestClassifier

# Set parameters for classification
rowsToKeep = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31] # 0-indexed
colsToKeep = [1,2,3,4,5,6,7,8,9,10,11]                    # 0-indexed
estimators = 59
k = 5
clf = RandomForestClassifier(n_estimators=estimators)
print "rows: ", rowsToKeep, ", cols: ", colsToKeep, ", estimators: ", estimators

# Read options from command line
parser = OptionParser()
parser.add_option("--numLangs", "--languages", dest="numLangs", default=15,
                  help="select number of languages", metavar="NUMLANGS")
parser.add_option("--downsample", "--downsample",
		                  action="store_true", dest="downsample", default=False,
				                    help="Take only 20 samples from each language")
(options, args) = parser.parse_args()
numLangs = int(options.numLangs)
downsample = options.downsample

# Read in training features and labels
featureFile = open('../extracted/features.lsvm', 'r')
languageLabels = open('../extracted/language_labels.txt', 'r')
genderLabels = open('../extracted/gender_labels.txt', 'r')

featureLines = [line.strip('\n') for line in featureFile.readlines()]
features = []

for line in featureLines:
	tokens = line.split()[1:]
	tokens = [float(token.split(':')[1]) for token in tokens]
	features.append(tokens)

feature = np.array(features)
languageLabels = np.array([int(line.strip('\n')) for line in languageLabels.readlines()])
genderLabels = np.array([line.strip('\n') for line in genderLabels.readlines()])

# Choose subset of features
numFeatures = len(rowsToKeep) * len(colsToKeep)
featureSubset = np.empty([len(feature), numFeatures])

for i in range(len(feature)):
	lineSubset = np.reshape(features[i], (32,12))
	lineSubset = lineSubset[rowsToKeep]
	lineSubset = lineSubset[:,colsToKeep]
	lineSubset = np.reshape(lineSubset, lineSubset.size)
	featureSubset[i] = lineSubset

features = featureSubset

# Choose a subset of languages depending on command line option
if numLangs == 5:
	indices = [i for i in range(len(languageLabels)) if languageLabels[i] in [0,9,12,13,14]]
elif numLangs == 10:
	indices = [i for i in range(len(languageLabels)) if languageLabels[i] in [0,2,3,4,7,9,11,12,13,14]]
elif numLangs == 15:
	indices = range(len(languageLabels))

features = features[indices]
languageLabels = languageLabels[indices]
genderLabels = genderLabels[indices]

# Separate into male and female
maleIndices = [i for i in range(len(genderLabels)) if genderLabels[i]=="m"]
maleFeatureSubset = features[maleIndices]
maleLanguageLabels = languageLabels[maleIndices]

femaleIndices = [i for i in range(len(genderLabels)) if genderLabels[i]=="f"]
femaleFeatureSubset = features[femaleIndices]
femaleLanguageLabels = languageLabels[femaleIndices]

# Downsample languages to 20 samples each if specified
if downsample:
	firstIndices =  [np.where(languageLabels==label)[0][0] for label in list(set(languageLabels))]
	rangeIndices = [range(firstIndex, firstIndex+20) for firstIndex in firstIndices]
	indices = []
	[indices.extend(el) for el in rangeIndices]
	featureSubset = features[indices]
	genderLabelSubset = genderLabels[indices]
	languageLabelSubset = languageLabels[indices]
else:
	featureSubset = features
	genderLabelSubset = genderLabels
	languageLabelSubset = languageLabels

# Language families
#IndoEuropean -> Dutch, French, German, Italian, Portuguese, Spanish, Macedonian, Polish, Russian
#Altaic -> Japanese, Korean, Turkish
#SinoTibetan -> Mandarin, Cantonese
#Semitic -> Arabic

#Language sub-families
#Turkic -> Turkish
#Germanic -> German, Dutch
#Romance -> Italian, French, Spanish, Portuguese
#Slavic -> Polish, Macedonian, Russian

# Run k-fold cross-validation on classifier
#scores = cross_validation.cross_val_score(clf, features, languageLabels, cv=k)
#maleScores = cross_validation.cross_val_score(clf, maleFeatureSubset, maleLanguageLabels, cv=k)
#femaleScores = cross_validation.cross_val_score(clf, femaleFeatureSubset, femaleLanguageLabels, cv=k)

# Print out and write cross-validation results
#print "Total cross-validation score: ", scores.mean()
#print "Male cross-validation score: ", maleScores.mean()
#print "Female cross-validation score: ", femaleScores.mean()

# Simulate game
numCorrect = 0.
numRounds = 100
for i in range(0,numRounds):
	print i
	languageLabel = random.choice(list(set(languageLabels)))
	if downsample:
		testFileIndex = random.choice([i for i,v in enumerate(languageLabels) if v == languageLabel and i not in indices])
		trainingFeatures = featureSubset
		trainingLabels = languageLabelSubset
	else:
		testFileIndex = random.choice([i for i,v in enumerate(languageLabels) if v == languageLabel])
		trainingFeatures = np.delete(features,(testFileIndex), axis=0)
		trainingLabels = np.delete(languageLabels,(testFileIndex),axis=0)
	
	testFeatures = features[testFileIndex]
	testLabel = languageLabels[testFileIndex]
		
	clf = RandomForestClassifier(n_estimators=estimators)
	clf.fit(trainingFeatures,trainingLabels)
	testPrediction = clf.predict(testFeatures)
	numCorrect += float(testPrediction == languageLabel)
	print numCorrect

print "Game accuracy: {}".format(numCorrect/numRounds)

