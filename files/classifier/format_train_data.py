# Class: CS225S
# Assignment: HW4
# Author: Frank Liu
#
# Formats the training data for use in the classifier.


# open the feature file
f_handle = open('feats/train.lsvm', 'r')
lines = f_handle.readlines()
f_handle.close()

startRows = [1,13,25,37,49,61,73,85,97,109,121,133,145,181,193,373]
columnsToKeep = [2,3,6,7,8,10,11,12]
featuresToKeep = []
for row in startRows:
  featuresToKeep.extend([row + i - 1 for i in columnsToKeep])


featuresToKeep.extend([])

featuresToRemove = []

for feat in featuresToRemove:
  featuresToKeep.remove(feat)

featuresToKeep.sort()


# rewrite the features to the same file (overwrite)
f = open('feats/train_formatted.lsvm', 'w')
for i, line in enumerate(lines):
    if i <= 2: # arabic
        label = 1
    elif i <= 5: # cantonese
        label = 2
    elif i <= 8: # dutch
        label = 3
    elif i <= 11: # mandarin
        label = 4
    elif i <= 14: # russian
        label = 5 
    else:
		label = 6 # turkish
  
    # Format: '1:5034 2:943 3:34 ...'
    tokens = line.split()
    formatted = str(label) + ' '
    for i in featuresToKeep:
      formatted += tokens[i] + ' '
    f.write(formatted[:-1] + '\n') # Remove trailing space
    # f.write(str(label) + line[1:])



f.close()
