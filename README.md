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

🤖 CoppeliaSim Robot Setup (Required Script)
By default, the Pioneer P3DX in CoppeliaSim runs an automated Braitenberg obstacle-avoidance script. To allow ROS 2 to control the motors and read the sensors, you must replace this default brain with a custom ROS 2 bridge script.

1-Drag a Pioneer P3DX robot into your CoppeliaSim scene.

2-In the Scene Hierarchy, double-click the small paper/script icon next to the Pioneer robot.

3-Delete all the existing Lua code inside that window.

4-Paste the following script and close the window:
```Lua
sim = require('sim')
simROS2 = require('simROS2')

function sysCall_init()
    motorLeft = sim.getObject("../leftMotor")
    motorRight = sim.getObject("../rightMotor")
    
    usensors = {}
    for i=1,16,1 do
        usensors[i] = sim.getObject("../ultrasonicSensor",{index=i-1})
    end
    
    wheel_radius = 0.0975
    wheel_distance = 0.381 
    target_vL = 0
    target_vR = 0

    sub = simROS2.createSubscription('/cmd_vel', 'geometry_msgs/msg/Twist', 'cmd_vel_callback')
    
    -- Using String to bypass the missing MultiArray C++ compilation error
    pub = simROS2.createPublisher('/ultrasonic_sensors', 'std_msgs/msg/String')
end

function cmd_vel_callback(msg)
    local v = msg.linear.x
    local w = msg.angular.z
    target_vL = (v - w * wheel_distance / 2) / wheel_radius
    target_vR = (v + w * wheel_distance / 2) / wheel_radius
end

function sysCall_actuation()
    sim.setJointTargetVelocity(motorLeft, target_vL)
    sim.setJointTargetVelocity(motorRight, target_vR)
    
    local sensor_data = {}
    for i=1,16,1 do
        local res, dist = sim.readProximitySensor(usensors[i])
        if res > 0 then
            sensor_data[i] = string.format("%.3f", dist) -- Format to 3 decimal places
        else
            sensor_data[i] = "1.000" -- Default max distance if nothing is detected
        end
    end
    
    -- Join all 16 distances into a single comma-separated string
    local msg = {}
    msg.data = table.concat(sensor_data, ",")
    simROS2.publish(pub, msg)
end

function sysCall_cleanup()
    sim.setJointTargetVelocity(motorLeft, 0)
    sim.setJointTargetVelocity(motorRight, 0)
end
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
