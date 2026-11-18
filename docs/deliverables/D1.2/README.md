# D1.2: STM publisher/subscriber with standard messages

[Assignment index](../README.md) | [Test results](TEST-RESULTS.md) | [Evidence](evidence.md)

## Assignment and source

- Current `Athens2026_ROS2.pptx`: slides 79.
- Older `Athens_ROS2_Course.pptx`: slides 85.
- Original scaffold: [7_stm_serial_node_pub_sub.py](../../../reference/templates/7_stm_serial_node_pub_sub.py), upstream revision `cf9e122904ebcb55d336aa7e82d0760bc94cbb07`.
- Status: **Implemented; ROS/hardware verification pending**.

Extend the serial publisher with the command subscriber (D1.2.1). Verify reading and writing serial data concurrently; inspect, command and record the station (D1.2.2). State array order: encoder, velocity, accel_x/y/z, gyro_x/y/z. Command order: control_type, setpoint, kp, pwm.

## Team implementation / checkpoint

[src/stm_station/stm_station/standard_serial_node.py](../../../src/stm_station/stm_station/standard_serial_node.py); pubsub_main

Runnable stage/configuration preserved in the current tree. These checkpoints were reconstructed for traceability, not presented as previously observed historical progress.

## Execution

[Prepare the Jazzy environment and ports first](../SETUP.md). Each long-running command needs its own prepared terminal. Start recording before the demonstration, and finish it with Ctrl+C. Only one serial stage may access each physical device at a time.

```bash
ros2 run stm_station stm_serial_node_pub_sub --ros-args -r __ns:=/group_7 -p port:=/dev/ttyACM0
# Separate terminals, after checking the firmware PWM range/direction:
ros2 topic echo /group_7/stm_state --once
ros2 topic pub --rate 10 /group_7/stm_control std_msgs/msg/Float32MultiArray "{data: [0.0, 0.0, 0.0, 0.0]}"
# Stop that publisher before this small PWM example:
ros2 topic pub --rate 10 /group_7/stm_control std_msgs/msg/Float32MultiArray "{data: [2.0, 0.0, 0.0, 10.0]}"
# Ctrl+C stops publishing: observe command timeout stop (~0.5 s).
ros2 bag record -o bags/d1_2_run01 /group_7/stm_state /group_7/stm_control
rqt_graph
```



## Acceptance and hand-in

1. Both state and command topics use std_msgs/msg/Float32MultiArray.
2. A valid four-element command reaches the STM while states continue.
3. Short arrays and fractional/invalid modes are rejected and trigger stop.
4. After command publisher stops the motor stops; record measured behavior and graph.

Record observed results in TEST-RESULTS.md and attach accessible evidence in evidence.md. Implementation, verified operation and actual submission are separate statuses. Follow the lecturers' upload/live-demo requirements.
