# SMPC_carla
MPC control framework for CARLA simulation. 
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
