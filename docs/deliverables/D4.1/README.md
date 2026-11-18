# D4.1: TF visualization of STM

[Assignment index](../README.md) | [Walkthrough](../WALKTHROUGH.md#d41-tf-rviz) | [Test results](TEST-RESULTS.md) | [Evidence](evidence.md)

## Assignment and implementation

Current Athens2026_ROS2.pptx slide 112 (D4.1); older Athens_ROS2_Course.pptx slide 132. [Original TODO scaffold](../../../reference/templates/11_stm_visualization.py) is unchanged at upstream cf9e122904ebcb55d336aa7e82d0760bc94cbb07.

**Implemented; ROS/RViz and physical verification pending.** [visualization_node.py](../../../src/stm_station/stm_station/visualization_node.py) subscribes to Group 7 STMState; [motion.py](../../../src/stm_station/stm_station/motion.py) performs calibration/integration. [Installed launch](../../../src/stm_station/launch/stm_visualization_launch.py) optionally starts the bridge and RViz with [saved configuration](../../../src/stm_station/rviz/stm_config.rviz).

## Frames, units and assumptions

TF: `world -> group_7/stm_station -> group_7/motor`. Station translation is the IMU estimate with identity orientation; the child motor rotates about z. Frames have no leading slash. Motor yaw = encoder ticks * 2*pi/(24*9.7), using the template's tick and gear-ratio values. Confirm these values and tick decoding on the actual device; encoder_direction can be -1.0.

Keep the station stationary at startup: the first 50 distinct valid timestamps calibrate the mean acceleration offset. Values are scaled by acceleration_scale (default 1.0, assuming m/s^2; use 9.81 if readings are in g). Integration uses message header time, falling back to ROS time only for zero stamps. Duplicate samples do not integrate; reversed time or a gap exceeding max_dt (0.2 s) clears velocity and skips that integration step. A 0.5 m/s^2 norm deadband removes small corrected accelerations; existing velocity still contributes to position.

This is a fixed-axis educational estimate: it does not recover IMU attitude or compensate changing gravity direction when tilted. Motor encoder yaw is not IMU body attitude. Translation drifts and is not an absolute position measurement. Reset while stationary to recalibrate. No unit/gain calibration or hardware performance is claimed.

## Run

[Prepare Jazzy and build first](../SETUP.md). Terminal A, with no other bridge on this device:

```bash
ros2 launch stm_station stm_visualization_launch.py group_id:=7 port:=/dev/ttyACM0
```

If the custom bridge is already running, use `start_serial:=false`. For headless use add `start_rviz:=false`. Copy/edit serial_params.yaml and pass params_file:=/absolute/path.yaml to adjust calibration/scale/encoder parameters.

Terminal B:

```bash
ros2 run tf2_ros tf2_echo world group_7/stm_station
# In another prepared terminal or after Ctrl+C:
ros2 run tf2_ros tf2_echo group_7/stm_station group_7/motor
ros2 service call /group_7/reset_visualization std_srvs/srv/Trigger "{}"
```

Expected: RViz shows connected TF axes and a bounded trajectory in world; motor rotation follows the encoder. Reset returns success=true, clears the path/translation and restarts stationary calibration. The path retains at most 1000 samples. Group IDs other than 7 also remap the RViz path topic.

Stop TF echo with Ctrl+C; stop launch with Ctrl+C. If start_serial=false, terminate the separately started bridge only when finished with it. The visualization sends no motor commands. See D4.2 for plotting/recording.

## Acceptance

1. Confirm installed launch/config lookup, correct topic/group and a connected TF tree in RViz.
2. Measure one motor/output revolution against encoder ticks and check rotation sign.
3. Demonstrate stationary calibration, translation response, reset, gap handling and stationary drift.
4. Save RViz screenshot/video, actual parameters and units, bag and observations in the linked test/evidence files.
