# SPARQ: A QoS-Aware Framework for Mitigating Cyber Risk in Self-Protecting IoT Systems

## Abstract

SPARQ is a novel framework for designing self-protecting IoT systems that considers both the security exposure to cyber attacks and the QoS performance.
We leverage Attack Graph as a threat model for analyzing the cyber exposure of the system and Queuing Network Models to analyze QoS in IoT systems.
Based on the analysis outcomes, SPARQ provides mitigation plans to reduce the cyber risk while also minimizing the impact on QoS.

## Requirements

Currently, SPARQ runs on Linux machines.
You can find all requirements in the file requirements.txt and install using the following command:

`pip install requirements.txt`

## Repository structure

This repository contains the following folders:

- `agSimulator`: contains all the files to simulate mitigation actions with the attack graph model

- `data`: contains the data file for the healtchare and smart home networks used in the paper

- `experiments`: contains the results and plots of the performed experiments

- `planning`: contains all the files to plan the optimal set of mitigation actions

- `qosSimulator`: contains all the files to simulate mitigation actions with the queueing network models

## Installation instruction

SPARQ is a modular project and can be used for different purposes related to security with Attack Graph, simulations with Queueing Network, and AI planning. For this reason, you need to run different modules to reproduce the entire SPARQ pipeline.

### 1. Prerequisites

Store in the folder `data` the json format of your network. You will find two preconfigured network (smart home, SH, and healthcare, HC). Adjust the parameters in the `config.py` file.

### 2. Run [AG simulations](agSimulator/README.md)

### 3. Run [QoS simulations](qosSimulator/README.md)

### 4. Run the [AI planner](planning/README.md)

## Cite this work
```
@inproceedings{palma_sparq_2025,
	title = {{SPARQ}: {A} {QoS}-{Aware} {Framework} for {Mitigating} {Cyber} {Risk} in {Self}-{Protecting} {IoT} {Systems}},
	isbn = {979-8-3315-0181-5},
	shorttitle = {{SPARQ}},
	url = {https://www.computer.org/csdl/proceedings-article/seams/2025/018100a159/27vTocbbfe8},
	doi = {10.1109/SEAMS66627.2025.00025},
	abstract = {Today's smart spaces deploy various IoT devices to offer services for occupants. Such devices are exposed to security risks that may pose serious threats to network services and users' privacy. To avoid the disruption of normal operations, selfprotecting solutions have been developed to allow IoT networks to autonomously respond to cyber threats in real-time. However, existing self-protecting systems focus solely on architectural adaptations to respond to cyber threats, overlooking the mitigation actions described in cybersecurity standards -which represent the correct cybersecurity posture- as well as the impact of the adaptation strategies on the Quality-of-Service (QoS) performance. To overcome these existing limitations, this paper presents SPARQ, a novel framework for designing self-protecting IoT systems that considers both the security exposure to cyber attacks and the QoS performance. We leverage Attack Graph as a threat model for analyzing the cyber exposure of the system and Queuing Network Models to analyze QoS in IoT systems. Based on the analysis outcomes, SPARQ provides mitigation plans to reduce the cyber risk while also minimizing the impact on QoS. We evaluate the proposed approach on two use cases from real-world scenarios including a critical infrastructure and a smart home. The experimental evaluation shows that SPARQ is capable of reducing the cyber risk significantly while also improving the QoS performance by 35\% compared to existing approaches.},
	language = {English},
	urldate = {2025-06-17},
	publisher = {IEEE Computer Society},
	author = {Palma, Alessandro and Hassan, Houssam Hajj and Bouloukakis, Georgios},
	month = apr,
	year = {2025},
	pages = {159--170},
}
```
