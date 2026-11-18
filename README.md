<div align="center">

# Athens ROS 2 - Team WinningLeos

**Group 7 | ATHENS 2026 | UPM Madrid**

ROS 2 nodes for STM communication, master/slave control and the course deliverables.

[Quickstart](#quickstart) ? [Deliverables](#deliverables) ? [Documentation](#documentation) ? [Tests](#tests-and-acceptance)

</div>

## Table of Contents

- [About](#about)
- [Deliverables](#deliverables)
- [Quickstart](#quickstart)
- [Documentation](#documentation)
- [D1: STM serial bridge](#d1-stm-serial-bridge)
- [D2: Master/slave control](#d2-masterslave-control)
- [Tests and acceptance](#tests-and-acceptance)
- [Submission evidence](#submission-evidence)
- [Remaining work](#remaining-work)

## About

ROS 2 workspace with introductory exercises and STM deliverables D1/D2.

## Deliverables

| Deliverable | Implementation | Outstanding verification |
| --- | --- | --- |
| D1 serial bridge and custom messages | Implemented | ROS build, STM test, graph and bag |
| D2 master/slave and P/PD control | Implemented | ROS integration and two-STM tuning/test |
| D3 launch files | Planned | Implementation |
| D4 RViz/TF | Planned | Implementation |
| D5 Gazebo/Bug0/robot | Planned | Implementation |

Implementation does not mean hardware acceptance. No STM hardware or ROS installation was available during development. The course templates remain in the separate ROS_course checkout; they are not needed to build this workspace.

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
- `stm_station`: D1 serial bridge and D2 controller.
- [Course templates](https://github.com/Robolabo/ROS_course): reference implementation scaffolding. Its sample group 1/2 IDs are examples; our station is group 7.

The bridge uses parameters `port` and `baudrate`. The template YAML uses `serial_port` and `baud_rate` and cannot be passed to this node unchanged. Current routing parameters are startup-only.

## D1: STM serial bridge

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

Store the following under `docs/deliverables/D1/` and `docs/deliverables/D2/`:

- `README.md`: tested commit, date, team members, Ubuntu/ROS version, station IDs/ports, actual commands and gains.
- A test table with expected behavior, observed behavior and pass/fail for each test.
- `graph.png`: rqt_graph screenshot showing topics and nodes.
- `terminal.txt`: build, interface, topic and service outputs.
- `evidence.md`: accessible links to demonstration videos and bags, including the recording name and what each demonstrates.

```bash
mkdir -p docs/deliverables/{D1,D2}
# Run in a dedicated recording terminal, stop cleanly with Ctrl+C:
ros2 bag record -o bags/d2_run01 /group_7/stm_state /group_2/stm_state /group_2/stm_control
# After recording:
ros2 bag info bags/d2_run01 > docs/deliverables/D2/bag-info.txt
```

Bags and large videos go in the agreed course submission storage; Git currently ignores bags. Test results must reflect actual observations. Mark a deliverable as hardware-verified only after its tests pass, and record the submission date/location separately. Follow the lecturers' requirements for upload or live demonstration; a Git push alone does not establish acceptance.

## Remaining work

D3: installed launch files and shared configuration. D4: TF broadcaster, encoder rotation, IMU integration and saved RViz configuration. D5: Bug0 in Gazebo, real Galileo validation, optional STM-to-cmd_vel mapping. See Athens2026_ROS2 course slides for the assignment and starred extensions.
