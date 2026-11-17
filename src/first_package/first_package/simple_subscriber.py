import rclpy
from rclpy.node import Node
from first_interfaces.msg import ExampleMessage


class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__('subscriber_7')
        self.subscription = self.create_subscription(
            ExampleMessage, 'topic_7_out', self.listener_callback, 10
        )

    def listener_callback(self, msg):
        self.get_logger().info(
            f'Received: {msg.my_string}, Wert: {msg.my_float}, '
            f'Array: {list(msg.my_float_array)}'
        )



def main(args=None):
    rclpy.init(args=args)
    node = MinimalSubscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
