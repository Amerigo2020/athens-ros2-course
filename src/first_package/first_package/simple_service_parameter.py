import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
from rcl_interfaces.msg import SetParametersResult
from example_interfaces.srv import AddTwoInts


class AddTwoIntsServer(Node):
    def __init__(self):
        super().__init__('add_two_ints_server')
        self.declare_parameter('extra_term', 10)
        self.add_on_set_parameters_callback(self.parameter_callback)
        self.service = self.create_service(
            AddTwoInts, 'add_two_ints', self.handle_request
        )
        self.get_logger().info('Service mit Parameter extra_term bereit')

    def handle_request(self, request, response):
        extra_term = self.get_parameter('extra_term').value
        response.sum = request.a + request.b + extra_term
        self.get_logger().info(
            f'{request.a} + {request.b} + {extra_term} = {response.sum}'
        )
        return response

    def parameter_callback(self, params):
        for param in params:
            if param.name == 'extra_term':
                if param.type_ != Parameter.Type.INTEGER:
                    return SetParametersResult(
                        successful=False,
                        reason='extra_term muss eine ganze Zahl sein'
                    )
        return SetParametersResult(successful=True)


def main(args=None):
    rclpy.init(args=args)
    node = AddTwoIntsServer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
