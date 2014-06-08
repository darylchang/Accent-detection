import os, subprocess

languages = os.listdir('../../nonaligned/wav')
for language in languages:
	files = os.listdir('../../nonaligned/wav/{}'.format(language))
	for f in files:
		subprocess.call(['python',
				 		 '../../p2fa/align.py', 
				 		 '../../nonaligned/wav/{}/{}'.format(language,f), 
				 		 '../align.txt', 
				 		 '../textgrid/{}/{}'.format(language,f).replace('wav', 'TextGrid')
				 		 ]) 