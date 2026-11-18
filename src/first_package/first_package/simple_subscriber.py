# Course source: https://github.com/Robolabo/ROS_course
# Upstream revision: cf9e122904ebcb55d336aa7e82d0760bc94cbb07
# Template: Templates/2_simple_subscriber.py
# DONE marks code implementation, not a successful ROS/hardware test.
# Import the ROS2 Python client library
import rclpy
from rclpy.node import Node
# If the publisher uses Int data type, use:
# from std_msgs.msg import Int
# ADAPTATION: This chain uses the custom ExampleMessage instead.
from first_interfaces.msg import ExampleMessage


# Step 1: Define a class for the subscriber node
# Replace 'Node_ID' with a unique name for your group’s node (e.g., 'node_1' if you’re Group 1)
class MinimalSubscriber(Node):
    def __init__(self):
        # Initialize the node with the custom name 'node_NICKNAME'
        super().__init__('subscriber_7')
        # Step 2: Create a subscription to your group's topic
        # Replace 'topic_ID' with the topic name you want to subscribe to (e.g., 'topic_1' for Group 1)
        # The callback function 'listener_callback' will be called whenever a message is received
        # ADAPTATION: Subscribe to topic_7_out after the forwarding node.
        self.subscription = self.create_subscription(
            ExampleMessage, 'topic_7_out', self.listener_callback, 10
        )

    # Step 3: Define the callback function that will be called when a message is received
    def listener_callback(self, msg):
        # Log the received message to the console
        self.get_logger().info(
            f'Received: {msg.my_string}, Wert: {msg.my_float}, '
            f'Array: {list(msg.my_float_array)}'
        )



# Step 4: Define the main function to run the node
def main(args=None):
    # Initialize the ROS2 Python client library
    rclpy.init(args=args)
    # Create an instance of the MinimalSubscriber node
    node = MinimalSubscriber()
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
