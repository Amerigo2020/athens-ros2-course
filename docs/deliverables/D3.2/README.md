# D3.2: Combined serial/control launch

[Assignment index](../README.md) | [Test results](TEST-RESULTS.md) | [Evidence](evidence.md)

## Assignment and source

- Current `Athens2026_ROS2.pptx`: slides 102 (D3.1 in current slides).
- Older `Athens_ROS2_Course.pptx`: slides 117 (D3.2).
- Original scaffold: [stm_station_launch.py](../../../reference/templates/stm_station_launch.py), upstream revision `cf9e122904ebcb55d336aa7e82d0760bc94cbb07`.
- Status: **Implemented; ROS/hardware verification pending**.

Start serial bridge and control node together, with explicit master/slave groups and YAML parameters. Optional start_slave=true starts both bridges on one machine. With false the partner must run its bridge elsewhere. Do not start duplicate bridges on either device.

## Team implementation / checkpoint

[src/stm_station/launch/stm_serial_control_launch.py](../../../src/stm_station/launch/stm_serial_control_launch.py)

Runnable stage/configuration preserved in the current tree. These checkpoints were reconstructed for traceability, not presented as previously observed historical progress.

## Execution

[Prepare the Jazzy environment and ports first](../SETUP.md). Each long-running command needs its own prepared terminal. Start recording before the demonstration, and finish it with Ctrl+C. Only one serial stage may access each physical device at a time.

```bash
# Group 2 is an example only. Choose the actual partner group.
ros2 launch stm_station stm_serial_control_launch.py --show-args
ros2 launch stm_station stm_serial_control_launch.py master_group_id:=7 slave_group_id:=2 master_port:=/dev/ttyACM0 start_slave:=true slave_port:=/dev/ttyACM1
# Another prepared terminal: service is namespaced with the master.
ros2 node list
ros2 param get /group_7/stm_control_node pwm_limit
ros2 service call /group_7/stm_setcontrol_type stm_interfaces/srv/STMSetControlType "{control_type: 0, kp: 0.0, kd: 0.0}"
rqt_graph
```



## Acceptance and hand-in

1. Combined launch starts expected nodes with correct group routing; starts in stop.
2. Explicit slave ID is required; equal IDs or identical port strings with local slave are rejected.
3. Controller YAML pwm_limit is 25.0 and service is /group_7/stm_setcontrol_type.
4. Ctrl+C terminates launched processes; observe physical stop and check no duplicate publishers.

Record observed results in TEST-RESULTS.md and attach accessible evidence in evidence.md. Implementation, verified operation and actual submission are separate statuses. Follow the lecturers' upload/live-demo requirements.
