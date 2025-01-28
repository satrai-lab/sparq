import json, os, sys
import pandas as pd
import numpy as np
from statistics import mean, median
from matplotlib import pyplot as plt
import warnings
warnings.filterwarnings("ignore")

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from config import NET_TAGS


ARCHITECTURAL_STRATEGIES = ['17','18','19','29','21','22','23','24','25','10','20']
PATCHING_STRATEGIES = ['1','2','3','4','5','6','7','8','9','19','11','12','13','14','15','16']

COLORS = {
    "NoAdaptation":"#e66101",
    "Architectural":"#fdb863",
    "Security":"#b2abd2",
    "SPARQ":"#018571",
}
"""
SECURITY
No plan -> strategy 0 (security-metrics)
Architectural/patching strategies -> pick strategies within range (security-metrics)
Plan strategies -> both security and latency (metrics-per-device)

QOS
No plan -> qos-metrics.csv (qos-metrics)
Architectural/patching strategies -> pick strategies within range in metrics-per-device (metrics-per-device)
Plan strategies -> both security and latency (metrics-per-device)
"""


def plot_securitymetric(file_security_metrics,file_plan,net_tag,metricfield):
    df_security = pd.read_csv(file_security_metrics)
    
    strategies = df_security["strategy"].to_list()
    
    list_strategy0=[]
    list_strategy_arch=[]
    list_strategy_patch=[]
    for s in strategies:
        components = s.split(" ")
        strategyID = components[0]
        if strategyID == "0":
            list_strategy0.append(s)
        elif strategyID in ARCHITECTURAL_STRATEGIES:
            list_strategy_arch.append(s)
        elif strategyID in PATCHING_STRATEGIES:
            list_strategy_patch.append(s)
            
    
    #NoPlan
    df_noplan = df_security[df_security['strategy'].isin(list_strategy0)]
    df_device_0 = df_noplan[["dst",metricfield]]
    
    #Architectural
    df_architectural = df_security[df_security['strategy'].isin(list_strategy_arch)]
    df_device_arch = df_architectural[["dst",metricfield]].groupby(by=["dst"])
    
    #Patch
    df_patch = df_security[df_security['strategy'].isin(list_strategy_patch)]
    df_device_patch = df_patch[["dst",metricfield]].groupby(by=["dst"])
    
    #Plan
    with open(file_plan) as f: full_plan = json.load(f)
    
    # set width of bar 
    barWidth = 0.2
    fig = plt.subplots(figsize =(8, 5)) 

    # set height of bar 
    noplan = []
    arch = []
    patch = []
    plan = []
    for d in list(df_device_0["dst"]):
        
        list_strategy_plan=[]
        for s in strategies:
            components = s.split(" ")
            strategyID = components[0]
            if strategyID in list(map(str, full_plan[d])): 
                list_strategy_plan.append(s)
        
        df_plan = df_security[df_security['strategy'].isin(list_strategy_plan)]
        df_plan = df_plan[["dst",metricfield]].groupby(by=["dst"])
        
                        
        risk0=float(df_device_0[df_device_0['dst'] == d][metricfield])
        if d in dict(df_device_arch.groups).keys():
            riskarch=mean(list(df_device_arch.get_group(d)[metricfield]))
        else:
            riskarch=risk0
        if d in dict(df_device_patch.groups).keys():
            riskpatch=max(list(df_device_patch.get_group(d)[metricfield]))
        else:
            riskpatch=risk0  
            
        # if riskpatch>10000: riskpatch=9500 #TODO
        
        riskplan = risk0
        if len(list_strategy_plan)>0:
            riskplan=mean(list(df_plan.get_group(d)[metricfield]))
        
        noplan.append(risk0)
        arch.append(riskarch)
        patch.append(riskpatch)
        plan.append(riskplan)

    # Set position of bar on X axis 
    br1 = np.arange(len(noplan)) 
    br2 = [x + barWidth for x in br1] 
    br3 = [x + barWidth for x in br2] 
    br4 = [x + barWidth for x in br3] 

    # Make the plot
    plt.bar(br1, noplan, color = COLORS["NoAdaptation"], width = barWidth, 
            edgecolor ='grey', label ='NoAdaptation') 
    plt.bar(br2, arch, color = COLORS["Architectural"], width = barWidth, 
            edgecolor ='grey', label ='Architectural') 
    plt.bar(br3, patch, color = COLORS["Security"], width = barWidth, 
            edgecolor ='grey', label ='Security') 
    plt.bar(br4, plan, color = COLORS["SPARQ"], width = barWidth, 
            edgecolor ='grey', label ='SPARQ') 
    
    # Print information risk
    print(metricfield,"of network", net_tag)
    print("NoAdaptation", mean(noplan))
    print("Architectural", mean(arch))
    print("Security", mean(patch))
    print("SPARQ", mean(plan))
    print()
    
    # Adding Xticks 
    label_y = "Cyber Risk" if metricfield=="avg_risk" else "Num. Attacks"
    if metricfield=="avg_risk": plt.ylim(0,1)
    plt.xlabel('Devices', fontsize = 12) 
    plt.ylabel(label_y, fontsize = 12) 
    plt.xticks([r + barWidth for r in range(len(noplan))], 
            range(1, len(list(df_device_0["dst"]))+1))
    plt.legend(ncol=2)
    plt.savefig("experiments/plot/"+metricfield+"_"+net_tag+".png", bbox_inches='tight')

def plot_qos(file_security_metrics,file_qos_metrics,file_plan,folder_plans,file_network,metricfield,net_tag):
    
    with open(file_network) as f: devices = json.load(f)["devices"]
    with open(file_plan) as f_plan: full_plan = json.load(f_plan)
    
    #NoPlan
    noplandict={}
    df_noplan = pd.read_csv(file_qos_metrics)
    list_app = list(df_noplan["app"])
    for d in devices:
        deviceID = d["deviceId"]
        noplandict[deviceID]=[0]
        for app in list_app:
            if "app_"+app in d["applications"] or app in d["applications"]:
                values = df_noplan[df_noplan["app"] == app].drop(['topic','app'], axis=1)
                values_list = [x for xs in np.array(values).tolist() for x in xs]
                if deviceID not in noplandict.keys(): noplandict[deviceID] = values_list
                else: noplandict[deviceID]+=values_list
    
    #Architectural/Patch
    archdict={}
    patchdict={}
    plandict={}
    for d in devices:
        deviceID = d["deviceId"]
        archdict[deviceID]=[0]
        patchdict[deviceID]=[0]
        plandict[deviceID]=[0]
        for filename in os.listdir(folder_plans):
            if "csv" not in filename: continue
            df_file = pd.read_csv(folder_plans+filename)
            name_dev = filename.replace(".csv","")
        
            if name_dev == deviceID or name_dev in d["applications"]:
                strategyIDs = list(df_file["mitigationId"])
                for sID in strategyIDs:
                    if str(sID) in ARCHITECTURAL_STRATEGIES:
                        # if deviceID not in archdict.keys(): archdict[deviceID] = [float(df_file[df_file['mitigationId'] == sID][metricfield])]
                        # else: archdict[deviceID].append(float(df_file[df_file['mitigationId'] == sID][metricfield]))
                        archdict[deviceID].append(float(df_file[df_file['mitigationId'] == sID][metricfield]))
                    if str(sID) in PATCHING_STRATEGIES:
                        # if deviceID not in patchdict.keys(): patchdict[deviceID] = [float(df_file[df_file['mitigationId'] == sID][metricfield])]
                        # else: patchdict[deviceID].append(float(df_file[df_file['mitigationId'] == sID][metricfield]))
                        patchdict[deviceID].append(float(df_file[df_file['mitigationId'] == sID][metricfield]))
                    if str(sID) in list(map(str, full_plan[deviceID])): 
                        # if deviceID not in plandict.keys(): plandict[deviceID] = [float(df_file[df_file['mitigationId'] == sID][metricfield])]
                        # else: plandict[deviceID].append(float(df_file[df_file['mitigationId'] == sID][metricfield]))
                        plandict[deviceID].append(float(df_file[df_file['mitigationId'] == sID][metricfield]))
                      
                      
    # if net_tag=="SHnet": 
    #     print(noplandict)
    #     print(plandict)
      
    noplan = []
    arch = []
    patch = []
    plan = []
    for d in devices:
        deviceID = d["deviceId"]
        
        # if mean(noplandict[deviceID])>0.35: noplan.append(0.31) #TODO
        # else:noplan.append(mean(noplandict[deviceID]))
        
        arch.append(mean(archdict[deviceID]))
        patch.append(mean(patchdict[deviceID]))
        plan.append(mean(plandict[deviceID]))
    
    if net_tag=="HCnet":
        for i in range(0,len(noplan)):
            if (noplan[i] != 0 or arch[i] != 0) and patch[i] == 0:
                patch[i] = mean(patch)
            if (noplan[i] != 0 or arch[i] != 0) and plan[i] == 0:
                plan[i] = mean(plan)
            if noplan[i] == 0 and arch[i] != 0:
                noplan[i] = mean(noplan)
    
    # set width of bar 
    barWidth = 0.2
    fig = plt.subplots(figsize =(8, 5)) 
    
    # Set position of bar on X axis 
    br1 = np.arange(len(noplan)) 
    br2 = [x + barWidth for x in br1] 
    br3 = [x + barWidth for x in br2] 
    br4 = [x + barWidth for x in br3] 

    # Make the plot
    plt.bar(br1, noplan, color = COLORS["NoAdaptation"], width = barWidth, 
            edgecolor ='grey', label ='NoAdaptation') 
    plt.bar(br2, arch, color = COLORS["Architectural"], width = barWidth, 
            edgecolor ='grey', label ='Architectural') 
    plt.bar(br3, patch, color = COLORS["Security"], width = barWidth, 
            edgecolor ='grey', label ='Security') 
    plt.bar(br4, plan, color = COLORS["SPARQ"], width = barWidth, 
            edgecolor ='grey', label ='SPARQ') 
    
    # Print information risk
    print(metricfield,"of network", net_tag)
    print("NoAdaptation", mean(noplan))
    print("Architectural", mean(arch))
    print("Security", mean(patch))
    print("SPARQ", mean(plan))
    print()
    
    # Adding Xticks 
    plt.ylim(0,0.6)
    plt.xlabel('Devices', fontsize = 12) 
    plt.ylabel("Latency", fontsize = 12) 
    plt.xticks([r + barWidth for r in range(len(noplan))], 
            range(1, len(list(devices))+1))
    plt.legend(ncol=2)
    plt.savefig("experiments/plot/"+metricfield+"_"+net_tag+".png", bbox_inches='tight')
    

if __name__=="__main__":
    for net_tag in NET_TAGS:
        file_metrics_all = "data/"+net_tag+"-security-metrics-all.csv"
        file_metrics = "data/"+net_tag+"-security-metrics.csv"
        file_network = "data/"+net_tag+"-network.json"
        file_plan = "experiments/strategy_device_"+net_tag+".json"
        
        if net_tag == "SHnet":
            file_qos_metrics = "planning/qos-metrics_realnetwork.csv"
            folder_plans = "planning/metrics-per-device/realnetwork/"
        else:
            file_qos_metrics = "planning/qos-metrics.csv"
            folder_plans = "planning/metrics-per-device/healthcare/"
    
        plot_securitymetric(file_metrics_all,file_plan,net_tag,"avg_risk")
        plot_securitymetric(file_metrics_all,file_plan,net_tag,"num_paths")
        
        plot_qos(file_metrics_all,file_qos_metrics,file_plan,folder_plans,file_network,"avg_latency",net_tag)
