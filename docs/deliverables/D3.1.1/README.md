# D3.1.1: Install launch and configuration assets

[Assignment index](../README.md) | [Test results](TEST-RESULTS.md) | [Evidence](evidence.md)

## Assignment and source

- Current `Athens2026_ROS2.pptx`: slides 102 (combined D3 assignment).
- Older `Athens_ROS2_Course.pptx`: slides 116 (D3.1.1).
- Original scaffold: [stm_station_launch.py](../../../reference/templates/stm_station_launch.py), upstream revision `cf9e122904ebcb55d336aa7e82d0760bc94cbb07`.
- Status: **Implemented; ROS/hardware verification pending**.

Install launch/*.py and config/*.yaml into share/stm_station via setup.py. Declare launch, launch_ros and ament_index_python runtime dependencies. Ensure launch uses the installed package share rather than a source-directory assumption.

## Team implementation / checkpoint

[src/stm_station/setup.py](../../../src/stm_station/setup.py); package.xml; config/serial_params.yaml

Runnable stage/configuration preserved in the current tree. These checkpoints were reconstructed for traceability, not presented as previously observed historical progress.

## Execution

[Prepare the Jazzy environment and ports first](../SETUP.md). Each long-running command needs its own prepared terminal. Start recording before the demonstration, and finish it with Ctrl+C. Only one serial stage may access each physical device at a time.

```bash
colcon build --symlink-install --packages-up-to stm_station
source install/setup.bash
ros2 pkg prefix --share stm_station
ls "$(ros2 pkg prefix --share stm_station)/launch"
ls "$(ros2 pkg prefix --share stm_station)/config"
# Change directory to prove installed lookup works:
(cd /tmp && ros2 launch stm_station stm_serial_node_launch.py --show-args)
```



## Acceptance and hand-in

1. Both launch files and serial_params.yaml are installed.
2. --show-args works outside the workspace root.
3. Package dependencies resolve on the Jazzy VM.

Record observed results in TEST-RESULTS.md and attach accessible evidence in evidence.md. Implementation, verified operation and actual submission are separate statuses. Follow the lecturers' upload/live-demo requirements.
