# D4.1: TF visualization of STM

[Assignment index](../README.md) | [Test results](TEST-RESULTS.md) | [Evidence](evidence.md)

## Assignment and source

- Current `Athens2026_ROS2.pptx`: slides 112 (D4.1).
- Older `Athens_ROS2_Course.pptx`: slides 132.
- Original scaffold: [11_stm_visualization.py](../../../reference/templates/11_stm_visualization.py), upstream revision `cf9e122904ebcb55d336aa7e82d0760bc94cbb07`.
- Status: **Planned; no completed solution**.

Implement stm_visualization_node in stm_station. Subscribe to STMState; convert encoder to motor rotation; estimate velocity/position by integrating IMU acceleration with measured dt; publish a documented TF tree. Resolve units, gravity/offset treatment, frame convention and reset/drift behavior. Add executable, dependencies and a saved RViz configuration.

## Team implementation / checkpoint

**Not implemented.** The original TODO template is only a reference.

Implement the task above, add the missing executable/assets and verify them before marking it complete.

## Execution

[Prepare the Jazzy environment and ports first](../SETUP.md). Each long-running command needs its own prepared terminal. Start recording before the demonstration, and finish it with Ctrl+C. Only one serial stage may access each physical device at a time.

```bash
# Planned executable: NOT IMPLEMENTED. Do not run the TODO reference as a solution.
# After implementation, with custom serial bridge running:
ros2 run stm_station stm_visualization_node --ros-args -r __ns:=/group_7
ros2 run tf2_ros tf2_echo world group_7/stm
rviz2
```



## Acceptance and hand-in

1. TF tree is connected and RViz fixed frame resolves all displayed frames.
2. Encoder rotation direction/scaling is correct.
3. Estimated translation responds plausibly; stationary drift and reset behavior are measured.

Record observed results in TEST-RESULTS.md and attach accessible evidence in evidence.md. Implementation, verified operation and actual submission are separate statuses. Follow the lecturers' upload/live-demo requirements.
