import json, csv, os.path, sys
import pandas as pd
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from attack_graph import generate_ag_model, generate_paths, analyze_network, get_vulns_by_hostid
from remove_duplicates import parse_applications
from config import NET_TAGS

#Startegy IDs: 10,11,16,17,25
def no_strategy(devices,vulnerabilities,edges):
    dev_IDs=[]
    for d in devices: dev_IDs.append(d["id"])

    AG = generate_ag_model(devices,vulnerabilities,edges)
    paths_dev = generate_paths(vulnerabilities, AG, dev_IDs, dev_IDs)
    
    qos_strategies=[]
    for dev in devices:
        iddev = dev["id"]
        qos_strategies.append("0 "+iddev)
    return analyze_network(paths_dev, qos_strategies, True)

#Startegy IDs: 1-9,12-15,18
def strategy_vulnerability(devices,vulnerabilities,edges,dev_patch,vuln_patch,net_tag):
    dev_IDs=[]
    for d in devices: dev_IDs.append(d["id"])

    AG = generate_ag_model(devices,vulnerabilities,edges,[vuln_patch["id"]],[dev_patch["id"]])
    paths_dev = generate_paths(vulnerabilities, AG, dev_IDs, dev_IDs)

    qos_strategies=[]
    for descr in vuln_patch["descriptions"]:
        if net_tag=="SHnet":
            if "size" in descr["value"]:
                qos_strategies.append("14 <"+dev_patch["id"]+", "+str(dev_patch["messageSize"]/2)+">")
                continue
        else:
            if "size" in descr[0]:
                qos_strategies.append("14 <"+dev_patch["id"]+", "+str(dev_patch["messageSize"]/2)+">")
                continue
    for app in dev_patch["applications"]:
        qos_strategies.append("2 "+ app)
        qos_strategies.append("9 "+ app)
    return analyze_network(paths_dev, qos_strategies)

#Startegy IDs: 19-24
def strategy_host(devices,vulnerabilities,edges,dev_removed):
    dev_IDs=[]
    for d in devices: dev_IDs.append(d["id"])

    AG = generate_ag_model(devices,vulnerabilities,edges)
    paths_dev = generate_paths(vulnerabilities, AG, dev_IDs, dev_IDs)

    appString=""
    for app in dev_removed["applications"]:
        if app not in appString:
            appString+=app+" "
    qos_strategies=[
        "18 "+appString,
        "19 "+appString,
        "20 "+dev_removed["id"]+" ",
        "21 "+dev_removed["id"]+" ",
        "22 "+dev_removed["id"]+" ",
        "24 "+dev_removed["id"]+" "
    ]
    return analyze_network(paths_dev, qos_strategies)

def format_security_metrics(input_metrics, output_metrics):
    df = pd.read_csv(input_metrics)
    df_nodup = df.groupby('strategy').mean().reset_index()
    df_nodup.to_csv(output_metrics, index=False)

def run_ag_simulator(input_file_p,net_tag_p):
    if input_file_p==0 and net_tag_p==0:
        for net_tag in NET_TAGS:
            file_metrics_all = "data/"+net_tag+"-security-metrics-all.csv"
            file_metrics = "data/"+net_tag+"-security-metrics.csv"
            file_network = "data/"+net_tag+"-network.json"
            
            with open(file_network) as nf:
                content = json.load(nf)
            devices=content["devices"]
            vulnerabilities=content["vulnerabilities"]
            edges=content["edges"]

            ## no strategy
            metrics_nostrategy=no_strategy(devices,vulnerabilities,edges)

            metrics=metrics_nostrategy
            with open(file_metrics_all, 'w', encoding='utf8', newline='') as output_file:
                fc = csv.DictWriter(output_file, fieldnames=metrics[0].keys())
                fc.writeheader()
                fc.writerows(metrics)
            print("Simulation no strategy protection")

            ## host
            metrics_host=[]
            for d in devices:
                devices_h = [dev for dev in devices if dev['id'] != d["id"]]
                metrics_host+=strategy_host(devices_h,vulnerabilities,edges,d)
                print("Simulation strategy protection for host ", d["id"])
            
            metrics=metrics_nostrategy+metrics_host
            with open(file_metrics_all, 'w', encoding='utf8', newline='') as output_file:
                fc = csv.DictWriter(output_file, fieldnames=metrics[0].keys())
                fc.writeheader()
                fc.writerows(metrics)

            ## vuln
            metrics_vuln=[]
            for d in devices:
                for v in vulnerabilities:
                    dev_vuln=get_vulns_by_hostid(d['id'],devices)
                    if v['id'] in dev_vuln[:100]:
                        metrics_vuln+=strategy_vulnerability(devices,vulnerabilities,edges,d,v, net_tag)
                        # print(d["id"],v["id"])
                        print("Simulation patching", v['id'], "in host ", d["id"])
                print("Simulation patching vulnerabilities in host ", d["id"])
                    
            metrics=metrics_nostrategy+metrics_host+metrics_vuln
            with open(file_metrics_all, 'w', encoding='utf8', newline='') as output_file:
                fc = csv.DictWriter(output_file, fieldnames=metrics[0].keys())
                fc.writeheader()
                fc.writerows(metrics)
                
            
            if net_tag=="HCnet":
                parse_applications(file_metrics_all,file_network,file_metrics_all)
            
    else:
        file_metrics_all = "data/"+net_tag_p+"-security-metrics-all.csv"
        file_metrics = "data/"+net_tag_p+"-security-metrics.csv"
        file_network = input_file_p
        
        with open(file_network) as nf:
            content = json.load(nf)
        devices=content["devices"]
        vulnerabilities=content["vulnerabilities"]
        edges=content["edges"]

        ## no strategy
        metrics_nostrategy=no_strategy(devices,vulnerabilities,edges)

        metrics=metrics_nostrategy
        with open(file_metrics_all, 'w', encoding='utf8', newline='') as output_file:
            fc = csv.DictWriter(output_file, fieldnames=metrics[0].keys())
            fc.writeheader()
            fc.writerows(metrics)
        print("Simulation no strategy protection")

        ## host
        metrics_host=[]
        for d in devices:
            devices_h = [dev for dev in devices if dev['id'] != d["id"]]
            metrics_host+=strategy_host(devices_h,vulnerabilities,edges,d)
            print("Simulation strategy protection for host ", d["id"])
        
        metrics=metrics_nostrategy+metrics_host
        with open(file_metrics_all, 'w', encoding='utf8', newline='') as output_file:
            fc = csv.DictWriter(output_file, fieldnames=metrics[0].keys())
            fc.writeheader()
            fc.writerows(metrics)

        ## vuln
        metrics_vuln=[]
        for d in devices:
            for v in vulnerabilities:
                dev_vuln=get_vulns_by_hostid(d['id'],devices)
                if v['id'] in dev_vuln[:100]:
                    metrics_vuln+=strategy_vulnerability(devices,vulnerabilities,edges,d,v, net_tag_p)
                    # print(d["id"],v["id"])
                    print("Simulation patching", v['id'], "in host ", d["id"])
            print("Simulation patching vulnerabilities in host ", d["id"])
                
        metrics=metrics_nostrategy+metrics_host+metrics_vuln
        with open(file_metrics_all, 'w', encoding='utf8', newline='') as output_file:
            fc = csv.DictWriter(output_file, fieldnames=metrics[0].keys())
            fc.writeheader()
            fc.writerows(metrics)

if __name__ == "__main__":
    
    input_file_p= sys.argv[1]
    net_tag_p= sys.argv[2]
    run_ag_simulator(input_file_p,net_tag_p)
    
    