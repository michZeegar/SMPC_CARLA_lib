****************************
Discussion -
****************************


This chapter discusses some known problems of the CARLA simulation framework.

Vehicle Models Difference
==================================

The MPC controller currently uses a kinematic vehicle model, a simplified approximation compared to CARLA's realistic
model, especially in curves. 
Because kinematic models are a function of the vehicle geometry, they can represent the vehicle motion in a range of conditions that do not involve highly dynamic maneuvers and /or tire force saturation. 
Therefore, the MPC prediction has problems in the curve situation with a higher EV’s velocity and the start (== zero EV’s velocity). This model mismatch leads to a small lateral offset in curves.

MPC assumes that the first steering input is enough to bring the vehicle back to the curve centerlane, then only smaller inputs are planned to keep the vehicle on the centerlane. 
However, the first MPC input is not sufficient in the CARLA simulation, as the kinematic model overestimates the influence of the steering angle on the lateral motion.

casADi calculation errors 
====================================

By manually calculating the prediction steps under the suggested control from MPC, slightly different values result
compared to casADi can be observed. 
The reason is still unclear.


Reference curve problem 
===================================

The reference curve generation process has some problems getting the right sampling waypoints WP during intersections. 
Here, the MPC may assume that the passed waypoints of EV comes from a different direction. 
Also in some cases also the future direction is wrongly predicted.

The reason for this lies in the difficulty of finding the lane following waypoint if two or more possible WP successors points are available. 
The distinction is currently made based on the angle to the last sampled WP. 
Small angles are assumed to be lane following, angles above a threshold are labeled as right or left turns, depending on the sign of the angle. 
If there are only WP marked as turns, the one with the smaller angle is picked.
  

Visualization 
==================================

The calculation of the simulation is made with 30 fps.
However, the simulation of the simulation runs with 10-15 fps due to the current *GPU* limitation.
CARLA server alone needs already ~ 0.05-0.06 seconds to perform all the necessary simulation steps for the next frame.
With the additional computation of the OCP solving of the MPC, the passed time between two visualization frames t_vis is actual ~0.065-0.075 seconds.
This leads to visible fps output of 1/t_vis = 10-15 frames per seconds. 


So the visualization is actually running in slow motion.
