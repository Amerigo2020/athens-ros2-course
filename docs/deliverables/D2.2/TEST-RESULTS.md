# D2.2 test results

Status: **NOT RUN on ROS / hardware**. Code exists; local checks are recorded centrally. This document contains expected outcomes, not claimed observations.

- Tester(s): not recorded
- Run date/time: not recorded
- Tested commit (`git rev-parse HEAD`): not recorded
- Environment: intended Ubuntu 24.04 / ROS 2 Jazzy; actual not recorded
- Station IDs, serial ports, firmware/robot version: not recorded
- Actual gains, limits, units and configuration: not recorded

| Test | Expected result | Status | Observed result / evidence |
| --- | --- | --- | --- |
| 1 | Published mode is 2 (firmware PWM), not onboard position mode. | NOT RUN | Not recorded |
| 2 | PWM follows proportional position error with correct sign and configured saturation. | NOT RUN | Not recorded |
| 3 | Physical error decreases; record actual kp, units, limit and response. | NOT RUN | Not recorded |
| 4 | Feedback loss stops/disarms; graphs compare master and slave encoder trajectories. | NOT RUN | Not recorded |

Build and actual ROS startup: NOT RUN. Physical demonstration: NOT RUN. Attach command output and failures as well as successful results. Replace NOT RUN only after carrying out the test. [Local checks and limitations](../LOCAL-VALIDATION.md).
