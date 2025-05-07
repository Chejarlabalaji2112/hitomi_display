import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from pathlib import Path
from launch_ros.actions import Node

PACKAGE_NAME = "hitomi"

def generate_launch_description():

    world_arg = DeclareLaunchArgument(
        'world',
        default_value='maze2.sdf',
        description='Specify the world file for Gazebo (eg., empty.sdf)')
    
    gazebo_sim_path = PathJoinSubstitution([
        get_package_share_directory(PACKAGE_NAME), 'launch', 'gzx.launch.py'
    ])

    gazebo_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([gazebo_sim_path]),
        launch_arguments={'world': LaunchConfiguration('world')}.items()
    )

    slam_toolbox_launch_path = PathJoinSubstitution([
        get_package_share_directory("slam_toolbox"), 'launch', 'online_async_launch.py'

    ])

    slam_toolbox_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([slam_toolbox_launch_path]),
        launch_arguments={"use_sim_time": "true"}.items()
    )

    rviz_config_path = PathJoinSubstitution([
                get_package_share_directory(PACKAGE_NAME), 'rviz', 'slam.rviz'
            ])
    
    rviz2 = Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=['-d', rviz_config_path],
            parameters=[{'use_sim_time': True}]
        )
    
    return LaunchDescription([
        world_arg,
        gazebo_sim,
        slam_toolbox_launch,
        rviz2
    ])
    
