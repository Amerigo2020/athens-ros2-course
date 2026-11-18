# D1.3: Custom STM interfaces

[Assignment index](../README.md) | [Test results](TEST-RESULTS.md) | [Evidence](evidence.md)

## Assignment and source

- Current `Athens2026_ROS2.pptx`: slides 80-81.
- Older `Athens_ROS2_Course.pptx`: slides 86-87.
- Original scaffold: [7_stm_serial_node_pub_sub.py](../../../reference/templates/7_stm_serial_node_pub_sub.py), upstream revision `cf9e122904ebcb55d336aa7e82d0760bc94cbb07`.
- Status: **Implemented; ROS/hardware verification pending**.

Create stm_interfaces with STMState.msg and STMControl.msg (D1.3.1); configure generation with std_msgs/Header dependency; replace both standard-array topics with the custom messages (D1.3.2). The final serial node is this checkpoint.

## Team implementation / checkpoint

[src/stm_interfaces](../../../src/stm_interfaces); [src/stm_station/stm_station/serial_node.py](../../../src/stm_station/stm_station/serial_node.py)

Runnable stage/configuration preserved in the current tree. These checkpoints were reconstructed for traceability, not presented as previously observed historical progress.

## Execution

[Prepare the Jazzy environment and ports first](../SETUP.md). Each long-running command needs its own prepared terminal. Start recording before the demonstration, and finish it with Ctrl+C. Only one serial stage may access each physical device at a time.

```bash
ros2 interface show stm_interfaces/msg/STMState
ros2 interface show stm_interfaces/msg/STMControl
ros2 run stm_station stm_serial_node --ros-args -r __ns:=/group_7 -p port:=/dev/ttyACM0
# Separate prepared terminals:
ros2 topic echo /group_7/stm_state --once
ros2 topic pub --rate 10 /group_7/stm_control stm_interfaces/msg/STMControl "{control_type: 0}"
ros2 bag record -o bags/d1_3_run01 /group_7/stm_state /group_7/stm_control
rqt_graph
```



## Acceptance and hand-in

1. Both interfaces build and show expected fields, including Header.
2. STMState has plausible named values and advancing timestamps.
3. STMControl produces the expected serial command/motor response; test mode 2 with a small PWM as in D1.2.
4. Graph and bag use custom interfaces and no standard-message stage is running.

Record observed results in TEST-RESULTS.md and attach accessible evidence in evidence.md. Implementation, verified operation and actual submission are separate statuses. Follow the lecturers' upload/live-demo requirements.
