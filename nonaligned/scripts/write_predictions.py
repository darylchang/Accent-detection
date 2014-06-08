import numpy as np
import pickle, re
from optparse import OptionParser
from sklearn import cross_validation, svm, tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier

# Set parameters for classification
rowsToKeep = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31] # 0-indexed
colsToKeep = [1,2,3,4,5,6,7,8,9,10,11]                    # 0-indexed
estimators = 59
clf = svm.SVC(kernel='rbf')
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
fileNames = pickle.load(open('../../metadata/file_map.pickle', 'r')).values()

featureLines = [line.strip('\n') for line in featureFile.readlines()]
features = []

for line in featureLines:
	tokens = line.split()[1:]
	tokens = [float(token.split(':')[1]) for token in tokens]
	features.append(tokens)

features = np.array(features)
languageLabels = np.array([int(line.strip('\n')) for line in languageLabels.readlines()])
genderLabels = np.array([line.strip('\n') for line in genderLabels.readlines()])
fileNames = np.array(fileNames)

# Choose subset of features
numFeatures = len(rowsToKeep) * len(colsToKeep)
featureSubset = np.empty([len(features), numFeatures])

for i in range(len(features)):
	lineSubset = np.reshape(features[i], (32,12))
	lineSubset = lineSubset[rowsToKeep]
	lineSubset = lineSubset[:,colsToKeep]
	lineSubset = np.reshape(lineSubset, lineSubset.size)
	featureSubset[i] = lineSubset

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
fileNames = fileNames[indices]

# Write to prediction file
if downsample:
	outputFileName = '../predictions/svcrbf_{}_downsample.txt'.format(numLangs)
else:
	outputFileName = '../predictions/svcrbf_{}.txt'.format(numLangs)
f = open(outputFileName, 'a')

for i in range(len(features)):
	print i
	trainingFeatures = np.delete(features,(i), axis=0)
	trainingLabels = np.delete(languageLabels,(i),axis=0)
	testFeatures = features[i]
	testLabel = languageLabels[i]

	# Downsample languages to 20 training samples each if specified
	if downsample:
		firstIndices = [np.where(languageLabels==label)[0][0] for label in list(set(languageLabels))]
		rangeIndices = [range(firstIndex, firstIndex+20) for firstIndex in firstIndices]
		indices = []
		[indices.extend(el) for el in rangeIndices]
		trainingFeatures = trainingFeatures[indices]
		trainingLabels = trainingLabels[indices]
	
	clf = RandomForestClassifier(n_estimators=estimators)
	clf.fit(trainingFeatures,trainingLabels)
	testPrediction = clf.predict(testFeatures)
	
	fileId = re.findall('.*-[mf](\d+).wav', fileNames[i])[0]
	f.write(str(fileId) + ' ')
	f.write(str(testLabel) + ' ')
	f.write(str(testPrediction[0]) + ' ')
	f.write(str(testLabel == testPrediction[0]) + '\n')

f.close()
