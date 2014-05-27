 #!/bin/bash

iterations=2

for i in $(seq 0 $((iterations-1)))
do
	# Clear train and test feature files
	rm -f feats/train.lsvm
	rm -f feats/test.lsvm
	
	for language in ../data/*
	do 
		numFiles=$(ls $language| wc -l)
		testFileIndex=$(expr $i % $numFiles)
		count=0
		
		# Run OpenSMILE and record train vs. test
		for j in $language/*
		do
			if [ $count != $testFileIndex ]
				then
					echo "Extracting features for training example: $j"
					# Extract the features and write to train.lsvm
					openSMILE/SMILExtract_standalone_64bit_generic -C config/cs224s.conf -I $j -O feats/train.lsvm -noconsoleoutput
				else
					echo "Extracting features for test example: $j"
					# Extract features and write to test.lsvm
					openSMILE/SMILExtract_standalone_64bit_generic -C config/cs224s.conf -I $j -O feats/test.lsvm -noconsoleoutput
			fi
			# Run Python script to format last line, provide file name as argument
			((count++))
		done
	done

	# Run Python classifier on the train and test data
	# Returns an accuracy, append to array

done

# Average accuracies and print out
