 #!/bin/bash

iterations=2

for i in $(seq 0 $((iterations-1)))
do
	# Clear train and test feature files
	rm -f feats/*
	
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
					isTrain=1
					openSMILE/SMILExtract_standalone_64bit_generic -C config/cs224s.conf -I $j -O feats/train.lsvm -noconsoleoutput
				else
					echo "Extracting features for test example: $j"
					# Extract features and write to test.lsvm
					isTrain=0
					openSMILE/SMILExtract_standalone_64bit_generic -C config/cs224s.conf -I $j -O feats/test.lsvm -noconsoleoutput
			fi
			# Run Python script to format last line, provide file name as argument
			python label.py $j $isTrain 
			((count++))
		done
	done

	# Run Python classifier on the train and test data
	a=$(python classify.py)
	accuracies[i]=$a
done

# Average accuracies and print out
#echo ${accuracies[*]}
sum=0
for i in $(seq 0 $((${#accuracies[@]}-1)))
do
	sum=$(echo $sum + ${accuracies[i]} | bc)
done

averageAccuracy=$(echo $sum / $iterations | bc -l)
echo $averageAccuracy
