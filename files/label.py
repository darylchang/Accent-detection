import sys

labelDict = {
	'arabic': 0,
	'cantonese': 1,
	'dutch': 2,
	'french': 3,
	'german': 4,
	'italian': 5,
	'japanese': 6,
	'korean': 7,
	'macedonian': 8,
	'mandarin': 9,
	'polish': 10,
	'portuguese': 11,
	'russian': 12,
	'spanish': 13,
	'turkish': 14,
}

fileName = sys.argv[1]
language = fileName.split('-')[0].split('/')[-1]
gender = fileName.split('-')[1][0]

f = open('extracted/language_labels.txt', 'a')
f.write(str(labelDict[language]) + '\n')

f = open('extracted/gender_labels.txt', 'a')
f.write(gender + '\n')