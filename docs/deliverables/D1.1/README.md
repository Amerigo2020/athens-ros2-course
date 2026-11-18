# D1.1: STM state publisher with standard messages

[Assignment index](../README.md) | [Test results](TEST-RESULTS.md) | [Evidence](evidence.md)

## Assignment and source

- Current `Athens2026_ROS2.pptx`: slides 78 (D1 overview: 77).
- Older `Athens_ROS2_Course.pptx`: slides 84 (overview: 83).
- Original scaffold: [6_stm_serial_node_pub.py](../../../reference/templates/6_stm_serial_node_pub.py), upstream revision `cf9e122904ebcb55d336aa7e82d0760bc94cbb07`.
- Status: **Implemented; ROS/hardware verification pending**.

Create stm_station (D1.1.1); complete the publisher template (D1.1.2); configure and build (D1.1.3); inspect and record state (D1.1.4). This reconstructed checkpoint deliberately publishes Float32MultiArray and has no command subscription.

## Team implementation / checkpoint

[src/stm_station/stm_station/standard_serial_node.py](../../../src/stm_station/stm_station/standard_serial_node.py); publisher_main; shared serial_node.py

Runnable stage/configuration preserved in the current tree. These checkpoints were reconstructed for traceability, not presented as previously observed historical progress.

## Execution

[Prepare the Jazzy environment and ports first](../SETUP.md). Each long-running command needs its own prepared terminal. Start recording before the demonstration, and finish it with Ctrl+C. Only one serial stage may access each physical device at a time.

```bash
ros2 run stm_station stm_serial_node_pub --ros-args -r __ns:=/group_7 -p port:=/dev/ttyACM0
# In another prepared terminal:
ros2 topic type /group_7/stm_state
ros2 topic echo /group_7/stm_state --once
ros2 topic hz /group_7/stm_state
ros2 node info /group_7/stm_serial_node
ros2 bag record -o bags/d1_1_run01 /group_7/stm_state
rqt_graph
```



## Acceptance and hand-in

1. Topic type is std_msgs/msg/Float32MultiArray; data contains eight fields in course order.
2. Encoder and IMU readings respond plausibly to movement; measure actual frequency.
3. No stm_control subscription exists in this publisher-only stage.
4. Bag is readable and graph shows publisher/topic; include outputs/screenshots.

Record observed results in TEST-RESULTS.md and attach accessible evidence in evidence.md. Implementation, verified operation and actual submission are separate statuses. Follow the lecturers' upload/live-demo requirements.
