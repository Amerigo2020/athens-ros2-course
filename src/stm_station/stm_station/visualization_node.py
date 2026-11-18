# Course source: https://github.com/Robolabo/ROS_course
# Upstream revision: cf9e122904ebcb55d336aa7e82d0760bc94cbb07
# Template: Templates/11_stm_visualization.py
# DONE marks code implementation, not a successful ROS/hardware test.
"""D4 TF frames and bounded path from the custom STM state."""
from collections import deque
import math

# Step 1: Import requiered libraries
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


# Step 2: Create the STMVisualizationNode class
# Objective:
# Create a ROS2 node that subscribes to `STMState` messages from an STM module, processes acceleration and encoder data from the motor and IMU
# to compute position and orientation, broadcasts TF transforms for the STM frame, and publishes a Path message for visualization in RViz.
class VisualizationNode(Node):
    def __init__(self):
        super().__init__('stm_visualization_node')
        # DONE (template TODO): Step 2.1 Declare and retrieve parameters
        # 'group_id': Unique identifier for the STM node (default: 1)
        # ADAPTATION: Default group 7; calibration, units and encoder scale are configurable.
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
        # Step 2.3: Initialize state variables
        # Numerical state/integration lives in motion.MotionEstimate.
        self.model = MotionEstimate(**values)
        self.poses = deque(maxlen=max_points)
        # Step 2.5: Initialize the TF broadcaster
        self.broadcaster = TransformBroadcaster(self)
        self.path_publisher = self.create_publisher(Path, 'stm_path', 10)
        self.position_publisher = self.create_publisher(PointStamped, 'stm_position', 10)
        self.velocity_publisher = self.create_publisher(Vector3Stamped, 'stm_velocity', 10)
        # DONE (template TODO): Step 2.2 Define topic name based on group ID for subscribing to STM data
        # DONE (template TODO): Step 2.4 Create a subscriber for the STM data topic
        self.subscription = self.create_subscription(
            STMState, f'/{self.group}/stm_state', self.state_callback, 10)
        self.reset_service = self.create_service(Trigger, 'reset_visualization', self.reset)
        # Step 2.6: Log setup details
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

    # Step 3: Define the callback function for STMState messages
    def state_callback(self, msg):
        stamp = msg.header.stamp
        # Bridge stamps samples. A zero stamp from manual test messages uses ROS time.
        if stamp.sec == 0 and stamp.nanosec == 0:
            stamp = self.get_clock().now().to_msg()
        timestamp = stamp.sec + stamp.nanosec * 1e-9
        try:
            # Step 3.1: Read acceleration and encoder data from the STMState message
            # Steps 3.2-3.5 are completed in motion.py.
            self.model.update((msg.accel_x, msg.accel_y, msg.accel_z),
                              msg.motor_encoder, timestamp)
        except ValueError as exc:
            self.get_logger().warning(f'Discarding motion sample: {exc}')
            return
        # Step 4: Define the function to broadcast TF transforms
        # ADAPTATION: Construct both transforms here instead of a separate broadcast_transform method.
        # Step 4.1: Implement the broadcasting of the TF transform
        body = TransformStamped()
        # DONE (template TODO): Step 4.2 Set the frame details for the transform
        body.header.stamp = stamp
        body.header.frame_id = 'world'
        body.child_frame_id = f'{self.group}/stm_station'
        # DONE (template TODO): Step 4.3 Set the translation (position) values
        body.transform.translation.x, body.transform.translation.y, body.transform.translation.z = self.model.position
        body.transform.rotation.w = 1.0
        motor = TransformStamped()
        motor.header.stamp = stamp
        motor.header.frame_id = body.child_frame_id
        motor.child_frame_id = f'{self.group}/motor'
        # Step 4.4 Set the rotation (orientation) as a quaternion (z-axis rotation)
        # Transform the rotation angle to a quaternion
        # DONE (template TODO): Step 4.5 Set the rotation values in the transform
        # ADAPTATION: z/w give the yaw-only quaternion without tf_transformations;
        # motor yaw is a child of the translating station frame, not IMU attitude.
        motor.transform.rotation.z = math.sin(self.model.yaw / 2.0)
        motor.transform.rotation.w = math.cos(self.model.yaw / 2.0)
        # DONE (template TODO): Step 3.6 Broadcast the TF transform
        # Publish the transform
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


# Step 5: Define the main function
def main(args=None):
    # Step 5.1: Initialize the rclpy library
    rclpy.init(args=args)
    node = None
    try:
        node = VisualizationNode()
        # Step 5.3: Spin the node to keep it running and processing callbacks
        rclpy.spin(node)
    # Gracefully handle shutdown when Ctrl+C is pressed
    except KeyboardInterrupt:
        pass
    finally:
        if node is not None:
            # Step 5.4: Clean up and shut down the node
            node.destroy_node()
        rclpy.try_shutdown()
