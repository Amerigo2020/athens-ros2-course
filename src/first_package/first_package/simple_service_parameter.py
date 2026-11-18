# Course source: https://github.com/Robolabo/ROS_course
# Upstream revision: cf9e122904ebcb55d336aa7e82d0760bc94cbb07
# Template: Templates/4_simple_service_parameter.py
# DONE marks code implementation, not a successful ROS/hardware test.
# 1. Import necessary libraries and custom message/service types
import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
from rcl_interfaces.msg import SetParametersResult
from first_interfaces.srv import ExampleService


# 2. Define the AddTwoIntsServer class
# Objective:
# To create a ROS 2 node that uses parameters in a service to add two integers
# and an extra term defined by the parameter value and return the sum.
class AddTwoIntsServer(Node):
    def __init__(self):
        super().__init__('add_two_ints_server')
        # 3. Declare the parameter 'extra_term' with a default value of 10
        self.declare_parameter('extra_term', 10)
        # Register callback to detect parameter updates dynamically
        self.add_on_set_parameters_callback(self.parameter_callback)
        # DONE (template TODO): 4. Create the service
        # The service name is 'add_two_ints'
        # The service type is your custom srv interface
        # The callback function is 'handle_request'
        self.service = self.create_service(
            ExampleService, 'add_two_ints', self.handle_request
        )
        self.get_logger().info('Service mit Parameter extra_term bereit')

    # DONE (template TODO): 5. Define the handle_request method to process the request and return the response
    def handle_request(self, request, response):
        # Add the parameter value to the sum
        # Update the extra term to the current value of the param:
        extra_term = self.get_parameter('extra_term').value
        response.sum = request.a + request.b + extra_term
        self.get_logger().info(
            f'{request.a} + {request.b} + {extra_term} = {response.sum}'
        )
        # Return the response to the client
        return response

    # DONE (template TODO): 6. Implement the parameter callback to update 'extra_term' dynamically
    def parameter_callback(self, params):
        for param in params:
            # ADAPTATION (template TODO): Update self.extra_term with the new parameter value.
            # rclpy applies accepted parameter updates; handle_request reads the current value
            # rather than keeping a second self.extra_term attribute.
            if param.name == 'extra_term':
                if param.type_ != Parameter.Type.INTEGER:
                    return SetParametersResult(
                        successful=False,
                        reason='extra_term muss eine ganze Zahl sein'
                    )
        # DONE (template TODO): Return SetParametersResult confirming success
        return SetParametersResult(successful=True)


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
