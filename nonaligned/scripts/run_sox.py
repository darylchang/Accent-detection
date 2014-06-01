import subprocess, os

dirs = sorted(os.listdir('../wav'))
for dir in dirs:
	for file in sorted(os.listdir('../wav/{}'.format(dir))):
		oldFilePath = '../wav/{}/{}'.format(dir,file)
		newFilePath = '../new_wav/{}/{}'.format(dir,file)
		subprocess.call(['../../sox/sox', oldFilePath, newFilePath])
