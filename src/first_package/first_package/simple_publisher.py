# Course source: https://github.com/Robolabo/ROS_course
# Upstream revision: cf9e122904ebcb55d336aa7e82d0760bc94cbb07
# Template: Templates/1_simple_publisher.py
# DONE marks code implementation, not a successful ROS/hardware test.
# Import the ROS2 Python client library
import rclpy
from rclpy.node import Node
from first_interfaces.msg import ExampleMessage


# Step 1: Define a class for the publisher node
# Replace 'Node_ID' with a unique name for your group’s node (e.g., 'node_1' if you’re Group 1)
class MinimalPublisher(Node):
    def __init__(self):
        # Initialize the node with the custom name 'node_NICKNAME'
        super().__init__('publisher_7')
        # Step 2: Create a publisher for your topic
        # Replace 'topic_ID' with a unique topic name (e.g., 'topic_1' for Group 1)
        self.publisher_ = self.create_publisher(
            ExampleMessage, 'topic_7', 10
        )
        # Step 4: Initialize a counter to keep track of message numbers
        self.i = 0
        # Step 3: Set a timer to publish messages at a chosen frequency
        # Modify 'timer_period' to control how often messages are published (e.g., 2.0 for every 2 seconds)
        self.timer = self.create_timer(2.0, self.timer_callback)

    # Step 5: Define the callback function that will be called by the timer
    def timer_callback(self):
        # Create a new String message
        # ADAPTATION: The exercise now uses ExampleMessage, not String.
        msg = ExampleMessage()
        # Customize the message data with a unique message
        # Modify the message content to include your group number and a custom message
        msg.my_float = float(self.i)
        msg.my_float_array = [1.0, 2.0, 3.0]
        msg.my_string = f'Hallo von Gruppe 7, Nachricht {self.i}'

        # Publish the message
        self.publisher_.publish(msg)
        # Log the published message to the console
        self.get_logger().info(f'Publishing: {msg}')
        # Increment the message counter
        self.i += 1


# Step 6: Define the main function to run the node
def main(args=None):
    # Initialize the ROS2 Python client library
    rclpy.init(args=args)
    # Create an instance of the MinimalPublisher node
    node = MinimalPublisher()
    try:
        # Run the node until interrupted
        rclpy.spin(node)
    # Gracefully handle shutdown when Ctrl+C is pressed
    except KeyboardInterrupt:
        pass
    finally:
        # Destroy the node and shutdown the ROS2 Python client library
        node.destroy_node()
        rclpy.try_shutdown()


# Entry point of the script
if __name__ == '__main__':
    main()
