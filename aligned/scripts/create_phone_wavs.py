# Run on Mac
import os, pickle, re, subprocess

phonemes = pickle.load(open('../../metadata/phonemes.pickle','r'))

for language in sorted(os.listdir('../textgrid/')):
	for f in sorted(os.listdir('../textgrid/{}/'.format(language))):
		filePath= '../textgrid/{}/{}'.format(language,f)
		lines = [line.strip('[\t\n]') for line in open(filePath, 'r').readlines()]
		startCutoff = lines.index('intervals [1]:')
		endCutoff = lines.index('item [2]:')
		lines = lines[startCutoff:endCutoff]
		
		# Use sox to trim files into individual phones and write to wav directory
		for i in range(len(lines)/4):
			xmin, xmax, phone = lines[i*4+1:i*4+4]
			xmin = re.findall('xmin = (\d*\.\d*)', xmin)[0]
			xmax = re.findall('xmax = (\d*\.\d*)', xmax)[0]
			phone = re.findall('text = "(.*)"', phone)[0].strip('[012]')

			if phone in phonemes:
				outputPath = '../wav/{}/{}-{}-{}.wav'.format(language, f.replace('.TextGrid',''), phone, i)
				inputPath = '../../nonaligned/wav/{}/{}'.format(language, f.replace('.TextGrid','.wav'))
				subprocess.call(['../../sox/sox', inputPath, outputPath, 'trim', xmin, '={}'.format(xmax)])		