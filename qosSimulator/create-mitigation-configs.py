# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 21:44:36 2024

@author: houss
"""

import pandas as pd


security_metrics_file = 'security-metrics-mapped.csv'
mitigation_configs_file = '../planning/configurations-ids_healthcare.csv'

mitigation_configs_dict = dict()
df = pd.read_csv(security_metrics_file)

i = 1
for index, row in df.iterrows():
    config = row[0]
    mitigation_configs_dict[i] = config
    i += 1
    
(pd.DataFrame.from_dict(data=mitigation_configs_dict, orient='index')
   .to_csv(mitigation_configs_file, header=False))
    
    
