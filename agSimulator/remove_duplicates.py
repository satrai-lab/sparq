import csv, json
import pandas as pd

def remove_duplicates(input_file,output_file):
    # Read the CSV file
    df = pd.read_csv(input_file).drop('dst', axis=1)

    # Remove duplicate rows, keeping only the first occurrence
    df_no_duplicates = df.drop_duplicates(subset=['strategy'], keep='first')

    # Save the result to a new CSV file
    df_no_duplicates.to_csv(output_file, index=False)
    print(f"Duplicate rows have been removed. Cleaned data saved to '{output_file}'.")

def parse_applications(input_file,network_file,output_file):
    
    with open(network_file) as nf:
        devices = json.load(nf)["devices"]
    
    dict_res = []
    rules = []
    with open(input_file, 'r') as f:
        fr = csv.reader(f)
        i=0
        for row in fr:
            if i==0: 
                i+=1
                continue
            if i==1:
                dict_res.append({
                    "strategy":row[0],
                    "avg_lik":row[1],
                    "avg_imp":row[2],
                    "avg_risk":row[3],
                    "avg_len":row[4],
                    "num_paths":row[5],
                    "dst":row[6]
                })
                i+=1
                continue
            
            elems = row[0].split(" ")
            for app in elems[1:]:
                for dev in devices:
                    dev_apps = dev["applications"]
                    if app in dev_apps:
                        if elems[0]+" "+dev["id"] not in rules:
                            rules.append(elems[0]+" "+dev["id"])
                            dict_res.append({
                                "strategy":elems[0]+" "+dev["id"],
                                "avg_lik":row[1],
                                "avg_imp":row[2],
                                "avg_risk":row[3],
                                "avg_len":row[4],
                                "num_paths":row[5],
                                "dst":row[6]
                            })
                        # print(elems[0], dev["id"])
                    elif app == dev["id"]:
                        if row[0] not in rules:
                            rules.append(row[0])
                            dict_res.append({
                                "strategy":row[0],
                                "avg_lik":row[1],
                                "avg_imp":row[2],
                                "avg_risk":row[3],
                                "avg_len":row[4],
                                "num_paths":row[5],
                                "dst":row[6]
                            })
            i+=1
    
    with open(output_file, 'w', encoding='utf8', newline='') as output_file:
        fc = csv.DictWriter(output_file, fieldnames=dict_res[0].keys())
        fc.writeheader()
        fc.writerows(dict_res)
            
                
if __name__ == "__main__":
    parse_applications()