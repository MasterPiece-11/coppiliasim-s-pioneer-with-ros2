# coppiliasim's-pioneer-with-ros2
Pioneer ROS 2 Teleop Controller 🕹️
A ROS 2 package to teleoperate a Pioneer P3DX robot in CoppeliaSim using keyboard inputs.

This node acts as a publisher, sending geometry_msgs/Twist messages to the /cmd_vel topic at 10Hz to control the differential drive kinematics of the simulated robot.

🛠️ Prerequisites
Before building, ensure you have the following installed on your system:

ROS 2: (Jazzy)

CoppeliaSim: With the ROS 2 Interface plugin enabled.

pynput: This Python package is required to capture keyboard events. Install it via pip:
```bash
pip3 install pynput
```

🏗️ Build Instructions

1- Navigate to the src directory of your ROS 2 workspace:
```bash
cd ~/ros2_ws/src
```
{Change ros2_ws with your ros2 workspace name}

2-Extract or clone this pioneer_control package into the src directory.

3-Return to the root of your workspace and build the package:
```bash
cd ~/ros2_ws
colcon build --packages-select pioneer_control
```
4-Source the workspace overlay to make the package visible to ROS 2:
```bash
source install/setup.bash
```
🗺️ CoppeliaSim Scene Setup (Important)
To fully test the robot's capabilities, your CoppeliaSim scene should contain blocks or obstacles for the robot to navigate around.

⚠️ Troubleshooting Ultrasonic Sensors:
If you add obstacles but the Pioneer's ultrasonic proximity sensors do not detect them, the objects are likely missing the correct physical properties. To fix this:

1-Double-click the obstacle in the Scene Hierarchy to open its properties.
2-Navigate to the Common properties tab.
3-Under the Object special properties section, ensure the "Detectable" checkbox is checked.

🚀 Run Instructions

1-Start the Simulation:
Open CoppeliaSim, load your scene with the Pioneer P3DX and obstacles, and press the Play button.

2-Run the Teleop Node:
Open a new terminal, source your workspace, and launch the node:
```bash
source ~/ros2_ws/install/setup.bash
ros2 run pioneer_control teleop_node
```

3-run the subscriber:
in another terminal, run 
```bash
ros2 run pioneer_control sensor_viz_node
```

(Note: If your entry point in setup.py is named differently, replace teleop_node with your exact executable name).

🎮 Usage
Ensure the terminal running the node is actively selected (in focus). Use the following keys to drive the robot:

W - Move forward

S - Move backward

A - Rotate counter-clockwise (left)

D - Rotate clockwise (right)

ESC - Exit the node gracefully
