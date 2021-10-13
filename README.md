# SMPC_carla
MPC control framework for CARLA simulation. 

---

## Structure of directory 

 1. Report: Containing everything related to the report (latex source file, report, ..:)
 2. Presentation: Contains powerpoint presentation + pdf version 
 3. mpcCARLA: Containing the python libary for mpc controller for the CARLA vehicle simulator
 4. tools: Visualization tools to analyze the performance of the MPC controller (jupyter notebooks)
 5. logs + plots: Dedicated saving location for log-files and created logs from the visualizing tools
 6. docs: Documentation how to use the mpcCarla libary based on the simulation computer in the LSR lab


---

## How to install libary
 
	pip3 install --user -e .  

---

## How to start example controller

First start Carla server on your system (carla needs to be installed first, command can differ for different systems): 

	./opt/carla-simulator/CarlaUE4.sh
	
More information on this can be found in the documentation.

Starting MPC vehicle controller: 

	python3 simpleCar_MPC2.py -f './logs/*xy*.h5'
