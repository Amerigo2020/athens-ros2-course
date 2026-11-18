"""D4 TF frames and bounded path from the custom STM state."""
from collections import deque
import math

import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import ParameterDescriptor
from geometry_msgs.msg import PointStamped, PoseStamped, TransformStamped, Vector3Stamped
from nav_msgs.msg import Path
from std_srvs.srv import Trigger
from stm_interfaces.msg import STMState
from tf2_ros import TransformBroadcaster

from .launch_settings import group_namespace
from .motion import MotionEstimate


class VisualizationNode(Node):
    def __init__(self):
        super().__init__('stm_visualization_node')
        defaults = dict(group_id=7, calibration_samples=50, acceleration_scale=1.0,
                        deadband=0.5, max_dt=0.2, ticks_per_revolution=24.0,
                        gear_ratio=9.7, encoder_direction=1.0, max_path_points=1000)
        for name, value in defaults.items():
            self.declare_parameter(name, value, ParameterDescriptor(read_only=True))
        values = {name: self.get_parameter(name).value for name in defaults}
        self.group = group_namespace(values.pop('group_id'))
        max_points = values.pop('max_path_points')
        if max_points < 1:
            raise ValueError('max_path_points must be positive')
        self.model = MotionEstimate(**values)
        self.poses = deque(maxlen=max_points)
        self.broadcaster = TransformBroadcaster(self)
        self.path_publisher = self.create_publisher(Path, 'stm_path', 10)
        self.position_publisher = self.create_publisher(PointStamped, 'stm_position', 10)
        self.velocity_publisher = self.create_publisher(Vector3Stamped, 'stm_velocity', 10)
        self.subscription = self.create_subscription(
            STMState, f'/{self.group}/stm_state', self.state_callback, 10)
        self.reset_service = self.create_service(Trigger, 'reset_visualization', self.reset)
        self.get_logger().info(
            f'Keep the station still for {self.model.calibration_samples} samples. '
            f'TF: world -> {self.group}/stm_station -> {self.group}/motor')

    def reset(self, request, response):
        self.model.reset()
        self.poses.clear()
        path = Path()
        path.header.frame_id = 'world'
        path.header.stamp = self.get_clock().now().to_msg()
        self.path_publisher.publish(path)
        response.success = True
        response.message = 'Translation/path cleared; keep station still for recalibration.'
        return response

    def state_callback(self, msg):
        stamp = msg.header.stamp
        # Bridge stamps samples. A zero stamp from manual test messages uses ROS time.
        if stamp.sec == 0 and stamp.nanosec == 0:
            stamp = self.get_clock().now().to_msg()
        timestamp = stamp.sec + stamp.nanosec * 1e-9
        try:
            self.model.update((msg.accel_x, msg.accel_y, msg.accel_z),
                              msg.motor_encoder, timestamp)
        except ValueError as exc:
            self.get_logger().warning(f'Discarding motion sample: {exc}')
            return
        body = TransformStamped()
        body.header.stamp = stamp
        body.header.frame_id = 'world'
        body.child_frame_id = f'{self.group}/stm_station'
        body.transform.translation.x, body.transform.translation.y, body.transform.translation.z = self.model.position
        body.transform.rotation.w = 1.0
        motor = TransformStamped()
        motor.header.stamp = stamp
        motor.header.frame_id = body.child_frame_id
        motor.child_frame_id = f'{self.group}/motor'
        motor.transform.rotation.z = math.sin(self.model.yaw / 2.0)
        motor.transform.rotation.w = math.cos(self.model.yaw / 2.0)
        self.broadcaster.sendTransform([body, motor])

        position = PointStamped()
        position.header = body.header
        position.point.x, position.point.y, position.point.z = self.model.position
        self.position_publisher.publish(position)
        velocity = Vector3Stamped()
        velocity.header = body.header
        velocity.vector.x, velocity.vector.y, velocity.vector.z = self.model.velocity
        self.velocity_publisher.publish(velocity)

        pose = PoseStamped()
        pose.header = body.header
        pose.pose.position.x, pose.pose.position.y, pose.pose.position.z = self.model.position
        pose.pose.orientation.w = 1.0
        self.poses.append(pose)
        path = Path()
        path.header = body.header
        path.poses = list(self.poses)
        self.path_publisher.publish(path)


def main(args=None):
    rclpy.init(args=args)
    node = None
    try:
        node = VisualizationNode()
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if node is not None:
            node.destroy_node()
        rclpy.try_shutdown()
