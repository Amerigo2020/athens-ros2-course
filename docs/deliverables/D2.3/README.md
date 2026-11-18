# D2.3: Host impedance PD control (starred extension)

[Assignment index](../README.md) | [Test results](TEST-RESULTS.md) | [Evidence](evidence.md)

## Assignment and source

- Current `Athens2026_ROS2.pptx`: slides 96-97.
- Older `Athens_ROS2_Course.pptx`: slides 110-111 (D2.1.5 extra points).
- Original scaffold: [10_stm_control_node_master_slave_impedance_control.py](../../../reference/templates/10_stm_control_node_master_slave_impedance_control.py), upstream revision `cf9e122904ebcb55d336aa7e82d0760bc94cbb07`.
- Status: **Implemented; ROS/hardware verification pending**.

Extend the position loop with measured velocity error: PWM = kp * position_error + kd * velocity_error. Use kd consistently even though the original template also refers to kv. Compare behavior to D2.2 at recorded gains.

## Team implementation / checkpoint

[src/stm_station/stm_station/control_node.py](../../../src/stm_station/stm_station/control_node.py) mode 2 with kd>0; protocol.feedback_pwm

Runnable stage/configuration preserved in the current tree. These checkpoints were reconstructed for traceability, not presented as previously observed historical progress.

## Execution

[Prepare the Jazzy environment and ports first](../SETUP.md). Each long-running command needs its own prepared terminal. Start recording before the demonstration, and finish it with Ctrl+C. Only one serial stage may access each physical device at a time.

```bash
# Both custom bridges must already be running.
ros2 run stm_station stm_control_node --ros-args -p master_group_id:=7 -p slave_group_id:=2 -p pwm_limit:=25.0
# Separate terminals, example gains to tune:
ros2 service call /stm_setcontrol_type stm_interfaces/srv/STMSetControlType "{control_type: 2, kp: 1.0, kd: 0.1}"
ros2 bag record -o bags/d2_3_run01 /group_7/stm_state /group_2/stm_state /group_2/stm_control
ros2 service call /stm_setcontrol_type stm_interfaces/srv/STMSetControlType "{control_type: 0, kp: 0.0, kd: 0.0}"
```

D2 commands here use the standalone root service /stm_setcontrol_type. With the D3 combined launch it is /group_7/stm_setcontrol_type instead. Partner group 2 is an example, not our team ID.

## Acceptance and hand-in

1. Both position and velocity errors contribute with the documented sign.
2. Output remains inside pwm_limit and stop/feedback-loss behavior works.
3. Compare P vs PD traces and document kp/kd, units and observed damping.

Record observed results in TEST-RESULTS.md and attach accessible evidence in evidence.md. Implementation, verified operation and actual submission are separate statuses. Follow the lecturers' upload/live-demo requirements.
