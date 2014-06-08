import os, subprocess

for language in sorted(os.listdir('../wav/')):
	for f in sorted(os.listdir('../wav/{}/'.format(language))):
		inputPath = '../wav/{}/{}'.format(language,f)
		fileName = ('-').join([f.split('-')[0], f.split('-')[2]]) + '.lsvm'
		outputPath = '../feats/{}/{}'.format(language, fileName)
		print inputPath, outputPath
		subprocess.call(['../../openSMILE/SMILExtract_standalone_64bit_generic','-C','../../config/cs224s.conf','-I',inputPath, '-O',outputPath,'-noconsoleoutput'])

