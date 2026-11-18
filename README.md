<div align="center">

# Athens ROS 2 - Team WinningLeos

**Group 7 | ATHENS 2026 | UPM Madrid**

ROS 2 nodes for STM communication, master/slave control and the course deliverables.

[**Step-by-step deliverables walkthrough**](docs/WALKTHROUGH.md) | [Quickstart](#quickstart) | [Deliverables](#deliverables) | [Documentation](#documentation) | [Tests](#tests-and-acceptance)

</div>

## Table of Contents

- [About](#about)
- [Deliverables](#deliverables)
- [Quickstart](#quickstart)
- [Documentation](#documentation)
- [D1: STM serial bridge](#d1-stm-serial-bridge)
- [D2: Master/slave control](#d2-masterslave-control)
- [D3: Launch files](#d3-launch-files)
- [D4: RViz visualization](#d4-rviz-visualization)
- [Deliverables walkthrough](docs/WALKTHROUGH.md)
- [Tests and acceptance](#tests-and-acceptance)
- [Submission evidence](#submission-evidence)
- [Remaining work](#remaining-work)

## About

ROS 2 workspace with introductory exercises and STM deliverables D1-D4.

## Deliverables

| Deliverable | Implementation | Outstanding verification |
| --- | --- | --- |
| D1 serial bridge and custom messages | Implemented | ROS build, STM test, graph and bag |
| D2 master/slave and P/PD control | Implemented | ROS integration and two-STM tuning/test |
| D3 launch files and YAML configuration | Implemented | Installed launch / ROS / hardware tests |
| D4 TF, bounded Path, RViz and plotting | Implemented | ROS/RViz launch and physical verification; evidence |
| D5 Gazebo/Bug0/robot | Planned | Implementation |

Implementation does not mean hardware acceptance. No STM hardware or ROS installation was available during development. Original course templates are archived with provenance in reference/templates; they are not needed to build this workspace.

## Quickstart

The course environment is **Ubuntu 24.04 with ROS 2 Jazzy** (course VM and Jazzy commands in the slides). Run from the repository root inside that VM. This Windows checkout is not the ROS runtime.

```bash
git clone https://github.com/Athens-ROS2-Course/Athens-ROS2-Team-WinningLeos.git
cd Athens-ROS2-Team-WinningLeos
```

For an existing checkout, use `git pull` from its configured team branch instead.

```bash
source /opt/ros/jazzy/setup.bash
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
```

Source ROS and `install/setup.bash` in every additional terminal. Give your user access to the serial device, usually through the `dialout` group, and reconnect your session if group membership changes.

## Documentation

- `first_package` and `first_interfaces`: existing Group 7 publisher/subscriber and custom service exercises, carried over from the original repository.
- `stm_interfaces`: STMState, STMControl and STMSetControlType.
- `stm_station`: D1 checkpoints, D2 controller and installed D3 launches.
- [Course templates](https://github.com/Robolabo/ROS_course): reference implementation scaffolding. Its sample group 1/2 IDs are examples; our station is group 7.

The bridge uses parameters `port` and `baudrate`. The original template YAML uses `serial_port` and `baud_rate` and cannot be passed unchanged. The installed team YAML in `src/stm_station/config/` uses our actual parameter names. Current routing parameters are startup-only.

## D1: STM serial bridge

Three separately runnable checkpoints are preserved:

| Task | Executable | State / command type |
| --- | --- | --- |
| [D1.1](docs/D1.md#d1-1) | `stm_serial_node_pub` | Float32MultiArray state only |
| [D1.2](docs/D1.md#d1-2) | `stm_serial_node_pub_sub` | Float32MultiArray state and command |
| [D1.3](docs/D1.md#d1-3) | `stm_serial_node` | STMState / STMControl |

These are reconstructed exercise stages sharing the serial transport. Stop the previous stage before starting the next: one bridge per device, one message type per topic. The commands below use the final D1.3 stage.

```bash
ros2 run stm_station stm_serial_node --ros-args -r __ns:=/group_7 -p port:=/dev/ttyACM0
```

Parameters (startup only): `port` (/dev/ttyACM0), `baudrate` (115200), `loop_frequency` (100.0 Hz), `command_timeout` (0.5 seconds).

The node publishes relative topic `stm_state` (stm_interfaces/msg/STMState) and subscribes to `stm_control` (stm_interfaces/msg/STMControl). Namespaces therefore separate stations.

Serial input is newline-terminated UTF-8:
`{motor_encoder,motor_velocity,accel_x,accel_y,accel_z,gyro_x,gyro_y,gyro_z}`.
Commands are `{control_type,setpoint,kp,pwm}` followed by a newline. Firmware modes: 0 stop, 1 onboard position control, 2 PWM. PWM is clamped to +/-250 per the course template. Confirm firmware units, direction and PWM range on the actual station before tuning.

```bash
ros2 topic echo /group_7/stm_state
ros2 topic pub --rate 10 /group_7/stm_control stm_interfaces/msg/STMControl "{control_type: 0}"
ros2 bag record -o bags/d1 /group_7/stm_state /group_7/stm_control
rqt_graph
```

Malformed/nonfinite frames are discarded. Partial lines are buffered. The bridge sends stop when commands cease for `command_timeout` and on normal shutdown. A stopped/crashed host or disconnected USB cannot guarantee a delivered stop; firmware watchdog behavior must be checked on hardware.

## D2: Master/slave control

Our station is **group 7**. The commands below use it as master and **group 2 only as an example partner**. Replace group 2 and its port with your actual slave station. If group 7 is the slave, exchange the IDs accordingly. A second station is required for the physical master/slave demonstration.

Start the group 7 bridge from D1, then the second serial bridge in another terminal (use its actual port):

```bash
ros2 run stm_station stm_serial_node --ros-args -r __ns:=/group_2 -p port:=/dev/ttyACM1
ros2 run stm_station stm_control_node --ros-args -p master_group_id:=7 -p slave_group_id:=2
```

Run each command in its own terminal. The controller subscribes to both `/group_N/stm_state` topics, publishes `/group_2/stm_control` at 50 Hz, and exposes `/stm_setcontrol_type`.

Service modes:

- 0: stop.
- 1: send master encoder position as the slave onboard position setpoint, using kp.
- 2: compute host PWM = kp * (master position - slave position) + kd * (master velocity - slave velocity). With kd=0 this is D2.2 position P control; with kd>0 it is D2.3 impedance PD control.

```bash
# Onboard position tracking (example gain; tune on actual hardware)
ros2 service call /stm_setcontrol_type stm_interfaces/srv/STMSetControlType "{control_type: 1, kp: 1.0, kd: 0.0}"
# Host P control
ros2 service call /stm_setcontrol_type stm_interfaces/srv/STMSetControlType "{control_type: 2, kp: 1.0, kd: 0.0}"
# Host PD / impedance control
ros2 service call /stm_setcontrol_type stm_interfaces/srv/STMSetControlType "{control_type: 2, kp: 1.0, kd: 0.1}"
# Stop
ros2 service call /stm_setcontrol_type stm_interfaces/srv/STMSetControlType "{control_type: 0, kp: 0.0, kd: 0.0}"
```

Use a single command publisher for the slave. Start in stop mode. Arm only after both state streams are present. Missing/stale feedback (> `state_timeout`, default 0.5 seconds) stops and disarms the controller; call the service again after feedback resumes. Invalid service requests stop and return success=false. `pwm_limit` defaults to 250.0 and can be reduced at startup. Group IDs must be distinct positive integers. All controller parameters are startup-only; restart to change group routing.

## D3: Launch files

Rebuild and source the workspace after pulling. The installed YAML defaults to 115200 baud, 100 Hz serial polling, 0.5 s timeouts and a reduced controller PWM limit of 25.0. This limit applies to host PWM mode; onboard position control uses firmware behavior.

```bash
# Single Group 7 station:
ros2 launch stm_station stm_serial_node_launch.py group_id:=7 port:=/dev/ttyACM0

# Alternative: master bridge plus controller; partner runs its bridge separately.
# Group 2 is an example; replace it with the actual partner group.
ros2 launch stm_station stm_serial_control_launch.py master_group_id:=7 slave_group_id:=2

# Alternative: both USB devices are on this machine:
ros2 launch stm_station stm_serial_control_launch.py master_group_id:=7 slave_group_id:=2 start_slave:=true master_port:=/dev/ttyACM0 slave_port:=/dev/ttyACM1
```

Choose one setup, not all at once. The combined launch puts the controller under the master's namespace: its service is **`/group_7/stm_setcontrol_type`**, whereas standalone `ros2 run` examples above use `/stm_setcontrol_type`. Both start in stop mode.

```bash
# In a separate prepared terminal after the combined launch:
ros2 service call /group_7/stm_setcontrol_type stm_interfaces/srv/STMSetControlType "{control_type: 0, kp: 0.0, kd: 0.0}"
ros2 param get /group_7/stm_control_node pwm_limit
ros2 launch stm_station stm_serial_control_launch.py --show-args
```

Override groups/ports through launch arguments. To change baudrate, frequency, timeouts or PWM limit, copy `src/stm_station/config/serial_params.yaml`, edit it and pass `params_file:=/absolute/path/to/config.yaml`. Parameters are startup-only. Launch argument port/group values override configuration. Use stable `/dev/serial/by-id/` paths where available; two aliases of the same device must never be launched together.

## D4: RViz visualization

[Follow the English walkthrough](docs/WALKTHROUGH.md#d41-tf-rviz) for terminal-by-terminal instructions, expected behavior, cleanup and evidence. Rebuild/source after pulling, then keep the station stationary during startup calibration:

```bash
ros2 launch stm_station stm_visualization_launch.py group_id:=7 port:=/dev/ttyACM0
```

This starts the custom bridge, visualization node and saved RViz view. Set start_serial:=false if the bridge already runs; start_rviz:=false supports headless operation. TF is `world -> group_7/stm_station -> group_7/motor`. The node publishes a bounded Path plus position/velocity topics for plotting. Reset with:

```bash
ros2 service call /group_7/reset_visualization std_srvs/srv/Trigger "{}"
```

The template's defaults are 24 encoder ticks/revolution and gear ratio 9.7. Acceleration is assumed m/s^2; configure acceleration_scale=9.81 for g units through the YAML file. Keep still for 50 offset samples. This fixed-axis integration drifts and does not compensate changing IMU tilt. [D4.1 details](docs/D4.md#d4-1) and [D4.2 plots/recordings](docs/D4.md#d4-2) explain tests and evidence. ROS/hardware operation is not yet verified.

## Tests and acceptance

Pure Python protocol/math tests (without ROS):

```bash
PYTHONPATH=src/stm_station python3 -m pytest src/stm_station/test -q
```

On the ROS machine additionally run `colcon test` and `colcon test-result --verbose`, then verify:

1. D1: state field order/units and timestamps; commanded stop and motor response; malformed input handling.
2. D2: both subscriptions and slave command topic; mode changes; P/PD sign and saturation; invalid request stops.
3. Stop one state publisher: controller must send mode 0 and require rearming. Stop controller: bridge must stop after its command timeout.
4. Save graph, state/command bags and a short demonstration for each deliverable.

Bags are intentionally ignored by Git. Keep recordings in the agreed submission storage and add their links to the hand-in documentation.

## Submission evidence

The [deliverable index](docs/INDEX.md) maps every task from both PPTX decks to its original template, runnable solution/configuration or planned work. The five D1.md-D5.md documents contain execution instructions, test results and evidence sections for all 15 subtasks. D1.1, D1.2 and D1.3 are separate checkpoints; duplicate D5 numbering and the older D3 subpoints are explained.

[Original templates and provenance](reference/README.md) are archived unchanged; TODO templates are not completed solutions. [Setup and evidence capture](docs/SETUP.md) explains terminal transcripts, bags, graphs, video and submission records. [Local validation](docs/LOCAL-VALIDATION.md) separates local checks from unperformed ROS/hardware tests.

No hardware or course submission is marked passed. Fill the task's actual observations and accessible recording links after testing, then record the required portal upload or live demonstration. Bags remain ignored by Git.

## Remaining work

D1-D4: ROS build, installed launch/RViz and physical verification plus hand-in evidence. D5: Bug0 in Gazebo, real Galileo validation, optional STM-to-cmd_vel mapping. See Athens2026_ROS2 course slides for the assignment and starred extensions.
