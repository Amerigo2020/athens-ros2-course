# D2.1: Master/slave control node and service

[Assignment index](../README.md) | [Test results](TEST-RESULTS.md) | [Evidence](evidence.md)

## Assignment and source

- Current `Athens2026_ROS2.pptx`: slides 92-93.
- Older `Athens_ROS2_Course.pptx`: slides 106-107; position diagram 109.
- Original scaffold: [8_stm_control_node_master_slave.py](../../../reference/templates/8_stm_control_node_master_slave.py), upstream revision `cf9e122904ebcb55d336aa7e82d0760bc94cbb07`.
- Status: **Implemented; ROS/hardware verification pending**.

Create STMSetControlType with control_type, kp, kd and success response (D2.1.1); implement the control node with two state subscriptions, one control publisher, service and group parameters (D2.1.2). Use mode 1 for the onboard position setpoint. Stop is mode 0.

## Team implementation / checkpoint

[src/stm_station/stm_station/control_node.py](../../../src/stm_station/stm_station/control_node.py); [src/stm_interfaces/srv/STMSetControlType.srv](../../../src/stm_interfaces/srv/STMSetControlType.srv)

Runnable stage/configuration preserved in the current tree. These checkpoints were reconstructed for traceability, not presented as previously observed historical progress.

## Execution

[Prepare the Jazzy environment and ports first](../SETUP.md). Each long-running command needs its own prepared terminal. Start recording before the demonstration, and finish it with Ctrl+C. Only one serial stage may access each physical device at a time.

```bash
# Start both custom bridges first (see ../SETUP.md); example partner group 2.
ros2 run stm_station stm_control_node --ros-args -p master_group_id:=7 -p slave_group_id:=2
# Other prepared terminals:
ros2 node info /stm_control_node
ros2 interface show stm_interfaces/srv/STMSetControlType
ros2 service call /stm_setcontrol_type stm_interfaces/srv/STMSetControlType "{control_type: 1, kp: 1.0, kd: 0.0}"
ros2 service call /stm_setcontrol_type stm_interfaces/srv/STMSetControlType "{control_type: 0, kp: 0.0, kd: 0.0}"
ros2 service call /stm_setcontrol_type stm_interfaces/srv/STMSetControlType "{control_type: 99, kp: 0.0, kd: 0.0}"
ros2 bag record -o bags/d2_1_run01 /group_7/stm_state /group_2/stm_state /group_2/stm_control
rqt_graph
```

D2 commands here use the standalone root service /stm_setcontrol_type. With the D3 combined launch it is /group_7/stm_setcontrol_type instead. Partner group 2 is an example, not our team ID.

## Acceptance and hand-in

1. Controller has two state subscribers, one slave command publisher and requested service.
2. Mode 1 passes master position and kp to the slave and the slave tracks physically.
3. Mode 0 stops; invalid mode returns success=false and stops.
4. Stopping master feedback disarms within state_timeout; restoring feedback requires a new service request.

Record observed results in TEST-RESULTS.md and attach accessible evidence in evidence.md. Implementation, verified operation and actual submission are separate statuses. Follow the lecturers' upload/live-demo requirements.
