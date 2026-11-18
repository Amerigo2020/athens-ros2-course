"""Construct real ROS launch actions on the course VM, without opening serial.

Skipped on machines without ROS; this is not a hardware/integration test.
"""
import importlib.util
from pathlib import Path

import pytest

pytest.importorskip('launch')
pytest.importorskip('launch_ros')
from launch import LaunchContext
from launch_ros.actions import Node


def load_launch(name):
    path = Path(__file__).resolve().parents[1] / 'launch' / name
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize('start_slave,count', [('false', 2), ('true', 3)])
def test_combined_constructs_real_ros_actions(start_slave, count):
    module = load_launch('stm_serial_control_launch.py')
    context = LaunchContext()
    context.launch_configurations.update({
        'master_group_id': '7', 'slave_group_id': '2',
        'master_port': '/dev/a', 'slave_port': '/dev/b',
        'start_slave': start_slave, 'params_file': '/unused/config.yaml'})
    nodes = module.launch_nodes(context)
    assert len(nodes) == count
    assert all(isinstance(node, Node) for node in nodes)


def test_single_station_constructs_real_ros_action():
    module = load_launch('stm_serial_node_launch.py')
    context = LaunchContext()
    context.launch_configurations.update({'group_id': '7', 'port': '/dev/a',
                                          'params_file': '/unused/config.yaml'})
    nodes = module.launch_nodes(context)
    assert len(nodes) == 1 and isinstance(nodes[0], Node)
