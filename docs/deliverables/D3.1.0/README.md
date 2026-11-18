# D3.1.0: Single-station launch

[Assignment index](../README.md) | [Test results](TEST-RESULTS.md) | [Evidence](evidence.md)

## Assignment and source

- Current `Athens2026_ROS2.pptx`: slides 102 (combined D3 assignment).
- Older `Athens_ROS2_Course.pptx`: slides 115 (D3.1.0).
- Original scaffold: [stm_station_launch.py](../../../reference/templates/stm_station_launch.py), upstream revision `cf9e122904ebcb55d336aa7e82d0760bc94cbb07`.
- Status: **Implemented; ROS/hardware verification pending**.

Provide an installed launch file for a single serial node with namespace, port and configuration. Older slides name this stm_serial_node_launch.py; use the custom-interface endpoint for subsequent tasks.

## Team implementation / checkpoint

[src/stm_station/launch/stm_serial_node_launch.py](../../../src/stm_station/launch/stm_serial_node_launch.py)

Runnable stage/configuration preserved in the current tree. These checkpoints were reconstructed for traceability, not presented as previously observed historical progress.

## Execution

[Prepare the Jazzy environment and ports first](../SETUP.md). Each long-running command needs its own prepared terminal. Start recording before the demonstration, and finish it with Ctrl+C. Only one serial stage may access each physical device at a time.

```bash
ros2 launch stm_station stm_serial_node_launch.py --show-args
ros2 launch stm_station stm_serial_node_launch.py group_id:=7 port:=/dev/ttyACM0
# Another prepared terminal:
ros2 node info /group_7/stm_serial_node
ros2 param get /group_7/stm_serial_node baudrate
ros2 topic echo /group_7/stm_state --once
```



## Acceptance and hand-in

1. Installed launch is found and exposes group_id, port and params_file.
2. Exactly one custom serial bridge starts under group_7.
3. YAML baudrate/frequency/timeouts are loaded and port override works.

Record observed results in TEST-RESULTS.md and attach accessible evidence in evidence.md. Implementation, verified operation and actual submission are separate statuses. Follow the lecturers' upload/live-demo requirements.
