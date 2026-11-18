# Course source: https://github.com/Robolabo/ROS_course
# Upstream revision: cf9e122904ebcb55d336aa7e82d0760bc94cbb07
# Template: Templates/13_bug0_lidar_stm.py
# Template: Templates/stm_station_launch.py
# DONE marks code implementation, not a successful ROS/hardware test.
# Team launch/helper code adapts the listed course pattern; no separate numbered scaffold exists.
"""D5.1 course controller, independent of simulator process startup."""
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
    for flag in ('enable_stm', 'use_sim_time'):
        if arg(flag).lower() not in ('true', 'false'):
            raise ValueError(f'{flag} must be true or false')
    if not arg('scan_topic').strip() or not arg('cmd_vel_topic').strip():
        raise ValueError('Scan and velocity topics must not be empty')
    return [Node(package='stm_station', executable='bug0_lidar_stm_node',
                 namespace=group_namespace(group_id), name='bug0_lidar_stm_node',
                 output='screen', parameters=[LaunchConfiguration('params_file'), {
                     'group_id': group_id,
                     'scan_topic': ParameterValue(arg('scan_topic'), value_type=str),
                     'cmd_vel_topic': ParameterValue(arg('cmd_vel_topic'), value_type=str),
                     'use_sim_time': arg('use_sim_time').lower() == 'true',
                     'enable_stm': arg('enable_stm').lower() == 'true'}])]


# Course launch pattern: return a LaunchDescription containing Node actions.
def generate_launch_description():
    share = get_package_share_directory('stm_station')
    return LaunchDescription([
        DeclareLaunchArgument('group_id', default_value='7'),
        DeclareLaunchArgument('scan_topic', default_value='/scan'),
        DeclareLaunchArgument('cmd_vel_topic', default_value='/diff_drive_controller/cmd_vel'),
        DeclareLaunchArgument('use_sim_time', default_value='true'),
        DeclareLaunchArgument('enable_stm', default_value='false'),
        DeclareLaunchArgument('params_file', default_value=os.path.join(share, 'config', 'bug0_params.yaml')),
        OpaqueFunction(function=launch_nodes),
    ])
