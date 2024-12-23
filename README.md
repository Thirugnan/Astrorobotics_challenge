 # Astrorobotics Challenge

This repository contains the solution for the Astrorobotics Challenge. Follow the steps below to set up and execute the solution.


---


### Setup Instructions



### Step 1: Create a Workspace

Start by creating a workspace for the project:

bash```
mkdir astrorobot_ws
cd astrorobot_ws
```

---

### Step 2: Clone Required Repositories

2.1 Create a subfolder named src:

bash```
mkdir src
cd src
```



2.2 Clone the required repositories with the following commands:

bash```
git clone https://github.com/nithishk03/astrorobotics_challenge.git
git clone --branch ros2 https://github.com/aws-robotics/aws-robomaker-small-warehouse-world.git aws-robomaker-small-warehouse-world
```


2.3 Navigate back to the root directory:

bash```
cd ..
```

---

### Step 3: Install Dependencies and Build the Workspace

Use these commands to install dependencies and build the workspace:

bash```
rosdep install --from-paths . --ignore-src -r -y
colcon build
```

### Step 4: Source the Workspace

Set up the environment by sourcing the workspace:

bash```
source install/setup.bash
```
---

### Step 5: Run the Simulation and Navigation

5.1 Spawn the robot in the Gazebo environment:

bash```
ros2 launch robot_bringup bringup.launch.py
```
5.2 Launch the navigation stack:

bash```
ros2 launch robot_navigation navigation.launch.py
```
5.3 Move the robot through waypoints:

bash```
ros2 run robot_navigation waypoint_node
