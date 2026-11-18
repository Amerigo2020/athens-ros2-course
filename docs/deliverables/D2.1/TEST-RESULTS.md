# D2.1 test results

Status: **NOT RUN on ROS / hardware**. Code exists; local checks are recorded centrally. This document contains expected outcomes, not claimed observations.

- Tester(s): not recorded
- Run date/time: not recorded
- Tested commit (`git rev-parse HEAD`): not recorded
- Environment: intended Ubuntu 24.04 / ROS 2 Jazzy; actual not recorded
- Station IDs, serial ports, firmware/robot version: not recorded
- Actual gains, limits, units and configuration: not recorded

| Test | Expected result | Status | Observed result / evidence |
| --- | --- | --- | --- |
| 1 | Controller has two state subscribers, one slave command publisher and requested service. | NOT RUN | Not recorded |
| 2 | Mode 1 passes master position and kp to the slave and the slave tracks physically. | NOT RUN | Not recorded |
| 3 | Mode 0 stops; invalid mode returns success=false and stops. | NOT RUN | Not recorded |
| 4 | Stopping master feedback disarms within state_timeout; restoring feedback requires a new service request. | NOT RUN | Not recorded |

Build and actual ROS startup: NOT RUN. Physical demonstration: NOT RUN. Attach command output and failures as well as successful results. Replace NOT RUN only after carrying out the test. [Local checks and limitations](../LOCAL-VALIDATION.md).
