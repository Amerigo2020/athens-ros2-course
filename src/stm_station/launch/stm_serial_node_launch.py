# Course source: https://github.com/Robolabo/ROS_course
# Upstream revision: cf9e122904ebcb55d336aa7e82d0760bc94cbb07
# Template: Templates/stm_station_launch.py
# DONE marks code implementation, not a successful ROS/hardware test.
# Team launch/helper code adapts the listed course pattern; no separate numbered scaffold exists.
"""D3.1: one namespaced custom-interface serial bridge."""
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from stm_station.launch_settings import group_namespace


def launch_nodes(context):
    # ADAPTATION (original template comment): Read the group ID from the YAML file and build the namespace.
    # This launch uses the group_id launch argument; YAML supplies serial settings.
    group = group_namespace(LaunchConfiguration('group_id').perform(context))
    port = LaunchConfiguration('port').perform(context)
    if not port.strip():
        raise ValueError('A serial port is required')
    return [Node(package='stm_station', executable='stm_serial_node',
                 namespace=group, name='stm_serial_node', output='screen',
                 parameters=[LaunchConfiguration('params_file'),
                             {'port': ParameterValue(port, value_type=str)}])]


# Course launch pattern: return a LaunchDescription containing Node actions.
def generate_launch_description():
    config = os.path.join(get_package_share_directory('stm_station'),
                          'config', 'serial_params.yaml')
    return LaunchDescription([
        DeclareLaunchArgument('group_id', default_value='7', description='Our station group'),
        DeclareLaunchArgument('port', default_value='/dev/ttyACM0'),
        DeclareLaunchArgument('params_file', default_value=config),
        OpaqueFunction(function=launch_nodes),
    ])
