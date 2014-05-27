#!/bin/bash

for i in {1..10}
do
	bash extract_feat.sh
	bash train.sh
	bash predict.sh
done
