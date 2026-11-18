# Deliverables walkthrough - Group 7

Work through this guide in order on **Ubuntu 24.04 / ROS 2 Jazzy**. Our station is Group 7. **Group 2 below is an example partner: replace every 2 with your actual partner ID and use its actual port.** Code is implemented through D4; ROS and physical acceptance are still unverified. D5 is pending.

## Before every task

Update and build from the team repository root:

```bash
git pull
source /opt/ros/jazzy/setup.bash
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
mkdir -p bags
ls -l /dev/serial/by-id/
```

Use actual device paths. Do not recreate packages; they are already in src. In **every Terminal A/B/C/D** below, cd to the repository and source /opt/ros/jazzy/setup.bash and install/setup.bash. Each long-running command needs its own terminal. Stop the previous task before starting the next: only one serial bridge per USB device, one controller per slave, and one message type per topic. Record before movement and Ctrl+C the recorder to finish its bag cleanly. New bag output directories must not already exist.

For every task, open its README, TEST-RESULTS.md and evidence.md using the links below. Fill tested commit (`git rev-parse HEAD`), tester/date, actual IDs/ports, units, gains and observations. Save small logs/screenshots/parameter dumps in that task folder. Upload bags/large videos to the agreed course storage and paste accessible links in evidence.md. Record actual submission separately; code or a push alone is not a delivered hardware result. [Detailed capture workflow](SETUP.md).

## D1.1 - Standard-message publisher

[Task](D1.1/README.md) | [Test log](D1.1/TEST-RESULTS.md) | [Evidence](D1.1/evidence.md)

**Prerequisites:** One STM attached and serial permissions configured; previous stages stopped.

Observe encoder/IMU changes while keeping the state stream live. Check that no command subscriber exists.

**Terminal A:** Start only this exercise stage.

```bash
ros2 run stm_station stm_serial_node_pub --ros-args -r __ns:=/group_7 -p port:=/dev/ttyACM0
```

**Terminal B:** Start recording before demonstrating movement.

```bash
ros2 bag record -o bags/d1_1_run01 /group_7/stm_state
```

**Terminal C:** Inspect the interfaces and graph. Close long-running viewers before the next command.

```bash
ros2 topic type /group_7/stm_state
ros2 topic echo /group_7/stm_state --once
ros2 node info /group_7/stm_serial_node
rqt_graph
```

**Expected:** Float32MultiArray contains eight values in encoder, velocity, acceleration xyz, gyro xyz order; no stm_control subscription.

**Stop / cleanup:** Ctrl+C any command publisher; for D1.2/1.3 observe motor stop after approximately 0.5 seconds without commands. Ctrl+C recorder, then bridge; close graph. Run `ros2 bag info bags/d1_1_run01` after recording.

**Hand-in:** State output, node/topic graph, interface types and bag; for command stages include a short response/stop video and measured observations. Save results and links under `docs/deliverables/D1.1/`.


## D1.2 - Standard-message publisher and subscriber

[Task](D1.2/README.md) | [Test log](D1.2/TEST-RESULTS.md) | [Evidence](D1.2/evidence.md)

**Prerequisites:** One STM attached and serial permissions configured; previous stages stopped.

Observe encoder/IMU changes while keeping the state stream live. Demonstrate command reception and timeout stop.

**Terminal A:** Start only this exercise stage.

```bash
ros2 run stm_station stm_serial_node_pub_sub --ros-args -r __ns:=/group_7 -p port:=/dev/ttyACM0
```

**Terminal B:** Start recording before demonstrating movement.

```bash
ros2 bag record -o bags/d1_2_run01 /group_7/stm_state /group_7/stm_control
```

**Terminal C:** Inspect the interfaces and graph. Close long-running viewers before the next command.

```bash
ros2 topic type /group_7/stm_state
ros2 topic echo /group_7/stm_state --once
ros2 node info /group_7/stm_serial_node
rqt_graph
```

**Terminal D:** First send stop; Ctrl+C that publisher before the small PWM test. Verify firmware direction/range first.

```bash
ros2 topic pub --rate 10 /group_7/stm_control std_msgs/msg/Float32MultiArray "{data: [0.0, 0.0, 0.0, 0.0]}"
# After Ctrl+C, start the next publisher:
ros2 topic pub --rate 10 /group_7/stm_control std_msgs/msg/Float32MultiArray "{data: [2.0, 0.0, 0.0, 10.0]}"
```

**Expected:** Both topics use Float32MultiArray; valid commands reach the motor while state publication continues.

**Stop / cleanup:** Ctrl+C any command publisher; for D1.2/1.3 observe motor stop after approximately 0.5 seconds without commands. Ctrl+C recorder, then bridge; close graph. Run `ros2 bag info bags/d1_2_run01` after recording.

**Hand-in:** State output, node/topic graph, interface types and bag; for command stages include a short response/stop video and measured observations. Save results and links under `docs/deliverables/D1.2/`.


## D1.3 - Custom STM interfaces

[Task](D1.3/README.md) | [Test log](D1.3/TEST-RESULTS.md) | [Evidence](D1.3/evidence.md)

**Prerequisites:** One STM attached and serial permissions configured; previous stages stopped.

Observe encoder/IMU changes while keeping the state stream live. Demonstrate command reception and timeout stop.

**Terminal A:** Start only this exercise stage.

```bash
ros2 run stm_station stm_serial_node --ros-args -r __ns:=/group_7 -p port:=/dev/ttyACM0
```

**Terminal B:** Start recording before demonstrating movement.

```bash
ros2 bag record -o bags/d1_3_run01 /group_7/stm_state /group_7/stm_control
```

**Terminal C:** Inspect the interfaces and graph. Close long-running viewers before the next command.

```bash
ros2 interface show stm_interfaces/msg/STMState
ros2 interface show stm_interfaces/msg/STMControl
ros2 topic type /group_7/stm_state
ros2 topic echo /group_7/stm_state --once
ros2 node info /group_7/stm_serial_node
rqt_graph
```

**Terminal D:** First send stop; Ctrl+C that publisher before the small PWM test. Verify firmware direction/range first.

```bash
ros2 topic pub --rate 10 /group_7/stm_control stm_interfaces/msg/STMControl "{control_type: 0}"
# After Ctrl+C, start the next publisher:
ros2 topic pub --rate 10 /group_7/stm_control stm_interfaces/msg/STMControl "{control_type: 2, pwm: 10.0}"
```

**Expected:** State/control types are STMState and STMControl, with named fields and advancing state stamps.

**Stop / cleanup:** Ctrl+C any command publisher; for D1.2/1.3 observe motor stop after approximately 0.5 seconds without commands. Ctrl+C recorder, then bridge; close graph. Run `ros2 bag info bags/d1_3_run01` after recording.

**Hand-in:** State output, node/topic graph, interface types and bag; for command stages include a short response/stop video and measured observations. Save results and links under `docs/deliverables/D1.3/`.


## D2.1 - Master/slave onboard position

[Task](D2.1/README.md) | [Test log](D2.1/TEST-RESULTS.md) | [Evidence](D2.1/evidence.md)

**Prerequisites:** D1.3 working on two stations, IDs/ports verified, no other controller or manual slave command publisher.

Use separate terminals for both bridges. Gains below are examples to tune on your hardware. The controller starts in stop; arm only after both state streams are present. D2.2 and D2.3 are starred extensions.

**Terminal A:** Start our custom master bridge.

```bash
ros2 run stm_station stm_serial_node --ros-args -r __ns:=/group_7 -p port:=/dev/ttyACM0
```

**Terminal B:** Start the partner custom slave bridge.

```bash
ros2 run stm_station stm_serial_node --ros-args -r __ns:=/group_2 -p port:=/dev/ttyACM1
```

**Terminal C:** Start one controller with reduced host PWM limit. Onboard position mode uses firmware behavior, not this PWM clamp.

```bash
ros2 run stm_station stm_control_node --ros-args -p master_group_id:=7 -p slave_group_id:=2 -p pwm_limit:=25.0
```

**Terminal D:** Start the recording before enabling control.

```bash
ros2 bag record -o bags/d2_1_run01 /group_7/stm_state /group_2/stm_state /group_2/stm_control
```

**Terminal E:** Check states, then enable this mode and move the master slowly.

```bash
ros2 topic echo /group_7/stm_state --once
ros2 topic echo /group_2/stm_state --once
ros2 service call /stm_setcontrol_type stm_interfaces/srv/STMSetControlType "{control_type: 1, kp: 1.0, kd: 0.0}"
ros2 topic echo /group_2/stm_control --once
ros2 node info /stm_control_node
```

**Expected:** Slave setpoint follows master encoder, with control_type=1. Valid service requests return success=true. Physical behavior still requires testing.

**Stop / cleanup:** In Terminal E run `ros2 service call /stm_setcontrol_type stm_interfaces/srv/STMSetControlType "{control_type: 0, kp: 0.0, kd: 0.0}"`. Observe stop. Also test invalid mode 99 (success=false) and interrupted master feedback (stop/disarm; explicit rearm required). Ctrl+C recorder, controller and bridges, in that order.

**Hand-in:** Two state traces, slave command trace, graph and video. Record exact gains/units, firmware, PWM limit and stop/feedback-loss results. For P/PD include plots comparing master and slave. Save results and links under `docs/deliverables/D2.1/`.


## D2.2 - Host position P controller

[Task](D2.2/README.md) | [Test log](D2.2/TEST-RESULTS.md) | [Evidence](D2.2/evidence.md)

**Prerequisites:** D1.3 working on two stations, IDs/ports verified, no other controller or manual slave command publisher.

Use separate terminals for both bridges. Gains below are examples to tune on your hardware. The controller starts in stop; arm only after both state streams are present. D2.2 and D2.3 are starred extensions.

**Terminal A:** Start our custom master bridge.

```bash
ros2 run stm_station stm_serial_node --ros-args -r __ns:=/group_7 -p port:=/dev/ttyACM0
```

**Terminal B:** Start the partner custom slave bridge.

```bash
ros2 run stm_station stm_serial_node --ros-args -r __ns:=/group_2 -p port:=/dev/ttyACM1
```

**Terminal C:** Start one controller with reduced host PWM limit. Onboard position mode uses firmware behavior, not this PWM clamp.

```bash
ros2 run stm_station stm_control_node --ros-args -p master_group_id:=7 -p slave_group_id:=2 -p pwm_limit:=25.0
```

**Terminal D:** Start the recording before enabling control.

```bash
ros2 bag record -o bags/d2_2_run01 /group_7/stm_state /group_2/stm_state /group_2/stm_control
```

**Terminal E:** Check states, then enable this mode and move the master slowly.

```bash
ros2 topic echo /group_7/stm_state --once
ros2 topic echo /group_2/stm_state --once
ros2 service call /stm_setcontrol_type stm_interfaces/srv/STMSetControlType "{control_type: 2, kp: 1.0, kd: 0.0}"
ros2 topic echo /group_2/stm_control --once
ros2 node info /stm_control_node
```

**Expected:** Slave receives mode 2 PWM: kp*position_error, clamped to +/-25. Compare physical tracking against recorded master/slave traces. Valid service requests return success=true. Physical behavior still requires testing.

**Stop / cleanup:** In Terminal E run `ros2 service call /stm_setcontrol_type stm_interfaces/srv/STMSetControlType "{control_type: 0, kp: 0.0, kd: 0.0}"`. Observe stop. Also test invalid mode 99 (success=false) and interrupted master feedback (stop/disarm; explicit rearm required). Ctrl+C recorder, controller and bridges, in that order.

**Hand-in:** Two state traces, slave command trace, graph and video. Record exact gains/units, firmware, PWM limit and stop/feedback-loss results. For P/PD include plots comparing master and slave. Save results and links under `docs/deliverables/D2.2/`.


## D2.3 - Host impedance PD controller

[Task](D2.3/README.md) | [Test log](D2.3/TEST-RESULTS.md) | [Evidence](D2.3/evidence.md)

**Prerequisites:** D1.3 working on two stations, IDs/ports verified, no other controller or manual slave command publisher.

Use separate terminals for both bridges. Gains below are examples to tune on your hardware. The controller starts in stop; arm only after both state streams are present. D2.2 and D2.3 are starred extensions.

**Terminal A:** Start our custom master bridge.

```bash
ros2 run stm_station stm_serial_node --ros-args -r __ns:=/group_7 -p port:=/dev/ttyACM0
```

**Terminal B:** Start the partner custom slave bridge.

```bash
ros2 run stm_station stm_serial_node --ros-args -r __ns:=/group_2 -p port:=/dev/ttyACM1
```

**Terminal C:** Start one controller with reduced host PWM limit. Onboard position mode uses firmware behavior, not this PWM clamp.

```bash
ros2 run stm_station stm_control_node --ros-args -p master_group_id:=7 -p slave_group_id:=2 -p pwm_limit:=25.0
```

**Terminal D:** Start the recording before enabling control.

```bash
ros2 bag record -o bags/d2_3_run01 /group_7/stm_state /group_2/stm_state /group_2/stm_control
```

**Terminal E:** Check states, then enable this mode and move the master slowly.

```bash
ros2 topic echo /group_7/stm_state --once
ros2 topic echo /group_2/stm_state --once
ros2 service call /stm_setcontrol_type stm_interfaces/srv/STMSetControlType "{control_type: 2, kp: 1.0, kd: 0.1}"
ros2 topic echo /group_2/stm_control --once
ros2 node info /stm_control_node
```

**Expected:** Slave receives mode 2 PWM: kp*position_error + kd*velocity_error, clamped to +/-25. Compare physical tracking against recorded master/slave traces. Valid service requests return success=true. Physical behavior still requires testing.

**Stop / cleanup:** In Terminal E run `ros2 service call /stm_setcontrol_type stm_interfaces/srv/STMSetControlType "{control_type: 0, kp: 0.0, kd: 0.0}"`. Observe stop. Also test invalid mode 99 (success=false) and interrupted master feedback (stop/disarm; explicit rearm required). Ctrl+C recorder, controller and bridges, in that order.

**Hand-in:** Two state traces, slave command trace, graph and video. Record exact gains/units, firmware, PWM limit and stop/feedback-loss results. For P/PD include plots comparing master and slave. Save results and links under `docs/deliverables/D2.3/`.


## D3.1.0 - Single-station launch

[Task](D3.1.0/README.md) | [Test log](D3.1.0/TEST-RESULTS.md) | [Evidence](D3.1.0/evidence.md)

**Prerequisites:** D1.3 working; manual bridge stopped.

Launch the installed custom serial node using Group 7 namespace.

**Terminal A:** Inspect arguments, then start the station.

```bash
ros2 launch stm_station stm_serial_node_launch.py --show-args
ros2 launch stm_station stm_serial_node_launch.py group_id:=7 port:=/dev/ttyACM0
```

**Terminal B:** Verify the node and YAML parameters.

```bash
ros2 node info /group_7/stm_serial_node
ros2 param get /group_7/stm_serial_node baudrate
ros2 topic echo /group_7/stm_state --once
```

**Expected:** One /group_7/stm_serial_node exists; baudrate is 115200 and state arrives.

**Stop / cleanup:** Ctrl+C launch; ensure its bridge exits.

**Hand-in:** Argument output, node info, actual parameters and state transcript. Save results and links under `docs/deliverables/D3.1.0/`.


## D3.1.1 - Launch/config installation

[Task](D3.1.1/README.md) | [Test log](D3.1.1/TEST-RESULTS.md) | [Evidence](D3.1.1/evidence.md)

**Prerequisites:** Workspace built and sourced; hardware not needed.

Verify packaged launch, YAML and RViz assets independently of the source working directory.

**Terminal A:** Build and inspect installed share files.

```bash
colcon build --symlink-install --packages-up-to stm_station
source install/setup.bash
ls "$(ros2 pkg prefix --share stm_station)/launch"
ls "$(ros2 pkg prefix --share stm_station)/config"
ls "$(ros2 pkg prefix --share stm_station)/rviz"
(cd /tmp && ros2 launch stm_station stm_serial_node_launch.py --show-args)
```

**Expected:** Three launch files, serial_params.yaml and stm_config.rviz are installed; --show-args succeeds from /tmp.

**Stop / cleanup:** No device or long-running node is started by --show-args.

**Hand-in:** Build output, installed file listing and successful argument listing outside the workspace. Save results and links under `docs/deliverables/D3.1.1/`.


## D3.2 - Combined launch

[Task](D3.2/README.md) | [Test log](D3.2/TEST-RESULTS.md) | [Evidence](D3.2/evidence.md)

**Prerequisites:** Both USB devices available locally, or partner bridge running on the same ROS network. Stop manual bridges/controllers first.

Use the local-two-device example below. For a remote partner set start_slave:=false and let the partner start its bridge; do not launch two bridges for one station.

**Terminal A:** Launch both bridges and the controller; partner 2 must be replaced if different.

```bash
ros2 launch stm_station stm_serial_control_launch.py master_group_id:=7 slave_group_id:=2 master_port:=/dev/ttyACM0 start_slave:=true slave_port:=/dev/ttyACM1
```

**Terminal B:** Check namespaced controller and stop service.

```bash
ros2 node list
ros2 param get /group_7/stm_control_node pwm_limit
ros2 service call /group_7/stm_setcontrol_type stm_interfaces/srv/STMSetControlType "{control_type: 0, kp: 0.0, kd: 0.0}"
rqt_graph
```

**Expected:** Two bridges plus /group_7/stm_control_node; pwm_limit=25.0; namespaced stop service returns success=true. Starts in stop.

**Stop / cleanup:** Keep controller in stop, Ctrl+C launch, close graph; stop a separately started partner bridge when finished.

**Hand-in:** Graph, node/parameter/service output, arguments and observed process/motor stop. Save results and links under `docs/deliverables/D3.2/`.


<a id="d41-tf-rviz"></a>

## D4.1 - TF and RViz

[Task](D4.1/README.md) | [Test log](D4.1/TEST-RESULTS.md) | [Evidence](D4.1/evidence.md)

**Prerequisites:** D1.3 working; stationary STM for startup calibration. Stop any previous bridge, or set start_serial:=false.

Start visualization, keep the device still for the first 50 samples, then rotate the motor and translate without tilting. Confirm encoder and acceleration units from firmware.

**Terminal A:** Launch bridge, TF/Path node and saved RViz view.

```bash
ros2 launch stm_station stm_visualization_launch.py group_id:=7 port:=/dev/ttyACM0
```

**Terminal B:** Inspect body TF; Ctrl+C before inspecting motor TF.

```bash
ros2 run tf2_ros tf2_echo world group_7/stm_station
# After Ctrl+C:
ros2 run tf2_ros tf2_echo group_7/stm_station group_7/motor
```

**Terminal C:** Inspect position, reset while stationary, and confirm reset response.

```bash
ros2 topic echo /group_7/stm_position --once
ros2 service call /group_7/reset_visualization std_srvs/srv/Trigger "{}"
```

**Expected:** Connected world -> group_7/stm_station -> group_7/motor frames; encoder-driven motor yaw; bounded trajectory. Reset returns success=true, clears translation/path and recalibrates. Acceleration integration drifts; changing tilt is not compensated.

**Stop / cleanup:** Ctrl+C TF echo and launch. If bridge was started separately, terminate it when finished. Visualization itself sends no motor commands.

**Hand-in:** RViz view, rotation scaling/sign measurement, calibration/reset observations, actual config/units and movement video. Save results and links under `docs/deliverables/D4.1/`.


<a id="d42-plots-recording"></a>

## D4.2 - Plots and recording

[Task](D4.2/README.md) | [Test log](D4.2/TEST-RESULTS.md) | [Evidence](D4.2/evidence.md)

**Prerequisites:** D4.1 running, calibrated and units confirmed.

Record first, then capture an axis-motion and motor-rotation demonstration. Keep the station level; measure stationary drift and describe limitations.

**Terminal B:** Record state, estimates, path and transforms.

```bash
ros2 bag record -o bags/d4_run01 /group_7/stm_state /group_7/stm_position /group_7/stm_velocity /group_7/stm_path /tf /tf_static
```

**Terminal C:** Plot estimated translation.

```bash
ros2 run rqt_plot rqt_plot /group_7/stm_position/point/x /group_7/stm_position/point/y /group_7/stm_position/point/z
```

**Terminal D:** Save actual configuration; open graph.

```bash
ros2 param dump /group_7/stm_visualization_node > docs/deliverables/D4.2/parameters.yaml
rqt_graph
```

**Expected:** Position curves and TF/Path correspond to the same timestamped state stream. Document drift instead of claiming absolute accuracy.

**Stop / cleanup:** Ctrl+C recorder, then run `ros2 bag info bags/d4_run01 > docs/deliverables/D4.2/bag-info.txt`. Close plots/graph and stop D4 launch.

**Hand-in:** Plot and RViz screenshots, graph, parameters.yaml, bag-info.txt, video and linked bag. Physical evidence is not collected yet. Save results and links under `docs/deliverables/D4.2/`.


## D5.1-simulation - Bug0 in Gazebo - NOT IMPLEMENTED

[Task](D5.1-simulation/README.md) | [Test log](D5.1-simulation/TEST-RESULTS.md) | [Evidence](D5.1-simulation/evidence.md)

**Prerequisites:** Course Galileo/Gazebo bringup and documented scan/velocity interface.

Implement the Bug0 controller from reference/templates/13_bug0_lidar_stm.py, register its executable, and test free path, obstacle avoidance and missing-scan stop. The course simulator launcher is not included here.

**Terminal A:** After course bringup, inspect actual interfaces only. These commands do not launch a robot or a missing solution.

```bash
ros2 topic list -t
ros2 topic info /cmd_vel -v
```

**Expected:** A future simulation test must demonstrate avoidance, resumed motion, stop behavior and correct velocity type.

**Stop / cleanup:** No solution is started by this section. When testing future code, command zero velocity through the confirmed robot interface and stop recorder/controller/bringup according to the course robot instructions.

**Hand-in:** Prepare the linked test/evidence pages now; leave them NOT RUN. After implementation upload the task-specific video/bag and save graph, actual commands, robot version, topic types, limits and observations. Save results and links under `docs/deliverables/D5.1-simulation/`.


## D5.1-real - Real Galileo Bug0 - NOT IMPLEMENTED

[Task](D5.1-real/README.md) | [Test log](D5.1-real/TEST-RESULTS.md) | [Evidence](D5.1-real/evidence.md)

**Prerequisites:** Simulation task passed and real robot bringup available.

Port the tested Bug0 controller to the actual robot topics/units and course speed limits. No robot bringup or runnable Bug0 solution exists in this repo yet.

**Terminal A:** After course bringup, inspect actual interfaces only. These commands do not launch a robot or a missing solution.

```bash
ros2 topic list -t
ros2 topic info /cmd_vel -v
```

**Expected:** A future physical test must demonstrate repeatable avoidance and stop behavior; simulation evidence is insufficient.

**Stop / cleanup:** No solution is started by this section. When testing future code, command zero velocity through the confirmed robot interface and stop recorder/controller/bringup according to the course robot instructions.

**Hand-in:** Prepare the linked test/evidence pages now; leave them NOT RUN. After implementation upload the task-specific video/bag and save graph, actual commands, robot version, topic types, limits and observations. Save results and links under `docs/deliverables/D5.1-real/`.


## D5.2 - STM to simulated robot - NOT IMPLEMENTED

[Task](D5.2/README.md) | [Test log](D5.2/TEST-RESULTS.md) | [Evidence](D5.2/evidence.md)

**Prerequisites:** Course simulator and verified STM velocity/gyro units.

Implement/register stm_turtlebot_control from reference/templates/12_stm_turtlebot_control.py. Map motor_velocity to linear.x and gyro to angular.z with scaling, limits and stale-state stop. Do not run the unfinished reference template.

**Terminal A:** After course bringup, inspect actual interfaces only. These commands do not launch a robot or a missing solution.

```bash
ros2 topic list -t
ros2 topic info /cmd_vel -v
```

**Expected:** Future tests must demonstrate both speed axes and stale-input stop. Current slide 133 repeats this task, not a second completed assignment.

**Stop / cleanup:** No solution is started by this section. When testing future code, command zero velocity through the confirmed robot interface and stop recorder/controller/bringup according to the course robot instructions.

**Hand-in:** Prepare the linked test/evidence pages now; leave them NOT RUN. After implementation upload the task-specific video/bag and save graph, actual commands, robot version, topic types, limits and observations. Save results and links under `docs/deliverables/D5.2/`.


## D5-real-stm - STM to real robot - NOT IMPLEMENTED

[Task](D5-real-stm/README.md) | [Test log](D5-real-stm/TEST-RESULTS.md) | [Evidence](D5-real-stm/evidence.md)

**Prerequisites:** D5.2 verified plus course real-robot bringup.

Adapt the completed mapping to the actual robot and verify physical response and loss-of-input stop. No runnable solution is available yet.

**Terminal A:** After course bringup, inspect actual interfaces only. These commands do not launch a robot or a missing solution.

```bash
ros2 topic list -t
ros2 topic info /cmd_vel -v
```

**Expected:** Future tests must demonstrate real forward/turn control and stop behavior, with separate physical evidence.

**Stop / cleanup:** No solution is started by this section. When testing future code, command zero velocity through the confirmed robot interface and stop recorder/controller/bringup according to the course robot instructions.

**Hand-in:** Prepare the linked test/evidence pages now; leave them NOT RUN. After implementation upload the task-specific video/bag and save graph, actual commands, robot version, topic types, limits and observations. Save results and links under `docs/deliverables/D5-real-stm/`.
