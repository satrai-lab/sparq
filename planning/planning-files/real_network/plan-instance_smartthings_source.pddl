

NUMERIC_THREATS_MODE: 0

; Command line: ./lpg-td -o domain-instance_smartthings_source.pddl -f problem-instance_smartthings_source.pddl -n 1   


Parsing domain file:  domain 'IOT-DOMAIN-SMARTTHINGS_SOURCE' defined ... done.
Parsing problem file:  problem 'IOT-PROBLEM' defined ... done.



Modality: Incremental Planner

Number of actions             :       5
Number of conditional actions :       0
Number of facts               :       2


Analyzing Planning Problem:
	Temporal Planning Problem: NO
	Numeric Planning Problem: YES
	Problem with Timed Initial Literals: NO
	Problem with Derived Predicates: NO

Evaluation function weights:
     Action duration 0.00; Action cost 1.00


Computing mutex... done

Preprocessing total time: 0.00 seconds

Searching ('.' = every 50 search steps):
 solution found: 
 first_solution_cpu_time: 0.00 

Plan computed:
   Time: (ACTION) [action Duration; action Cost]
 0.0000: (STRATEGY-21 SMARTTHINGS_SOURCE) [D:1.00; C:463.78]



METRIC_VALUE = 463.78
Solution number: 1
Total time:      0.00
Search time:     0.00
Actions:         1
Duration:        1.000
Plan quality:    463.784 
Total Num Flips: 1
     Plan file:       plan_problem-instance_smartthings_source.pddl_1.SOL

