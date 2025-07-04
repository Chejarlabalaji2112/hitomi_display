#testing
import os
import xacro
from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, SetEnvironmentVariable
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from pathlib import Path
def generate_launch_description():
    robot_name = "hitomi_quadruped"
    PACKAGE_NAME = "hitomi_display"

    world_arg = DeclareLaunchArgument(
        'world',
        default_value='maze2.sdf',
        description='Specify the world file for Gazebo (eg., empty.sdf)'
    )
    pkg_path = get_package_share_directory(PACKAGE_NAME)
    ign_resource_path = SetEnvironmentVariable(
        name='GZ_SIM_RESOURCE_PATH',
        value=[
            str(Path(pkg_path).parent.resolve()), ":",
             os.path.join(pkg_path, 'worlds'),
            ])

    
    world_file = LaunchConfiguration('world')


    robot_model_path = os.path.join(
        get_package_share_directory(PACKAGE_NAME),
        'urdf',
        'combined.urdf.xacro'
    )

    gz_bridge_param_path = os.path.join(
        get_package_share_directory(PACKAGE_NAME),
        'config',
        'gz_bridge.yaml')

    robot_description = xacro.process_file(robot_model_path).toxml()

    gazebo_pkg_launch = PythonLaunchDescriptionSource(
        os.path.join(
            get_package_share_directory('ros_gz_sim'),
            'launch',
            'gz_sim.launch.py'
        )
    )

    gazebo_launch = IncludeLaunchDescription(
        gazebo_pkg_launch,
        launch_arguments={
            'gz_args': [f'-r -v 4 ', world_file],
            'on_exit_shutdown': 'true'
        }.items()
    )

    spawn_model_gazebo_node = Node(
        package='ros_gz_sim',
        executable='create',
        arguments= [
            '-name', robot_name,
            '-string', robot_description,
            '-z','0.5',
            '-allow_renaming', 'false'
        ],
    )

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[
            {'robot_description': robot_description, 'use_sim_time': True}
        ],
        output = 'screen'
    )

    gz_bridge_node = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '--ros-args',
            '-p',
            f'config_file:={gz_bridge_param_path}'
        ],
        output = 'screen'
    )

    return LaunchDescription(
        [
            world_arg,
            ign_resource_path,
            gazebo_launch,
            spawn_model_gazebo_node,
            robot_state_publisher_node,
            gz_bridge_node,
            
        ]
    )
