"""D2 master/slave control: onboard position or host P/PD via PWM."""
import math
import time
import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import ParameterDescriptor
from stm_interfaces.msg import STMState, STMControl
from stm_interfaces.srv import STMSetControlType
from .protocol import feedback_pwm


class ControlNode(Node):
    def __init__(self):
        super().__init__('stm_control_node')
        for name, value in {'master_group_id': 7, 'slave_group_id': 2,
                            'state_timeout': 0.5, 'pwm_limit': 250.0}.items():
            self.declare_parameter(name, value, ParameterDescriptor(read_only=True))
        master = self.get_parameter('master_group_id').value
        slave = self.get_parameter('slave_group_id').value
        self.timeout = self.get_parameter('state_timeout').value
        self.limit = self.get_parameter('pwm_limit').value
        if master <= 0 or slave <= 0 or master == slave or not 0 < self.limit <= 250 or not math.isfinite(self.timeout) or self.timeout <= 0:
            raise ValueError('Use distinct positive group IDs, positive timeout and PWM limit <= 250')
        self.states = {}
        self.mode = 0
        self.kp = self.kd = 0.0
        self.publisher = self.create_publisher(STMControl, f'/group_{slave}/stm_control', 10)
        self.master_sub = self.create_subscription(STMState, f'/group_{master}/stm_state',
                                                    lambda msg: self.state('master', msg), 10)
        self.slave_sub = self.create_subscription(STMState, f'/group_{slave}/stm_state',
                                                   lambda msg: self.state('slave', msg), 10)
        self.service = self.create_service(STMSetControlType, 'stm_setcontrol_type', self.configure)
        self.timer = self.create_timer(1.0 / 50.0, self.tick)

    def state(self, key, msg):
        values = (msg.motor_encoder, msg.motor_velocity)
        if all(math.isfinite(v) for v in values):
            self.states[key] = (values, time.monotonic())
        else:
            self.states.pop(key, None)

    def configure(self, request, response):
        valid = request.control_type in (0, 1, 2) and all(
            math.isfinite(v) and 0 <= v <= 1e6 for v in (request.kp, request.kd))
        self.mode = request.control_type if valid else 0
        self.kp, self.kd = (request.kp, request.kd) if valid else (0.0, 0.0)
        response.success = valid
        self.tick()
        return response

    def tick(self):
        msg = STMControl()
        msg.header.stamp = self.get_clock().now().to_msg()
        fresh = all(key in self.states and time.monotonic() - self.states[key][1] <= self.timeout
                    for key in ('master', 'slave'))
        if self.mode and not fresh:
            self.mode = 0  # Require explicit rearming after lost state.
        if self.mode == 1:
            msg.control_type = 1
            msg.setpoint = self.states['master'][0][0]
            msg.kp = self.kp
        elif self.mode == 2:
            msg.control_type = 2
            msg.pwm = feedback_pwm(self.states['master'][0], self.states['slave'][0],
                                   self.kp, self.kd, self.limit)
        self.publisher.publish(msg)

    def destroy_node(self):
        self.mode = 0
        self.tick()
        return super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = None
    try:
        node = ControlNode()
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if node is not None:
            node.destroy_node()
        rclpy.try_shutdown()
