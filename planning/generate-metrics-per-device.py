# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 16:56:31 2024

@author: houss
"""

import pandas as pd


sec_file ='SHnet-security-metrics.csv'
qos_file = 'qos-metrics.csv'
strategies_dict = 'configurations-ids_realnetwork.csv'
metrics_per_device_file = 'metrics-per-device/{}.csv'

metrics_file = 'SHnet-security-metrics.csv'
# mapping_file = '../qosSimulator/mapping.txt'
# output_file = '../qosSimulator/security-metrics-mapped.csv'


mapping_dict = dict()

# df = pd.read_csv(mapping_file, header=None)
# for index, row in df.iterrows():
#     device = row[0].split(' ')[0]
#     id = row[0].split(' ')[1]
#     mapping_dict[id] = device
    
# print(mapping_dict)
df = pd.read_csv(sec_file)

metrics_per_device = dict()
mitigation_dict=dict()
resp_times_dict = dict()

qos_df = pd.read_csv(qos_file)
for i in range (1, 66):
    strategyId = str(i)
    average = qos_df.loc[:, strategyId].mean()
    resp_times_dict[strategyId] = average
    

mitigation_df = pd.read_csv(strategies_dict)
for index, row in mitigation_df.iterrows():
    mitigationId = row[0]
    config = row[1]
    mitigation_dict[config] = mitigationId
    

for index, row in df.iterrows():
    strategyId = row[0].split(' ')[0]
    devices = row[0].split(' ')[1:]
    
    avg_lik,avg_imp,avg_risk,avg_len, num_paths = row[1], row[2], row[3], row[4], row[5]
    if '<' in devices[0]:
        devices = devices[0].split(';')[0]
        devices = devices.replace('<', '')
        devices = [devices]
    
    list_of_devices = devices
    
    ## Here we are mapping devices to hosts (N1  ... N12). This may not always be needed
    # list_of_devices[0] = mapping_dict[list_of_devices[0]]
    print(devices)
    mitigationId = mitigation_dict['{} {}'.format(strategyId, ' '.join(devices))]
    for device in list_of_devices:
        if device in metrics_per_device:
            existing_list = metrics_per_device[device]
            existing_list.append([strategyId, avg_lik,avg_imp,avg_risk,avg_len, num_paths])
        else:
            metrics_per_device[device] = [[strategyId, avg_lik,avg_imp,avg_risk,avg_len, num_paths]]
# print(metrics_per_device)

for device in metrics_per_device.keys():
    filename = metrics_per_device_file.format(device)
    with open(filename, 'a') as f:
        f.write('mitigationId,avg_lik,avg_imp,avg_risk,avg_len,num_paths,avg_latency')
        f.write('\n')
        for value in metrics_per_device[device]:
            # print(value)
            line = ''
            for field in value:
                # print(str(field))
                line += str(field)  + ','
                # print(line)
            line += str(resp_times_dict[str(value[0])])
            f.write(line[:-1])
            f.write('\n')
