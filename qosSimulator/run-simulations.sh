#! /bin/bash

i=0
while IFS= read -r line
do
	echo "Running simulation for $line"
	./qosSimulator.sh scenarios/healthcare-default.json qos-metrics-healthcare.csv 300 $line
  	i=i+1
done < scenarios/mitigations-healthcare.csv
echo "Simulations done!"