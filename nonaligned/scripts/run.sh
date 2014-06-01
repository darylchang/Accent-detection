 #!/bin/bash

# Clear feature and label files
rm -f ../extracted/*
	
for language in ../wav/*
do 
	# Run OpenSMILE to extract file features
	for j in $language/*
	do	
		echo "Extracting features for file: $j"
		# Extract the features and write to features.lsvm
		../../openSMILE/SMILExtract_standalone_64bit_generic -C ../../config/cs224s.conf -I $j -O ../extracted/features.lsvm -noconsoleoutput
		
		# Run Python script to write to label file - provide file name as argument
		python label.py $j 
	done
done

# Run Python classifier on the train and test data
python classify.py
