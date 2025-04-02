import csv
import time
from controller import Supervisor

# Create Supervisor instance
robot = Supervisor()

# Time step of the simulation
TIME_STEP = int(robot.getBasicTimeStep())

# Get the pedestrian node
pedestrian_node = robot.getFromDef("PEDESTRIAN")
if pedestrian_node is None:
    print("Error: No pedestrian found with DEF name 'PEDESTRIAN'")
    exit()

# Get pedestrian's translation and physics fields
translation_field = pedestrian_node.getField("translation")
physics_field = pedestrian_node.getField("physics")

# Disable physics for smooth position updates
if physics_field is not None:
    physics_field.setSFString("")

# CSV file path
csv_path = "/home/deepak/Documents/Astro_rob/pedestrian_motion.csv"

# Read trajectory from CSV file
trajectory = []

try:
    with open(csv_path, "r") as file:
        reader = csv.reader(file)
        header = next(reader)  # Skip header
        
        for row in reader:
            try:
                x, y = map(float, [row[1], row[2]])  # Extract X and Y (columns B, C)
                fixed_z = 1.27  # Keep Z constant
                trajectory.append([x, y, fixed_z])
            except ValueError:
                print(f"Skipping row due to conversion error: {row}")
except Exception as e:
    print(f"Error reading CSV file: {e}")
    exit()

# Check if trajectory data is available
if not trajectory:
    print("Error: No valid trajectory data found in CSV.")
    exit()

# Move pedestrian along the trajectory
for position in trajectory:
    translation_field.setSFVec3f(position)  # Update position
    print(f"Moving to position: {position}")

    if robot.step(TIME_STEP) == -1:  # Process Webots step
        break

    time.sleep(0.1)  # Delay for smoother movement

print("Trajectory execution completed.")
