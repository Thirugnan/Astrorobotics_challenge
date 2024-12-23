# Astrorobotics Challenge

This repository contains the solution for the Astrorobotics Challenge. Follow the steps below to set up and run the solution.

---

## Setup Instructions

### Step 1: Create a Workspace
Create a new workspace for the project:

bash
mkdir astrorobot_ws
cd astrorobot_ws


### Step 2: Download the required Repository's

2.1 Create a sub-folder called src


bash
mkdir src
cd src

2.2 git the clone the two required repository's by the following commands:

bash
git clone https://github.com/nithishk03/astrorobotics_challenge.git
git clone --branch ros2 https://github.com/aws-robotics/aws-robomaker-small-warehouse-world.git aws-robomaker-small-warehouse-world


2.3 Return to the root directory:
bash
cd ..

---
### Step 3: Install Dependencies and Build the Workspace

Run the following commands:

bash
rosdep install --from-paths . --ignore-src -r -y
colcon build


---
### Step 4: Source the Workspace

Source the workspace to set up the environment:

bash
source install/setup.bash


---

### Step 5: Run the Simulation and Navigation
5.1. Spawn the Robot in the Gazebo Environment

Run the following command:

bash
ros2 launch robot_bringup bringup.launch.py


5.2. Launch the Navigation Stack:

bash
ros2 launch robot_navigation navigation.launch.py


5.3. Move the Robot Through Waypoints

bash
ros2 run robot_navigation waypoint_node


#Thank you!! <
