# Course source: https://github.com/Robolabo/ROS_course
# Upstream revision: cf9e122904ebcb55d336aa7e82d0760bc94cbb07
# Template: Templates/5_stm_serial_communication_python.py
# Template: Templates/6_stm_serial_node_pub.py
# Template: Templates/7_stm_serial_node_pub_sub.py
# DONE marks code implementation, not a successful ROS/hardware test.
"""Nonblocking serial bridge using the final D1 custom interfaces."""
# 1. Import necessary libraries
import time
import math
import serial
import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import ParameterDescriptor
from stm_interfaces.msg import STMState, STMControl
from .protocol import parse_state, encode_control


# 2. Define the SerialPubSubNode class
# ADAPTATION: Shared transport; standard stages override message conversion.
# Objective:
# The goal is to create a ROS 2 node that reads data from a serial device and publishes it using standard messages like Float32MultiArray.
# Additionally, the node subscribes to Float32MultiArray messages to receive control commands and sends these commands to the serial device.
# ADAPTATION: Final messages are custom STMState/STMControl; standard stages are in standard_serial_node.py.
# Only the serial transport from template 5 is reused; its GUI is not ported.
class SerialNode(Node):
    state_message_type = STMState
    control_message_type = STMControl

    def __init__(self, enable_control=True):
        super().__init__('stm_serial_node')
        # DONE (template TODO): 3. Get Serial Configuration Values
        # ADAPTATION: Startup parameters replace hard-coded port/baudrate values;
        # nonblocking reads poll at 100 Hz by default rather than the template 1000 Hz.
        defaults = {'port': '/dev/ttyACM0', 'baudrate': 115200,
                    'loop_frequency': 100.0, 'command_timeout': 0.5}
        for name, value in defaults.items():
            self.declare_parameter(name, value, ParameterDescriptor(read_only=True))
        frequency = self.get_parameter('loop_frequency').value
        self.timeout = self.get_parameter('command_timeout').value
        if not all(math.isfinite(v) and v > 0 for v in (frequency, self.timeout)):
            raise ValueError('Frequency and timeout must be positive')
        # 4. Set up the serial port for communication
        self.device = serial.Serial(self.get_parameter('port').value,
                                    self.get_parameter('baudrate').value,
                                    timeout=0, write_timeout=0.1)
        self.buffer = bytearray()
        self.last_command = time.monotonic()
        self.active = False
        # DONE (template TODO): 5. Create a publisher to publish the received data from the serial port
        # using Float32MultiArray messages from the std_msgs package in the topic 'stm_state'
        # ADAPTATION: StandardSerialNode uses Float32MultiArray (D1.1/D1.2);
        # this final D1.3 node uses STMState.
        self.publisher = self.create_publisher(self.state_message_type, 'stm_state', 10)
        # DONE (template TODO): 7. Create a subscriber to receive control commands as Float32MultiArray messages
        # on the topic 'stm_control' with a queue size of 10 and a callback function 'stm_control_callback'
        # ADAPTATION: The subscription is omitted for the D1.1 publisher-only stage;
        # D1.2 uses Float32MultiArray; D1.3 uses STMControl.
        if enable_control:
            self.subscription = self.create_subscription(
                self.control_message_type, 'stm_control', self.control, 10)
        # 6. Create a timer to read data periodically and publish it
        self.timer = self.create_timer(1.0 / frequency, self.tick)

    # 8. Define the callback function for the timer
    def control(self, msg):
        try:
            values = self.control_values(msg)
            # DONE (template TODO): Format the control data as a comma-separated string and send it to the serial device
            # ADAPTATION: protocol.encode_control performs the formatting.
            command = encode_control(*values)
            # DONE (template TODO): Encode the control data as UTF-8 and write it to the serial port
            self.device.write(command)
            self.last_command = time.monotonic()
            self.active = values[0] != 0
        except (ValueError, serial.SerialException) as exc:
            self.get_logger().error(str(exc))
            self.stop()

    def control_values(self, msg):
        return msg.control_type, msg.setpoint, msg.kp, msg.pwm

    # D1.3 adaptation of the template standard-message population step.
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

    # 7. Define the callback function for the timer
    def tick(self):
        if self.active and time.monotonic() - self.last_command > self.timeout:
            self.stop()
        try:
            # Check if data is available to read (in_waiting is the number of bytes in the input buffer)
            # Read the data from the serial port
            # ADAPTATION: Buffer nonblocking chunks until newline, instead of readline().
            self.buffer.extend(self.device.read(min(self.device.in_waiting, 4096)))
            while b'\n' in self.buffer:
                line, _, rest = self.buffer.partition(b'\n')
                self.buffer = bytearray(rest)
                try:
                    # Serial template step 7: decode, strip braces and map eight fields in protocol.py.
                    values = parse_state(line)
                    # DONE (template TODO): Publish the float32_multi_array_msg
                    # ADAPTATION: Publish STMState or the overridden standard-message stage.
                    self.publisher.publish(self.state_message(values))
                except (ValueError, UnicodeError) as exc:
                    self.get_logger().warning(f'Discarding serial frame: {exc}')
            if len(self.buffer) > 4096:
                self.buffer.clear()
        except serial.SerialException as exc:
            self.get_logger().error(str(exc))
            self.stop()

    # 9. Define the destroy_node method
    def destroy_node(self):
        self.stop()
        # Clean up the node by closing the serial port.
        self.device.close()
        return super().destroy_node()


def main(args=None):
    run_node(SerialNode, args)


# Serial templates: initialize ROS, spin the node, close the port and shut down.
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
