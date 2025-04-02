import csv
import os
from controller import Supervisor, Keyboard

# Create the Supervisor instance
robot = Supervisor()

# Time step of the simulation
TIME_STEP = int(robot.getBasicTimeStep())

# Enable keyboard input
keyboard = robot.getKeyboard()
keyboard.enable(TIME_STEP)

# Get the pedestrian node
pedestrian_node = robot.getFromDef("PEDESTRIAN")
if pedestrian_node is None:
    print("Error: No pedestrian found with DEF name 'PEDESTRIAN'")
    exit()

# Get pedestrian's translation and rotation fields
translation_field = pedestrian_node.getField("translation")
rotation_field = pedestrian_node.getField("rotation")
physics_field = pedestrian_node.getField("physics")

# Check if fields exist
if translation_field is None or rotation_field is None:
    print("Error: Unable to access translation or rotation fields")
    exit()

# Check if pedestrian has physics
has_physics = physics_field is not None

# Movement parameters
speed = 0.09  # Movement speed
fixed_z = 1.27  # Keep Z at 1.27 permanently

# Boundary limits
x_min, x_max = -21.4, 21.4  # X-boundary conditions
y_min, y_max = -21.4, 21.4  # Y-boundary conditions

# Define rotation angles for each direction
rotation_angles = {
    "X+": [0, 0, 1, 0],      # Facing right (+X direction)
    "X-": [0, 0, 1, 3.14],   # Facing left (-X direction)
    "Y+": [0, 0, 1, 1.57],   # Facing up (+Y direction)
    "Y-": [0, 0, 1, -1.57]   # Facing down (-Y direction)
}

# Key mappings
KEY_UP = Keyboard.UP       # Move +X direction
KEY_DOWN = Keyboard.DOWN   # Move -X direction
KEY_LEFT = Keyboard.LEFT   # Move +Y direction
KEY_RIGHT = Keyboard.RIGHT # Move -Y direction

# CSV file setup
csv_dir = "/home/deepak/Documents/Astro_rob"
csv_file = os.path.join(csv_dir, "pedestrian_motion.csv")
if not os.path.exists(csv_dir):
    os.makedirs(csv_dir)

# Open CSV file and write header
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Time", "X", "Y", "Radian"])  # Updated header

while robot.step(TIME_STEP) != -1:
    key = keyboard.getKey()

    if key == -1:
        continue  # Skip loop iteration if no key is pressed (stops updating console & CSV)

    position = translation_field.getSFVec3f()
    new_x, new_y = position[0], position[1]
    rotation = rotation_field.getSFRotation()
    radian = rotation[3]  # Extract rotation in radians

    # Movement logic with boundary conditions
    if key == KEY_UP and new_x + speed <= x_max:
        new_x += speed
        rotation_field.setSFRotation(rotation_angles["X+"])
    elif key == KEY_DOWN and new_x - speed >= x_min:
        new_x -= speed
        rotation_field.setSFRotation(rotation_angles["X-"])
    elif key == KEY_LEFT and new_y + speed <= y_max:
        new_y += speed
        rotation_field.setSFRotation(rotation_angles["Y+"])
    elif key == KEY_RIGHT and new_y - speed >= y_min:
        new_y -= speed
        rotation_field.setSFRotation(rotation_angles["Y-"])
    else:
        continue  # Skip logging if no valid key is pressed

    # Apply movement
    if has_physics:
        velocity_x = speed if key == KEY_UP and new_x < x_max else -speed if key == KEY_DOWN and new_x > x_min else 0
        velocity_y = speed if key == KEY_LEFT and new_y < y_max else -speed if key == KEY_RIGHT and new_y > y_min else 0
        pedestrian_node.getField("velocity").setSFVec3f([velocity_x, velocity_y, 0])
    else:
        translation_field.setSFVec3f([new_x, new_y, fixed_z])

    # Log data to CSV
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([robot.getTime(), new_x, new_y, radian])  # Write radian value
    
    # Debugging info
    print(f"Time: {robot.getTime()} | Position: x={new_x}, y={new_y}, z={fixed_z} | Radian: {radian}")
