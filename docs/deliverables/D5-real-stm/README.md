# D5-real-stm: STM controls real robot (starred extension)

[Assignment index](../README.md) | [Test results](TEST-RESULTS.md) | [Evidence](evidence.md)

## Assignment and source

- Current `Athens2026_ROS2.pptx`: slides 130 (D5*).
- Older `Athens_ROS2_Course.pptx`: slides No separate explicit real-STM deliverable found.
- Original scaffold: [12_stm_turtlebot_control.py](../../../reference/templates/12_stm_turtlebot_control.py), upstream revision `cf9e122904ebcb55d336aa7e82d0760bc94cbb07`.
- Status: **Planned; no completed solution**.

Use the tested STM-to-velocity mapping on the real robot. Verify robot connection, namespaces, limits and loss-of-input stop. This is distinct from real Bug0 at slide 128 and needs separate evidence.

## Team implementation / checkpoint

**Not implemented.** The original TODO template is only a reference.

Implement the task above, add the missing executable/assets and verify them before marking it complete.

## Execution

[Prepare the Jazzy environment and ports first](../SETUP.md). Each long-running command needs its own prepared terminal. Start recording before the demonstration, and finish it with Ctrl+C. Only one serial stage may access each physical device at a time.

```bash
# Prerequisite: implemented D5.2 and course real-robot bringup.
# Real bringup and STM-to-velocity executable are not implemented here.
ros2 topic info /cmd_vel -v
ros2 bag record -o bags/d5_real_stm_run01 /group_7/stm_state /cmd_vel
```



## Acceptance and hand-in

1. Physical forward/turn control follows STM input with documented scaling.
2. Input loss stops and normal stop command works.
3. Separate physical demonstration, topic graph and bag are supplied.

Record observed results in TEST-RESULTS.md and attach accessible evidence in evidence.md. Implementation, verified operation and actual submission are separate statuses. Follow the lecturers' upload/live-demo requirements.
