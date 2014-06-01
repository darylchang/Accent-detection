import pickle, sys

f = open('../../metadata/lang_labels.pickle')
labelDict = pickle.load(f)

fileName = sys.argv[1]
language = fileName.split('-')[0].split('/')[-1]
gender = fileName.split('-')[1][0]

f = open('../extracted/language_labels.txt', 'a')
f.write(str(labelDict[language]) + '\n')

f = open('../extracted/gender_labels.txt', 'a')
f.write(gender + '\n')
