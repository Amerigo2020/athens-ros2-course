# D4.2: Plot and record visualization results

[Assignment index](../README.md) | [Test results](TEST-RESULTS.md) | [Evidence](evidence.md)

## Assignment and source

- Current `Athens2026_ROS2.pptx`: slides 112 (D4.2).
- Older `Athens_ROS2_Course.pptx`: slides 132 (recording requirement).
- Original scaffold: [11_stm_visualization.py](../../../reference/templates/11_stm_visualization.py), upstream revision `cf9e122904ebcb55d336aa7e82d0760bc94cbb07`.
- Status: **Planned; no completed solution**.

After D4.1, plot state/estimated motion and record the TF and STM topics. Save the RViz configuration, screenshot/video, bag and an explanation of integration drift. This is the evidence subtask, separate from implementing the broadcaster.

## Team implementation / checkpoint

**Not implemented.** The original TODO template is only a reference.

Implement the task above, add the missing executable/assets and verify them before marking it complete.

## Execution

[Prepare the Jazzy environment and ports first](../SETUP.md). Each long-running command needs its own prepared terminal. Start recording before the demonstration, and finish it with Ctrl+C. Only one serial stage may access each physical device at a time.

```bash
# Prerequisite: implement and run D4.1 first.
ros2 bag record -o bags/d4_run01 /group_7/stm_state /tf /tf_static
rqt_graph
# After clean Ctrl+C:
ros2 bag info bags/d4_run01
```



## Acceptance and hand-in

1. Bag contains moving transforms and source state; inspect timestamps.
2. Saved RViz screenshot/video and plots explain translation and motor rotation.
3. Document measured drift/limitations instead of claiming absolute positioning accuracy.

Record observed results in TEST-RESULTS.md and attach accessible evidence in evidence.md. Implementation, verified operation and actual submission are separate statuses. Follow the lecturers' upload/live-demo requirements.
