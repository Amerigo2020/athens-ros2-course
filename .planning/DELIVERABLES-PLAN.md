# Deliverables implementation plan

Scope: user request for D3 plus a traceable archive of all course deliverables.
Environment: Group 7, Ubuntu 24.04 / ROS 2 Jazzy. Preserve original templates.

- [x] Read both PPTX assignments and verify template revision cf9e122904ebcb55d336aa7e82d0760bc94cbb07.
- [x] Add D1.1 standard publisher and D1.2 standard pub/sub entry points sharing the tested serial transport; keep D1.3 as the custom interface endpoint.
- [x] Add installed serial and combined launch files with group/port arguments and YAML settings. Validate distinct groups and positive IDs before launching.
- [x] Archive byte-identical upstream templates with revision and SHA256 manifest; exclude from colcon discovery.
- [x] Document every current assignment and additional older subpoint with source slides, commands, acceptance steps, test status and evidence placeholders.
- [x] Run local tests, syntax/package/document checks. Record ROS/hardware limitations explicitly. The verified changes are prepared for separate commit and push operations, recorded in Git history.

Verification focus: separate standard/custom topic types, no two bridges on one device, correct namespaced service commands, installed launch/config assets, accurate untested status, every slide mapping covered.
