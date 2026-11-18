# Jazzy setup and evidence workflow

Use Ubuntu 24.04 / ROS 2 Jazzy in the course VM, with USB passthrough enabled. Work from the team repository root; do not recreate packages over the existing ones. Our group is 7. Group 2 in examples is only a partner placeholder.

## Build and terminals

```bash
source /opt/ros/jazzy/setup.bash
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
PYTHONPATH=src/stm_station python3 -m pytest src/stm_station/test -q
```

In every new terminal: cd to this repository and source both setup files. Inspect `ls -l /dev/serial/by-id/` and substitute actual port paths. Configure serial access/dialout as required by the VM and reconnect the session after group changes. Only one bridge may open a device. Stop each D1 stage before starting the next because standard and custom message types must not coexist on the same topics.

Two custom bridges for standalone D2 tests (separate terminals):

```bash
ros2 run stm_station stm_serial_node --ros-args -r __ns:=/group_7 -p port:=/dev/ttyACM0
ros2 run stm_station stm_serial_node --ros-args -r __ns:=/group_2 -p port:=/dev/ttyACM1
```

Start exactly one standalone controller from the D2 task page, or stop these processes and use D3 combined launch instead. Direct ros2 run controller exposes /stm_setcontrol_type; D3 launch exposes /group_7/stm_setcontrol_type.

## Evidence capture

```bash
mkdir -p bags docs/D1.1
script -a docs/D1/D1.1/terminal.txt
# Run inspection commands; exit finishes this transcript shell.
git rev-parse HEAD
printenv ROS_DISTRO
lsb_release -ds
ros2 topic list -t
exit
```

Start the task's rosbag recorder in a separate prepared terminal BEFORE demonstrating movement. Use a fresh output directory per run; Ctrl+C closes it cleanly. Save `ros2 bag info bags/<run>` output as bag-info.txt in the task folder. Save rqt_graph screenshots and a short video that identifies the task, group and behavior. For D2, record kp/kd, encoder/velocity units, PWM limit, firmware and the exact mode-change commands alongside the bag (service events are not automatically captured by recording state topics).

Use the task's acceptance list for expected behavior. Include observed behavior, measured timing and any failures. Local math tests do not establish physical tracking, stability or motor stop performance. Host disconnect cannot guarantee a stop packet reaches firmware; verify its watchdog separately.

## Submit

Upload bags/large videos to the agreed course storage; verify lecturer access and paste URLs into each evidence section. Commit small logs, screenshots, configuration and completed results:

```bash
git add docs README.md
git commit -m "Record actual deliverable verification and hand-in evidence"
git push team HEAD:main
```

The team remote is named `team` in the original checkout. A fresh clone calls it `origin`; use `git remote -v` and push the team repository's configured remote. Record the actual submission date/location and any live demonstration. Keep implementation / tests / submission statuses separate.
