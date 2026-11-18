# Course deliverables - Group 7 / WinningLeos

[Repository README](../README.md) | [Step-by-step English walkthrough](WALKTHROUGH.md) | [Setup and evidence workflow](SETUP.md) | [Local validation](LOCAL-VALIDATION.md) | [Original templates](../reference/README.md) | [Deck provenance](COURSE-SOURCES.md)

The current assignment source is `Athens2026_ROS2.pptx`. The older `Athens_ROS2_Course.pptx` is also mapped to retain its additional subpoints. Slide numbers are PPTX slide numbers; overview slides are included where relevant. Original decks remain in the local course Material folder; they are not redistributed in this repository.

## Assignment map

| Task | Outcome | Current slides | Older slides | Implementation status |
| --- | --- | --- | --- | --- |
| [D1.1](D1/D1.md#d1-1) | STM state publisher with standard messages | 78 (D1 overview: 77) | 84 (overview: 83) | Implemented; unverified on ROS/hardware |
| [D1.2](D1/D1.md#d1-2) | STM publisher/subscriber with standard messages | 79 | 85 | Implemented; unverified on ROS/hardware |
| [D1.3](D1/D1.md#d1-3) | Custom STM interfaces | 80-81 | 86-87 | Implemented; unverified on ROS/hardware |
| [D2.1](D2/D2.md#d2-1) | Master/slave control node and service | 92-93 | 106-107; position diagram 109 | Implemented; unverified on ROS/hardware |
| [D2.2](D2/D2.md#d2-2) | Host position P control (starred extension) | 95 | 109 (position controller under D2.1) | Implemented; unverified on ROS/hardware |
| [D2.3](D2/D2.md#d2-3) | Host impedance PD control (starred extension) | 96-97 | 110-111 (D2.1.5 extra points) | Implemented; unverified on ROS/hardware |
| [D3.1.0](D3/D3.md#d3-1-0) | Single-station launch | 102 (combined D3 assignment) | 115 (D3.1.0) | Implemented; unverified on ROS/hardware |
| [D3.1.1](D3/D3.md#d3-1-1) | Install launch and configuration assets | 102 (combined D3 assignment) | 116 (D3.1.1) | Implemented; unverified on ROS/hardware |
| [D3.2](D3/D3.md#d3-2) | Combined serial/control launch | 102 (D3.1 in current slides) | 117 (D3.2) | Implemented; unverified on ROS/hardware |
| [D4.1](D4/D4.md#d4-1) | TF visualization of STM | 112 (D4.1) | 132 | Implemented/workflow available; ROS and hardware unverified |
| [D4.2](D4/D4.md#d4-2) | Plot and record visualization results | 112 (D4.2) | 132 (recording requirement) | Planned |
| [D5.1-simulation](D5/D5.md#d5-1-simulation) | Bug0 navigation in Gazebo | 125 | No equivalent Bug0 deliverable found | Planned |
| [D5.1-real](D5/D5.md#d5-1-real) | Bug0 on the real Galileo | 128 (also labelled D5.1) | No equivalent Bug0 deliverable found | Planned |
| [D5.2](D5/D5.md#d5-2) | STM controls simulated robot (starred extension) | 129; repeated as D5 at 133 | 143 (D5) | Planned |
| [D5-real-stm](D5/D5.md#d5-real-stm) | STM controls real robot (starred extension) | 130 (D5*) | No separate explicit real-STM deliverable found | Planned |

## Reading the numbering

- D1 is split into three independently runnable checkpoints. D1.1.1-1.1.4, D1.2.1-1.2.2 and D1.3.1-1.3.2 are listed in their task pages.
- D2.1.1/1.2 are the service and control node; older D2.1.5 maps to current D2.3. Current D2.2 and D2.3 are starred extensions. The same shared controller exposes direct-position, P and PD configurations; each needs its own test evidence.
- Current slide 102 calls combined launch D3.1; older slides split single launch (D3.1.0), packaging (D3.1.1), combined launch (D3.2). All three are covered here.
- D4.1 implements visualization; D4.2 collects/plots results.
- Current D5.1 is printed on both simulation (125) and real Bug0 (128), so the folders distinguish them. Current D5.2* (129) is repeated as D5 (133) and is equivalent to older D5 (143). Real STM control at 130 is another starred variant. These are not counted as duplicate completed work.

## Traceability and completion

D1/D1.md-D5/D5.md collect every subtask, its runbook, test results and evidence/submission record. The templates intentionally retain TODOs. D1 checkpoints were reconstructed now for clarity; no earlier hardware completion is asserted. D4 TF/RViz and plotting workflow are implemented but have no physical results yet. Code commits are recorded by Git; tested commit IDs must be filled in after real tests.

**No task is currently recorded as delivered or passed on hardware.** A push alone is not course acceptance. Run the documented checks, save results and evidence, and record the actual portal submission or live demonstration required by the lecturers.

## Screenshots and evidence files

Use the D1-D5 folders directly. Name every screenshot after its subtask and content, for example:

```text
deliverables/
  D1/
    D1.md
    D1.1_graph.png
    D1.2_terminal.png
    D1.3_custom_interfaces.png
  D2/
    D2.md
    D2.1_graph.png
    D2.2_position_plot.png
    D2.3_impedance_plot.png
  D3/
    D3.md
    D3.1.0_launch.png
    D3.1.1_installed_files.png
    D3.2_graph.png
  D4/
    D4.md
    D4.1_rviz.png
    D4.2_position_plot.png
  D5/
    D5.md
    D5.1-simulation_bug0.png
    D5.1-real_bug0.png
    D5.2_stm_control.png
```

The image names above are examples, not collected evidence. Add each real file/link to the matching evidence section of D1.md-D5.md and record observed test results. Use the same subtask prefix for transcripts, parameter dumps and bag-info files. Keep large bags/videos in the agreed submission storage and link them from the evidence section.
