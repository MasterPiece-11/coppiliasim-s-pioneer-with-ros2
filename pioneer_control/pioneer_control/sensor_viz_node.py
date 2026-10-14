import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import matplotlib.pyplot as plt

class SensorVizNode(Node):
    def __init__(self):
        super().__init__('sensor_viz_node')
        # Subscribe to the string topic we created in the Lua script
        self.subscription = self.create_subscription(
            String,
            '/ultrasonic_sensors',
            self.listener_callback,
            10)
        # Initialize an array of 16 sensors defaulting to 1.0 meter
        self.sensor_data = [1.0] * 16

    def listener_callback(self, msg):
        try:
            # Parse the comma-separated string back into a list of floats
            self.sensor_data = [float(x) for x in msg.data.split(',')]
        except ValueError:
            pass

def main(args=None):
    rclpy.init(args=args)
    node = SensorVizNode()
    
    # Set up the Matplotlib interactive plot
    plt.ion()
    fig, ax = plt.subplots()
    sensor_indices = range(1, 17) # Sensors 1 to 16
    
    try:
        while rclpy.ok():
            # Check for new ROS 2 messages without blocking
            rclpy.spin_once(node, timeout_sec=0.01)
            
            # Clear and redraw the graph
            ax.clear()
            ax.bar(sensor_indices, node.sensor_data, color='teal')
            
            # Format the graph limits and labels
            ax.set_ylim(0, 1.0)
            ax.set_xlim(0, 17)
            ax.set_xticks(sensor_indices)
            ax.set_ylabel('Distance to Obstacle (m)')
            ax.set_xlabel('Ultrasonic Sensor Number')
            ax.set_title('Real-Time Pioneer 3-DX Sensor Data')
            
            # Update the window
            plt.pause(0.05)
            
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
        plt.close('all')

if __name__ == '__main__':
    main()

