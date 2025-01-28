# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 21:34:26 2024

@author: houss
"""
import pandas as pd
import csv

metrics_file = './security-metrics-healthcare.csv'
mapping_file = 'mapping.txt'
output_file = 'security-metrics-mapped.csv'


mapping_dict = dict()

df = pd.read_csv(mapping_file)
for index, row in df.iterrows():
    device = row[0].split(' ')[0]
    id = row[0].split(' ')[1]
    mapping_dict[id] = device
    
print(mapping_dict)

with open(metrics_file, 'r') as file:
    data = file.read()
    for key in mapping_dict.keys():
        data = data.replace(key, mapping_dict[key])
    with open(output_file, 'w') as ofile:
        ofile.write(data)
        
        
print('Done')