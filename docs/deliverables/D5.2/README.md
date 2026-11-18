# D5.2: STM controls simulated robot (starred extension)

[Assignment index](../README.md) | [Test results](TEST-RESULTS.md) | [Evidence](evidence.md)

## Assignment and source

- Current `Athens2026_ROS2.pptx`: slides 129; repeated as D5 at 133.
- Older `Athens_ROS2_Course.pptx`: slides 143 (D5).
- Original scaffold: [12_stm_turtlebot_control.py](../../../reference/templates/12_stm_turtlebot_control.py), upstream revision `cf9e122904ebcb55d336aa7e82d0760bc94cbb07`.
- Status: **Planned; no completed solution**.

Implement stm_turtlebot_control: map STM motor_velocity to cmd_vel.linear.x and IMU gyro to angular.z. Establish scale, units, deadband, limits and stale-input stop behavior. Confirm the course robot expects Twist or its actual velocity type. Current slide 133 repeats this task; do not claim a second implementation.

## Team implementation / checkpoint

**Not implemented.** The original TODO template is only a reference.

Implement the task above, add the missing executable/assets and verify them before marking it complete.

## Execution

[Prepare the Jazzy environment and ports first](../SETUP.md). Each long-running command needs its own prepared terminal. Start recording before the demonstration, and finish it with Ctrl+C. Only one serial stage may access each physical device at a time.

```bash
# Planned executable: NOT IMPLEMENTED; requires course simulator bringup.
# No stm_turtlebot_control executable exists yet. Implement it before running this task.
# After implementation, inspect and record the actual mapped topics:
ros2 topic info /cmd_vel -v
ros2 bag record -o bags/d5_2_run01 /group_7/stm_state /cmd_vel
```



## Acceptance and hand-in

1. Encoder velocity changes forward speed with stated scaling and limits.
2. Gyro motion changes turning speed with correct sign.
3. Stale state commands stop; video and bag demonstrate both axes.

Record observed results in TEST-RESULTS.md and attach accessible evidence in evidence.md. Implementation, verified operation and actual submission are separate statuses. Follow the lecturers' upload/live-demo requirements.
