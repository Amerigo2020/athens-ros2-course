# Original course templates

Source: https://github.com/Robolabo/ROS_course/tree/cf9e122904ebcb55d336aa7e82d0760bc94cbb07/Templates

Revision: `cf9e122904ebcb55d336aa7e82d0760bc94cbb07`. Files in `templates/` were extracted directly from Git blobs in the local `Lab/ROS_course` checkout at this revision, not rewritten from the working tree. `SHA256.json` records each source path and SHA256. All 16 template files are retained byte-for-byte, including incomplete TODOs and syntax errors. No LICENSE file is present at this source revision; this archive attributes the course source and does not relicense it.

**These files are assignment scaffolding, not completed solutions.** Do not build/run the archive as submitted implementations. `COLCON_IGNORE` keeps it outside colcon package discovery. Runnable team implementations are in `src/`; [the assignment index](../docs/INDEX.md) maps each checkpoint to its template and solution.

Known differences resolved in team code:

- Templates use sample groups 1/2; our station is group 7.
- Template YAML uses `serial_port`/`baud_rate`; our bridge uses `port`/`baudrate`.
- The impedance template mixes `kv` and `kd`; our service consistently uses `kd`, matching the slides.
- Service naming varies between template (`set_control_type`) and slides (`stm_setcontrol_type`); team code uses the latter.
- D3 launch templates refer to a different control executable and future RViz assets. Team D3 launches only implemented executables.
- Dynamic group reconfiguration shown in the templates remains outside the current implementation: routing parameters are startup-only. Record this limitation in D2 evidence if assessed.
