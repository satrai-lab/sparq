import sys, os, subprocess
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

# from attack_graph import generate_ag_model, generate_paths, analyze_paths
from agSimulator.ag_simulator import run_ag_simulator

def run_qos_simulator(input_file,output_file,simulation_duration,alias,mitigation_args):
    logfile = "simulations_log.log"
    
    # Remove logfile if it exists
    if os.path.exists(logfile):
        os.remove(logfile)
    
    # Check if mitigation arguments are provided
    if not mitigation_args:
        print("WARNING: No mitigation strategy is specified! Running normal simulation.")
        subprocess.run(["java", "-jar", "edict.jar", input_file, output_file, simulation_duration, alias])
        # Remove unnecessary files
        for file in os.listdir("./qosSimulator/scenarios/jsimg/"):
            if file.endswith(".jsimg"):
                os.remove(os.path.join("./qosSimulator/scenarios/jsimg/", file))
        sys.exit(0)
    
    strategy = mitigation_args[0]
    mitigation_array = [2, 9, 10, 11, 13, 14, 22]
    
    # Check if the strategy is in the predefined array
    if int(strategy) in mitigation_array:
        subprocess.run(["python", "qosSimulator/apply_mitigation_strategies.py", input_file, *mitigation_args])
    
    # Run the Java program
    subprocess.run(["java", "-jar", "edict.jar", input_file, output_file, simulation_duration, alias, *mitigation_args])
    
    # Remove unnecessary files
    for file in os.listdir("./qosSimulator/scenarios/jsimg/"):
        if file.endswith(".jsimg"):
            os.remove(os.path.join("./qosSimulator/scenarios/jsimg/", file))
            
def run_palnner():
    command = [
        "./lpg-td", 
        "-o", "domain-instance_app_app1.pddl", 
        "-f", "problem-instance_app_app1.pddl", 
        "-n", "1"
    ]
    try:
        # Run the command and capture the output
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print("Command executed successfully:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("An error occurred while running the command:")
        print(e.stderr)

if __name__ == "__main__":
    
    input_file_p= sys.argv[1]
    net_tag_p= sys.argv[2]
    simulation_duration = sys.argv[3]
    alias = sys.argv[4]
    mitigation_args = sys.argv[5:]  # All arguments after the fourth

    run_ag_simulator(input_file_p,net_tag_p)
    run_qos_simulator(input_file_p,"data/"+net_tag_p+"-qos-metrics.csv",simulation_duration,alias,mitigation_args)
    
    