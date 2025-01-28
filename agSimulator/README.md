# Attack Graph Simulator

This repository contains the scripts for running the AG simulator

## Usage

To run a simulation,

run the `ag_simulator.py` script as follows:

```
$ python ag_simulator.py <input_file> <network_tag>
```

where `<input_file>` is the default IoT network configuration, including devices, vulnerabilities, and reachability edges formatted according to the example network in the `data` folder, and `network_tag` is a meaningful identifier of the network (e.g., HC for Healthcare).

This command will run the simulation of multi-step attacks, collecting security metrics in two output files (`<net_tag>-security-metrics-all.csv` and `<net_tag>-security-metrics.csv`).

To reproduce the results in the paper, run the following command:

```
$ python ag_simulator.py 0 0
```
