# D1.3 test results

Status: **NOT RUN on ROS / hardware**. Code exists; local checks are recorded centrally. This document contains expected outcomes, not claimed observations.

- Tester(s): not recorded
- Run date/time: not recorded
- Tested commit (`git rev-parse HEAD`): not recorded
- Environment: intended Ubuntu 24.04 / ROS 2 Jazzy; actual not recorded
- Station IDs, serial ports, firmware/robot version: not recorded
- Actual gains, limits, units and configuration: not recorded

| Test | Expected result | Status | Observed result / evidence |
| --- | --- | --- | --- |
| 1 | Both interfaces build and show expected fields, including Header. | NOT RUN | Not recorded |
| 2 | STMState has plausible named values and advancing timestamps. | NOT RUN | Not recorded |
| 3 | STMControl produces the expected serial command/motor response; test mode 2 with a small PWM as in D1.2. | NOT RUN | Not recorded |
| 4 | Graph and bag use custom interfaces and no standard-message stage is running. | NOT RUN | Not recorded |

Build and actual ROS startup: NOT RUN. Physical demonstration: NOT RUN. Attach command output and failures as well as successful results. Replace NOT RUN only after carrying out the test. [Local checks and limitations](../LOCAL-VALIDATION.md).
