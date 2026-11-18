# Course source: https://github.com/Robolabo/ROS_course
# Upstream revision: cf9e122904ebcb55d336aa7e82d0760bc94cbb07
# Template: Templates/3_simple_service.py
# DONE marks code implementation, not a successful ROS/hardware test.
# 1. Import necessary libraries and custom message/service types
import rclpy
from rclpy.node import Node
from first_interfaces.srv import ExampleService


# 2. Define the AddTwoIntsServer class
# The Objective:
# To create a ROS 2 node that provides a service to add two integers and return the sum.
class AddTwoIntsServer(Node):
    def __init__(self):
        super().__init__('add_two_ints_server')
        # DONE (template TODO): 3. Create the service
        # The service name is 'add_two_ints'
        # The service type is your custom srv interface
        # The callback function is 'handle_request'
        self.service = self.create_service(
            ExampleService, 'add_two_ints', self.handle_request
        )
        self.get_logger().info('Service /add_two_ints bereit')

    # DONE (template TODO): 4. Define the handle_request method to process the request and return the response
    def handle_request(self, request, response):
        # Add a and b (first part of the service interface)
        # ADAPTATION: The template also says "Add the parameter value to sum".
        # The basic service has no extra parameter; see simple_service_parameter.py.
        response.sum = request.a + request.b
        self.get_logger().info(
            f'{request.a} + {request.b} = {response.sum}'
        )
        # Return the response to the client
        return response


# Define the main function to run the node
def main(args=None):
    # Initialize the ROS2 Python client library
    rclpy.init(args=args)
    node = AddTwoIntsServer()
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


if __name__ == '__main__':
    main()
