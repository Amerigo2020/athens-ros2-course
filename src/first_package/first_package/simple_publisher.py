import rclpy
from rclpy.node import Node
from first_interfaces.msg import ExampleMessage


class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('publisher_7')
        self.publisher_ = self.create_publisher(
            ExampleMessage, 'topic_7', 10
        )
        self.i = 0
        self.timer = self.create_timer(2.0, self.timer_callback)

    def timer_callback(self):
        msg = ExampleMessage()
        msg.my_float = float(self.i)
        msg.my_float_array = [1.0, 2.0, 3.0]
        msg.my_string = f'Hallo von Gruppe 7, Nachricht {self.i}'

        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: {msg}')
        self.i += 1


def main(args=None):
    rclpy.init(args=args)
    node = MinimalPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()