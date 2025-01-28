# QoS Simulator

This repository contains the scripts for running the QoS simulator

## Usage

To run a simulation, run the `qos-simualtor.sh` script as follows:

```
$ ./qos-simulator.sh <input_file> <output_file> <simulation_duration> <alias> <strategyId> <arguments>
```

where `<input_file>` is the default IoT network configuration, `<output_file>` is the path to the file where you would like to have the dataset, `<simulation_duration>` is the maximum duration of the simulation (in seconds), `<alias>` is an ID to give to the simulation, `<strategyId>` is the Id of the mitigation strategy to be applied, and `<arguments>` are the remaining arguments, according to the strategy used.
For example, to use strategy `10` to the IoT network defined in `scenarios/sample-scenario-default.json`, you can use the following command:

```
$ ./qos-simulator.sh scenarios/sample-scenario-default.json dataset.csv 60 experiment1 10 <app_app1, topic_topic1> <app_app2, topic_topic1 topic_topic2>`
```

This command will run the simulation for 60 seconds, and the results to the file `output.csv1`.
Refer to the file `4-strategies.xlsx` to check possible mitigation strategies, their Id, and the format of their command.
