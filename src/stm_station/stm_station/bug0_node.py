# Course source: https://github.com/Robolabo/ROS_course
# Upstream revision: cf9e122904ebcb55d336aa7e82d0760bc94cbb07
# Template: Templates/13_bug0_lidar_stm.py
# DONE marks code implementation, not a successful ROS/hardware test.
"""D5.1 scan-to-TwistStamped controller; movement requires explicit enable."""
# Step 1: Import required libraries
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


# Step 2: Create the Bug0LidarSTMNode class
# Objective:
# Create a ROS 2 node that subscribes to the LiDAR `/scan` topic, splits the ranges vector
# into three regions (right, front, and left), stores the measured distances at the LiDAR
# acquisition speed, and publishes fixed commands at 10 Hz both to the simulation and to the
# STM station to implement a simple Bug0-style obstacle avoidance node.
class Bug0Node(Node):
    def __init__(self):
        super().__init__('bug0_lidar_stm_node')
        # Step 2.1: Fixed values for the exercise
        # ADAPTATION: The template fixed values become startup parameters.
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
        # Step 2.5: Initialize the variables that store the latest minimum distance of each sector
        # ADAPTATION: ScanWatchdog stores valid sectors and requires explicit enable.
        self.watchdog = ScanWatchdog(values['scan_timeout'])
        self.min_valid_fraction = values['min_valid_fraction']
        self.forward_pwm, self.turn_pwm = values['forward_pwm'], values['turn_pwm']
        if (not 0 < self.min_valid_fraction <= 1
                or not all(math.isfinite(v) and 0 <= v <= 250 for v in (self.forward_pwm, self.turn_pwm))):
            raise ValueError('Invalid scan coverage or STM PWM limits')
        self.last_state = None
        # DONE (template TODO): Step 2.3 Create a publisher for the simulated robot velocity command
        # In Jazzy, the diff drive controller expects TwistStamped on this topic.
        self.velocity_publisher = self.create_publisher(TwistStamped, values['cmd_vel_topic'], 10)
        # DONE (template TODO): Step 2.4 Create a publisher for the STM control topic `/stm_control`
        # ADAPTATION: Use /group_7/stm_control and enable_stm=true; disabled by default.
        self.stm_publisher = (self.create_publisher(STMControl, f'/{group}/stm_control', 10)
                              if values['enable_stm'] else None)
        self.state_publisher = self.create_publisher(String, 'bug0_state', 10)
        # DONE (template TODO): Step 2.2 Create a subscriber for the LiDAR topic `/scan`
        self.subscription = self.create_subscription(
            LaserScan, values['scan_topic'], self.scan_callback, qos_profile_sensor_data)
        self.service = self.create_service(SetBool, 'bug0_enable', self.enable_callback)
        self.steady_clock = Clock(clock_type=ClockType.STEADY_TIME)
        # DONE (template TODO): Step 2.6 Create a timer to publish the commands at 10 Hz
        # Hint: 10 Hz means a period of 0.1 seconds
        # ADAPTATION: A steady-clock timer also detects stale scans while /clock is paused.
        self.timer = self.create_timer(0.1, self.tick, clock=self.steady_clock)
        # Step 2.7: Log setup details
        self.get_logger().info('Bug0 starts disabled. Check scan/cmd_vel interfaces, then call bug0_enable.')

    def ros_time(self):
        return self.get_clock().now().nanoseconds * 1e-9

    # Step 4: Define the callback function for the LiDAR messages
    def scan_callback(self, msg):
        was_armed = self.watchdog.armed
        try:
            # Template steps 4.1-4.3 are implemented in bug0.scan_sectors.
            sectors = scan_sectors(msg.ranges, msg.angle_min, msg.angle_increment,
                                   msg.range_min, msg.range_max, self.min_valid_fraction)
            stamp = msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9
            # DONE (template TODO): Step 4.4 Store the minimum distances in the node variables
            # ADAPTATION: A rejected scan latches disarm, even if a valid scan arrives before the timer.
            self.watchdog.accept(sectors, stamp, self.ros_time(), time.monotonic())
            # DONE (template TODO): Step 5.7 Print the three minimum distances for debugging
            # ADAPTATION: Log the minima at DEBUG level in the scan callback.
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

    # Step 5: Define the timer callback that publishes the commands at 10 Hz
    def tick(self):
        was_armed = self.watchdog.armed
        # Step 5.1: Wait until at least one LiDAR message has been received
        # ADAPTATION: Send zero when disabled/stale; do not keep the last movement command.
        sectors = self.watchdog.current(time.monotonic(), self.ros_time())
        if was_armed and not self.watchdog.armed:
            self.stop_for_scan_loss()
        command = self.policy.command(sectors) if self.watchdog.armed else Drive()
        self.publish_command(command, command.state if self.watchdog.armed else 'disabled')

    def publish_command(self, command, state):
        # Step 5.3: Add a timestamp to both messages
        stamp = self.get_clock().now().to_msg()
        # Step 5.2: Create the output messages
        velocity = TwistStamped()
        velocity.header.stamp = stamp
        velocity.header.frame_id = 'base_footprint'
        velocity.twist.linear.x = command.linear
        velocity.twist.angular.z = command.angular
        # DONE (template TODO): Step 5.6 Publish both commands
        self.velocity_publisher.publish(velocity)
        if self.stm_publisher is not None:
            # Step 5.4: Configure the STM command fields that stay constant
            # ADAPTATION: Stop uses mode 0; active movement uses mode 2 with zero setpoint/kp.
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


# Step 6: Define the main function
def main(args=None):
    # Step 6.1: Initialize ROS 2
    rclpy.init(args=args)
    node = None
    try:
        node = Bug0Node()
        # Step 6.3: Keep the node running
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        if node is not None:
            # Step 6.4: Clean up and shutdown
            node.destroy_node()
        rclpy.try_shutdown()
