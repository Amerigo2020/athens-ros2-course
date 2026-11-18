# Local validation

Environment: Windows, Python 3.12. No ROS 2 installation or connected STM/robot available.

## Executed checks

- `python -m pytest src/stm_station/test -q`: **32 passed, 1 skipped**. The skipped module constructs real ROS launch actions including D4 visualization and requires launch/launch_ros. See the captured [pytest output](local-pytest.txt).
- `python -m compileall -q src/stm_station`: passed. Original TODO reference templates are intentionally excluded.
- D4 tests cover stationary offset, encoder/gear conversion, three-axis integration, coasting, reset, invalid values, scaling/deadband and time gaps/reversal. YAML configuration and saved RViz configuration parse successfully. An independent code review reported no actionable findings; this is not runtime verification.
- All 16 archived template SHA256 hashes matched their manifest; archive content was extracted from upstream Git blobs at cf9e122904ebcb55d336aa7e82d0760bc94cbb07.
- Local Markdown file links resolve; all package.xml files parse.
- `git diff --check`: passed for team changes. Original scaffold bytes are preserved separately.

The local checks cover serial parsing, invalid values, standard array command order, P/PD math, saturation, group/port validation and setuptools installation asset declarations including the D4 launch and RViz file. They do not exercise a ROS graph, generated message serialization, a physical serial port or actual installed launch execution.

## Reproduce

On the course VM with Python pytest and setuptools installed, from the repository root:

```bash
source /opt/ros/jazzy/setup.bash
source install/setup.bash
PYTHONPATH=src/stm_station python3 -m pytest src/stm_station/test -q
```

On this Windows machine setuptools was absent and was installed into a temporary dependency directory; the test PYTHONPATH included src/stm_station and that directory. No ROS libraries were substituted with mocks to claim runtime success.

## Not executed

ROS build, installed launch lookup/parameter application, serial device behavior, master/slave tracking and stop timing, RViz/Gazebo and real robot tests: **NOT RUN**. Course submission: **NOT RECORDED**.

Every task's test results section intentionally retains NOT RUN until actual ROS/hardware observations are supplied. These local results cannot be used as physical pass evidence.
