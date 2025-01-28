#!/bin/bash

# Loop through all files in the current directory
for filename in *; do
  # Check if the filename contains "domain"
  if [[ "$filename" == *domain* ]]; then
    # Create the corresponding problem and plan filenames by replacing "domain"
    domainfile="$filename"
    problemfile="${filename//domain/problem}"
    planfile="${filename//domain/plan}"
    
    # Print the filenames
    echo "Domain file: $domainfile"
    echo "Problem file: $problemfile"
    echo "Plan file: $planfile"
    
    # Execute the command with the variables
    ./lpg-td -o "$domainfile" -f "$problemfile" -n 1 > "$planfile"
  fi
done
