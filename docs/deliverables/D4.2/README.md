# D4.2: Plot and record visualization results

[Assignment index](../README.md) | [Walkthrough](../WALKTHROUGH.md#d42-plots-recording) | [Test results](TEST-RESULTS.md) | [Evidence](evidence.md)

Current Athens2026_ROS2.pptx slide 112 (D4.2); older Athens_ROS2_Course.pptx slide 132. Based on [original visualization scaffold](../../../reference/templates/11_stm_visualization.py).

**Recording and plotting workflow available; actual results NOT COLLECTED.** D4.1 publishes `stm_position` (PointStamped, metres), `stm_velocity` (Vector3Stamped, m/s), `stm_path` (Path), plus TF. Implemented telemetry/visualization does not establish physical pose accuracy.

## Execution

Prerequisite: [D4.1](../D4.1/README.md) running and calibrated with verified sensor units. All terminals must source Jazzy and the workspace.

Terminal B, before demonstrating motion:

```bash
ros2 bag record -o bags/d4_run01 /group_7/stm_state /group_7/stm_position /group_7/stm_velocity /group_7/stm_path /tf /tf_static
```

Terminal C:

```bash
ros2 run rqt_plot rqt_plot /group_7/stm_position/point/x /group_7/stm_position/point/y /group_7/stm_position/point/z
```

Terminal D:

```bash
rqt_graph
ros2 param dump /group_7/stm_visualization_node > docs/deliverables/D4.2/parameters.yaml
```

Move the station along one axis without tilting, return it to rest, and rotate the motor. Capture RViz/plot screenshots and a short video; record units, calibration interval, duration and observed drift. Do not claim that drift-free absolute positioning was achieved. D4 reset clears estimation only and sends no motor command.

Stop the recorder with Ctrl+C and then:

```bash
ros2 bag info bags/d4_run01 > docs/deliverables/D4.2/bag-info.txt
```

Close plot/graph windows and stop D4 launch with Ctrl+C. To inspect a bag later, stop live producers first; ros2 bag play bags/d4_run01 republishes recorded topics and must not be mixed with a live TF producer for the same frames.

## Evidence and submission

Save small screenshots, parameter dump, transcript and bag-info.txt here; upload bags/large videos to the agreed course storage. Paste accessible URLs in evidence.md. TEST-RESULTS.md must describe actual plot/TF/recording observations, tested commit, hardware and drift. Mark submission separately after the required portal upload or live demonstration.
