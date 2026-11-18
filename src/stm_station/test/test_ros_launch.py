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


@pytest.mark.parametrize('serial,rviz,count', [('false', 'false', 1),
                                              ('true', 'false', 2),
                                              ('true', 'true', 3)])
def test_visualization_constructs_real_ros_actions(serial, rviz, count):
    module = load_launch('stm_visualization_launch.py')
    context = LaunchContext()
    context.launch_configurations.update({
        'group_id': '7', 'port': '/dev/a', 'start_serial': serial,
        'start_rviz': rviz, 'params_file': '/unused/config.yaml',
        'rviz_config': '/unused/view.rviz'})
    nodes = module.launch_nodes(context)
    assert len(nodes) == count
    assert all(isinstance(node, Node) for node in nodes)


def test_bug0_constructs_one_namespaced_controller():
    module = load_launch('stm_bug0_launch.py')
    context = LaunchContext()
    context.launch_configurations.update({
        'group_id': '7', 'scan_topic': '/scan',
        'cmd_vel_topic': '/diff_drive_controller/cmd_vel',
        'use_sim_time': 'true', 'enable_stm': 'false',
        'params_file': '/unused/config.yaml'})
    nodes = module.launch_nodes(context)
    assert len(nodes) == 1 and isinstance(nodes[0], Node)
