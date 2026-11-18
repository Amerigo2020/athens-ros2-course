# D5.1-simulation: Bug0 navigation in Gazebo

[Assignment index](../README.md) | [Test results](TEST-RESULTS.md) | [Evidence](evidence.md)

## Assignment and source

- Current `Athens2026_ROS2.pptx`: slides 125.
- Older `Athens_ROS2_Course.pptx`: slides No equivalent Bug0 deliverable found.
- Original scaffold: [13_bug0_lidar_stm.py](../../../reference/templates/13_bug0_lidar_stm.py), upstream revision `cf9e122904ebcb55d336aa7e82d0760bc94cbb07`.
- Status: **Planned; no completed solution**.

Implement Bug0 using LiDAR scan sectors and obstacle/free-motion behavior. Publish appropriate commands for the simulated Galileo and, where required by the template, STM feedback. Confirm the supplied world, robot launch and velocity message type from the actual course environment before adding exact startup commands.

## Team implementation / checkpoint

**Not implemented.** The original TODO template is only a reference.

Implement the task above, add the missing executable/assets and verify them before marking it complete.

## Execution

[Prepare the Jazzy environment and ports first](../SETUP.md). Each long-running command needs its own prepared terminal. Start recording before the demonstration, and finish it with Ctrl+C. Only one serial stage may access each physical device at a time.

```bash
# First start the course Galileo/Gazebo world using its supplied launcher.
# Simulator startup and our Bug0 executable are not implemented in this repo.
ros2 topic list -t
ros2 topic info /scan -v
ros2 topic info /cmd_vel -v
ros2 bag record -o bags/d5_1_sim_run01 /scan /cmd_vel /odom
```



## Acceptance and hand-in

1. Free path moves robot; obstacle triggers avoidance; robot resumes motion after clearing.
2. Test several obstacle placements and invalid/missing scans; document stop behavior.
3. Save video, graph and bag; verify course robot topics/message types.

Record observed results in TEST-RESULTS.md and attach accessible evidence in evidence.md. Implementation, verified operation and actual submission are separate statuses. Follow the lecturers' upload/live-demo requirements.
