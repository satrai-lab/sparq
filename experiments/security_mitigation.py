import json, os, sys
import numpy as np
from cwe2.database import Database
from matplotlib import pyplot as plt

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from config import NET_TAGS

# Associate strategies to each device
# MITIGATION_FILE='../_NIST/cwe_mitigation.csv'

MAPPING ={
    "Libraries or Frameworks":1,
    "Attack Surface Reduction":2,
    "Refactoring":3,
    "Language Selection":4,
    "Compilation or Build Hardening":5,
    "Environment Hardening":6,
    "Sandbox or Jail":7,
    "Parameterization":8,
    "Firewall":9,
    "Traffic redirection":10,
    "Reconfigure the network":11,
    "Enforcement by Conversion":12,
    "Separation of Privilege":13,
    "Resource Limitation":14,
    "Output Encoding":15,
    "Change IP address":16,
    "Restart":17,
    "Input Validation":18,
    "Packet dropping":19,
    "Network disconnection":20,
    "Process termination":21,
    "Block port":22,
    "Quarantine":23,
    "Switch off device":24,
    "Modify trust":25
}

EXECUTION_STRATEGY={
    "long":[1,2,3,4,5,6,7,8,9,19,11],
    "medium":[12,13,14,15,16],
    "short":[17,18,19,29,21,22,23,24,25]
}
EQUIVALENT_STRATEGY={
    "delay":[1,17],
    "reduce":[2,9,10,11,13,14,18,19,20,21,22,24],
    # "reduce":[13,14],
    "patch":[3,4,5,6,7,8,12,15,16,23,25]
}

def getCweMitigation(cveid, vulnerabilities):
    # df = pd.read_csv(MITIGATION_FILE, sep=';')
    # df = df[df['cve'] == cveid][["cve","phase","strategy"]]
    # return df.to_dict('records')
    cwe_list=[]
    for vuln in vulnerabilities:
        if vuln["id"]==cveid:
            if "cwe" in vuln.keys():
                for cwe in vuln["cwe"]:
                    if "value" in cwe.keys(): cwe_id = cwe["value"].replace("CWE-","")
                    else: cwe_id = cwe["cweId"].replace("CWE-","")
                    if cwe_id not in cwe_list: 
                        cwe_list.append(cwe_id)
                
    db = Database()
    result=[]
    for cwe_ in cwe_list:
        try:
            weakness = db.get(cwe_)
            mitigation = weakness.potential_mitigations
            
            if "STRATEGY" in mitigation:
                elem = mitigation.split(":STRATEGY:")[1]
                strategy_name = elem.split(":")[0]
                result.append({
                    "cve": cveid,
                    "cwe": cwe_,
                    "strategy": strategy_name
                })
        except:
            print(cwe_, " has not entry")
    return result
        

def getStrategyDevice(file_network, net_tag):
    with open(file_network) as f:
        content = json.load(f)
    devices = content["devices"]
    vulnerabilities = content["vulnerabilities"]
    
    strategies_GT={}
    strategies_GT_index={}
    for dev in devices:
        id_dev = dev["id"]
        strategies_GT[id_dev] = []
        strategies_GT_index[id_dev]=[]
        for cve in dev["cveList"]:
            mitigations = getCweMitigation(cve,vulnerabilities)
            for mitig in mitigations:
                if mitig["strategy"] != "Unknown" and mitig["strategy"] not in strategies_GT[id_dev]:
                    strategies_GT[id_dev].append(mitig["strategy"])
                    strategies_GT_index[id_dev].append(MAPPING[mitig["strategy"]])
    
    # with open("experiments/strategy_device.json", "w") as outfile: 
    #     json.dump(strategies_GT, outfile)
    # with open("experiments/strategy_device_id.json", "w") as outfile: 
    with open("experiments/strategy_device_"+net_tag+".json", "w") as outfile: 
        json.dump(strategies_GT_index, outfile)
    return strategies_GT

def getPlanStrategy(folder_planningfiles, net_tag):
    strategies_computed = {}
    for file in os.listdir(folder_planningfiles):
        if "plan_problem" in file:
            with open(folder_planningfiles+"/"+file, 'r') as fileread:
                for line in fileread:
                    if "MetricValue" in line:
                        cost = line.split(" ")[-1].replace("\n","")
                    if "0:" in line:
                        body = line.split("(")[1].split(")")[0].split(" ")
                        strategy_id = body[0].split("-")[1]
                        devapp_id = body[1].lower()
                        strategies_computed[devapp_id] = {
                            "strategy": strategy_id,
                            "cost": cost
                        }
    with open("experiments/strategy_computed_"+net_tag+".json", "w") as outfile: 
        json.dump(strategies_computed, outfile)

def compare_strategies(gt_file, predict_file, device_file):
    with open(device_file) as dv: devices = json.load(dv)["devices"]
    with open(gt_file) as gt: planGT = json.load(gt)
    with open(predict_file) as pp: planPredict = json.load(pp)
    
    TP=0
    TN=0
    FP=0
    FN=0
    for dev in devices:
        dev_id = dev["deviceId"]
        apps = dev["applications"]
        
        for k_predict in planPredict.keys():
            if (k_predict in apps) or (k_predict==dev_id):
                predicted = int(planPredict[k_predict]["strategy"])
                
                category_predicted=""
                for cat in EQUIVALENT_STRATEGY.keys():
                    if predicted in EQUIVALENT_STRATEGY[cat]:
                        category_predicted= cat
                        
                for k_gt in planGT.keys():
                    if k_gt == dev_id:
                        
                        categories_gt=[]
                        for elem in planGT[k_gt]:
                            for cat_gt in EQUIVALENT_STRATEGY.keys():
                                if elem in EQUIVALENT_STRATEGY[cat_gt]:
                                    if cat_gt not in categories_gt: 
                                        categories_gt.append(cat_gt)
        print(category_predicted, categories_gt)        
        if category_predicted=="" and len(categories_gt)==0: TN+=1
        elif category_predicted=="" and len(categories_gt)>=1: FN+=1
        elif category_predicted!="" and category_predicted in categories_gt: TP+=1
        elif category_predicted!="" and category_predicted not in categories_gt: FP+=1
    return TP,TN,FN,FP                                    
                            
def plot_confusion_matrix(TP,TN,FN,FP, net_tag):
    TOT=TP+FN+FP+TN
    print("Accuracy: ", (TP+TN)/TOT)

    confusion_m = np.matrix([[TP, FP], [FN, TN]])
    annot_text = np.matrix([["TP\n"+str(round(TP/TOT*100,2))+"%", "FP\n"+str(round(FP/TOT*100,2))+"%"], ["FN\n"+str(round(FN/TOT*100,2))+"%", "TN\n"+str(round(TN/TOT*100,2))+"%"]])

    fig = plt.figure(figsize=(8, 4))
    ax = plt.subplot(1, 2, 2)
    plt.imshow(confusion_m, interpolation='nearest', cmap=plt.cm.Blues)

    rows, cols = confusion_m.shape
    for i in range(rows):
        for j in range(cols):
            if i==0 and j==0:
                plt.text(j, i, annot_text[i, j], horizontalalignment='center', verticalalignment='center', color='white', fontsize=14)
            else:
                plt.text(j, i, annot_text[i, j], horizontalalignment='center', verticalalignment='center', color='black', fontsize=14)
    # min_val = min([TP,TN,FP,FN])
    # max_val = max([TP,TN,FP,FN])
    # sns.heatmap(confusion_m, vmin=min_val,vmax=max_val,linewidth=0.5,annot=annot_text,fmt="s",yticklabels=False,xticklabels=False,ax=axs,cmap="Blues")

    precision=round(TP/(TP+FP),2)
    recall=round(TP/(TP+FN),2)
    F1Score=round(2*(precision*recall)/(precision+recall),2)
    plt.title(f'Precision: {precision}, Recall: {recall}, F1: {F1Score}')
    plt.xticks([])
    plt.yticks([])
    plt.savefig("experiments/plot/conf_m_"+net_tag+".png", bbox_inches='tight')
    plt.close(fig)        
        
if __name__=="__main__":
    for net_tag in NET_TAGS:
        network_file = "data/"+net_tag+"-network.json"
        file_plan = "experiments/strategy_device_"+net_tag+".json"
        file_strategy = "experiments/strategy_computed_"+net_tag+".json"
        
        if net_tag == "SHnet":
            folderplans = "planning/planning-files/real_network"
        else:
            folderplans = "planning/planning-files/healthcare"
        
        strategy_per_device = getStrategyDevice(network_file,net_tag)
        getPlanStrategy(folderplans,net_tag)
        TP,TN,FN,FP = compare_strategies(file_plan, file_strategy, network_file)
        plot_confusion_matrix(TP,TN,FN,FP,net_tag)
            