# Run on Mac
import os, pickle, re, subprocess

phonemes = pickle.load(open('../../metadata/phonemes.pickle','r'))

for language in sorted(os.listdir('../textgrid/')):
	for f in sorted(os.listdir('../textgrid/{}/'.format(language))):
		print "Processing " + f
		filePath= '../textgrid/{}/{}'.format(language,f)
		lines = [line.strip('[\t\n]') for line in open(filePath, 'r').readlines()]
		startCutoff = lines.index("\"IntervalTier\"") + 5
		endCutoff = len(lines) - lines[::-1].index("\"IntervalTier\"") - 1
		lines = lines[startCutoff:endCutoff]
		
		# Use sox to trim files into individual phones and write to wav directory
		for i in range(len(lines)/3):
			xmin, xmax, phone = lines[i*3:i*3+3]
			phone = phone.strip('\"')

			if phone in phonemes and phone not in ['sp','sil']:
				outputPath = '../wav/{}/{}-{}-{}.wav'.format(language, f.replace('.TextGrid',''), phone, i)
				inputPath = '../../nonaligned/wav/{}/{}'.format(language, f.replace('.TextGrid','.wav'))
				subprocess.call(['../../sox/sox', inputPath, outputPath, 'trim', xmin, '={}'.format(xmax)])		