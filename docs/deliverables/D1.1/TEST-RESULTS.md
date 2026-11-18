# D1.1 test results

Status: **NOT RUN on ROS / hardware**. Code exists; local checks are recorded centrally. This document contains expected outcomes, not claimed observations.

- Tester(s): not recorded
- Run date/time: not recorded
- Tested commit (`git rev-parse HEAD`): not recorded
- Environment: intended Ubuntu 24.04 / ROS 2 Jazzy; actual not recorded
- Station IDs, serial ports, firmware/robot version: not recorded
- Actual gains, limits, units and configuration: not recorded

| Test | Expected result | Status | Observed result / evidence |
| --- | --- | --- | --- |
| 1 | Topic type is std_msgs/msg/Float32MultiArray; data contains eight fields in course order. | NOT RUN | Not recorded |
| 2 | Encoder and IMU readings respond plausibly to movement; measure actual frequency. | NOT RUN | Not recorded |
| 3 | No stm_control subscription exists in this publisher-only stage. | NOT RUN | Not recorded |
| 4 | Bag is readable and graph shows publisher/topic; include outputs/screenshots. | NOT RUN | Not recorded |

Build and actual ROS startup: NOT RUN. Physical demonstration: NOT RUN. Attach command output and failures as well as successful results. Replace NOT RUN only after carrying out the test. [Local checks and limitations](../LOCAL-VALIDATION.md).
