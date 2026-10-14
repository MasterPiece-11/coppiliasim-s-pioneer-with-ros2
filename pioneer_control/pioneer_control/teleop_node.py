import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from pynput import keyboard
import sys

class GamepadTeleopNode(Node):
    def __init__(self):
        super().__init__('teleop_node')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        
        self.linear_speed = 0.0
        self.angular_speed = 0.0
        
        self.get_logger().info('Game Controls Active!')
        self.get_logger().info('Hold W/A/S/D to move. Release to stop. Press ESC to exit.')
        
        self.timer = self.create_timer(0.1, self.timer_callback)
        
        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release)
        self.listener.start()

    def on_press(self, key):
        try:
            if key.char == 'w':
                self.linear_speed = 0.5
            elif key.char == 's':
                self.linear_speed = -0.5
            elif key.char == 'a':
                self.angular_speed = 1.0
            elif key.char == 'd':
                self.angular_speed = -1.0
        except AttributeError:
            pass

    def on_release(self, key):
        try:
            if key.char in ['w', 's']:
                self.linear_speed = 0.0
            elif key.char in ['a', 'd']:
                self.angular_speed = 0.0
        except AttributeError:
            pass
            
        if key == keyboard.Key.esc:
            self.get_logger().info('Exiting teleop node...')
            sys.exit(0)
            return False

    def timer_callback(self):
        msg = Twist()
        msg.linear.x = self.linear_speed
        msg.angular.z = self.angular_speed
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = GamepadTeleopNode()
    
    try:
        rclpy.spin(node)
    except SystemExit:
        pass
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()