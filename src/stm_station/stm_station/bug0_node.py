"""D5.1 scan-to-TwistStamped controller; movement requires explicit enable."""
import math
import time

import rclpy
from rclpy.clock import Clock, ClockType
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from rcl_interfaces.msg import ParameterDescriptor
from geometry_msgs.msg import TwistStamped
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String
from std_srvs.srv import SetBool
from stm_interfaces.msg import STMControl

from .bug0 import Bug0Policy, Drive, ScanWatchdog, scan_sectors
from .launch_settings import group_namespace


class Bug0Node(Node):
    def __init__(self):
        super().__init__('bug0_lidar_stm_node')
        defaults = dict(group_id=7, scan_topic='/scan',
                        cmd_vel_topic='/diff_drive_controller/cmd_vel',
                        obstacle_distance=1.0, release_distance=1.2,
                        linear_speed=0.3, angular_speed=0.5, turn_clearance=0.4,
                        scan_timeout=0.5, min_valid_fraction=0.5,
                        enable_stm=False, forward_pwm=90.0, turn_pwm=70.0)
        for name, value in defaults.items():
            self.declare_parameter(name, value, ParameterDescriptor(read_only=True))
        values = {name: self.get_parameter(name).value for name in defaults}
        group = group_namespace(values['group_id'])
        self.policy = Bug0Policy(**{key: values[key] for key in (
            'obstacle_distance', 'release_distance', 'linear_speed', 'angular_speed', 'turn_clearance')})
        self.watchdog = ScanWatchdog(values['scan_timeout'])
        self.min_valid_fraction = values['min_valid_fraction']
        self.forward_pwm, self.turn_pwm = values['forward_pwm'], values['turn_pwm']
        if (not 0 < self.min_valid_fraction <= 1
                or not all(math.isfinite(v) and 0 <= v <= 250 for v in (self.forward_pwm, self.turn_pwm))):
            raise ValueError('Invalid scan coverage or STM PWM limits')
        self.last_state = None
        self.velocity_publisher = self.create_publisher(TwistStamped, values['cmd_vel_topic'], 10)
        self.stm_publisher = (self.create_publisher(STMControl, f'/{group}/stm_control', 10)
                              if values['enable_stm'] else None)
        self.state_publisher = self.create_publisher(String, 'bug0_state', 10)
        self.subscription = self.create_subscription(
            LaserScan, values['scan_topic'], self.scan_callback, qos_profile_sensor_data)
        self.service = self.create_service(SetBool, 'bug0_enable', self.enable_callback)
        self.steady_clock = Clock(clock_type=ClockType.STEADY_TIME)
        self.timer = self.create_timer(0.1, self.tick, clock=self.steady_clock)
        self.get_logger().info('Bug0 starts disabled. Check scan/cmd_vel interfaces, then call bug0_enable.')

    def ros_time(self):
        return self.get_clock().now().nanoseconds * 1e-9

    def scan_callback(self, msg):
        was_armed = self.watchdog.armed
        try:
            sectors = scan_sectors(msg.ranges, msg.angle_min, msg.angle_increment,
                                   msg.range_min, msg.range_max, self.min_valid_fraction)
            stamp = msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9
            self.watchdog.accept(sectors, stamp, self.ros_time(), time.monotonic())
            self.get_logger().debug(
                f'Scan minima right={sectors.right}, front={sectors.front}, left={sectors.left}')
        except ValueError as exc:
            self.watchdog.invalidate()
            self.get_logger().warning(f'Discarding scan: {exc}')
        if was_armed and not self.watchdog.armed:
            self.stop_for_scan_loss()

    def stop_for_scan_loss(self):
        self.policy.reset()
        self.publish_command(Drive(), 'disabled')
        self.get_logger().warning('Scan missing/stale/invalid: stopped; explicit re-enable required.')

    def enable_callback(self, request, response):
        response.success = self.watchdog.arm(request.data, time.monotonic(), self.ros_time())
        self.policy.reset()
        self.publish_command(Drive(), 'enabled' if self.watchdog.armed else 'disabled')
        response.message = ('Enabled; keep scans running.' if self.watchdog.armed else
                            'Disabled.' if not request.data else 'No fresh complete scan; enable rejected.')
        return response

    def tick(self):
        was_armed = self.watchdog.armed
        sectors = self.watchdog.current(time.monotonic(), self.ros_time())
        if was_armed and not self.watchdog.armed:
            self.stop_for_scan_loss()
        command = self.policy.command(sectors) if self.watchdog.armed else Drive()
        self.publish_command(command, command.state if self.watchdog.armed else 'disabled')

    def publish_command(self, command, state):
        stamp = self.get_clock().now().to_msg()
        velocity = TwistStamped()
        velocity.header.stamp = stamp
        velocity.header.frame_id = 'base_footprint'
        velocity.twist.linear.x = command.linear
        velocity.twist.angular.z = command.angular
        self.velocity_publisher.publish(velocity)
        if self.stm_publisher is not None:
            control = STMControl()
            control.header.stamp = stamp
            if command.state != 'stop':
                control.control_type = 2
                control.pwm = (self.forward_pwm if command.state == 'forward' else
                               self.turn_pwm if command.state == 'left' else -self.turn_pwm)
            self.stm_publisher.publish(control)
        self.state_publisher.publish(String(data=state))
        if state != self.last_state:
            self.get_logger().info(f'Bug0 state: {state}')
            self.last_state = state

    def destroy_node(self):
        if self.context.ok():
            self.publish_command(Drive(), 'disabled')
        return super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = None
    try:
        node = Bug0Node()
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        if node is not None:
            node.destroy_node()
        rclpy.try_shutdown()
