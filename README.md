# Athens ROS 2 - Team WinningLeos

Group 7, ATHENS 2026, UPM Madrid. We use Ubuntu 24.04 and ROS 2 Jazzy in the course VM.

## Deliverables

Work through the guides in order. Each one has the task, commands by terminal, expected behavior, stop commands and a table for our results. Screenshots go in the same folder as the guide.

| Task | Guide | Status |
| --- | --- | --- |
| D1 | [STM communication](deliverables/D1/D1.md) | Publisher, subscriber and custom-message stages implemented |
| D2 | [Master/slave control](deliverables/D2/D2.md) | Position and impedance modes implemented |
| D3 | [Launch files](deliverables/D3/D3.md) | Single and combined startup implemented |
| D4 | [RViz visualization](deliverables/D4/D4.md) | TF, trajectory and plots implemented |
| D5 | [Robot navigation](deliverables/D5/D5.md) | Bug0 simulation code implemented; real-robot tests and STM mapping open |

The code still needs testing in ROS, Gazebo and on the course hardware. Record what actually happens in the guide's test table before marking a task complete.

## Setup

Clone once, or use git pull in an existing checkout:

```bash
git clone https://github.com/Athens-ROS2-Course/Athens-ROS2-Team-WinningLeos.git
cd Athens-ROS2-Team-WinningLeos
```

From the repository root in Ubuntu:

```bash
source /opt/ros/jazzy/setup.bash
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
mkdir -p bags
ls -l /dev/serial/by-id/
```

In every new terminal, return to the repository and source both setup files. Use the actual USB device paths, and pass the STM devices through to the VM. Serial access may require membership in dialout and a new login session.

Our group is 7. Group 2 in the D2/D3 examples is only a partner placeholder: replace it with the real partner group. Run one bridge per USB device and one command publisher per station.

## Repository layout

```text
src/
  first_interfaces/   # Introductory message/service exercises
  first_package/      # Introductory ROS nodes
  stm_interfaces/     # STMState, STMControl, STMSetControlType
  stm_station/        # Nodes, launch files, configuration and tests
reference/templates/  # Original course exercises with TODOs
deliverables/
  D1/ ... D5/         # One guide per task, plus our screenshots/results
```

Configuration files are in src/stm_station/config. Group IDs and ports are launch arguments; the guides show the exact commands. Original templates are references, not finished solutions.

## Tests

The tests in src/stm_station/test check parsing, control calculations, motion estimation, Bug0 decisions and package assets:

```bash
PYTHONPATH=src/stm_station python3 -m pytest src/stm_station/test -q
```

On the ROS machine, also run:

```bash
colcon test --packages-select stm_station
colcon test-result --verbose
```

These checks do not replace the movement, stop and recording tests in D1-D5.

## Screenshots and submission

Use names such as deliverables/D1/D1.1_graph.png or deliverables/D4/D4.2_position_plot.png. Save actual gains, ports, units and the tested commit alongside the result. Start rosbag recording before the demonstration and stop it cleanly with Ctrl+C.

Keep screenshots and short logs in Git. Upload large bags/videos to the agreed course storage, check that the lecturers can access them, and put links in the matching guide. Record the required course upload or live demonstration separately from the code status.

## Course material

The task guides map the current Athens2026_ROS2.pptx and the older Athens_ROS2_Course.pptx to their slide numbers. Both decks remain in the course Material folder.

The [original ROS_course templates](reference/README.md) are attributed to their upstream revision. D5 uses the external Galileo simulator; its pinned setup and command interface are documented in [D5](deliverables/D5/D5.md#d5-1-simulation).
