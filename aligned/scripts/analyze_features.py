import numpy as np
import math, os, pickle

# Parameters
n = 5 # Number of top z-scores to take from each language

# arabic = [[] MFCCs for AA
#           [] MFCCs for AE
#		    ..
#           []]

langFeaturesDict = {}
phonemes = list(pickle.load(open('../../metadata/phonemes.pickle')))

# Vectorize the MFCCs and add to dictionary
for language in sorted(os.listdir('../feats/')):
	for file in sorted(os.listdir('../feats/{}'.format(language))):
		phoneTempFeatures = open('../feats/{}/{}'.format(language, file), 'r').readlines()
		phoneTempFeatures = [line.strip('\n').split() for line in phoneTempFeatures]
		phoneCurrFeatures = []
		for line in phoneTempFeatures:
			phoneCurrFeatures.append([float(feature.split(':')[1]) for feature in line if feature != '0'])
		phoneCurrFeatures = np.mean(phoneCurrFeatures, axis=0)
		phoneCurrFeatures = np.delete(phoneCurrFeatures, range(180, 384)) # Delete F0 and delta features
		
		if language in langFeaturesDict:
			langFeaturesDict[language] = np.vstack([langFeaturesDict[language], phoneCurrFeatures])
		else:
			langFeaturesDict[language] = np.array([phoneCurrFeatures])
		
# Calculate the means and standard deviations for each phone-MFCC pair
featureMatrices = langFeaturesDict.values()
featureAverages = np.mean(featureMatrices, axis=0)
featureStds = np.std(featureMatrices, axis=0)

# Helper function for finding largest z-scores
def nlargest_indices(arr, n):
	#arr[arr == np.inf] = 0
	uniques = np.unique(arr)
	threshold = uniques[-n]
	x, y = np.where(arr >= threshold)
	return zip(x,y)

# Calculate z-score for languages
logZScoreDict = {}
for language, featureMatrix in sorted(langFeaturesDict.items()):
	logZScoreDict[language] = np.log(np.abs(featureMatrix - featureAverages)) - np.log(featureStds) 
	coords = nlargest_indices(featureMatrix, n)
	print "Top features for {}: ".format(language)
	for phonemeIndex, mfccIndex in coords:
		print "		Phoneme: {}, MFCC: {}".format(phonemes[phonemeIndex], mfccIndex)