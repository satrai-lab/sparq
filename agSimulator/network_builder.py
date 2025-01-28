import nvdlib, time, json, uuid

from config import nvd_complete_dump

ZNN_sw_list=[
    'apache jmeter 2.7',
    'modsecurity apache 2.7.5',
    'apr 1.4.6',
    'mysql 5.5.25',
    'apr util 1.4.1',
    'nagios 3.4.1',
    'nagiosgraph 1.4.4',
    'nagios plugins 1.4.15',
    'freetype 2.4.0',
    'nrpe 2.13',
    'httpd 2.4.2',
    'pcre 8.20',
    'libgd 2.1.0',
    'perl 5.20.2',
    'libpng 1.6.6',
    'php 5.6.2',
    'libxml2 2.9.2',
    'libz 1.2.3.4'
]
"""
1-5 'mysql 5.5.25', ==> MYSQL

6-12 'freetype 2.4.0', ==> WEB

13-25 'httpd 2.4.2', ==> LB, WEB

26 'libgd 2.1.0', ==> WEB

27-90 'php 5.6.2', == WEB

91-96'libxml2 2.9.2', ==> LB
"""

def get_cve(cpe_str):
    time.sleep(6)
    cve_list = nvdlib.searchCVE(cpeName = cpe_str, limit=2000)
    cve_ids=[]
    vulnerabilities=[]
    for curr_cve in cve_list:
            if len(curr_cve)>0:
                cve_ids.append(curr_cve.id)
                vulnerabilities.append(curr_cve)    
    if "oracle" in cpe_str: 
        return {
            'id': str(uuid.uuid4()),
            'hostname':"oracle server",
            'hosttype':"server",
            'network_interfaces':[{
                'ipaddress':"158.898.83.22",
                'macaddress':"ad:49:52:ba:19:76",
                'ports':[{
                    "number": 8080,
                    "state": "open",
                    "protocol": "TCP",
                    "services": [{
                        "name": "training port",
                        "cpe_list": [cpe_str],
                        "cve_list": cve_ids
                    }]
                }]
            }]
        }, vulnerabilities
    else: 
        return {
            'id':str(uuid.uuid4()),
            'hostname':"tensorflow client",
            'hosttype':"client",
            'network_interfaces':[{
                'ipaddress':"158.898.83.23",
                'macaddress':"ad:49:52:ba:19:77",
                'ports':[{
                    "number": 8080,
                    "state": "open",
                    "protocol": "TCP",
                    "services": [{
                        "name": "training port",
                        "cpe_list": [cpe_str],
                        "cve_list": cve_ids
                    }]
                }]
            }]
        }, vulnerabilities

def build_znn_net():
    #### BY FILE
    # with open(nvd_complete_dump) as f: nvd_dump = json.loads(f.read())
    # for page in nvd_dump:
    #     for nvd_cve_struct in page["vulnerabilities"]:
    #         if nvd_cve_struct["cve"]["id"] in total_vulnerability_set:
    #             vulnerability_list.append(nvd_cve_struct["cve"])

    #### BY NIST API
    vulnerabilities=[]
    for sw in ZNN_sw_list:
        time.sleep(6)
        cve_list = nvdlib.searchCVE(keywordSearch=sw, limit=2000)
        for curr_cve in cve_list:
            if len(curr_cve)>0: vulnerabilities.append(curr_cve)
        print(len(vulnerabilities))
    
    with open("data/znn_vulns.json", "w") as outfile:
        json_data = json.dumps({"vulnerabilities":vulnerabilities
                    },default=lambda o: o.__dict__, indent=2)
        outfile.write(json_data)
    return

if __name__=="__main__":
    build_znn_net()

    # server_cpe="cpe:2.3:a:oracle:sun_zfs_storage_appliance_kit:8.8.3:*:*:*:*:*:*:*"
    # tensorflow_cpe1="cpe:2.3:a:combust:mleap:0.18.0:*:*:*:*:*:*:*"
    # tensorflow_cpe2="cpe:2.3:a:google:tensorflow:0.1.7:*:*:*:lite:*:*:*"
    # d1,v1=get_cve(server_cpe)
    # d2,v2=get_cve(tensorflow_cpe1)
    # d3,v3=get_cve(tensorflow_cpe2)

    # edges=[]
    # for d_src in [d1,d2,d3]:
    #     d_id_src=d_src["id"]
    #     for d_dst in [d1,d2,d3]:
    #         d_id_dst=d_dst["id"]
    #         if d_id_src!=d_id_dst and [d_id_src,d_id_dst] not in edges:
    #             edges.append([d_id_src,d_id_dst])

    # with open("data/federated_network.json", "w") as outfile:
    #     json_data = json.dumps({"devices":[d1,d2,d3],
    #                             "vulnerabilities":v1+v2+v3,
    #                             "edges": edges
    #                 },default=lambda o: o.__dict__, indent=2)
    #     outfile.write(json_data)