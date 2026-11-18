# Course source: https://github.com/Robolabo/ROS_course
# Upstream revision: cf9e122904ebcb55d336aa7e82d0760bc94cbb07
# Template: Templates/stm_station_launch.py
# DONE marks code implementation, not a successful ROS/hardware test.
# Team launch/helper code adapts the listed course pattern; no separate numbered scaffold exists.
"""D3: master bridge and controller, with an optional local slave bridge."""
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from stm_station.launch_settings import group_namespace, validate_pair


def launch_nodes(context):
    def arg(name):
        return LaunchConfiguration(name).perform(context)

    # ADAPTATION (original template comment): Read the group ID from the YAML file and build the namespace.
    # Master/slave IDs are launch arguments; YAML supplies node settings.
    master, slave = arg('master_group_id'), arg('slave_group_id')
    flag = arg('start_slave').lower()
    if flag not in ('true', 'false'):
        raise ValueError('start_slave must be true or false')
    start_slave = flag == 'true'
    validate_pair(master, slave, arg('master_port'), arg('slave_port'), start_slave)

    def bridge(group, port):
        return Node(package='stm_station', executable='stm_serial_node',
                    namespace=group_namespace(group), name='stm_serial_node',
                    output='screen', parameters=[LaunchConfiguration('params_file'),
                        {'port': ParameterValue(port, value_type=str)}])

    nodes = [bridge(master, arg('master_port')),
             Node(package='stm_station', executable='stm_control_node',
                  namespace=group_namespace(master), name='stm_control_node',
                  output='screen', parameters=[LaunchConfiguration('params_file'),
                      {'master_group_id': int(master), 'slave_group_id': int(slave)}])]
    if start_slave:
        nodes.append(bridge(slave, arg('slave_port')))
    return nodes


# Course launch pattern: return a LaunchDescription containing Node actions.
def generate_launch_description():
    config = os.path.join(get_package_share_directory('stm_station'),
                          'config', 'serial_params.yaml')
    return LaunchDescription([
        DeclareLaunchArgument('master_group_id', default_value='7'),
        DeclareLaunchArgument('slave_group_id', description='Actual partner group; must differ'),
        DeclareLaunchArgument('master_port', default_value='/dev/ttyACM0'),
        DeclareLaunchArgument('slave_port', default_value='/dev/ttyACM1'),
        DeclareLaunchArgument('start_slave', default_value='false',
                              description='Start slave bridge on this machine too'),
        DeclareLaunchArgument('params_file', default_value=config),
        OpaqueFunction(function=launch_nodes),
    ])
