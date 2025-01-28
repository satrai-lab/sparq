import json, time, nvdlib, uuid
import networkx as nx
import pandas as pd

MITIGATION_FILE='data/NIST/cwe_mitigation.csv'

def build_panacea_reachability(file_net):
    with open(file_net) as f: sources = json.load(f)["sourceDevices"]

    edges=[]
    for src in sources:
        s=src["hostName"]
        for iface in src['reachedInterface']:
            for dev in iface['reachedDevices']:
                t=dev['hostName']
                edges.append((s,t))

    G=nx.DiGraph(edges)
    nx.write_graphml_lxml(G, "data/AG_healthcare.graphml")

def generate_vuln_files():
    ### ECG
    vuln_ecg=[]
    cve_ecg = nvdlib.searchCVE(keywordSearch='ECG')
    for cve in cve_ecg: 
        vuln_ecg.append(cve)
    with open("data/NIST/ecg.json", "w") as outfile:
        json_data = json.dumps({"vulnerabilities":vuln_ecg
                    },default=lambda o: o.__dict__, indent=2)
        outfile.write(json_data)

    time.sleep(6)
    ### XRAY
    vuln_xray=[]
    cve_xray = nvdlib.searchCVE(keywordSearch='x ray')
    for cve in cve_xray: 
        vuln_xray.append(cve)
    with open("data/NIST/xray.json", "w") as outfile:
        json_data = json.dumps({"vulnerabilities":vuln_xray
                    },default=lambda o: o.__dict__, indent=2)
        outfile.write(json_data)

    time.sleep(6)
    ### MAC
    vuln_mac=[]
    cve_mac = nvdlib.searchCVE(keywordSearch='Desktop Client macOS')
    for cve in cve_mac: 
        vuln_mac.append(cve)
    with open("data/NIST/mac.json", "w") as outfile:
        json_data = json.dumps({"vulnerabilities":vuln_mac
                    },default=lambda o: o.__dict__, indent=2)
        outfile.write(json_data)

    time.sleep(6)
    ### WINDOWS
    vuln_win=[]
    cve_win = nvdlib.searchCVE(keywordSearch='windows Remote Desktop Manager')
    for cve in cve_win: 
        vuln_win.append(cve)
    with open("data/NIST/win.json", "w") as outfile:
        json_data = json.dumps({"vulnerabilities":vuln_win
                    },default=lambda o: o.__dict__, indent=2)
        outfile.write(json_data)

    time.sleep(6)
    ### Postgres
    vuln_postgres=[]
    cve_postgres = nvdlib.searchCVE(keywordSearch='postgresql 15')
    for cve in cve_postgres: 
        vuln_postgres.append(cve)
    with open("data/NIST/postgres.json", "w") as outfile:
        json_data = json.dumps({"vulnerabilities":vuln_postgres
                    },default=lambda o: o.__dict__, indent=2)
        outfile.write(json_data)
    
    time.sleep(6)
    ### filebrowser
    vuln_file=[]
    cve_file = nvdlib.searchCVE(keywordSearch='filebrowser 2')
    for cve in cve_file: 
        vuln_file.append(cve)
    with open("data/NIST/file.json", "w") as outfile:
        json_data = json.dumps({"vulnerabilities":vuln_file
                    },default=lambda o: o.__dict__, indent=2)
        outfile.write(json_data)

    with open("data/NIST/storage.json", "w") as outfile:
        json_data = json.dumps({"vulnerabilities":vuln_ecg+vuln_xray+vuln_win+vuln_mac+vuln_file+vuln_postgres
                    },default=lambda o: o.__dict__, indent=2)
        outfile.write(json_data)


def getCweMitigation(cveid) :
    df = pd.read_csv(MITIGATION_FILE, sep=';')
    df = df[df['cve'] == cveid][["cve","phase","strategy"]]
    return df.to_dict('records')

def build_healtcare_net(num_ecg=1,num_xray=1,num_mac=1,num_win=1,num_db=1,num_file=1):
    ### ECG
    vulnid_ecg=[]
    mitig_ecg=[]
    with open("data/NIST/ecg.json") as f: vuln_ecg = json.load(f)["vulnerabilities"]
    for v in vuln_ecg: 
        vulnid_ecg.append(v["id"])
        mitig_ecg+=getCweMitigation(v["id"])
    ecg_hosts=[]
    for i in range(0,num_ecg):
        iddev=str(uuid.uuid4())
        ecg_hosts.append({
            'id': iddev,
            'hostname':"ECG",
            'network_interfaces':[{
                'ipaddress':"192.168.0.1",
                'macaddress':"ad:49:52:ba:19:76",
                'ports':[{
                    "number": 1883,
                    "state": "open",
                    "protocol": "MQTT",
                    "services": [{
                        "name": "pubsub",
                        "cve_list": vulnid_ecg
                    }]
                }]
            }]
        })

    ### xray
    vulnid_xray=[]
    mitig_xray=[]
    with open("data/NIST/xray.json") as f: vuln_xray = json.load(f)["vulnerabilities"]
    for v in vuln_xray: 
        vulnid_xray.append(v["id"])
        mitig_xray+=getCweMitigation(v["id"])
    xray_hosts=[]
    for i in range(0,num_xray):
        iddev=str(uuid.uuid4())
        xray_hosts.append({
            'id': iddev,
            'hostname':"xray",
            'network_interfaces':[{
                'ipaddress':"192.168.0.1",
                'macaddress':"ad:49:52:ba:19:76",
                'ports':[{
                    "number": 1883,
                    "state": "open",
                    "protocol": "MQTT",
                    "services": [{
                        "name": "pubsub",
                        "cve_list": vulnid_xray
                    }]
                }]
            }]
        })

    ### mac
    vulnid_mac=[]
    mitig_mac=[]
    with open("data/NIST/mac.json") as f: vuln_mac = json.load(f)["vulnerabilities"]
    for v in vuln_mac: 
        vulnid_mac.append(v["id"])
        mitig_mac+=getCweMitigation(v["id"])
    mac_hosts=[]
    for i in range(0,num_mac):
        iddev=str(uuid.uuid4())
        mac_hosts.append({
            'id': iddev,
            'hostname':"mac",
            'network_interfaces':[{
                'ipaddress':"192.168.0.1",
                'macaddress':"ad:49:52:ba:19:76",
                'ports':[{
                    "number": 1883,
                    "state": "open",
                    "protocol": "MQTT",
                    "services": [{
                        "name": "pubsub",
                        "cve_list": vulnid_mac
                    }]
                }]
            }]
        })

    ### win
    vulnid_win=[]
    mitig_win=[]
    with open("data/NIST/win.json") as f: vuln_win = json.load(f)["vulnerabilities"]
    for v in vuln_win: 
        vulnid_win.append(v["id"])
        mitig_win+=getCweMitigation(v["id"])
    win_hosts=[]
    for i in range(0,num_win):
        iddev=str(uuid.uuid4())
        win_hosts.append({
            'id': iddev,
            'hostname':"win",
            'network_interfaces':[{
                'ipaddress':"192.168.0.1",
                'macaddress':"ad:49:52:ba:19:76",
                'ports':[{
                    "number": 1883,
                    "state": "open",
                    "protocol": "MQTT",
                    "services": [{
                        "name": "pubsub",
                        "cve_list": vulnid_win
                    }]
                }]
            }]
        })

    ### postgres
    vulnid_postgres=[]
    mitig_postgres=[]
    with open("data/NIST/postgres.json") as f: vuln_postgres = json.load(f)["vulnerabilities"]
    for v in vuln_postgres: 
        vulnid_postgres.append(v["id"])
        mitig_postgres+=getCweMitigation(v["id"])
    postgres_hosts=[]
    for i in range(0,num_db):
        iddev=str(uuid.uuid4())
        postgres_hosts.append({
            'id': iddev,
            'hostname':"postgres",
            'network_interfaces':[{
                'ipaddress':"192.168.0.1",
                'macaddress':"ad:49:52:ba:19:76",
                'ports':[{
                    "number": 1883,
                    "state": "open",
                    "protocol": "MQTT",
                    "services": [{
                        "name": "pubsub",
                        "cve_list": vulnid_postgres
                    }]
                }]
            }]
        })

    ### file
    vulnid_file=[]
    mitig_file=[]
    with open("data/NIST/file.json") as f: vuln_file = json.load(f)["vulnerabilities"]
    for v in vuln_file: 
        vulnid_file.append(v["id"])
        mitig_file+=getCweMitigation(v["id"])
    file_hosts=[]
    for i in range(0,num_file):
        iddev=str(uuid.uuid4())
        file_hosts.append({
            'id': iddev,
            'hostname':"file",
            'network_interfaces':[{
                'ipaddress':"192.168.0.1",
                'macaddress':"ad:49:52:ba:19:76",
                'ports':[{
                    "number": 1883,
                    "state": "open",
                    "protocol": "MQTT",
                    "services": [{
                        "name": "pubsub",
                        "cve_list": vulnid_file
                    }]
                }]
            }]
        })

    edges=[]
    for h1 in ecg_hosts+xray_hosts:
        h1id=h1["id"]
        for h2 in postgres_hosts+file_hosts:
            h2id=h2["id"]
            if h1id!=h2id:
                edges.append([h1id,h2id])
                edges.append([h2id,h1id])
    
    for h1 in mac_hosts+win_hosts:
        h1id=h1["id"]
        for h2 in postgres_hosts+file_hosts:
            h2id=h2["id"]
            if h1id!=h2id:
                edges.append([h1id,h2id])
                edges.append([h2id,h1id])

    with open("data/healthcare_network.json", "w") as outfile:
        json_data = json.dumps({
            "devices": ecg_hosts+xray_hosts+mac_hosts+win_hosts+postgres_hosts+file_hosts,
            "vulnerabilities":vuln_ecg+vuln_xray+vuln_mac+vuln_win+vuln_postgres+vuln_file,
            "edges":edges,
            "mitigations": mitig_ecg+mitig_xray+mitig_mac+mitig_win+mitig_postgres+mitig_file
        },default=lambda o: o.__dict__, indent=2)
        outfile.write(json_data)


if __name__ == "__main__":
    # build_panacea_reachability("data/reachabilityInventory.json")
    generate_vuln_files()
    build_healtcare_net()