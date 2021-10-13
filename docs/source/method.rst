****************************
Method -
****************************


This chapter depicts how to operate CARLA with MPC control scripts and how to start a CARLA server.
First, a small summary of the necessary installation steps is given to initialize the CARLA system like assumed in the later sections.
The second section assumes that CARLA system is already installed.



Quick start guide
==================

If everthing is already installed, the MPC CARLA simulation can  be started as followed:
    
    1. Opening up two terminals.
    2. Starting the carla server in the first terminal with::
        
        carla-serv
    
    3. Navigate in the second terminal to the SMPC_Carla directory by::
        
        cd SMPC_carla/
        
    4. Start the simulation in the second terminal with the following command (but wait till carla server runs smoothly)::
        
        python3 simpleCar_MPC2.py
        

Installation
==============

This section shows the required installation steps to retrieve the same system as the carla-simulation computer located in the LSR student lab. 


Installing CARLA 
--------------------

To install CARLA system follow the instructions on `CARLA install <https://carla.readthedocs.io/en/latest/start_quickstart/>`_.

The most important commands are the following::
    
    pip install --user pygame numpy
    sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 1AF1527DE64CB8D9
    sudo add-apt-repository "deb [arch=amd64] http://dist.carla.org/carla $(lsb_release -sc) main"
    sudo apt-get update # Update the Debian package index
    sudo apt-get install carla-simulator # Install the latest CARLA version, or update the current installation
    cd /opt/carla-simulator # Open the folder where CARLA is installed
        
        

The following sections are assuming that CARLA is installed as a Debian installation.

To make CARLA accessible as a python package, the CARLA PythonAPI package has to be installed with the carla-*-
py3.*.egg file located inside CARLA installation location at /opt/carla-simulator/PythonAPI/carla/dist/.

    
    
Installing casADi 
----------------------

The MPC control method uses casADi to solve the optimal control problem (OCP). 
Therefore, casADi has to be installed before starting any MPC script for CARLA. 

CasADi provides an extra mpctools package for python, which is available on `MPCTOOLS CASADI <https://https://bitbucket.org/rawlings-group/mpc-tools-casadi/src/master/>`_.

Use the following command inside the downloaded mpctools directory to install the python package mpctools for casADi::

    python3 mpctoolssetup.py install --user


    
Installing the MPC CARLA package 
-----------------------------------

The MPC control methods can also be installed as a python package by executing the following inside the *SMPC_Carla* directory::
    
     pip3 install --user -e .

     

Usage CARLA
=============

.. _client-server:
.. figure::  /_static/carla_client_overview.pdf 

    Client-server architecture overview.

The CARLA simulator consists of a scalable client and server architecture (:numref:`client-server`).

    * CARLA server: 
                    Responsible for everything related with the simulation itself: computation of physics, updates on the world-state and its actors and much more. 
                    As it aims for realistic results, the best fit would be running the server with a dedicated GPU, especially when dealing with machine learning.
    * Client side: 
                    Consisting of a sum of client modules controlling the logic of actors on scene. 
                    A example for a client script is the script ‘simpleCar_MPC2.py’. 
                    
     
Starting the CARLA Server 
-------------------------

To start a CARLA server use the following command::
    
    carla-serv

In case this commands is not already in your local bash-alias list, you can add the command by::

    echo "alias carla-serv='bash /opt/carla-simulator/CarlaUE4.sh'" >> ~/.bashrc
    
    
Starting the MPC client script
--------------------------------

The necessary layout of a CARLA script using the MPC control approach is presented in ‘simpleCar_MPC2.py’.
To start a script inside CARLA, a CARLA server must be running, and then in a second terminal, a script can be
executed.

The scripts must be executed with python3; python2 causes malfunction.
Example::

    python3 simpleCar_MPC2.py -f './logs/ff_states_log.h5'
    
With this script, an additional window should open, which shows a car on the CARLA TOWN04 (:numref:`town04`) controlled by MPC control logic.
The passed arguments with -f refers to the desired filename of the log-data and the saving location. 
Other possible arguments to pass along with the script are the size of the up-poping window, with -x
and -y for the corresponding sizes.
It also possible to change the port of the CARLA server to listen to by passing -p and the respective port number.

In the visualization window (shown in :numref:`carlaVis`) , the green line shows the reference curve used in the MPC OCP problem.
The yellow lines show the prediction from implemented MPC vehicle model by using the derived controls. 
Crosses mark sample waypoints, which are used in the reference curve approximation and the conversion to a road-aligned EV-state.


.. _carlaVis:
.. figure::  /_static/CARLA_script.png
   :align:   center

   Visualization of CARLA with MPC control script.


.. _town04:
.. figure::  /_static/Town04.jpg 
   :align:   center

   Town4 of the CARLA map package.


Structure of the MPC approach 
=========================================

The design of the MPC controller can be split into the three major parts, as also shown in :numref:`client-server`:

    1. Script to interact with *CARLA* server:
        Synchronization of the optimization process with the CARLA server.
        Triggering a new Carla frame after finishing the other two scripts
        Sending the derived optimal control to the CARLA server.
    2. Script to generate reference curve and handle further constraints:
        Mathematical approximation of the reference curve from the given road layout information from the CARLA server.
        Providing the OCP with an optimization goal and with scenario constraint based on the current scene.\
        Performes the logging process of the Frenet Frame states.
    3. Road-aligned MPC class:
        Solving the OCP by having the position of the CARLA vehicle, the reference curve, and WP_C and WP_N.
        The solving process is solved every 6th simulation timestep, in the other simulation timesteps the previous derived optimal control is used. (simulation timestep = 1/30 seconds ==> solving OCP every 0.2 seconds)
        The road-aligned MPC class is implemented in the model_predicitve_control.py.


All the basic functions to convert the ego vehicle (EV)'s xy-state to a road-aligned state are collected in the file waypoint_utilities.py.

MPC Constraints
----------------

So far only three simple cases of traffic scenes are realized in simpleCar_MPC_TVs.py

    1. Case B:  one target vehicle (TV)  in front (same lane)  is consider for constraints --> vertical xi constraint.
    2. Case D:  one TV in front (same lane) is considered, constraint set to overtake the TV.
    3. Case B + F: one TV vehicle in front and one TV on right lane of EV consider in constraints.

The control agent class is responsible for analyzing the scene and sending the fitted constraint to OCP problem of the MPC.

The constraint are split into hard and soft constraints.
Hard constraints limiting the legible state space by considering the time-varying position of the other vehicles.
Soft constraints ensure a desired behaviour depending on the scene.
For example in case B, a vertical constraint approximately 30 meters beyond the rear of the TV front of the EV establish a safe distance to the TV in front.


MPC - FT - Architecture
--------------------------

The script simpleCar_MPC_FT.py, control_agent_mpc_ft.py, ft_mpc.py contain a draft version of a SMPC + FT control layout.
The general framework is similar to the one shown in :numref:`client-server`, however here the control agent contains additionally a second MPC controller.
This second MPC controller derives a failsafe trajectory based on the predicted state after applying the derived u_0 control of the first agent.
The framework is described in [Bruedigam2020]_ in great detail.

.. [Bruedigam2020] Brüdigam, T., Olbrich, M., Wollherr, D., and Leibold, M., “Stochastic Model Predictive Control with a Safety Guarantee for Automated Driving”, `link <https://arxiv.org/pdf/2009.09381.pdf>`_, 2020.


The constraints for the FT MPC method works similar like to the normal MPC, the control agent sends them based on the current scene (other TVs).
A difference is that the FT MPC class method holds to every time a FT safe trajectory for the EV (accessible with agent_ft.controller.failsafe_trajectory).
Then if the FT controller does not find a legible solution, the saved ft trajectory gets reinitialized with a emergency braking one.

Visualization of the MPC performance 
===============================================

To evaluate the performance, the EV's road-aligned state will be logged and later be plotted.
A variety of helping plotting functions can be found in 'visualization_tools.py'.

The jupyter-script 'Visualization_frenet.ipynb' gives an example of helping evaluation plots.

Quick visualization guide
--------------------------

    1. Open new terminal and navigate to SMPC folder ::

        cd SMPC_carla/

    2. Opening a jupyter server with::

        jupyter-lab

    3. Select the Visualization_MPC.ipynb file and change the variable file to the desired recording to visualize

    4. To Execute a row of code in jupyter, use the enter key in the desired row (every has to be reexecuted by restarting the notebook)



