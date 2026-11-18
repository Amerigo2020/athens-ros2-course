# Local validation

Environment: Windows, Python 3.12. No ROS 2 installation or connected STM/robot available.

## Executed checks

- `python -m pytest src/stm_station/test -q`: **57 passed, 1 skipped**. The skipped module constructs real ROS launch actions including D4 visualization and D5.1 Bug0 and requires launch/launch_ros. See the captured [pytest output](local-pytest.txt).
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

## D5.1 verification scope

Bug0 tests cover angle sectors with reversed scan order, infinity versus NaN, too-close readings, invalid metadata/missing coverage, forward/turn decisions, hysteresis and watchdog expiry. Regression tests cover invalid-then-valid scans and expired-then-new scans before the next timer: neither restores the armed state without an enable request. Package tests include the installed Bug0 launch, config and executable. Independent review found the callback-ordering disarm issue; it was fixed and regression-tested.

Simulator source was inspected at c70103a97268658b0ee562944996b9294b9599cd and the Jazzy controller documentation confirms the stamped interface. This is source/interface verification, not Gazebo execution. The external simulator was not installed or launched here.

## Not executed

ROS build, installed launch lookup/parameter application, serial device behavior, master/slave tracking and stop timing, RViz/Gazebo and real robot tests: **NOT RUN**. Course submission: **NOT RECORDED**.

Every task's test results section intentionally retains NOT RUN until actual ROS/hardware observations are supplied. These local results cannot be used as physical pass evidence.
