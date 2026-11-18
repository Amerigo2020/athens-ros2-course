# D5.1-real: Bug0 on the real Galileo

[Assignment index](../README.md) | [Test results](TEST-RESULTS.md) | [Evidence](evidence.md)

## Assignment and source

- Current `Athens2026_ROS2.pptx`: slides 128 (also labelled D5.1).
- Older `Athens_ROS2_Course.pptx`: slides No equivalent Bug0 deliverable found.
- Original scaffold: [13_bug0_lidar_stm.py](../../../reference/templates/13_bug0_lidar_stm.py), upstream revision `cf9e122904ebcb55d336aa7e82d0760bc94cbb07`.
- Status: **Planned; no completed solution**.

Port the tested simulated Bug0 behavior to the real Galileo. Verify actual LiDAR/velocity topics, units, robot interface and speed limits; demonstrate avoidance in the designated test area. This shares D5.1 numbering with simulation but needs separate physical evidence.

## Team implementation / checkpoint

**Not implemented.** The original TODO template is only a reference.

Implement the task above, add the missing executable/assets and verify them before marking it complete.

## Execution

[Prepare the Jazzy environment and ports first](../SETUP.md). Each long-running command needs its own prepared terminal. Start recording before the demonstration, and finish it with Ctrl+C. Only one serial stage may access each physical device at a time.

```bash
# Prerequisite: completed simulated Bug0 and course robot bringup.
# Robot bringup/executable is not implemented in this repository.
ros2 topic list -t
ros2 topic info /scan -v
ros2 topic info /cmd_vel -v
ros2 bag record -o bags/d5_1_real_run01 /scan /cmd_vel /odom
```



## Acceptance and hand-in

1. Real robot receives expected commands and clears obstacles reproducibly.
2. Stop behavior works when scans/control disappear.
3. Separate real-robot video and bag; record hardware, limits and differences from simulation.

Record observed results in TEST-RESULTS.md and attach accessible evidence in evidence.md. Implementation, verified operation and actual submission are separate statuses. Follow the lecturers' upload/live-demo requirements.
