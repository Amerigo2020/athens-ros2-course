# Course source: https://github.com/Robolabo/ROS_course
# Upstream revision: cf9e122904ebcb55d336aa7e82d0760bc94cbb07
# Template: Templates/8_stm_control_node_master_slave.py
# Template: Templates/9_stm_control_node_master_slave_poscontrol.py
# Template: Templates/10_stm_control_node_master_slave_impedance_control.py
# DONE marks code implementation, not a successful ROS/hardware test.
"""D2 master/slave control: onboard position or host P/PD via PWM."""
import math
import time
import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import ParameterDescriptor
# DONE (template TODO): Import the custom message types STMState and STMControl
from stm_interfaces.msg import STMState, STMControl
# DONE (template TODO): Import the custom service type STMSetControlType
from stm_interfaces.srv import STMSetControlType
from .protocol import feedback_pwm


# 2. Define the STMControlNode class
# Objective:
# The goal of this exercise is to create a ROS2 node named 'STMControlNode' that controls the slave STM motor using Stop, Master-Slave Position Control and Close loop Impedance Control.
# Templates 8 and 9 supply the Stop/onboard-position and host P stages;
# template 10 adds the position and velocity error feedback.
class ControlNode(Node):
    def __init__(self):
        # Initialize the ROS 2 node with a unique name 'stm_control_node'
        super().__init__('stm_control_node')
        # DONE (template TODO): 3. Declare parameters 'master_group_id' and 'slave_group_id as set default values
        # 'master_group_id': ID for the master STM data topic, set the default value to 1
        # 'slave_group_id': ID for the slave control command topic, set the default value to 2
        # ADAPTATION: Our master defaults to Group 7; Group 2 is a partner example.
        # TODO (templates 8/9/10, step 17): Implement the parameter callback to handle dynamic changes in group IDs.
        # TODO (template TODO): Update master_group_id and master_state_topic.
        # TODO (template TODO): If the subscriber already exists, destroy it and create a new one with the updated topic.
        # TODO (template TODO): Update slave_group_id and slave_control_topic.
        # TODO (template TODO): If the publisher already exists, destroy it and create a new one with the updated topic.
        # ADAPTATION: Parameters are currently read-only; restart to change routing.
        for name, value in {'master_group_id': 7, 'slave_group_id': 2,
                            'state_timeout': 0.5, 'pwm_limit': 250.0}.items():
            self.declare_parameter(name, value, ParameterDescriptor(read_only=True))
        # DONE (template TODO): 4. Retrieve parameter values from the node's configuration and assign them to instance
        # variables
        master = self.get_parameter('master_group_id').value
        slave = self.get_parameter('slave_group_id').value
        self.timeout = self.get_parameter('state_timeout').value
        self.limit = self.get_parameter('pwm_limit').value
        if master <= 0 or slave <= 0 or master == slave or not 0 < self.limit <= 250 or not math.isfinite(self.timeout) or self.timeout <= 0:
            raise ValueError('Use distinct positive group IDs, positive timeout and PWM limit <= 250')
        # 11. Initialize variables for storing master position
        # ADAPTATION: Store both position and velocity with receive time per group.
        self.states = {}
        # 12. Initialize control type to 'Stop' (0), allowing dynamic changes via a service
        self.mode = 0
        # 13. Initialize control gains kp and kv to default value
        # ADAPTATION: kd consistently names the derivative gain (template mixes kd/kv).
        self.kp = self.kd = 0.0
        # DONE (template TODO): 5. Define topic names for master and slave based on group IDs obtained from parameters
        # DONE (template TODO): 7. Create publishers for STM control (slave)
        # Group-specific topic names are constructed inline from the startup IDs.
        self.publisher = self.create_publisher(STMControl, f'/group_{slave}/stm_control', 10)
        # DONE (template TODO): 6. Create subscribers for STM state (master and slave)
        self.master_sub = self.create_subscription(STMState, f'/group_{master}/stm_state',
                                                    lambda msg: self.state('master', msg), 10)
        self.slave_sub = self.create_subscription(STMState, f'/group_{slave}/stm_state',
                                                   lambda msg: self.state('slave', msg), 10)
        # 8. Define the service name ('set_control_type')
        # DONE (template TODO): 9. Create a service of type 'STMSetControlType' to allow dynamic change of the control settings of the node:
        # Request:  Control types ->  0 = Stop  |  1 = Position Control
        # Request:  Control gains -> kp = Proportional gain, kd = Derivative gain
        # Response: Success status
        # ADAPTATION: stm_setcontrol_type matches the slides, instead of set_control_type.
        self.service = self.create_service(STMSetControlType, 'stm_setcontrol_type', self.configure)
        # DONE (template TODO): 10. Create a timer for the publisher and to control the STM.
        # !!! set the loop at 50Hz !!! (set the period to: 1 / self.loop_frequency) !!
        self.timer = self.create_timer(1.0 / 50.0, self.tick)

    # DONE (template TODO): 14. Implement callback functions
    # DONE (template TODO): 15. Implement callback functions
    # DONE (template TODO): Update master_position with value from msg
    # ADAPTATION: One keyed callback handles master and slave position/velocity;
    # the original slave callback incorrectly repeats the master_position comment.
    def state(self, key, msg):
        values = (msg.motor_encoder, msg.motor_velocity)
        if all(math.isfinite(v) for v in values):
            self.states[key] = (values, time.monotonic())
        else:
            self.states.pop(key, None)

    # DONE (template TODO): 15. Implement the service callback (template 8).
    # DONE (template TODO): 16. Implement the service callback
    def configure(self, request, response):
        # DONE (template TODO): Update control_type based on the service request values
        # If an invalid control type is requested, default to Stop (0)
        # DONE (template TODO): Update control kp gain based on the received requested message,
        # DONE (template TODO): Update control kv gain based on the received requested message,
        # ensure the value is non-negative
        # ADAPTATION: request.kd replaces the template request.kv spelling.
        valid = request.control_type in (0, 1, 2) and all(
            math.isfinite(v) and 0 <= v <= 1e6 for v in (request.kp, request.kd))
        self.mode = request.control_type if valid else 0
        self.kp, self.kd = (request.kp, request.kd) if valid else (0.0, 0.0)
        # Confirm the service request was handled successfully
        # ADAPTATION: Invalid mode/gains return false, rather than unconditional success.
        # TODO (template comments): Log the updated control type and gains.
        response.success = valid
        self.tick()
        return response

    # DONE (template TODO): 16. Implement control logic in timer_control_loop callback (template 8).
    # DONE (template TODO): 18. Implement control logic in timer_control_loop callback
    def tick(self):
        # DONE (template TODO): Initialize a STMControl message that will be published to the slave node
        # Do things if control type is 0 (Stop), 1 (Position Control) or 2 (Close loop PWM Control)
        # DONE (template TODO): Default to stop mode
        # Default message fields are zero; stale feedback also selects Stop.
        msg = STMControl()
        msg.header.stamp = self.get_clock().now().to_msg()
        fresh = all(key in self.states and time.monotonic() - self.states[key][1] <= self.timeout
                    for key in ('master', 'slave'))
        if self.mode and not fresh:
            self.mode = 0  # Require explicit rearming after lost state.
        # DONE (template TODO): Fill in the control message based on the control type and control constant received from the service request
        # and the slave setpoint position based on the master position received from the subscriber
        if self.mode == 1:
            msg.control_type = 1
            msg.setpoint = self.states['master'][0][0]
            msg.kp = self.kp
        # DONE (template TODO): Close loop for position control using PWM
        # DONE (template TODO): Update the PWM control command in the STMControl message
        # Error calculation and saturation are in protocol.feedback_pwm (templates 9/10).
        elif self.mode == 2:
            msg.control_type = 2
            msg.pwm = feedback_pwm(self.states['master'][0], self.states['slave'][0],
                                   self.kp, self.kd, self.limit)
        # DONE (template TODO): Publish the constructed control command
        # DONE (template TODO): Publish the control message (template 8).
        # TODO (template comment): Log the published command for debugging and monitoring.
        self.publisher.publish(msg)

    def destroy_node(self):
        self.mode = 0
        self.tick()
        return super().destroy_node()


# Define the main function to run the node
def main(args=None):
    # Initialize the ROS2 Python client library
    rclpy.init(args=args)
    node = None
    try:
        node = ControlNode()
        # Run the node until interrupted
        rclpy.spin(node)
    # Gracefully handle shutdown when Ctrl+C is pressed
    except KeyboardInterrupt:
        pass
    finally:
        if node is not None:
            # Destroy the node and shutdown the ROS2 Python client library
            node.destroy_node()
        rclpy.try_shutdown()
