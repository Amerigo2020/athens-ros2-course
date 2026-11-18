"""Nonblocking serial bridge using the final D1 custom interfaces."""
import time
import math
import serial
import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import ParameterDescriptor
from stm_interfaces.msg import STMState, STMControl
from .protocol import parse_state, encode_control


class SerialNode(Node):
    state_message_type = STMState
    control_message_type = STMControl

    def __init__(self, enable_control=True):
        super().__init__('stm_serial_node')
        defaults = {'port': '/dev/ttyACM0', 'baudrate': 115200,
                    'loop_frequency': 100.0, 'command_timeout': 0.5}
        for name, value in defaults.items():
            self.declare_parameter(name, value, ParameterDescriptor(read_only=True))
        frequency = self.get_parameter('loop_frequency').value
        self.timeout = self.get_parameter('command_timeout').value
        if not all(math.isfinite(v) and v > 0 for v in (frequency, self.timeout)):
            raise ValueError('Frequency and timeout must be positive')
        self.device = serial.Serial(self.get_parameter('port').value,
                                    self.get_parameter('baudrate').value,
                                    timeout=0, write_timeout=0.1)
        self.buffer = bytearray()
        self.last_command = time.monotonic()
        self.active = False
        self.publisher = self.create_publisher(self.state_message_type, 'stm_state', 10)
        if enable_control:
            self.subscription = self.create_subscription(
                self.control_message_type, 'stm_control', self.control, 10)
        self.timer = self.create_timer(1.0 / frequency, self.tick)

    def control(self, msg):
        try:
            values = self.control_values(msg)
            command = encode_control(*values)
            self.device.write(command)
            self.last_command = time.monotonic()
            self.active = values[0] != 0
        except (ValueError, serial.SerialException) as exc:
            self.get_logger().error(str(exc))
            self.stop()

    def control_values(self, msg):
        return msg.control_type, msg.setpoint, msg.kp, msg.pwm

    def state_message(self, values):
        msg = self.state_message_type()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = self.get_namespace().strip('/') + '/stm'
        for name, value in values.items():
            setattr(msg, name, value)
        return msg

    def stop(self):
        self.active = False
        try:
            self.device.write(encode_control(0, 0.0, 0.0, 0.0))
        except serial.SerialException as exc:
            self.get_logger().error(f'Could not send stop: {exc}')

    def tick(self):
        if self.active and time.monotonic() - self.last_command > self.timeout:
            self.stop()
        try:
            self.buffer.extend(self.device.read(min(self.device.in_waiting, 4096)))
            while b'\n' in self.buffer:
                line, _, rest = self.buffer.partition(b'\n')
                self.buffer = bytearray(rest)
                try:
                    values = parse_state(line)
                    self.publisher.publish(self.state_message(values))
                except (ValueError, UnicodeError) as exc:
                    self.get_logger().warning(f'Discarding serial frame: {exc}')
            if len(self.buffer) > 4096:
                self.buffer.clear()
        except serial.SerialException as exc:
            self.get_logger().error(str(exc))
            self.stop()

    def destroy_node(self):
        self.stop()
        self.device.close()
        return super().destroy_node()


def main(args=None):
    run_node(SerialNode, args)


def run_node(factory, args=None):
    rclpy.init(args=args)
    node = None
    try:
        node = factory()
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if node is not None:
            node.destroy_node()
        rclpy.try_shutdown()
