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
		#iphoneCurrFeatures = np.delete(phoneCurrFeatures, range(180, 384)) # Delete F0 and delta features
		
		if language in langFeaturesDict:
			langFeaturesDict[language] = np.vstack([langFeaturesDict[language], phoneCurrFeatures])
		else:
			langFeaturesDict[language] = np.array([phoneCurrFeatures])
		
# Calculate the means and standard deviations for each phone-MFCC pair
featureMatrices = langFeaturesDict.values()
featureAverages = np.mean(featureMatrices, axis=0)
featureStds = np.std(featureMatrices, axis=0)

# Replace the 0's in the stds to avoid infinite z-scores
featureStds[featureStds == 0.] = 15000.

# Helper function for finding largest z-scores
def nlargest_indices(arr, n):
	#arr[arr == np.inf] = 0
	uniques = np.unique(arr)
	threshold = uniques[-n]
	x, y = np.where(arr >= threshold)
	return zip(x,y, arr[x,y])

# Calculate z-score for languages
zScoreDict = {}
for language, featureMatrix in sorted(langFeaturesDict.items()):
	zScoreDict[language] = np.abs(featureMatrix - featureAverages) / featureStds
	coords = nlargest_indices(zScoreDict[language], n)
	print "Top features for {}: ".format(language)
	for phonemeIndex, mfccIndex, zScore in coords:
		print "		Phoneme: {}, OpenSmile feature: {}, value: {}, average: {}, std: {}, zScore: {}".format(
			  phonemes[phonemeIndex], mfccIndex, featureMatrix[phonemeIndex][mfccIndex], featureAverages[phonemeIndex][mfccIndex], 
			  featureStds[phonemeIndex][mfccIndex], zScore)