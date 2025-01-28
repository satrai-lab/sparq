import json, random

"""
Convert network scan to pub/sub format
(crf. real_network.json)
    "id": "",
    "deviceId": "",
    "deviceName": "",
    "publishFrequency": 1,
    "messageSize": 1,
    "distribution": "",
    "publishesTo": [],
    "cveList": [],
    "applications": []
"""
def convert_format(scan_format):
    with open(scan_format) as f: scan = json.load(f)

    format_devices=[]
    for d in scan["devices"]:
        id_dev = d["id"]
        name_dev = d["hostname"]

        cpe_list=[]
        cve_list=[]
        for iface in d["network_interfaces"]:
            for port in iface["ports"]:
                for service in port["services"]:
                    cpe_list = service["cpe_list"]
                    cve_list = service["cve_list"]
        apps=[]
        for cpe in cpe_list:
            component_cpe=cpe.split(":")
            apps.append(component_cpe[len(component_cpe)-1])


        format_devices.append({
            "id": id_dev,
            "deviceId": id_dev,
            "deviceName": name_dev,
            "publishFrequency": 1,
            "messageSize": random.randrange(101789,47583789),
            "distribution": "exponential",
            "publishesTo": [],
            "cveList": cve_list,
            "applications": apps
        })
    
    format_edges=[]
    for e in scan["edges"]:
        format_edges.append(e["host_link"])

    with open("data/hc_network_format.json", "w") as outfile:
        json_data = json.dumps({"devices":format_devices,
                                "vulnerabilities": scan["vulnerabilities"],
                                "edges": format_edges
                    },default=lambda o: o.__dict__, indent=2)
        outfile.write(json_data)

if __name__=="__main__":
    convert_format("data/hc_network.json")