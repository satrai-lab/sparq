#! /bin/bash

logfile=simulations_log.log
if [ -e $logfile ]; then
	rm $logfile
fi

inputFile=$1
outputFile=$2
simulationDuration=$3
alias=$4

shift 4

mitigation_args=$@

if [[ -z $mitigation_args ]]; then
	echo "WARNING: No mitigation strategy is specified! Running normal simulation."
	java -jar edict.jar $inputFile $outputFile $simulationDuration $alias
	rm ./scenarios/jsimg/*.jsimg
	exit 0
fi

array=(2 9 10 11 13 14 22)
strategy=$1

if [[ ${array[@]} =~ $strategy ]]; then
	python apply_mitigation_strategies.py $inputFile $mitigation_args
fi

java -jar edict.jar $inputFile $outputFile $simulationDuration $alias $mitigation_args

# removing unnecessary jmt files
rm ./scenarios/jsimg/*.jsimg

exit 0
