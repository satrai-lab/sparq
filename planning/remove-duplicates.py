# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 13:42:25 2024

@author: houss
"""

import pandas as pd

# Load the CSV file into a DataFrame
input_file = 'security-metrics.csv'  # Replace with your file name
output_file = 'sec-metrics.csv'  # File to save the deduplicated data

# Read the CSV file
df = pd.read_csv(input_file)

# Remove duplicate rows, keeping only the first occurrence
df_no_duplicates = df.drop_duplicates(subset=['strategy'], keep='first')

# Save the result to a new CSV file
df_no_duplicates.to_csv(output_file, index=False)

print(f"Duplicate rows have been removed. Cleaned data saved to '{output_file}'.")
