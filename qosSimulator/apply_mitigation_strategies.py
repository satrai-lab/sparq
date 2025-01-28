# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 11:05:26 2024

@author: houss
"""

import json
import sys



def remove_topic_subscription_from_app(data, app, topics_to_remove):
    for topic_to_remove in topics_to_remove:
        for apps in data['applications']:
            if apps['applicationId'] == app and topic_to_remove in apps['subscribesTo']:
                apps['subscribesTo'].remove(topic_to_remove)
                
        for topic in data['topics']:
            if topic['topicId'] == topic_to_remove and app in topic['subscribers']: 
                topic['subscribers'].remove(app)
    return data
    
    
# Function to remove a topic from subscriptions
def remove_topic_subscription(data, topics_to_remove):
    for topic_to_remove in topics_to_remove:
        for apps in data['applications']:
            if topic_to_remove in apps['subscribesTo']:
                apps['subscribesTo'].remove(topic_to_remove)
                
        for topic in data['topics']:
            if topic['topicId'] == topic_to_remove:
                topic['subscribers'] = []  # Remove all subscribers for the topic
        return data
    
def reduce_arrival_rate(device, new_arrival_rate):
    for devices in data['IoTdevices']:
        if devices['deviceId'] == device:
            print(devices['deviceId'])
            devices['publishFrequency'] = new_arrival_rate
    return data

def convert_str(input_str):
    app_dict = {}

    # Split the string by the '>' symbol, which separates different app entries
    entries = input_str.split(">")

    # Process each entry
    for entry in entries:
        # Clean up each entry by removing '<' and extra spaces
        entry = entry.strip().replace("<", "")
        
        # If the entry is not empty, split it into app and subscriptions
        if entry:
            parts = entry.split(", ")
            app = parts[0]  # First part is the app name
            subscriptions = parts[1:]  # Remaining parts are subscriptions
            
            # Add app and subscriptions to the dictionary
            app_dict[app] = subscriptions
            
    return app_dict



'''Used for debugging purposes'''
# strategyId = 10
# topics_to_remove = ["topic_topic1"]
# device = "topic1_source"
# new_arrival_rate = 100
# input_str = "<app_app2, topic_topic2, topic_topic3> <app_app1, topic_topic1>"
# input_file = 'scenarios/sample-scenario-default.json'

if __name__ == '__main__':
    input_file = sys.argv[1]
    strategyId = float(sys.argv[2])
    parameters = sys.argv[3:]
    parameters = ' '.join(parameters)
    print("Input file: ", input_file)
    with open(input_file) as json_data:
        data = json.load(json_data)
    
    updated_data = data
    if (strategyId == 2 or strategyId == 9 or strategyId == 22):
        topics_to_remove = parameters
        updated_data = remove_topic_subscription(data, topics_to_remove)
    elif strategyId == 14:
        arrival_rates_dict = convert_str(parameters)
        for device, new_arrival_rate in arrival_rates_dict.items():
            updated_data = reduce_arrival_rate(device, new_arrival_rate)
    elif strategyId == 10 or strategyId == 11 or strategyId == 13:
        subscriptions_dict = convert_str(parameters)
        for app, topics_to_remove in subscriptions_dict.items():
            updated_data = remove_topic_subscription_from_app(data, app, topics_to_remove)

    with open(input_file.replace('-default', '') , 'w') as f:
        json.dump(updated_data, f, ensure_ascii=False, indent=4)


