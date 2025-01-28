import os, json, time, nvdlib, uuid
import networkx as nx
import pandas as pd

DEVICES_CVE={
    "printing_source":"toshiba printers",
    "energymanagement_source":"energy management cloud services",
    "occupancymanagement_source":"avtech",
    "videosurveillance_source":"synology camera",
    "firedetection_source":"firesight",
    "intrusiondetection_source":"snort",
    "amazonecho_source":"amazon echo",
    "smartthings_source":"smartthings",
    "bms_source":"bems"
}
DEVICES_APP={
    "printing_source":"TS",
    "energymanagement_source":"AN",
    "occupancymanagement_source":"TS",
    "videosurveillance_source":"VS",
    "firedetection_source":"RT",
    "intrusiondetection_source":"RT",
    "amazonecho_source":"AN",
    "smartthings_source":"AN",
    "bms_source":"TS"
}

def generate_reach_edges(iot_traces):
    with open(iot_traces) as f: content = json.load(f)
    applications=content["applications"]
    topics=content["topics"]

    edges=[]
    for topic in topics:
        topic_pubDevs=topic["publishers"]
        topic_subApps=topic["subscribers"]
        for pub_id in topic_pubDevs:
            for subApp in topic_subApps:
                for app in applications:
                    if subApp==app["applicationId"]: 
                        subCategory=app["applicationCategory"]
                        for dev_category_k in DEVICES_APP.keys():
                            if subCategory == DEVICES_APP[dev_category_k] and \
                            dev_category_k!=pub_id and [pub_id,dev_category_k] not in edges:
                                edges.append([pub_id,dev_category_k])
    return edges  

def generate_vuln_files():
    vulns={}
    vulns_list=[]
    for dev in DEVICES_CVE.keys():
        time.sleep(6)
        vulns[dev]=[]
        cve_search = DEVICES_CVE[dev]
        cve_list = nvdlib.searchCVE(keywordSearch=cve_search)
        for cve in cve_list: 
            vulns[dev].append(cve)
            vulns_list.append(cve)
        with open("data/real-network_backup.json", "a+") as outfile:
            json_data = json.dumps({"vulnerabilities":vulns[dev]
                        },default=lambda o: o.__dict__, indent=2)
            outfile.write(json_data)

    with open("data/real-network-vulnerabilities.json", "w") as outfile:
        json_data = json.dumps({"vulnerabilities":vulns_list
                    },default=lambda o: o.__dict__, indent=2)
        outfile.write(json_data)
    os.remove("data/real-network_backup.json")
    return

def generate_dev_list(iot_traces, vuln_file):
    with open(iot_traces) as f: content = json.load(f)
    with open(vuln_file) as g: vulnerabilities = json.load(g)["vulnerabilities"]

    iot_devices=content["IoTdevices"]
    applications=content["applications"]
    topics=content["topics"]

    devices=[]
    for dev in iot_devices:
        devid=dev["deviceId"]
        dev_cpy=dev
        dev_cpy["id"]=devid
        dev_cpy["cveList"]=[]
        dev_cpy["applications"]=[]

        cve_k=DEVICES_CVE[devid]
        for vuln in vulnerabilities:
            for vuln_descr in vuln["descriptions"]:
                if cve_k in vuln_descr["value"].lower():
                    dev_cpy["cveList"].append(vuln["id"])
        
        for app in applications:
            category = app["applicationCategory"]
            if category == DEVICES_APP[devid]:
                dev_cpy["applications"].append(app["applicationId"])

        devices.append(dev_cpy)
    return devices

if __name__ == "__main__":
    iot_trace_file="qosSimulator/scenarios/real-traces-default.json"
    vuln_file="data/real-network-vulnerabilities.json"
    
    devices = generate_dev_list(iot_trace_file, vuln_file)
    # generate_vuln_files()
    with open(vuln_file) as g: vulnerabilities = json.load(g)["vulnerabilities"]
    edges = generate_reach_edges(iot_trace_file)
    
    with open("data/real_network.json", "w") as outfile:
        json_data = json.dumps({
            "devices": devices,
            "vulnerabilities": vulnerabilities,
            "edges":edges
        },default=lambda o: o.__dict__, indent=2)
        outfile.write(json_data)