"""D4 visualization, optional serial bridge and RViz, default Group 7."""
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from stm_station.launch_settings import group_namespace


def launch_nodes(context):
    def arg(name):
        return LaunchConfiguration(name).perform(context)

    group_id = int(arg('group_id'))
    group = group_namespace(group_id)
    nodes = [Node(package='stm_station', executable='stm_visualization_node',
                  namespace=group, name='stm_visualization_node', output='screen',
                  parameters=[LaunchConfiguration('params_file'), {'group_id': group_id}])]
    for flag in ('start_serial', 'start_rviz'):
        if arg(flag).lower() not in ('true', 'false'):
            raise ValueError(f'{flag} must be true or false')
    if arg('start_serial').lower() == 'true':
        if not arg('port').strip():
            raise ValueError('A serial port is required')
        nodes.append(Node(package='stm_station', executable='stm_serial_node',
                          namespace=group, name='stm_serial_node', output='screen',
                          parameters=[LaunchConfiguration('params_file'),
                              {'port': ParameterValue(arg('port'), value_type=str)}]))
    if arg('start_rviz').lower() == 'true':
        nodes.append(Node(package='rviz2', executable='rviz2', name='stm_rviz',
                          arguments=['-d', LaunchConfiguration('rviz_config')],
                          remappings=[('/group_7/stm_path', f'/{group}/stm_path')],
                          output='screen'))
    return nodes


def generate_launch_description():
    share = get_package_share_directory('stm_station')
    return LaunchDescription([
        DeclareLaunchArgument('group_id', default_value='7'),
        DeclareLaunchArgument('port', default_value='/dev/ttyACM0'),
        DeclareLaunchArgument('start_serial', default_value='true'),
        DeclareLaunchArgument('start_rviz', default_value='true'),
        DeclareLaunchArgument('params_file', default_value=os.path.join(share, 'config', 'serial_params.yaml')),
        DeclareLaunchArgument('rviz_config', default_value=os.path.join(share, 'rviz', 'stm_config.rviz')),
        OpaqueFunction(function=launch_nodes),
    ])
